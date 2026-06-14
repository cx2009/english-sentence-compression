from flask import Blueprint, request, jsonify
from models import get_db
import json

errors_bp = Blueprint('errors', __name__)


@errors_bp.route('/review', methods=['GET'])
def get_error_review():
    """按知识点聚合用户近期错题（PRD 模块六）"""
    user_id = request.args.get('user_id', 'anonymous')
    limit = request.args.get('limit', 20, type=int)

    db = get_db()
    cursor = db.cursor()

    # 查询近期有错误的训练记录
    cursor.execute('''
        SELECT tr.*, s.content, s.core_indices, s.tags
        FROM training_records tr
        JOIN sentences s ON tr.sentence_id = s.id
        WHERE tr.user_id = ?
          AND tr.error_tags IS NOT NULL
          AND tr.error_tags != '[]'
        ORDER BY tr.created_at DESC
        LIMIT ?
    ''', (user_id, limit))

    rows = cursor.fetchall()
    db.close()

    # 按知识点聚合
    tag_groups = {}
    for row in rows:
        r = dict(row)
        error_tags = json.loads(r['error_tags']) if r.get('error_tags') else []
        errors = json.loads(r['errors']) if r.get('errors') else []
        content = r['content']
        deleted_words = json.loads(r['deleted_words']) if r.get('deleted_words') else []

        for tag in error_tags:
            if tag not in tag_groups:
                tag_groups[tag] = []
            tag_groups[tag].append({
                'sentence': content,
                'error_type': 'missed_delete',
                'user_action': f"删除了 {len(deleted_words)} 个词",
                'correct_action': '参照标准压缩版本',
                'words': [e.get('word', '') for e in errors if 'word' in e],
            })

    # 按错误频率降序排列
    result = [
        {'tag': tag, 'count': len(items), 'errors': items}
        for tag, items in sorted(tag_groups.items(), key=lambda x: -len(x[1]))
    ][:5]  # Top 5

    return jsonify(result)
