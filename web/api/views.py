from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponseRedirect, JsonResponse
from .serializers import TimeStepSerializer, InfectedNodeSerializer
from simulator.models import Experiment, TimeStep, InfectedNode


class TimeStepData(APIView):
    """
    View to list the fields and values of all time steps related to an
    Experiment.
    """
    serializer_class = TimeStepSerializer
    authentication_classes = list()
    permission_classes = list()

    def get(self, request, pk, format=None):
        """Return a list of all time steps with fields and values.

           request(HttpRequest): the GET request sent to the server
           pk(int): unique id value of an Experiment instance
           format(str): the suffix applied to the endpoint to indicate how the
                        data is structured (i.e. html, json)

           Returns:
           Response: the data used to make bar charts on the front end

        """
        # get all Time Steps related to the Experiment, return the last
        time_step = (
            TimeStep.objects.filter(experiment__id=pk).order_by('pk').last()
        )
        population_size = time_step.alive + time_step.dead
        data = {
                "labels": [
                    "Dead",
                    "Alive - Vaccinated",
                    "Alive - Uninfected",
                    "Alive - No Interaction"
                ],
                "pop_sizes": [
                    time_step.dead,
                    time_step.total_vaccinated,
                    time_step.uninfected,
                    time_step.uninteracted
                ]
        }
        return Response(data)


class InfectedNodeData(APIView):
    """
    View to list the fields and values of all time steps related to an
    Experiment.
    """
    serializer_class = InfectedNodeSerializer
    authentication_classes = list()
    permission_classes = list()

    def get(self, request, pk, format=None):
        """Return a recursively list of all instances of InfectedNode that
           are related to a certain Experiment.

           request(HttpRequest): the GET request sent to the server
           pk(int): unique id value of an Experiment instance
           format(str): the suffix applied to the endpoint to indicate how the
                        data is structured (i.e. html, json)

           Returns:
           Response: the data used to make a population tree on the front end

        """
        # get all InfectedNodes related to the Experiment
        experiment = Experiment.objects.get(id=pk)
        # start with the InfectedNode that holds the virus
        infected_nodes = InfectedNode.objects.filter(experiment=experiment)
        virus = infected_nodes.get(identifer=experiment.virus_name)
        # return the data on the Infected Nodes
        data = {}
        return Response(data)
