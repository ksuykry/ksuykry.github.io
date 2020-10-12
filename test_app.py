from unittest import TestCase
from app import app
app.config['TESTING'] = True
class ConvertTester(TestCase):
    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True
    
    def test_homepage(self):
        with self.client as client:
            response = client.get('/currency')
            # test that you're getting a template
            html = response.get_data(as_text=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn('<form action="/changed"', html)
    def test_convert(self):
        with self.client as client:
            #check to see if USD and USD with amount 1 comes to $1
            #check to see if an error is created when 
            data = dict(convertingf = "WHY", convertingt = "GPU", amount ="10i")
            response = client.post('/changed', data=data, follow_redirects=True)
            self.assertIn('Not a valid code: WHY',response.get_data(as_text=True))
            self.assertIn('Not a valid code: GPU',response.get_data(as_text=True))
            self.assertIn('Not a valid amount',response.get_data(as_text=True))

            