import requests
from bs4 import BeautifulSoup

class RecipeScraper:
    def __init__(self, url):
        self.url = url
    
    def fetch_page(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Error fetching page: {e}")
            return None
    
    def parse_recipe(self, html):
        soup = BeautifulSoup(html, 'html.parser')

        title = soup.find('h1').text.strip()
        ingredients = [li.text.strip() for li in soup.find_all('li', {'class': 'ingredient'})]
        instructions = [p.text.strip() for p in soup.find_all('p', {'class': 'instruction'})]

        return {"title": title, "ingredients": ingredients, "instructions": instructions}
