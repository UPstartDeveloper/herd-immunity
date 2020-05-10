from django.db import models
from analysis.person import Person
from analysis.simulation import WebSimulation
from analysis.virus import Virus
from web import settings
from django.utils import timezone
from django.urls import reverse
from data_structures.mwaytree import MWayTree, MWayTreeNode
from queue import Queue
from django.contrib.postgres.fields import ArrayField


class Experiment(models.Model):
    '''An experiment by the user to test the herd immunity of a population.'''
    title = models.CharField(max_length=settings.EXPER_TITLE_MAX_LENGTH,
                             unique=False,
                             help_text="Title of your experiment.")
    population_size = models.IntegerField(help_text=(
        "How large is the population?"))
    vaccination_percent = models.FloatField(help_text=(
        "What percentage of the population is initially vaccinated " +
        "against the virus?"
    ))
    virus_name = models.CharField(max_length=settings.EXPER_TITLE_MAX_LENGTH,
                                  unique=False, null=True,
                                  help_text="What virus are you testing?")
    mortality_chance = models.FloatField(help_text=(
        "How likely is a patient infected with the virus likely to succumb?" +
        " Must be a percentage between 0.00 and 1.00."
    ))
    reproductive_rate = models.FloatField(help_text=(
        "How effective is the virus at spreading between individuals?" +
        " Must be a percentage between 0.00 and 1.00."
    ))
    initial_infected = models.IntegerField(help_text=(
        "At the beginning of the experiment, how many people in the " +
        "population are infected with the virus?"
    ))

    def __str__(self):
        '''Return the title of the Experiment instance.'''
        return self.title

    def get_absolute_url(self):
        '''Returns a path to the experimental results after form submission.'''
        path_components = {'pk': self.pk}
        return reverse('simulator:simulation_detail', kwargs=path_components)

    def generate_web_sim(self):
        """Update atttributes for Simulation, based on new data from an
           Experiment instance.

           Parameters:
           self(Experiment): the calling Experiment instance

           Returns:
           WebSimulation: a new instance of the class

        """
        # init population related fields
        pop_size = self.population_size
        # init related fields, virus fields
        virus = Virus(self.virus_name, self.reproductive_rate,
                      self.mortality_chance)
        initial_infected = self.initial_infected
        vacc_percentage = self.vaccination_percent
        # create the population
        return WebSimulation(pop_size, vacc_percentage, virus,
                             initial_infected)

    def make_basic_node(self, node):
        """Return an InfectedNode instance with an empty parent field
           If there is already an InfectedNode instance for the node, retrieve
           that from the db instead.
        """
        infected_node, truth = InfectedNode.objects.get_or_create(
            experiment=self,
            identifier=node.character,
            children=list(node.children.keys())
        )

        return infected_node

    def store_infected_persons(self, population_tree):
        """Instaniates and saves instances of InfectedNode related to this
           Experiment.

        """
        # Create queue to store nodes not yet traversed in level-order
        queue = Queue()
        # Enqueue starting at the virus, and then all the initial infected
        virus_node = population_tree.root
        queue.put(virus_node)
        # Loop until queue is empty
        while queue.qsize() > 0:
            # Dequeue node at front of queue
            parent_node = queue.get()
            # Set the node's children to point to their parent
            infected_by_parent = list()
            for node in parent_node.children:
                # grab instance of MWayTreeNode
                child = parent_node.children[node]
                # enqueue the MWayTreeNode to be the next parent
                queue.put(child)
                # prepare the InfectedNodes for initialization
                next_node = self.make_basic_node(child)
                infected_by_parent.append(next_node)
            # make basic node of the parent
            parent_node = self.make_basic_node(parent_node)
            for next_node in infected_by_parent:
                # point out its relationship to the parent, and save
                next_node.parent = parent_node
                next_node.save()
            # Save the parent in the db
            parent_node.save()

    def run_experiment(self):
        '''Runs through the experiment, and generates time step graphs.'''
        # update Simulation properties with form data
        web_sim = self.generate_web_sim()
        # run through the simulation, collect data to make TimeStep instances
        data_collection = web_sim.run_and_collect(self)
        # insert new TimeSteps into the db
        for ts in data_collection[:-1]:
            time_step = TimeStep.objects.create(
                step_id=ts.get('step_id'),
                total_infected=ts.get('total_infected'),
                current_infected=ts.get('current_infected'),
                dead=ts.get('dead'),
                total_vaccinated=ts.get('total_vaccinated'),
                alive=ts.get('alive'),
                uninfected=ts.get('uninfected'),
                uninteracted=ts.get('uninteracted'),
                experiment=ts.get('experiment')
            )
            time_step.save()
        # initialize population tree of infected persons
        population_tree = data_collection[-1]
        self.store_infected_persons(population_tree)


class TimeStep(models.Model):
    '''A visual representation of a time step for a Simulation.'''
    step_id = models.IntegerField(help_text=(
        "What time step is this TimeStep for?"))
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE,
                                   help_text="The related Experiment model.")
    total_infected = models.IntegerField(help_text=(
        "People who contracted the virus thus far in the experiment."
    ))
    current_infected = models.IntegerField(help_text=(
        "People infected who are still alive in this step of the experiment."
    ))
    dead = models.IntegerField(help_text="People thus far who have succumbed.")
    total_vaccinated = models.IntegerField(help_text=(
        "Amount of individuals who are now vaccinated in the population."
    ))
    alive = models.IntegerField(help_text="People who are currently alive.")
    uninfected = models.IntegerField(help_text=(
        "People who have not had any interaction with the virus."
    ))
    uninteracted = models.IntegerField(help_text=(
        "Alive people in the"
        + " population who are both uninfected, not vaccinated."))
    created = models.DateTimeField(auto_now_add=True,
                                   help_text=("The date and time this TimeStep"
                                              + " was created. Auto-generated "
                                              + "when the model " +
                                              "saves, used for ordering."))

    def __str__(self):
        '''Return a unique phrase identifying the TimeStep.'''
        return f'{self.experiment} Step {self.step_id}'


class InfectedNode(models.Model):
    """
    A node in the population tree of infected persons. Begins with the root
    being the virus, then diverges into each person whom was infected by the
    previous node.
    """
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE,
                                   help_text="The related Experiment.")
    identifier = models.CharField(max_length=settings.EXPER_TITLE_MAX_LENGTH,
                                  unique=False,
                                  help_text=("identifier of the person/virus "
                                             + "in experiment."))
    parent = models.ForeignKey('InfectedNode', on_delete=models.CASCADE,
                               help_text="Source of this person's infection.",
                               null=True)
    children = ArrayField(
                    models.CharField(
                        max_length=settings.EXPER_TITLE_MAX_LENGTH,
                        unique=False), blank=True, null=True)

    def __str__(self):
        '''Return a unique phrase identifying the TimeStep.'''
        return f'{self.experiment}: {self.identifier}'
