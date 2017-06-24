import pickle
import matplotlib.pyplot as plt

def unpickle_data(file_name):
    with open(file_name, mode="rb") as pckl_file:
        return pickle.load(pckl_file)

angles = [15.0, 30.0, 45.0, 60.0, 75.0]

for angle in angles:
    relative_dists = unpickle_data(f"relative_dists_{angle:.0f}.pkl")
    times = unpickle_data(f"times_{angle:.0f}.pkl")
    view_factors = unpickle_data(f"view_factors_{angle:.0f}.pkl")
    plt.plot(relative_dists, view_factors, label=f"${angle:.0f}^o$")

plt.legend()
plt.xscale('log')
plt.xlim(0.1, 10.0)
plt.show()
