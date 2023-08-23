from django.db import models


class User(models.Model):
    phone_number = models.CharField(max_length=20, unique=True)
    invite_code = models.CharField(max_length=6, unique=True, null=True, blank=True)
    invited_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    used_invite_code = models.CharField(max_length=20, blank=True, null=True)


    def __str__(self):
        return self.phone_number

    def save(self, *args, **kwargs):
        if self.used_invite_code and not self.invited_by:
            invited_by = User.objects.filter(invite_code=self.used_invite_code).first()
            if invited_by:
                self.invited_by = invited_by
        super().save(*args, **kwargs)
