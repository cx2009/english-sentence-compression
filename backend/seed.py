"""句子题库管理工具

用法：
  python seed.py                    # 初始化种子数据
  python seed.py --validate         # 验证句子数据完整性
  python seed.py --import data.json # 从外部 JSON 文件导入
  python seed.py --stats            # 统计句子库状态
"""
from models import init_db, get_db
import json
import sys
import os

SENTENCES = [
    {
        "content": "The boy who was running in the park yesterday suddenly stopped because he saw something strange.",
        "difficulty": "中等",
        "core_indices": [0, 1, 5, 6, 8, 9],
        "tags": ["定语从句", "状语从句", "介词短语", "时间状语"],
        "analysis": {"subject": "The boy", "predicate": "stopped", "modifiers": ["who was running in the park", "yesterday", "because he saw something strange"]}
    },
    {
        "content": "The book that I bought yesterday is very interesting.",
        "difficulty": "简单",
        "core_indices": [0, 1, 5, 6, 7],
        "tags": ["定语从句", "时间状语"],
        "analysis": {"subject": "The book", "predicate": "is", "modifiers": ["that I bought yesterday"]}
    },
    {
        "content": "Students who study hard usually get good grades.",
        "difficulty": "简单",
        "core_indices": [0, 2, 4, 5, 6],
        "tags": ["定语从句"],
        "analysis": {"subject": "Students", "predicate": "get", "modifiers": ["who study hard"]}
    },
    {
        "content": "He arrived at the airport in the morning but the flight had already left.",
        "difficulty": "简单",
        "core_indices": [0, 1, 5, 7, 8, 9, 10],
        "tags": ["介词短语", "时间状语"],
        "analysis": {"subject": "He", "predicate": "arrived", "modifiers": ["at the airport", "in the morning", "but the flight had already left"]}
    },
    {
        "content": "Although it was raining heavily, the children continued to play outside.",
        "difficulty": "中等",
        "core_indices": [1, 4, 5, 6, 7, 8],
        "tags": ["状语从句"],
        "analysis": {"subject": "the children", "predicate": "continued", "modifiers": ["Although it was raining heavily"]}
    },
    {
        "content": "The woman who lives next door is a famous doctor.",
        "difficulty": "简单",
        "core_indices": [0, 1, 5, 6, 7, 8],
        "tags": ["定语从句"],
        "analysis": {"subject": "The woman", "predicate": "is", "modifiers": ["who lives next door"]}
    },
    {
        "content": "He looked after his sick mother for three years.",
        "difficulty": "中等",
        "core_indices": [0, 1, 2, 3, 4, 6, 7],
        "tags": ["短语动词", "介词短语"],
        "analysis": {"subject": "He", "predicate": "looked after", "modifiers": ["for three years"]}
    },
    {
        "content": "The experiment conducted by the scientists in the laboratory last month proved the theory.",
        "difficulty": "高考",
        "core_indices": [0, 1, 7, 8, 9],
        "tags": ["介词短语", "时间状语", "非谓语动词"],
        "analysis": {"subject": "The experiment", "predicate": "proved", "modifiers": ["conducted by the scientists", "in the laboratory", "last month"]}
    },
    {
        "content": "If you work hard, you will succeed in the end.",
        "difficulty": "简单",
        "core_indices": [1, 2, 3, 4, 5, 6, 7],
        "tags": ["状语从句"],
        "analysis": {"subject": "you", "predicate": "will succeed", "modifiers": ["If you work hard", "in the end"]}
    },
    {
        "content": "Having finished his homework, the boy went out to play with his friends.",
        "difficulty": "中等",
        "core_indices": [3, 4, 5, 8, 9, 10, 11],
        "tags": ["非谓语动词", "介词短语"],
        "analysis": {"subject": "the boy", "predicate": "went out", "modifiers": ["Having finished his homework", "to play with his friends"]}
    },
    {
        "content": "The factory where his father works is located in the southern part of the city.",
        "difficulty": "高考",
        "core_indices": [0, 1, 5, 6, 7, 8],
        "tags": ["定语从句", "介词短语"],
        "analysis": {"subject": "The factory", "predicate": "is located", "modifiers": ["where his father works", "in the southern part of the city"]}
    },
    {
        "content": "She gave up her job to take care of her children.",
        "difficulty": "简单",
        "core_indices": [0, 1, 2, 3, 4, 5, 6],
        "tags": ["短语动词"],
        "analysis": {"subject": "She", "predicate": "gave up", "modifiers": ["to take care of her children"]}
    },
    {
        "content": "The information that he provided in his report was very useful for our research.",
        "difficulty": "高考",
        "core_indices": [0, 1, 5, 6, 7, 8, 9],
        "tags": ["定语从句", "介词短语"],
        "analysis": {"subject": "The information", "predicate": "was", "modifiers": ["that he provided in his report"]}
    },
    {
        "content": "Walking along the beach, she found a beautiful shell.",
        "difficulty": "中等",
        "core_indices": [5, 6, 7, 8],
        "tags": ["非谓语动词", "介词短语"],
        "analysis": {"subject": "she", "predicate": "found", "modifiers": ["Walking along the beach"]}
    },
    {
        "content": "The man standing at the door is my uncle who came from Shanghai.",
        "difficulty": "高考",
        "core_indices": [0, 1, 5, 6, 7, 8, 9],
        "tags": ["非谓语动词", "定语从句", "介词短语"],
        "analysis": {"subject": "The man", "predicate": "is", "modifiers": ["standing at the door", "who came from Shanghai"]}
    },
    {
        "content": "Because he was late for school, the teacher punished him.",
        "difficulty": "简单",
        "core_indices": [4, 5, 6, 7],
        "tags": ["状语从句"],
        "analysis": {"subject": "the teacher", "predicate": "punished", "modifiers": ["Because he was late for school"]}
    },
    {
        "content": "The children playing in the garden are having a great time.",
        "difficulty": "中等",
        "core_indices": [0, 5, 6, 7, 8, 9],
        "tags": ["非谓语动词", "介词短语"],
        "analysis": {"subject": "The children", "predicate": "are having", "modifiers": ["playing in the garden"]}
    },
    {
        "content": "A new hospital will be built in this area next year.",
        "difficulty": "中等",
        "core_indices": [0, 1, 2, 3, 4, 5],
        "tags": ["介词短语", "时间状语"],
        "analysis": {"subject": "A new hospital", "predicate": "will be built", "modifiers": ["in this area", "next year"]}
    },
    {
        "content": "The reason why he was absent is that he was ill.",
        "difficulty": "中等",
        "core_indices": [0, 1, 4, 5, 6, 7, 8],
        "tags": ["定语从句"],
        "analysis": {"subject": "The reason", "predicate": "is", "modifiers": ["why he was absent", "that he was ill"]}
    },
    {
        "content": "Putting out the fire quickly saved the whole building.",
        "difficulty": "高考",
        "core_indices": [4, 5, 6, 7, 8],
        "tags": ["短语动词", "非谓语动词"],
        "analysis": {"subject": "Putting out the fire quickly", "predicate": "saved", "modifiers": []}
    },
]


