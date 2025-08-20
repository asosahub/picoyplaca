from django.urls import path
from .views import ParityCheckView

urlpatterns = [
    path('parity/', ParityCheckView.as_view(), name='parity-check'),
]