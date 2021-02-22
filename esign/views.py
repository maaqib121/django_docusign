from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from docusign_esign import EnvelopeDefinition, Recipients, Tabs, SignHere, Signer, Document, EnvelopesApi, ApiClient, TextCustomField, CustomFields, BulkEnvelopesApi, Envelope
from docusign_esign.models import BulkSendingCopyRecipient, BulkSendingCopy, BulkSendingList, BulkSendRequest
import base64
from django_docusign.settings import BASE_DIR
import xml.etree.ElementTree as ET
from esign.models import SigEnvelope, SignRequest, Recipient
import jwt
from datetime import datetime, timedelta
import requests
import json
import time


USER_ID = '05050086-c4a6-462c-9e72-dbe3a5923ac1'
INTEGRATION_KEY = 'bfa347f3-b3d3-451b-8e31-ea81907ab1e6'
ACCOUNT_ID = '46e5d2d8-0f26-4f74-890f-8205867d46e6'
BASE_PATH = 'https://demo.docusign.net/restapi'
PUBLIC_KEY = '''-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAu8s+QSn1gLDlLnbhuQZn
/6BSLbf9OH+VQKF1AWipSetxXcb6zikoMT4DIB62UMdOwGnJJyWwVJ2rpY6lacb6
CaRdZeJ7vwLO1GZYZ8tpWF3X4epJo97OzWSnaABWMIl+N7oZ9oMT4lQZE9aN+klg
DQLEvj3gqk7DrOSlw0Myi3Q0sgMjmb/hPgTdnM1gytvfDyas9ofGeE3n9SDY7umF
UDXXVMnt2WC7j4/l85fzlAN/KaE55BokxCibT8mwgGdZRlaZZks9S9ODsUtnY0Te
a7WttFebkQ4aNz4d/v+8zx+6uN19dWi8NNcPTrbYXhMokYdqBG/HXbQ+bSsGOgAo
cwIDAQAB
-----END PUBLIC KEY-----'''
PRIVATE_KEY = '''-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEAu8s+QSn1gLDlLnbhuQZn/6BSLbf9OH+VQKF1AWipSetxXcb6
zikoMT4DIB62UMdOwGnJJyWwVJ2rpY6lacb6CaRdZeJ7vwLO1GZYZ8tpWF3X4epJ
o97OzWSnaABWMIl+N7oZ9oMT4lQZE9aN+klgDQLEvj3gqk7DrOSlw0Myi3Q0sgMj
mb/hPgTdnM1gytvfDyas9ofGeE3n9SDY7umFUDXXVMnt2WC7j4/l85fzlAN/KaE5
5BokxCibT8mwgGdZRlaZZks9S9ODsUtnY0Tea7WttFebkQ4aNz4d/v+8zx+6uN19
dWi8NNcPTrbYXhMokYdqBG/HXbQ+bSsGOgAocwIDAQABAoIBAAOFOrj3Jh1UoVKq
PG6+821Kx4i/Tao3MO0WYue0/7dvmnq9SC+AoXFmTer7Fh/dilj369oBKbmjNnf3
fJt94tjttilfXYul/mYIW/2fRgAA8BMa+UQlvI9NJOP4gjdpAQFMuGRzN3Z+tj41
iJqwjE2NkOBW+J4UIsbuYl9qJDdJAYt/KfIZfB0rRjaN5RbfXGGKXhFl2MamaKDf
PWU9gCYpwPkylGZIJov4ncqovU/Edx7YdBFd2S2LJLj685UBUVe5ufsfVbLIloeM
fIkbNeGUCkMEsXvbJD7XDWxvNWwdsW/ZqypISsucUDIQycT7BvpRjycZDDRawSY1
GVQfLkECgYEA9+YG3A5f3o6FeO2NZAUFQjhHVCdkl5Bu3jRUGPKyOhwd4maKzGYs
cooxD4FvUTXtVjpt9TBuXbZ9UBY1GaXHFjINR/45Xndnpg0HLsrVtkf2LMNlOayh
aqULzbYOAxsRsMdhb6cyJdvULAgVnCozc9rLvGsFct56Ex2WIzEqY18CgYEAwe5e
NiKX3ofbFjGb3UwsnhSSv2CKFTPE/jvyBcd1wQiYBIJX6+1fz6nccjiYzddn1dkk
X3hzhc+RGkLvj3sQSzJd6y/VNkMJeowP7o8zHlSkghcHWmU/LhYnL2jXnpO7rRrA
AoEMzrAeMfYr/F6xKIbBUzUd6eAg+GL/bpFrx20CgYEAvN0pWLoy3BJlKe6CDDOu
//Z0kW65uqc1cGEZuTAeDRuiwPwyvusQ7erO2etY7dxSB6HYaDcPvqHr8voYVoPw
m75iU/khqBD8jIvcbw/lpkxJB22OT1RwXhmEVqNfJYqX/cDJQRF2qVVD3pACNsoI
DToiglhe/Fb3VlzyJ7mre60CgYA5iLFUmDC8KUv7Kp6WKco2392lf0uX/LLdxgUI
Z+NscFNBSzYwXU0Ge9tV26qhrt00WWZsGH0VXr4qr18JDzaHSJsKcjdsELlYLQNw
//Tnc68WlSRuUglLb/ESJKWLe0K7mWsLkyOskh1zLxhfl+wxHMFwIRsNzpuZdS1Y
rTXvhQKBgG8qVuR+lGJ8xzPA4ktFjANqa84Qr6eTO3nKmlPv+nOYcs7OD9rtZP3r
K/1in9yhOVHodijm8ZEu9SL0HGURSX6QOAH5eb2MO8lMfo97F06cqD7Vqw/uW1zg
3wHIgffPMYmPdUQ20kJKFnm4FmF1cL7x/ZVwd7mdP6cEs8EydP3B
-----END RSA PRIVATE KEY-----'''


