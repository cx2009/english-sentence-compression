from flask import Blueprint, request, jsonify
from models import get_db

user_bp = Blueprint('user', __name__)


@user_bp.route('/login', methods=['POST'])
def login():
    """微信静默授权登录"""
    data = request.json
    code = data.get('code')

    # TODO: 调用微信接口 code2session 换取 openid
    # url = f'https://api.weixin.qq.com/sns/jscode2session?appid={APPID}&secret={SECRET}&js_code={code}&grant_type=authorization_code'

    # Mock: 测试用 openid
    openid = f'mock_openid_{hash(code) % 10000}'

    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE openid=?", (openid,))
    user = cursor.fetchone()

    if not user:
        cursor.execute("INSERT INTO users (openid) VALUES (?)", (openid,))
        db.commit()

    db.close()
    return jsonify({'openid': openid})


@user_bp.route('/profile', methods=['GET'])
def get_profile():
    """获取用户信息"""
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': '需要 user_id'}), 400

    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE openid=?", (user_id,))
    user = cursor.fetchone()
    db.close()

    if not user:
        return jsonify({'error': '用户不存在'}), 404

    return jsonify(dict(user))
