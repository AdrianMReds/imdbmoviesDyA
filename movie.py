class Movie:

    def __init__(self, rnk, na, yr, rtng ) -> None:
        self.rank = rnk
        self.name = na
        self.year = yr
        self.rating = rtng
    
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