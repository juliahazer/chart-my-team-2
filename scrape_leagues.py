import requests
import bs4
# import re

data = requests.get('https://www.ustanorcal.com/listdivisions.asp?seasonid=192')
soup = bs4.BeautifulSoup(data.text, "html.parser")

seasons_sql_exp = 'INSERT INTO seasons (id, year, name) VALUES'

season_id_list = []

options = soup.findAll('option')

for option in options:
  if option['value'] != '0':
    season_id = int(option['value'])
    season_id_list.append(season_id)
    option_text = option.text
    year = int(option_text[0:4])
    name = option_text[5:]
    name = name.rstrip()

    #SINCE INSERTING INTO SQL replace any single apostrophes with double single apostrophes  
    name = name.replace("'", "''")

    if seasons_sql_exp[-6:] != 'VALUES':
      seasons_sql_exp += ','

    seasons_sql_exp += " ({}, {}, '{}')".format(season_id, year, name)

seasons_sql_exp += ";"
# print(seasons_sql_exp)

# with open('seasons.sql', 'w') as file:
#   file.write(seasons_sql_exp)
#   file.close()

print(season_id_list)

for season in season_id_list:
  curr_url = url + url_id
  data = requests.get(curr_url)
  soup = bs4.BeautifulSoup(data.text, "html.parser")


