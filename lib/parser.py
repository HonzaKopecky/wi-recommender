from model.user import User
import pickle


class Parser:
    @staticmethod
    def parse_rating(line):
        values = line.split('\t')
        user_id = int(values[0])
        movie_id = int(values[1])
        rating = int(values[2])
        return {
            'user': user_id,
            'movie': movie_id,
            'value': rating
        }

    @staticmethod
    def read_data(db, filename, user_limit, movie_limit, init_only):
        with open(filename) as file:
            for _, line in enumerate(file):
                rating = Parser.parse_rating(line);
                if rating['user'] > user_limit:
                    continue
                if rating['user'] not in db:
                    db[rating['user']] = User(rating['user'])
                if rating['movie'] > movie_limit:
                    continue
                if init_only:
                    rating['value'] = None
                db[rating['user']].add_rating(rating['movie'], rating['value'])

    @staticmethod
    def save_dump(data, path):
        f = open(path, "wb")
        pickle.dump(data, f)
        f.close()

    @staticmethod
    def load_dump(path):
        f = open(path, "rb")
        return pickle.load(f)

    @staticmethod
    def create_matrix(db):
        r = []
        for user_id in db.users:
            r.append([None] * len(db.movies))
            for movie_id in db.users[user_id].ratings:
                r[user_id - 1][movie_id - 1] = db.users[user_id].ratings[movie_id]
        return r
