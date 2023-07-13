import sys
import simulation
import reporting
import parameters

# New instance of class simulation
s = parameters.Simulation()


##Configuration
#Quick parameters and first action selection

def default_parameters():
    """This function shows the default parameters at the start of the program."""
    print("These are the quick parameters:\n"
          "Shape and size of the world:", s.world, "\n"
          "Initial size of the rabbit population:", s.rabbits.initial_size, "\n"
          "Initial size of the fox population:", s.foxes.initial_size, "\n"
          "Maximum number of simulation steps:", s.execution.max_steps, "\n"
          "True for batch and False for visual Simulation Modality:", s.execution.batch, "\n")


def actions():
    """This function lets the user choose a possible action."""
    print("These are the possible actions: \n"
          "1 for Display parameters \n"
          "2 for Quick Setup \n"
          "3 for Advanced Setup \n"
          "4 for Run \n"
          "5 for Quit \n")
    action = input("Choose an action:")
    if action == "1":
        display_parameters()
    elif action == "2":
        quick_setup()
    elif action == "3":
        advanced_setup_actions()
    elif action == "4":
        results = simulation.run(s)
        report(results)
        # save results and lead to reporting
    elif action == "5":
        sys.exit()
    else:
        print("This is not a valid action.")
        actions()


## Display all parameters
def display_parameters():
    """This function prints all parameters."""
    print("These are the parameters:\n"
          "World: \n"
          "Shape and size of the world:", s.world, "\n"
          "Rabbit population: \n"
          "Initial size of the rabbit population:", s.rabbits.initial_size, "\n"
          "Maximum age of the rabbit population:", s.rabbits.max_age, "\n"
          "Metabolism of the rabbit population:", s.rabbits.metabolism, "\n"
          "Maximum energy of the rabbit population:", s.rabbits.max_energy, "\n"
          "Minimum reproduction age of the rabbit population:", s.rabbits.reproduction_min_age, "\n"
          "Minimum reproduction energy of the rabbit population:", s.rabbits.reproduction_min_energy, "\n"
          "Reproduction probability of the rabbit population:", s.rabbits.reproduction_probability, "\n"
          "Fox population: \n"
          "Initial size of the fox population:", s.foxes.initial_size, "\n"
          "Maximum age of the fox population:", s.foxes.max_age, "\n"
          "Metabolism of the fox population:", s.foxes.metabolism, "\n"
          "Maximum energy of the fox population:", s.foxes.max_energy, "\n"
          "Minimum reproduction age of the fox population:", s.foxes.reproduction_min_age, "\n"
          "Minimum reproduction energy of the fox population:", s.foxes.reproduction_min_energy, "\n"
          "Reproduction probability of the fox population:", s.foxes.reproduction_probability, "\n"
          "Execution: \n"
          "Maximum number of simulation steps:", s.execution.max_steps, "\n"
          "True for batch and False for visual Simulation Modality:", s.execution.batch, "\n"
          "Step delay in seconds:", s.execution.step_delay, "\n")
    actions()


##Quick setup
def quick_setup():
    """This function lets the user choose the main parameters.
    To choose more parameters, the user should use the advanced setup. """

    # Size of the world
    def north_south():
        """This function checks, whether the entered north south length is valid. It needs to be a positive integer."""
        try:
            ns = int(input("Enter north south length as integer:"))
            if ns > 0:
                s.world.north_south_length = ns
            else:
                print("This is not a valid north south length.")
                north_south()
        except ValueError:
            print("This is not a valid north south length.")
            north_south()
    north_south()

    def east_west():
        """This function checks, whether the entered east west length is valid. It needs to be a positive integer."""
        try:
            ew = int(input("Enter east west length as integer:"))
            if ew > 0:
                s.world.west_east_length = ew
            else:
                print("This is not a valid east west length.")
                east_west()
        except ValueError:
            print("This is not a valid east west length.")
            east_west()
    east_west()

    # Size of the populations
    def size_rabbits():
        """This function checks, whether the entered initial size of the rabbit population is valid.
         It has to be a positive integer, that is smaller or equal to the size of the world."""
        try:
            size = int(input("Enter the initial size of the rabbit population as integer:"))
            if size > 0 and size <= s.world.area():
                s.rabbits.initial_size = size
            else:
                print("This is not a valid size.")
                size_rabbits()
        except ValueError:
            print("This is not a valid size.")
            size_rabbits()
    size_rabbits()

    def size_foxes():
        """This function checks, whether the entered initial size of the fox population is valid.
        It has to be a positive integer, that is smaller or equal to the size of the world."""
        try:
            size = int(input("Enter the initial size of the fox population as integer:"))
            if size > 0 and size <= s.world.area():
                s.foxes.initial_size = size
            else:
                print("This is not a valid size.")
                size_foxes()
        except ValueError:
            print("This is not a valid size.")
            size_foxes()
    size_foxes()

    # Maximum number of simulation steps
    def max_steps():
        """This function lets the user choose a maximum number of simulation steps.
        It has to be a positive integer."""
        try:
            max = int(input("Enter maximum number of simulation steps as integer:"))
            if max > 0:
                s.execution.max_steps = max
            else:
                print("This is not a valid number of simulation steps.")
                max_steps()
        except ValueError:
            print("This is not a valid number of simulation steps.")
            max_steps()
    max_steps()

    # Simulation modality
    def modality_choice():
        """This function lets the user choose a simulation modality.
        It has to be either 1 for batch or 2 for visual modality.."""
        modality = input("Choose 1 for batch or 2 for visual simulation modality:")
        if modality == "1":
            s.execution.batch == True
        elif modality == "2":
            s.execution.batch == False
        else:
            print("You have to choose 1 or 2.")
            modality_choice()
    modality_choice()
    print("You successfully changed the quick parameters.")
    actions()


