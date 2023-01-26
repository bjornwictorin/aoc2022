#!/usr/bin/env python3

from typing import List, Set
from collections import namedtuple
import re

BP = namedtuple("BP", "ore_ore clay_ore obsidian_ore obsidian_clay geode_ore geode_obsidian")
State = namedtuple("State", "ore clay obsidian geodes ore_robots clay_robots obsidian_robots geode_robots")

def parse_input(input_file: str) -> List[BP]:
    blueprints = []
    with open(input_file, "r") as f:
        for line in f:
            numbers = re.findall("[0-9]+", line)
            blueprints.append(BP(*[int(ii) for ii in numbers[1:]]))
    return blueprints


def get_new_state(state: State, bp: BP, ore_robots: int = 0, clay_robots: int = 0, obsidian_robots: int = 0, geode_robots: int = 0) -> State:
    assert 0 <= ore_robots + clay_robots + obsidian_robots + geode_robots <= 1, "Can only build one robot per round!"
    assert 0 <= ore_robots <= 1
    assert 0 <= clay_robots <= 1
    assert 0 <= obsidian_robots <= 1
    assert 0 <= geode_robots <= 1
    spent_ore = 0
    spent_clay = 0
    spent_obsidian = 0
    if ore_robots == 1:
        spent_ore = bp.ore_ore
    elif clay_robots == 1:
        spent_ore = bp.clay_ore
    elif obsidian_robots == 1:
        spent_ore = bp.obsidian_ore
        spent_clay = bp.obsidian_clay
    elif geode_robots == 1:
        spent_ore = bp.geode_ore
        spent_obsidian = bp.geode_obsidian
    return State(state.ore + state.ore_robots - spent_ore,
                 state.clay + state.clay_robots - spent_clay,
                 state.obsidian + state.obsidian_robots - spent_obsidian,
                 state.geodes + state.geode_robots,
                 state.ore_robots + ore_robots,
                 state.clay_robots + clay_robots,
                 state.obsidian_robots + obsidian_robots,
                 state.geode_robots + geode_robots)


def can_afford(state: State, ore: int = 0, clay: int = 0, obsidian: int = 0) -> bool:
    if state.ore >= ore and state.clay >= clay and state.obsidian >= obsidian:
        return True
    return False


def find_next_states(current_states: Set[State], bp: BP) -> Set[State]:
    next_states = set()
    for state in current_states:
        next_states.add(get_new_state(state, bp)) # One option is to not build any robot
        if can_afford(state, ore=bp.ore_ore):
            next_states.add(get_new_state(state, bp, ore_robots=1))
        if can_afford(state, ore=bp.clay_ore):
            next_states.add(get_new_state(state, bp, clay_robots=1))
        if can_afford(state, ore=bp.obsidian_ore, clay=bp.obsidian_clay):
            next_states.add(get_new_state(state, bp, obsidian_robots=1))
        if can_afford(state, ore=bp.geode_ore, obsidian=bp.geode_obsidian):
            next_states.add(get_new_state(state, bp, geode_robots=1))
    return next_states


def prune_states(states: Set[State]) -> Set[State]:
    max_state = max(states, key=lambda x: x.geodes)
    max_geodes = max_state.geodes
    pruned_states = set()
    for state in states:
        if state.geodes == max_geodes:
            pruned_states.add(state)
    return pruned_states


def calc_max_geodes(blueprint: BP) -> int:
    initial_state = State(0, 0, 0, 0, 1, 0, 0, 0)
    possible_states = {initial_state}
    for round in range(24):
        possible_states = find_next_states(possible_states, blueprint)
        possible_states = prune_states(possible_states)
        print(f"Possible states after {round + 1} rounds: {len(possible_states)}")
    max_state = max(possible_states, key=lambda x: x.geodes)
    print(max_state)
    return max_state.geodes


def main():
    blueprints = parse_input("input.txt")
    max_geodes = []
    for blueprint in blueprints:
        max_geodes.append(calc_max_geodes(blueprint))
    print(sum([(ii + 1) * geodes for ii, geodes in enumerate(max_geodes)]))


if __name__ == "__main__":
    main()
