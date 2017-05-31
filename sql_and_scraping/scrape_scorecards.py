import requests
import bs4
import re
from datetime import datetime

#teams_id_list = [61885, 61216, 61217, 61627, 61994, 61584, 62297, 61417, 61339, 61864, 62019, 61895, 61900, 61334, 61602, 61700, 61586, 61205]

#league=1699
teams_id_list = [66078, 66114, 66131, 65899, 66744, 66701, 66564, 66565, 66566, 66772, 65684, 66393, 66168, 66219, 66834, 65653, 65760, 66030, 65817, 66498, 66796, 66251, 66174, 65644, 66227, 66397, 66433, 66071, 66414, 65973, 66699, 65733, 65734, 65654, 66420, 65971, 66867, 66034, 66833, 66604, 66896, 65999, 65804, 65779, 65960, 66711, 66550, 66002, 65929, 65941, 65835, 66212, 66144, 66606, 66253, 66813, 66668, 66669, 65751, 65807, 66537, 66445, 66709, 66756, 66705, 66104, 66142, 66820, 66059, 66468, 65769, 66095, 66654, 66557, 65944, 66112, 65703, 65805, 66737, 66762, 65710, 66434, 66704, 66198, 66487, 65918, 66177, 65699, 66271, 66173, 66133, 65685, 65939, 66102, 66872, 66873, 66646, 66672, 66407, 65822, 66396, 66722, 66854, 66780, 66781, 66782, 66783, 66305, 66752, 66181, 66706, 66625, 66626, 65967, 66687, 65993, 66125, 65868, 66392, 66088, 66080, 66455, 66760, 65990, 66128, 65922, 65723, 65781, 66278, 66642, 66842, 65977, 66662, 66266, 66893, 65754, 65659, 65714, 65745, 66033, 66505, 66146, 66664, 66179, 66052, 66431, 66465, 66240, 65655, 65729, 65712, 66531, 66042, 66043, 66725, 66810, 66410, 66459, 66450, 66180, 66244, 66504, 65845, 66635, 66124, 66199, 66558, 66217, 65830, 66644, 65798, 66007, 66232, 66741, 66829, 66218, 66679, 65980, 65956, 65667, 65636, 65639, 65666, 65677, 66264, 66856]

scorecards_sql_exp = 'INSERT INTO scorecards (id, home_team_id, visitor_team_id, date, league_id) VALUES'
   
url = 'https://www.ustanorcal.com/teaminfo.asp?id='


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
      if league_id == '':
        league_id = int(re.match('.*?:([0-9]+)$', a_href).group(1))
      scorecard_ids.append(scorecard_id)
      visitor_team_a = a_tag.parent.next_sibling.next_sibling.next_sibling.next_sibling
      visiting_a = visitor_team_a.find('a')
      visit_a_href = visiting_a['href']
      visitor_team_id = int(re.match('.*?id=([0-9]+)', visit_a_href).group(1))

      #SINCE INSERTING INTO SQL replace any single apostrophes with double single apostrophes  
      # name = name.replace("'", "''")

      if scorecards_sql_exp[-6:] != 'VALUES':
        scorecards_sql_exp += ','

      scorecards_sql_exp += " ({}, {}, {}, '{}', {})".format(scorecard_id, home_team_id, visitor_team_id, date, league_id)

scorecards_sql_exp += ";"

with open('scorecards.sql', 'w') as file:
  file.write(scorecards_sql_exp)
file.close()

print(scorecard_ids);
print(scorecards_sql_exp)