def validate_sentence(s: dict) -> list[str]:
    """验证单条句子标注的合法性，返回错误列表"""
    errors = []
    words = s['content'].split(' ')

    # 必填字段
    for field in ['content', 'difficulty', 'core_indices', 'tags']:
        if field not in s:
            errors.append(f'缺少必填字段: {field}')

    # 难度分级
    if s.get('difficulty') not in ('简单', '中等', '高考'):
        errors.append(f"difficulty 必须是'简单'/'中等'/'高考'，当前: {s.get('difficulty')}")

    # core_indices 不越界
    for idx in s.get('core_indices', []):
        if idx < 0 or idx >= len(words):
            errors.append(f'core_indices 索引 {idx} 越界（总词数 {len(words)}）')

    # core_indices 至少保留 2 个词（主谓）
    if len(s.get('core_indices', [])) < 2:
        errors.append(f'core_indices 至少保留 2 个词（主语+谓语），当前仅 {len(s.get("core_indices", []))} 个')

    # core_indices 不能包含所有词（全部保留等于没压缩）
    if len(s.get('core_indices', [])) >= len(words):
        errors.append(f'core_indices 包含了所有词（{len(words)} 个），无法作为压缩训练')

    # tags 非空
    if not s.get('tags'):
        errors.append('tags 不能为空，至少标注一个知识点标签')

    return errors


