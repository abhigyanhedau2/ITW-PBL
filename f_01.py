
from IPython.display import HTML
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation #creates the animation of our plots later on

import numpy as np # linear algebra
import pandas as pd
import geopandas as gpd



#load the dataset
dataset = pd.read_csv("python\ITW02_PBL\covid_19_clean_complete.csv")
print(dataset.head())
#prepare datasets for world visualisation
#groupby country and date and aggregate with summing up the county values which can later be plotted as a heatmap/colormap
active_world = dataset.groupby(["Date","Country/Region"], as_index= False).Active.sum()
recovered_world = dataset.groupby(["Date","Country/Region"], as_index= False).Recovered.sum()
death_world = dataset.groupby(["Date","Country/Region"], as_index= False).Deaths.sum()
total_world = dataset.groupby(["Date","Country/Region"], as_index= False).Confirmed.sum()

world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
print(world.head())
merged = pd.merge(
    left = total_world,
    right = world.drop("gdp_md_est", axis = "columns"),
    left_on = "Country/Region",
    right_on = "name",
    how = "left",
    
)

merged_world = merged.sort_values(by = "Date")
merged_world_drop_na = merged_world.dropna()
merged_world_drop_na  = gpd.GeoDataFrame(merged_world_drop_na)

print(f"{len(merged_world[merged_world.isna().any(axis=1)])/len(dataset)*100} percent of the dataset is missing due to missing values in geopandas naturalearthlowres")


merged_tss_index = merged_world_drop_na.set_index("Date")
active = dataset.groupby(["Date"],as_index= False).Active.sum()
recovered = dataset.groupby(["Date"],as_index= False).Recovered.sum()
death = dataset.groupby(["Date"],as_index= False).Deaths.sum()
total = dataset.groupby(["Date"],as_index= False).Confirmed.sum()
fig, ax = plt.subplots(2,1 ,figsize =(10,7))
def animate(i):
    # new axes
    ax[0].clear()
    ax[1].clear()
    # Plotting the line graphs for each of the category
    ax[0].plot(active.Date[:i], active.Active[:i], label = "Active", color = "blue" )
    ax[0].plot(active.Date[:i],recovered.Recovered[:i], label= "Recovered", color = "green")
    ax[0].plot(active.Date[:i],death.Deaths[:i], label = "Deaths", color = "red")
    ax[0].plot(active.Date[:i],total.Confirmed[:i], label = "Confirmed", color = "yellow")
    merged_tss_index.loc[active.Date[i]].plot("Confirmed", ax = ax[1])
    # setting the hue
    ax[0].legend()
    ax[0].set_xlabel("Time")
    ax[0].set_ylabel("Number of Cases Worldwide")
    ax[0].set_title("Coronavirus Cases Worlwide from January 2020 to August 2020")
    # plt.tight_layout() automatically adjusts subplot params so that the subplot(s) fits in to the figure area.
    plt.tight_layout()
    
        
# for animation
anim = FuncAnimation(fig,animate, interval = 100, blit = False)
# to display graph
plt.show()
# HTML(FuncAnimation(fig,animate, interval = 500).to_jshtml())
