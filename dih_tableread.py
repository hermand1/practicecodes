# Name: dih_tableread.py
#
#
#
#
#
#
#
#
#
import sys
import numpy as np
import matplotlib
matplotlib.use('ps')
import matplotlib.pyplot as plt 
import pylab
import glob
import matplotlib.cm as cm
from scipy import signal
import dih_errmaker as d

#helper fct grabs columns of data from ascii files and returns x and y columns
def dih_filegrab(filename):
    grabbedcol = np.genfromtxt(filename, skip_header=1,skip_footer=1)
    columns = [list(row) for row in grabbedcol]
    return columns
#helper fct same as filegrab but with no skipping header
#
#Name: dih_filegrab2
#
#Purpose:taking human readable data and turning it into lists
#
#Inputs: file containing columns of data
#
#Outputs: columns -> (list of coordinates) can be unzipped to give columns
#
#Example: columns = zip(*dih_filegrab2('data.txt'))
#
#Written:7/31/14 Dan Herman daniel.herman@cfa.harvard.edu
#
#

def dih_filegrab2(filename):
    grabbedcol = np.genfromtxt(filename,skip_header=1)
    columns = [list(row) for row in grabbedcol]
    return columns

#helper fct removes files from directory and grabs columns of data
def dih_tablereader(dirname):
    filelist = glob.glob(dirname+"/*.data")
    openlist = []
    for filename in filelist:
        filecontent = dih_filegrab(filename)
        openlist.append(filecontent)
    print filelist
    return openlist
#Name:dih_plotter
#
#Purpose:plots the first number = (numplot) files in directory = (dirname) filled with 
#ascii files and places marker on peak data point for each plot saves plot as savename
#
#Inputs:dirname-- directory name, savename-- plot file saved as postscript with this name,
# numplot-- number of files from directory to be plotted
#
#
#Outputs:postscript plot file with markers on peaks, returns array of x and y columns 
#contained in the plot
#
#Example: f = dih_plotter("../datafolder","thisplot",8)
#
#Written:6/19/14 Daniel Herman, daniel.herman@cfa.harvard.edu
#
#
#Purpose:plots the first number = (numplot) files in directory = (dirname) filled with ascii files and places marker on peak data point for each plot saves plot as savename
#
#Inputs:dirname-- directory name, savename-- plot file saved as postscript with this name, numplot-- number of files from directory to be plotted
#
def dih_plotter(dirname,savename,numplot):
    inlist = dih_tablereader(dirname)
    plotlist = inlist[0:numplot]
    colors = iter(cm.rainbow(np.linspace(0,1,len(plotlist)))) #creates color table
    errlist = d.dih_errmaker(dirname)
    print errlist
    for idx,memberlist in enumerate(plotlist):
        x = memberlist[0] #x coordinate data
        y = memberlist[1] #y coordinate data
        peaklist =signal.find_peaks_cwt(y, np.arange(1,30))
        plt.plot(x,y,color = next(colors))
        for num in peaklist:
            plt.plot(x[num],y[num],'gD')#places markers on peaks
            plt.errorbar(x[num],y[num],xerr=errlist[idx],yerr=0.15,ecolor = 'b')
#finish up plot characteristics

    plt.title('Super Most Awesome Graph!')
    plt.ylabel('Flux')
    plt.xlabel('Time')       
    pylab.ylim([-5,5])
    pylab.xlim([0,6.3])
    plt.savefig(savename)#saves postscript file
    return plotlist


    
    
    



#parsing code

if __name__ == "__main__": 
    
    if len(sys.argv) != 4:
        print("You suck!")
        sys.exit(1)
    
    dih_plotter(sys.argv[1], sys.argv[2],sys.argv[3])