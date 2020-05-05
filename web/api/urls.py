from django.urls import path
from .views import TimeStepData, InfectedNodeData

app_name = 'api'
urlpatterns = [
    # used to send data to use for AJAX calls, then make graphs with Chart.js
    path('<int:pk>/charts/time-step/', TimeStepData.as_view(), name="ts_data"),
    path('<int:pk>/chart/infected-node/', InfectedNodeData.as_view(),
         name="in_data"),
]
