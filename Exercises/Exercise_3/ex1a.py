import pandas as pd

columns = ["user", "movie", "date", "rating"]
netflix = pd.read_csv("./hw3_ex1_martin.vold@epfl.ch/com402-1.csv", quotechar='"', skipinitialspace=True,
	usecols=columns)
imdb = pd.read_csv("./hw3_ex1_martin.vold@epfl.ch/imdb-1.csv", quotechar='"', skipinitialspace=True,
	usecols=columns)

print(netflix.date.unique(), netflix.shape)