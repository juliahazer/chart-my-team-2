import requests
import bs4
import re

teams_id_list = [71786, 71837, 71491, 71264, 71881, 71966, 71793, 71857, 71904, 71384, 72381, 72205, 71643, 72333, 71358, 71290, 71903, 71364, 71381, 71934, 71370, 72347, 71874, 71794, 71939, 71791, 71895, 71332, 71262, 71901, 71911, 72219, 72042, 72270, 71886, 72118, 71299, 71549, 72073, 71715, 72294, 71570, 71575, 71676, 72140, 72292, 72088, 71951, 72393, 72390, 72391, 72000, 71888, 71498, 72209, 71409, 71607, 71418, 71661, 71562, 71731, 72100, 71496, 72233, 72089, 72092, 71705, 71645, 72255, 72258, 71481, 71608, 71631, 71436, 71300, 71301, 72322, 71909, 71353, 71860, 71949, 72414, 71702, 72363, 72068, 72371, 71346, 71816, 71889, 72364, 71815, 72274, 71524, 72095, 71339, 71842, 72249, 71590, 71769, 72037, 72159, 71985, 71995, 71536, 71944, 71340, 71988, 71460, 71552, 72149, 71236, 71240, 71475, 71841, 72352, 71718, 72295, 72296, 72336, 71739, 72056, 71804, 71571, 71572, 72280, 72281, 72282, 72115, 72267, 71313, 72156, 71612, 71318, 71688, 72012, 71955, 72022, 72361, 72119, 72216, 71334, 72186, 72415, 71706, 72032, 72001, 71400, 71690, 71343, 71878, 71450, 71586, 71249, 71506, 72105, 71444, 71700, 72350, 71312, 71493, 71505, 72328, 71775, 71390, 71890, 71668, 71984, 71788, 71352, 71395, 71478, 72061, 72055, 71869, 72234, 72302, 71653, 71687, 72184, 71657, 71932, 71870, 72384, 71435, 71914, 71303, 72083, 72323, 72324, 71912, 72338, 72203, 71354, 71516, 71979, 71449, 71388, 71534, 71790, 72166, 72167, 71247, 71502, 71295, 71638, 72025, 72148, 72276, 71922, 72287, 71751, 72199, 72158, 72372, 71367, 71270, 71503, 71745, 71785, 72087, 72143, 71356, 72275, 71795, 71887, 71309, 71937, 71884, 72110, 71843, 71483, 72250, 71617, 71940, 71712, 71863, 71986, 72017, 72412, 71538, 71663, 72160, 71819, 71825, 72103, 72183, 71689, 71316, 71365, 71461, 71501, 71708, 72150, 71784, 71799, 71685, 71238, 71375, 71426, 72368, 71523, 71377, 71721, 71755, 72262, 72264, 72225, 71527, 71573, 71805, 72278, 71787, 72284, 72285, 72266, 71314, 71942, 72227, 71317, 71579, 71513, 72240, 71968, 72008, 72389, 71975, 72377, 72348, 72175, 72416, 71335, 71941, 72358, 72076, 72198, 71691, 71342, 71879, 71417, 71994, 71623, 72114, 71250, 71750, 72369, 72123, 71452, 71734, 71391, 72378, 71277, 71348, 71551, 72137, 72244, 72069, 71497, 71330, 71443, 71584, 72261, 71558, 71732, 71834, 71993, 71633, 72015, 71256, 72182, 71891, 72325, 72326, 72204, 72417, 72283, 71978, 71273, 71457, 71743, 72063, 71297, 71464, 71385, 71602, 71376, 71445, 72370, 72373, 71530, 71992, 71379, 71800, 71826, 72407, 71929, 71382, 71938, 72135, 71844, 72303, 71357, 71373, 72195, 72256, 72395, 72397, 71566, 71900, 72277, 71650, 71535, 72387, 71296, 71306, 71344, 72379, 72117, 72359, 72246, 71686, 72120, 71811, 71241, 71425, 71604, 71606, 71710, 72265, 72297, 72174, 71374, 71880, 71989, 72064, 72154, 72420, 72239, 71616, 72419, 72327, 71773, 71960, 71973, 71257, 71547, 71386, 71921, 72034, 71494, 71405, 71419, 72006, 71845, 72304, 71763, 72113, 71539, 71859, 71413, 71404, 72288, 71965, 72028, 72141, 71952, 71446, 71956, 71729, 71639, 71807, 72319, 72355, 72194, 71876, 72169, 71778, 71946, 71765, 71948]

players_sql_exp = 'INSERT INTO players (player_id, name, city, gender, rating, np_sw, expiration, won, lost, matches, defaults, win_percent, singles, doubles, team_id) VALUES'
   
url = 'https://www.ustanorcal.com/teaminfo.asp?id='

for id in teams_id_list:
  curr_url = url + str(id)
  data = requests.get(curr_url)
  soup = bs4.BeautifulSoup(data.text, "html.parser")

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

    team_id = id
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

    if players_sql_exp[-6:] != 'VALUES':
      players_sql_exp += ','

    players_sql_exp += " ({}, '{}', '{}', '{}', '{}', '{}', '{}', {}, {}, {}, {}, {}, {}, {}, {})".format(player_id, name, city, gender, rating, np_sw, expiration, won, lost, matches, defaults, win_percent, singles, doubles, team_id)

players_sql_exp += ";"

with open('players.sql', 'w') as file:
  file.write(players_sql_exp)
file.close()

print(players_sql_exp)