# Herd Immunity Simulation
![Brandmark Image](https://i.postimg.cc/52ZwGXYG/Screen-Shot-2020-04-23-at-10-14-06-AM.png)

## Table of Contents
1. [The Why](#the-why)
2. [Goals](#goals)
    - [Rules](#rules)
    - [Suggested Analysis Questions](#suggested-analysis-questions)
3. [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Basic Structure](#basic-structure)
    - [Running Analysis Programs (CLI)](#running-analysis-programs-(cli))
    - [Installing Requirements](#installing-requirements)
    - [How to Contribute To This Project](#how-to-contribute-to-this-project)
4. [Running the Tests](#running-the-tests)
5. [Tech Stack](#tech-stack)
6. [Open Source License](#open-source-license)
7. [More Resources](#resources)
8. [Acknowledgements](#acknowledgements)

## The Why
We're going to create a basic simulation of herd immunity by modeling how a virus moves through a population where some (but not all) of a population is vaccinated against this virus.

## Goals
* Get your data for virus name, mortality rate, and reproductive rate from [this Guardian article](https://www.theguardian.com/news/datablog/ng-interactive/2014/oct/15/visualised-how-ebola-compares-to-other-infectious-diseases).  
* During every time step of the simulation, **every sick person** should randomly interact with **100 other people** in the population. The chance of a sick person infecting a person that they interact with is the virus's reproductive rate.  Example: if a virus has a reproductive rate of 15, then, on average, a sick person should infect 15 of the 100 people they interact with during that time step.

### Rules

1. A sick person only has a chance at infecting healthy, unvaccinated people they encounter.
1. An infected person cannot infect a vaccinated person.  This still counts as an interaction.  
1. An infected person cannot infect someone that is already infected.  This still counts as an interaction.
1. At the end of a time step, an infected person will either die of the infection or get better.  The chance they will die is the percentage chance stored in mortality_rate.  
1. For simplicity's sake, if the person does not die, we will consider them immune to the virus and change is_vaccinated to True when this happens.  
1. Dead people can no longer be infected, either.  Any time an individual dies, we should also change their .infected attribute to False.  
1. All state changes for a person should occur at the **end** of a time step, after all infected persons have finished all of their interactions.  
1. During the interactions, make note of any new individuals infected on this turn.  After the interactions are over, we will change the .infected attribute of all newly infected individuals to True.  1. Resolve the states of all individuals that started the turn infected by determining if they die or survive the infection, and change the appropriate attributes.  
1. The simulation should output a logfile that contains a record of every interaction that occurred during the simulation.  We will use this logfile to determine final statistics and answer questions about the simulation.

### Suggested Analysis Questions

Once you have successfully run a simulation, use your python skills to answer to analyze the simulation results
1. What were the inputs you gave the simulation? (Population size, percent vaccinated, virus name, mortality rate,  reproductive rate)
1. What percentage of the population became infected at some point before the virus burned out?
1.  What percentage of the population died from the virus?
1.  Out of all interactions sick individuals had during the entire simulation, how many total interactions did we see where a vaccination saved a person from potentially becoming infected?
<br>
<br>
*When you have answered these questions, please put your answers in a file called 'answers.txt' and commit this to your repo.*

## Getting Started
### Prerequisites
- Must have Git installed
- Must have a GitHub account
- Must have Python 3.7.* installed
- Must know how to work in a [Python virtual environment](https://realpython.com/python-virtual-environments-a-primer/)
(Docker should work as well, I've just never used it before)

## Basic Structure

The program consists of 4 classes: `Person`, `Virus`, `Simulation`, and `Logger`.

* `Simulation`: Highest level of abstraction. The main class that runs the entire simulation.
* `Person`: Represents the people that make up the population that the virus is spreading through.
* `Virus`: Models the properties of the virus we wish to simulate.
* `Logger`: A helper class for logging all events that happen in the simulation.

When you run `simulation.py` with the corresponding command-line arguments necessary for a simulation, a simulation object is created.  This simulation object then calls the `.run()` method.  This method should continually check if the simulation needs to run another step using a helper method contained in the class, and then call `.time_step()` if the simulation has not ended yet.  Within the `time_step()` method, you'll find all the logic necessary for actually simulating everything--that is, once you write it.  As is, the file just contains a bunch of method stubs, as well as numerous comments for explaining what you need to do to get everything working.

## Running Analysis Programs (CLI)

The program is designed to be run from the command line.  You can do this by running
`python3 simulation.py` followed by the command line arguments in the following order,
separated by spaces:
 {population size} {vacc_percentage} {virus_name} {mortality_rate} {repro_rate} {optional: number of people initially infected (default is 1)}

 Let's look at an example:
 * Population Size: 100,000
 * Vaccination Percentage: 90%
 * Virus Name: Ebola
 * Mortality Rate: 70%
 * Reproduction Rate: 25%
 * People Initially Infected: 10

 Then I would type: <br>
 `python3 simulation.py 100000 0.90 Ebola 0.70 0.25 10` in the terminal.

### Installing Requirements
  To ensure you have a development experience that's **as smooth as possible**, please follow these instructions:

  - Once you have activated your Python virtual environment, please be sure to run the following command from the command line, to ensure you have all the dependencies
  you may need to use for this project:
  ```
  python -m pip install -r requirements.txt
  ```
  - You may always double check the dependencies you have using this command:
  ```
  python -m pip list
  ```
  - If you install any new dependencies, please be sure to record them using
  ```
  python -m pip freeze > requirements.txt
  ```
  Thank you in advance for contributing to this project!

  ## Running the Tests
  Within the `fiercely-souvenir/travelly` directory, you can run the tests for this project from the command line, using:
  ```
  python manage.py test
  ```
  If you would like to add tests of your own and don't know how, please be sure to read the [Django 3.0 documentation on testing](https://docs.djangoproject.com/en/2.2/topics/testing/overview/#).
  If you are writing tests for the `api` package, you may also like to consult the [Django REST Framework documentation](https://www.django-rest-framework.org/api-guide/testing/).

### How to Contribute To This Project:
 These instructions will help you get a copy of the repository up and running on your local machine.
 - Fork this repository (click the "Fork" button at the top right of the page, then click on your profile image).
 - Clone your forked repository onto your local machine
 ```
 git clone https://github.com/<YOUR_GITHUB_USERNAME>/fiercely-souvenir.git
 ```
 - Start your virtual environment, and be sure to see the 'Installing Requirements' section below to make sure you have all the required dependencies!

 - Create a new branch for the feature you want to work on, or the bug fix you want to make:
 ```
 git checkout -b feature/branch-name or bugfix/branch-name
 ```
 - Make your changes (be sure to commit and push!)
 ```
 git add .
 git commit -m "[YOUR COMMIT MESSAGE HERE]"
 git push origin branch-name
 ```
 - Don't forget to add yourself to the [CONTRIBUTORS.md](CONTRIBUTORS.md) file!
 Please credit your own work, by adding your name to the list in this format:
 ```
 Name: [YOUR_NAME](Link to your GitHub Account, social media, or other personal link)
 About Me: 2-3 sentences to introduce yourself
 Feature: What did you contribute?
 Technologies: What did you use to build your contribution?
 Fun Fact: optional trivia about yourself!
 ```
 - Create new Pull Request from your forked repository - Click the "New Pull Request" button located at the top of your repo
 - Wait for your PR review and merge approval!
 - If you care about this work, then I humbly ask you to **please star this repository and spread the word with more developers! Thank you!**

## Running the Tests
 Tests are not implemented for this site at the moment. Please come back to this section later, I appreciate your patience.

## Tech Stack
 - Django - web framework for the backend
 - Bootstrap 4 - styling the front end
 - PostgreSQL - production database schema
 - Django REST Framework - framework building the API (found in the [web.api package](web/api/)).
 - AWS S3 - file storage for uploading static files

## Open Source License

## More Resources

## Acknowledgements
