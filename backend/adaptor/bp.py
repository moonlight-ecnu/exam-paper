from backend.adaptor.controller import user, group


def register_bp(app):
    app.register_blueprint(group.bp)
    app.register_blueprint(user.bp)
