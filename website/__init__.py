from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME= "database.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY']="helloworld"
    app.config['SQLALCHEMY_DATABASE_URI']=f'sqlite:///{DB_NAME}'
    db.init_app(app)
    
    from .views import views
    from .auth import auth
    
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")
    
    from .models import User
    
    create_database(app)
    
    #login manager enables to access to pages user logged in
    login_manager =  LoginManager()
    #if user want to access page and they are not logged in it will redirect
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)
    
    #function for login manager to find the user model when it is loggedin, it allow to access to the database given the id of the user, session
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    
    
    return app


def create_database(app):
    if not path.exists("website/"+ DB_NAME):
        with app.app_context():
            db.create_all()
        print("Created database!")