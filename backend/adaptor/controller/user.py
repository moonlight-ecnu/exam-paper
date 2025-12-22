from flask import Blueprint, request

bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route('/register', methods=['POST'])
def register():
    """用户注册"""

@bp.route('/login', methods=['POST'])
def login():
    """用户登录"""

