#!/usr/bin/env python

import math
import numpy as np
import turtle

# GM1 is for the Sun
GM1 = 4*(math.pi**2)
m_sun = 1.989e30

# GM2 is for the new star
GM2 = 4*(math.pi**2)

# planet masses (kg)
m_merc = 3.285e23
m_venus = 4.867e24
m_earth = 5.972e24
m_mars = 6.39e23
m_jup = 1.898e27
m_sat = 5.683e26
m_ur = 8.681e25
m_nep = 1.024e26
m_planets = [m_merc, m_venus, m_earth, m_mars, m_jup, m_sat, m_ur, m_nep]

# planet GM's
gm_planets = []
for i in range(len(m_planets)):
    gm_planets.append(GM1 * m_planets[i] / m_sun)

# star eccentricities
#ecc_1 = 0.1                         # eccentricty of suns new orbit (approx fixed before)
#ecc_2 = (GM1/GM2)**2*(1+ecc_1)-1    # eccentricity of new star

# Sun's perihelion (and new star's perihelion)
perihelion_star = 1

# planet perhelions
AU = 149597870.7 # (1 Astronomical Unit in km)

#a1 = perihelion_star/(1-ecc_1)
#a2 = perihelion_star/(1-ecc_2)

def rad_from_RA(hr,m,sec):
    mins = m + sec/60.0
    hrs = hr + mins/60.0
    return hrs*2*math.pi/24.0

#vp_star = math.sqrt(GMs) * math.sqrt((1+ecc_star) / (a*(1-ecc_star)) * (1+(m_1/m_2)))
#vp_1 = math.sqrt(GM1+GM2) * math.sqrt((1+ecc_1) / (a1*(1-ecc_1)))
#vp_2 = math.sqrt(GM1+GM2) * math.sqrt((1+ecc_2) / (a2*(1-ecc_2)))

# initial velocity and position of the sun
vx1 = 0
vy1 = 0
x1 = 0
y1 = 0
thetaa = rad_from_RA(0,42,44) # angle of approach of the Andromeda galaxy
#va = -120/AU*60*60*24*365.25 # average velocity of Andromeda galaxy relative to earth, about -120 km/s (- means approaching)
va = -1 # initial velocity of new star
da = 5 # initial distance of new star
vx2 = va*math.cos(thetaa)
vy2 = va*math.sin(thetaa)
x2 = da*math.cos(thetaa+math.pi/2)
y2 = da*math.sin(thetaa+math.pi/2)

# planet starting positions (km, April 29, 2021)
xy_merc = [-3.1633e6, 4.6046e7]
xy_venus = [5.3028e7,9.4033e7]
xy_earth = [-1.1661e8,-9.5415e7]
xy_mars = [-1.3485e8, 2.04653e8]
xy_jup = [5.53229e8, -5.159579e8]
xy_sat = [8.96914e8, -1.19106e9]
xy_urn = [2.25127e9, 1.91478e9]
xy_nep = [4.41637e9, -7.27284e8]
xy_km = [xy_merc, xy_venus, xy_earth, xy_mars, xy_jup, xy_sat, xy_urn, xy_nep]
xyps = [[i[0]/AU,i[1]/AU] for i in xy_km] # convert to AU

#planet starting velocities (km/s, April 29, 2021)
v_merc = [-5.8371e1,-1.5691]
v_venus = [-3.0617e1,1.7045e1]
v_earth = [1.8367e1,-2.3162e1]
v_mars=[-1.93183e1, -1.12703e1]
v_jup=[8.76363, 1.01805e1]
v_sat=[7.18766, 5.79719]
v_urn=[-4.45428, 4.88007]
v_nep=[8.5687e-1, 5.40798]
vpskmps = [v_merc, v_venus, v_earth, v_mars, v_jup, v_sat, v_urn, v_nep]
AUpY = 3600*24*365.25/AU # multiply by AUpY to convert km/s to AU/year
vps = [[i[0]*AUpY,i[1]*AUpY] for i in vpskmps] # convert to AU/year

