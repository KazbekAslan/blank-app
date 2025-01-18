import streamlit as st
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt


st.set_page_config(
   page_title = "Aslan Kazbek",
   page_icon="🔱",
   layout="centered",
)
st.title(":blue[Test app] :green[Aslan]")

@st.cache_data
def load_data(url):
   df = pd.read_csv(url, sep=',').iloc[:,:8].drop(columns="MatchTime")
   df['MatchDate'] = pd.to_datetime(df['MatchDate'], format='%Y-%m-%d')
   df['Date'] = df['MatchDate'].dt.date
   df['Year'] = df['MatchDate'].dt.year
   df['Month'] = df['MatchDate'].dt.month

   df_Elo_1 = df[['Date', 'HomeTeam', 'HomeElo']] \
      .rename(columns={'HomeTeam': 'Team', 'HomeElo': 'Elo'})
   df_Elo_2 = df[['Date', 'AwayTeam', 'AwayElo']] \
      .rename(columns={'AwayTeam': 'Team', 'AwayElo': 'Elo'})
   df_Elo = pd.concat([df_Elo_1, df_Elo_2]) \
      .sort_values(by=['Team', 'Date'])

   df_Elo['Rank'] = df_Elo.groupby(['Team', 'Elo'])['Date'] \
      .rank(method='first', ascending=True)
   df_Elo = df_Elo[df_Elo['Rank'] == 1]

   unic_team = df_Elo.copy()
   unic_team['Date'] = pd.to_datetime(unic_team['Date'], format='%Y-%m-%d')
   unic_team['Year'] = unic_team['Date'].dt.year
   unic_team = unic_team.groupby('Year') \
      .agg({'Team': pd.Series.nunique})

   return df, df_Elo, unic_team

def data_for_elo(df):
   df = df.copy()
   if chose_team:
      df = df[df['Team'] == chose_team]
      return df
   return df

def agg_date(df):
   df = df.copy()
   if chose_division:
      df_div = df[df['Division'] == chose_division]
      df_agg = df_div.groupby('Year') \
         .agg({'HomeTeam': pd.Series.nunique}) \
         .rename({'HomeTeam':'Team'})
      return df_agg
   return df
def chose_year_team(df):
   df = df.copy()
   if chose_year:
      value_of_teams = df.reset_index()
      value_of_current_year = value_of_teams[value_of_teams['Year'] == chose_year]
      if chose_year == 2000:
         value_of_teams_year_ago = 0
         return value_of_current_year.iloc[0, 1], value_of_teams_year_ago
      else:
         value_of_teams_year_ago = value_of_teams[value_of_teams['Year'] == (chose_year-1)]
         return value_of_current_year.iloc[0,1], value_of_teams_year_ago.iloc[0,1]

def other_metrics(df):
   df = df.copy()
   if chose_year:
      div_count_teams = df.groupby('Year').agg({'Division':pd.Series.nunique,
                           'MatchDate':pd.Series.nunique,
                           'HomeElo':'max',
                           'AwayElo':'max'
                          }).reset_index()
      div_count_teams['Elo'] = div_count_teams \
         .apply(lambda x: x['HomeElo'] if x['HomeElo'] >= x['AwayElo']
          else x['AwayElo'], axis=1)
      div_count = div_count_teams.copy()
      div_count_teams = div_count[div_count['Year'] == chose_year]
      div_count_teams_ego = div_count[div_count['Year'] == (chose_year - 1)]
      div = div_count_teams.iloc[0, 1]
      match = div_count_teams.iloc[0, 2]
      elo = div_count_teams.iloc[0, 5]
      if chose_year == 2000:
         div_ago = 0
         match_ago = 0
         elo_ego = 0
         return div, match, elo, div_ago, match_ago, elo_ego
      else:
         div_ago = div_count_teams_ego.iloc[0, 1]
         match_ago = div_count_teams_ego.iloc[0, 2]
         elo_ego = div_count_teams_ego.iloc[0, 5]
         return div, match, elo, div_ago, match_ago, elo_ego


data, data_Elo, teams = load_data("Matches.csv")
Division = np.unique(data['Division'])
Team = np.unique(data_Elo['Team'])
Year = np.unique(data['Year'])


with st.sidebar:
   chose_year = st.slider('Choose Year', min_value=min(Year), max_value=max(Year))
   chose_team = st.selectbox('Choose Team', Team)
   chose_division = st.selectbox('Choose Division', Division)

###Метрики
st.subheader(f"{chose_year} Year Key Metrics:", divider='blue')
a,b,c,d = st.columns(4)
div, match, elo, div_ago, match_ago, elo_ego= other_metrics(data)

with a:
   count_teams, count_teams_ago = chose_year_team(teams)
   delta = (count_teams/count_teams_ago-1).round(2)*100
   teams = st.metric('Count_of_Teams', count_teams, delta=f"{delta}%")
with b:
   delta = (div/div_ago-1).round(2)*100
   division = st.metric('Count_of_Division', div, delta=f"{delta}%")
with c:
   delta = (match/match_ago-1).round(2)*100
   match = st.metric('Count_of_Match', match, delta=f"{delta}%")
with d:
   delta = (elo/elo_ego-1).round(2)*100
   elo = st.metric('Max_of_Elo', elo, delta=f"{delta}%")

###Линейный график по райтингу Elo
show_Elo_data = data_for_elo(data_Elo)
show_Div_data = agg_date(data)

st.header("Data of Matches")
st.dataframe(data, height=150)
st.header(f"{chose_team} Elo point")
Elo = show_Elo_data[['Date','Elo']].reset_index(drop=True)
#matplot
fig, ax = plt.subplots(facecolor='black')
fig.set_size_inches((8,3))
ax.plot(Elo['Date'], Elo['Elo'])
ax.tick_params(axis='y', colors='white')
ax.set_xlabel('Date')
ax.xaxis.label.set_color('green')
ax.set_ylabel('Raiting Elo')
ax.yaxis.label.set_color('green')
ax.tick_params(axis='x', colors='white')
st.pyplot(fig)

###Столбчатый график по количеству команд в лиге
st.header(f"Count of teams in {chose_division}")
st.bar_chart(show_Div_data, height=200)