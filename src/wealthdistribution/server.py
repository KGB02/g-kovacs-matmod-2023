import mesa
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

import src.wealthdistribution as wd


def bsr_model_portrayal(agent):
    if agent is None:
        return

    portrayal = {}

    if type(agent) is wd.GrainAgent:
        portrayal = {"Shape": "rect", "w": 1, "h": 1, "Filled": "true", "Layer": 0}
        (x, y) = agent.pos
        portrayal["x"] = x
        portrayal["y"] = y
        if agent.grain_here > 30:
            portrayal["Color"] = "#FFFF00"
        else:
            portrayal["Color"] = "#FFFFAD"

    elif type(agent) is wd.PersonAgent:
        if agent.state == 0:
            portrayal["Shape"] = "pics/inf.png"
            portrayal["scale"] = 0.9
            portrayal["Layer"] = 3
        elif agent.state == 1:
            portrayal["Shape"] = "pics/rec.png"
            portrayal["scale"] = 0.9
            portrayal["Layer"] = 2
        elif agent.state == 2:
            portrayal["Shape"] = "pics/susc.png"
            portrayal["scale"] = 0.9
            portrayal["Layer"] = 1
    return portrayal


canvas_element = CanvasGrid(bsr_model_portrayal, 50, 50, 500, 500)

chart1 = mesa.visualization.ChartModule([{"Label": "Low", "Color": "Red"}, {"Label": "Medium", "Color": "Blue"},
                                         {"Label": "High", "Color": "Green"}],
                                        data_collector_name='datacollector')

model_params = {
    "height": 50,
    "width": 50,
    "max_grain": 50,
    "percent_best_land": mesa.visualization.Slider(name="percent_best_land", value=0.5, min_value=0, max_value=1, step=0.1),
    "num_people": mesa.visualization.Slider(name="num_people", value=500, min_value=10, max_value=900, step=1),
    "life_expectancy_max": 30,
    "life_expectancy_min": 5,
    "metabolism_max": 10,
    "num_grain_grow": 7
}

server = ModularServer(
    wd.WealthModel, [canvas_element, chart1], "Wealth Distribution", model_params
)
