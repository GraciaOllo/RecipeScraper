from flask import Flask, render_template, request, jsonify
from controllers.scrape_controller import RecipeScraper

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        scraper = RecipeScraper(url)
        html = scraper.fetch_page()
        if html:
            recipe = scraper.parse_recipe(html)
            return render_template('recipe.html', recipe=recipe)
        else:
            return render_template('error.html', message="Failed to fetch data.")
    return render_template('index.html')

@app.route('/api/recipe', methods=['POST'])
def api_scrape():
    url = request.json.get('url')
    scraper = RecipeScraper(url)
    html = scraper.fetch_page()
    if html:
        recipe = scraper.parse_recipe(html)
        return jsonify(recipe)
    return jsonify({"error": "Failed to fetch recipe."}), 400

if __name__ == '__main__':
    app.run(debug=True)
