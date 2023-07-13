## Importing the modules

import random

import entities
e = entities  # create a new instance of module entities

import visualiser
v = visualiser  # create a new instance of module visualiser

import results
simstat = results.SimulationStats()  # create a new instance of class SimulationStats in module results


## INITIALISATION

# Helper-function for initialisation of the world
def uniform_ones(width, height, ones):  # in 1D list
    """The function uniform ones creates a 1D list with a certain number of ones, which are uniformly distributed.
    Here, it is used to assign random positions for foxes and rabbits in the simulated world, so the width and the
    height correspond to the the west-east- and north-south-length of the world. The amount of ones is the initial
    size of rabbits or foxes."""
    sampling = []
    for o in range(ones):
        sampling.append(1)  # first the right amount of ones are added to the list
    for n in range(width * height - ones):
        sampling.append(0)  # then zeros are added to achieve the right length
    random.shuffle(sampling)  # list with ones and zeros in random order
    return sampling


# Main-function for initialisation
def initialisation(par):
    """This function takes care of all steps for initialising the simulation considering the saved parameters
    provided as an argument of the function."""
    patch_list = []  # empty list, that should contain all patches as 1D list

    # lists for initialisation of rabbits and foxes:
    rabbit_list_in = uniform_ones(par.world.west_east_length, par.world.north_south_length, par.rabbits.initial_size)
    fox_list_in = uniform_ones(par.world.west_east_length, par.world.north_south_length, par.foxes.initial_size)

    # lists for tracking and statistics of rabbits and foxes
    rl = []
    fl = []

    # add patches to the patch list as new instances (s) and include their coordinates
    for p in range(par.world.west_east_length * par.world.north_south_length):
        s = e.Patch(p % par.world.west_east_length, p // par.world.west_east_length)
        # comparing the current patch with the list for rabbits and foxes
        # add rabbit or fox with random age to the patch s, if entry in animal list == 1
        # add rabbit or fox to the tracking lists
        if rabbit_list_in[p] == 1:
            age = random.randint(0, par.rabbits.max_age) # random age as integer
            e.Rabbit(par.rabbits, s, age)  # to patch
            rl.append(e.Rabbit(par.rabbits, s, age))  # to tracking list
        if fox_list_in[p] == 1:
            age_fox = random.randint(0, par.foxes.max_age)  # random age as integer
            e.Fox(par.foxes, s, age_fox)  # to patch
            fl.append(e.Fox(par.foxes, s, age_fox))  # to tracking list
        patch_list.append(s)
    # return patch list and tracking lists as a list (compare function run(par))
    return [patch_list, rl, fl]


## UPDATE STEP 1 and 2

# Grass grows, animals age, consume energy and feed:
def ticking(patch_list):
    """This function lets the grass on the patches grow, animals age and consume energy. Animals die, when they reach the
    maximal age or due to starvation. The alive animals feed using resources on their current patch. The function
    takes the patch list as an argument to iterate through the patches and the animals located on the patches."""

    for p in patch_list:  # for every patch p in the patch list
        p.tick()  # grass grows
        animals = p.animals()  # create a list of the animals on the patch p
        for a in animals:  # for every animal a on the patch p
            a.tick()  # the animal ages and consumes energy or dies
            a.feed()  # the alive animal feeds


## UPDATE STEP 3 and 4

# Helper-function for reproduction and moving of the animals
def moving_patch(par, patch_list, i, a):
    """This function checks for possible patches around the specified patch with index i, that the animal a can move to
    or where an offspring can be located. The new patch can be north, east, south or west of the current patch and
    it needs to be free of animals of the same species and predators. The four possible directions get checked in a
    random order and the new patch gets returned. If there is no possible patch, the function returns None.
    The function works both for toroid and island. Besides the saved parameters for the simulation, the index of
    the patch i and the animal a, the function requires the patch list."""

    directions = [1, 2, 3, 4]  # list of the four possible directions
    random.shuffle(directions)  # list gets shuffled into a random order

    for d in directions:  # iterate through possible directions until new index is found or no more directions
        if d == 1:  # North
            if i >= par.world.west_east_length:
                # if the animal is not at the northern edge of the world
                # the new patch has index i - par.world.west_east_length in the 1D patch list
                if not a.same_species_in(patch_list[i - par.world.west_east_length]) and not a.predators_in(
                        patch_list[i - par.world.west_east_length]):
                    return patch_list[i - par.world.west_east_length]  # returns patch if it is free
            else:
                # if the animal is at the northern edge of the world
                if par.world.is_toroid:
                    # if the world is a toroid, it can appear on the southern edge of the world
                    # the new patch has index new_i in the patch list
                    new_i = par.world.area() - par.world.west_east_length + i
                    if not a.same_species_in(patch_list[new_i]) and not a.predators_in(patch_list[new_i]):
                        return patch_list[new_i]  # returns patch if it is free
                else:
                    # if the world is an island, the animal cannot move
                    pass

        elif d == 2:  # East
            if i % par.world.west_east_length != par.world.west_east_length - 1:
                # if the animal is not at the eastern edge of the world.
                # The new patch has index i + 1 in the patch list
                if not a.same_species_in(patch_list[i + 1]) and not a.predators_in(patch_list[i + 1]):
                    return patch_list[i + 1]  # returns patch if it is free
            else:
                # if the animal is at the eastern edge of the world
                if par.world.is_toroid:
                    # if the world is a toroid, it can appear at the western edge of the world
                    # the new patch has index new_i in the patch list
                    new_i = i - (par.world.west_east_length - 1)
                    if not a.same_species_in(patch_list[new_i]) and not a.predators_in(patch_list[new_i]):
                        return patch_list[new_i]  # returns patch if it is free
                else:
                    # if the world is an island, the animal cannot move
                    pass

        elif d == 3:  # South
            if i < par.world.area() - par.world.west_east_length:
                # if the animal is not at the southern edge of the world
                # the new patch has index i + par.world.west_east_length in the patch list
                if not a.same_species_in(patch_list[i + par.world.west_east_length]) and not a.predators_in(
                        patch_list[i + par.world.west_east_length]):
                    return patch_list[i + par.world.west_east_length]  # returns patch if it is free
            else:
                # if the animal is at the southern edge of the world
                if par.world.is_toroid:
                    # because it is a toroid, it can appear at the northern edge of the world
                    # the new patch has index new_i in the patch list
                    new_i = i - (par.world.area() - par.world.west_east_length)
                    if not a.same_species_in(patch_list[new_i]) and not a.predators_in(patch_list[new_i]):
                        return patch_list[new_i]  # returns patch if it is free
                else:
                    # if the world is an island, the animal cannot move
                    pass

        elif d == 4:  # West
            if i % par.world.west_east_length != 0:
                # if the animal is not at the western edge of the world.
                # The new patch has index i - 1 in the patch list
                if not a.same_species_in(patch_list[i - 1]) and not a.predators_in(patch_list[i - 1]):
                    return patch_list[i - 1]  # returns patch if it is free
            else:
                # if the animal is at the western edge of the world
                if par.world.is_toroid:
                    # because it is a toroid, it can appear at the eastern edge of the world
                    # the new patch has index new_i in the patch list
                    new_i = i + (par.world.west_east_length - 1)
                    if not a.same_species_in(patch_list[new_i]) and not a.predators_in(patch_list[new_i]):
                        return patch_list[new_i]  # returns patch if it is free
                else:
                    # if the world is an island, the animal cannot move
                    pass


# Main function for reproduction and moving of the animals:
def reproduction_moving(par, patch_list, rl, fl):
    """This function lets the animals reproduce, if they reached minimal reproduction age and energy.
    If they cannot reproduce, they can move instead. Both actions require an empty patch close to the animal.
    Besides the saved parameters for the simulation, the function requires the patch list and the tracking lists
    for foxes and rabbits."""

    for i in range(len(patch_list)):  # for every patch in the patch list (i as index)
        animals = patch_list[i].animals()  # create a list for the animals on the patch
        for a in animals:  # for every animal on the patch
            if a.is_alive() and a.can_reproduce():  # if animal can reproduce
                try:
                    offspring = a.reproduce(moving_patch(par, patch_list, i, a))  # moving_patch returns the patch,
                    # where the newborn should be located or None
                    if offspring != None:
                        if type(a) == e.Rabbit:  # if newborn is a rabbit
                            rl.append(offspring)  # newborn is added to tracking list of rabbits
                        elif type(a) == e.Fox:  # if newborn is a fox
                            fl.append(offspring)  # newborn is added to tracking list of foxes
                except AttributeError:  # adding "None" causes error
                    pass  # skip and go to next animal instead

            elif a.is_alive(): # if animal cannot reproduce
                try:
                    a.move_to(moving_patch(par, patch_list, i, a))  # moving_patch returns the patch,
                    # that the animal can move to or None
                except AttributeError:  # moving to "None" causes error
                    pass  # skip and go to next animal instead


## COLLECTION OF STATISTICS

# Statistic 4 (The average energy level of the combined and separate populations at each time step)
def energy_statistics(par, rl, fl):
    """This function calculates the average energy level of the combined and separate populations at each time step.
    It takes an instance of class parameters.Simulation and lists containing all rabbits and foxes as arguments.
    It adds the results of the calculation to the corresponding list of class results.SimulationStats."""
    E_rab = 0
    try:
        for r in rl:  # changed from index to element!
            if r.is_alive():
                E_rab += r.energy()
        avrE_rab = E_rab / simstat.rabbits.size_per_step[-1]  # average energy
        relE_rab = avrE_rab / par.rabbits.max_energy  # relative energy to the maximum energy level
        simstat.rabbits.avg_energy_per_step.append(relE_rab)
    except ZeroDivisionError:  # when rabbit goes extinct, then 'simstat.rabbits.size_per_step[-1]' = 0
        relE_rab = 0
        simstat.rabbits.avg_energy_per_step.append(relE_rab)

    E_fox = 0
    try:
        for f in fl:  # changed from index to element!
            if f.is_alive():
                E_fox += f.energy()
        avrE_fox = E_fox / simstat.foxes.size_per_step[-1]  # average energy
        relE_fox = avrE_fox / par.foxes.max_energy  # relative energy to the maximum energy level
        simstat.foxes.avg_energy_per_step.append(relE_fox)
    except ZeroDivisionError:  # when fox goes extinct, then 'simstat.foxes.size_per_step[-1]' = 0
        relE_fox = 0
        simstat.foxes.avg_energy_per_step.append(relE_fox)

    simstat.avg_energy_per_step.append((relE_rab + relE_fox) / 2)



def collection(par, patch_list, rl, fl):
    """This function collects all the statistics, that need to be obtained after finishing the simulation. It takes an
    instance of class parameters.Simulation as argument as well as lists containing all patches and all foxes and
    rabbits. It then adds the statistics to the corresponding list in class results.Simulationstats."""

    # Statistic 1 (The total size of each population over the entire execution of the simulation)
    simstat.rabbits.total = len(rl)  # Rabbit
    simstat.foxes.total = len(fl)  # Fox

    # Statistic 3 (The age at the time of death of each individual)
    # Statistic 5 (The total of deaths by each cause)
    # Rabbits
    for r in rl:  # for every rabbit in rabbit list
        if not r.is_alive():  # if it is dead
            simstat.rabbits.age_at_death.append(r.age())  # add the age to the list, then check cause of death
            if r.was_killed():
                simstat.rabbits.dead_by_predation += 1
            elif r.energy() <= 0:
                simstat.rabbits.dead_by_starvation += 1
            elif r.age() >= par.rabbits.max_age:
                simstat.rabbits.dead_by_old_age += 1
    # Foxes
    for f in fl:  # for every fox in fox list
        if not f.is_alive():  # if it is dead
            simstat.foxes.age_at_death.append(f.age())  # add the age to the list, then check cause of death
            if f.energy() <= 0:
                simstat.foxes.dead_by_starvation += 1
            elif f.age() >= par.foxes.max_age:
                simstat.foxes.dead_by_old_age += 1

    # Statistic 6 (The number of deaths by predation on each patch of the grid)
    for i in range(par.world.north_south_length):  # add as many inner lists as number of "rows" in the world
        simstat.kills_per_patch.append([])

    count = 0  # set number of death count to zero
    for p in patch_list:  # for every patch in patch list
        for r in rl:  # iterate through rabbit list
            if r.was_killed() and r.patch() == p:  # if rabbit r was killed on the patch p
                count += 1  # increase number of death counts for patch p
        co = p.coordinates()  # get x and y coordinates of patch p as a tuple, y equals "row" of the world
        simstat.kills_per_patch[co[1]].append(count)  # add number of deaths to inner list of kills_per_patch list
        count = 0  # set count back to 0 and continue with next patch


## EXECUTION OF THE SIMULATION

# Helper-functions for running the simulation:
def check_species(patch_list):
    alive_rabbits = 0  # set number of alive rabbits to zero
    maybe_rabbit = False  # until an alive rabbit is found, maybe rabbit should be False
    alive_foxes = 0  # set number of alive foxes to 0
    maybe_fox = False  # until an alive fox is found, maybe fox should be False

    for p in patch_list:
        if p.has_alive_rabbit():
            maybe_rabbit = True  # maybe rabbits is True, when an alive rabbit is found
            alive_rabbits += 1  # the number of alive rabbits increases
        if p.has_alive_fox():
            maybe_fox = True  # maybe fox is True, when an alive fox is found
            alive_foxes += 1  # the number of alive foxes increases
    simstat.rabbits.size_per_step.append(alive_rabbits)  # Statistic 2, add the number of alive rabbits
    simstat.foxes.size_per_step.append(alive_foxes)  # Statistic 2, add the number of alive foxes
    if not maybe_rabbit and not maybe_fox:
        return False
    else:
        return True


# Main-function for running the simulation:
def run(par):
    """This function is the main function for running the simulation. It takes an instance of class parameters.Simulation
     as an argument and goes through initialisation, updating and data collection of the simulation."""

    # Initialisation:
    par_init = initialisation(par)  # returns a list of initial parameters
    patch_list = par_init[0]  # get patch list of initialisation
    rl = par_init[1]  # get rabbit list of initialisation
    fl = par_init[2]  # get fox list of initialisation

    # Visualisation:
    if par.execution.batch:  # for simulation modality batch
        graphics = v.Batch(par.execution.max_steps)
    else:  # for simulation modality visual
        graphics = v.ColourGraphics(par.execution.max_steps, patch_list, par.world.west_east_length,
                                    par.world.north_south_length, par.execution.step_delay, True)
    graphics.start()  # start visualisation
    graphics.update(0)  # update visualisation
    simstat.steps = 1  # set simulation steps to one

    # Updating and statistics:
    species_alive = check_species(patch_list)
    energy_statistics(par, rl, fl)  # get average energy levels for statistics
    # Only update, if under maximum simulation steps and both species still exist
    while simstat.steps <= par.execution.max_steps and species_alive:
        ticking(patch_list)  # animals are aging and consuming energy (eventually dying)
        reproduction_moving(par, patch_list, rl, fl)  # animals reproduce or move if patch is available
        graphics.update(simstat.steps)  # the graphics updates
        energy_statistics(par, rl, fl)  # get average energy levels for statistics
        species_alive = check_species(patch_list)
        simstat.steps += 1  # go to next simulation step

    # Statistics and end of visualisation:
    collection(par, patch_list, rl, fl)  # collect different statistics
    graphics.stop()  # stop visualisation
    return simstat
