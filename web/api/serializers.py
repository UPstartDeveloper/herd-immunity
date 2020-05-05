from rest_framework.serializers import ModelSerializer

from simulator.models import (
    Experiment,
    TimeStep,
    InfectedNode
)


class ExperimentSerializer(ModelSerializer):
    class Meta:
        model = Experiment
        fields = '__all__'


class TimeStepSerializer(ModelSerializer):
    class Meta:
        model = TimeStep
        fields = '__all__'


class InfectedNodeSerializer(ModelSerializer):
    class Meta:
        model = InfectedNode
        fields = '__all__'
