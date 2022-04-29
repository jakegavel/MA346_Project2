import pandas as pd
import streamlit as st
import numpy as np
data = pd.read_csv('cleaned-data-project-2.csv', index_col=0) #Import the cleaned dataset
df = data[['playerID', 'commonName', 'league', 'startYear', 'endYear', 'positionWar', 'averageHit', 'patience', 'power', 'speed', 'defense', 'playerLabel', 'shortWar', 'positionCat', 'fact']] #Gathers only the desired columns of the data set
df_NLB = df[df['league'] == 'NLB'].drop(['league', 'playerLabel'], axis = 1) #This subsets the dataframe to store only players in the Negro League
df_NLB = df_NLB.reset_index().drop('index', axis = 1)
df_MLB_current = df[df['league'] == 'MLB'].drop('league', axis = 1) #This subsets the dataframe to store only current MLB players
df_MLB_current = df_MLB_current[df_MLB_current['playerLabel'] == 'Active Player'].drop('playerLabel', axis = 1)
df_MLB_current = df_MLB_current.reset_index().drop('index', axis = 1)
df_MLB_past = df[df['league'] == 'MLB'].drop('league', axis = 1)
df_MLB_past = df_MLB_past[df_MLB_past['playerLabel'] == 'Hall of Famer'].drop('playerLabel', axis = 1) #This subsets the dataframe to stre only past MLB players
df_MLB_past = df_MLB_past.reset_index().drop('index', axis = 1)
opt = {'Options' : [' ','Current', "Hall of Famer", "Both"]} #Create the options dictionary for the selectbox
option = pd.DataFrame(data = opt)
st.sidebar.title('Pick your favorite Baseball Player')
select = st.sidebar.selectbox('Would you like to pick a Current Player or a Hall of Famer?', option.Options) #Streamlit selectbox to pick which subseted dataframe we will use
if select == " ": #This will create a home page effect to display information before the usre makes their selection
    st.title("Negro League Baseball Representation")
    st.write("The Negro Baseball League was an all black baseball league that existed from 1920 to 1960. Because of racial issues of the time the game of baseball was segregated and little attention was paid to this league. To provide some representation to these historic athletes, you can search your favorite MLB players of past and present and learn about their closest match in the Negro League.")
