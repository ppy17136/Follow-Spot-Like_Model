import pandas as pd
import numpy as np
import itertools
from scipy.optimize import leastsq
from scipy import interpolate 
from scipy.interpolate import RegularGridInterpolator
import random
import math
import sympy as sp
import pylab as pl
import matplotlib as mpl 
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import matplotlib.cm as cm 
from mpl_toolkits.mplot3d import Axes3D

aa=6.9932932
bb=4.0375797
cc=4.9450051/2   
my_file=open(r"./tongjife2.txt","r") 
Xi=np.linspace(0,aa,49)             
Yi=np.linspace(0,bb,49)            
Xii,Yii=np.meshgrid(Xi,Yi)         
Zii=np.loadtxt(my_file)            
my_file.close()                  
Zii=Zii
mm=49  
nn=49  
zdh=np.zeros(mm)    
zd=np.zeros(mm)     
zdg=np.zeros(mm)     

data = """
11	17	18	5	1	4	7	16	13	16	7	4	1	5	18	17	11	17	18	5	1	4	7	16	13	16	7	4	1	5	18	17	11	17	18	5	1	4	7	16	13	16	7	4	1	5	18	17	11
"""
data = data.replace("\n", " ").strip() 
result = list(map(int, data.split())) 
yh=result 
yg=np.zeros(mm)      
zg=np.zeros(mm)      
zgg=np.zeros(mm) 
i=0
pi=3.1415926
for j in yh:
   yg[i]=Yii[j,i]   
   zg[i]=Zii[j,i]    
   i=i+1
for deta in np.arange(0,1):
    for i in np.arange(0,mm,1):
       if i==48:
         dd0=np.sqrt((Xii[1,1]-Xii[1,0])**2+(yg[1]-yg[0])**2)
         theta0=np.abs(np.arctan((yg[1]-yg[0])/(Xii[1,1]-Xii[1,0])))
         zd[i]=(zg[1]-zg[0])/(cc*2*cc*dd0)/(np.cos(theta0))
       else:
         dd=np.sqrt((Xii[1,i+1]-Xii[1,i])**2+(yg[i+1]-yg[i])**2)
         theta=np.abs(np.arctan((yg[i+1]-yg[i])/(Xii[1, i+1] - Xii[1, i])))
         zd[i]=(zg[i+1]-zg[i])/(cc*2*cc*dd)/(np.cos(theta))
    zdg=zd[:]*1.6021892*10**(-19)/((10**(-10))**3)/10**9 
    print (max(zdg)) 
Xii1=Xii[1,:]  
Zii1=zg[:]     
Zii2=zdg[:]    
xnew=np.linspace(0,aa,501) 
f1=interpolate.interp1d(Xii1,Zii1,kind="quadratic") 
f2=interpolate.interp1d(Xii1,Zii2,kind="quadratic") 
f3=interpolate.interp1d(Xii1,yg,kind="linear")      
ynew1=f1(xnew)   
ynew2=f2(xnew)    
ynew3=f3(xnew)  

fig1 = plt.figure() 
ax1 = fig1.add_subplot(111)
ax1.set_ylabel('ΔE(eV)')           
ax1.set_xlabel('x(Å)')
plt.plot(Xii1,Zii1,"o")
pl.plot(xnew, ynew1,'r-',label="Peierls potential")
plt.legend(loc=2)          
plt.ylim(3.74,3.81)  
"""
ax2 = ax1.twinx()
pl.plot(xnew, ynew2,'b--',label="Applied stress")
#ax2.set_yticks(np.arange(min(Zd),max(Zd),0.0001))  
ax2.set_ylabel('τ(GPa)')      
ax2.set_xlabel('x(Å)')              
plt.legend(loc=1)            
"""
plt.savefig('zongneng+yinglixian.tif', dpi=400, bbox_inches='tight')  
plt.show()                              

