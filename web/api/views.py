from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponseRedirect, JsonResponse
from .serializers import TimeStepSerializer, InfectedNodeSerializer
from simulator.models import Experiment, TimeStep, InfectedNode
from pprint import pprint


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
        pprint(len(infected_nodes))
        # give each node a 'children' atttribute
        for node in infected_nodes:
            node.children = []
            node.save()
        # point out parent-child node relationships
        for node in infected_nodes:
            parent = node.parent
            if parent is not None:
                if not hasattr(parent, 'children') or len(parent.children) == 0:
                    parent.children = []
                    print(f'Created empty list of children on parent {parent.identifier}')
                parent.children.append(node)
                print(f'Connected parent {parent.identifier} to child {node.identifier}')
            else:
                print(f'InfectedNode {node.identifier} has no parent')
        return None

    """def add_object_to_data(self, data, doc):
        '''Inserts new object into the data dictionary.'''
        found = False
        while found is not True:
            # start by traversing the children of the root node
            children = data['children']"""

    def define_data(self, node, parent=None, data=None):
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
        """temp_data = {
            'name': node.identifier,
            'children': node.children
        }
        # begin traversal of other nodes
        for next_node in node.children:
            # next_node = node.children[i]
            self.define_data(next_node, node, temp_data)
        # base case: data needs to be initialized to a dictionary
        if data is None:
            data = temp_data
            return data
        # recursive case: child node need to be converted to dictionary
        else:  # data is not None
            child_index = parent_node.children.index(node)
            parent_node.children[child_index] = temp_data
            # when the recursive call ends, return to avoid ending too early
            return None"""
        data = {'name': node.identifier}
        # data['name'] = node.identifier
        # begin traversal of other nodes
        if hasattr(node, 'children'):
            children_data = list()
            for child_node in node.children:
                child_data = self.define_data(child_node, node)
                children_data.append(child_data)
            # Equivalent list comprehension:
            # children_data = [self.define_data(child, node) for child in node.children]
            # Only add to dict if has children
            if len(children_data) > 0:
                data['children'] = children_data
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
        virus = infected_nodes.get(identifier=experiment.virus_name)
        # TODO turn query set into python list of InfectedNode objects
        infected_nodes = list(infected_nodes)
        # return data on InfectedNodes in a top-down structure
        self.invert_relationships(infected_nodes)
        data = self.define_data(virus)
        # data = {}
        # self.define_data(virus, parent=None, data=data)
        pprint(data)
        return Response(data)
