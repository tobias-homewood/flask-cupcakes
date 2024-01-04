from flask import Flask, jsonify, request, render_template
from models import db, Cupcake, connect_db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SECRET_KEY'] = "oh-so-secret"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

with app.app_context():
    connect_db(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/cupcakes')
def get_cupcakes():
    cupcakes = db.session.query(Cupcake).all()
    serialized = [c.serialize() for c in cupcakes]
    return jsonify({'cupcakes': serialized})

@app.route('/api/cupcakes/<int:cupcake_id>')
def get_cupcake(cupcake_id):
    cupcake = db.session.query(Cupcake).get_or_404(cupcake_id)
    serialized = cupcake.serialize()
    return jsonify({'cupcake': serialized})

@app.route('/api/cupcakes', methods=['POST'])
def create_cupcake():
    data = request.json
    id = data.get('id')
    flavor = data.get('flavor')
    size = data.get('size')
    rating = data.get('rating')
    image = data.get('image')

    cupcake = Cupcake(id=id, flavor=flavor, size=size, rating=rating, image=image)
    db.session.add(cupcake)
    db.session.commit()
    serialized = cupcake.serialize()
    return (jsonify({'cupcake': serialized}), 201)

@app.route('/api/cupcakes/<int:cupcake_id>', methods=['PATCH'])
def update_cupcake(cupcake_id):
    data = request.json
    cupcake = db.session.query(Cupcake).get_or_404(cupcake_id)
    cupcake.flavor = data.get('flavor', cupcake.flavor)
    cupcake.size = data.get('size', cupcake.size)
    cupcake.rating = data.get('rating', cupcake.rating)
    cupcake.image = data.get('image', cupcake.image)
    db.session.commit()
    serialized = cupcake.serialize()
    return jsonify({'cupcake': serialized})

@app.route('/api/cupcakes/<int:cupcake_id>', methods=['DELETE'])
def delete_cupcake(cupcake_id):
    cupcake = db.session.query(Cupcake).get_or_404(cupcake_id)
    db.session.delete(cupcake)
    db.session.commit()
    return jsonify({'message': 'deleted'})