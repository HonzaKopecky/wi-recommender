class User:
    def __init__(self, id):
        self.id = id
        self.ratings = dict()

    def add_rating(self, movie, rating):
        self.ratings[movie] = rating

    def get_sum_rating(self):
        sum = 0
        for rating in self.ratings.values():
            if rating is not None:
                sum = sum + rating
        return sum
