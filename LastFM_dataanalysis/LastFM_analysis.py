# Patrick Conway
# INLS 570 - Project 2 - LastFM Data Analysis
# Final Version

from pandas import Series, DataFrame
import pandas as pd
from numpy.random import randn
import numpy as np

print('Welcome to Project 2: LastFM Data Analysis')
print()
# create dataframes
# contains ID, Name, URL, pictureURL of ARTISTS
artists_df = pd.read_table('artists.dat',encoding="utf-8",sep="\t", index_col='id')
# contains ID, artistID and weight of artist for USERS
user_artists_df = pd.read_table('user_artists.dat', encoding="utf-8",sep="\t", index_col = ['userID','artistID'])
#contains userID and list of friends for each USER
user_friends_df = pd.read_table('user_friends.dat',encoding="utf-8",sep="\t", 
                                index_col=['userID'])
# info about tagged artists and the time
user_taggedartists_df = pd.read_table('user_taggedartists.dat',encoding="utf-8",sep="\t",
                                     index_col = ['userID', 'artistID'])
user_taggedartists_time_df = pd.read_table('user_taggedartists-timestamps.dat',encoding="utf-8",sep="\t",
                                          index_col=['userID', 'artistID'])
# contains tagID and tagValue
tags_df = pd.read_table('tags.dat', index_col = ['tagID'])

# question # 1
print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
print()
print('Question 1: Who are the top artists?')
print()
mostplays = user_artists_df.sum(level=1)
q1 = pd.merge(artists_df, mostplays, left_index = True, right_on = 'artistID').sort_values('weight', ascending = False).head(10)
q1 = q1.rename(columns=({'weight': 'plays'}))
print(q1[['name', 'plays']].to_string())

# question #2
print()
print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
print()
print('Question 2: What artists have the most listeners?')
print()
q2 = user_artists_df.swaplevel()
q2 = q2.count(level = 0).sort_values('weight', ascending = False).head(10)
q2 = pd.merge(q2, artists_df, left_index = True, right_index = True)
q2.index.name = 'artistID'
q2.reset_index(inplace=True)
q2 = q2[['name', 'artistID', 'weight']]
q2 = q2.rename(columns = {'name': 'Name', 'weight': 'Number of Listeners'})
print(q2.to_string(index=False))

# question 3
print()
print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
print()
print('Question 3: Who are the top users in terms of play counts?')
print()
q3 = user_artists_df.groupby('userID')['weight'].sum().reset_index().sort_values('weight', ascending = False).head(10)
q3 = q3.rename(columns = {'userID' : 'userID', 'weight': 'plays'})
print(q3.to_string(index=False))

#question 4
print()
print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
print()
print('Question 4: What artists have the highest average number of plays per listener?') 
print()
most_plays = user_artists_df.sum(level=1)
user_plays = user_artists_df.swaplevel()
user_plays = user_plays.count(level = 0)
q4 = pd.merge(user_plays, most_plays, left_index = True, right_index = True)
q4['average_plays'] = (q4['weight_y'] / q4['weight_x']).round()
q4 = q4.sort_values('average_plays', ascending = False)
q4 = pd.merge(q4, artists_df, left_index = True, right_index = True)
q4 = q4[['name', 'weight_y', 'weight_x', 'average_plays']].head(10)
q4 = q4.rename(columns = {'weight_y': 'total_plays', 'weight_x':'listeners'})
print(q4.to_string())

#question 5
print()
print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
print()
print('Question 5: What artists with at least 50 listeners have the highest average number of plays per listener?')
print()
most_plays = user_artists_df.sum(level=1)
user_plays = user_artists_df.swaplevel()
user_plays = user_plays.count(level = 0)
# print(most_plays)
# print(user_plays)
q5 = pd.merge(user_plays, most_plays, left_index = True, right_index = True)
q5['average_plays'] = (q5['weight_y'] / q5['weight_x']).round()
filter = q5['weight_x'] > 50
q5 = q5.rename(columns = {'weight_x': 'Listeners', 'weight_y': 'total_plays'})
q5 = q5.where(filter).sort_values('average_plays', ascending = False).head(10)
final_q5 = pd.merge(artists_df, q5, left_index=True, right_index=True)
print(final_q5[['name','total_plays', 'Listeners', 'average_plays' ]].sort_values('average_plays', ascending=(False)))


#question 6
# Q6 - artist similartities
print()
print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
print()
print('Question 6: Artist Similarity Function Demonstration.')
print()

# generate a list of artists, followed by the users. When i do '.loc[artistID]' on this table, i can pull
# a list of users that have played the artist.
q6 = user_artists_df.swaplevel()
def artist_sim(aid1, aid2):
    # get a list of users who have played that artist.
    # https://pandas.pydata.org/docs/reference/api/pandas.Index.tolist.html
    artist1 = set(q6.loc[aid1].index.tolist())
    artist2 = set(q6.loc[aid2].index.tolist())
    #generate the union of the two sets
    # https://www.programiz.com/python-programming/methods/set/union
    union = artist1.union(artist2)
    # generate the intersection of the two artist sets.
    # https://www.programiz.com/python-programming/methods/set/intersection
    intersect = artist1.intersection(artist2)
    # jacard index is the intersection divided by the union. len() will get the count. 
    jacard = (len(intersect) / len(union))
    print(jacard)

    
print('Similarity between artist 735 and 562: ')
artist_sim(735,562)
print('Similarity between artist 735 and 89: ')
artist_sim(735,89)
print('Similarity between artist 735 and 289: ')
artist_sim(735,289)
print('Similarity between artist 89 and 289: ')
artist_sim(89,289)
print('Similarity between artist 89 and 67: ')
artist_sim(89,67)
print('Similarity between artist 67 and 735: ')
artist_sim(67,735)

#question 7
#implement a feature that recommends artists to a user based on what their friends have been listening to.

# take a user id as input and will output a list of the top 10 artists that should be recommended to that user
# based on their friends’ listening frequencies

def recommend(user_id):
    # get list of friends based on user id.
    friends = user_friends_df.loc[user_id]['friendID'].to_list()
    
    # create a dataframe of the artists that multiple friends have listened
    # to, as well as the count of friends who have listened to this artist.
    artists = user_artists_df.loc[friends].count(level=1).sort_values('weight', ascending = False)
    
    # filter to only the artists where mutiple friends have listened.
    artists = artists.where(artists['weight'] >= 2, inplace = False).dropna()
    
    # dataframe of the total plays of the artists that the friends have listened to. 
    # this will be used to calculate the average.
    plays = user_artists_df.loc[friends].groupby('artistID').sum().sort_values('weight', ascending=False)
    # create a joined table that has the above information.
    combined = pd.merge(artists, plays, left_index=True, right_index=True)
    
    # create a column that takes the total amount of plays amongst friends and divide by the
    # number of users.
    combined['influence'] = (combined['weight_y'] / combined['weight_x'])
    
    # trim this to the top 10. 
    combined = combined.sort_values('influence', ascending = False).head(10)
    
    # create a list of the artists (the index)
    recommendations = combined.index.to_list()
    print('Hello, user',str(user_id) + ',', "Based on your friends' listening habits, we recommend you try the following artists: ")
    for item in recommendations:
        print('ArtistID: ', item)
    
print()
print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
print()
print('Question 7: Recommending music based on friends.')
print()
recommend(2)
print()
recommend(4)
print()
recommend(135)