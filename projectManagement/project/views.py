from rest_framework import viewsets
from project.models import Project,ProjectMembers,Task,Comment
from project.serializers import ProjectSerializer, ProjectMemberSerializer,TaskSerializer,CommentSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
##project
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

##project Member
class ProjectMemberViewSet(viewsets.ModelViewSet):
    queryset = ProjectMembers.objects.all()
    serializer_class = ProjectMemberSerializer
    permission_classes = [IsAuthenticated]

##Task
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Filter tasks by project_id for list and create operations.
        """
        project_id = self.kwargs.get('project_id')
        if project_id:
            return Task.objects.filter(project_id=project_id)
        return Task.objects.all()

    def list(self, request, *args, **kwargs):
        """
        Override the list method to retrieve tasks for a specific project.
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


    def create(self, request, *args, **kwargs):
        """
        Override the create method to associate a new task with a specific project.
        """
        project_id = self.kwargs['project_id']
        
        # Create a mutable copy of the POST data
        mutable_data = request.data.copy()
        
        # Add the project_id to the task data
        mutable_data['project'] = project_id
        
        # Use the modified data in the serializer
        serializer = self.get_serializer(data=mutable_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        
        return Response(serializer.errors, status=400)

    # PUT and PATCH requests are handled by DRF's built-in methods
    def update(self, request, *args, **kwargs):
        """
        Handle full update (PUT).
        """
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """
        Handle partial update (PATCH).
        """
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        Handle task deletion.
        """
        task = self.get_object()  # Retrieve the task object by `id`
        task.delete()
        return Response(status=204)

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        task_id = self.kwargs.get('task_id')
        if task_id:
            return Comment.objects.filter(task_id=task_id)
        return Comment.objects.all()

    def perform_create(self, serializer):
        task_id = self.kwargs.get('task_id')
        task = Task.objects.get(id=task_id)
        serializer.save(task=task)

    def update(self, request, *args, **kwargs):
        # Ensure the comment exists and is fetched from the database
        comment = self.get_object()
        
        # Optionally, you could do additional validation or logging here
        # If you need to check for task association, you can add custom logic here.

        serializer = self.get_serializer(comment, data=request.data, partial=True)
        
        # Validate and save the updated comment
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        # Return the updated comment
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def perform_update(self, serializer):
        # Optional: Override if you need to perform any specific actions on comment update
        serializer.save()