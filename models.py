from flask_sqlalchemy import SQLAlchemy
"""Models for Cupcake app."""
db = SQLAlchemy()

class Cupcake(db.Model):
    """Cupcake model."""

    __tablename__ = 'cupcakes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    flavor = db.Column(db.String(50), nullable=False)
    size = db.Column(db.String(50), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(200), nullable=False, default='https://tinyurl.com/demo-cupcake')

    def __repr__(self):
        return f'<Cupcake id={self.id} flavor={self.flavor} size={self.size} rating={self.rating}>'
    
    def serialize(self):
        """Serialize to dictionary."""

        return {
            'id': self.id,
            'flavor': self.flavor,
            'size': self.size,
            'rating': self.rating,
            'image': self.image
        }
