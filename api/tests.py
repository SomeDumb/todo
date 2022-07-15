from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from .models import CustomUser


class RegistationTestCase(APITestCase):
    
    def test_registration(self):
        data = {"username":"username", "password":"password", "email":"someemail@mail.ru"}
        response = self.client.post("/api/register/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
class CreateAndDeleteTaskListCase(APITestCase):
    
    def setUp(self):
        self.user = CustomUser.objects.create_user(username="user", \
            password="pass", email="email@email.ru")
        data = {"username":"user", "password":"pass"}
        response = self.client.post('/api/token/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
    
    def create_task(self):
        data = {"header":"header", "text":"text", "deadline":"2023-03-04T13:01"}
        response = self.client.post("/api/create_task", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task_id = response.data['task']['id']
    
    def delete_task(self):
        response = self.client.delete(f"/api/delete_task/{self.task_id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    def get_tasks(self):
        response = self.client.get("/api/get_list")
        self.assertEqual(response.status_code, (status.HTTP_200_OK or status.HTTP_204_NO_CONTENT))
        print(response.content)
    
    def test_delete_get(self):
        self.create_task()
        print("Created!")
        self.get_tasks()
        
        self.delete_task()
        print("Deleted!")
        self.get_tasks()
        
class CheckTaskCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username="user", \
            password="pass", email="email@email.ru")
        data = {"username":"user", "password":"pass"}
        response = self.client.post('/api/token/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
    
    def create_task(self):
        print("Created!")
        data = {"header":"header", "text":"text", "deadline":"2023-03-04T13:01"}
        response = self.client.post("/api/create_task", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task_id = response.data['task']['id']
        print(response.content)
    
    def check_task(self):
        print("Checked!")
        response = self.client.patch(f"/api/check_task/{self.task_id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.content)
    
    def test_create_and_check(self):
        self.create_task()
        self.check_task()