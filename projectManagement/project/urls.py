from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, ProjectMemberViewSet,TaskViewSet,CommentViewSet

router = DefaultRouter()
router.register(r'', ProjectViewSet)
router.register(r'project-members', ProjectMemberViewSet)
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'comments', CommentViewSet, basename='comment')


urlpatterns = [
    path('', include(router.urls)),
    # List and Create Tasks for a specific project
    path('<int:project_id>/tasks/', TaskViewSet.as_view({'get': 'list', 'post': 'create'}), name='project-tasks-list-create'),
    # Retrieve, Update (PUT/PATCH), and Delete Task by ID
    path('tasks/<int:id>/', TaskViewSet.as_view({'get': 'retrieve', 'put': 'update_task', 'patch': 'update_task', 'delete': 'destroy'}), name='task-detail'),
 # List and Create Comments for a specific Task
    path('tasks/<int:task_id>/comments/', CommentViewSet.as_view({'get': 'list', 'post': 'create'}), name='task-comments-list-create'),
    # Retrieve, Update (PUT/PATCH), and Delete Comment by ID
    path('comments/<int:id>/', CommentViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'update', 'delete': 'destroy'}), name='comment-detail'),
]
