from django.db import models
from analysis.person import Person
from analysis.simulation import Simulation
from analysis.virus import Virus
from analysis.visualizer import Visualizer, WebVisualizer
from web import settings
from django.utils import timezone
from django.urls import reverse
from django.core.files.images import ImageFile


class WebSimulation(Simulation):
    '''A Simulation class especially made to work with Django models.'''
    def store_vacc_persons(self, alive):
        """Return people in the population who are alive and vaccinated.

           Parameters:
           alive(list): a collection of Person objects

           Return:
           persons(list): a collection of Person objects who are both alive and
                          vaccinated

        """
        persons = list()
        for person in self.population:
            if person in alive and person.is_vaccinated:
                persons.append(person)
        return persons

    def store_uninfected_persons(self, alive, vaccinated):
        """Return people who are alive, not vaccinated, and not infected.

           Parameters:
           alive(list): a collection of Person objects
           vaccinated(list): a collection of Person objects who are vaccinated

           Returns:
           persons(list): a collection of Person objects who're alive,
                          uninfected, nor vaccinated

        """
        persons = list()
        for person in alive:
            if person not in vaccinated and person.infection:
                persons.append(person)
        return persons

    def make_report(self, counter):
        """Return a report of the results of this time step.

           Parameters:
           counter(int): the numeric identifier of the current step

           Returns:
           str: a verbal record of the TimeStep results

        """
        # create a list of alive persons
        alive = self.get_alive()
        # create a list of vaccinated persons
        vaccinated = self.store_vacc_persons(alive)
        # create a list of uninfected persons
        uninfected = self.store_uninfected_persons(alive, vaccinated)
        # return values to init TimeStep fields
        return [
            counter,
            self.total_infected,
            self.current_infected(),
            self.vacc_percentage,
            self.total_dead,
            len(vaccinated),
            len(alive),
            len(uninfected),
            self.get_neither()
        ]

    def create_time_step(self, step_id, visualizer, experiment):
        """Make a TimeStep instance out of the simulation step.

           Parameters:
           step_id(int): the numeric id of the time step
           visualizer(WebVisualizer): makes the bar graph
           experiment(Experiment): the related Experiment instance

           Return:
           TimeStep: a single instance of the model, related to the calling
                     Experiment model
        """
        # compute the logic for this step
        self.time_step(step_id)
        # get a verbal report of the time step results
        description = self.make_report(step_id)
        # init TimeStep object
        graph = visualizer.bar_graph(step_id,
                                     (self.vacc_percentage *
                                      self.get_alive_num()),
                                     self.current_infected(),
                                     self.get_dead(),
                                     self.get_neither(),
                                     experiment)
        image = ImageFile(file=graph)
        # return a TimeStep instance with these fields
        return TimeStep.objects.create(step_id=step_id,
                                       total_infected=description[1],
                                       current_infected=description[2],
                                       vaccinated_population=description[3],
                                       dead=description[4],
                                       total_vaccinated=description[5],
                                       alive=description[6],
                                       uninfected=description[7],
                                       uninteracted=description[8],
                                       experiment=experiment, image=image)

    def run_and_collect(self, visualizer, experiment):
        """This method should run the simulation until all requirements for
           ending the simulation are met.

           Parameters:
           visualizer(Visualizer): constructs bar graph using matplotlib
           experiment(Experiment): related to the TimeStep objects being made

           Returns:
           NoneType: just to mark where the method ends

        """
        results = list()  # return value
        time_step_counter = 1
        simulation_should_continue = 0
        should_continue = None
        assert self.population[0]._id == 0
        # make TimeStep instances as the simulation runs
        while True:
            time_step = self.create_time_step(time_step_counter, visualizer,
                                              experiment)
            time_step.save()
            # decide to continue
            if self._simulation_should_continue():
                simulation_should_continue += 1
                break
            time_step_counter += 1
        return None


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
        return reverse('simulator:experiment_detail', kwargs=path_components)

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

    def run_experiment(self):
        '''Runs through the experiment, and generates time step graphs.'''
        # update Simulation properties with form data
        web_sim = self.generate_web_sim()
        # run through time steps, collect visuals and reports
        imager = WebVisualizer("Number of Survivors",
                               "Herd Immunity Defense Against Disease Spread")
        web_sim.run_and_collect(imager, self)


class TimeStep(models.Model):
    '''A visual representation of a time step for a Simulation.'''
    step_id = models.IntegerField(help_text=(
        "What time step is this TimeStep for?"))
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE,
                                   help_text="The related Experiment model.")
    image = models.ImageField(upload_to='images/',
                              help_text=("Graph representing changes to the " +
                                         "population during the TimeStep."))
    # description = models.TextField(help_text="Verbal summary of time step.")
    total_infected = models.IntegerField(help_text=(
        "People who contracted the virus thus far in the experiment."
    ))
    current_infected = models.IntegerField(help_text=(
        "People infected who are still alive in this step of the experiment."
    ))
    vaccinated_population = models.FloatField(help_text=(
        "Percentage of the overall population which is currently vaccinated."
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
