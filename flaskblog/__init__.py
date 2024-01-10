from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flaskblog.config import Config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'users.login_page'
login_manager.login_message_category = 'info'


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    login_manager.init_app(app)

    from flaskblog.main.routes import main
    from flaskblog.users.routes import users
    from flaskblog.market.routes import market
    from flaskblog.purchases.routes import purchases
    from flaskblog.errors.handlers import errors

    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(market)
    app.register_blueprint(purchases)
    app.register_blueprint(errors)

    return app
