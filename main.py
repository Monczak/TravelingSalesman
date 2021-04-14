from algorithms import nearest_neighbor, two_swap, anneal

with open("dantzig42_d.txt", "r") as file:
    distances = [list(map(float, line.split())) for line in file if line.strip() != ""]

print("Nearest neighbor: ", nearest_neighbor(distances))
print("Two swap: ", two_swap(distances))
print("Simulated annealing: ", anneal(distances, 10000, 0.9))
