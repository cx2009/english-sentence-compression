"""LLM 智能反馈服务
PRD §4 模块五：LLM 智能反馈引擎
"""

import json
import time
import os
from models import get_db

# 降级模板：按知识点标签匹配预设反馈文案
FALLBACK_TEMPLATES = {
    '定语从句': {
        'feedback': '你漏删了定语从句部分。定语从句修饰名词，在阅读压缩时通常可以整体删除，只保留被修饰的名词即可。',
        'review': '建议复习：定语从句的基本结构（关系代词 who/which/that 引导的从句），练习识别从句的边界。'
    },
    '状语从句': {
        'feedback': '状语从句中的逻辑连接词（because, although, unless, if等）应该保留，它们是句子逻辑关系的骨架。其余从句内容可以压缩。',
        'review': '建议复习：状语从句的连接词分类，区分"必须保留的逻辑连接词"和"可压缩的从句内容"。'
    },
    '介词短语': {
        'feedback': '介词短语（in the park, at school, on Monday等）是典型的可压缩信息。阅读时只需知道主干，时间地点细节可以跳过。',
        'review': '建议复习：常见介词的用法，练习识别句子中的介词短语边界。'
    },
    '时间状语': {
        'feedback': '时间状语（yesterday, last week, in 2020等）在阅读压缩时通常可以删除，除非时间信息是句子的核心逻辑。',
        'review': '建议练习：快速识别句子中的时间表达，判断其是否为核心信息。'
    },
    '短语动词': {
        'feedback': '短语动词（look after, give up, put up with等）应该整体保留，不能拆开。其中的介词/副词是动词的一部分，不是独立的修饰语。',
        'review': '建议复习：常见短语动词列表，注意区分"短语动词+介词短语"的边界。'
    },
    '非谓语动词': {
        'feedback': '非谓语动词（doing, to do, done）的识别需要结合上下文。作定语或状语的非谓语通常可以压缩，作主语或宾语时必须保留。',
        'review': '建议复习：非谓语动词的三种形式及其在句子中的成分功能。'
    },
}

# 默认反馈
DEFAULT_FEEDBACK = {
    'feedback': '你在阅读压缩训练中还有一些干扰词没有完全识别。建议多练习"找主干-删干扰"的阅读方法，先抓住句子的主谓宾，再判断其他成分是否可以删除。',
    'review': '建议从简单句子开始，逐步建立"主干优先"的阅读习惯。'
}


def generate_feedback(training_record_id: int, user_id: str) -> dict:
    """
    生成 LLM 反馈（含降级逻辑）

    Args:
        training_record_id: 训练记录 ID
        user_id: 用户 ID

    Returns:
        dict: 与 LLM 输出结构一致的反馈数据
    """
    # 先查缓存
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "SELECT * FROM feedback_cache WHERE training_record_id=? AND user_id=?",
        (training_record_id, user_id)
    )
    cached = cursor.fetchone()
    if cached:
        db.close()
        return json.loads(cached['feedback_raw'])

    # 获取训练记录
    cursor.execute("SELECT * FROM training_records WHERE id=?", (training_record_id,))
    record = cursor.fetchone()
    if not record:
        db.close()
        return _generate_template_feedback({'error_tags': []})

    error_tags = json.loads(record['error_tags']) if record['error_tags'] else []
    errors = json.loads(record['errors']) if record['errors'] else []

    # 获取句子信息
    cursor.execute("SELECT content, tags FROM sentences WHERE id=?", (record['sentence_id'],))
    sentence = cursor.fetchone()
    db.close()

    try:
        # 尝试调用 LLM API
        return _call_llm_api(sentence, record, errors, error_tags, user_id)
    except Exception as e:
        # LLM 失败，降级到规则模板
        print(f'LLM API 调用失败: {e}, 使用降级模板')
        return _generate_template_feedback(error_tags)


def _call_llm_api(sentence, record, errors, error_tags, user_id):
    """调用 LLM API（需配置 API Key）"""
    import requests

    # API 配置（从环境变量读取）
    api_key = os.environ.get('LLM_API_KEY', '')
    api_url = os.environ.get('LLM_API_URL', 'https://api.deepseek.com/v1/chat/completions')

    if not api_key:
        raise ValueError('LLM_API_KEY 未配置')

    # 组装结构化 Prompt
    sentence_tags = json.loads(sentence['tags']) if sentence and sentence['tags'] else []
    prompt = {
        'model': 'deepseek-chat',
        'messages': [
            {'role': 'system', 'content': '你是一个英语阅读压缩训练的教学助手。根据用户的训练数据，分析薄弱知识点，给出具体的反馈和复习建议。以JSON格式返回。'},
            {'role': 'user', 'content': json.dumps({
                'sentence': sentence['content'] if sentence else '',
                'user_deleted': json.loads(record['deleted_words']),
                'errors': errors,
                'sentence_tags': sentence_tags,
                'history_weak_tags': error_tags,
            }, ensure_ascii=False)}
        ],
        'response_format': {'type': 'json_object'},
        'temperature': 0.3,
        'max_tokens': 500,
        'timeout': 5,
    }

    resp = requests.post(api_url, json=prompt, headers={
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
    }, timeout=5)

    if resp.status_code != 200:
        raise ValueError(f'LLM API 返回错误: {resp.status_code}')

    result = resp.json()
    feedback = json.loads(result['choices'][0]['message']['content'])

    # 写入缓存
    _cache_feedback(user_id, record['id'], feedback, error_tags, is_template=False)
    return feedback


def _generate_template_feedback(error_tags: list) -> dict:
    """降级：按错误标签生成模板反馈"""
    weak_points = []
    for tag in error_tags[:3]:  # 最多取前3个
        template = FALLBACK_TEMPLATES.get(tag, DEFAULT_FEEDBACK)
        weak_points.append({
            'tag': tag,
            'severity': 'medium',
            'feedback': template['feedback'],
            'is_praise': False,
        })

    if not weak_points:
        weak_points.append({
            'tag': '基础识别',
            'severity': 'low',
            'feedback': '做得不错！继续保持训练，你的阅读压缩能力会越来越强。',
            'is_praise': True,
        })

    review_suggestions = [FALLBACK_TEMPLATES.get(t, DEFAULT_FEEDBACK)['review'] for t in error_tags[:2]]

    feedback = {
        'weak_points': weak_points,
        'overall_assessment': f'你的薄弱知识点集中在：{"、".join(error_tags[:3])}。建议重点加强这些方向的练习。',
        'review_suggestion': '；'.join(review_suggestions) if review_suggestions else DEFAULT_FEEDBACK['review'],
        'next_focus': error_tags[0] if error_tags else '综合训练',
    }

    # 缓存模板生成的反馈
    _cache_feedback('anonymous', 0, feedback, error_tags, is_template=True)
    return feedback


def _cache_feedback(user_id: str, record_id: int, feedback: dict, weak_tags: list, is_template: bool):
    """写入反馈缓存"""
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            INSERT INTO feedback_cache
            (user_id, training_record_id, feedback_raw, weak_tags, is_praise, is_template, expires_at)
            VALUES (?, ?, ?, ?, ?, ?, datetime('now', '+7 days'))
        ''', (
            user_id, record_id,
            json.dumps(feedback, ensure_ascii=False),
            json.dumps(weak_tags, ensure_ascii=False),
            1 if all(w.get('is_praise') for w in feedback['weak_points']) else 0,
            1 if is_template else 0,
        ))
        db.commit()
        db.close()
    except Exception as e:
        print(f'缓存写入失败: {e}')
