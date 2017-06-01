import requests
import bs4
import re
from datetime import datetime

#get teams from league
#get scorecards from teams

league_id_list = [1891, 1894, 1895, 1897, 1856, 1857, 1858, 1859, 1860, 1809, 1810, 1811, 1813, 1814, 1815, 1816, 1818, 1819, 1820, 1821, 1822, 1823, 1824, 1825] #[1872, 1873, 1874, 1875, 1876, 1877, 1878, 1879, 1881, 1882, 1883, 1884, 1885] #NOT IN ALL FILE: [1858, 1924] 

#TEAMS FROM LEAGUES PAGE####################################
league_url = 'https://www.ustanorcal.com/listteams.asp?leagueid='

teams_id_list = []

###NEED TO UNCOMMENT FOR TEAMS
# teams_sql_exp = 'INSERT INTO teams (id, league_id, season_id, org_id, facility_id, name, area, num_match_scheduled, num_match_played, matches_won, matches_lost) VALUES'

for league_id in league_id_list:
  curr_league_url = league_url + str(league_id)
  data = requests.get(curr_league_url)
  soup = bs4.BeautifulSoup(data.text, "html.parser")  

  urlsIdArr = []

  pattern = re.compile(r'teaminfo.asp')
  a_tags = soup.findAll('a', href=pattern)

  for a_tag in a_tags:
    ###NEED TO UNCOMMENT FOR TEAMS
    # area_code = a_tag.find_parent('td').next_sibling.next_sibling.next_sibling.next_sibling.text
    # if area_code == 'EB' or area_code == 'SF': #or area_code == 'SB' or area_code == 'UP' or area_code == 'MA':
      #extract last numbers of url only
    a_team_href = a_tag['href']
    team_id = int(re.match('.*?([0-9]+)$', a_team_href).group(1))
    ###NEED TO UNCOMMENT FOR TEAMS
    # urlsIdArr.append(team_id)
    teams_id_list.append(team_id)
   
  ###NEED TO UNCOMMENT FOR TEAMS
  # url = 'https://www.ustanorcal.com/teaminfo.asp?id='

  # #create a list with a sub list with data for each player
  # list_players = []
  # header_lst = []

  # for url_id in urlsIdArr:
  #   curr_url = url + str(url_id)
  #   data = requests.get(curr_url)
  #   soup = bs4.BeautifulSoup(data.text, "html.parser")

  #   #selects all tables from the page
  #   tables = soup.select("table")

  #   #get league id
  #   pattern_league = re.compile(r'leagueid=')
  #   a_league = soup.find('a', href=pattern_league)
  #   a_league_href = a_league['href']
  #   league_id = int(re.match('.*?([0-9]+)$', a_league_href).group(1))

  #   #get season id
  #   pattern = re.compile(r'seasonid=')
  #   a = soup.find('a', href=pattern)
  #   a_href= a['href']
  #   season_id = int(re.match('.*?([0-9]+)$', a_href).group(1))

  #   #get org id
  #   org_id = 0
  #   org_pattern = re.compile(r'Organization:')
  #   org_a = soup.find(text=org_pattern)
  #   if org_a is not None:
  #     if org_a.next_sibling is not None: 
  #       if org_a.next_sibling.name == 'a':
  #         org_a = org_a.next_sibling
  #         a_org_href= org_a['href']
  #         org_id = int(re.match('.*?([0-9]+)$', a_org_href).group(1))

  #   #get facility id
  #   facility_id = 0
  #   fac_pattern = re.compile(r'Home facility:')
  #   fac_a = soup.find(text=fac_pattern)
  #   if fac_a is not None:
  #     if fac_a.next_sibling is not None:
  #       if fac_a.next_sibling.name == 'a':
  #         fac_a = fac_a.next_sibling
  #         a_fac_href = fac_a['href']
  #         facility_id = int(re.match('.*?([0-9]+)$', a_fac_href).group(1))     

  #   #get team name, season, and area
  #   header_team = tables[1].find_all('td')[-1]
  #   season = header_team.find('b').text
  #   team_name = ''.join(header_team.find('br').next_siblings)

  #   area_text = ''
  #   area_pattern = re.compile(r'Area:')
  #   area_text_full = soup.find(text=area_pattern)
  #   if area_text_full is not None:
  #     if area_text_full.next_sibling is not None:
  #       area_text = area_text_full.next_sibling.text
    
  #   # print(area_text)
  #   # print(season)
  #   print(url_id)
  #   print(team_name)
  #   print(league_id)

