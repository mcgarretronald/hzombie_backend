from django.db import models
from users.models import User

class Script(models.Model):
    script_id = models.AutoField(primary_key=True)  # PK, auto-increment
    title = models.CharField(max_length=255)
    synopsis = models.TextField()
    genre = models.CharField(max_length=100)
    google_doc_link = models.URLField(max_length=500)
    pdf_file = models.FileField(upload_to='scripts/', blank=True, null=True)  # Optional
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # FK to User model
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
