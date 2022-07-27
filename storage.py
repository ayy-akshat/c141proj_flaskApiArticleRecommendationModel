import csv

all_articles = []
liked_articles = []
disliked_articles = []
unwatched_articles = []

with open("data.csv") as data:
    reader = csv.reader(data)
    for row in reader:
        all_articles.append(row[12])
    all_articles = all_articles[1:]