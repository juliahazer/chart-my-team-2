import requests
import bs4
import re

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
print(seasons_sql_exp)

with open('seasons.sql', 'w') as file:
  file.write(seasons_sql_exp)
  file.close()

# print(season_id_list)

# season_id_list = [198, 196, 197, 204, 201, 206, 203, 205, 202, 207, 184, 182, 183, 192, 188, 195, 190, 194, 189, 193, 200, 199, 166, 168, 177, 172, 179, 176, 180, 173, 178, 174, 186, 185, 146, 145, 158, 152, 153, 155, 167, 161, 163, 164, 159, 160, 154, 171, 169, 134, 135, 130, 131, 141, 138, 142, 140, 148, 147, 144, 139, 143, 136, 149, 150, 98, 110, 111, 113, 116, 123, 132, 129, 127, 119, 125, 112, 117, 126, 122, 137, 128, 92, 85, 99, 105, 97, 108, 115, 90, 86, 104, 103, 106, 79, 83, 94, 82, 78, 73, 71, 95, 81, 80, 84, 60, 65, 77, 70, 69, 63, 61, 76, 62, 68, 67, 53, 56, 58, 55, 54, 59, 57, 49, 51, 48, 47, 52, 50, 42, 46, 44, 41, 40, 45, 43, 35, 39, 37, 33, 34, 38, 36, 29, 32, 31, 27, 28, 30, 23, 26, 25, 21, 20, 24, 17, 22, 19, 15, 14, 18, 12, 10, 11, 13, 8, 6, 7, 9, 4, 3, 2, 5, 1]


###################NEED TO ADD LOOP FOR ALL SEASONS!!!!!!!!!!!!##################

leagues_sql_exp = 'INSERT INTO leagues (id, year, name, season_id) VALUES'

league_id_list = []

for season in season_id_list:
  curr_url = 'https://www.ustanorcal.com/listdivisions.asp?seasonid=' + str(season)
  data = requests.get(curr_url)
  soup = bs4.BeautifulSoup(data.text, 'html.parser')

  pattern_league = re.compile(r'leagueid=')
  a_leagues = soup.findAll('a', href=pattern_league)
  for a_league in a_leagues:
    a_league_href = a_league['href']
    league_id = int(re.match('.*?([0-9]+)$', a_league_href).group(1))
    league_id_list.append([league_id, season])

print(league_id_list)

for league in league_id_list:
  print(league[0])
  curr_url = 'https://www.ustanorcal.com/listdivisions.asp?leagueid=' + str(league[0])
  data = requests.get(curr_url)
  soup = bs4.BeautifulSoup(data.text, 'html.parser')
  pattern_league = re.compile(r'leagueid=')
  a_league = soup.findAll('a', href=pattern_league)
  full_name = a_league[0].text
  #TO ACCOUNT FOR THIS LEAGUE WHICH STARTS WITH 'DEMO' INSTEAD OF A YEAR: 
  #https://www.ustanorcal.com/listdivisions.asp?leagueid=880
  if full_name[0:4] == "DEMO":
    year = 2010
    name = full_name[0:]
  else:
    year = int(full_name[0:4])
    name = full_name[5:]
  season_id = league[1]

  #SINCE INSERTING INTO SQL replace any single apostrophes with double single apostrophes  
  name = name.replace("'", "''")

  if leagues_sql_exp[-6:] != 'VALUES':
    leagues_sql_exp += ','

  leagues_sql_exp += " ({}, {}, '{}', {})".format(league[0], year, name, season_id)

leagues_sql_exp += ";"
print(leagues_sql_exp)

with open('leagues.sql', 'w') as file:
  file.write(leagues_sql_exp)
  file.close()

