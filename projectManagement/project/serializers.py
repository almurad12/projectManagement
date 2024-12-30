from rest_framework import serializers
from .models import Project, ProjectMembers
from django.contrib.auth.models import User
from project.models import Task,Comment
class ProjectMemberSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # To display the username instead of the user ID
    role = serializers.ChoiceField(choices=[('Admin', 'Admin'), ('Member', 'Member')])

    class Meta:
        model = ProjectMembers
        fields = ['id', 'project', 'user', 'role']

class ProjectSerializer(serializers.ModelSerializer):
    # Nested serializer to include project members
    members = ProjectMemberSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'owner', 'created_at', 'members']
        read_only_fields = ['id', 'created_at']

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'priority', 'assigned_to', 'project', 'created_at', 'due_date']



class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'content', 'user', 'task', 'created_at']
        read_only_fields = ['user', 'created_at']
    