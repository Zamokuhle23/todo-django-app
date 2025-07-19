from django.db import models

class TodoItem(models.Model):
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
    translated_title = models.CharField(max_length=200, blank=True, null=True)
    language = models.CharField(max_length=10, default='en')  # store language code

    def __str__(self):
        return self.title
