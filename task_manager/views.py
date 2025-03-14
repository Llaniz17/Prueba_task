from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from .models import Task
from .forms import TaskForm
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
import requests
from django.conf import settings
from .serializers import TaskSerializer

class TaskViewSet(viewsets.ModelViewSet):
    #pylint: disable=E1101
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    @action(detail=True, methods=['get'])
    def weather(self, request, pk=None):
        task = self.get_object()
    
        if not task.city:
            return Response({"error": "No se ha especificado una ciudad para esta tarea"}, status=400)

        API_KEY = settings.WEATHER_API_KEY # Reemplázalo con tu apikey
        url = f"https://api.openweathermap.org/data/2.5/weather?q={task.city}&appid={API_KEY}"

        try:
            response = requests.get(url, timeout=5) 
            #response.raise_for_status()  # Lanza un error si el código es 4xx o 5xx

            data = response.json()
            return Response({
                "city": task.city,
                "temperature": data["main"]["temp"],
                "humidity": data["main"]["humidity"],
                "weather": data["weather"][0]["description"],
            })
    
    #validaciones de posibles eerrores
        except requests.exceptions.ConnectionError:
            return Response({"error": "No se pudo conectar con la API de OpenWeatherMap."}, status=503)

        except requests.exceptions.HTTPError:
            return Response({"error": "Ciudad no encontrada"}, status=response.status_code)

        except requests.exceptions.RequestException:
            return Response({"error": "Error inesperado al obtener los datos del clima."}, status=500)

class TaskListView(ListView):
    model = Task
    template_name = 'tasks/list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        completed_filter = self.request.GET.get('completed')
        if completed_filter == 'true':
            #pylint: disable=E1101
            return Task.objects.filter(completed=True)    
        elif completed_filter == 'false':
            #pylint: disable=E1101
            return Task.objects.filter(completed=False)
        #pylint: disable=E1101
        return Task.objects.all()

class TaskDetailView(DetailView):
    model = Task
    template_name = 'tasks/detail.html'
    context_object_name = 'task'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task = self.get_object()
        context["form"] = kwargs.get("form", TaskForm(instance=task)) 

        # Obtener clima desde API interna creada con DRF
        if task.city:
            api_url = f"http://127.0.0.1:8000/api/tasks/{task.pk}/weather/"
            try:
                response = requests.get(api_url, timeout=5)
                data = response.json()

                if response.status_code == 200:
                    context["weather"] = {
                        "temperature": round(data["temperature"] - 273.15), # se le resta 273.15 para convertir de Kelvin a Celsius, siguiendo la formula
                        "humidity": data["humidity"],
                        "description": data["weather"].capitalize(),
                    }
                else:
                    context["weather_error"] = data.get("error", "Ciudad no encontrada.")
            except requests.exceptions.RequestException:
                context["weather_error"] = "API no disponible"

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        task = self.object
        form = TaskForm(request.POST, instance=self.object)  

        
        # Eliminar
        if "delete_task" in request.POST:
            task.delete()
            return redirect('task_list')

        # Marcar o desmcarcar como completada
        if "toggle_completed" in request.POST:
            task.completed = not task.completed
            task.save()
            return redirect('task_detail', pk=task.pk)
        
        if form.is_valid():
            form.save()  # Guardar cambios
            return redirect('task_detail', pk=self.object.pk)
        
        return self.render_to_response(self.get_context_data(form=form))

def create_task(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    
    return render(request, 'tasks/task_form.html', {'form': form})

def mark_task_completed(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if request.method == "POST":
        task.completed = True
        task.save()
        return redirect('task_detail', pk=task.pk)

    return HttpResponse("Método no permitido", status=405)
