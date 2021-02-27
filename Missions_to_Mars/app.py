from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars


app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

@app.route("/")
def index():
    text = 'Mission to Mars'
    return render_template("index.html", text = text)


@app.route("/scrape")
def scraper():
    titlepara = scrape_mars.scrape_titlepara()
    image_url = scrape_mars.scrape_image_url()
    mars_hemi = scrape_mars.scrape_marshemi()
    table = scrape_mars.scrape_table()

    mars_data = {
        'news_title_p':titlepara,
        'featured_image_url':image_url,
        'hemisphere_image_urls': mars_hemi,
        'table':table}

    mongo.db.collection.update({}, mars_data, upsert=True)
    mars_data = mongo.db.collection.find_one()

    return render_template("scrape.html", mars = mars_data)


if __name__ == "__main__":
    app.run(debug=True)