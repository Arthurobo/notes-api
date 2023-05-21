from django.db import models


class Note(models.Model):
    user = models.ForeignKey("accounts.Profile", blank=True, null=True, on_delete=models.SET_NULL)
    invites = models.ManyToManyField("accounts.Profile", blank=True, related_name='note_invites')
    title = models.CharField(max_length=255)
    content = models.TextField()
    date_created =  models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.pk)