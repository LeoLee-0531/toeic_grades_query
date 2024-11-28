from flask import Flask, jsonify, request
from flask_cors import CORS
from database import GradeDatabase
import os

app = Flask(__name__)
CORS(app)  # 啟用 CORS 支援

# 初始化資料庫
db = GradeDatabase()


@app.route('/api/query', methods=['POST'])
def query():
    try:
        data = request.get_json()
        student_id = data.get('student_id')

        if not student_id:
            return jsonify({
                'success': False,
                'message': '請提供學號'
            }), 400

        grades = db.get_grades(student_id)

        if grades:
            return jsonify({
                'success': True,
                'data': grades
            })

        return jsonify({
            'success': False,
            'message': '找不到該學號的成績'
        }), 404

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'查詢失敗：{str(e)}'
        }), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
