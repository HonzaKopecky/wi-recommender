from model.user import User
from model.movie import Movie
from random import randint


class Database:
    def __init__(self, data):
        self.users = dict()
        self.movies = dict()
        for user_id in data:
            self.users[user_id] = User(user_id)
            for movie_id in data[user_id].ratings:
                self.users[user_id].add_rating(movie_id, data[user_id].ratings[movie_id])
                if movie_id not in self.movies:
                    self.movies[movie_id] = Movie(movie_id)
                self.movies[movie_id].add_rating(user_id, data[user_id].ratings[movie_id])
        self.align_data()

    def get_movie(self, movie_id):
        return self.movies[movie_id]

    def get_user(self, user_id):
        return self.users[user_id]

    def get_sum_movie(self, movie_id):
        return self.movies[movie_id].get_sum_rating()

    def get_sum_user(self, user_id):
        return self.users[user_id].get_sum_rating()

    def update_pair(self, user_id, movie_id, new_value):
        self.users[user_id].ratings[movie_id] = new_value
        self.movies[movie_id].ratings[user_id] = new_value

    def get_pair(self, user_id, movie_id):
        return self.users[user_id].ratings[movie_id]

    def get_random_pair(self):
        r = u = m = None
        while r is None:
            m = randint(1, len(self.movies))
            u = randint(1, len(self.users))
            if m in self.movies and u in self.users:
                r = self.get_pair(u, m)
        return u, m, r

    def get_all_ratings(self):
        cnt = 0
        sum = 0
        for user in self.users.values():
            for rating in user.ratings.values():
                if rating is not None:
                    cnt = cnt + 1
                    sum = sum + rating
        return cnt, sum

    def align_data(self):
        for user in self.users.values():
            for i in range(1, len(self.movies) + 1):
                if i not in user.ratings:
                    user.add_rating(i, None)
        for movie in self.movies.values():
            for i in range(1, len(self.users) + 1):
                if i not in movie.ratings:
                    movie.add_rating(i, None)
