from .views import TaskListView, TaskDetailView, create_task, mark_task_completed
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet

router = DefaultRouter()
router.register(r'tasks', TaskViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('tasks/', TaskListView.as_view(), name='task_list'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task_detail'),
    path('tasks/create/', create_task, name='create_task'),
    path('tasks/<int:pk>/complete/', mark_task_completed, name='mark_task_completed'),
]
