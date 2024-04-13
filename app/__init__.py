import os
from flask import Flask
from app.webhook.routes import webhook
from app.extensions import mongo
from dotenv import load_dotenv

load_dotenv()

# Creating our flask app
def create_app():

    app = Flask(__name__, template_folder='template/')
    app.config["MONGO_URI"] = os.getenv('MONGO_URI')
    mongo.init_app(app)

    # registering all the blueprints
    app.register_blueprint(webhook)
    return app,mongo

app = create_app()
