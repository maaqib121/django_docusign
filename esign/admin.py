from django.contrib import admin
from esign.models import SigEnvelope, SignRequest, Recipient


admin.site.register(SigEnvelope)
admin.site.register(SignRequest)
admin.site.register(Recipient)