# league_id_list = [1891, 1894, 1895, 1897, 1872, 1873, 1874, 1875, 1876, 1877, 1878, 1879, 1881, 1882, 1883, 1884, 1885, 1886, 1887, 1888, 1889, 1939, 1940, 1941, 1942, 1943, 1944, 1945, 1947, 1948, 1949, 1950, 1951, 1952, 1953, 1954, 1955, 1956, 1909, 1910, 1912, 1914, 1915, 1917, 1918, 1919, 1920, 1921, 1922, 1916, 1923, 1924, 1969, 1970, 1971, 1972, 1973, 1974, 1975, 1976, 1931, 1932, 1933, 1957, 1934, 1935, 1936, 1964, 1965, 1966, 1967, 1968, 1925, 1926, 1927, 1928, 1977, 1707, 1708, 1711, 1713, 1689, 1690, 1691, 1692, 1693, 1695, 1694, 1696, 1697, 1698, 1699, 1700, 1701, 1702, 1703, 1704, 1705, 1809, 1810, 1811, 1813, 1814, 1815, 1816, 1818, 1819, 1820, 1821, 1822, 1823, 1824, 1825, 1780, 1781, 1782, 1783, 1784, 1785, 1786, 1787, 1788, 1789, 1790, 1861, 1862, 1863, 1864, 1865, 1866, 1867, 1868, 1798, 1799, 1800, 1801, 1802, 1803, 1856, 1857, 1858, 1859, 1860, 1791, 1792, 1793, 1794, 1855, 1907, 1908, 1421, 1422, 1423, 1424, 1425, 1426, 1428, 1429, 1430, 1431, 1432, 1441, 1442, 1443, 1444, 1515, 1516, 1517, 1518, 1519, 1520, 1521, 1523, 1524, 1525, 1526, 1527, 1528, 1529, 1477, 1478, 1479, 1480, 1490, 1481, 1482, 1483, 1484, 1485, 1551, 1552, 1553, 1554, 1555, 1556, 1557, 1558, 1508, 1509, 1510, 1512, 1513, 1559, 1560, 1561, 1562, 1563, 1564, 1486, 1487, 1488, 1489, 1550, 1492, 1493, 1494, 1495, 1738, 1739, 1168, 1169, 1170, 1171, 1172, 1175, 1176, 1177, 1178, 1179, 1162, 1163, 1164, 1165, 1249, 1250, 1251, 1252, 1253, 1254, 1255, 1257, 1258, 1259, 1260, 1261, 1262, 1220, 1203, 1204, 1205, 1206, 1207, 1208, 1209, 1210, 1211, 1212, 1213, 1214, 1215, 1216, 1217, 1218, 1219, 1224, 1225, 1227, 1228, 1434, 1438, 1440, 1267, 1288, 1289, 1290, 1291, 1292, 1293, 1301, 1302, 1303, 1304, 1264, 1266, 1461, 1462, 1088, 1089, 1090, 1091, 1092, 1093, 1095, 1096, 1097, 1098, 1099, 1101, 1081, 1082, 1083, 1084, 1086, 1130, 1131, 1132, 1133, 1134, 1135, 1136, 1139, 1140, 1141, 1142, 1143, 1144, 1138, 1112, 1113, 1114, 1115, 1116, 1117, 1118, 1119, 1146, 1147, 1148, 1149, 1150, 1151, 1152, 1153, 1120, 1121, 1123, 1124, 1181, 1184, 1185, 1186, 1180, 1155, 1156, 1157, 1158, 1159, 1160, 1161, 1126, 1127, 1128, 1129, 1154, 1187, 1188, 880, 972, 973, 974, 975, 978, 979, 980, 981, 982, 983, 998, 985, 986, 987, 988, 989, 999, 1000, 1025, 1026, 1027, 1028, 1029, 1030, 1038, 1031, 1032, 1033, 1034, 1035, 1036, 1037, 1087, 1062, 1063, 1064, 1065, 1051, 1052, 1053, 1054, 1055, 1056, 1017, 1042, 1008, 1009, 1010, 1011, 1012, 1013, 1014, 1015, 1044, 1045, 1046, 1048, 1049, 1050, 1020, 1021, 1023, 1024, 1110, 1111, 1061, 858, 868, 827, 828, 829, 884, 885, 886, 887, 888, 889, 890, 891, 892, 893, 894, 895, 896, 897, 939, 940, 941, 942, 871, 872, 873, 874, 875, 876, 877, 945, 1004, 831, 832, 833, 834, 837, 838, 839, 840, 932, 933, 934, 936, 937, 938, 902, 903, 905, 906, 943, 778, 779, 780, 781, 782, 783, 784, 785, 786, 787, 788, 789, 790, 791, 793, 813, 814, 815, 816, 817, 819, 820, 821, 822, 823, 863, 808, 809, 810, 811, 771, 777, 772, 773, 774, 775, 776, 742, 743, 744, 745, 747, 748, 749, 750, 865, 801, 802, 803, 805, 806, 807, 794, 795, 796, 797, 798, 799, 825, 638, 639, 640, 641, 642, 643, 645, 646, 647, 648, 649, 690, 691, 692, 693, 694, 695, 696, 697, 698, 699, 700, 701, 702, 703, 705, 770, 731, 732, 733, 734, 735, 737, 738, 739, 740, 726, 727, 728, 729, 668, 669, 670, 671, 672, 673, 767, 651, 652, 653, 654, 657, 658, 659, 660, 718, 719, 720, 723, 724, 725, 712, 713, 714, 715, 716, 717, 575, 576, 577, 578, 579, 581, 582, 583, 584, 604, 605, 606, 607, 608, 609, 610, 611, 612, 613, 614, 615, 616, 617, 619, 626, 627, 628, 629, 586, 587, 588, 589, 590, 591, 593, 594, 595, 596, 599, 600, 601, 602, 630, 631, 632, 635, 636, 620, 621, 622, 623, 624, 625, 510, 511, 512, 513, 514, 515, 516, 517, 518, 519, 520, 521, 522, 523, 525, 562, 563, 564, 565, 492, 493, 494, 495, 496, 497, 499, 500, 501, 502, 505, 506, 507, 508, 566, 567, 568, 569, 571, 572, 573, 526, 527, 528, 529, 560, 561, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 461, 482, 483, 484, 485, 487, 488, 489, 490, 491, 468, 469, 470, 471, 428, 429, 430, 431, 432, 433, 435, 436, 437, 438, 441, 442, 443, 444, 472, 473, 474, 475, 477, 478, 479, 462, 463, 465, 466, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 417, 418, 419, 420, 421, 423, 424, 425, 426, 427, 404, 405, 406, 407, 360, 361, 362, 363, 364, 367, 368, 369, 370, 373, 374, 375, 376, 411, 412, 413, 415, 408, 409, 410, 395, 396, 397, 400, 401, 317, 318, 319, 320, 321, 322, 323, 324, 325, 326, 327, 328, 329, 330, 350, 351, 352, 353, 355, 356, 357, 343, 344, 345, 346, 299, 300, 301, 302, 303, 306, 307, 308, 309, 311, 312, 313, 314, 315, 334, 335, 336, 339, 340, 247, 248, 249, 250, 251, 252, 253, 254, 255, 256, 257, 258, 259, 260, 262, 278, 279, 280, 281, 282, 284, 285, 286, 287, 288, 273, 274, 275, 276, 217, 218, 219, 220, 221, 224, 225, 226, 227, 230, 231, 232, 233, 264, 265, 266, 269, 270, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 235, 236, 237, 238, 239, 240, 242, 243, 244, 245, 246, 211, 212, 213, 214, 174, 170, 171, 172, 173, 159, 160, 161, 162, 165, 166, 167, 168, 200, 201, 202, 208, 209, 210, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 139, 140, 124, 120, 121, 122, 123, 125, 110, 111, 112, 113, 114, 115, 116, 117, 118, 144, 145, 146, 152, 153, 154, 155, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 67, 63, 64, 65, 66, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 95, 96, 97, 103, 104, 105, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 21, 22, 23, 24, 25, 13, 14, 15, 16, 17, 18, 19, 20, 49, 50, 51, 56, 57, 58, 59, 26, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
# league_id_list.sort()
# len(league_id_list)