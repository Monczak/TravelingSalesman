from itertools import combinations
import math
import random


def nearest_neighbor(distances, initial=0):
    current = initial
    path = [initial]
    total_length = 0

    for _ in range(len(distances)):
        neighbors = distances[current]

        nearest, nearest_index = float("inf"), -1
        for i in range(len(neighbors)):
            if i not in path:
                if neighbors[i] < nearest and i != current:
                    nearest = neighbors[i]
                    nearest_index = i

        path.append(nearest_index)
        total_length += distances[current][nearest_index]

        current = nearest_index

        if len(path) == len(distances):
            path.append(initial)
            total_length += distances[current][initial]
            return path, total_length


def calc_total_length(distances, path):
    result = 0
    for i in range(len(path) - 1):
        result += distances[path[i]][path[i + 1]]
    return result


def two_swap(distances, initial=0):
    current_path, _ = nearest_neighbor(distances, initial)

    for a, b in combinations(range(1, len(distances)), 2):
        length_before = calc_total_length(distances, current_path)
        current_path[a], current_path[b] = current_path[b], current_path[a]
        length_after = calc_total_length(distances, current_path)

        if length_after > length_before:
            current_path[a], current_path[b] = current_path[b], current_path[a]

    return current_path, calc_total_length(distances, current_path)


def anneal(distances, iterations, temp_drop, initial=0):
    current_path, _ = nearest_neighbor(distances, initial)
    best_path = current_path.copy()

    current_temp = math.sqrt(len(current_path))

    for i in range(iterations):
        k, l = random.randint(2, len(current_path) - 1), random.randint(0, len(current_path) - 1)

        candidate_path = current_path.copy()
        candidate_path[max(l, 1):min(k + l, len(candidate_path) - 1)] = reversed(candidate_path[max(l, 1):min(k + l, len(candidate_path) - 1)])

        delta = calc_total_length(distances, candidate_path) - calc_total_length(distances, best_path)

        if delta < 0:
            best_path = candidate_path.copy()
            current_path = candidate_path.copy()
        else:
            p = math.exp(-abs(delta) / current_temp)
            if random.random() <= p:
                best_path = candidate_path.copy()
                current_path = candidate_path.copy()

        current_temp *= temp_drop

    return best_path, calc_total_length(distances, best_path)