def get_access_token():
    encoded_jwt = jwt.encode({
        'iss': INTEGRATION_KEY,
        'sub': USER_ID,
        'exp': datetime.now().strftime('%s'),
        'aud': 'account-d.docusign.com',
        'scope': 'signature impersonation'
    }, PRIVATE_KEY, algorithm='RS256')

    response = requests.post('https://account-d.docusign.com/oauth/token', data={
        'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer',
        'assertion': encoded_jwt
    })
    return json.loads(response.content)['access_token']


def make_envelope():
    with open(f'{BASE_DIR}/document.pdf', 'rb') as pdf_file:
        content_bytes = pdf_file.read()
    base64_file_content = base64.b64encode(content_bytes).decode('ascii')
    document = Document(document_base64=base64_file_content, name='Employee Contract',
                        file_extension='pdf', document_id='1')
    signer = Signer(email='m.aaqib@thedevden.co', name='M Aaqib', recipient_id='1', routing_order='1')
    sign_here = SignHere(anchor_string='**Employee Signature**', anchor_units='pixels',
                         anchor_y_offset='10', anchor_x_offset='20')
    signer.tabs = Tabs(sign_here_tabs=[sign_here])
    recipients = Recipients(signers=[signer])
    envelope_definition = EnvelopeDefinition(email_subject='Please sign this document set', documents=[document],
                                             recipients=recipients, status='sent')
    return envelope_definition


def get_api_client():
    api_client = ApiClient()
    api_client.host = BASE_PATH
    api_client.set_default_header('Authorization', f'Bearer {get_access_token()}')
    return api_client


class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'home.html')


class SignView(View):
    def get(self, request, *args, **kwargs):
        envelope_definition = make_envelope()
        envelopes_api = EnvelopesApi(get_api_client())
        results = envelopes_api.create_envelope(ACCOUNT_ID, envelope_definition=envelope_definition)
        sign_envelope = SigEnvelope.objects.create(envelope_id=results.envelope_id)
        sign_request = SignRequest.objects.create(envelope=sign_envelope, error_details=results.error_details,
                                                  status_date_time=results.status_date_time)
        Recipient.objects.create(recipient_id='1', sign_request=sign_request, email='m.aaqib@thedevden.co')
        return JsonResponse({'envelope_id': results.envelope_id})


