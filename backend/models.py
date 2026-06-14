"""数据库模型定义（SQLite）
PRD §9.3 核心数据表设计
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'data', 'english_train.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()

    # 用户表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            openid TEXT PRIMARY KEY,
            phone TEXT,
            level INTEGER DEFAULT 1,
            paid INTEGER DEFAULT 0,
            paid_expire_at TEXT,
            created_at TEXT DEFAULT (datetime('now'))
        )
    ''')

    # 句子表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sentences (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            difficulty TEXT CHECK(difficulty IN ('简单','中等','高考')),
            core_indices TEXT NOT NULL,
            tags TEXT,
            analysis TEXT,
            created_at TEXT DEFAULT (datetime('now'))
        )
    ''')

    # 训练记录表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS training_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            sentence_id INTEGER NOT NULL,
            training_mode TEXT CHECK(training_mode IN ('normal','targeted')),
            deleted_words TEXT NOT NULL,
            score_core_retention REAL,
            score_deletion_accuracy REAL,
            time_spent INTEGER,
            compression_index REAL,
            errors TEXT,
            error_tags TEXT,
            feedback_generated INTEGER DEFAULT 0,
            created_at TEXT DEFAULT (datetime('now'))
        )
    ''')

    # 反馈缓存表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedback_cache (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            training_record_id INTEGER NOT NULL,
            feedback_raw TEXT,
            weak_tags TEXT,
            is_praise INTEGER DEFAULT 0,
            is_template INTEGER DEFAULT 0,
            created_at TEXT DEFAULT (datetime('now')),
            expires_at TEXT
        )
    ''')

    # 支付订单表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            amount INTEGER,
            product TEXT,
            status TEXT CHECK(status IN ('待支付','已支付','已退款')),
            transaction_id TEXT,
            created_at TEXT DEFAULT (datetime('now'))
        )
    ''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print('数据库初始化完成')
