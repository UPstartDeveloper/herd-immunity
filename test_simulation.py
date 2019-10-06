import unittest
import random
import sys
from person import Person
from logger import Logger
from virus import Virus
from simulation import *

random.seed(42)


class TestSimulation(unittest.TestCase):
    def test__init__(self):
        """Test values passed into Simulation instance properties at
           instantiation."""
        # test virus
        virus = Virus("HIV", 0.8, 0.3)
        # test instances with and without args for initial infected
        sim_no_arg = Simulation(1000, 0.05, virus)
        sim_yes_arg = Simulation(1000, 0.05, virus, 10)

        assert sim_no_arg.pop_size == sim_yes_arg.pop_size == 1000
        assert sim_no_arg.vacc_percentage == sim_yes_arg.vacc_percentage == .05
        assert sim_no_arg.initial_infected == 1
        assert sim_yes_arg.initial_infected == 10
        assert sim_no_arg.virus == sim_yes_arg.virus == virus
        # self.population cannot be tested, because assigned using random
        assert sim_no_arg.file_name == ("HIV_simulation_pop_1000_vp_0.05_" +
                                        "infected_1.txt")
        assert sim_yes_arg.file_name == ("HIV_simulation_pop_1000_vp_0.05_" +
                                         "infected_10.txt")
        test_file_no_arg = open(sim_no_arg.file_name, "r")
        assert test_file_no_arg.read() == ("Population size: 1000" +
                                           "\tVaccination percentage: 0.05	" +
                                           "Virus name: HIV	Mortality rate: " +
                                           "0.3	Basic reproduction " +
                                           "number: 0.8\n")
        test_file_no_arg.close

    def test_get_infected(self):
        """Test list returned by get_infected to ensure it only contains
           people who are both alive and infected."""
        virus = Virus("HIV", 0.8, 0.3)
        sim = Simulation(1000, 0.05, virus)
        alive_infected = sim.get_infected()  # stores value returned by method

        count = 0
        for person in alive_infected:
            if person.infection and person.is_alive:
                count += 1
        assert count == len(alive_infected)


if __name__ == "__main__":
    unittest.main()
