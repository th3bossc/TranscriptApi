from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from flask_cors import CORS
db = SQLAlchemy()

SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['UPLOAD_FOLDER'] = 'transcript_api/common/files/'
    db.init_app(app)

    from transcript_api.resources.routes import resources
    app.register_blueprint(resources)

    from transcript_api.main.routes import main
    app.register_blueprint(main)

    return app