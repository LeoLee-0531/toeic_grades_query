from flask import Flask, jsonify, request
from flask_cors import CORS
from database import GradeDatabase
import os

app = Flask(__name__)

# 啟用 CORS，允許來自指定來源的請求
CORS(app, resources={
     r"/*": {"origins": "https://leolee-0531.github.io"}}, supports_credentials=True)

# 初始化資料庫
db = GradeDatabase()


@app.route('/')
def home():
    return "Welcome to the TOEIC Grades Query API!"


@app.route('/api/query', methods=['POST', 'OPTIONS'])
def query():
    if request.method == 'OPTIONS':
        # 處理預檢請求，返回 200 狀態碼
        return jsonify({'success': True}), 200

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
    # 默認使用 5000，但 Heroku 會提供 PORT
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
