import requests
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import sys
import traceroute as tr

def get_lat_lon(ip_list=[], lats=[], lons=[]):
  print("Processing {} IPs...".format(len(ip_list)))
  for ip in ip_list:
    r = requests.get("https://freegeoip.net/json/" + ip)
    json_response = r.json()
    print("{ip}, {region_name}, {country_name}, {latitude}, {longitude}".format(**json_response))
    if json_response['latitude'] and json_response['longitude']:
      lats.append(json_response['latitude'])
      lons.append(json_response['longitude'])
  return lats, lons

def geolocate(ip_list=[]):
  ip = []
  lat = []
  lon = []
  for v in range(0, len(ip_list)):
    ip.append(ip_list[v][0])

  get_lat_lon(ip, lat, lon)

  res = []
  for v in range(0, len(lat)):
    res.append( (lat[v], lon[v]) )

  return res

def plot(coords=[]):
  m = Basemap(projection='merc',llcrnrlat=-60,urcrnrlat=80,\
            llcrnrlon=-180,urcrnrlon=180,lat_ts=20,resolution='c')

  m.fillcontinents()
  m.drawcoastlines()
  m.drawparallels(range(0, 90, 20))
  m.drawmeridians(range(0, 180, 20))

  def gps_to_point(coord):
    x, y = m(coord[1], coord[0])
    return (x,y)

  def plot_point(point):
    m.plot(point[0], point[1], 'ro')
    return

  # Transforms GPS coordinates to X,Y to be places on map
  points = map(gps_to_point, coords)
  # Adds points to map
  map(plot_point, points)

  # Separated X form Y in different arrays and plots lines
  x = [ point[0] for point in points ]
  y = [ point[1] for point in points ]
  m.plot(x,y,linewidth=2,color='r')

  plt.title("Ruta realizada")
  plt.show()


if __name__ == '__main__':
  host_destino = sys.argv[1]
  ip_list = tr.TraceRoute(host_destino)
  lat_longs = geolocate(ip_list)
  plot(lat_longs)
