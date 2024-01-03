from flask import Flask, jsonify
from models import db, Cupcake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['FLASK_DEBUG'] = True
db.init_app(app)

# Rest of your Flask app code goes here...
@app.route('/')
def home():
    return 'the api is running!'

@app.route('/api/cupcakes')
def get_cupcakes():
    cupcakes = db.session.query(Cupcake).all()
    serialized = [c.serialize() for c in cupcakes]
    return jsonify(serialized)