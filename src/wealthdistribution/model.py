from mesa.datacollection import DataCollector
from mesa.model import Model
from mesa.space import MultiGrid
from mesa.time import RandomActivationByType

import numpy as np

import src.wealthdistribution as wd


class WealthModel(Model):
    def __init__(self, width: int, height: int, max_grain: int, percent_best_land: float, num_people: int,
                 life_expectancy_max: int, life_expectancy_min: int, metabolism_max: int, num_grain_grow: int):
        super().__init__()
        self.height = height
        self.width = width
        self.max_grain = max_grain
        self.percent_best_land = percent_best_land
        self.num_grain_grow = num_grain_grow
        self.life_expectancy_max = life_expectancy_max
        self.life_expectancy_min = life_expectancy_min
        self.metabolism_max = metabolism_max
        self.max_wealth = 0

        self.schedule = RandomActivationByType(model=self)
        self.grid = MultiGrid(width=width, height=height,
                              torus=True)

        for agent_idx in range(num_people):
            a = wd.PersonAgent(unique_id=self.next_id(), model=self)
            self.schedule.add(agent=a)
            x = self.random.randrange(0, height)
            y = self.random.randrange(0, width)
            self.grid.place_agent(agent=a, pos=(x, y))
            a.life_expectancy = (life_expectancy_min + np.random.randint(life_expectancy_max - life_expectancy_min + 1))
            a.metabolism = 1 + np.random.randint(metabolism_max)
            a.wealth = a.metabolism + np.random.randint(50)
            a.age = np.random.randint(a.life_expectancy)
            if a.wealth <= (self.max_wealth / 3):
                a.state = 0
            elif (self.max_wealth / 3) < a.wealth <= (self.max_wealth * 2 / 3):
                a.state = 1
            else:
                a.state = 2

        for x in range(height):
            for y in range(width):
                element = [0, 1]
                percent = [1 - percent_best_land, percent_best_land]
                yes_or_no = np.random.choice(element, 1, p=percent)
                if yes_or_no == 1:
                    grain = wd.GrainAgent(pos=(x, y), model=self)
                    self.schedule.add(grain)
                    self.grid.place_agent(pos=(x, y), agent=grain)
                    grain.grain_here = np.random.randint(max_grain)

        self.datacollector = DataCollector(
            model_reporters={
                "Low": low,
                "Medium": medium,
                "High": high
            }

        )
        self.datacollector.collect(model=self)

    def step(self):
        self.schedule.step(shuffle_types=False, shuffle_agents=True)
        self.datacollector.collect(model=self)
        self.max_wealth = 0


def low(model: WealthModel):
    l = 0
    for a in model.schedule.agents:
        if type(a) == wd.PersonAgent:
            a: wd.PersonAgent
            if a.wealth <= (model.max_wealth / 3):
                l += 1
    return l


def medium(model: WealthModel):
    m = 0
    for a in model.schedule.agents:
        if type(a) == wd.PersonAgent:
            a: wd.PersonAgent
            if (model.max_wealth / 3) < a.wealth <= (model.max_wealth * 2 / 3):
                m += 1
    return m


def high(model: WealthModel):
    h = 0
    for a in model.schedule.agents:
        if type(a) == wd.PersonAgent:
            a: wd.PersonAgent
            if a.wealth > (model.max_wealth * 2 / 3):
                h += 1
    return h
