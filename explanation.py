import requests
from bs4 import BeautifulSoup

url = "https://www.africanbites.com/ndole/"

response = requests.get(url)

# raise an error if the request failed
response.raise_for_status()

content = response.content

print(content[:100])
soup = BeautifulSoup(content, "html.parser")