from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import AccessLog

class AccessLogModelTest(TestCase):
    
    def setUp(self):
        self.access_log = AccessLog.objects.create(
            card_id="C1001",
            door_name="Main Entrance",
            access_granted=True
        )
    
    def test_access_log_creation(self):
        self.assertEqual(self.access_log.card_id, "C1001")
        self.assertEqual(self.access_log.door_name, "Main Entrance")
        self.assertTrue(self.access_log.access_granted)
        self.assertIsNotNone(self.access_log.timestamp)
    
    def test_access_log_str(self):
        expected = "C1001 - Main Entrance - GRANTED"
        self.assertEqual(str(self.access_log), expected)


class AccessLogAPITest(APITestCase):
    
    def setUp(self):
        self.access_log = AccessLog.objects.create(
            card_id="C1001",
            door_name="Main Entrance",
            access_granted=True
        )
        self.list_url = reverse('accesslog-list')
        self.detail_url = reverse('accesslog-detail', kwargs={'pk': self.access_log.pk})
    
    def test_create_access_log(self):
        data = {
            'card_id': 'C1002',
            'door_name': 'Back Door',
            'access_granted': False
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(AccessLog.objects.count(), 2)
        self.assertEqual(response.data['card_id'], 'C1002')
    
    def test_list_access_logs(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_retrieve_access_log(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['card_id'], 'C1001')
    
    def test_update_access_log(self):
        data = {
            'card_id': 'C1001',
            'door_name': 'Main Entrance Updated',
            'access_granted': False
        }
        response = self.client.put(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.access_log.refresh_from_db()
        self.assertEqual(self.access_log.door_name, 'Main Entrance Updated')
    
    def test_delete_access_log(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(AccessLog.objects.count(), 0)
    
    def test_filter_by_card_id(self):

        AccessLog.objects.create(
            card_id="C1002",
            door_name="Back Door",
            access_granted=False
        )
        response = self.client.get(self.list_url, {'card_id': 'C1001'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['card_id'], 'C1001')