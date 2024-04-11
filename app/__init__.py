from flask import Flask
from app.webhook.routes import webhook
from app.extensions import mongo

# Creating our flask app
def create_app():

    app = Flask(__name__, template_folder='template/')
    app.config["MONGO_URI"] = "mongodb://localhost:27017/webhookdb"
    mongo.init_app(app)

    # registering all the blueprints
    app.register_blueprint(webhook)
    return app,mongo

app = create_app()
