import requests
import bs4
import re

#PULL DATA FOR A SUBSET OF THE USTA NORCAL TENNIS TEAM DATA:
#SPECIFALLY FOR: 
  #2016 ADULT 18 & OVER WOMENS 4.0 
  #SF & EB & SB (South Bay) & UP & MA ONLY
#FROM THIS LIST: 
#https://www.ustanorcal.com/listteams.asp?leagueid=1823
#MASTER LIST:
#https://www.ustanorcal.com/listdivisions.asp

data = requests.get('https://www.ustanorcal.com/listteams.asp?leagueid=1823')
soup = bs4.BeautifulSoup(data.text, "html.parser")  

urlsIdArr = []
sql_exp = 'INSERT INTO teams (id, season_id, name, area, num_match_scheduled, num_match_played, matches_won, matches_lost) VALUES'

pattern = re.compile(r'teaminfo.asp')
a_tags = soup.findAll('a', href=pattern)

for a_tag in a_tags:
  area_code = a_tag.find_parent('td').next_sibling.next_sibling.next_sibling.next_sibling.text
  if area_code == 'EB' or area_code == 'SF': #or area_code == 'SB' or area_code == 'UP' or area_code == 'MA':
    #extra last 5 numbers of url only
    urlsIdArr.append(a_tag['href'][-5:])
 
#urlsIdArr = ['68931', '69395', '70194', '69089', '69294', '69415', '69568', '69350', '70076', '69726', '68869', '70162', '69846', '69355', '69815', '69402', '69492', '69401', '69200', '70073', '68989', '69881', '69672', '69026']
url = 'https://www.ustanorcal.com/teaminfo.asp?id='

#create a list with a sub list with data for each player
list_players = []
header_lst = []

for i,url_id in enumerate(urlsIdArr):
  curr_url = url + url_id
  data = requests.get(curr_url)
  soup = bs4.BeautifulSoup(data.text, "html.parser")

  #selects all tables from the page
  tables = soup.select("table")

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
  
  print(area_text)
  print(season)
  print(season_id)
  print(team_name)

  #get num_match_scheduled, num_match_played, matches_won, matches_lost
  local_td = soup.find('td',text=re.compile(r'Local'))
  num_match_scheduled = int(local_td.next_sibling.text)
  num_match_played = int(local_td.next_sibling.next_sibling.text)
  matches_won = int(local_td.next_sibling.next_sibling.next_sibling.text)
  matches_lost = int(local_td.next_sibling.next_sibling.next_sibling.next_sibling.text)

  if (i > 0):
    sql_exp += ','

  team_name = team_name.replace("'", "''") #SINCE INSERTING INTO SQL replace team name with double single apostrophes

  sql_exp += " ({}, {}, '{}', '{}', {}, {}, {}, {})".format(url_id, season_id, team_name, area_text, num_match_scheduled, num_match_played, matches_won, matches_lost)

sql_exp += ";"
print(sql_exp)

  # if team_name == '':
  #   id += 1
  #   continue

  # roster_table = []

  #selects the team roster table because it has cells containing 'expiration' & 'rating'
  # for table in tables:
  #   if table.find('td', string='Expiration') and table.find('td', string='Rating'):
  #     roster_table = table

  #stores the rows from the roster table and removes the 1st row (that only has 'eligibility')
  # rows = roster_table.select('tr')
  # rows.pop(0)

  #create the header row
  # headers = rows.pop(0)
  # header_tds = headers.select('td')
  # header_lst = [header_td.text.rstrip() for header_td in header_tds]
  # header_lst.insert(0, 'Team Name')
  # header_lst.append('Won')
  # header_lst.append('Lost')
  # header_lst.append('Area')
  # header_lst.append('Season')
  # header_lst.append('Team ID')

  #write each player row
  # for row in rows:
  #   tds = row.select('td')
  #   sublist_player = [td.text.rstrip() for td in tds]
  #   sublist_player.insert(0, team_name)
  #   sublist_player.append(url_id)
  #   list_players.append(sublist_player)

  # id += 1

#print(list_players)

# for player in list_players:
#   str_win_loss = player[7]
#   #regex to account for variances in win/loss str
#   # which could be in formats such as:
#   #'17/2 (9/0)', '3 / 0', '5/4', '0 / 1'
#   str_win = re.search(r'(\d+)', str_win_loss).group(0)
#   str_loss = re.search(r'/\s?(\d+)', str_win_loss).group(1)
#   player.insert(-1, str_win) #append Win
#   player.insert(-1, str_loss) #append Loss
#   #add area (e.g., SF)
#   player.insert(-1, area_text)
#   #add season
#   player.insert(-1, season)

# save the data as a tab-separated file
# with open('player_data.tsv', 'w') as tsvfile:
#   writer = csv.writer(tsvfile, delimiter="\t")
#   writer.writerow(header_lst)
#   writer.writerows(list_players)
