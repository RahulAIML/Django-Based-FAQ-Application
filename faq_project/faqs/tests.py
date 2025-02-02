from django.test import TestCase

# Create your tests here.
from rest_framework.test import APIClient
from .models import FAQ

class FAQTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.faq = FAQ.objects.create(question="What is Django?", answer="A Python-based web framework.")

    def test_faq_creation(self):
        faq = FAQ.objects.get(id=1)
        self.assertEqual(faq.question, "What is Django?")
        self.assertEqual(faq.answer, "A Python-based web framework.")

    def test_api_faqs(self):
        response = self.client.get('/api/faqs/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('question', response.data[0])