if select == 'Current' : #User selected current players to pick from
    current_player = st.sidebar.selectbox('Current Players:', df_MLB_current.commonName) #Selection box of all the current players name in the dataset of current players only
    df_position = df_NLB #Create a new dataframe as to not change the initial dataframe
    df_player = df_MLB_current[df_MLB_current['commonName'] == current_player] #Store only the information of the one selected player
    position = df_player['positionCat'].values #Get just the position of that player
    for i in range(0, len(df_NLB['positionCat'])) :
        if df_NLB.iloc[i, 11] != position:
            df_position = df_position.drop(index = i) #Creates a new dataframe of all NLB players that are the same position as the selected current player
    scr = {'Player' : df_position.commonName, 'Score_positionWar' : 0, 'Score_averageHit' : 0, 'Score_patience' : 0, 'Score_power' : 0, 'Score_speed' : 0, 'Score_defense' : 0, 'Score_shortWar' : 0, 'Score' : 0}
    score = pd.DataFrame(data = scr) #This new dataframe will store all the scoring data for each NLB player
    for i in range(0, len(df_position['positionCat'])): #This for loop calculates the squared difference between all statistics of the NLB players of the same position and the statistics of the selected player
        score.iloc[i,1] = np.square(df_position.iloc[i,4] - df_player['positionWar'])
        score.iloc[i,2] = np.square(df_position.iloc[i,5] - df_player['averageHit'])
        score.iloc[i,3] = np.square(df_position.iloc[i,6] - df_player['patience'])
        score.iloc[i,4] = np.square(df_position.iloc[i,7] - df_player['power'])
        score.iloc[i,5] = np.square(df_position.iloc[i,8] - df_player['speed'])
        score.iloc[i,6] = np.square(df_position.iloc[i,9] - df_player['defense'])
        score.iloc[i,7] = np.square(df_position.iloc[i,10] - df_player['shortWar'])
    norms_of_rows = np.linalg.norm(score.iloc[:,1:8], axis=1 ) #This section normalizes the previously calculated differences and multiplies them by 100 to avoid extremely small values
    norm_score = score.iloc[:,1:8].div(norms_of_rows, axis=0 ) * 100
    norm_score['Score'] = 0
    for i in range(0, len(norm_score['Score_defense'])): #This for loop completes the distance formula and calculates a final score value for each NLB player
        score.iloc[i,8] = np.sqrt(np.sum(norm_score.iloc[i,0:6]))
    recomendation = np.min(score.Score) #This variable holds the lowest score value
    df_recomendation = score[score.Score == recomendation] #This subset gets the one row in the score dataframe where the score is the lowest value
    recomend_player = score[score.Score == recomendation]['Player'].values[0] #This variable stores the name of the player who got the lowest score
    df_final = df_recomendation.merge(df_NLB, how = 'inner', left_on = 'Player', right_on = 'commonName') #By merging the subset of the lowest score value from the score dataframe with the NLB subset so all information that will be outputed about the player will be in one dataframe
    startYear = df_final[df_final.Score == recomendation]['startYear'].values[0] #Holds the start year of the recommended player
    endYear = df_final[df_final.Score == recomendation]['endYear'].values[0] #Holds the end year of the recommended player
    traits = df_final.iloc[:,14:19] #This subsets the final dataset to only include the values of the characteristic scores
    first_val = traits.max(axis = 1).values[0] #The max value of the characteristic scores
    if first_val == traits.iloc[0,0]: #This section of code checks which of the characteristics is the highest and stores it as first_trait
        first_trait = "hitting"
        traits.averageHit = 0
    elif first_val == traits.iloc[0,1]:
        first_trait = "patience"
        traits.patience = 0
    elif first_val == traits.iloc[0,2]:
        first_trait = "power"
        traits.power = 0
    elif first_val == traits.iloc[0,3]:
        first_trait = "speed"
        traits.speed = 0
    elif first_val == traits.iloc[0,4]:
        first_trait = "defense"
        traits.defense = 0
    second_val = traits.max(axis = 1).values[0] #This section uses the same process to check for the second highest characteristic
    if second_val == traits.iloc[0,0]:
        second_trait = "hitting"
    elif second_val == traits.iloc[0,1]:
        second_trait = "patience"
    elif second_val == traits.iloc[0,2]:
        second_trait = "power"
    elif second_val == traits.iloc[0,3]:
        second_trait = "speed"
    elif second_val == traits.iloc[0,4]:
        second_trait = "defense"
    position = df_final[df_final.Score == recomendation]['positionCat'].values[0] #This variable stores the position of the recommended player
    fact = df_final[df_final.Score == recomendation]['fact'].values[0] #This variable stores the position of the recommended player
    link = "https://en.wikipedia.org/wiki/" + recomend_player #This creates a string of a general link to the recommended players wikipedia page
    link = link.replace(" ", "_")
    st.header("The player in the Negro League who most resembles your favorite player is " + recomend_player + ".") #This section writes all of the formatted variables to a streamlit page
    st.subheader("Era:")
    st.write(recomend_player, " played from the years ", startYear, " to ", endYear, ".")
    st.subheader("Basic Info:")
    st.write("He was a ",position, " who was best known for his ", first_trait, " and ", second_trait, ".")
    st.subheader("Fun Fact:")
    st.write(fact)
    st.write("Check out this link to learn more!\t", link)
