#!/usr/bin/env python3

from typing import List, Dict, Set, Tuple
import re

MAX_PRESSURE = 0
NUM_MINUTES = 30
SORTED_FLOW_RATES: List[Tuple[str, int]] = []

class Valve:
    def __init__(self, name: str, flow_rate: int, neighbors: List[str]):
        self.name = name
        self.flow_rate = flow_rate
        self.neighbors = neighbors
        self.best_so_far = 30 * [0]
    
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
    global SORTED_FLOW_RATES
    SORTED_FLOW_RATES = sorted([(valve.name, valve.flow_rate) for valve in valve_table.values()], reverse=True, key=lambda x: x[1])
    return valve_table


def upper_bound(minute: int, open_valves: Set[str], open_flow: int, pressure:int) -> int:
    # Assume that we in the remaining rounds could open the best, then the second best, ...
    # Which total pressure would we reach then?
    index = 0
    for remaining_minute in range(NUM_MINUTES - minute + 1):
        pressure += open_flow
        if (remaining_minute % 2) == 0:
            while True:
                if index == len(SORTED_FLOW_RATES):
                    next_flow_rate = 0
                    break
                next_flow_valve, next_flow_rate = SORTED_FLOW_RATES[index]
                if next_flow_valve not in open_valves:
                    break
                index += 1
            open_flow += next_flow_rate
    return pressure


def next_step(minute: int, current_valve_name: str, open_valves: Set[str], open_flow: int, pressure: int, valve_table: Dict[str, Valve]) -> None:
    # print(current_valve_name)
    current_valve = valve_table[current_valve_name]
    # TODO: Comment this assert out to improve speed
    assert open_flow == sum([valve_table[valve].flow_rate for valve in open_valves])
    global MAX_PRESSURE
    pressure += open_flow
    if minute > 1:
        # If we previously visited this valve with a higher pressure,
        # we can discard the current path
        # Don't check first minute because slicing below will
        # return empty sequence, and pressure after first minute is always 0.
        # Also check againt flow rate?
        if pressure < max(current_valve.best_so_far[:minute - 1]):
            return
        else:
            current_valve.best_so_far[minute - 1] = pressure
    if minute > NUM_MINUTES - 10:
        if upper_bound(minute, open_valves, open_flow, pressure) < MAX_PRESSURE:
            return
    if minute == NUM_MINUTES:
        # print(pressure)
        if pressure > MAX_PRESSURE:
            MAX_PRESSURE = pressure
    else:
        # Open current valve
        if current_valve.flow_rate != 0 and current_valve.name not in open_valves:
            open_valves.add(current_valve.name)
            next_step(minute + 1, current_valve.name, open_valves, open_flow + current_valve.flow_rate, pressure, valve_table)
            open_valves.remove(current_valve.name)

        if minute == NUM_MINUTES - 1:
            # If it is the second last minute, then no need to step to next valve.
            # Better to just stay
            next_step(minute + 1, current_valve.name, open_valves, open_flow, pressure, valve_table)
        else:
            # Move to next valve
            for neighbor in current_valve.neighbors:
                next_step(minute + 1, neighbor, open_valves, open_flow, pressure, valve_table)


def release_pressure(valve_table: Dict[str, Valve]) -> None:
    """Do a Depth-First Search (DFS)"""
    next_step(minute=1, current_valve_name="AA", open_valves=set(), open_flow=0, pressure=0, valve_table=valve_table)


def main():
    valve_table = parse_input("input.txt")
    for name, valve in valve_table.items():
        print(f"{name}: {valve}")
    release_pressure(valve_table)
    print(MAX_PRESSURE)


if __name__ == "__main__":
    main()
