import unittest
from app import app

class AdminRoutes(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()
    
    def test_coach_application_details(self):
        coach_id = 4

        response = self.client.get(f"/admin/coach-applications/{coach_id}")
        