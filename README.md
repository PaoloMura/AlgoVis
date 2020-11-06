# AlgoVis

## Project Overview

AlgoVis is a Python program that visualises some basic search and sort algorithms. It includes a minimalist home screen that allows the user to select the desired algorithm. On running this simulation, a random array of values is generated and displayed as a grid of cells. The user can then step forward or backward through the states of the algorithm by pressing 'Next' or 'Previous'. Pressing 'Next' advances the algorithm to its next state, updating the array and displaying information on what step the algorithm is currently performing. The 'New' button destroys the current simulation and generates a new simulation for the same chosen algorithm. The 'Home' button returns the user to the home screen where they can select a different algorithm.

## Project Specs

Python 3.8.2

Pygame 1.9.3

Tkinter (included with Python 3.7.0 or later)

To run AlgoVis, ensure the above are installed, download this repository and run the Home.py file.

## Background

I created this project for use in tutoring GCSE Computer Science students and to familiarise myself with OOP design patterns. The chosen algorithms are the ones common to GCSE exams. The OOP design patterns used include:

-the mediator pattern (as an interface between the algorithms and the UI)

-the memento pattern (to capture the state of the program, allowing use of a 'Previous' button)

-the factory method (for instantiating algorithms)
