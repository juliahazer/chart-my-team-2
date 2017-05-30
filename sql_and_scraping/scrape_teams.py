import requests
import bs4
import re


league_id_list = [1891, 1894, 1895, 1897, 1872, 1873, 1874, 1875, 1876, 1877, 1878, 1879, 1881, 1882, 1883, 1884, 1885, 1886, 1887, 1888, 1889, 1939, 1940, 1941, 1942, 1943, 1944, 1945, 1947, 1948, 1949, 1950, 1951, 1952, 1953, 1954, 1955, 1956, 1909, 1910, 1912, 1914, 1915, 1917, 1918, 1919, 1920, 1921, 1922, 1916, 1923, 1924, 1969, 1970, 1971, 1972, 1973, 1974, 1975, 1976, 1931, 1932, 1933, 1957, 1934, 1935, 1936, 1964, 1965, 1966, 1967, 1968, 1925, 1926, 1927, 1928, 1977, 1707, 1708, 1711, 1713, 1689, 1690, 1691, 1692, 1693, 1695, 1694, 1696, 1697, 1698, 1699, 1700, 1701, 1702, 1703, 1704, 1705, 1809, 1810, 1811, 1813, 1814, 1815, 1816, 1818, 1819, 1820, 1821, 1822, 1823, 1824, 1825, 1780, 1781, 1782, 1783, 1784, 1785, 1786, 1787, 1788, 1789, 1790, 1861, 1862, 1863, 1864, 1865, 1866, 1867, 1868, 1798, 1799, 1800, 1801, 1802, 1803, 1856, 1857, 1858, 1859, 1860, 1791, 1792, 1793, 1794, 1855, 1907, 1908, 1421, 1422, 1423, 1424, 1425, 1426, 1428, 1429, 1430, 1431, 1432, 1441, 1442, 1443, 1444, 1515, 1516, 1517, 1518, 1519, 1520, 1521, 1523, 1524, 1525, 1526, 1527, 1528, 1529, 1477, 1478, 1479, 1480, 1490, 1481, 1482, 1483, 1484, 1485, 1551, 1552, 1553, 1554, 1555, 1556, 1557, 1558, 1508, 1509, 1510, 1512, 1513, 1559, 1560, 1561, 1562, 1563, 1564, 1486, 1487, 1488, 1489, 1550, 1492, 1493, 1494, 1495, 1738, 1739, 1168, 1169, 1170, 1171, 1172, 1175, 1176, 1177, 1178, 1179, 1162, 1163, 1164, 1165, 1249, 1250, 1251, 1252, 1253, 1254, 1255, 1257, 1258, 1259, 1260, 1261, 1262, 1220, 1203, 1204, 1205, 1206, 1207, 1208, 1209, 1210, 1211, 1212, 1213, 1214, 1215, 1216, 1217, 1218, 1219, 1224, 1225, 1227, 1228, 1434, 1438, 1440, 1267, 1288, 1289, 1290, 1291, 1292, 1293, 1301, 1302, 1303, 1304, 1264, 1266, 1461, 1462, 1088, 1089, 1090, 1091, 1092, 1093, 1095, 1096, 1097, 1098, 1099, 1101, 1081, 1082, 1083, 1084, 1086, 1130, 1131, 1132, 1133, 1134, 1135, 1136, 1139, 1140, 1141, 1142, 1143, 1144, 1138, 1112, 1113, 1114, 1115, 1116, 1117, 1118, 1119, 1146, 1147, 1148, 1149, 1150, 1151, 1152, 1153, 1120, 1121, 1123, 1124, 1181, 1184, 1185, 1186, 1180, 1155, 1156, 1157, 1158, 1159, 1160, 1161, 1126, 1127, 1128, 1129, 1154, 1187, 1188, 880, 972, 973, 974, 975, 978, 979, 980, 981, 982, 983, 998, 985, 986, 987, 988, 989, 999, 1000, 1025, 1026, 1027, 1028, 1029, 1030, 1038, 1031, 1032, 1033, 1034, 1035, 1036, 1037, 1087, 1062, 1063, 1064, 1065, 1051, 1052, 1053, 1054, 1055, 1056, 1017, 1042, 1008, 1009, 1010, 1011, 1012, 1013, 1014, 1015, 1044, 1045, 1046, 1048, 1049, 1050, 1020, 1021, 1023, 1024, 1110, 1111, 1061] 

