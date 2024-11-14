# Script Model
from django.db import models
from users.models import User

class Script(models.Model):
    script_id = models.AutoField(primary_key=True)  # PK, auto-increment
    title = models.CharField(max_length=255)
    synopsis = models.TextField()
    genre = models.CharField(max_length=100)
    google_doc_link = models.URLField(max_length=500)
    pdf_file = models.FileField(upload_to='scripts/', blank=True, null=True)  # Optional
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    total_likes = models.IntegerField(default=0)
    total_dislikes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def update_rating_counts(self):
        """Updates total likes and dislikes based on associated ratings."""
        from ratings.models import Rating  # Move import here
        self.total_likes = self.ratings.filter(rating=1).count()  # Count likes
        self.total_dislikes = self.ratings.filter(rating=-1).count()  # Count dislikes
        self.save(update_fields=['total_likes', 'total_dislikes'])  # Save only the updated fields
