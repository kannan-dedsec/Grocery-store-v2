import os
import logging

import globalConstants
import globalConstants as gc
from flask import Flask
from utils import redisUtil, DBUtil, JobsPool
from objects.Objects import ORM_BASE
from routes.routes import grocery_store_bp
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime

logs_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
os.makedirs(logs_folder, exist_ok=True)
celery_instance = None
def create_app():

    app = Flask(gc.GROCERY_STORE)

    app.config['JWT_SECRET_KEY'] = "dMSa01WnHfsEpmEExQz84QP2sh08IA"  # JSON web token configuration
    #app.config['JWT_TOKEN_LOCATION'] = ['cookies']
    #pp.config['JWT_COOKIE_SECURE'] = True
    #app.config['JWT_COOKIE_CSRF_PROTECT'] = False
    #app.config['PROPAGATE_EXCEPTIONS'] = True

    app.config['SQLALCHEMY_DATABASE_URI'] = gc.DATA_BASE_URI  #sql alchemy configuration

    app.config['REDIS_URL'] = gc.REDIS_URI   #redis and celery configuration
    app.config['REDIS_BACKEND_URL'] = gc.REDIS_BACKEND_URI
    app.config['REDIS_BROKER_URL'] = gc.REDIS_BROKER_URI

    celery_instance = JobsPool.celery
    celery_instance.Task = JobsPool.taskHandler


    log_formatter = logging.Formatter('%(asctime)s [%(levelname)s] - %(message)s') ## app logger

    log_handler = TimedRotatingFileHandler(os.path.join(logs_folder,f'grocery_store_logs_{datetime.now().strftime("%Y-%m-%d")}.log'), when='midnight',backupCount=5)
    log_handler.setFormatter(log_formatter)
    log_handler.setLevel(logging.INFO)
    app.logger.addHandler(log_handler)

    logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)  # sql logger
    sqlalchemy_log_handler = TimedRotatingFileHandler(os.path.join(logs_folder,f'sql_queries_{datetime.now().strftime("%Y-%m-%d")}.log'),when='midnight',backupCount=5)
    sqlalchemy_log_handler.setFormatter(log_formatter)
    sqlalchemy_log_handler.setLevel(logging.INFO)
    logging.getLogger('sqlalchemy.engine').addHandler(sqlalchemy_log_handler)

    CORS(app)  # to allow cross origing request

    JWTManager(app)

    app.register_blueprint(grocery_store_bp)
    ORM_BASE.init_app(app)
    redisUtil.redis.init_app(app)

    return app,celery_instance



if __name__ =='__main__':
    app, celery_instance = create_app()
    with app.app_context():
        ORM_BASE.create_all()
        if(DBUtil.getUser(gc.ADMIN_USERNAME) == None):
            userId = DBUtil.addUser(username=gc.ADMIN_USERNAME,password=gc.ADMIN_PASS,email=gc.ADMIN_EMAIL,role=gc.ADMIN)
            DBUtil.addStore("Grocery Store",userId)
    app.run(debug=True)
