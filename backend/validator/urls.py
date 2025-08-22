from django.urls import path
from .views import CirculationRestrictionView

urlpatterns = [
    path('validator-placa/', CirculationRestrictionView.as_view(), name='validator-placa-particular'),
]