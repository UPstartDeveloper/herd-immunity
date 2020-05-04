from django.contrib import admin
from .models import Experiment, TimeStep, InfectedNode

admin.site.register(Experiment)
admin.site.register(TimeStep)
admin.site.register(InfectedNode)
