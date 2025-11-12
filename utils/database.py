import sqlite3
import datetime
from PyQt6.QtGui import QColor

class DatabaseManager:
    def __init__(self):
        self.conn = sqlite3.connect('paint_history.db')
        self.create_tables()

    def create_tables(self):
        """Создает таблицы в базе данных"""
        cursor = self.conn.cursor()
        
        # Таблица сессий рисования
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS drawing_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                start_time TEXT NOT NULL,
                end_time TEXT,
                tools_used TEXT
            )
        ''')
        
        # Таблица действий
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS drawing_actions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id INTEGER,
                tool_name TEXT NOT NULL,
                color TEXT NOT NULL,
                brush_size INTEGER,
                timestamp TEXT NOT NULL,
                FOREIGN KEY (session_id) REFERENCES drawing_sessions (id)
            )
        ''')
        
        self.conn.commit()

    def start_session(self):
        """Начинает новую сессию рисования"""
        cursor = self.conn.cursor()
        start_time = datetime.datetime.now().isoformat()
        cursor.execute(
            'INSERT INTO drawing_sessions (start_time) VALUES (?)',
            (start_time,)
        )
        self.conn.commit()
        return cursor.lastrowid

    def log_action(self, session_id, tool_name, color, brush_size):
        """Логирует действие рисования"""
        cursor = self.conn.cursor()
        timestamp = datetime.datetime.now().isoformat()
        
        # Конвертируем QColor в строку
        color_str = f"{color.red()},{color.green()},{color.blue()}"
        
        cursor.execute(
            '''INSERT INTO drawing_actions 
               (session_id, tool_name, color, brush_size, timestamp) 
               VALUES (?, ?, ?, ?, ?)''',
            (session_id, tool_name, color_str, brush_size, timestamp)
        )
        self.conn.commit()

    def end_session(self, session_id):
        """Завершает сессию рисования"""
        cursor = self.conn.cursor()
        end_time = datetime.datetime.now().isoformat()
        cursor.execute(
            'UPDATE drawing_sessions SET end_time = ? WHERE id = ?',
            (end_time, session_id)
        )
        self.conn.commit()

    def get_session_stats(self, session_id):
        """Получает статистику по сессии"""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT tool_name, COUNT(*) as usage_count 
            FROM drawing_actions 
            WHERE session_id = ? 
            GROUP BY tool_name
        ''', (session_id,))
        return cursor.fetchall()

    def close(self):
        """Закрывает соединение с БД"""
        self.conn.close()
