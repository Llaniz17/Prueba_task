from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField(null=True, blank=True)
    city = models.CharField(max_length=100, blank=True)  # api

    def __str__(self):
        return str(self.title)

class City(models.Model):
    city = models.CharField(max_length=100)
    consulted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.city} - {self.consulted_at.strftime('%Y-%m-%d %H:%M')}"
