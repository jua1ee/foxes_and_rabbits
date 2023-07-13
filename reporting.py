import matplotlib as plt



def print_summary(results):
    """This function prints a summary of statistic for the simulation run""" 

    aggregated = [] #aggregated fox and rabbit list - used for statistic of the population combined
    for i in range(results.steps):
        aggregated.append(results.foxes.size_per_step[i] + results.rabbits.size_per_step[i])
        
    print("Number of foxes ever lived:", results.foxes.total, "\n"
          "Number of rabbits ever lived:", results.rabbits.total, "\n"
          "Total number of animals ever lived:", results.foxes.total + results.rabbits.total, "\n"
          "\n" #added to create space to make it more readable 
          "The minumum, maximum and average number of foxes alive at each step:", min(results.foxes.size_per_step), ",", max(results.foxes.size_per_step), ",", (sum(results.foxes.size_per_step))/results.steps, "\n"
          "The minumim, maximum and average number of rabbits alive at each step:", min(results.rabbits.size_per_step), ",", max(results.rabbits.size_per_step), ",", (sum(results.rabbits.size_per_step))/results.steps, "\n"
          "The minimum, maximum and average number of animals alive at each step:", min(aggregated), ",", max(aggregated), ",", (sum(aggregated))/results.steps, "\n",
          "\n"
          "Number of foxes died by old age:", results.foxes.dead_by_old_age, "\n" 
          "Number of rabbits died by old age:", results.rabbits.dead_by_old_age, "\n"
          "Total number of animals died by old age:", results.foxes.dead_by_old_age + results.rabbits.dead_by_old_age, "\n"
          "\n"
          "Number of foxes died by starvation:", results.foxes.dead_by_starvation, "\n"
          "Number of rabbits died by starvation:", results.rabbits.dead_by_starvation, "\n"
          "Total number of animals died by starvation:", results.foxes.dead_by_starvation + results.rabbits.dead_by_starvation, "\n"
          "\n"
          "Number of rabbits died by predation:", results.rabbits.dead_by_predation, "\n"
          "\n"
          "Total number of animals died:", results.foxes.dead_by_starvation + results.rabbits.dead_by_starvation + results.foxes.dead_by_old_age + results.rabbits.dead_by_old_age + results.rabbits.dead_by_predation)


def plot_pop_size(results):
    """This function visualise how the size of the population of fox, rabbits and the two combined over time(steps). The result will be presented with all three plots in the same figure"""

    time = list(range(results.steps)) #create list over time from simulation step 0 to maximum simulation step.
    
    aggregated = [] #aggregated fox and rabbit list - used for statistic of the population combined
    for i in range(results.steps):
        aggregated.append(results.foxes.size_per_step[i] + results.rabbits.size_per_step[i])
        
    plt.plot(time, results.foxes.size_per_step, label='Foxes', color='tab:orange') #fox population over time
    plt.plot(time, results.rabbits.size_per_step, label='Rabbits', color='tab:gray') #rabbit populaion over time
    plt.plot(time, aggregated, label='Aggregated', color='tab:cyan') #aggregated population over time
    plt.legend() 
    plt.title("Population of animals over time", fontsize=16)
    plt.ylabel("Size of population")
    plt.xlabel("Time (number of simulation steps)")
    plt.show() #open figure window with the plot


def plot_lifespan(results): #made in three subPlot due to the difference in number of animals (x-axis).
    """visualise the distribution of lifespans across individuals of each population and of the two combined"""

    No_fox = list(range(results.foxes.dead_by_old_age + results.foxes.dead_by_starvation)) #creates a list with numbers from 0 to total number of foxes died.
    sorted_age_fox = sorted(results.foxes.age_at_death, reverse=True) #sort the fox list with age at death in decreasing manner

    No_rabbits = list(range(results.rabbits.dead_by_starvation + results.rabbits.dead_by_predation + results.rabbits.dead_by_old_age))
    sorted_age_rabbit = sorted(results.rabbits.age_at_death, reverse=True)

    No_animals = list(range(results.foxes.dead_by_old_age + results.foxes.dead_by_starvation + results.rabbits.dead_by_starvation + results.rabbits.dead_by_predation + results.rabbits.dead_by_old_age))
    aggregated_age_at_death = results.foxes.age_at_death + results.rabbits.age_at_death
    sorted_age_aggregated = sorted(aggregated_age_at_death, reverse=True)

    plt.figure()
    plt.subplot(311) #plt.subplot takes three arguments, the number of rows (nrows), the number of columns (ncols) and the plot number.
    plt.plot(No_fox, sorted_age_fox, color="tab:orange", label="Foxes")
    plt.legend()
    plt.suptitle("Lifespan of animal population", fontsize=16)
    
    plt.subplot(312)
    plt.plot(No_rabbits, sorted_age_rabbit, color="tab:gray", label="Rabbits")
    plt.legend()
    plt.ylabel("Age at death")
    plt.legend()

    plt.subplot(313)
    plt.plot(No_animals, sorted_age_aggregated, color="tab:cyan", label="Aggregated")
    plt.xlabel("Number of Animal")
    plt.legend()
    
    plt.show()               


def plot_energy(results):
    """This function visualise how the average energy of foxes, of rabbits, and of the two combined changes over time. The three plots will be presented in th same figure.
       The energy will be plotted as the relative energy to the maximum energy"""
    
    time = list(range(results.steps)) #create list over time
    
    plt.plot(time, results.foxes.avg_energy_per_step, label='Foxes', color='tab:orange')#fox population over time
    plt.plot(time, results.rabbits.avg_energy_per_step, label='Rabbits', color='tab:gray')#rabbit populaion over time
    plt.plot(time, results.avg_energy_per_step, label='Aggregated', color='tab:cyan') #aggregated population over time
    plt.legend() 
    plt.title("Average energy of animals over time")
    plt.ylabel("Relative energy")
    plt.xlabel("Time (number of simulation steps)")
    plt.show()


def plot_kills(results):
    """This funtion visualose how deaths by predation are spatially distributed across the world/grid. The number of death is symbolised with a color
        presenting the number of death on the specific patch. The colorbar on the right indicates the number of death a color correlates to"""

    plt.matshow(results.kills_per_patch, cmap="Greys")
    plt.colorbar().set_label("Number of death on patch", fontsize = 10)  
    plt.title("Spatial distribution of death by predation")
    plt.show()
    
    
