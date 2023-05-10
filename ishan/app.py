import os
from flask import Flask
from flask_restful import Api
from application.config import LocalDevelopmentConfig
from application.database import db
from flask_login import LoginManager


def create_app(app=None,api=None):
    app= Flask(__name__)

    if os.getenv('ENV',"development") == "production":
        raise Exception("No production config setup")
    else:
        print("Starting local development")
        app.config.from_object(LocalDevelopmentConfig)
    
    db.init_app(app) 
    api=Api(app)   
    app.app_context().push()


    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from application.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from application.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app,api

app,api = create_app()


if __name__=="__main__":
    app.run(host='0.0.0.0',port=8080)