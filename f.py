from flask import Flask, jsonify, request
import storage
import model
import csv

app = Flask(__name__)

all_titles = []

with open("data.csv", "r") as data_csv:
    reader = csv.reader(data_csv)
    all_titles = list(reader)[1:]

@app.route("/")
def index():
    return jsonify({"data": [i[12] for i in all_titles], "status": "success"})

@app.route("/article")
def get_article():
    title = request.args.get("name")
    if (title == None):
        return jsonify({"status": "error", "message": "enter title as 'name' parameter"})
    article = model.get_article_info(title)
    return jsonify({"data": article, "status": "success"})

@app.route("/like", methods=["POST"])
def like_article():
    title = request.args.get("name")
    if (title == None):
        return jsonify({"status": "error", "message": "enter title as 'name' parameter"})
    storage.liked_articles.append(title)
    return jsonify({"status": "success"})

@app.route("/dislike", methods=["POST"])
def dislike_article():
    title = request.args.get("name")
    if (title == None):
        return jsonify({"status": "error", "message": "enter title as 'name' parameter"})
    storage.disliked_articles.append(title)
    return jsonify({"status": "success"})

@app.route("/unwatch", methods=["POST"])
def unwatch_article():
    title = request.args.get("name")
    if (title == None):
        return jsonify({"status": "error", "message": "enter title as 'name' parameter"})
    storage.unwatched_articles.append(title)
    return jsonify({"status": "success"})

@app.route("/popular")
def get_popular_articles():
    d = model.get_popular()
    return jsonify({"data": d, "status": "success"})

@app.route("/recommendations")
def get_rec():
    d = model.get_all_recommendations(storage.liked_articles)
    return jsonify({"data": d, "status": "success"})

if (__name__ == "__main__"):
    app.run(debug=True)