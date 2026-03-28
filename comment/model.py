from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class CommentManager(models.Manager):
    def filter_parents_by_object(self, obj):
        """
        This is the exact method your BlogItem needs.
        It looks up the 'ContentType' for the object (e.g. BlogItem)
        and filters comments linked to that specific ID.
        """
        content_type = ContentType.objects.get_for_model(obj)
        # We filter by the type of model and the specific primary key (ID)
        return self.filter(content_type=content_type, object_id=obj.id)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(verbose_name="Comment Content")
    date_created = models.DateTimeField(auto_now_add=True)

    # --- Generic Foreign Key Fields ---
    # This stores the 'type' of model (e.g., BlogItem)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # This stores the ID of the specific blog post
    object_id = models.PositiveIntegerField()
    # This is the 'virtual' field that gives you access to the object itself
    content_object = GenericForeignKey('content_type', 'object_id')

    # Attach the custom manager
    objects = CommentManager()

    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return f"Comment by {self.user.username} on {self.content_object}"