
from numpy import *
import matplotlib.pyplot as p
from scipy import integrate

#function that defines the emissions trajectory.
def getemissions(time):
        if time > 0 and time < 2012:
                x = 1900
        else:
            #alter emissions here to define different emissions trajectories. Currently 1900 Mg/y
                x = 1900
        return x

#This creates a six box model with the same timescales as Selin (2014).
#Specified constant emissions at 1900 Mg
#All units of k's are in #y-1
#Fluxes in Mg
#Also returns total deposition
def sixboxmercury(state,t):
	emis=getemissions(t)
	atmosphere=state[0]
	organicsoil=state[1]
	mineralsoil=state[2]
	surfaceocean=state[3]
	interocean=state[4]
	deepocean=state[5]
	deposition=state[6]
	geogenic=200
	katmland=0.44
	katmocean=0.73
	koceanatm=0.68
	ksoilatm=0.01
	ksoilsink=0.003
	ksinking=1.12
	kupwelling=0.019
	krivers=0.0019
	kdeepsinking=0.0033
	kdeeptoint=0.0006
	kburial=0.001
	atmd=geogenic+emis-katmland*atmosphere-katmocean*atmosphere+koceanatm*surfaceocean+ksoilatm*organicsoil
	orgsoild=(katmland*atmosphere)-ksoilatm*organicsoil-krivers*organicsoil-ksoilsink*organicsoil
	minsoild=ksoilsink*organicsoil
	surfocd=(katmocean*atmosphere)+krivers*organicsoil+kupwelling*interocean-koceanatm*surfaceocean-ksinking*surfaceocean
	interocd=ksinking*surfaceocean-kdeepsinking*interocean+kdeeptoint*deepocean-kupwelling*interocean
	deepocd=kdeepsinking*interocean-kdeeptoint*deepocean-kburial*deepocean
	ddepo=-deposition+katmland*atmosphere+katmocean*atmosphere
	return [atmd, orgsoild, minsoild, surfocd,interocd,deepocd,ddepo]

#Pull out a yearly timestep beginning in 2012 (can be changed to enable longer scenarios)
t=linspace(2012,2050,39)
#initial conditions (state0) are based on the present day in Selin (2014)
state0=[5000,110000,860000,3800,160000,270000,5800]

#use ode solver to integrate the six box model
constant=integrate.odeint(sixboxmercury, state0,t)