#     #get num_match_scheduled, num_match_played, matches_won, matches_lost
#     local_td = soup.find('td',text=' Local')
#     if local_td is not None:
#       num_match_scheduled = int(local_td.next_sibling.text)
#       num_match_played = int(local_td.next_sibling.next_sibling.text)
#       matches_won = int(local_td.next_sibling.next_sibling.next_sibling.text)
#       matches_lost = int(local_td.next_sibling.next_sibling.next_sibling.next_sibling.text)
#     else:
#       num_match_scheduled=0
#       num_match_played=0
#       matches_won=0
#       matches_lost=0

#     if teams_sql_exp[-6:] != 'VALUES':
#       teams_sql_exp += ','

#     #SINCE INSERTING INTO SQL replace any single apostrophes with double single apostrophes  
#     area_text = area_text.replace("'", "''")
#     team_name = team_name.replace("'", "''")

#     teams_sql_exp += " ({}, {}, {}, {}, {}, '{}', '{}', {}, {}, {}, {})".format(url_id, league_id, season_id, org_id, facility_id, team_name, area_text, num_match_scheduled, num_match_played, matches_won, matches_lost)

# teams_sql_exp += ";"


#SCORECARDS AND ROSTERS FROM TEAMS PAGE####################################
scorecards_sql_exp = 'INSERT INTO scorecards (id, home_team_id, visitor_team_id, date, league_id) VALUES'
   
url = 'https://www.ustanorcal.com/teaminfo.asp?id='

rosters_sql_exp = 'INSERT INTO rosters (player_id, name, city, gender, rating, np_sw, expiration, won, lost, matches, defaults, win_percent, singles, doubles, team_id) VALUES'

scorecard_ids = []
league_id = ''

for home_team_id in teams_id_list:
  print(home_team_id)
  curr_url = url + str(home_team_id)
  data = requests.get(curr_url)
  soup = bs4.BeautifulSoup(data.text, "html.parser")

  pattern = re.compile(r'scorecard.asp\?id=')
  a_tags = soup.findAll('a', href=pattern)

  for a_tag in a_tags:
    date_str = a_tag.text

    date = datetime.strptime(date_str, '%m/%d/%y').date()
    print(date)

    a_href = a_tag['href']
    scorecard_id = int(re.match('.*?id=([0-9]+)', a_href).group(1))
    if scorecard_id not in scorecard_ids:
      homeAway = a_tag.parent.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.text
      print(homeAway)
      if league_id == '':
        league_id = int(re.match('.*?:([0-9]+)$', a_href).group(1))
      scorecard_ids.append(scorecard_id)
      visitor_team_a = a_tag.parent.next_sibling.next_sibling.next_sibling.next_sibling
      visiting_a = visitor_team_a.find('a')
      visit_a_href = visiting_a['href']
      visitor_team_id = int(re.match('.*?id=([0-9]+)', visit_a_href).group(1))

      if homeAway == "Away":
        visitor_team_id_temp = visitor_team_id
        visitor_team_id = home_team_id
        home_team_id = visitor_team_id_temp

      #SINCE INSERTING INTO SQL replace any single apostrophes with double single apostrophes  
      # name = name.replace("'", "''")

      if scorecards_sql_exp[-6:] != 'VALUES':
        scorecards_sql_exp += ','

      scorecards_sql_exp += " ({}, {}, {}, '{}', {})".format(scorecard_id, home_team_id, visitor_team_id, date, league_id)

      if homeAway == "Away":
        home_team_id = visitor_team_id

  #selects all tables from the page
  tables = soup.select("table")

  # selects the team roster table because it has cells containing 'expiration' & 'rating'
  for table in tables:
    if table.find('td', text=re.compile(r'Expiration')) and table.find('td', text=re.compile(r'Rating')):
      roster_table = table

  rows = roster_table.select('tr')
  rows.pop(0) #pop off eligibility row
  rows.pop(0) #pop off header row

  # create each player insert statement for each player row
  for row in rows:
    tds = row.select('td')
 
    if tds[0].find('a') is not None:
      player_href = tds[0].find('a')['href']
      player_id = re.match('.*?([0-9]+)$', player_href).group(1)

      sublist_player = [td.text.rstrip() for td in tds]

      name = sublist_player[0]
      city = sublist_player[1]
      gender = sublist_player[2]
      rating = sublist_player[3]
      np_sw = sublist_player[4]
      expiration = sublist_player[5]
      matches = sublist_player[7]

      defaults = sublist_player[8]
      if defaults == "-":
        defaults = 0
      defaults = int(defaults)

      singles = sublist_player[10]
      if singles == "-":
        singles = 0
      singles = int(singles)

      doubles = sublist_player[11]
      if doubles == "-":
        doubles = 0
      doubles = int(doubles)

      team_id = home_team_id
      print(team_id)

      #regex to account for variances in win/loss str
      # which could be in formats such as:
      #'17/2 (9/0)', '3 / 0', '5/4', '0 / 1'
      str_win_loss = sublist_player[6]
      str_win = re.search(r'(\d+)', str_win_loss).group(0)
      str_loss = re.search(r'/\s?(\d+)', str_win_loss).group(1)
      won = int(str_win)
      lost = int(str_loss)

      #NEED WIN %
      win_percent = sublist_player[9]
      win_percent = win_percent.strip('%')
      if win_percent == '-':
        win_percent = 0
      win_percent = int(float(win_percent))

      #SINCE INSERTING INTO SQL replace any single apostrophes with double single apostrophes  
      name = name.replace("'", "''")

      if rosters_sql_exp[-6:] != 'VALUES':
        rosters_sql_exp += ','

      rosters_sql_exp += " ({}, '{}', '{}', '{}', '{}', '{}', '{}', {}, {}, {}, {}, {}, {}, {}, {})".format(player_id, name, city, gender, rating, np_sw, expiration, won, lost, matches, defaults, win_percent, singles, doubles, team_id)

