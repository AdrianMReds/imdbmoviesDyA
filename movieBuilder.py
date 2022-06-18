from movie import Movie

#Builder pattern

class MovieBuilder:
    
    def __init__(self):
        self.pref_key = 0
        self.rank = ''
        self. name = ''
        self.year = ''
        self.rating = ''

    @staticmethod
    def item():
        return MovieBuilder()

    def setPrefKey(self, pk):
        self.pref_key = pk
        return self

    def setRank(self, r):
        self.rank = r
        return self

    def setName(self, n):
        self.name = n
        return self

    def setYear(self, y):
        self.year = y
        return self

    def setRating(self, rt):
        self.rating = rt
        return self
    
    def build(self):
        return Movie(self.pref_key ,self.rank, self.name, self.year, self.rating)
