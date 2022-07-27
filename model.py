import json
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

df = pd.read_csv("data.csv")

count = CountVectorizer(stop_words="english")

print("model is learning...")
countMatrix = count.fit_transform(df["metadata"])
sim = cosine_similarity(countMatrix, countMatrix)
print("model learned!\n")

indices = pd.Series(df.index, index=df["title"])

viewer_info = ["title", "url", "lang"]


def get_article_info(title):
    index = indices[title]
    return df[viewer_info].iloc[index].to_dict()


def get_recommendations(title):
    try:
        index = indices[title]
    except:
        return []
    sim_score = list(enumerate(sim[index]))

    def key(x):
        return x[1]
    sim_score.sort(key=key, reverse=True)
    sim_score = sim_score[1:11]
    indexes = [i[0] for i in sim_score]
    return df["title"].iloc[indexes]


def get_all_recommendations(titles):
    all_rec = []
    for i in titles:
        r = get_recommendations(i)
        all_rec.append(list(r))
    a = []
    for i in all_rec:
        for t in i:
            a.append(t)
    print(a)
    return list(set(a))


def get_popular(more_info=False):
    df.sort_values("scores")
    d = []
    for i in range(0, 10):
        d.append(df[viewer_info].iloc[i].to_dict())
    return d