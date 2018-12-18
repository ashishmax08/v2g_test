from django.urls import path
from todo_app import views

urlpatterns = [
	path('task',views.Task.as_view()),
	path('task/filter',views.FilterTask.as_view())
]