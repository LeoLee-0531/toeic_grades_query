import sqlite3
from pathlib import Path

class GradeDatabase:
    def __init__(self):
        self.db_path = 'grades.db'
        self.init_db()

    def init_db(self):
        """初始化資料庫並導入資料"""
        try:
            # 如果資料庫不存在，則創建並導入資料
            if not Path(self.db_path).exists():
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                # 讀取並執行 SQL 檔案
                with open('grades.sql', 'r', encoding='utf-8') as sql_file:
                    sql_script = sql_file.read()
                    cursor.executescript(sql_script)
                
                conn.commit()
                conn.close()
                print("Database initialized successfully")
        except Exception as e:
            print(f"Error initializing database: {e}")
            raise

    def get_grades(self, student_id):
        """查詢學生成績"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT student_id, listening_score, reading_score, total_score 
                FROM grades 
                WHERE student_id = ?
            ''', (student_id,))
            
            result = cursor.fetchone()
            conn.close()

            if result:
                return {
                    'student_id': result[0],
                    'listening_score': result[1],
                    'reading_score': result[2],
                    'total_score': result[3]
                }
            return None

        except Exception as e:
            print(f"Error querying database: {e}")
            return None