##Advanced setup
# Advanced setup - Action selection
def advanced_setup_actions():
    """This function lets the user choose an action."""
    print("These are the possible advanced setup actions: \n"
          "1 for World \n"
          "2 for Rabbit population \n"
          "3 for Fox population \n"
          "4 for Execution \n"
          "5 for Done / Go back \n")
    advanced_action = input("Choose an action:")
    if advanced_action == "1":
        advanced_setup_world()
    elif advanced_action == "2":
        advanced_setup_rabbits()
    elif advanced_action == "3":
        advanced_setup_foxes()
    elif advanced_action == "4":
        advanced_setup_execution()
    elif advanced_action == "5":
        actions()
    else:
        print("This is not a valid action.")
        advanced_setup_actions()


# Advanced setup - World
def advanced_setup_world():
    """This function lets the user choose the size and the shape of the world."""
    # Size of the world
    def north_south():
        """This function checks, whether the entered north south length is valid. It needs to be a positive integer."""
        try:
            ns = int(input("Enter north south length as integer:"))
            if ns > 0:
                s.world.north_south_length = ns
            else:
                print("This is not a valid north south length.")
                north_south()
        except ValueError:
            print("This is not a valid north south length.")
            north_south()
    north_south()

    def east_west():
        """This function checks, whether the entered east west length is valid. It needs to be a positive integer."""
        try:
            ew = int(input("Enter east west length as integer:"))
            if ew > 0:
                s.world.west_east_length = ew
            else:
                print("This is not a valid east west length.")
                east_west()
        except ValueError:
            print("This is not a valid east west length.")
            east_west()
    east_west()

    # Shape of the world
    def shape_world():
        """This function lets the user choose the shape of the world.
        It has to be either 1 for toroid or 2 for island."""
        shape = input("Choose 1 for toroid or 2 for island:")
        if shape == "1":
            s.world.is_toroid = True
        elif shape == "2":
            s.world.is_toroid = False
        else:
            print("You have to choose either 1 or 2.")
            shape_world()
    shape_world()
    advanced_setup_actions()