# league_id_list =[858, 868, 827, 828, 829, 884, 885, 886, 887, 888, 889, 890, 891, 892, 893, 894, 895, 896, 897, 939, 940, 941, 942, 871, 872, 873, 874, 875, 876, 877, 945, 1004, 831, 832, 833, 834, 837, 838, 839, 840, 932, 933, 934, 936, 937, 938, 902, 903, 905, 906, 943, 778, 779, 780, 781, 782, 783, 784, 785, 786, 787, 788, 789, 790, 791, 793, 813, 814, 815, 816, 817, 819, 820, 821, 822, 823, 863, 808, 809, 810, 811, 771, 777, 772, 773, 774, 775, 776, 742, 743, 744, 745, 747, 748, 749, 750, 865, 801, 802, 803, 805, 806, 807, 794, 795, 796, 797, 798, 799, 825, 638, 639, 640, 641, 642, 643, 645, 646, 647, 648, 649, 690, 691, 692, 693, 694, 695, 696, 697, 698, 699, 700, 701, 702, 703, 705, 770, 731, 732, 733, 734, 735, 737, 738, 739, 740, 726, 727, 728, 729, 668, 669, 670, 671, 672, 673, 767, 651, 652, 653, 654, 657, 658, 659, 660, 718, 719, 720, 723, 724, 725, 712, 713, 714, 715, 716, 717, 575, 576, 577, 578, 579, 581, 582, 583, 584, 604, 605, 606, 607, 608, 609, 610, 611, 612, 613, 614, 615, 616, 617, 619, 626, 627, 628, 629, 586, 587, 588, 589, 590, 591, 593, 594, 595, 596, 599, 600, 601, 602, 630, 631, 632, 635, 636, 620, 621, 622, 623, 624, 625, 510, 511, 512, 513, 514, 515, 516, 517, 518, 519, 520, 521, 522, 523, 525, 562, 563, 564, 565, 492, 493, 494, 495, 496, 497, 499, 500, 501, 502, 505, 506, 507, 508, 566, 567, 568, 569, 571, 572, 573, 526, 527, 528, 529, 560, 561, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 461, 482, 483, 484, 485, 487, 488, 489, 490, 491, 468, 469, 470, 471, 428, 429, 430, 431, 432, 433, 435, 436, 437, 438, 441, 442, 443, 444, 472, 473, 474, 475, 477, 478, 479, 462, 463, 465, 466, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 417, 418, 419, 420, 421, 423, 424, 425, 426, 427, 404, 405, 406, 407, 360, 361, 362, 363, 364, 367, 368, 369, 370, 373, 374, 375, 376, 411, 412, 413, 415, 408, 409, 410, 395, 396, 397, 400, 401, 317, 318, 319, 320, 321, 322, 323, 324, 325, 326, 327, 328, 329, 330, 350, 351, 352, 353, 355, 356, 357, 343, 344, 345, 346, 299, 300, 301, 302, 303, 306, 307, 308, 309, 311, 312, 313, 314, 315, 334, 335, 336, 339, 340, 247, 248, 249, 250, 251, 252, 253, 254, 255, 256, 257, 258, 259, 260, 262, 278, 279, 280, 281, 282, 284, 285, 286, 287, 288, 273, 274, 275, 276, 217, 218, 219, 220, 221, 224, 225, 226, 227, 230, 231, 232, 233, 264, 265, 266, 269, 270, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 235, 236, 237, 238, 239, 240, 242, 243, 244, 245, 246, 211, 212, 213, 214, 174, 170, 171, 172, 173, 159, 160, 161, 162, 165, 166, 167, 168, 200, 201, 202, 208, 209, 210, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 139, 140, 124, 120, 121, 122, 123, 125, 110, 111, 112, 113, 114, 115, 116, 117, 118, 144, 145, 146, 152, 153, 154, 155, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 67, 63, 64, 65, 66, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 95, 96, 97, 103, 104, 105, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 21, 22, 23, 24, 25, 13, 14, 15, 16, 17, 18, 19, 20, 49, 50, 51, 56, 57, 58, 59, 26, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

# league_id_list = [1891, 1894, 1895, 1897, 1872, 1873, 1874, 1875, 1876, 1877, 1878]

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

    area_pattern = re.compile(r'Area:')
    area_text= soup.find(text=area_pattern).next_sibling.text
    
    # print(area_text)
    # print(season)
    print(url_id)
    print(team_name)
    print(league_id)

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

    teams_sql_exp += " ({}, {}, {}, {}, {}, '{}', '{}', {}, {}, {}, {})".format(url_id, league_id, season_id, org_id, facility_id, team_name, area_text, num_match_scheduled, num_match_played, matches_won, matches_lost)

teams_sql_exp += ";"

with open('teams.sql', 'w') as file:
  file.write(teams_sql_exp)
file.close()

print(teams_id_list)
