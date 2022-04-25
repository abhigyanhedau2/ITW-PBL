import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation  # Creates animations
import geopandas as gpd

# Loading the dataset
dataset = pd.read_csv('covid_19_clean_complete.csv')

# Printing the first few rows of dataset
print("\nPrinting the first few rows of the dataset: ")
print(dataset.head())

# Transform date columns to datetime. It'll simplyfy plotting of the data
dataset["Date"] = pd.to_datetime(dataset.Date)
print("\nConverted the date columns to datetime. \nResult: ")
print(dataset.head())

# Getting the unique dates which we'll later use in plotting later in my plotting
dates = dataset.Date.unique()
print("\n Printing few entries of dates to verify the unique function: ")
print(dates[:5])

# Preparing the datasets for world visualization, grouping by country and date and summing up the values to later used as heatmap/color map
active_world = dataset.groupby(
    ["Date", "Country/Region"], as_index=False).Active.sum()
recovered_world = dataset.groupby(
    ["Date", "Country/Region"], as_index=False).Recovered.sum()
death_world = dataset.groupby(
    ["Date", "Country/Region"], as_index=False).Deaths.sum()
total_world = dataset.groupby(
    ["Date", "Country/Region"], as_index=False).Confirmed.sum()

world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
print("\nPrinting the head of world regions: ")
print(world.head())


# pd.merge is used to merge DataFrame or named Series objects with a database-style join.
# left: use only keys from left frame, similar to a SQL left outer join; preserve key order.
# right: use only keys from right frame, similar to a SQL right outer join; preserve key order.
# left_onlabel or list, or array-like - Column or index level names to join on in the left DataFrame. Can also be an array or list of arrays of the length of the left DataFrame. These arrays are treated as if they are columns.
# right_onlabel or list, or array-like - Column or index level names to join on in the right DataFrame. Can also be an array or list of arrays of the length of the right DataFrame. These arrays are treated as if they are columns.
# how : how to join the datasets - choices - how{‘left’, ‘right’, ‘outer’, ‘inner’, ‘cross’}, default ‘inner’
merged = pd.merge(
    left=total_world,
    right=world.drop("gdp_md_est", axis="columns"),
    left_on="Country/Region",
    right_on="name",
    how="left",
)

# Sorting the values by date
merged_world = merged.sort_values(by="Date")

# Dropping the NULL values
merged_world_drop_na = merged_world.dropna()

# A GeoDataFrame object is a pandas.DataFrame that has a column with geometry.
# Creating a geodataframe
merged_world_drop_na = gpd.GeoDataFrame(merged_world_drop_na)

merged_tss_index = merged_world_drop_na.set_index("Date")
active = dataset.groupby(["Date"], as_index=False).Active.sum()
recovered = dataset.groupby(["Date"], as_index=False).Recovered.sum()
death = dataset.groupby(["Date"], as_index=False).Deaths.sum()
total = dataset.groupby(["Date"], as_index=False).Confirmed.sum()
fig, ax = plt.subplots(2, 1, figsize=(10, 7))


def animate(i):
    # Clearing the axes
    ax[0].clear()
    ax[1].clear()

    # Plotting the line graphs
    ax[0].plot(active.Date[:i], active.Active[:i],
               label="Active", color="blue")
    ax[0].plot(active.Date[:i], recovered.Recovered[:i],
               label="Recovered", color="green")
    ax[0].plot(active.Date[:i], death.Deaths[:i],
               label="Deaths", color="red")
    ax[0].plot(active.Date[:i], total.Confirmed[:i],
               label="Confirmed", color="black")

    # Plotting the world graph
    merged_tss_index.loc[active.Date[i]].plot("Confirmed", ax=ax[1])

    # Setting legends
    ax[0].legend()
    ax[0].set_xlabel("Time")
    ax[0].set_ylabel("Number of Cases Worldwide")

    # Giving title
    ax[0].set_title(
        "Coronavirus Cases Worlwide from January 2020 to August 2020")

    # plt.tight_layout() automatically adjusts subplot params so that the subplot(s) fits in to the figure area.
    plt.tight_layout()

ani = FuncAnimation(fig, animate, interval=50)
plt.show()
