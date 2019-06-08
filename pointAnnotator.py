# -*- coding: utf-8 -*-
"""
Created on Fri Jun 07 16:34:30 2019

@author: svc_ccg
"""

import numpy as np
from matplotlib import pyplot as plt

#class to handle annotating the images with points of interest
#USE: left mouse clicks will draw red dots on image and populate a list of x y coordinates for each dot
#     right mouse clicks will clear the dots and the x y coordinate list
#     key presses will delete only the last point
class pointAnnotator:
    def __init__(self, im, ax):
        self.ax = ax
        self.ax.set_xlim([0,im.get_array().shape[1]])
        self.ax.set_ylim([im.get_array().shape[0],0])
        
        self.im = im
        self.xs = []
        self.ys = []
        self.annos = []
        self.labels = []
        self.cid = im.figure.canvas.mpl_connect('button_press_event', self.onclick)
        self.cidrelease = im.figure.canvas.mpl_connect('button_release_event', self.onrelease)
        
        self.kid = im.figure.canvas.mpl_connect('key_press_event', self.keypress)

    def onclick(self, event):
        if event.inaxes==self.ax:
            if event.button == 1:
                print('x ' + str(event.xdata) + '\ty ' + str(event.ydata))
                self.xs.append(event.xdata)
                self.ys.append(event.ydata)

                anno, = self.ax.plot(event.xdata, event.ydata, 'ro')
                self.annos.append(anno)
                lab = self.ax.text(event.xdata+0.2, event.ydata+0.2, str(len(self.annos)))
                self.labels.append(lab)
                self.im.figure.canvas.draw()  
            else:
                self.resetAnnotations()
    def onrelease(self, event):
        #check to see if this was a click and drag, in which case, don't draw point
        if event.inaxes==self.ax:
            distance = ((event.xdata-self.xs[-1])**2 + (event.ydata-self.ys[-1])**2)**0.5
            if distance > 10:
                self.deleteLastAnnotation()
    def keypress(self, event):
        if event.inaxes==self.ax:
            self.deleteLastAnnotation()
    
    def resetAnnotations(self):
        self.xs=[]
        self.ys=[]
        for a, l in zip(self.annos, self.labels):
            a.remove()
            l.remove()
        self.im.figure.canvas.draw()
        self.annos=[]
        self.labels=[]
    
    def deleteLastAnnotation(self):
        self.xs = self.xs[:-1]
        self.ys = self.ys[:-1]
        self.annos[-1].remove()
        self.labels[-1].remove()
        self.annos = self.annos[:-1]
        self.labels = self.labels[:-1]
        self.im.figure.canvas.draw()
    
    def loadPoints(self, points):
        self.xs = list(points[:, 0])
        self.ys = list(points[:, 1])
        self.drawPoints()
        
    def drawPoints(self):
        for i, (x,y) in enumerate(zip(self.xs, self.ys)):
            anno, = self.ax.plot(x,y, 'ro')
            self.annos.append(anno)
            lab = self.ax.text(x,y,str(i+1))
            self.labels.append(lab)
            self.im.figure.canvas.draw()
            
class pointCopier(pointAnnotator):
    def __init__(self, im, ax):
        pointAnnotator.__init__(self, im, ax)
        
    def onclick(self, event):
        if event.button == 1:
            print('x ' + str(event.xdata) + '\ty ' + str(event.ydata))
            self.xs.append(event.xdata)
            self.ys.append(event.ydata)

            anno, = self.ax.plot(event.xdata, event.ydata, 'ro')
            self.annos.append(anno)
            lab = self.ax.text(event.xdata+0.2, event.ydata+0.2, str(len(self.annos)))
            self.labels.append(lab)
            self.im.figure.canvas.draw()  
        else:
            self.resetAnnotations()        
    
    def onrelease(self, event):
        #check to see if this was a click and drag, in which case, don't draw point        
        distance = ((event.xdata-self.xs[-1])**2 + (event.ydata-self.ys[-1])**2)**0.5
        if distance > 10:
            self.deleteLastAnnotation()
    
    def keypress(self, event):
        self.deleteLastAnnotation()  
        