if select == 'Hall of Famer' : #User selected Hall of Fame players to pick from
    past_player = st.sidebar.selectbox('Hall of Famers:', df_MLB_past.commonName) #Selection box of all the current players name in the dataset of past players only
    df_position = df_NLB #Create a new dataframe as to not change the initial dataframe
    df_player = df_MLB_past[df_MLB_past['commonName'] == past_player] #Store only the information of the one selected player
    position = df_player['positionCat'].values #Get just the position of that player
    for i in range(0, len(df_NLB['positionCat'])):
        if df_NLB.iloc[i, 11] != position:
            df_position = df_position.drop(index = i) #Creates a new dataframe of all NLB players that are the same position as the selected current player
    scr = {'Player' : df_position.commonName, 'Score_positionWar' : 0, 'Score_averageHit' : 0, 'Score_patience' : 0, 'Score_power' : 0, 'Score_speed' : 0, 'Score_defense' : 0, 'Score_shortWar' : 0, 'Score' : 0}
    score = pd.DataFrame(data = scr) #This new dataframe will store all the scoring data for each NLB player
    for i in range(0, len(df_position['positionCat'])): #This for loop calculates the squared difference between all statistics of the NLB players of the same position and the statistics of the selected player
        score.iloc[i,1] = np.square(df_position.iloc[i,4] - df_player.iloc[0,4])
        score.iloc[i,2] = np.square(df_position.iloc[i,5] - df_player.iloc[0,5])
        score.iloc[i,3] = np.square(df_position.iloc[i,6] - df_player.iloc[0,6])
        score.iloc[i,4] = np.square(df_position.iloc[i,7] - df_player.iloc[0,7])
        score.iloc[i,5] = np.square(df_position.iloc[i,8] - df_player.iloc[0,8])
        score.iloc[i,6] = np.square(df_position.iloc[i,9] - df_player.iloc[0,9])
        score.iloc[i,7] = np.square(df_position.iloc[i,10] - df_player.iloc[0,10])
    norms_of_rows = np.linalg.norm(score.iloc[:,1:8], axis=1 ) #This section normalizes the previously calculated differences and multiplies them by 100 to avoid extremely small values
    norm_score = score.iloc[:,1:8].div(norms_of_rows, axis=0 ) * 100
    norm_score['Score'] = 0
    for i in range(0, len(norm_score['Score_defense'])): #This for loop completes the distance formula and calculates a final score value for each NLB player
        score.iloc[i,8] = np.sqrt(np.sum(norm_score.iloc[i,0:6]))
    recomendation = np.min(score.Score) #This variable holds the lowest score value
    df_recomendation = score[score.Score == recomendation] #This subset gets the one row in the score dataframe where the score is the lowest value
    recomend_player = score[score.Score == recomendation]['Player'].values[0] #This variable stores the name of the player who got the lowest score
    df_final = df_recomendation.merge(df_NLB, how = 'inner', left_on = 'Player', right_on = 'commonName') #By merging the subset of the lowest score value from the score dataframe with the NLB subset so all information that will be outputed about the player will be in one dataframe
    startYear = df_final[df_final.Score == recomendation]['startYear'].values[0] #Holds the start year of the recommended player
    endYear = df_final[df_final.Score == recomendation]['endYear'].values[0] #Holds the end year of the recommended player
    traits = df_final.iloc[:,14:19] #This subsets the final dataset to only include the values of the characteristic scores
    first_val = traits.max(axis = 1).values[0] #The max value of the characteristic scores
    if first_val == traits.iloc[0,0]: #This section of code checks which of the characteristics is the highest and stores it as first_trait
        first_trait = "hitting"
        traits.averageHit = 0
    elif first_val == traits.iloc[0,1]:
        first_trait = "patience"
        traits.patience = 0
    elif first_val == traits.iloc[0,2]:
        first_trait = "power"
        traits.power = 0
    elif first_val == traits.iloc[0,3]:
        first_trait = "speed"
        traits.speed = 0
    elif first_val == traits.iloc[0,4]:
        first_trait = "defense"
        traits.defense = 0
    second_val = traits.max(axis = 1).values[0] #This section uses the same process to check for the second highest characteristic
    if second_val == traits.iloc[0,0]:
        second_trait = "hitting"
    elif second_val == traits.iloc[0,1]:
        second_trait = "patience"
    elif second_val == traits.iloc[0,2]:
        second_trait = "power"
    elif second_val == traits.iloc[0,3]:
        second_trait = "speed"
    elif second_val == traits.iloc[0,4]:
        second_trait = "defense"
    position = df_final[df_final.Score == recomendation]['positionCat'].values[0] #This variable stores the position of the recommended player
    fact = df_final[df_final.Score == recomendation]['fact'].values[0] #This variable stores the position of the recommended player
    link = "https://en.wikipedia.org/wiki/" + recomend_player #This creates a string of a general link to the recommended players wikipedia page
    link = link.replace(" ", "_")
    st.header("The player in the Negro League who most resembles your favorite player is " + recomend_player + ".") #This section writes all of the formatted variables to a streamlit page
    st.subheader("Era:")
    st.write(recomend_player, " played from the years ", startYear, " to ", endYear, ".")
    st.subheader("Basic Info:")
    st.write("He was a ",position, " who was best known for his ", first_trait, " and ", second_trait, ".")
    st.subheader("Fun Fact:")
    st.write(fact)
    st.write("Check out this link to learn more!\t", link)
