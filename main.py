import tornado.ioloop
import tornado.web

from astropy.time import Time
from astropy.coordinates import solar_system_ephemeris, EarthLocation
from astropy.coordinates import get_body_barycentric, get_body, get_moon
from astropy.timeseries import TimeSeries
from astropy import units as u

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
from math import sin, cos, radians
from random import randint

planets = ['sun',
 'mercury',
 'venus',
 'earth',
 'moon',
 'mars',
 'jupiter',
 'saturn',
 'uranus',
 'neptune']
 # 'pluto'

planets1 = ['sun',
            'mercury',
            'venus',
            'earth',
            'mars']

sizes = [100, 15, 37, 40, 22]

clrs = ['#%06X' % randint(0, 0xFFFFFF) for i in range(len(planets1))]



def get_coordinates(t):
    with solar_system_ephemeris.set('builtin'):
        coords = [get_body(i, t) for i in planets1]
        x = [i.heliocentrictrueecliptic.lon.deg for i in coords]
        y = [i.heliocentrictrueecliptic.lat.deg for i in coords]
        z = [i.heliocentrictrueecliptic.distance.value for i in coords]

        dx = [i.heliocentrictrueecliptic.distance.value * sin(radians(i.heliocentrictrueecliptic.lon.deg)) * cos(radians(i.heliocentrictrueecliptic.lat.deg)) for i in coords]
        dy = [i.heliocentrictrueecliptic.distance.value * sin(radians(i.heliocentrictrueecliptic.lon.deg)) * sin(radians(i.heliocentrictrueecliptic.lat.deg)) for i in coords]
        dz = [i.heliocentrictrueecliptic.distance.value * cos(radians(i.heliocentrictrueecliptic.lon.deg)) for i in coords]
    return (dx,dy,dz)



class MainHandler(tornado.web.RequestHandler):
    def get(self):
        t = Time.now()

        fig = plt.figure()
        ax = plt.axes(projection='3d')


        dx,dy,dz = get_coordinates(t)
        ax.scatter(dx, dy, dz, marker='o', sizes = sizes, c = clrs)

        for i, txt in enumerate(planets1):
            ax.text(dx[i], dy[i], dz[i], txt)


        for i in range(10):
            print(t)
            t -= 10
            x,y,z = get_coordinates(t)
            ss = [s * (0.5 - 0.02 * i) for s in sizes]
            ax.scatter(x, y, z, marker='o', sizes = ss, c = clrs)

        
        print(t)
        plt.show()

        self.write("Hello, world")

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
