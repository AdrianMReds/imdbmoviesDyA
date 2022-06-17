from movie import Movie

class MovieBuilder:
    
    def __init__(self):
        self.rank = ''
        self. name = ''
        self.year = ''
        self.rating = ''

    @staticmethod
    def item():
        return MovieBuilder()

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
        return Movie(self.rank, self.name, self.year, self.rating)
