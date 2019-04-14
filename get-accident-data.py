import requests
import overpass
import mysql.connector as mysql
import time

db = mysql.connect(
    host="localhost",
    user="user",
    password="password",
    database="traffic"
)

drop_table = (
  "DROP TABLE IF EXISTS `collisions`"
)

create_table = (
    "CREATE TABLE `collisions` ("
    "  `id` int(11) NOT NULL AUTO_INCREMENT,"
    "  `latitude` varchar(20) NOT NULL,"
    "  `longitude` varchar(20) NOT NULL,"
    "  `impact_type` varchar(100) NOT NULL,"
    "  `date` varchar(20) NOT NULL,"
    "  PRIMARY KEY (`id`))")

insert_point = (
  "INSERT INTO `collisions`"
  "(latitude, longitude, impact_type, date)"
  "VALUES (%s, %s, %s, %s)"
)

def main():
  cursor = db.cursor()
  cursor.execute(drop_table)
  cursor.execute(create_table)
  URL = "https://services.arcgis.com/S9th0jAJ7bqgIRjw/arcgis/rest/services/Fatal_Collisions/FeatureServer/0/query?where=1%3D1&outFields=*&outSR=4326&f=json"
  res = requests.get(URL)
  data = res.json()
  features = data["features"]
  for feature in features:
    point = feature["attributes"]
    epoch = point["DATE"] / 1000
    date = time.strftime('%Y-%m-%d', time.localtime(epoch))
    point_data = (point["LATITUDE"], point["LONGITUDE"], point["IMPACTYPE"], date)
    cursor.execute(insert_point, point_data)
    db.commit()
  # lat, long = point["LATITUDE"], point["LONGITUDE"]
  # op = overpass.API()
  # query = "node(around:{:f},{:f},10)".format(lat, long)
  # print(query)
  # res = op.get(query)
  # print`(res)

if __name__ == '__main__':
    main()
