from django.shortcuts import render
from bs4 import BeautifulSoup
import requests

# Create your views here.
def home(request):
  # Weather API
  url = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}"
  city = 'Toronto'
  api_key = 'a1c7cdd90159b4459ed96cc67ae2b3ca'
  weather_data = requests.get(url.format(city, api_key)).json()
  icon = weather_data['weather'][0]['icon']

  # Beautiful Soup
  page = requests.get("https://dev.to/")
  soup = BeautifulSoup(page.content, 'html5lib')
  results = soup.find_all("div", class_="crayons-story__body")
  news = []
  for article in results:
    news_obj = {
      'title': article.find("h2").contents[1].string.lstrip(),
      'href': f"https://dev.to{article.find('h2').a['href']}",
      'time': article.find('small').contents[0].string.lstrip()
    }
    print(article.find("h2").contents[1].string.lstrip())
    news.append(news_obj)
  return render(request, 'home.html', {'weather_data': weather_data, 'icon': icon, 'news': news[:8]})