if select == 'Both' : #User selected both player sets to pick from
    current_player = st.sidebar.selectbox('Current Player:', df_MLB_current.commonName) #Selection box of all the current players name in the dataset of current players only
    past_player = st.sidebar.selectbox('Past Player:', df_MLB_past.commonName) #Selection box of all the current players name in the dataset of past players only
    df_position = df_NLB #Create a new dataframe as to not change the initial dataframe
    df_player1 = df_MLB_past[df_MLB_past['commonName'] == past_player] #Store only the information of the one selected player
    df_player2 = df_MLB_current[df_MLB_current['commonName'] == current_player] #Store only the information of the other selected player
    position = [df_player1['positionCat'].values, df_player2['positionCat'].values] # list of the two positions of both selected players
    for i in range(0, len(df_NLB['positionCat'])) : #This for loop drops the rows from the position dataframe that doesn't have the same position as either of the two selected players
        if (df_NLB.iloc[i, 11] != position[0]) and (df_NLB.iloc[i, 11] != position[1]):
            df_position = df_position.drop(index = i) #This new dataframe will store all the scoring data for each NLB player
    scr = {'Player' : df_position.commonName, 'Score_positionWar' : 0, 'Score_averageHit' : 0, 'Score_patience' : 0, 'Score_power' : 0, 'Score_speed' : 0, 'Score_defense' : 0, 'Score_shortWar' : 0, 'Score' : 0}
    score = pd.DataFrame(data = scr)
    for i in range(0, len(df_position['positionCat'])): #This for loop calculates the squared difference between the statistics of both selected players and each of the NLB players
        score.iloc[i,1] = np.square((df_position.iloc[i,4] - df_player1.iloc[0,4]) + (df_position.iloc[i,4] - df_player2.iloc[0,4]))
        score.iloc[i,2] = np.square((df_position.iloc[i,5] - df_player1.iloc[0,5]) + (df_position.iloc[i,5] - df_player2.iloc[0,5]))
        score.iloc[i,3] = np.square((df_position.iloc[i,6] - df_player1.iloc[0,6]) + (df_position.iloc[i,6] - df_player2.iloc[0,6]))
        score.iloc[i,4] = np.square((df_position.iloc[i,7] - df_player1.iloc[0,7]) + (df_position.iloc[i,7] - df_player2.iloc[0,7]))
        score.iloc[i,5] = np.square((df_position.iloc[i,8] - df_player1.iloc[0,8]) + (df_position.iloc[i,8] - df_player2.iloc[0,8]))
        score.iloc[i,6] = np.square((df_position.iloc[i,9] - df_player1.iloc[0,9]) + (df_position.iloc[i,9] - df_player2.iloc[0,9]))
        score.iloc[i,7] = np.square((df_position.iloc[i,10] - df_player1.iloc[0,10]) + (df_position.iloc[i,10] - df_player2.iloc[0,10]))
    norms_of_rows = np.linalg.norm(score.iloc[:,1:8], axis=1 ) #This section normalizes the previously calculated differences and multiplies them by 100 to avoid extremely small values
    norm_score = score.iloc[:,1:8].div(norms_of_rows, axis=0 ) * 100
    norm_score['Score'] = 0
    for i in range(0, len(norm_score['Score_defense'])): #This for loop completes the distance formula and calculates a final score value for each NLB player
        score.iloc[i,8] = np.sqrt(np.sum(norm_score.iloc[i,0:6]))
    recomendation = np.min(score.Score) #This variable holds the lowest score value
    df_recomendation = score[score.Score == recomendation] #This subset gets the one row in the score dataframe where the score is the lowest value
    recomend_player = score[score.Score == recomendation]['Player'].values[0] #This variable stores the name of the player who got the lowest score
    df_final = df_recomendation.merge(df_NLB, how = 'inner', left_on = 'Player', right_on = 'commonName') #By merging the subset of the lowest score value from the score dataframe with the NLB subset so all information that will be outputed about the player will be in one dataframe
    startYear = df_final[df_final.Score == recomendation]['startYear'].values[0] #Holds the start year of the recommended player
    endYear = df_final[df_final.Score == recomendation]['endYear'].values[0] #Holds the end year of the recommended player
    traits = df_final.iloc[:,14:19] #This subsets the final dataset to only include the values of the characteristic scores
    first_val = traits.max(axis = 1).values[0] #The max value of the characteristic scores
    if first_val == traits.iloc[0,0]: #This section of code checks which of the characteristics is the highest and stores it as first_trait
        first_trait = "hitting"
        traits.averageHit = 0
    elif first_val == traits.iloc[0,1]:
        first_trait = "patience"
        traits.patience = 0
    elif first_val == traits.iloc[0,2]:
        first_trait = "power"
        traits.power = 0
    elif first_val == traits.iloc[0,3]:
        first_trait = "speed"
        traits.speed = 0
    elif first_val == traits.iloc[0,4]:
        first_trait = "defense"
        traits.defense = 0
    second_val = traits.max(axis = 1).values[0] #This section uses the same process to check for the second highest characteristic
    if second_val == traits.iloc[0,0]:
        second_trait = "hitting"
    elif second_val == traits.iloc[0,1]:
        second_trait = "patience"
    elif second_val == traits.iloc[0,2]:
        second_trait = "power"
    elif second_val == traits.iloc[0,3]:
        second_trait = "speed"
    elif second_val == traits.iloc[0,4]:
        second_trait = "defense"
    position = df_final[df_final.Score == recomendation]['positionCat'].values[0] #This variable stores the position of the recommended player
    fact = df_final[df_final.Score == recomendation]['fact'].values[0] #This variable stores the position of the recommended player
    link = "https://en.wikipedia.org/wiki/" + recomend_player #This creates a string of a general link to the recommended players wikipedia page
    link = link.replace(" ", "_")
    st.header("The player in the Negro League who most resembles your favorite player is " + recomend_player + ".") #This section writes all of the formatted variables to a streamlit page
    st.subheader("Era:")
    st.write(recomend_player, " played from the years ", startYear, " to ", endYear, ".")
    st.subheader("Basic Info:")
    st.write("He was a ",position, " who was best known for his ", first_trait, " and ", second_trait, ".")
    st.subheader("Fun Fact:")
    st.write(fact)
    st.write("Check out this link to learn more!\t", link)
