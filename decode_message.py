from pygad.pygad import GA
import pygad
import random

import warnings
warnings.filterwarnings("ignore")

def ascii_to_str(solution) -> str:
  return ''.join([chr(int(x)) for x in solution])

def get_crossover_type(crossover: str)-> str:
    if crossover == "1":
        return "single_point"
    elif crossover == "2":
        return "two_points"
    elif crossover == "3":
        return "uniform"
    elif crossover == "4":
        return "scattered"
    else:
        return "single_point"

def get_selection_type(selection: str) -> str:
    if selection == "sss":
        return "single_point"
    elif selection == "2":
        return "rws"
    elif selection == "3":
        return "sus"
    elif selection == "4":
        return "rank"
    elif selection == "5":
        return "random"
    elif selection == "6":
        return "tournament"
    else:
        return "sss"

def decode_message(output: str, generations: int = 200, crossover_type: str = "single_point", selection_type: str = "sss", mutation_percentage: int = 5):
  desired_output = [ord(x) for x in output]

  ascci_range = range(97, 123)
  ascii_space = 32
  gen_space = [*ascci_range, ascii_space]

  population_size = 50
  initial_population = [[random.randint(97, 123) for i in range(0,len(desired_output))] for k in range(0, population_size)]

  num_generations = generations
  num_parents_mating = 4

  num_genes = len(output)

  parent_selection_type = selection_type
  keep_parents = 1

  mutation_type = "random"
  mutation_percent_genes = mutation_percentage

  stop_criteria = "reach_1"

  def fitness_func(solution, solution_idx) -> float:
    fitness = 0

    for i in range(len(solution)):
      if(solution[i] == desired_output[i]):
        fitness += 1

    return fitness / len(solution)

  
  def on_generation(ga_instance: GA):
    solution, solution_fitness, solution_idx = ga_instance.best_solution()
    print(f"Best solution: {ascii_to_str(solution)} Best fitness: {solution_fitness} Generation: {ga_instance.generations_completed}")

  ga_instance = pygad.GA(num_generations=num_generations,
                        num_parents_mating=num_parents_mating,
                        fitness_func=fitness_func,
                        sol_per_pop=population_size,
                        num_genes=num_genes,
                        parent_selection_type=parent_selection_type,
                        keep_parents=keep_parents,
                        crossover_type=crossover_type,
                        mutation_type=mutation_type,
                        mutation_percent_genes=mutation_percent_genes,
                        save_solutions=True,
                        gene_type=int,
                        initial_population=initial_population,
                        on_generation=on_generation,
                        gene_space=gen_space,
                        stop_criteria=stop_criteria)

  ga_instance.run()

  solution, solution_fitness, solution_idx = ga_instance.best_solution()

  ga_instance.plot_fitness()

def main():
    output = input("Type the message to decode: ")

    num_generations = int(input("Type number of generations: "))

    print("Select crossover type:")
    print("[1] single_point(default)")
    print("[2] two_points")
    print("[3] uniform")
    print("[4] scattered")

    crossover_type_input = input()

    crossover_type = get_crossover_type(crossover_type_input)

    print("Select selection type:")
    print("[1] steady-state selection(default)")
    print("[2] roulette wheel selection")
    print("[3] stochastic universal selection")
    print("[4] rank ")
    print("[5] random")
    print("[6] tournament")

    selection_type_input = input()

    selection_type = get_selection_type(selection_type_input)

    mutation_percentage = int(input("Type mutation percentage: "))

    decode_message(output, num_generations, crossover_type, selection_type, mutation_percentage)


if __name__ == '__main__':
    main()