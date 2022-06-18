#Adrián Montemayor Rojas A01283139
#Iván Gonzalez Luján A00823187

from scraper import Scraper
from excelGen import ExcelGen
import sys
import random

#SOLID Principles

#-Single Responsability-
#Every class has a single responsability
#Scraper is used to scrape the information from the IMDB web page
#ExcelGen is used to generate and modify the excel file
#Movie is used to store the movies information
#MovieBuilder is used to create Movie objects

#Open-Closed Principle
#Code can be extended without modifying what is already done, we could add more functionality, like showing movies with X rating or less, or from certain year to certain year.

def printMenu():
    print('What would you like to do?')
    print('1. Top 250 Movies')
    print('2. Top 250 Movies in descending order')
    print('3. My preference movies')
    print('4. Show movies by rating')
    print('5. Show movies by year')
    print('0. Exit')

#Print the top 250 movies in IMDB
def top250(s:Scraper) -> None:
    for m in s.movieList:
        print('{pk} {rnk}. {mn} {yr} {rtn}'.format(pk=m.pref_key, rnk=m.rank, mn=m.name, yr=m.year, rtn=m.rating))
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

#Print and save movies by X rating or higher
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

#Print and save movies from a certain year
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

#Print movie preferences for the user based on its preference key
def moviePreferences(s:Scraper, e:ExcelGen, upk:int, rat:bool=False) -> ExcelGen:
    sn = 'My movie preferences'
    e.createSheet(sn)
    i = 'Movies I might like'
    e.appendIt(sn, i)
    pkm = []
    for mo in s.movieList:
        if mo.pref_key == upk:
            pkm.append(mo) #Guardamos las películas con esa pref_key
    
    if rat:
        for i in range(10):
            print('{rnk}. {mn} {yr} {rtn}'.format(rnk=pkm[i].rank, mn=pkm[i].name, yr=pkm[i].year, rtn=pkm[i].rating))
            e.appendToSheet(sn, [pkm[i].rank, pkm[i].name, pkm[i].year, pkm[i].rating])
    else:
        #Random sample of movies
        samp = random.sample(pkm, 10)
        for m in samp:
            print('{rnk}. {mn} {yr} {rtn}'.format(rnk=m.rank, mn=m.name, yr=m.year, rtn=m.rating))
            e.appendToSheet(sn, [m.rank, m.name, m.year, m.rating])
    
    print("\nThis information has been captured on the excel file.\n")
    return e

#Generate user preference key
def getUserPrefKey(prefs:str):
    lst = prefs.split()
    for i in range(len(lst)):
        try:
            lst[i] = int(lst[i])
        except Exception as ex:
            return None
    
    u = ((lst[0]*lst[1]*lst[2])%5)+1
    return u

#Main
if __name__ == '__main__':

    egen = ExcelGen('IMDB Movies.xlsx')
    s = Scraper.getInstance()
    #Estas 3 líneas de código comentadas se escribieron para probas el singleton, si gusta probarlo puede descomentarlas
    # s2 = Scraper.getInstance()
    # print(s)
    # print(s2)
    s.url = 'https://www.imdb.com/chart/top/'
    egen = s.scrape(egen)

    called = False
    opt = -1

    print("Welcome, please make sure to have the excel file closed.\n")

    print('Choose your three movie preferences:\n1. Comedy\n2. Drama\n3. Sci-Fi\n4. Romantic\n5. Adventure\n')
    print('Please introduce them in one line with spaces')
    print('For example: 1 2 3')
    ps = input()

    if(getUserPrefKey(ps) != None):
        upk = getUserPrefKey(ps)
    else:
        print('Your input was incorrect, please try running the program again')
        sys.exit()

    print('Your preference key is {}\n'.format(upk))

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
            print('Would you like to see the best rated movies or some random movies you would like?')
            print('1 --> Best rated\n2 --> Random movies')
            a = 0
            while a!=1 and a!=2:
                print('Pick 1 or 2')
                try:
                    a = int(input())
                except:
                    print('Invalid input')
                    continue
            if a==1:
                egen = moviePreferences(s,egen, upk, True)
            else:
                egen = moviePreferences(s,egen, upk)
            
        elif opt == 4:
            print("I want to see movies with rating X or higher")
            r = float(input("X = "))
            if r < float(s.getMinRating()) or r > float(s.getMaxRating()):
                print("There are no movies with this rating.")
                continue
            egen = moviesByRating(s,egen,r)
        elif opt == 5:
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

