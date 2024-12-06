import matplotlib.pyplot as plt

import src.wealthdistribution as wd


def main():
    width = 50
    height = 50
    max_grain = 50
    percent_best_land = 0.5
    num_people = 500
    life_expectancy_max = 15
    life_expectancy_min = 3
    metabolism_max = 5
    num_grain_grow = 10
    model = wd.WealthModel(width=width, height=height, max_grain=max_grain, percent_best_land=percent_best_land,
                           num_people=num_people, life_expectancy_max=life_expectancy_max,
                           life_expectancy_min=life_expectancy_min, metabolism_max=metabolism_max,
                           num_grain_grow=num_grain_grow)
    time = 5
    for t in range(time):
        model.step()
    model_data = model.datacollector.get_model_vars_dataframe()


if __name__ == "__main__":
    main()
