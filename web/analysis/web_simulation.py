import random
import sys
from .person import Person
from .logger import Logger
from .virus import Virus
from . import visualizer
from .simulation import Simulation
from data_structures.mwaytree import MWayTree, MWayTreeNode
random.seed(42)


class WebSimulation(Simulation):
    '''A Simulation class especially made to work with Django models.'''
    def __init__(self, pop_size, vacc_percentage, virus, initial_infected=1):
        '''Same as super class initializer, except no use of Logger.'''
        self.population = []  # List of Person objects
        self.pop_size = pop_size  # Int
        self.next_person_id = pop_size  # Int
        self.virus = virus  # Virus object
        self.initial_infected = initial_infected  # Int
        self.total_infected = MWayTree(virus_name=virus.name)
        self.vacc_percentage = vacc_percentage  # float between 0 and 1
        self.total_dead = 0  # Int
        self.newly_infected = []
        self.population = self._create_population()

    def _create_population(self):
        '''This method will create the initial population.
            Args:
                initial_infected (int): The number of infected people that the
                simulation will begin with.

            Returns:
                population: A list of Person objects.

        '''
        # section off population demographics
        population = list()
        number_vaccinated = round(self.vacc_percentage * self.pop_size)
        total = random.sample(range(self.pop_size), number_vaccinated +
                              self.initial_infected)
        # load the initially infected into the tree of infected persons
        indices_infected = self.random_infected(total)
        for id in indices_infected:
            self.total_infected.insert(self.total_infected.root.id, id)
        # form a list of Persons for the whole population
        indices_vaccinated = total
        for index in range(self.pop_size):
            if index in indices_vaccinated and index not in indices_infected:
                population.insert(index, Person(index, True))
            elif index not in indices_vaccinated and index in indices_infected:
                population.insert(index, Person(index, False, self.virus))
            else:
                population.insert(index, Person(index, False))
        return population

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
            self.total_infected.size,
            self.current_infected(),
            self.total_dead,
            len(vaccinated),
            len(alive),
            len(uninfected),
            self.get_neither()
        ]

    def create_time_step(self, step_id, experiment):
        """Make a TimeStep instance out of the simulation step.

           Parameters:
           step_id(int): the numeric id of the time step
           experiment(Experiment): the related Experiment instance

           Return:
           TimeStep: a single instance of the model, related to the calling
                     Experiment model
        """
        # compute the logic for this step
        self.time_step(step_id)
        # get a verbal report of the time step results
        description = self.make_report(step_id)
        # return fields and values to make new TimeStep
        return {
            'step_id': step_id,
            'total_infected': description[1],
            'current_infected': description[2],
            'dead': description[3],
            'total_vaccinated': description[4],
            'alive': description[5],
            'uninfected': description[6],
            'uninteracted': description[7],
            'experiment': experiment
        }

    def interaction(self, person, random_person):
        """This method should be called any time two living people are selected
            for an interaction. It assumes that only living people are passed
            in as parameters.

            Parameters:
            person1 (person): The initial infected person
            random_person (person): The person that person1 interacts with.

        """

        assert person.is_alive is True
        assert random_person.is_alive is True

        if random_person.is_vaccinated:
            pass
        elif random_person.infection:
            pass
        elif (random_person.infection is None and
              not random_person.is_vaccinated):
            num = random.random()
            if num < self.virus.repro_rate:
                random_person.infection = self.virus
                self.newly_infected.append(random_person._id)
                self.total_infected.insert(person._id, random_person._id)

    def run_and_collect(self, experiment):
        """This method should run the simulation until all requirements for
           ending the simulation are met.

           Parameters:
           experiment(Experiment): related to the TimeStep objects being made

           Returns:
           NoneType: just to mark where the method ends

        """
        results = list()  # return value
        time_step_counter = 1
        simulation_should_continue = 0
        should_continue = None
        assert self.population[0]._id == 0
        # collect data to make TimeStep instances as the simulation runs
        collection_data = list()
        while True:
            collection_data.append(
                self.create_time_step(time_step_counter, experiment))
            # decide to continue
            if self._simulation_should_continue():
                simulation_should_continue += 1
                break
            time_step_counter += 1
        # finally, add the tree of infection spread to the output
        collection_data.append(self.total_infected)
        return collection_data


if __name__ == "__main__":
    params = sys.argv[1:]
    pop_size = int(params[0])
    vacc_percentage = float(params[1])
    virus_name = str(params[2])
    mortality_rate = float(params[3])
    repro_rate = float(params[4])

    if len(params) == 6:
        initial_infected = int(params[5])
    else:
        initial_infected = 1

    virus = Virus(virus_name, repro_rate, mortality_rate)
    sim = Simulation(pop_size, vacc_percentage,  virus, initial_infected)
    graph = visualizer.WebVisualizer("Number of Survivors",
                                     ("Herd Immunity Defense Against Disease "
                                      + "Spread"))
    sim.run_and_collect(graph)