# Advanced setup - Rabbit population
def advanced_setup_rabbits():
    """This function lets the user choose the parameters for the rabbit population."""

    def initial_size_rabbits():
        """This function checks, whether the entered initial size of the rabbit population is valid.
         It has to be a positive integer, that is smaller or equal to the size of the world."""
        try:
            size = int(input("Enter the initial size of the rabbit population as integer:"))
            if size > 0:
                if size <= s.world.area():
                    s.rabbits.initial_size = size
            else:
                print("This is not a valid size.")
                initial_size_rabbits()
        except ValueError:
            print("This is not a valid size.")
            initial_size_rabbits()
    initial_size_rabbits()

    def max_age_rabbits():
        """This function checks, whether the entered maximum age of a rabbit is valid.
        It has to be a positive integer."""
        try:
            age = int(input("Enter the maximum age of a rabbit as integer:"))
            if age > 0:
                s.rabbits.max_age = age
            else:
                print("This is not a valid age.")
                max_age_rabbits()
        except ValueError:
            print("This is not a valid age.")
            max_age_rabbits()
    max_age_rabbits()

    def metabolism_rabbits():
        """This function checks, whether the entered consumed energy of a rabbit during each simulation step is valid.
        It has to be a non-negative integer."""
        try:
            meta = int(input("Enter the consumed energy of a rabbit during each simulation step as integer:"))
            if meta >= 0:
                s.rabbits.metabolism = meta
            else:
                print("This is not a valid metabolism.")
                metabolism_rabbits()
        except ValueError:
            print("This is not a valid metabolism.")
            metabolism_rabbits()
    metabolism_rabbits()

    def max_energy_rabbits():
        """This function checks, whether the entered maximum energy level of a rabbit is valid.
        It has to be a positive integer."""
        try:
            max = int(input("Enter the maximum energy level of a rabbit as integer:"))
            if max > 0:
                s.rabbits.max_energy = max
            else:
                print("This is not a valid level of energy.")
                max_energy_rabbits()
        except ValueError:
            print("This is not a valid level of energy.")
            max_energy_rabbits()
    max_energy_rabbits()

    def reproduction_min_age_rabbits():
        """This function checks, whether the entered minimum age for reproduction of a rabbit is valid.
        It has to be a positive integer."""
        try:
            min = int(input("Enter the minimum energy for reproduction of a rabbit as integer:"))
            if min > 0:
                s.rabbits.reproduction_min_age = min
            else:
                print("This is not a valid minimum age for reproduction.")
                reproduction_min_age_rabbits()
        except ValueError:
            print("This is not a valid minimum energy for reproduction.")
            reproduction_min_age_rabbits()
    reproduction_min_age_rabbits()

    def reproduction_min_energy_rabbits():
        """This function checks, whether the entered minimum energy for reproduction of a rabbit is valid.
        It has to be a positive integer."""
        try:
            min = int(input("Enter the minimum energy for reproduction of a rabbit as integer:"))
            if min > 0:
                s.rabbits.reproduction_min_energy = min
            else:
                print("This is not a valid minimum energy for reproduction.")
                reproduction_min_energy_rabbits()
        except ValueError:
            print("This is not a valid minimum energy for reproduction.")
            reproduction_min_energy_rabbits()
    reproduction_min_energy_rabbits()

    def reproduction_probability_rabbits():
        """This function checks, whether the entered reproduction probability of a rabbit is valid.
        It has to be a float between 0 and 1."""
        try:
            rep_pro = float(input("Enter the reproduction probability of a rabbit as a float between 0 and 1:"))
            if rep_pro >= 0 and rep_pro <= 1:
                s.rabbits.reproduction_probability = rep_pro
            else:
                print("This is not a valid reproduction probability.")
                reproduction_probability_rabbits()
        except ValueError:
            print("This is not a valid reproduction probability.")
            reproduction_probability_rabbits()
    reproduction_probability_rabbits()
    advanced_setup_actions()


