from django.urls import path
from .views import ValidatePlaca

urlpatterns = [
    path('validator-placa/', ValidatePlaca.as_view(), name='validator-placa-particular'),
]