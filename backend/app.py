from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)

    # 注册路由
    from routes.training import training_bp
    from routes.user import user_bp
    from routes.feedback import feedback_bp
    from routes.payment import payment_bp
    from routes.errors import errors_bp

    app.register_blueprint(training_bp, url_prefix='/api/train')
    app.register_blueprint(user_bp, url_prefix='/api/user')
    app.register_blueprint(feedback_bp, url_prefix='/api/feedback')
    app.register_blueprint(payment_bp, url_prefix='/api/pay')
    app.register_blueprint(errors_bp, url_prefix='/api/errors')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
