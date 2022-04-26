import pandas as pd
import streamlit as st
import numpy as np
data = pd.read_csv('cleaned-data-project-2.csv', index_col=0)
df = data[['playerID', 'commonName', 'league', 'startYear', 'endYear', 'positionWar', 'averageHit', 'patience', 'power', 'speed', 'defense', 'playerLabel', 'shortWar', 'positionCat', 'fact']]
df_NLB = df[df['league'] == 'NLB'].drop(['league', 'playerLabel'], axis = 1)
df_NLB = df_NLB.reset_index().drop('index', axis = 1)
df_MLB_current = df[df['league'] == 'MLB'].drop('league', axis = 1)
df_MLB_current = df_MLB_current[df_MLB_current['playerLabel'] == 'Active Player'].drop('playerLabel', axis = 1)
df_MLB_current = df_MLB_current.reset_index().drop('index', axis = 1)
df_MLB_past = df[df['league'] == 'MLB'].drop('league', axis = 1)
df_MLB_past = df_MLB_past[df_MLB_past['playerLabel'] == 'Hall of Famer'].drop('playerLabel', axis = 1)
df_MLB_past = df_MLB_past.reset_index().drop('index', axis = 1)
opt = {'Options' : [' ','Current', "Hall of Famer", "Both"]}
option = pd.DataFrame(data = opt)
st.sidebar.title('Pick your favorite Baseball Player')
select = st.sidebar.selectbox('Would you like to pick a Current Player or a Hall of Famer?', option.Options)
if select == " ":
    st.title("Negro League Baseball Representation")
    st.write("The Negro Baseball League was an all black baseball league that existed from 1920 to 1960. Because of racial issues of the time the game of baseball was segregated and little attention was paid to this league. To provide some representation to these historic athletes, you can search your favorite MLB players of past and present and learn about their closest match in the Negro League.")
if select == 'Current' :
    current_player = st.sidebar.selectbox('Current Players:', df_MLB_current.commonName)
    df_position = df_NLB
    df_player = df_MLB_current[df_MLB_current['commonName'] == current_player]
    position = df_player['positionCat'].values
    for i in range(0, len(df_NLB['positionCat'])) :
        if df_NLB.iloc[i, 11] != position:
            df_position = df_position.drop(index = i)
    scr = {'Player' : df_position.commonName, 'Score_positionWar' : 0, 'Score_averageHit' : 0, 'Score_patience' : 0, 'Score_power' : 0, 'Score_speed' : 0, 'Score_defense' : 0, 'Score_shortWar' : 0, 'Score' : 0}
    score = pd.DataFrame(data = scr)
    for i in range(0, len(df_position['positionCat'])):
        score.iloc[i,1] = np.abs(df_position.iloc[i,4] - df_player['positionWar'])
        score.iloc[i,2] = np.abs(df_position.iloc[i,5] - df_player['averageHit'])
        score.iloc[i,3] = np.abs(df_position.iloc[i,6] - df_player['patience'])
        score.iloc[i,4] = np.abs(df_position.iloc[i,7] - df_player['power'])
        score.iloc[i,5] = np.abs(df_position.iloc[i,8] - df_player['speed'])
        score.iloc[i,6] = np.abs(df_position.iloc[i,9] - df_player['defense'])
        score.iloc[i,7] = np.abs(df_position.iloc[i,10] - df_player['shortWar'])
        score.iloc[i,8] = np.average(score.iloc[i,1:7])
        recomendation = np.min(score.Score)
        df_recomendation = score[score.Score == recomendation]
        recomend_player = score[score.Score == recomendation]['Player'].values[0]
    df_final = df_recomendation.merge(df_NLB, how = 'inner', left_on = 'Player', right_on = 'commonName')
    startYear = df_final[df_final.Score == recomendation]['startYear'].values[0]
    endYear = df_final[df_final.Score == recomendation]['endYear'].values[0]
    traits = df_final.iloc[:,14:19]
    first_val = traits.max(axis = 1).values[0]
    if first_val == traits.iloc[0,0]:
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
    second_val = traits.max(axis = 1).values[0]
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
    position = df_final[df_final.Score == recomendation]['positionCat'].values[0]
    fact = df_final[df_final.Score == recomendation]['fact'].values[0]
    link = "https://en.wikipedia.org/wiki/" + recomend_player
    link = link.replace(" ", "_")
    st.header("The player in the Negro League who most resembles your favorite player is " + recomend_player + ".")
    st.subheader("Era:")
    st.write(recomend_player, " played from the years ", startYear, " to ", endYear, ".")
    st.subheader("Basic Info:")
    st.write("He was a ",position, " who was best known for his ", first_trait, " and ", second_trait, ".")
    st.subheader("Fun Fact:")
    st.write(fact)
    st.write("Check out this link to learn more!\t", link)
