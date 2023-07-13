import parameters
import random

from typing import Optional, Tuple, List


class Patch:
    """A patch of grass at a given pair of coordinates."""

    min_grass_growth = 1
    max_grass_growth = 4
    max_grass_amount = 30

    def __init__(self, x: int, y: int):
        """x is the west-east- and y the north-south-coordinate."""
        # private and not changeable:
        self._coordinates = (x, y)
        # not private, so it can be changed in the classes Animal, Foxes and Rabbits
        self.grass_amount = random.randrange(
            round(Patch.max_grass_amount * 0.3), Patch.max_grass_amount)
        self.fox = None  # cannot contain more than one. Dead animals are saved in lists in module simulation
        self.rabbit = None

    def coordinates(self) -> Tuple[int, int]:
        """Returns coordinates of the patch as a tuple."""
        return self._coordinates

    def grass(self) -> int:
        """Returns grass amount of the patch."""
        return self.grass_amount

    def tick(self):
        """Increases the amount of grass on the Patch by a value between min grass growth and max grass growth.
        It cannot grow over the max grass amount."""
        self.grass_amount = self.grass_amount + \
            random.randint(Patch.min_grass_growth, Patch.max_grass_growth)
        if self.grass_amount > Patch.max_grass_amount:
            self.grass_amount = Patch.max_grass_amount

    def add(self, animal):
        """This function adds an animal to the patch."""
        if isinstance(animal, Fox):
            self.fox = animal
        elif isinstance(animal, Rabbit):
            self.rabbit = animal

    def remove(self, animal):
        """This function removes an animal from the patch."""
        if isinstance(animal, Fox):
            self.fox = None
        elif isinstance(animal, Rabbit):
            self.rabbit = None

    def has_alive_fox(self) -> bool:
        """This function checks, if there is an alive fox on the patch."""
        if self.fox != None and self.fox.is_alive():
            return True
        return False

    def has_alive_rabbit(self) -> bool:
        """This function checks, if there is an alive rabbit on the patch."""
        if self.rabbit != None and self.rabbit.is_alive():
            return True
        return False

    def animals(self) -> List:
        """This function returns a list of the animals on the patch."""
        animals = []
        if self.fox != None:
            animals.append(self.fox)
        else:
            pass
        if self.rabbit != None:
            animals.append(self.rabbit)
        else:
            pass
        return animals

    def __str__(self) -> str:
        return f"""Patch:
    coordinates       {self.coordinates()}
    grass:            {self.grass()}
    has alive fox:    {self.has_alive_fox()}
    has alive rabbit: {self.has_alive_rabbit()}
    """


class Animal:
    """
    A generic animal in the simulation. See classes Fox and Rabbit.
    """

    def __init__(self, population: parameters.Population, patch: Patch, energy: int, age: int):
        self._population = population
        self._patch = patch
        self._energy = energy
        self._age = age
        self._patch.add(self)

    def age(self) -> int:
        """ Returns the age of the animal. The value does not change after the death of the animal."""
        return self._age

    def energy(self) -> int:
        """Returns the energy of the animal. The value does not change after the death of the animal."""
        return self._energy

    def patch(self) -> Patch:
        """Returns the position of the animal. The value does not change after the death of the animal."""
        return self._patch

    def can_reproduce(self) -> bool:
        """Returns True if the animal is alive, is old enough, and has enough energy to reproduce, False otherwise."""
        if self.is_alive() and self._age >= self._population.reproduction_min_age and self._energy >= self._population.reproduction_min_energy:
            return True
        return False

    def tick(self):
        """Records the passage of time(one step in the simulation).
        If the animal is alive, it ages and consumes its energy.
        If the animal becomes too old or depletes its energy reserve, it dies and it is removed from its current patch."""
        if self.is_alive():
            self._age += 1
            self._energy -= self._population.metabolism
            if self._age > self._population.max_age or self._energy < 0:
                # animal is dead now and gets removed from the patch
                self._patch.remove(self)

    def move_to(self, patch: Patch):
        """If the animal is alive, it goes from its current patch to the given one.
        The method assumes that the given patch is different from the current one and that it does not contain (alive)
        animals of the same species of this animal. Patches are updated accordingly."""
        if self.is_alive():
            assert self._patch != patch
            assert self.same_species_in(patch) == False
            self._patch.remove(self)  # remove from current patch
            patch.add(self)  # add to new patch
            self._patch = patch  # save new patch for the animal

    def same_species_in(self, patch: Patch) -> bool:
        """Return True if the given patch contains an alive animal of the same species."""
        same_species = False
        if isinstance(self, Rabbit):
            if patch.has_alive_rabbit():
                same_species = True
        elif isinstance(self, Fox):
            if patch.has_alive_fox():
                same_species = True
        return same_species

    def is_alive(self) -> bool:
        """Returns True if the animal is alive, False otherwise."""
        alive = False
        if self._age <= self._population.max_age and self._energy > 0:
            if isinstance(self, Fox):
                alive = True
            elif isinstance(self, Rabbit) and not self._killed:
                alive = True
        return alive

    def predators_in(self, patch: Patch) -> bool:
        """Returns True if the given patch contains an alive predator of this animal."""
        if isinstance(self, Rabbit) and patch.has_alive_fox():
            return True
        return False

    # Functions in subclasses
    # They use subclass specific attributes
    def feed(self):
        """Feeds itself using the resources at its current location(patch), if it is alive."""
        pass

    def reproduce(self, newborn_patch: Patch) -> Optional['Animal']:
        """If the animal is alive, it tries to reproduce using the patch provided.
        Returns an instance for the newborn(located at `newborn_patch`) or None.
        Patches are updated accordingly."""
        pass


