"""种子数据：初始化句子题库"""
from models import init_db, get_db
import json

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


def seed():
    init_db()
    db = get_db()
    cursor = db.cursor()

    # 清空旧数据
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
    print(f'种子数据初始化完成，共 {count} 条句子')


if __name__ == '__main__':
    seed()
