#!/usr/bin/env python3


from typing import List, Dict, Tuple, Set
import re

MAX_PRESSURE = 0
NUM_MINUTES = 26
VALVE_TABLE: Dict[str, "Valve"] = {}
DIST_TABLE: Dict[str, Dict[str, int]] = {}
RESULT_TABLE: Dict[int, int] = {}

class Valve:
    def __init__(self, name: str, flow_rate: int, neighbors: List[str]):
        self.name = name
        self.flow_rate = flow_rate
        self.neighbors = [(name, int(1)) for name in neighbors]
    
    def __str__(self):
        return f"{self.name}, {self.neighbors}, {self.flow_rate}"
    
    def __repr__(self):
        return self.__str__()

def parse_input(input_file: str) -> Dict[str, Valve]:
    valve_table = {}
    with open(input_file, "r") as f:
        for line in f:
            valve_names = re.findall("[A-Z][A-Z]", line)
            this_valve = valve_names[0]
            flow_rate = int(re.findall("[0-9]+", line)[0])
            valve_table[this_valve] = Valve(this_valve, flow_rate, valve_names[1:])
    assert "AA" in valve_table, "No AA valve in table"
    return valve_table


def valve_name2tuple(valve_name: str, nbr_nbr_list: List[Tuple[str, int]]) -> Tuple[str, int]:
    zero_valve_link = (valve_name, 0)
    for link in nbr_nbr_list:
        if link[0] == valve_name:
            zero_valve_link = link
    # assert zero_valve_link[1] != 0
    return zero_valve_link


def remove_zero_valves(valve_table: Dict[str, Valve]) -> None:
    # Find all valves with flow rate 0
    zero_valves = [valve.name for valve in valve_table.values() if valve.flow_rate == 0 and valve.name != "AA"]
    for zero_valve in zero_valves:
        neighbors = valve_table[zero_valve].neighbors
        for nbr_name, nbr_dist in neighbors:
            nbr_nbr_list = valve_table[nbr_name].neighbors
            # Remove the zero_valve neighbor
            nbr_nbr_list.remove(valve_name2tuple(zero_valve, nbr_nbr_list))
            # Add new neighbors
            new_nbrs = [(x_name, x_dist + nbr_dist) for x_name, x_dist in neighbors if x_name != nbr_name]
            for new_nbr in new_nbrs:
                # Only add the new neighbors if they provide a shorter path to the valve
                existing_entry = valve_name2tuple(new_nbr[0], nbr_nbr_list)
                if existing_entry[1] == 0:
                    nbr_nbr_list.append(new_nbr)
                elif existing_entry[1] > new_nbr[1]:
                    nbr_nbr_list.remove(existing_entry)
                    nbr_nbr_list.append(new_nbr)
        # Remove zero valve from valve table
        valve_table.pop(zero_valve)


def floyd_warshall(valve_table: Dict[str, Valve]) -> Dict[str, Dict[str, int]]:
    """Calculate shortest distance between all pairs of nodes
    using Floyd-Warshall algorithm"""
    big_int = 10000 # larger than any possible value
    dist_table = {}
    # Initialization
    for valve_name, valve in valve_table.items():
        sub_table = {}
        for inner_valve in valve_table:
            sub_table[inner_valve] = 0 if inner_valve == valve_name else big_int
        for nbr in valve.neighbors:
            nbr_name, nbr_dist = nbr
            sub_table[nbr_name] = nbr_dist
        dist_table[valve_name] = sub_table
        print(sub_table)
    # Find shortest paths
    for kk in valve_table:
        for ii in valve_table:
            for jj in valve_table:
                if dist_table[ii][jj] > dist_table[ii][kk] + dist_table[kk][jj]:
                    dist_table[ii][jj] = dist_table[ii][kk] + dist_table[kk][jj]
    print(25 * "=")
    for key, val in dist_table.items():
        print(f"{key}: {val}")
    return dist_table


def open_valves_hash(open_valves: Set[str]) -> int:
    hash_code = 0
    for valve in VALVE_TABLE.keys():
        hash_code <<= 1
        if valve in open_valves:
            hash_code += 1
    return hash_code


def next_step(minute: int, current_valve_name: str, open_valves: Set[str], open_flow: int, pressure: int) -> None:
    # TODO: Comment this assert out to improve speed
    assert open_flow == sum([VALVE_TABLE[valve].flow_rate for valve in open_valves])
    global MAX_PRESSURE
    global RESULT_TABLE
    hash_code = open_valves_hash(open_valves)
    final_pressure = pressure + open_flow * (NUM_MINUTES - minute + 1)
    if hash_code in RESULT_TABLE:
        if final_pressure > RESULT_TABLE[hash_code]:
            RESULT_TABLE[hash_code] = final_pressure
    else:
        RESULT_TABLE[hash_code] = final_pressure
    if final_pressure > MAX_PRESSURE:
        MAX_PRESSURE = final_pressure

    for neighbor, dist in DIST_TABLE[current_valve_name].items():
        if minute + dist <= NUM_MINUTES and neighbor not in open_valves and neighbor != current_valve_name and neighbor != "AA":
            # Enough time to reach next node
            open_valves.add(neighbor)
            next_step(minute + dist + 1, neighbor, open_valves, open_flow + VALVE_TABLE[neighbor].flow_rate, pressure + open_flow * (dist + 1))
            open_valves.remove(neighbor)


def find_best_combo() -> int:
    best_combo_pressure = 0
    for hash_code_a, value_a in RESULT_TABLE.items():
        for hash_code_b, value_b in RESULT_TABLE.items():
            if not (hash_code_a & hash_code_b):
                # No overlap between open valves
                combo_pressure = value_a + value_b
                best_combo_pressure = max(best_combo_pressure, combo_pressure)
    return best_combo_pressure


def main():
    valve_table = parse_input("input.txt")
    for name, valve in valve_table.items():
        print(f"{name}: {valve}")
    print(30 * "-")
    remove_zero_valves(valve_table)
    for name, valve in valve_table.items():
        print(f"{name}: {valve}")
    dist_table = floyd_warshall(valve_table)
    global VALVE_TABLE
    global DIST_TABLE
    VALVE_TABLE = valve_table
    DIST_TABLE = dist_table
    next_step(minute=1, current_valve_name="AA", open_valves=set(), open_flow=0, pressure=0)
    print(find_best_combo())


if __name__ == "__main__":
    main()
