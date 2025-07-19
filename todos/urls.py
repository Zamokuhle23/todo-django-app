# todos/urls.py
from django.urls import path
from .views import TodoItemViewSet, index
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'todos', TodoItemViewSet)

urlpatterns = [
    path('', index),  # main frontend
]

urlpatterns += router.urls
