import requests
import bs4
import re

scorecard_id_list = []

matches_sql_exp = 'INSERT INTO scorecards (id, home_team_id, visitor_team_id, date, league_id) VALUES'
   
url = 'https://www.ustanorcal.com/scorecard.asp?id='


match_ids = []

for scorecard_id in scorecard_id_list:
  print(scorecard_id)
  curr_url = url + str(scorecard_id)
  data = requests.get(curr_url)
  soup = bs4.BeautifulSoup(data.text, "html.parser")

  pattern = re.compile(r'scorecard.asp\?id=')
  a_tags = soup.findAll('a', href=pattern)

  for a_tag in a_tags:
    a_href = a_tag['href']
    scorecard_id = int(re.match('.*?id=([0-9]+)', a_href).group(1))
    if league_id == '':
      league_id = int(re.match('.*?:([0-9]+)$', a_href).group(1))
    scorecard_ids.append(scorecard_id)
    visitor_team_a = a_tag.parent.next_sibling.next_sibling.next_sibling.next_sibling
    visiting_a = visitor_team_a.find('a')
    visit_a_href = visiting_a['href']
    visitor_team_id = int(re.match('.*?id=([0-9]+)', visit_a_href).group(1))

    #SINCE INSERTING INTO SQL replace any single apostrophes with double single apostrophes  
    # name = name.replace("'", "''")

    if matches_sql_exp[-6:] != 'VALUES':
      matches_sql_exp += ','

    matches_sql_exp += " ({}, {}, {}, '{}', {})".format(scorecard_id, home_team_id, visitor_team_id, date, league_id)

matches_sql_exp += ";"

with open('matches.sql', 'w') as file:
  file.write(matches_sql_exp)
file.close()

print(matches_sql_exp)
print(match_ids)