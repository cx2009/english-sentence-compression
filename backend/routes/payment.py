from flask import Blueprint, request, jsonify
from models import get_db
import json

payment_bp = Blueprint('payment', __name__)


@payment_bp.route('/create-order', methods=['POST'])
def create_order():
    """创建支付订单"""
    data = request.json
    user_id = data.get('user_id')
    product = data.get('product', '7day')

    if not user_id:
        return jsonify({'error': '需要 user_id'}), 400

    # 定价
    prices = {'7day': 2900, '21day': 9900}  # 单位：分
    amount = prices.get(product, 2900)

    # TODO: 调用微信支付统一下单 API
    # 需要微信商户号、API 密钥等配置

    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO orders (user_id, amount, product, status) VALUES (?, ?, ?, ?)",
        (user_id, amount, product, '待支付')
    )
    db.commit()
    order_id = cursor.lastrowid
    db.close()

    # Mock prepay_id
    return jsonify({
        'order_id': str(order_id),
        'prepay_id': f'mock_prepay_{order_id}',
    })


@payment_bp.route('/callback', methods=['POST'])
def pay_callback():
    """微信支付回调通知"""
    # TODO: 验证微信回调签名
    data = request.get_data(as_text=True)
    # 解析 XML，更新订单状态
    # ...

    return 'SUCCESS', 200


@payment_bp.route('/check-order', methods=['GET'])
def check_order():
    """前端轮询订单状态"""
    order_id = request.args.get('order_id')
    if not order_id:
        return jsonify({'error': '需要 order_id'}), 400

    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT status FROM orders WHERE id=?", (order_id,))
    order = cursor.fetchone()
    db.close()

    if not order:
        return jsonify({'error': '订单不存在'}), 404

    return jsonify({'status': order['status']})