# Advanced setup - Fox population
def advanced_setup_foxes():
    """This function lets the user choose the parameters for the fox population."""

    def initial_size_foxes():
        """This function checks, whether the entered initial size of the fox population is valid.
         It has to be a positive integer, that is smaller or equal to the size of the world."""
        try:
            size = int(input("Enter the initial size of the fox population as integer:"))
            if size > 0 and size <= s.world.area():
                s.foxes.initial_size = size
            else:
                print("This is not a valid size.")
                initial_size_foxes()
        except ValueError:
            print("This is not a valid size.")
            initial_size_foxes()
    initial_size_foxes()

    def max_age_foxes():
        """This function checks, whether the entered maximum age of a fox is valid.
        It has to be a positive integer."""
        try:
            age = int(input("Enter the maximum age of a fox as integer:"))
            if age > 0:
                s.foxes.max_age = age
            else:
                print("This is not a valid age.")
                max_age_foxes()
        except ValueError:
            print("This is not a valid age.")
            max_age_foxes()
    max_age_foxes()

    def metabolism_foxes():
        """This function checks, whether the entered consumed energy of a fox during each simulation step is valid.
        It has to be a non-negative integer."""
        try:
            meta = int(input("Enter the consumed energy of a fox during each simulation step as integer:"))
            if meta >= 0:
                s.foxes.metabolism = meta
            else:
                print("This is not a valid metabolism.")
                metabolism_foxes()
        except ValueError:
            print("This is not a valid metabolism.")
            metabolism_foxes()
    metabolism_foxes()

    def max_energy_foxes():
        """This function checks, whether the entered maximum energy level of a fox is valid.
        It has to be a positive integer."""
        try:
            max = int(input("Enter the maximum energy level of a rabbit as integer:"))
            if max > 0:
                s.foxes.max_energy = max
            else:
                print("This is not a valid level of energy.")
                max_energy_foxes()
        except ValueError:
            print("This is not a valid level of energy.")
            max_energy_foxes()
    max_energy_foxes()

    def reproduction_min_age_foxes():
        """This function checks, whether the entered minimum age for reproduction of a fox is valid.
        It has to be a positive integer."""
        try:
            min = int(input("Enter the minimum energy for reproduction of a fox as integer:"))
            if min > 0:
                s.foxes.reproduction_min_age = min
            else:
                print("This is not a valid minimum age for reproduction.")
                reproduction_min_age_foxes()
        except ValueError:
            print("This is not a valid minimum energy for reproduction.")
            reproduction_min_age_foxes()
    reproduction_min_age_foxes()

    def reproduction_min_energy_foxes():
        """This function checks, whether the entered minimum energy for reproduction of a fox is valid.
        It has to be a positive integer."""
        try:
            min = int(input("Enter the minimum energy for reproduction of a fox as integer:"))
            if min > 0:
                s.foxes.reproduction_min_energy = min
            else:
                print("This is not a valid minimum energy for reproduction.")
                reproduction_min_energy_foxes()
        except ValueError:
            print("This is not a valid minimum energy for reproduction.")
            reproduction_min_energy_foxes()
    reproduction_min_energy_foxes()

    def reproduction_probability_foxes():
        """This function checks, whether the entered reproduction probability of a fox is valid.
        It has to be a float between 0 and 1."""
        try:
            rep_pro = float(input("Enter the reproduction probability of a fox as a float between 0 and 1:"))
            if rep_pro >= 0 and rep_pro <= 1:
                s.foxes.reproduction_probability = rep_pro
            else:
                print("This is not a valid reproduction probability.")
                reproduction_probability_foxes()
        except ValueError:
            print("This is not a valid reproduction probability.")
            reproduction_probability_foxes()
    reproduction_probability_foxes()
    advanced_setup_actions()


# Advanced setup - Execution
def advanced_setup_execution():
    """This function lets the user choose the parameters for the execution."""

    # Maximum number of simulation steps
    def max_steps():
        """This function lets the user choose a maximum number of simulation steps.
        It has to be a positive integer."""
        try:
            max = int(input("Enter maximum number of simulation steps as integer:"))
            if max > 0:
                s.execution.max_steps = max
            else:
                print("This is not a valid number of simulation steps.")
                max_steps()
        except ValueError:
            print("This is not a valid number of simulation steps.")
            max_steps()
    max_steps()

    # Simulation modality
    def modality_choice():
        """This function lets the user choose a simulation modality.
        It has to be either 1 for batch or 2 for visual modality.."""
        modality = input("Choose 1 for batch or 2 for visual simulation modality:")
        if modality == "1":
            s.execution.batch == True
        elif modality == "2":
            s.execution.batch == False
        else:
            print("You have to choose 1 or 2.")
            modality_choice()
    modality_choice()

    #Step delay
    def step_delay():
        """This function lets the user choose a step delay. It has to be a positive float."""
        try:
            delay = float(input("Enter the step delay in seconds:"))
            if delay > 0:
                s.execution.step_delay = delay
            else:
                print("This is not a valid step delay.")
                step_delay()
        except ValueError:
            print("This is not a valid step delay.")
            step_delay()
    step_delay()
    advanced_setup_actions()


## Reporting
def report(result_input):
    """This is a function that makes reports based on the simulation results."""

    print("\n"
          "Choose an action for your report: \n"
          "1 for Print summary \n"
          "2 for Plot pop. size / time \n"
          "3 for Plot lifespan \n"
          "4 for Plot energy \n"
          "5 for Plot kills distribution \n"
          "6 for Quit \n")
    action = input("Choose an action:")

    if action == "1":
        reporting.print_summary(result_input)
    elif action == "2":
        reporting.plot_pop_size(result_input)
    elif action == "3":
        reporting.plot_lifespan(result_input)
    elif action == "4":
        reporting.plot_energy(result_input)
    elif action == "5":
        reporting.plot_kills(result_input)
    elif action == "6":
        sys.exit()
    else:
        print("This is not a valid action. Choose a number between 1 and 6.")
    report(result_input)


if __name__ == "__main__":
    print("Foxes and Rabbits - A predator prey model.", '\n')
    default_parameters()
    actions()
