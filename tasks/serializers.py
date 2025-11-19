from rest_framework import serializers
from .models import Task, TaskActivity

class TaskActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskActivity
        fields = ['id', 'action', 'description', 'timestamp']

class TaskSerializer(serializers.ModelSerializer):
    activities = TaskActivitySerializer(many=True, read_only=True)
    
    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'priority', 'status',
            'created_at', 'updated_at', 'due_date', 'location',
            'weather_info', 'activities'
        ]
    
    def create(self, validated_data):
        task = Task.objects.create(**validated_data)
        TaskActivity.objects.create(
            task=task,
            action='created',
            description=f'Task "{task.title}" was created'
        )
        return task
    
    def update(self, instance, validated_data):
        old_status = instance.status
        task = super().update(instance, validated_data)
        
        if old_status != task.status:
            TaskActivity.objects.create(
                task=task,
                action='status_changed',
                description=f'Status changed from {old_status} to {task.status}'
            )
        
        return task