Zii=Zii/cc
xnew4 = np.linspace(0,aa,201)#x 
ynew4 = np.linspace(0,bb,201)#y 
xnew5, ynew5 = np.meshgrid(xnew4, ynew4) 
interpolating_function = RegularGridInterpolator((Xi, Yi), Zii, method='cubic')
points_to_interpolate = np.array([xnew5.ravel(), ynew5.ravel()]).T 
fnew = interpolating_function(points_to_interpolate).reshape(201, 201).T
xnew5, ynew5 = np.meshgrid(xnew4, ynew4)
fig4 = plt.figure()
ax4 = fig4.add_subplot(111, projection='3d', proj_type='ortho')
ax4.view_init(elev=35, azim=-60)
surf2 = ax4.plot_surface(xnew5, ynew5, fnew, rstride=1, cstride=1, cmap='jet', antialiased=True)
ax4.set_xlabel('x(Å)')
ax4.set_ylabel('z(Å)')
ax4.set_zlabel('ΔE(eV)')
plt.plot((0,0,0), (0,0,0), (2,2,2))
plt.colorbar(surf2, shrink=0.5, aspect=20,pad=0.1)
plt.xlim(0, aa)
plt.ylim(0 - (aa - bb) / 2, bb + (aa - bb) / 2)
plt.savefig('sanwei.tif', dpi=400, bbox_inches='tight')
plt.show()
fig41 = plt.figure() 
ax41 = fig41.add_subplot(111,projection = '3d',proj_type='ortho')
ax41.view_init(elev=90,azim=-90)
surf3 = ax41.plot_surface(xnew5, ynew5, fnew, rstride=1, cstride=1, cmap=cm.jet, antialiased=True) 
ax41.set_xlabel('x(Å)') 
ax41.set_ylabel('z(Å)') 
cc2=plt.colorbar(surf3, shrink=0.5, aspect=20)
ax41 = plt.gca()  
cc3=cc2.ax
cc3.set_title('eV',fontsize=10)
plt.xlim(0,aa)  
plt.ylim(0-(aa-bb)/2,bb+(aa-bb)/2) 
plt.savefig('sanweifushi.tif', dpi=400, bbox_inches='tight')  
plt.show()
fig5 = plt.figure() 
ax5 = fig5.add_subplot(111)
plt.axis('equal') 
plt.plot(xnew, ynew3,label="Glide trajectory",color='k',linewidth=3)
ax5.set_xlabel('x(Å)')                
ax5.set_ylabel('z(Å)')              
plt.legend(loc=2)         
C = plt.contour(xnew5, ynew5, fnew, 8,cmap=cm.jet)
cc=plt.colorbar(C, shrink=0.5, aspect=20)
cc1=cc.ax
cc1.set_title('eV',fontsize=10)
plt.legend(loc=2)             
plt.savefig('guijixian+denggaoxian.tif', dpi=400, bbox_inches='tight') 
plt.show()                              
xnew4 = np.linspace(aa/4,aa*3/4,200)
ynew4 = np.linspace(0,bb/3,200)
interpolating_function = RegularGridInterpolator((Xi, Yi), Zii, method='cubic')
xnew5, ynew5 = np.meshgrid(xnew4, ynew4) 
fnew = interpolating_function(points_to_interpolate).reshape(200, 200).T
fig4 = plt.figure() 
ax4 = fig4.add_subplot(111,projection = '3d',proj_type='ortho')
plt.axis('equal') 
surf2 = ax4.plot_surface(xnew5, ynew5, fnew, rstride=1, cstride=1, cmap=cm.jet, antialiased=True) 
ax4.set_xlabel('x(Å)') 
ax4.set_ylabel('z(Å)') 
ax4.set_zlabel('ΔE(eV)') 
cc=plt.colorbar(surf2, shrink=0.5, aspect=20, pad=0.1)
cc1=cc.ax
cc1.set_title('eV',fontsize=10)
plt.savefig('sanweijubu.tif', dpi=400, bbox_inches='tight')
plt.show()                              


