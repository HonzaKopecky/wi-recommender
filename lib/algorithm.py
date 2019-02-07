from math import sqrt


def preprocess(db):
    n, sum = db.get_all_ratings()
    avg = sum / n
    for u in db.users:
        mu = len(db.get_user(u).ratings)
        sum_rru = db.get_sum_user(u)
        for m in db.users[u].ratings:
            rmu = db.get_pair(u, m)
            if rmu is None:
                continue
            sum_rms = db.get_sum_movie(m)
            um = len(db.get_movie(m).ratings)
            new_value = rmu - (sum_rms / um) - (sum_rru / mu) + avg
            db.update_pair(u, m, new_value)


def create_matrices(db, k):
    DEF_VALUE = 0.3
    a = list()
    b = list()
    for i in range(0, len(db.movies)):
        a.append(list())
        for j in range(0, k):
            a[i].append(DEF_VALUE)
    for i in range(0, len(db.users)):
        b.append(list())
        for j in range(0, k):
            b[i].append(DEF_VALUE)
    return a, b


def do_update(db, a, b, u, m, k_max):
    rmu = db.get_pair(u, m)
    u = u - 1
    m = m - 1
    sum_i = get_k_sum(a, b, k_max, u, m)
    for k in range(0, k_max):
        amk = a[m][k]
        bku = b[u][k]
        new_amk = amk + (0.001 * (rmu - sum_i) * bku)
        # maybe the updated amk value should be used below
        new_bku = bku + (0.001 * (rmu - sum_i) * amk)
        a[m][k] = new_amk
        b[u][k] = new_bku


def get_k_sum(a, b, k_max, u, m):
    sum = 0
    for k in range(0, k_max):
        sum = sum + (a[m][k] * b[u][k])
    return sum


def count_error(db, a, b, max_k):
    error_sum = 0
    for u in range(0, len(db.users) - 1):
        for m in range(0, len(db.movies) - 1):
            rmu = db.get_pair(u + 1, m + 1)
            if rmu is None:
                continue
            my = 0
            for k in range(0, max_k):
                my = my + a[m][k] * b[u][k]
            error_sum = error_sum + pow((rmu - my), 2)
    return error_sum


def root_mean_square_error(realdb, predictions_matrix):
    error_sum = 0
    cnt = 0
    for u in realdb.users:
        for m in realdb.movies:
            if u not in realdb.users or m not in realdb.users[u].ratings:
                continue
            real = realdb.get_pair(u, m)
            if real is None:
                continue
            prediction = predictions_matrix[u-1][m-1]
            # print('real: ' + str(real) + ', predicted: ' + str(prediction))
            error_sum = error_sum + pow((prediction - real), 2)
            cnt = cnt + 1
    return sqrt((error_sum / cnt))
