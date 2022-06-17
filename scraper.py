from bs4 import BeautifulSoup
from pyrsistent import m
import requests
from excelGen import ExcelGen
from movie import Movie

class Scraper:
    movieList = []

    def __init__(self, u) -> None:
        self.url = u
    
    def scrape(self, e:ExcelGen) -> ExcelGen:
        try:
            source = requests.get(self.url)
            source.raise_for_status()

            soup = BeautifulSoup(source.text, 'html.parser')

            movies = soup.find('tbody', class_='lister-list').find_all('tr')

            for movie in movies:
                name = movie.find('td', class_='titleColumn').a.text
                rank = movie.find('td', class_='titleColumn').get_text(strip=True).split('.')[0]
                year = movie.find('td', class_='titleColumn').span.text.strip('()')
                rating = movie.find('td', class_='ratingColumn imdbRating').strong.text

                e.appendToSheet(sn='IMDB Top 250 Movies', lst=[rank, name, year, rating])
                mov = Movie(rank, name, year, rating)
                self.movieList.append(mov)

        except Exception as e:
            print(e)
        
        return e

    def getMinRating(self):
        if len(self.movieList) > 0:
            return self.movieList[-1].rating
        else:
            return 0

    def getMaxRating(self):
        if len(self.movieList) > 0:
            return self.movieList[0].rating
        else:
            return 0

    def lookForMovies(self, y) -> bool:
        for m in self.movieList:
            if m.year == y:
                return True
        
        return False
