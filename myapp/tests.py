from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Item

class ItemModelTest(TestCase):
    
    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.item = Item.objects.create(name='Test Item', user=self.user)

    # Test Case 1: Test the Item Model Fields
    def test_item_fields(self):
        self.assertEqual(self.item.name, 'Test Item')
        self.assertEqual(self.item.user.username, 'testuser')
    
    # Test Case 2: Test ListView URL and Template
    def test_item_list_view(self):
        response = self.client.get(reverse('item-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'myapp/item_list.html')  # Updated path
    
    # Test Case 3: Test DetailView URL and Content
    def test_item_detail_view(self):
        response = self.client.get(reverse('item-detail', args=[self.item.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'myapp/item_detail.html')  # Updated path
        self.assertContains(response, 'Test Item')

    # Test Case 5: Test Incorrect URL Handling
    def test_incorrect_url(self):
        response = self.client.get('/invalid-url/')
        self.assertEqual(response.status_code, 404)
