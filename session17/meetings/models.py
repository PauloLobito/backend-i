from django.db import models
from django.core.exceptions import PermissionDenied


class Meeting(models.Model):
    title = models.CharField(max_length=150)
    date = models.DateField()
    owner = models.CharField(max_length=100)

    def user_can_edit(self, user):
        if user.is_superuser:
            return True
        if user.groups.filter(name="admin").exists():
            return True
        if user.groups.filter(name="editor").exists():
            return True
        return str(user.username) == self.owner

    def user_can_delete(self, user):
        if user.is_superuser:
            return True
        return user.groups.filter(name="admin").exists()


class ActionItem(models.Model):
    meeting = models.ForeignKey(
        Meeting, on_delete=models.CASCADE, related_name="action_items"
    )
    description = models.CharField(max_length=300)
    owner = models.CharField(max_length=100)
    due_date = models.DateField()
    status = models.CharField(max_length=20, default="open")

    def clean(self):
        super().clean()
        if self.pk:
            original = ActionItem.objects.get(pk=self.pk)
            if original.owner != self.owner and original.owner != getattr(
                self, "_request_user", None
            ):
                raise PermissionDenied("Cannot change ownership of action item")

    def save(self, *args, **kwargs):
        user = kwargs.pop("request_user", None)
        self._request_user = user.username if user and user.is_authenticated else None
        super().save(*args, **kwargs)

    def user_can_edit(self, user):
        if user.is_superuser:
            return True
        if user.groups.filter(name="admin").exists():
            return True
        return str(user.username) == self.owner

    def user_can_delete(self, user):
        if user.is_superuser:
            return True
        if user.groups.filter(name="admin").exists():
            return True
        return str(user.username) == self.owner
