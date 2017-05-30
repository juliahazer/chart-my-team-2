import requests
import bs4
import re

league_id_list = [1891, 1894, 1895, 1897, 1872, 1873, 1874, 1875, 1876, 1877, 1878]

league_url = 'https://www.ustanorcal.com/listteams.asp?leagueid='

teams_id_list = []

teams_sql_exp = 'INSERT INTO teams (id, league_id, season_id, name, area, num_match_scheduled, num_match_played, matches_won, matches_lost) VALUES'

for league_id in league_id_list:
  curr_league_url = league_url + str(league_id)
  data = requests.get(curr_league_url)
  soup = bs4.BeautifulSoup(data.text, "html.parser")  

  urlsIdArr = []

  pattern = re.compile(r'teaminfo.asp')
  a_tags = soup.findAll('a', href=pattern)

  for a_tag in a_tags:
    area_code = a_tag.find_parent('td').next_sibling.next_sibling.next_sibling.next_sibling.text
    # if area_code == 'EB' or area_code == 'SF': #or area_code == 'SB' or area_code == 'UP' or area_code == 'MA':
      #extract last numbers of url only
    a_team_href = a_tag['href']
    team_id = int(re.match('.*?([0-9]+)$', a_team_href).group(1))
    urlsIdArr.append(team_id)
    teams_id_list.append(team_id)
   
  url = 'https://www.ustanorcal.com/teaminfo.asp?id='

  #create a list with a sub list with data for each player
  list_players = []
  header_lst = []

  for url_id in urlsIdArr:
    curr_url = url + str(url_id)
    data = requests.get(curr_url)
    soup = bs4.BeautifulSoup(data.text, "html.parser")

    #selects all tables from the page
    tables = soup.select("table")

    #get league id
    pattern_league = re.compile(r'leagueid=')
    a_league = soup.find('a', href=pattern_league)
    a_league_href = a_league['href']
    league_id = int(re.match('.*?([0-9]+)$', a_league_href).group(1))

    #get season id
    pattern = re.compile(r'seasonid=')
    a = soup.find('a', href=pattern)
    a_href= a['href']
    season_id = int(re.match('.*?([0-9]+)$', a_href).group(1))

    #get team name, season, and area
    header_team = tables[1].find_all('td')[-1]
    season = header_team.find('b').text
    team_name = ''.join(header_team.find('br').next_siblings)

    area_pattern = re.compile(r'Area:')
    area_text= soup.find(text=area_pattern).next_sibling.text
    
    # print(area_text)
    # print(season)
    print(url_id)
    print(team_name)

    #get num_match_scheduled, num_match_played, matches_won, matches_lost
    local_td = soup.find('td',text=re.compile(r'Local'))
    num_match_scheduled = int(local_td.next_sibling.text)
    num_match_played = int(local_td.next_sibling.next_sibling.text)
    matches_won = int(local_td.next_sibling.next_sibling.next_sibling.text)
    matches_lost = int(local_td.next_sibling.next_sibling.next_sibling.next_sibling.text)

    if teams_sql_exp[-6:] != 'VALUES':
      teams_sql_exp += ','

    #SINCE INSERTING INTO SQL replace any single apostrophes with double single apostrophes  
    area_text = area_text.replace("'", "''")
    team_name = team_name.replace("'", "''")

    teams_sql_exp += " ({}, {}, {}, '{}', '{}', {}, {}, {}, {})".format(url_id, league_id, season_id, team_name, area_text, num_match_scheduled, num_match_played, matches_won, matches_lost)

teams_sql_exp += ";"

with open('teams.sql', 'w') as file:
  file.write(teams_sql_exp)
file.close()

print(teams_id_list)
