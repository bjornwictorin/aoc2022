#!/usr/bin/env python3

from typing import List
from collections import namedtuple
import re

BP = namedtuple("BP", "ore_ore clay_ore obsidian_ore obsidian_clay geode_ore geode_obsidian")
State = namedtuple("State", "ore clay obsidian geodes ore_robots clay_robots obsidian_robots geode_robots minute")

MAX_GEODES_SO_FAR = 0
NUM_MINUTES = 32

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
                 state.geode_robots + geode_robots,
                 state.minute + 1)


def can_afford(state: State, ore: int = 0, clay: int = 0, obsidian: int = 0) -> bool:
    if state.ore >= ore and state.clay >= clay and state.obsidian >= obsidian:
        return True
    return False


def can_get_best(state: State, bp: BP) -> bool:
    """Rough upper bound on how many geodes could possibly be collected.
    Following assumptions/simplifications are made:
    * Unlimited ore.
    * One robot of each sort can be built per round
    * Build one clay robot per remaining round
    * Build one obsidian robot every time we can afford one
    * Build one geode robot every time we can afford one
    Finally compare with the max number of geodes collected
    in round 32 encountered in the search (DFS) so far.
    """
    geodes = state.geodes
    clay = state.clay
    obsidian = state.obsidian
    clay_robots = state.clay_robots
    obsidian_robots = state.obsidian_robots
    geode_robots = state.geode_robots
    for _ in range(state.minute, NUM_MINUTES):
        init_clay_robots = clay_robots
        init_obsidian_robots = obsidian_robots
        init_geode_robots = geode_robots
        clay_robots += 1
        if clay >= bp.obsidian_clay:
            obsidian_robots += 1
            clay -= bp.obsidian_clay
        if obsidian >= bp.geode_obsidian:
            geode_robots += 1
            obsidian -= bp.geode_obsidian
        clay += init_clay_robots
        obsidian += init_obsidian_robots
        geodes += init_geode_robots
    return geodes > MAX_GEODES_SO_FAR


def next_step(state: State, bp: BP) -> None:
    global MAX_GEODES_SO_FAR
    if state.minute == NUM_MINUTES:
        if state.geodes > MAX_GEODES_SO_FAR:
            MAX_GEODES_SO_FAR = state.geodes
            print(f"max so far: {MAX_GEODES_SO_FAR}")
    # Only meaningful to continue this path if it is possible to
    # collect more geodes than the best so far
    elif state.minute < NUM_MINUTES - 10 or can_get_best(state, bp):
        # Order below matters because we want to find best option ASAP
        if can_afford(state, ore=bp.geode_ore, obsidian=bp.geode_obsidian):
            next_step(get_new_state(state, bp, geode_robots=1), bp)
        if can_afford(state, ore=bp.obsidian_ore, clay=bp.obsidian_clay) and state.obsidian_robots < bp.geode_obsidian:
            next_step(get_new_state(state, bp, obsidian_robots=1), bp)
        if can_afford(state, ore=bp.clay_ore) and state.clay_robots < bp.obsidian_clay:
            next_step(get_new_state(state, bp, clay_robots=1), bp)
        if can_afford(state, ore=bp.ore_ore) and state.ore_robots < max(bp.ore_ore, bp.clay_ore, bp.obsidian_ore):
            next_step(get_new_state(state, bp, ore_robots=1), bp)
        next_step(get_new_state(state, bp), bp)


def calc_max_geodes(blueprint: BP) -> int:
    global MAX_GEODES_SO_FAR
    MAX_GEODES_SO_FAR = 0
    initial_state = State(0, 0, 0, 0, 1, 0, 0, 0, 0)
    next_step(initial_state, blueprint)
    return MAX_GEODES_SO_FAR


def main():
    blueprints = parse_input("input.txt")
    max_geodes = []
    for blueprint in blueprints[:3]:
        max_geodes.append(calc_max_geodes(blueprint))
        print(".")
        print(max_geodes[-1])
    print(max_geodes)
    print(max_geodes[0] * max_geodes[1] * max_geodes[2])


if __name__ == "__main__":
    main()
