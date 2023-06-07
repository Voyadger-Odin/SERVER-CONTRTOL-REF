import numpy as np
from tabulate import tabulate

m = np.array([[111111, 2, 3], [4, 5, 6]])
headers = ["col 1", "col 2 jahdj jlfhads  hfouaqsho faoius nn asoiugfoiusa", "col 3"]

# Generate the table in fancy format.
table = tabulate(m, headers, tablefmt="fancy_grid")

# Show it.
print(table)