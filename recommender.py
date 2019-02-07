from model.user import User
from lib.parser import Parser
from model.database import Database
from lib.algorithm import preprocess, create_matrices, do_update, count_error, root_mean_square_error
from numpy import matmul, transpose
from random import randint

# RECOMMENDER SYSTEMS
#   - recommender systems help to match users and items, lower information overload using the information
#   - we know about the user
#   - the task is to generate a ranking score for each item saying whether the user will like the recommended product
#   1. Content based filtering
#       - show the user more things he likes
#       - based on history of the user and the information about items
#   2. Collaborative filtering
#       - show what is popular between like minded people
#       - based on users ratings and other users ratings
#   3. Hybrid
#       - combining all the information together to provide as accurate prediction as possible

# CONTENT BASED FILTERING
# Basic method
#   - adaptive process - user accepting recommendation improves recommender
#   - basic method is to represent user profile same as an item
#   - some data are structured some others are not
#   - similarity between user and item is computed
#   - similarity measure will be different for different attributes (text, ratings, price, ...)
# Similarity to product recommendation
#   - for kNN we might be using nearest neighbors to predict rating that a user would give to an item
#   - that is basically the same what we did in assignment 2
#   - the only difference is that we are considering friendships instead of user similarity
# Memory filtering
#   - the predictions are made from raw items at runtime
#   - does not scale well as the amount of items might be huge
#   - easy to add new items as everything happens at runtime
# Model-based filtering
#   - items represented in a static pre-computed model
#   - predictions are made based on the model
#   - scales much better
#   - adding new items might be difficult / worst case is periodical retraining of the model
# Implementation is collaborative filtering
# Advantages & drawbacks
#   + does not require a community
#   + transparency - only based on users history
#   + new items are not problem - when using the right model
#   - no data for a new user
#   - many similar recommendations - serendipity problem
# Extending to hybrid
#   - user history, movie descriptions, genres, movie review etc.

# COLLABORATIVE FILTERING
# User based kNN
#   - input is the ratings matrix provided by the community
#   - outputs ranked list of items based on the rating predictions
#   - assumption is that similar users have similar tastes and that the tastes do not change a lot
#   - that is what I did in the assignment
# Item based kNN
#   - input is the ratings matrix provided by the community
#   - output rating of an item for a user
#   - looking for similar items (items with similar ratings)
#   - computing the prediction according to ratings of similar products
# Matrix factorization
#   - goal is to reduce the number of dimensions that are stored
#   - for example the netflix matrix is pretty huge
#   - SVD theorem says we can approximate matrix by keeping only the most important features
# SVD-Funk
#   - uses matrix factorization idea
#   - user is not interpreted by all ratings but just K factors / member of communities
#   - movie is represented by the same K of ratings / ratings of the communities
#   - to find the matrices we need to minimize error between the original matrix and the new ones
#   - during finding this matrix we also fill in the missing values
#   - using stochastic gradient descent - doing small steps in the right direction
# Cut corners
#   - weight decay - that's why I get predictions > 5
#   - preprocessing
#   - final prediction - multiplication of A and B
# Some notes
#   - there is certain threshold of RMSE and the accumulated error that I cannot overcome
#   - that is probably all right because of overtraining of the model
#   - it is very well visible that the learning slows down as the accumulated error difference is decreasing with every
#   - update iteration


def print_matrix(a):
    for i in range(0, len(a)):
        for j in range(0, len(a[i])):
            print(str(a[i][j]) + ', ', end='')
        print('')


def random_pair(data):
    r = u = m = None
    while r is None:
        u = randint(1, U_LIM)
        m = randint(1, M_LIM)
        if u in data and m in data[u].ratings:
            r = data[u].ratings[m]
    return u, m, r


U_LIM = M_LIM = 400
K_MAX = 40
data_file = 'out/training'

data = dict()
# read training data - actual rating values included
Parser.read_data(data, 'data/u1.base', U_LIM, M_LIM, False)
# read test data - actual rating values dropped
Parser.read_data(data, 'data/u1.test', U_LIM, M_LIM, True)
Parser.save_dump(data, data_file)

##########################################

# data = Parser.load_dump(data_file)

db = Database(data)

# preprocess(db)

a, b = create_matrices(db, K_MAX)

# printMatrix(a)
# printMatrix(b)

for i in range(0, 800000):
    u, m, r = random_pair(data)
    do_update(db, a, b, u, m, K_MAX)
    if i % 10000 == 0:
        print(str(count_error(db, a, b, K_MAX)))



# printMatrix(a)
# printMatrix(b)

predictions = matmul(a, transpose(b))

# printMatrix(r)

testdata = dict()
Parser.read_data(testdata, 'data/u1.base', U_LIM, M_LIM, False)
tdb = Database(testdata)
rmse = root_mean_square_error(tdb, predictions)

print(rmse)