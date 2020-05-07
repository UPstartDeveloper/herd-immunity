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

    def invert_relationships(self, infected_nodes):
        """Reorganizes InfectedNode instances such that parent nodes point
           to children.

           Parameters:
           infected_nodes(QuerySet)

           Returns: None

        """
        # give each node a 'children' atttribute
        for node in infected_nodes:
            node.children = []
        # point out parent-child node relationships
        for node in infected_nodes:
            parent = node.parent
            if parent is not None:
                parent.children.append(node)
        return None

    """def add_object_to_data(data, doc):
        '''Inserts new object into the data dictionary.'''
        found = False
        while found is not True:
            # start by traversing the children of the root node
            children = data['children']"""

    def define_data(node, parent=None, data=None):
        """Organize nodes in a top-down structure, starting from the virus
           node.

           Parameters:
           infected_nodes(QuerySet):
                    each has attributes of the InfectedNode model, as well as
                    a 'children' attribute, which is a list of all the
                    InfectedNode instances representing those whom they
                    infected.

           virus(InfectedNode): represents the virus who began infecting other
                                persons initially. Occupies the root of the
                                whole nested structure.

           Return: dict - nested dictionary of virus node.
                   Contains fields for its id value, and its children, then
                   their children, and so on.
                   Recursively structured.

        """
        # base case: data needs to be initialized to a dictionary
        if data is None:
            data = {
                'name': node.identifer,
                'children': node.children
            }
            # begin traversal of other nodes
            for i in range(len(node.children)):
                next_node = node.children[i]
                self.define_data(infected_nodes, next_node, node, data)
        # recursive case: child node need to be converted to dictionary
        else:  # data is not None
            child_index = parent_node.children.index(node)
            parent_node.children[child_index] = {
                'name': node.identifer,
                'children': node.children
            }
            # traverse over their child as well, if needed
            for i in range(node.children):
                next_node = node.children[i]
                self.define_data(infected_nodes, next_node, node, data)
                # when the recursive call end, return to avoid ending too early
                return None
        return data

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
        # return data on InfectedNodes in a top-down structure
        self.invert_relationships(infected_nodes)
        data = self.define_data(virus)
        print(data)
        return Response(data)
