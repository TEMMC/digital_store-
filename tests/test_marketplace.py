import os, re, tempfile, unittest
from pathlib import Path

_TMP = tempfile.TemporaryDirectory()
os.environ["DATABASE_URL"] = "sqlite:///" + str(Path(_TMP.name) / "test.db")
os.environ["UPLOAD_FOLDER"] = str(Path(_TMP.name) / "uploads")
os.environ["SECRET_KEY"] = "test-only-secret"

import app as marketplace

class MarketplaceSmokeTests(unittest.TestCase):
    def setUp(self):
        marketplace.app.config.update(TESTING=True, WTF_CSRF_ENABLED=False)
        with marketplace.app.app_context():
            marketplace.db.drop_all()
            marketplace.db.create_all()
        self.client = marketplace.app.test_client()

    def token(self, page):
        response = self.client.get(page)
        self.assertEqual(response.status_code, 200, response.data[:500])
        match = re.search(rb'name="_csrf_token" value="([^"]+)"', response.data)
        self.assertIsNotNone(match, "CSRF token missing from form")
        return match.group(1).decode()

    def register_and_login(self, role="buyer", username="tester"):
        token = self.token("/register")
        response = self.client.post("/register", data={
            "_csrf_token": token, "username": username,
            "email": username + "@example.test", "password": "StrongPass123",
            "role": role
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        token = self.token("/login")
        response = self.client.post("/login", data={
            "_csrf_token": token, "username": username,
            "password": "StrongPass123"
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_catalog_and_health(self):
        self.assertEqual(self.client.get("/").status_code, 200)
        self.assertEqual(self.client.get("/health").json["status"], "ok")
        self.assertEqual(self.client.get("/api/v1/status").json["status"], "online")

    def test_registration_role_is_limited_and_login(self):
        self.register_and_login(role="admin", username="publicuser")
        with self.client.session_transaction() as sess:
            self.assertEqual(sess["role"], "buyer")

    def test_seller_can_publish_and_edit(self):
        self.register_and_login(role="seller", username="creator")
        with marketplace.app.app_context():
            product = marketplace.Product(name="Demo Asset", description="A test product",
                price=0, is_free=1, category="Apps", seller="creator",
                file_path="https://example.test/demo.zip", approved=1)
            marketplace.db.session.add(product)
            marketplace.db.session.commit()
            product_id = product.id
        self.assertEqual(self.client.get("/dashboard").status_code, 200)
        self.assertEqual(self.client.get(f"/edit/{product_id}").status_code, 200)
        self.assertEqual(self.client.get(f"/product/{product_id}").status_code, 200)

    def test_favorites_and_reviews(self):
        self.register_and_login(username="buyer")
        with marketplace.app.app_context():
            product = marketplace.Product(name="Free Tool", category="Apps",
                seller="creator", file_path="https://example.test/tool.zip",
                is_free=1, approved=1)
            marketplace.db.session.add(product)
            marketplace.db.session.commit()
            product_id = product.id
        token = self.token(f"/product/{product_id}")
        self.assertEqual(self.client.post(f"/favorite/{product_id}",
            data={"_csrf_token": token}, follow_redirects=True).status_code, 200)
        self.assertEqual(self.client.get("/favorites").status_code, 200)
        token = self.token(f"/product/{product_id}")
        self.assertEqual(self.client.post(f"/review/{product_id}",
            data={"_csrf_token": token, "rating": "5", "comment": "Excellent"},
            follow_redirects=True).status_code, 200)
        with marketplace.app.app_context():
            saved = marketplace.db.session.get(marketplace.Product, product_id)
            self.assertEqual(saved.rating_count, 1)
            self.assertEqual(saved.rating, 5.0)

    def test_post_without_csrf_is_rejected(self):
        response = self.client.post("/login", data={"username": "x", "password": "y"})
        self.assertEqual(response.status_code, 400)


    def test_social_feed_and_about(self):
        self.register_and_login(username="socialuser")
        token = self.token("/feed")
        response = self.client.post("/feed", data={"_csrf_token": token, "body": "Hello MT community!"}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Hello MT community!", response.data)
        self.assertEqual(self.client.get("/about").status_code, 200)
        self.assertIn(b"Tinotenda Enock Mapfumo", self.client.get("/about").data)

    def test_direct_messages_and_group_membership(self):
        self.register_and_login(username="sender")
        with marketplace.app.app_context():
            recipient = marketplace.User(username="receiver", email="receiver@example.test",
                password=marketplace.generate_password_hash("StrongPass123"), role="buyer")
            marketplace.db.session.add(recipient)
            marketplace.db.session.commit()
            recipient_id = recipient.id
        token = self.token(f"/messages/{recipient_id}")
        response = self.client.post(f"/messages/{recipient_id}",
            data={"_csrf_token": token, "body": "Hello from MT"},
            follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Hello from MT", response.data)
        token = self.token("/mt-group")
        response = self.client.post("/mt-group",
            data={"_csrf_token": token, "action": "join"}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        token = self.token("/mt-group")
        response = self.client.post("/mt-group",
            data={"_csrf_token": token, "action": "send", "body": "Hello MT Group"},
            follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Hello MT Group", response.data)

    def test_call_request_is_recorded_without_claiming_live_call(self):
        self.register_and_login(username="caller")
        with marketplace.app.app_context():
            recipient = marketplace.User(username="callee", email="callee@example.test",
                password=marketplace.generate_password_hash("StrongPass123"), role="buyer")
            marketplace.db.session.add(recipient)
            marketplace.db.session.commit()
            recipient_id = recipient.id
        token = self.token(f"/messages/{recipient_id}")
        response = self.client.post(f"/call/{recipient_id}",
            data={"_csrf_token": token, "call_type": "video"}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        with marketplace.app.app_context():
            self.assertEqual(marketplace.CallRequest.query.count(), 1)

if __name__ == "__main__":
    unittest.main()
