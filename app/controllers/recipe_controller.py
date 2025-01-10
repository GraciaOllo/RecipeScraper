from flask import Blueprint, render_template, request, jsonify
from app.models.recipe import Recipe
from app.services.scraper import RecipeScraper
from app import db

recipe_bp = Blueprint('recipe', __name__)
scraper = RecipeScraper()

@recipe_bp.route('/')
def index():
    recipes = Recipe.query.order_by(Recipe.created_at.desc()).all()
    return render_template('index.html', recipes=recipes)

@recipe_bp.route('/recipe/<int:id>')
def view_recipe(id):
    recipe = Recipe.query.get_or_404(id)
    return render_template('recipe.html', recipe=recipe)

@recipe_bp.route('/scrape', methods=['POST'])
def scrape_recipe():
    url = request.form.get('url')
    if not url:
        return jsonify({'error': 'URL is required'}), 400
    
    try:
        recipe_data = scraper.scrape(url)
        recipe = Recipe(
            title=recipe_data['title'],
            ingredients=recipe_data['ingredients'],
            instructions=recipe_data['instructions'],
            cooking_time=recipe_data['cooking_time'],
            servings=recipe_data['servings'],
            source_url=url
        )
        db.session.add(recipe)
        db.session.commit()
        return jsonify({'message': 'Recipe scraped successfully', 'id': recipe.id})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
