from unittest import TestCase

from app import app
from models import db, Cupcake, connect_db

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True



CUPCAKE_DATA = {
    "flavor": "TestFlavor",
    "size": "TestSize",
    "rating": 5,
    "image": "http://test.com/cupcake.jpg"
}

CUPCAKE_DATA_2 = {
    "flavor": "TestFlavor2",
    "size": "TestSize2",
    "rating": 10,
    "image": "http://test.com/cupcake2.jpg"
}


class TestCupcakeViews(TestCase):
    """Tests for views of API."""

    def setUp(self):
        """Make demo data."""
        with app.app_context():
            Cupcake.query.delete()
            db.session.commit()

    def tearDown(self):
        """Clean up fouled transactions."""
        with app.app_context():
            db.session.rollback()

    def test_list_cupcakes(self):
        with app.test_client() as client:
            with app.app_context():
                cupcake = Cupcake(flavor="TestFlavor", size="TestSize", rating=5, image="http://test.com/cupcake.jpg")
                db.session.add(cupcake)
                db.session.commit()

                url = f"/api/cupcakes"
                resp = client.get(url)

                data = resp.json

                self.assertIn({
                            "id": cupcake.id,
                            "flavor": cupcake.flavor,
                            "size": cupcake.size,
                            "rating": cupcake.rating,
                            "image": cupcake.image
                        }, data['cupcakes'])

    def test_get_cupcake(self):
        with app.test_client() as client:
            with app.app_context():
                cupcake = Cupcake(flavor="TestFlavor", size="TestSize", rating=5, image="http://test.com/cupcake.jpg")
                db.session.add(cupcake)
                db.session.commit()

                url = f"/api/cupcakes/{cupcake.id}"
                resp = client.get(url)

            self.assertEqual(resp.status_code, 200)
            data = resp.json
            self.assertEqual(data, {
                "cupcake": {
                    "id": cupcake.id,
                    "flavor": "TestFlavor",
                    "size": "TestSize",
                    "rating": 5,
                    "image": "http://test.com/cupcake.jpg"
                }
            })

    def test_create_cupcake(self):
        with app.test_client() as client:
            url = "/api/cupcakes"
            resp = client.post(url, json=CUPCAKE_DATA_2)

            self.assertEqual(resp.status_code, 201)

            data = resp.json

            # don't know what ID we'll get, make sure it's an int & normalize
            self.assertIsInstance(data['cupcake']['id'], int)
            del data['cupcake']['id']

            self.assertEqual(data, {
                "cupcake": {
                    "flavor": "TestFlavor2",
                    "size": "TestSize2",
                    "rating": 10,
                    "image": "http://test.com/cupcake2.jpg"
                }
            })

            self.assertEqual(Cupcake.query.count(), 1)