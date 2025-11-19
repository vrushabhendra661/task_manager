from django.contrib import admin
from django.urls import path, include
from tasks.views import dashboard_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('tasks.urls')),
    path('', dashboard_view, name='dashboard'),  # Add this line for the root URL
]