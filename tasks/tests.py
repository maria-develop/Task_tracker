from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from tasks.models import Task, Employee, Manager, ParentTask
from users.models import User


class TaskTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="test88@mail.ru")
        self.employee = Employee.objects.create(
            full_name="Ершов Г.Г.", department="Самозанятый"
        )
        self.task = Task.objects.create(
            title="Раздел 2 ПД",
            start_date="2024-12-30",
            end_date="2025-02-20",
            is_important=True,
            employee=Employee.objects.get(pk=self.employee.id),
        )
        self.client.force_authenticate(user=self.user)

    def test_task_retrieve(self):
        url = reverse("tasks:task_retrieve", args=(self.task.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["title"], self.task.title)

    def test_task_retrieve_unauthenticated(self):
        url = reverse("tasks:task_retrieve", args=(self.task.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_task_retrieve_authenticated(self):
        url = reverse("tasks:task_retrieve", args=(self.task.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_task_create(self):
        url = reverse("tasks:task_create")
        data = {
            "title": "Раздел 3 ПД",
            "start_date": "2024-12-30",
            "end_date": "2025-02-20",
            "employee": self.employee.id,
            "limit_time": "30",  # Добавьте, если поле обязательно
        }
        response = self.client.post(url, data)
        print(response.data)  # Для отладки
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.all().count(), 2)

    def test_task_create_invalid(self):
        url = reverse("tasks:task_create")
        data = {"title": "", "start_date": "2024-12-30", "end_date": "2025-02-20"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("title", response.data)

    def test_task_update(self):
        url = reverse("tasks:task_update", args=(self.task.pk,))
        data = {"title": "Task3"}
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["title"], "Task3")

    def test_task_destroy(self):
        url = reverse("tasks:task_delete", args=(self.task.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.all().count(), 0)

    def test_task_list(self):
        url = reverse("tasks:task_list")
        response = self.client.get(url)
        data = response.json()
        result = {
            "id": self.task.pk,
            "title": "Раздел 2 ПД",
            "start_date": "2024-12-30",
            "end_date": "2025-02-20",
            "status": "not_started",
            "comments": None,
            "is_active": True,
            "is_important": True,
            "parent_task": None,
            "employee": self.task.employee.id,
            "completion_days": 52,  # Добавьте это поле
            "limit_time": "",  # Добавьте это поле, если оно есть в ответе
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(result, data["results"])
