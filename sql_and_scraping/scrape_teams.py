import requests
import bs4
import re

#LEFT TO RUN
#league_id_list = [1921, 1920, 1919, 1918, 1917, 1916, 1908, 1907, 1868, 1867, 1866, 1865, 1864, 1863, 1862, 1861, 1860, 1859, 1858, 1857, 1856, 1855, 1825, 1824, 1823, 1822, 1821, 1820, 1819, 1818, 1816, 1815, 1814, 1813, 1811, 1810, 1809, 1803, 1802, 1801, 1800, 1799, 1798, 1794, 1793, 1792, 1791, 1790, 1789, 1788, 1787, 1786, 1785, 1784, 1783, 1782, 1781, 1780, 1739, 1738, 1713, 1711, 1708, 1707, 1705, 1704, 1703, 1702, 1701, 1700, 1699, 1698, 1697, 1696, 1695, 1694, 1693, 1692, 1691, 1690, 1689, 1564, 1563, 1562, 1561, 1560, 1559, 1558, 1557, 1556, 1555, 1554, 1553, 1552, 1551, 1550, 1529, 1528, 1527, 1526, 1525, 1524, 1523, 1521, 1520, 1519, 1518, 1517, 1516, 1515, 1513, 1512, 1510, 1509, 1508, 1495, 1494, 1493, 1492, 1490, 1489, 1488, 1487, 1486, 1485, 1484, 1483, 1482, 1481, 1480, 1479, 1478, 1477, 1462, 1461, 1444, 1443, 1442, 1441, 1440, 1438, 1434, 1432, 1431, 1430, 1429, 1428, 1426, 1425, 1424, 1423, 1422, 1421, 1304, 1303, 1302, 1301, 1293, 1292, 1291, 1290, 1289, 1288, 1267, 1266, 1264, 1262, 1261, 1260, 1259, 1258, 1257, 1255, 1254, 1253, 1252, 1251, 1250, 1249, 1228, 1227, 1225, 1224, 1220, 1219, 1218, 1217, 1216, 1215, 1214, 1213, 1212, 1211, 1210, 1209, 1208, 1207, 1206, 1205, 1204, 1203]

#next to run (haven't run yet)
league_id_list = [1977, 1976, 1975, 1974, 1973, 1972, 1971, 1970, 1969, 1968, 1967, 1966, 1965, 1964, 1957, 1936, 1935, 1934, 1933, 1932, 1931, 1928, 1927, 1926, 1925, 1924, 1923, 1922]

league_url = 'https://www.ustanorcal.com/listteams.asp?leagueid='

teams_id_list = []

teams_sql_exp = 'INSERT INTO teams (id, league_id, season_id, org_id, facility_id, name, area, num_match_scheduled, num_match_played, matches_won, matches_lost) VALUES'

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

    #get org id
    org_id = 0
    org_pattern = re.compile(r'Organization:')
    org_a = soup.find(text=org_pattern)
    if org_a is not None:
      if org_a.next_sibling is not None: 
        if org_a.next_sibling.name == 'a':
          org_a = org_a.next_sibling
          a_org_href= org_a['href']
          org_id = int(re.match('.*?([0-9]+)$', a_org_href).group(1))

    #get facility id
    facility_id = 0
    fac_pattern = re.compile(r'Home facility:')
    fac_a = soup.find(text=fac_pattern)
    if fac_a is not None:
      if fac_a.next_sibling is not None:
        if fac_a.next_sibling.name == 'a':
          fac_a = fac_a.next_sibling
          a_fac_href = fac_a['href']
          facility_id = int(re.match('.*?([0-9]+)$', a_fac_href).group(1))     

    #get team name, season, and area
    header_team = tables[1].find_all('td')[-1]
    season = header_team.find('b').text
    team_name = ''.join(header_team.find('br').next_siblings)

    area_text = ''
    area_pattern = re.compile(r'Area:')
    area_text_full = soup.find(text=area_pattern)
    if area_text_full is not None:
      if area_text_full.next_sibling is not None:
        area_text = area_text_full.next_sibling.text
    
    # print(area_text)
    # print(season)
    print(url_id)
    print(team_name)
    print(league_id)

    #get num_match_scheduled, num_match_played, matches_won, matches_lost
    local_td = soup.find('td',text=re.compile(r'Local'))
    if local_td is not None:
      num_match_scheduled = int(local_td.next_sibling.text)
      num_match_played = int(local_td.next_sibling.next_sibling.text)
      matches_won = int(local_td.next_sibling.next_sibling.next_sibling.text)
      matches_lost = int(local_td.next_sibling.next_sibling.next_sibling.next_sibling.text)
    else:
      num_match_scheduled=0
      num_match_played=0
      matches_won=0
      matches_lost=0

    if teams_sql_exp[-6:] != 'VALUES':
      teams_sql_exp += ','

    #SINCE INSERTING INTO SQL replace any single apostrophes with double single apostrophes  
    area_text = area_text.replace("'", "''")
    team_name = team_name.replace("'", "''")

    teams_sql_exp += " ({}, {}, {}, {}, {}, '{}', '{}', {}, {}, {}, {})".format(url_id, league_id, season_id, org_id, facility_id, team_name, area_text, num_match_scheduled, num_match_played, matches_won, matches_lost)

teams_sql_exp += ";"

with open('teams.sql', 'w') as file:
  file.write(teams_sql_exp)
file.close()

print(teams_id_list)