rosters_sql_exp += ";"

scorecards_sql_exp += ";"


#MATCHES FROM SCORECARDS PAGE####################################

matches_sql_exp = 'INSERT INTO matches (id, scorecard_id, match_type, line, h_1_player_id, h_1_player_name, h_2_player_id, h_2_player_name, v_1_player_id, v_1_player_name, v_2_player_id, v_2_player_name, winning_score, winner) VALUES'
   
url = 'https://www.ustanorcal.com/scorecard.asp?id='

match_ids = []
pattern = re.compile(r'playermatches.asp\?id=')

for scorecard_id in scorecard_ids:
  print(scorecard_id)

  curr_url = url + str(scorecard_id)
  data = requests.get(curr_url)
  soup = bs4.BeautifulSoup(data.text, "html.parser")

  singles_table = None
  doubles_table = None

  #selects all tables from the page
  tables = soup.select("table")
  for table in tables:
    if table.find('b', text=re.compile(r'Singles')):
      singles_table = table
    elif table.find('b', text=re.compile(r'Doubles')):
      doubles_table = table

  if singles_table is not None:
    next_s_table = singles_table.next_sibling
    all_rows = next_s_table.findAll('tr')
    del all_rows[0:2]
    for match_row in all_rows:
      tds = match_row.findAll('td')
      line = int(match_row.find('font').text)

      player_as = match_row.findAll('a')

      winner = tds[4].text
      if tds[5].text == "DD":
        h_1_player_id = 'null'
        h_1_player_name = ''
        v_1_player_id = 'null'
        v_1_player_name = ''
      elif tds[5].text == "DF":
        if winner == "Home":
          h_1_player_name = player_as[0].text.rstrip()
          player_1_href = player_as[0]['href']
          h_1_player_id = re.match('.*?([0-9]+)$', player_1_href).group(1)
        elif winner == "Visitor":
          v_1_player_name = player_as[0].text.rstrip()
          player_2_href = player_as[0]['href']
          v_1_player_id = re.match('.*?([0-9]+)$', player_2_href).group(1)
      else:
        h_1_player_name = player_as[0].text.rstrip()
        v_1_player_name = player_as[1].text.rstrip()

        player_1_href = player_as[0]['href']
        h_1_player_id = re.match('.*?([0-9]+)$', player_1_href).group(1)
        player_2_href = player_as[1]['href']
        v_1_player_id = re.match('.*?([0-9]+)$', player_2_href).group(1)

      winning_score = tds[3].text
      h_2_player_id = 'null'
      h_2_player_name = ''
      v_2_player_id = 'null'
      v_2_player_name = ''
      match_type = 'singles'

      # SINCE INSERTING INTO SQL replace any single apostrophes with double single apostrophes  
      h_1_player_name = h_1_player_name.replace("'", "''")
      v_1_player_name = v_1_player_name.replace("'", "''")

      if matches_sql_exp[-6:] != 'VALUES':
        matches_sql_exp += ','

      match_id = str(scorecard_id) + "1" + str(line)
      match_ids.append(match_id)

      matches_sql_exp += " ({}, {}, '{}', {}, {}, '{}', {}, '{}', {}, '{}', {}, '{}', '{}', '{}')".format(match_id, scorecard_id, match_type, line, h_1_player_id, h_1_player_name, h_2_player_id, h_2_player_name, v_1_player_id, v_1_player_name, v_2_player_id, v_2_player_name, winning_score, winner)

  if doubles_table is not None:
    next_d_table = doubles_table.next_sibling
    all_rows = next_d_table.findAll('tr')
    del all_rows[0:2]
    for match_row in all_rows:
      tds = match_row.findAll('td')
      line = int(match_row.find('font').text)
      player_as = match_row.findAll('a')

      winner = tds[4].text

      if tds[5].text == "DD":
        h_1_player_id = 'null'
        h_1_player_name = ''
        v_1_player_id = 'null'
        v_1_player_name = ''
        h_2_player_id = 'null'
        h_2_player_name = ''
        v_2_player_id = 'null'
        v_2_player_name = ''


      elif tds[5].text == "DF":
        if winner == "Home":
          h_1_player_name = player_as[0].text.rstrip()
          h_2_player_name = player_as[1].text.rstrip()

          player_1_href = player_as[0]['href']
          h_1_player_id = re.match('.*?([0-9]+)$', player_1_href).group(1)
          player_2_href = player_as[1]['href']
          h_2_player_id = re.match('.*?([0-9]+)$', player_2_href).group(1)
        elif winner == "Visitor":
          v_1_player_name = player_as[0].text.rstrip()
          v_2_player_name = player_as[1].text.rstrip()

          player_3_href = player_as[0]['href']
          v_1_player_id = re.match('.*?([0-9]+)$', player_3_href).group(1)
          player_4_href = player_as[1]['href']
          v_2_player_id = re.match('.*?([0-9]+)$', player_4_href).group(1)
      else:    
        h_1_player_name = player_as[0].text.rstrip()
        h_2_player_name = player_as[1].text.rstrip()
        v_1_player_name = player_as[2].text.rstrip()
        v_2_player_name = player_as[3].text.rstrip()

        player_1_href = player_as[0]['href']
        h_1_player_id = re.match('.*?([0-9]+)$', player_1_href).group(1)
        player_2_href = player_as[1]['href']
        h_2_player_id = re.match('.*?([0-9]+)$', player_2_href).group(1)
        player_3_href = player_as[2]['href']
        v_1_player_id = re.match('.*?([0-9]+)$', player_3_href).group(1)
        player_4_href = player_as[3]['href']
        v_2_player_id = re.match('.*?([0-9]+)$', player_4_href).group(1)

      winning_score = tds[3].text
      match_type = 'doubles'

      # SINCE INSERTING INTO SQL replace any single apostrophes with double single apostrophes  
      h_1_player_name = h_1_player_name.replace("'", "''")
      h_2_player_name = h_2_player_name.replace("'", "''")
      v_1_player_name = v_1_player_name.replace("'", "''")
      v_2_player_name = v_2_player_name.replace("'", "''")

      if matches_sql_exp[-6:] != 'VALUES':
        matches_sql_exp += ','

      match_id = str(scorecard_id) + "2" + str(line)
      match_ids.append(match_id)

      matches_sql_exp += " ({}, {}, '{}', {}, {}, '{}', {}, '{}', {}, '{}', {}, '{}', '{}', '{}')".format(match_id, scorecard_id, match_type, line, h_1_player_id, h_1_player_name, h_2_player_id, h_2_player_name, v_1_player_id, v_1_player_name, v_2_player_id, v_2_player_name, winning_score, winner)


matches_sql_exp += ";"

####NEED TO UNCOMMENT FOR TEAMS
# full_exp = teams_sql_exp + "\n" + scorecards_sql_exp + "\n" + matches_sql_exp + "\n" + rosters_sql_exp;
full_exp = scorecards_sql_exp + "\n" + matches_sql_exp + "\n" + rosters_sql_exp;

with open('all.sql', 'w') as file:
  file.write(full_exp)
file.close()