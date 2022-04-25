import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation  # Creates animations
from IPython.display import HTML

# Loading the dataset
dataset = pd.read_csv('covid_19_clean_complete.csv')

active_world = dataset.groupby(["Date","Country/Region"], as_index= False).Active.sum()
print(active_world)