from flask import Blueprint, request, jsonify
from models import get_db
from services.llm_service import generate_feedback
import json

feedback_bp = Blueprint('feedback', __name__)


@feedback_bp.route('/<int:record_id>', methods=['GET'])
def get_feedback(record_id):
    """获取 LLM 反馈"""
    user_id = request.args.get('user_id', 'anonymous')

    # 生成反馈（含缓存逻辑）
    feedback = generate_feedback(record_id, user_id)
    return jsonify(feedback)
