"""Scrape NBA player database."""

# Import libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Get the data
year = input("Enter the year: ")
url = f"https://www.basketball-reference.com/leagues/NBA_{year}_per_game.html"
response = requests.get(url, timeout=5)
soup = BeautifulSoup(response.content, "html.parser")

# Get the table
table = soup.find("table", {"id": "per_game_stats"})
table_body = table.find("tbody")

# Get the rows
rows = table_body.find_all("tr")

# Get the headers
headers = [th.text for th in table.find("thead").find_all("th")]

# Get the data
data = []
for row in rows:
    cols = row.find_all("td")
    cols = [ele.text.strip() for ele in cols]
    data.append([ele for ele in cols if ele])

# Create the dataframe
df = pd.DataFrame(data, columns=headers[1:])
df = df.dropna()

# Filter by position (user input)
position = input("Enter the position (blank if none): ")
if position != "":
    df = df[df["Pos"] == position]

# Filter by minutes played (user input)
minutes = input("Enter the minimum minutes played: ")
df = df[df["MP"] >= minutes]

# Filter by points (user input)
points = input("Enter the minimum points: ")
df = df[df["PTS"] >= points]

# Print the results
print("Results:")
print(df)

# Save the data
save = input("Save the data? (y/n): ")
if save == "y":
    df.to_csv(f"nba_{year}_per_game.csv")