# years
h = 0.001
t_final = 10
t_initial = 0
t = t_initial
count = 0

xarr1 = np.array([x1])
yarr1 = np.array([y1])
xarr2 = np.array([x2])
yarr2 = np.array([y2])
tarr = np.array([t])

# initialize planet coordinate arrays
planet_coordinates = []
for i in range(len(xyps)):
    planet_coordinates.append( [ np.array([xyps[i][0]]), np.array([xyps[i][1]]) ] )

# planetid -> 0 (merc), 1 (venus),...

def dist(p1, p2):
    return math.sqrt( ( p1[0] - p2[0] )**2 + ( p1[1] - p2[1] )**2 )

def accelx(gm1, xy1, xy2, r):
    return (gm1 * (xy1[0] - xy2[0]) / r**3)

def accely(gm1, xy1, xy2, r):
    return (gm1 * (xy1[1] - xy2[1]) / r**3)

def ax(pid, xy1, xy2, xyps):
    r1 = dist(xyps[pid],xy1)
    a1 = accelx(GM1, xy1, xyps[pid], r1)
    r2 = dist(xyps[pid],xy2)
    a2 = accelx(GM2, xy2, xyps[pid], r2)
    ax_total = a1 + a2
    plist = list(range(len(xyps)))
    plist.remove(pid)
    for i in plist:
        r = dist(xyps[pid],xyps[i])
        ax_total += accelx(gm_planets[i], xyps[i], xyps[pid], r)
    return ax_total

def ay(pid, xy1, xy2, xyps):
    r1 = dist(xyps[pid],xy1)
    a1 = accely(GM1, xy1, xyps[pid], r1)
    r2 = dist(xyps[pid],xy2)
    a2 = accely(GM2, xy2, xyps[pid], r2)
    ay_total = a1 + a2
    plist = list(range(len(xyps)))
    plist.remove(pid)
    for i in plist:
        r = dist(xyps[pid],xyps[i])
        ay_total += accely(gm_planets[i], xyps[i], xyps[pid], r)
    return ay_total

def ax1(x1,y1,x2,y2):
    r=math.sqrt((x2-x1)**2+(y2-y1)**2)
    return(GM2*(x2-x1)/(r**3))

def ay1(x1,y1,x2,y2):
    r=math.sqrt((x2-x1)**2+(y2-y1)**2)
    return(GM2*(y2-y1)/(r**3))

def ax2(x1,y1,x2,y2):
    r=math.sqrt((x2-x1)**2+(y2-y1)**2)
    return(GM1*(x1-x2)/(r**3))

def ay2(x1,y1,x2,y2):
    r=math.sqrt((x2-x1)**2+(y2-y1)**2)
    return(GM1*(y1-y2)/(r**3))

aps = []
apsn = []
for i in range(len(xyps)):
    aps.append([0,0])
    apsn.append([0,0])

