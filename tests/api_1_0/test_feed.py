from unittest import TestCase
import json
from app import create_app,db
from app.models import Feed

class Test(TestCase):
    def setUp(self):
        self.app = create_app('default')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all(bind=['news_test'])
        Feed.generate_fake(50)
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_feed(self):
        response=self.client.get("/get_feed/8")
        json_response = json.loads(response.data.decode('utf-8'))
        print("==================the response is======================\n",json_response)
        self.assertTrue(json_response['has_more'])
