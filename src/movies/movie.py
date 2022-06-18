class Movie:

    def __init__(self, pk, rnk, n, y, rt) -> None:
        self.pref_key = pk
        self.rank = rnk
        self.name = n
        self.year = y
        self.rating = rt
    
    def __repr__(self) -> str:
        return("The movie {n} is from the year {year} has a rating of {rat}".format(n=self.name, year=self.year, rat=self.rating))

    def ratingGreater(self, r) -> bool:
        if float(self.rating) >= r:
            return True
        return False
    
    def fromYear(self, y) -> bool:
        if self.year == y:
            return True
        return False