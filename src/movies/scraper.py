from bs4 import BeautifulSoup
import requests
from excelGen import ExcelGen
from movieBuilder import MovieBuilder

#Class responsible for scraping the information from the IMDB webpage
class Scraper:
    movieList = []

    __instance = None
    url = ''

    #Singleton implemented here
    @staticmethod
    def getInstance():
        if Scraper.__instance == None:
            Scraper()
        return Scraper.__instance


    def __init__(self) -> None:
        if Scraper.__instance != None:
            raise Exception('Scraper exists already!')
        else:
            Scraper.__instance = self

    def scrape(self, e:ExcelGen) -> ExcelGen:
        counter = 0
        try:
            source = requests.get(self.url)
            source.raise_for_status()

            soup = BeautifulSoup(source.text, 'html.parser')

            movies = soup.find('tbody', class_='lister-list').find_all('tr')

            for movie in movies:
                #Observando el código que nos proporcionó el profesor usamos el mismo método para asignar género o (preference_key)
                pref_key = counter % 5 + 1
                name = movie.find('td', class_='titleColumn').a.text
                rank = movie.find('td', class_='titleColumn').get_text(strip=True).split('.')[0]
                year = movie.find('td', class_='titleColumn').span.text.strip('()')
                rating = movie.find('td', class_='ratingColumn imdbRating').strong.text

                e.appendToSheet(sn='IMDB Top 250 Movies', lst=[pref_key, rank, name, year, rating])
                mov = MovieBuilder.item().setPrefKey(pref_key).setRank(rank).setName(name).setYear(year).setRating(rating).build()
                self.movieList.append(mov)
                counter += 1

        except Exception as ex:
            print(ex)
        
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
