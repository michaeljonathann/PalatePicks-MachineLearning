# Import Libraries and Load Data
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import csv
import pickle

df=pd.read_csv('likes.csv')
# df.head()
# df.info()

# store all cafes in a dictionary with their id's, names likes, number of likes and average likes
itemDict = {} # create an empty item Dictionary
# Read in the likes data from the CSV file
with open('likes.csv', mode='r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    next(csv_reader)  # skip the first row
    for row in csv_reader:
        if row[1] == '' or row[2] == '' or row[3] == '' or row[4] == '':
            continue
        # get the right columns
        cafe_id = int(row[1])
        name = row[2]
        user_id = int(row[3])
        like = int(row[4])

        if cafe_id not in itemDict:
            itemDict[cafe_id] = {'name': name, 'likes': [], 'numLikes': 0, 'totalLike': 0}
        itemDict[cafe_id]['likes'].append(like)
        itemDict[cafe_id]['numLikes'] += 1
        itemDict[cafe_id]['totalLike'] += like

# Calculate the average rating for each item
for cafe_id in itemDict:
    cafe = itemDict[cafe_id]
    name = cafe['name']
    likes = cafe['likes']
    numLikes = cafe['numLikes']
    totalLike = cafe['totalLike']
    avgLike = totalLike / numLikes
    itemDict[cafe_id] = {'name': name, 'likes': likes, 'numLikes': numLikes, 'avgLike': avgLike}

# print(itemDict)

# function that finds the distance of an item from another item
def ComputeDistance(a, b):
    # Find the common likes for both item
    common_likes = [like for like in a['likes'] if like in b['likes']]

    # If there are no common likes, the distance is infinity
    if len(common_likes) == 0:
        return float('inf')

    # If the lists of likes are not the same length, return infinity
    if len(a['likes']) != len(b['likes']):
        return float('inf')

    # Calculate the sum of the squared differences between the likes
    sum_squared_differences = sum([(a['likes'][i] - b['likes'][i]) ** 2 for i in range(len(common_likes))])

    # Return the square root of the sum of squared differences, which is the distance between the two items
    return sum_squared_differences ** 0.5

# function to get K-Nearest Neighbors
def getNeighbors(cafe_id, K):
    # Get the item object for the given cafe_id
    target_item = itemDict[cafe_id]

    # Create a list of tuples (distance, itemID) for all items in the dictionary
    distances = [(ComputeDistance(target_item, itemDict[cafe_id]), cafe_id) for cafe_id in itemDict if itemDict[cafe_id]['name'] != target_item['name']]

    # Sort the list of tuples by distance (ascending)
    distances.sort()

    # Return the K nearest neighbors (item with the lowest distances)
    return distances[:K]

# # get the smallest distances as a list
# neighbors = getNeighbors(1, 10)
# # Print the item names and distances of the nearest neighbors
# for distance, cafe_id in neighbors:
#     print(f"{itemDict[cafe_id]['name']}: {distance:.2f}")

with open('palatepicks_model.pkl', 'wb') as f:
    pickle.dump(itemDict, f)