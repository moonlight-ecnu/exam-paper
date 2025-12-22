from flask import Blueprint, request
bp = Blueprint('group', __name__, url_prefix='/group')

@bp.route('/create', methods=['POST'])
def create():
    """创建组"""
    pass

@bp.route('/dismiss', methods=['POST'])
def dismiss():
    """解散小组"""
    pass