def validate_all(sentences: list[dict]) -> int:
    """验证所有句子，返回错误数"""
    total_errors = 0
    for i, s in enumerate(sentences):
        errs = validate_sentence(s)
        if errs:
            total_errors += len(errs)
            print(f'  ❌ 句子 #{i + 1} ({s.get("content", "")[:30]}...):')
            for e in errs:
                print(f'     - {e}')
    return total_errors


def import_from_json(filepath: str) -> int:
    """从外部 JSON 文件导入句子（追加模式）"""
    if not os.path.exists(filepath):
        print(f'文件不存在: {filepath}')
        return 0

    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    if isinstance(data, dict):
        data = data.get('sentences', [data])
    if not isinstance(data, list):
        print('JSON 格式错误：应为数组或包含 sentences 字段的对象')
        return 0

    # 验证
    print(f'验证 {len(data)} 条句子...')
    err_count = validate_all(data)
    if err_count > 0:
        print(f'发现 {err_count} 个错误，导入中止')
        return 0

    # 导入
    db = get_db()
    cursor = db.cursor()
    imported = 0
    for s in data:
        cursor.execute(
            "INSERT INTO sentences (content, difficulty, core_indices, tags, analysis) VALUES (?, ?, ?, ?, ?)",
            (s['content'], s['difficulty'],
             json.dumps(s['core_indices'], ensure_ascii=False),
             json.dumps(s['tags'], ensure_ascii=False),
             json.dumps(s.get('analysis', {}), ensure_ascii=False))
        )
        imported += 1

    db.commit()
    db.close()
    print(f'成功导入 {imported} 条句子')
    return imported


def show_stats():
    """显示句子库统计信息"""
    db = get_db()
    cursor = db.cursor()

    total = cursor.execute("SELECT COUNT(*) FROM sentences").fetchone()[0]
    by_difficulty = cursor.execute(
        "SELECT difficulty, COUNT(*) FROM sentences GROUP BY difficulty"
    ).fetchall()
    all_tags = cursor.execute("SELECT tags FROM sentences").fetchall()

    # 统计知识点标签频率
    tag_counts = {}
    for row in all_tags:
        tags = json.loads(row['tags']) if row['tags'] else []
        for tag in tags:
            tag_counts[tag] = tag_counts.get(tag, 0) + 1

    db.close()

    print(f'📊 句子库统计')
    print(f'  总计: {total} 句')
    for d, c in by_difficulty:
        print(f'  {d}: {c} 句')
    print(f'  知识点分布:')
    for tag, count in sorted(tag_counts.items(), key=lambda x: -x[1]):
        print(f'    {tag}: {count} 句')


def seed():
    """初始化种子数据（清空后重新导入）"""
    init_db()
    db = get_db()
    cursor = db.cursor()

    print(f'验证 {len(SENTENCES)} 条种子句子...')
    err_count = validate_all(SENTENCES)
    if err_count > 0:
        print(f'⚠ 种子数据存在 {err_count} 个错误，仍将继续导入')

    cursor.execute("DELETE FROM sentences")
    for s in SENTENCES:
        cursor.execute(
            "INSERT INTO sentences (content, difficulty, core_indices, tags, analysis) VALUES (?, ?, ?, ?, ?)",
            (s['content'], s['difficulty'],
             json.dumps(s['core_indices'], ensure_ascii=False),
             json.dumps(s['tags'], ensure_ascii=False),
             json.dumps(s['analysis'], ensure_ascii=False))
        )

    db.commit()
    count = cursor.execute("SELECT COUNT(*) FROM sentences").fetchone()[0]
    db.close()
    print(f'✅ 种子数据初始化完成，共 {count} 条句子')
    show_stats()


if __name__ == '__main__':
    if '--validate' in sys.argv:
        print('验证种子数据...')
        err_count = validate_all(SENTENCES)
        if err_count == 0:
            print('✅ 所有句子验证通过')
        else:
            print(f'❌ 发现 {err_count} 个错误')

    elif '--import' in sys.argv:
        idx = sys.argv.index('--import')
        if idx + 1 < len(sys.argv):
            import_from_json(sys.argv[idx + 1])
        else:
            print('请指定 JSON 文件路径')

    elif '--stats' in sys.argv:
        show_stats()

    else:
        seed()
