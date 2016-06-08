from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

# m = Basemap(projection='robin', lat_0=0, lon_0=-100,
#               resolution='l', area_thresh=1000.0)
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

coords = [(35.69, 139.69),(-34.6033, -58.3817), (-26.2044, 28.0456)]

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
