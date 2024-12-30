from django.db import models
from account.models import CustomUser
# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # User as owner
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set the time when the object is created

    def __str__(self):
        return self.name

class ProjectMembers(models.Model):
    # Foreign key to the Project model
    project = models.ForeignKey(Project, related_name='members', on_delete=models.CASCADE)
    # Foreign key to the User model
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    # Role of the user in the project
    role = models.CharField(max_length=50, choices=[('Admin', 'Admin'), ('Member', 'Member')])

    class Meta:
        unique_together = ('project', 'user')  # Ensures that a user can only be in the project once

    def __str__(self):
        return f"{self.user.username} - {self.role} in {self.project.name}"
    


class Task(models.Model):
    STATUS_CHOICES = [
        ('To Do', 'To Do'),
        ('In Progress', 'In Progress'),
        ('Done', 'Done'),
    ]
    
    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='To Do')
    priority = models.CharField(max_length=50, choices=PRIORITY_CHOICES, default='Medium')
    assigned_to = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    
    def __str__(self):
        return self.title
    

class Comment(models.Model):
    content = models.TextField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comments')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user} on {self.created_at}'
