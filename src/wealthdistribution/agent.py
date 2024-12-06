import math
import numpy as np

from mesa.agent import Agent

import src.wealthdistribution as wd


class GrainAgent(Agent):
    def __init__(self, pos: tuple, model: wd.WealthModel):
        super().__init__(pos, model)
        # Position of the cell
        self.pos = pos
        self.grain_here = None

    def step(self):
        self.grow_grain()

    def grow_grain(self):
        self.model: wd.WealthModel
        agents_in_cell = self.model.grid.get_cell_list_contents([self.pos])
        agents_in_cell.remove(self)
        if len(agents_in_cell) == 0:
            self.grain_here += self.model.num_grain_grow
        else:
            self.grain_here = self.model.num_grain_grow


class PersonAgent(Agent):
    def __init__(self, unique_id: int, model: wd.WealthModel):
        super().__init__(unique_id=unique_id, model=model)
        self.age = None
        self.metabolism = None
        self.wealth = None
        self.life_expectancy = None
        self.state = None

    def step(self):
        self.move()
        self.harvest()
        self.eat_age_die()

    def move(self):
        self.model: wd.WealthModel
        cell_to_move = self.model.grid.get_neighborhood(
            pos=self.pos,
            moore=True,
            include_center=False,
            radius=6)
        dest_cell = self.model.random.choice(cell_to_move)
        self.model.grid.move_agent(agent=self, pos=dest_cell)

    def harvest(self):
        self.model: wd.WealthModel
        agents_in_cell = self.model.grid.get_cell_list_contents([self.pos])
        if len(agents_in_cell) == 1:
            pass
        else:
            grain = None
            for agent in agents_in_cell:
                if type(agent) == wd.GrainAgent:
                    grain = agent.grain_here
            if grain is not None:
                self.wealth += (grain / (len(agents_in_cell)-1))

    def eat_age_die(self):
        self.model: wd.WealthModel
        self.wealth -= self.metabolism
        self.age += 1
        pos = self.pos
        if self.wealth > self.model.max_wealth:
            self.model.max_wealth = self.wealth
        if self.wealth <= (self.model.max_wealth / 3):
            self.state = 0
        elif (self.model.max_wealth / 3) < self.wealth <= (self.model.max_wealth * 2 / 3):
            self.state = 1
        else:
            self.state = 2
        if self.wealth < 0 or self.age > self.life_expectancy:
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)
            g = wd.PersonAgent(unique_id=self.model.next_id(), model=self.model)
            self.model.schedule.add(agent=g)
            self.model.grid.place_agent(agent=g, pos=pos)
            g.life_expectancy = (self.model.life_expectancy_min +
                                 np.random.randint(self.model.life_expectancy_max - self.model.life_expectancy_min + 1))
            g.metabolism = 1 + np.random.randint(self.model.metabolism_max)
            g.wealth = g.metabolism + np.random.randint(50)
            g.age = np.random.randint(g.life_expectancy)
            if g.wealth <= (self.model.max_wealth / 3):
                g.state = 0
            elif (self.model.max_wealth / 3) < g.wealth <= (self.model.max_wealth * 2 / 3):
                g.state = 1
            else:
                g.state = 2


