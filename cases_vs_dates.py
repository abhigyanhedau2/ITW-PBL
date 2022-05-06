import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation  # Creates animations

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

# Getting the covid numbers according to categories
active = dataset.groupby(["Date"]).Active.sum()
recovered = dataset.groupby(["Date"]).Recovered.sum()
death = dataset.groupby(["Date"]).Deaths.sum()
total = dataset.groupby(["Date"]).Confirmed.sum()

# Plotting the line graphs for each of the category
plt.plot(dates, active, label="Active", color="blue")
plt.plot(dates, recovered, label="Recovered", color="green")
plt.plot(dates, death, label="Deaths", color="red")
plt.plot(dates, total, label="Confirmed", color="black")

# Writing the legends
plt.legend()
plt.xlabel("Time")
plt.ylabel("Number of Cases Worldwide")

# Giving title to the graph
plt.title("Coronavirus Cases Worlwide from January 2020 to August 2020")

# plt.tight_layout() automatically adjusts subplot params so that the subplot(s) fits in to the figure area.
plt.tight_layout()

# Displaying the graph
plt.show()

# Grouping the datasets according to date
# We use as_index=False to indicate to groupby() that we don't want to set the column ID as the index
active = dataset.groupby(["Date"], as_index=False).Active.sum()
recovered = dataset.groupby(["Date"], as_index=False).Recovered.sum()
death = dataset.groupby(["Date"], as_index=False).Deaths.sum()
total = dataset.groupby(["Date"], as_index=False).Confirmed.sum()

fig, ax = plt.subplots(1, 1, figsize=(10, 7))

def animate(i):
    # Clearing the axes
    ax.clear()

    # Plotting the line graphs for each of the category
    ax.plot(active.Date[:i], active.Active[:i], label="Active", color="blue")
    ax.plot(active.Date[:i], recovered.Recovered[:i],
            label="Recovered", color="green")
    ax.plot(active.Date[:i], death.Deaths[:i], label="Deaths", color="red")
    ax.plot(active.Date[:i], total.Confirmed[:i],
            label="Confirmed", color="black")

    # Writing the legends
    ax.legend()
    ax.set_xlabel("Time")
    ax.set_ylabel("Number of Cases Worldwide")

    # Giving the title to the graph
    ax.set_title("Coronavirus Cases Worlwide from January 2020 to August 2020")

    # plt.tight_layout() automatically adjusts subplot params so that the subplot(s) fits in to the figure area.
    plt.tight_layout()

ani = FuncAnimation(fig, animate, interval=0.01, blit=False)

# Displaying the graph
plt.show()