if select == 'Hall of Famer' :
    past_player = st.sidebar.selectbox('Hall of Famers:', df_MLB_past.commonName)
    df_position = df_NLB
    df_player = df_MLB_past[df_MLB_past['commonName'] == past_player]
    position = df_player['positionCat'].values
    for i in range(0, len(df_NLB['positionCat'])):
        if df_NLB.iloc[i, 11] != position:
            df_position = df_position.drop(index = i)
    scr = {'Player' : df_position.commonName, 'Score_positionWar' : 0, 'Score_averageHit' : 0, 'Score_patience' : 0, 'Score_power' : 0, 'Score_speed' : 0, 'Score_defense' : 0, 'Score_shortWar' : 0, 'Score' : 0}
    score = pd.DataFrame(data = scr)
    for i in range(0, len(df_position['positionCat'])):
        score.iloc[i,1] = np.abs(df_position.iloc[i,4] - df_player.iloc[0,4])
        score.iloc[i,2] = np.abs(df_position.iloc[i,5] - df_player.iloc[0,5])
        score.iloc[i,3] = np.abs(df_position.iloc[i,6] - df_player.iloc[0,6])
        score.iloc[i,4] = np.abs(df_position.iloc[i,7] - df_player.iloc[0,7])
        score.iloc[i,5] = np.abs(df_position.iloc[i,8] - df_player.iloc[0,8])
        score.iloc[i,6] = np.abs(df_position.iloc[i,9] - df_player.iloc[0,9])
        score.iloc[i,7] = np.abs(df_position.iloc[i,10] - df_player.iloc[0,10])
        score.iloc[i,8] = np.average(score.iloc[i,1:7])
        recomendation = np.min(score.Score)
        df_recomendation = score[score.Score == recomendation]
        recomend_player = score[score.Score == recomendation]['Player'].values[0]
    df_final = df_recomendation.merge(df_NLB, how = 'inner', left_on = 'Player', right_on = 'commonName')
    startYear = df_final[df_final.Score == recomendation]['startYear'].values[0]
    endYear = df_final[df_final.Score == recomendation]['endYear'].values[0]
    traits = df_final.iloc[:,14:19]
    first_val = traits.max(axis = 1).values[0]
    if first_val == traits.iloc[0,0]:
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
    second_val = traits.max(axis = 1).values[0]
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
    position = df_final[df_final.Score == recomendation]['positionCat'].values[0]
    fact = df_final[df_final.Score == recomendation]['fact'].values[0]
    link = "https://en.wikipedia.org/wiki/" + recomend_player
    link = link.replace(" ", "_")
    st.header("The player in the Negro League who most resembles your favorite player is " + recomend_player + ".")
    st.subheader("Era:")
    st.write(recomend_player, " played from the years ", startYear, " to ", endYear, ".")
    st.subheader("Basic Info:")
    st.write("He was a ",position, " who was best known for his ", first_trait, " and ", second_trait, ".")
    st.subheader("Fun Fact:")
    st.write(fact)
    st.write("Check out this link to learn more!\t", link)
