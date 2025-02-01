# app/services/scraper.py
import requests
from bs4 import BeautifulSoup
import re
import json
from urllib.parse import urlparse

class RecipeScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def scrape(self, url):
        try:
            response = requests.get(url, headers=self.headers)
            
            if response.status_code != 200:
                raise Exception(f"Failed to fetch the page. Status code: {response.status_code}")
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Debugging: Output raw HTML for verification
            print("DEBUG: Raw HTML content fetched.")
            with open("debug_page.html", "w", encoding="utf-8") as f:
                f.write(str(soup))
            
            # Extract JSON-LD data if available
            json_ld = self._extract_json_ld(soup)
            if json_ld:
                return json_ld
            
            # Fall back to HTML parsing
            domain = urlparse(url).netloc
            recipe = {
                'title': self._get_title(soup, domain),
                'ingredients': self._get_ingredients(soup, domain),
                'instructions': self._get_instructions(soup, domain),
                'cooking_time': self._get_cooking_time(soup, domain),
                'servings': self._get_servings(soup, domain),
                'source_url': url
            }
            return recipe
        except Exception as e:
            print(f"ERROR: {str(e)}")
            return {'error': str(e)}

    def _extract_json_ld(self, soup):
        json_ld = soup.find('script', {'type': 'application/ld+json'})
        if json_ld:
            try:
                data = json.loads(json_ld.string)
                if isinstance(data, list):
                    data = next((item for item in data if item.get('@type') == 'Recipe'), None)
                if data and data.get('@type') == 'Recipe':
                    return {
                        'title': data.get('name', ''),
                        'ingredients': '\n'.join(data.get('recipeIngredient', [])),
                        'instructions': '\n'.join(
                            step.get('text', step) if isinstance(step, dict) else step
                            for step in data.get('recipeInstructions', [])
                        ),
                        'cooking_time': self._format_time(data.get('cookTime', '')),
                        'servings': str(data.get('recipeYield', '')),
                    }
            except Exception as e:
                print(f"DEBUG: JSON-LD extraction failed - {e}")
        return None

    def _get_title(self, soup, domain):
        selectors = [
            'h1.recipe-title',
            'h1.entry-title',
            'h1.title',
            'h1[class*="title"]',
            'h1[class*="recipe"]',
            'h1',
        ]
        for selector in selectors:
            title = soup.select_one(selector)
            if title and title.text.strip():
                return title.text.strip()
        return "Unknown Recipe"

    def _get_ingredients(self, soup, domain):
        ingredients = []
        selectors = [
            '.recipe-ingredients li',
            '.ingredients li',
            '[itemprop="recipeIngredient"]',
            '.ingredient-list li',
            '.ingredient',
            '[class*="ingredient"]',
        ]
        for selector in selectors:
            items = soup.select(selector)
            if items:
                ingredients = [item.text.strip() for item in items if item.text.strip()]
                break
        
        # If no ingredients found, fallback to container search
        if not ingredients:
            ingredient_container = soup.find(class_=re.compile(r'ingredient', re.I)) or \
                                   soup.find(id=re.compile(r'ingredient', re.I))
            if ingredient_container:
                ingredients = [li.text.strip() for li in ingredient_container.find_all('li')]
        
        return '\n'.join(ingredients) if ingredients else "Ingredients not found"

    def _get_instructions(self, soup, domain):
        instructions = []
        selectors = [
            '.recipe-instructions li',
            '.instructions li',
            '[itemprop="recipeInstructions"]',
            '.preparation-steps li',
            '.prep-steps li',
            '[class*="instruction"] li',
            '[class*="step"] li',
        ]
        for selector in selectors:
            items = soup.select(selector)
            if items:
                instructions = [item.text.strip() for item in items if item.text.strip()]
                break
        
        # Fallback for container search
        if not instructions:
            instruction_container = soup.find(class_=re.compile(r'(instruction|step)', re.I)) or \
                                    soup.find(id=re.compile(r'(instruction|step)', re.I))
            if instruction_container:
                instructions = [li.text.strip() for li in instruction_container.find_all('li')]
        
        return '\n'.join(instructions) if instructions else "Instructions not found"

    def _get_cooking_time(self, soup, domain):
        selectors = [
            '[itemprop="totalTime"]',
            '[itemprop="cookTime"]',
            '.recipe-time',
            '.cooking-time',
            '[class*="time"]',
        ]
        for selector in selectors:
            time_elem = soup.select_one(selector)
            if time_elem:
                return time_elem.text.strip()
        return "Time not specified"

    def _get_servings(self, soup, domain):
        selectors = [
            '[itemprop="recipeYield"]',
            '.recipe-yield',
            '.servings',
            '[class*="yield"]',
            '[class*="serving"]',
        ]
        for selector in selectors:
            serving_elem = soup.select_one(selector)
            if serving_elem:
                return serving_elem.text.strip()
        return "Servings not specified"

    def _format_time(self, iso_time):
        if not iso_time:
            return ""
        iso_time = iso_time.replace('PT', '')
        hours = minutes = 0
        if 'H' in iso_time:
            hours = int(iso_time.split('H')[0])
            iso_time = iso_time.split('H')[1]
        if 'M' in iso_time:
            minutes = int(iso_time.split('M')[0])
        parts = []
        if hours:
            parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
        if minutes:
            parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
        return ' '.join(parts) if parts else "Time not specified"
