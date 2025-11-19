import requests
from django.conf import settings
from django.db.models import Count, Q
from django.utils import timezone
from django.shortcuts import render
from datetime import timedelta
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Task, TaskActivity
from .serializers import TaskSerializer

def dashboard_view(request):
    """Serve the frontend dashboard"""
    return render(request, 'index.html')

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    
    def perform_create(self, serializer):
        task = serializer.save()
        # Fetch weather info if location is provided
        if task.location:
            self.update_weather_info(task)
    
    def perform_update(self, serializer):
        task = serializer.save()
        # Update weather info if location changed
        if 'location' in serializer.validated_data and task.location:
            self.update_weather_info(task)
    
    def update_weather_info(self, task):
        """Fetch weather information from OpenWeatherMap API"""
        try:
            params = {
                'q': task.location,
                'appid': settings.WEATHER_API_KEY,
                'units': 'metric'
            }
            response = requests.get(settings.WEATHER_API_URL, params=params)
            
            if response.status_code == 200:
                weather_data = response.json()
                task.weather_info = {
                    'temperature': weather_data['main']['temp'],
                    'description': weather_data['weather'][0]['description'],
                    'humidity': weather_data['main']['humidity'],
                    'wind_speed': weather_data['wind']['speed'],
                    'fetched_at': timezone.now().isoformat()
                }
                task.save()
                
                TaskActivity.objects.create(
                    task=task,
                    action='weather_updated',
                    description=f'Weather info updated for {task.location}'
                )
        except Exception as e:
            print(f"Error fetching weather data: {e}")
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get task statistics for data visualization"""
        total_tasks = Task.objects.count()
        
        # Status distribution
        status_stats = Task.objects.values('status').annotate(
            count=Count('id')
        ).order_by('status')
        
        # Priority distribution
        priority_stats = Task.objects.values('priority').annotate(
            count=Count('id')
        ).order_by('priority')
        
        # Tasks created in last 7 days
        last_week = timezone.now() - timedelta(days=7)
        recent_tasks = Task.objects.filter(
            created_at__gte=last_week
        ).extra(
            select={'day': 'date(created_at)'}
        ).values('day').annotate(
            count=Count('id')
        ).order_by('day')
        
        # Overdue tasks
        overdue_tasks = Task.objects.filter(
            due_date__lt=timezone.now(),
            status__in=['pending', 'in_progress']
        ).count()
        
        # Completion rate
        completed_tasks = Task.objects.filter(status='completed').count()
        completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        
        return Response({
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'overdue_tasks': overdue_tasks,
            'completion_rate': round(completion_rate, 2),
            'status_distribution': list(status_stats),
            'priority_distribution': list(priority_stats),
            'daily_creation_trend': list(recent_tasks)
        })
    
    @action(detail=False, methods=['get'])
    def weather_summary(self, request):
        """Get weather summary for tasks with location data"""
        tasks_with_weather = Task.objects.filter(
            weather_info__isnull=False,
            location__isnull=False
        ).exclude(location='')
        
        weather_summary = []
        for task in tasks_with_weather:
            if task.weather_info:
                weather_summary.append({
                    'task_id': task.id,
                    'task_title': task.title,
                    'location': task.location,
                    'temperature': task.weather_info.get('temperature'),
                    'description': task.weather_info.get('description'),
                    'last_updated': task.weather_info.get('fetched_at')
                })
        
        return Response({
            'total_tasks_with_weather': len(weather_summary),
            'weather_data': weather_summary
        })
    
    @action(detail=True, methods=['post'])
    def refresh_weather(self, request, pk=None):
        """Manually refresh weather information for a specific task"""
        task = self.get_object()
        if not task.location:
            return Response(
                {'error': 'Task has no location set'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        self.update_weather_info(task)
        serializer = self.get_serializer(task)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        """Combined dashboard data for frontend visualization"""
        stats = self.statistics(request).data
        weather = self.weather_summary(request).data
        
        # Recent activities
        recent_activities = TaskActivity.objects.select_related('task')[:10]
        activities_data = [{
            'id': activity.id,
            'task_title': activity.task.title,
            'action': activity.action,
            'description': activity.description,
            'timestamp': activity.timestamp
        } for activity in recent_activities]
        
        return Response({
            'statistics': stats,
            'weather_summary': weather,
            'recent_activities': activities_data
        })