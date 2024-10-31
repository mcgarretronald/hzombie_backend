from django.db import models
from users.models import User
from script.models import Script
class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    script = models.ForeignKey(Script, on_delete=models.CASCADE, related_name='ratings')
    rating = models.IntegerField()  # 1 for like, -1 for dislike
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'script')  # Ensure a user can only rate a script once

    def __str__(self):
        return f"{self.user.email} rated {self.script.title}: {self.rating}"