from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch
from .models import Task
from .forms import TaskForm

class TaskModelTest(TestCase):
    def test_create_task(self):
        """Prueba que una tarea se cree correctamente """
        #pylint: disable=E1101 Agregar esta linea antes del task.objects por si sale error, normalmente el pylint lo detecta como error pero no lo es
        task = Task.objects.create(
            title="Prueba",
            description="Esta es una tarea de prueba",
            city="Cucuta"
        )
        self.assertEqual(task.title, "Prueba")
        self.assertFalse(task.completed)  
        self.assertIsNotNone(task.created_at)  

class TaskFormTest(TestCase):
    def test_form_validation(self):
        """Prueba que el formulario valide correctamente el título de la tarea"""
        form = TaskForm(data={'title': '', 'description': 'Sin titulo'})
        self.assertFalse(form.is_valid())  
        self.assertIn('title', form.errors)  

class TaskCompletionTest(TestCase):
    def setUp(self):
        """Crea una tarea para usar en las pruebas"""
        self.task = Task.objects.create(title="Prueba")

    def test_mark_task_completed(self):
        """Prueba que una tarea puede marcarse como completada"""
        self.task.completed = True
        self.task.save()
        self.task.refresh_from_db()
        self.assertTrue(self.task.completed) 

class TaskAPITest(TestCase):
    def setUp(self):
        """Crea una tarea para probar la API"""
        self.task = Task.objects.create(title="Tarea para API", city="Cucuta")

    def test_api_get_task_list(self):
        """Prueba que la API devuelve la lista de tareas"""
        response = self.client.get(reverse('task-list'))  # Endpoint api/tasks/
        self.assertEqual(response.status_code, 200)
        self.assertIn("Tarea para API", response.content.decode())

    def test_api_get_task_detail(self):
        """Prueba que la API devuelve los detalles de una tarea"""
        response = self.client.get(reverse('task-detail', args=[self.task.id]))
        self.assertEqual(response.status_code, 200)
        self.assertIn("Tarea para API", response.content.decode())

class WeatherAPITest(TestCase):
    def setUp(self):
        """Crea una tarea con ciudad para probar la API de clima"""
        self.task = Task.objects.create(title="Tarea con ciudad", city="Bogota")

    @patch("requests.get")
    def test_get_weather(self, mock_get):
        """Prueba que se obtiene el clima desde la API externa"""

        # Simulación de respuesta de la api
        mock_response = {
            "main": {"temp": 10.5, "humidity": 95},
            "weather": [{"description": "inundación"}]
        }
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        #  Cambio la URL para que use el endpoint correcto /api/tasks/id/weather/
        response = self.client.get(reverse('task-weather', args=[self.task.id]))

        self.assertEqual(response.status_code, 200)
        self.assertIn("inundación", response.content.decode())

