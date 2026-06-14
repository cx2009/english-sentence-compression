from flask import Blueprint, request, jsonify
import json
from models import get_db

training_bp = Blueprint('training', __name__)


@training_bp.route('/sentence', methods=['GET'])
def get_sentence():
    """获取训练句子（支持 normal / targeted 模式）"""
    mode = request.args.get('mode', 'normal')
    tag = request.args.get('tag')

    db = get_db()
    cursor = db.cursor()

    if mode == 'targeted' and tag:
        # 针对性训练：从指定知识点的句子中随机抽取
        cursor.execute(
            "SELECT * FROM sentences WHERE tags LIKE ? ORDER BY RANDOM() LIMIT 1",
            (f'%{tag}%',)
        )
    else:
        # 正常训练：按顺序取
        cursor.execute("SELECT * FROM sentences ORDER BY RANDOM() LIMIT 1")

    row = cursor.fetchone()
    db.close()

    if not row:
        return jsonify({'error': '没有更多句子'}), 404

    sentence = dict(row)
    sentence['core_indices'] = json.loads(sentence['core_indices'])
    if sentence.get('tags'):
        sentence['tags'] = json.loads(sentence['tags'])
    if sentence.get('analysis'):
        sentence['analysis'] = json.loads(sentence['analysis'])

    return jsonify(sentence)


@training_bp.route('/submit', methods=['POST'])
def submit_training():
    """提交训练结果"""
    data = request.json
    user_id = data.get('user_id', 'anonymous')
    sentence_id = data['sentence_id']
    deleted_words = data['deleted_words']
    time_spent = data['time_spent']
    training_mode = data.get('training_mode', 'normal')

    # 获取句子标准答案
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM sentences WHERE id=?", (sentence_id,))
    sentence = cursor.fetchone()

    if not sentence:
        return jsonify({'error': '句子不存在'}), 404

    sentence_dict = dict(sentence)
    core_indices = json.loads(sentence_dict['core_indices'])
    content = sentence_dict['content']
    total_words = len(content.split(' '))

    # 计算评分
    from services.scoring import calculate_full_scores
    scores = calculate_full_scores(core_indices, deleted_words, total_words, time_spent)

    # 提取错误关联的知识点标签
    error_tags = []
    if scores['falsely_deleted'] or scores['missed_deletions']:
        tags_raw = sentence_dict.get('tags')
        tags = json.loads(tags_raw) if tags_raw else []
        error_tags = tags  # 简化：有错误就把句子的标签都记上

    # 保存训练记录
    cursor.execute('''
        INSERT INTO training_records
        (user_id, sentence_id, training_mode, deleted_words,
         score_core_retention, score_deletion_accuracy, time_spent,
         compression_index, errors, error_tags)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        user_id, sentence_id, training_mode,
        json.dumps(deleted_words),
        scores['core_retention'], scores['deletion_accuracy'], time_spent,
        scores['compression_index'],
        json.dumps(scores['errors'], ensure_ascii=False),
        json.dumps(error_tags, ensure_ascii=False)
    ))
    db.commit()
    record_id = cursor.lastrowid
    db.close()

    return jsonify({
        'record_id': record_id,
        'scores': {
            'core_retention': scores['core_retention'],
            'deletion_accuracy': scores['deletion_accuracy'],
            'compression_index': scores['compression_index'],
        },
        'errors': scores['errors'],
    })


@training_bp.route('/daily', methods=['GET'])
def get_daily():
    """获取今日训练列表"""
    user_id = request.args.get('user_id', 'anonymous')
    db = get_db()
    cursor = db.cursor()

    # 获取今日已完成句子ID
    cursor.execute(
        "SELECT sentence_id FROM training_records WHERE user_id=? AND date(created_at)=date('now')",
        (user_id,)
    )
    completed = [row['sentence_id'] for row in cursor.fetchall()]

    # 获取未完成的句子（取3句）
    if completed:
        placeholders = ','.join('?' * len(completed))
        cursor.execute(
            f"SELECT * FROM sentences WHERE id NOT IN ({placeholders}) ORDER BY RANDOM() LIMIT 3",
            completed
        )
    else:
        cursor.execute("SELECT * FROM sentences ORDER BY RANDOM() LIMIT 3")

    sentences = []
    for row in cursor.fetchall():
        s = dict(row)
        s['core_indices'] = json.loads(s['core_indices'])
        if s.get('tags'):
            s['tags'] = json.loads(s['tags'])
        sentences.append(s)

    db.close()
    return jsonify({'sentences': sentences, 'completed': completed})


@training_bp.route('/targeted', methods=['GET'])
def get_targeted():
    """获取针对性训练句子"""
    tag = request.args.get('tag')
    if not tag:
        return jsonify({'error': '需要指定知识点标签'}), 400

    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "SELECT * FROM sentences WHERE tags LIKE ? ORDER BY RANDOM() LIMIT 3",
        (f'%{tag}%',)
    )
    sentences = []
    for row in cursor.fetchall():
        s = dict(row)
        s['core_indices'] = json.loads(s['core_indices'])
        if s.get('tags'):
            s['tags'] = json.loads(s['tags'])
        sentences.append(s)

    db.close()
    return jsonify(sentences)
