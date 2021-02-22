from django.db import models


class SigEnvelope(models.Model):
    envelope_id = models.CharField(max_length=50)

    def __str__(self):
        return self.envelope_id


class SignRequest(models.Model):
    envelope = models.OneToOneField(SigEnvelope, blank=True, null=True, on_delete=models.CASCADE)
    error_details = models.TextField(null=True)
    status_date_time = models.DateTimeField(auto_now_add=True)
    attachment = models.FileField(null=True)


class Recipient(models.Model):
    sign_request = models.ForeignKey(SignRequest, blank=True, null=True, on_delete=models.CASCADE)
    recipient_id = models.CharField(max_length=50)
    email = models.EmailField()