class RetrieveView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(RetrieveView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        response = request.body
        root = ET.fromstring(response)
        pdf_file = open(f'{root[1][0][0].text}.pdf', 'wb')
        pdf_file.write(base64.b64decode(root[1][0][1].text))
        sign_request = SignRequest.objects.get(envelope=SigEnvelope.objects.get(envelope_id=root[0][2].text))
        sign_request.attachment = pdf_file.name
        sign_request.save()
        return JsonResponse({'success': True})


class EnvelopeListView(View):
    def get(self, request, *args, **kwargs):
        envelopes_api = EnvelopesApi(get_api_client())
        context = {}
        from_date = (datetime.utcnow() - timedelta(days=60)).isoformat()
        # retrieve all envelopes of last 2 months
        context['envelope_list'] = envelopes_api.list_status_changes(ACCOUNT_ID, status='sent, delivered',
                                                                     from_date=from_date).envelopes
        return render(request, 'envelopes/envelope_list.html', context=context)


class EnvelopeDetailView(View):
    def get(self, request, envelope_id):
        envelopes_api = EnvelopesApi(get_api_client())
        context = {
            'envelope_recipients': envelopes_api.list_recipients(ACCOUNT_ID, envelope_id),
            'envelope': envelopes_api.get_envelope(ACCOUNT_ID, envelope_id)
        }
        return render(request, 'envelopes/envelope_detail.html', context=context)


class EnvelopeDeleteView(View):
    def get(self, request, envelope_id):
        envelopes_api = EnvelopesApi(get_api_client())
        envelope = envelopes_api.get_envelope(ACCOUNT_ID, envelope_id)
        envelope.status = 'voided'
        envelope.voided_reason = 'changed my mind'
        envelope.purge_state = None
        envelopes_api.update(ACCOUNT_ID, envelope_id, envelope=envelope)
        SigEnvelope.objects.get(envelope_id=envelope_id).delete()
        return redirect('esign:envelope_list')


class RecipientDeleteView(View):
    def get(self, request, envelope_id, recipient_id):
        envelopes_api = EnvelopesApi(get_api_client())
        envelopes_api.delete_recipient(ACCOUNT_ID, envelope_id, recipient_id)
        return redirect(reverse('esign:envelope_detail', kwargs={'envelope_id': envelope_id}))


class RecipientCreateView(View):
    def post(self, request, envelope_id):
        signer = Signer(email=request.POST['email'], name='Aaqib 2', recipient_id='2', routing_order='1')
        sign_here = SignHere(anchor_string='**Employee Signature**', anchor_units='pixels',
                             anchor_y_offset='10', anchor_x_offset='100')
        signer.tabs = Tabs(sign_here_tabs=[sign_here])
        recipients = Recipients(signers=[signer])
        envelopes_api = EnvelopesApi(get_api_client())
        envelope = envelopes_api.create_recipient(ACCOUNT_ID, envelope_id, recipients=recipients,
                                                  resend_envelope='true')
        sign_request = SignRequest.objects.get(envelope=SigEnvelope.objects.get(envelope_id=envelope_id))
        Recipient.objects.create(email=request.POST['email'], recipient_id='2', sign_request=sign_request)
        return redirect(reverse('esign:envelope_detail', kwargs={'envelope_id': envelope_id}))


class BulkEnvelopeView(View):
    def get(self, request, *args, **kwargs):
        api_client = get_api_client()
        bulk_envelopes_api = BulkEnvelopesApi(api_client)
        recipient_1 = BulkSendingCopyRecipient(role_name='signer', name='Aaqib 1', email='f168324@nu.edu.pk')
        recipient_2 = BulkSendingCopyRecipient(role_name='signer', name='Aaqib 2', email='m.aaqib@thedevden.co')
        bulk_copies = [
            BulkSendingCopy(recipients=[recipient_1], custom_fields=[]),
            BulkSendingCopy(recipients=[recipient_2], custom_fields=[]),
        ]
        bulk_sending_list = BulkSendingList(name='employee_contract', bulk_copies=bulk_copies)
        bulk_list = bulk_envelopes_api.create_bulk_send_list(ACCOUNT_ID, bulk_sending_list=bulk_sending_list)
        bulk_list_id = bulk_list.list_id

        envelopes_api = EnvelopesApi(api_client)
        with open(f'{BASE_DIR}/document.pdf', 'rb') as pdf_file:
            content_bytes = pdf_file.read()
        base64_file_content = base64.b64encode(content_bytes).decode('ascii')
        document = Document(document_base64=base64_file_content, name='Employee Contract',
                            file_extension='pdf', document_id='1')
        envelope_definition = EnvelopeDefinition(email_subject='Please sign this document set', documents=[document],
                                                 recipients={}, status='created', envelope_id_stamping='true')
        envelope = envelopes_api.create_envelope(account_id=ACCOUNT_ID, envelope_definition=envelope_definition)
        envelope_id = envelope.envelope_id

        text_custom_fields = TextCustomField(name='mailingListId', required='false', show='false', value=bulk_list_id)
        custom_fields = CustomFields(list_custom_fields=[], text_custom_fields=[text_custom_fields])
        envelopes_api.create_custom_fields(account_id=ACCOUNT_ID, envelope_id=envelope_id, custom_fields=custom_fields)

        signer = Signer(name='Multi Bulk Recipient::signer', email='multiBulkRecipients-signer@docusign.com',
                        role_name='signer', note='', routing_order='1', status='created', delivery_method='email',
                        recipient_id='13', recipient_type='signer')
        envelopes_api.create_recipient(ACCOUNT_ID, envelope_id, recipients=Recipients(signers=[signer]))
        bulk_send_request = BulkSendRequest(envelope_or_template_id=envelope_id)
        batch = bulk_envelopes_api.create_bulk_send_request(ACCOUNT_ID, bulk_list_id,
                                                            bulk_send_request=bulk_send_request)

        time.sleep(10)
        from_date = (datetime.utcnow() - timedelta(seconds=60)).isoformat()
        envelopes = envelopes_api.list_status_changes(ACCOUNT_ID, status='sent', from_date=from_date).envelopes
        for envelope in envelopes:
            env, created = SigEnvelope.objects.get_or_create(envelope_id=envelope.envelope_id)
            if created:
                sign_request = SignRequest.objects.create(envelope=env, status_date_time=envelope.status_date_time)
                recipients = envelopes_api.list_recipients(ACCOUNT_ID, envelope.envelope_id)
                Recipient.objects.create(sign_request=sign_request, email=recipients.signers[0].email,
                                         recipient_id=recipients.signers[0].recipient_id)
        return redirect('esign:envelope_list')
