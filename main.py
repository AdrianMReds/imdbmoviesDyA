#Adrián Montemayor Rojas A01283139
#Iván Gonzalez Luján

# from movie import Movie
from scraper import Scraper
from excelGen import ExcelGen



def printMenu():
    print('What would you like to do?')
    print('1. Top 250 Movies')
    print('2. Top 250 Movies in descending order')
    print('3. Show movies by rating')
    print('4. Show movies by year')
    print('0. Exit')

#Print the top 250 movies in IMDB
def top250(s:Scraper) -> None:
    for m in s.movieList:
        print('{rnk}. {mn} {yr} {rtn}'.format(rnk=m.rank, mn=m.name, yr=m.year, rtn=m.rating))
        print()

#Print the top 250 movies in IMDB in descending order
def top250Desc(s:Scraper, e:ExcelGen, called:bool=False) -> ExcelGen:
    if called==False:
        sn = 'Top 250 Movies Descending'
        e.createSheet(sn)
        i = 'Search # 1 and only'
        e.appendIt(sn, i)
    for m in reversed(s.movieList):
        print('{rnk}. {mn} {yr} {rtn}'.format(rnk=m.rank, mn=m.name, yr=m.year, rtn=m.rating))
        if called==False:
            e.appendToSheet(sn, [m.rank, m.name, m.year, m.rating])
    
    print("\nThis information has been captured on the excel file.\n")
    return e

def moviesByRating(s:Scraper, e:ExcelGen, r:float) -> ExcelGen:
    sn = 'Movies by Rating'
    e.createSheet(sn)
    i = 'Search Movies with rating {} or higher'.format(str(r))
    e.appendIt(sn, i)
    for m in s.movieList:
        if m.ratingGreater(r):
            print('{rnk}. {mn} {yr} {rtn}'.format(rnk=m.rank, mn=m.name, yr=m.year, rtn=m.rating))
            e.appendToSheet(sn, [m.rank, m.name, m.year, m.rating])
    
    print("\nThis information has been captured on the excel file.\n")
    return e

def moviesByYear(s:Scraper, e:ExcelGen, y:str) -> ExcelGen:
    sn = 'Movies by Year'
    e.createSheet(sn)
    i = 'Search Movies from the year {}'.format(y)
    e.appendIt(sn, i)
    for m in s.movieList:
        if m.fromYear(y):
            print('{rnk}. {mn} {yr} {rtn}'.format(rnk=m.rank, mn=m.name, yr=m.year, rtn=m.rating))
            e.appendToSheet('Movies by Year', [m.rank, m.name, m.year, m.rating])
    
    print("\nThis information has been captured on the excel file.\n")
    return e



if __name__ == '__main__':

    egen = ExcelGen('IMDB Movies.xlsx')
    s = Scraper('https://www.imdb.com/chart/top/')
    egen = s.scrape(egen)

    called = False
    opt = -1

    print("Welcome, please make sure to have the excel file closed.\n")

    while opt != 0:
        printMenu()
        opt = input()
        
        try:
            opt = int(opt)
        except Exception as e:
            print("Please type a number\n")
            continue

        if opt == 1:
            top250(s)
        elif opt == 2:
            egen = top250Desc(s,egen,called)
            called = True
        elif opt == 3:
            print("I want to see movies with rating X or higher")
            r = float(input("X = "))
            if r < float(s.getMinRating()) or r > float(s.getMaxRating()):
                print("There are no movies with this rating.")
                continue
            egen = moviesByRating(s,egen,r)
        elif opt == 4:
            print("I want to see movies from the year Y")
            y = input('Y = ')
            if s.lookForMovies(y)==False:
                print("There are no movies made on that year.")
                continue
            egen = moviesByYear(s,egen,y)
        elif opt != 0:
            print("\nThat option is not valid, please enter your option again.\n")
            continue
    
    egen.saveFile()

