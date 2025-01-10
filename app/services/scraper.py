import requests
from bs4 import BeautifulSoup
import re

class RecipeScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

    def scrape(self, url):
        try:
            response = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            recipe = {
                'title': self._get_title(soup),
                'ingredients': self._get_ingredients(soup),
                'instructions': self._get_instructions(soup),
                'cooking_time': self._get_cooking_time(soup),
                'servings': self._get_servings(soup),
                'source_url': url
            }
            return recipe
        except Exception as e:
            breakpoint()
            raise Exception(f"Failed to scrape recipe: {str(e)}")

    def _get_title(self, soup):
        title = soup.find('h1')
        print("Returning title")
        return title.text.strip() if title else "Unknown Recipe"

    def _get_ingredients(self, soup):
        try:
            print("Getting ingredients")
            ingredients = soup.find_all(['li', 'p'], class_=re.compile(r'ingredient', re.I))
            print("Getting ingredients list")
            ingredients_list = soup.select_one(".wprm-recipe-ingredients")
            print(ingredients_list.count(), ingredients_list)
            ingredients = [
                li.text for li in ingredients_list.findall('li')
            ]
            print("Returning ingredients")
        except TypeError as e:
            breakpoint()
        return '\n'.join(ingredients)
        return '\n'.join([i.text.strip() for i in ingredients]) if ingredients else ""

    def _get_instructions(self, soup):
        instructions = soup.find_all(['li', 'p'], class_=re.compile(r'(instruction|step)', re.I))
        print("Returning instructions")
        return ''
        return '\n'.join([i.text.strip() for i in instructions]) if instructions else ""

    def _get_cooking_time(self, soup):
        time_elem = soup.find(text=re.compile(r'(cook|prep|total)\s+time', re.I))
        print("Returning cooking time")
        return ''
        return time_elem.parent.text.strip() if time_elem else "Not specified"

    def _get_servings(self, soup):
        servings = soup.select("wprm-recipe-details-label.wprm-block-text-bold.wprm-recipe-servings-label")
        # servings = soup.find(text=re.compile(r'servings|yields', re.I))
        print("Returning servings")
        return servings.text.strip()
        return servings.parent.text.strip() if servings else "Not specified"