while (t < t_final):
      
      #verlet method of gravitational force
      ax01=ax1(x1,y1,x2,y2)
      ay01=ay1(x1,y1,x2,y2)
      ax02=ax2(x1,y1,x2,y2)
      ay02=ay2(x1,y1,x2,y2)

      # calculate current accelerations of planets
      for i in range(len(xyps)):
          aps[i] = [ax(i,[x1,y1],[x2,y2],xyps), ay(i,[x1,y1],[x2,y2],xyps)]

      x1=x1+vx1*h+(1/2)*ax01*(h**2)
      y1=y1+vy1*h+(1/2)*ay01*(h**2)
      x2=x2+vx2*h+(1/2)*ax02*(h**2)
      y2=y2+vy2*h+(1/2)*ay02*(h**2)

      # calculate next positions of planets
      for i in range(len(xyps)):
          xyps[i] = [xyps[i][0] + vps[i][0]*h + .5*aps[i][0]*h**2, xyps[i][1] + vps[i][1]*h + .5*aps[i][1]*h**2]
      
      axn1=ax1(x1,y1,x2,y2)
      ayn1=ay1(x1,y1,x2,y2)
      axn2=ax2(x1,y1,x2,y2)
      ayn2=ay2(x1,y1,x2,y2)

      # calculate next accelerations of planets
      for i in range(len(xyps)):
          apsn[i] = [ax(i,[x1,y1],[x2,y2],xyps), ay(i,[x1,y1],[x2,y2],xyps)]
      
      vx1=vx1+(h/2)*(ax01+axn1)
      vy1=vy1+(h/2)*(ay01+ayn1)
      vx2=vx2+(h/2)*(ax02+axn2)
      vy2=vy2+(h/2)*(ay02+ayn2)

      # update velocities of planets
      for i in range(len(xyps)):
          vps[i] = [vps[i][0] + h/2*(aps[i][0] + apsn[i][0]), vps[i][1] + h/2*(aps[i][1] + apsn[i][1])]
      
      #if (count%200 == 0 ):                                                                                                         
      xarr1 = np.append(xarr1,x1)
      yarr1 = np.append(yarr1,y1)
      xarr2 = np.append(xarr2,x2)
      yarr2 = np.append(yarr2,y2)
      for i in range(len(xyps)):
          planet_coordinates[i][0] = np.append(planet_coordinates[i][0], xyps[i][0])
          planet_coordinates[i][1] = np.append(planet_coordinates[i][1], xyps[i][1])
      count = count + 1
  
      t = t + h
      tarr = np.append(tarr,t)

#turtle
world_radius = 30
turtle.setup(width=1000,height=1000)
sc = turtle.Screen()
sc.setworldcoordinates(-world_radius,-world_radius,world_radius,world_radius)
sc.bgcolor("black")
sc.title("New Solar System")

# star turtles
t1 = turtle.Turtle()
t2 = turtle.Turtle()
t1.color("White")
t2.color("White")
t1.pensize(1)
t2.pensize(2)
t1.shape("circle")
t2.shape("circle")
t1.shapesize(0.6,0.6)

# pick planet colors
c_planets = ["Gray","Yellow","Green","Red","Orange","Yellow","Blue","Blue"]

t_planets = []
for i in range(len(c_planets)):
    t_planets.append(turtle.Turtle())

# planet images
i_planets = ["mercury.gif","venus.gif","earth.gif","mars.gif","jupiter.gif","saturn.gif","uranus.gif","neptune.gif"]

for i in range(len(c_planets)):
    t_planets[i].color(c_planets[i])
    t_planets[i].pensize(1)
    t_planets[i].speed("fastest")
    sc.addshape(i_planets[i])
    t_planets[i].shape(i_planets[i])

# all turtles up
t1.up()
t2.up()
for i in range(len(t_planets)):
    t_planets[i].up()

# get the stars and planets to their initial positions
t1.goto(xarr1[0],yarr1[0])
t2.goto(xarr2[0],yarr2[0])
for j in range(len(c_planets)):
    t_planets[j].goto(planet_coordinates[j][0][0],planet_coordinates[j][1][0])

# all turtles down
t1.down()
t2.down()
for i in range(len(t_planets)):
    t_planets[i].down()

# get slimmed down position arrays
speed = 20
x1arr = xarr1[2::speed]
y1arr = yarr1[2::speed]
x2arr = xarr2[2::speed]
y2arr = yarr2[2::speed]
pcoord = np.array(planet_coordinates)[:,:,2::speed]

# turtle animation loop
for i in range(len(pcoord[0][0])):
    t1.goto(x1arr[i],y1arr[i])
    t2.goto(x2arr[i],y2arr[i])
    for j in range(len(c_planets)):
        t_planets[j].goto(pcoord[j][0][i],pcoord[j][1][i])
turtle.done()