if select == 'Both' :
    current_player = st.sidebar.selectbox('Current Player:', df_MLB_current.commonName)
    past_player = st.sidebar.selectbox('Past Player:', df_MLB_past.commonName)
    df_position = df_NLB
    df_player1 = df_MLB_past[df_MLB_past['commonName'] == past_player]
    df_player2 = df_MLB_current[df_MLB_current['commonName'] == current_player]
    position = [df_player1['positionCat'].values, df_player2['positionCat'].values]
    for i in range(0, len(df_NLB['positionCat'])) :
        if (df_NLB.iloc[i, 11] != position[0]) and (df_NLB.iloc[i, 11] != position[1]):
            df_position = df_position.drop(index = i)
    scr = {'Player' : df_position.commonName, 'Score_positionWar' : 0, 'Score_averageHit' : 0, 'Score_patience' : 0, 'Score_power' : 0, 'Score_speed' : 0, 'Score_defense' : 0, 'Score_shortWar' : 0, 'Score' : 0}
    score = pd.DataFrame(data = scr)
    for i in range(0, len(df_position['positionCat'])):
        score.iloc[i,1] = np.abs((df_position.iloc[i,4] - df_player1.iloc[0,4]) + (df_position.iloc[i,4] - df_player2.iloc[0,4]))
        score.iloc[i,2] = np.abs((df_position.iloc[i,5] - df_player1.iloc[0,5]) + (df_position.iloc[i,5] - df_player2.iloc[0,5]))
        score.iloc[i,3] = np.abs((df_position.iloc[i,6] - df_player1.iloc[0,6]) + (df_position.iloc[i,6] - df_player2.iloc[0,6]))
        score.iloc[i,4] = np.abs((df_position.iloc[i,7] - df_player1.iloc[0,7]) + (df_position.iloc[i,7] - df_player2.iloc[0,7]))
        score.iloc[i,5] = np.abs((df_position.iloc[i,8] - df_player1.iloc[0,8]) + (df_position.iloc[i,8] - df_player2.iloc[0,8]))
        score.iloc[i,6] = np.abs((df_position.iloc[i,9] - df_player1.iloc[0,9]) + (df_position.iloc[i,9] - df_player2.iloc[0,9]))
        score.iloc[i,7] = np.abs((df_position.iloc[i,10] - df_player1.iloc[0,10]) + (df_position.iloc[i,10] - df_player2.iloc[0,10]))
        score.iloc[i,8] = np.average(score.iloc[i,1:7])
        recomendation = np.min(score.Score)
        df_recomendation = score[score.Score == recomendation]
        recomend_player = score[score.Score == recomendation]['Player'].values[0]
    df_final = df_recomendation.merge(df_NLB, how = 'inner', left_on = 'Player', right_on = 'commonName')
    startYear = df_final[df_final.Score == recomendation]['startYear'].values[0]
    endYear = df_final[df_final.Score == recomendation]['endYear'].values[0]
    traits = df_final.iloc[:,14:19]
    first_val = traits.max(axis = 1).values[0]
    if first_val == traits.iloc[0,0]:
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
    second_val = traits.max(axis = 1).values[0]
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
    position = df_final[df_final.Score == recomendation]['positionCat'].values[0]
    fact = df_final[df_final.Score == recomendation]['fact'].values[0]
    link = "https://en.wikipedia.org/wiki/" + recomend_player
    link = link.replace(" ", "_")
    st.header("The player in the Negro League who most resembles your favorite player is " + recomend_player + ".")
    st.subheader("Era:")
    st.write(recomend_player, " played from the years ", startYear, " to ", endYear, ".")
    st.subheader("Basic Info:")
    st.write("He was a ",position, " who was best known for his ", first_trait, " and ", second_trait, ".")
    st.subheader("Fun Fact:")
    st.write(fact)
    st.write("Check out this link to learn more!\t", link)
