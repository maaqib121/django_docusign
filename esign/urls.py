from django.urls import path
from esign.views import (
    HomeView, SignView, RetrieveView, EnvelopeListView, EnvelopeDetailView, EnvelopeDeleteView,
    BulkEnvelopeView, RecipientDeleteView, RecipientCreateView
)


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('sign/', SignView.as_view(), name='sign'),
    path('retrieve/', RetrieveView.as_view(), name='retrieve'),
    path('envelopes/', EnvelopeListView.as_view(), name='envelope_list'),
    path('envelopes/<str:envelope_id>/', EnvelopeDetailView.as_view(), name='envelope_detail'),
    path('envelopes/<str:envelope_id>/delete/', EnvelopeDeleteView.as_view(), name='envelope_delete'),
    path('envelopes/<str:envelope_id>/recipients/', RecipientCreateView.as_view(), name='recipient_create'),
    path('envelopes/<str:envelope_id>/recipients/<str:recipient_id>/delete/',
         RecipientDeleteView.as_view(), name='recipient_delete'),
    path('bulk/', BulkEnvelopeView.as_view(), name='bulk'),
]