class Rabbit(Animal):
    """
    A rabbit in the simulated world.
    """

    feeding_metabolism_rate = 2.5
    reproduction_cost_rate = 0.9

    def __init__(self, population: parameters.Population, patch: Patch, age: int):
        """
        population: the parameters for the rabbit population used in this run of the simulation.
        patch: the position assigned to this animal(the constructor takes care of adding it to the list of animals of this patch).
        age: the current age of the animal.
        """
        energy = round(population.max_energy * 0.25)
        super().__init__(population, patch, energy, age)
        self._killed = False

    def feed(self):
        """Feeds itself using the resources at its current location(patch), if it is alive."""
        if self.is_alive() and self._energy < self._population.max_energy:
            # if the amount of grass is smaller than the total metabolism, rabbit can maximum gain the energy of the existing grass
            if self._patch.grass_amount <= self._population.metabolism * self.feeding_metabolism_rate:
                self._energy += self._patch.grass_amount
                self._patch.grass_amount = 0
                if self._energy > self._population.max_energy:
                    self._energy = self._population.max_energy
            else:
                self._energy += self._population.metabolism * self.feeding_metabolism_rate
                self._patch.grass_amount -= self._population.metabolism * self.feeding_metabolism_rate
                if self._energy > self._population.max_energy:
                    self._energy = self._population.max_energy

    def reproduce(self, newborn_patch: Patch) -> Optional['Rabbit']:
        """If the animal is alive, it tries to reproduce using the patch provided.
        Returns an instance for the newborn(located at `newborn_patch`) or None.
        Patches are updated accordingly."""
        if random.random() > self._population.reproduction_probability:
            self._energy -= self._population.reproduction_min_energy * self.reproduction_cost_rate
            return Rabbit(self._population, newborn_patch, age=0)
        return None

    # Rabbit specific functions
    def kill(self):
        """If the rabbit is alive, it kills it and removes it from its patch."""
        self._killed = True
        self._patch.remove(self)

    def was_killed(self) -> bool:
        """True if the rabbit was killed(see method kill)."""
        return self._killed

    def __str__(self) -> str:
        if self.is_alive():
            st = "alive"
        else:
            st = "dead"
        return f"""Rabbit:
        position: {self.patch().coordinates()}
        age:      {self.age()}
        energy:   {self.energy()}
        status:   {st}
        """


class Fox(Animal):
    """
    A fox in the simulated world.
    """

    food_energy_per_unit = 15
    reproduction_cost_rate = 0.85

    def __init__(self, population: parameters.Population, patch: Patch, age: int):
        """
        population: the parameters for the fox population used in this run of the simulation.
        patch: the position assigned to this animal(the constructor takes care of adding it to the list of animals of this patch).
        age: the current age of the animal.
        """
        energy = round(population.max_energy * 0.7)
        super().__init__(population, patch, energy, age)

    def feed(self):
        """Feeds itself using the resources at its current location(patch), if it is alive."""
        if self.is_alive() and self._energy < self._population.max_energy and self._patch.has_alive_rabbit():
            self._patch.rabbit.kill()  # kill the rabbit on that patch
            self._energy += self.food_energy_per_unit
            if self._energy > self._population.max_energy:
                self._energy = self._population.max_energy

    def reproduce(self, newborn_patch: Patch) -> Optional['Fox']:
        """If the animal is alive, it tries to reproduce using the patch provided.
        Returns an instance for the newborn(located at `newborn_patch`) or None.
        Patches are updated accordingly."""
        if random.random() > self._population.reproduction_probability:
            self._energy -= self._population.reproduction_min_energy * self.reproduction_cost_rate
            return Fox(self._population, newborn_patch, age=0)
        return None

    def __str__(self) -> str:
        if self.is_alive():
            st = "alive"
        else:
            st = "dead"
        return f"""Fox:
        position: {self.patch().coordinates()}
        age:      {self.age()}
        energy:   {self.energy()}
        status:   {st}
        """
