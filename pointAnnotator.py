# -*- coding: utf-8 -*-
"""
Created on Fri Jun 07 16:34:30 2019

@author: svc_ccg
"""

import numpy as np
from matplotlib import pyplot as plt
import os
import logging

#class to handle annotating the images with points of interest
#USE: left mouse clicks will draw red dots on image and populate a list of x y coordinates for each dot
#     right mouse clicks will clear the dots and the x y coordinate list
#     key presses will delete only the last point
class pointAnnotator:
    def __init__(self, im, ax):
        self.ax = ax
        self.respond_in_ax = ax
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
        if event.inaxes==self.respond_in_ax:
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
        if event.inaxes==self.respond_in_ax:
            distance = ((event.xdata-self.xs[-1])**2 + (event.ydata-self.ys[-1])**2)**0.5
            if distance > 10:
                self.deleteLastAnnotation()
    def keypress(self, event):
        if event.inaxes==self.respond_in_ax:
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
        try:
            self.xs = list(points[:, 0])
            self.ys = list(points[:, 1])         
            self.drawPoints()
        except TypeError as E:
            if points is None:
                print('No points to load')
            else:
                raise(E)
        
    def drawPoints(self):
        for i, (x,y) in enumerate(zip(self.xs, self.ys)):
            anno, = self.ax.plot(x,y, 'ro')
            self.annos.append(anno)
            lab = self.ax.text(x,y,str(i+1))
            self.labels.append(lab)
            self.im.figure.canvas.draw()
            
    @property
    def points(self):
        return np.stack((self.xs, self.ys)).astype(np.float32).T
            
class pointCopier(pointAnnotator):
    def __init__(self, im, ax, copy_ax):
        pointAnnotator.__init__(self, im, ax)
        self.respond_in_ax = copy_ax
        
    #def onclick(self, event):
    #    if event.inaxes==self.respond_in_ax:
    #        if event.button == 1:
     #           print('x ' + str(event.xdata) + '\ty ' + str(event.ydata))
     #           self.xs.append(event.xdata)
     #           self.ys.append(event.ydata)
#
 #               anno, = self.ax.plot(event.xdata, event.ydata, 'ro')
  #              self.annos.append(anno)
   #             lab = self.ax.text(event.xdata+0.2, event.ydata+0.2, str(len(self.annos)))
    #            self.labels.append(lab)
     #           self.im.figure.canvas.draw()  
      #      else:
       #         self.resetAnnotations()        
    
    #def onrelease(self, event):
    #    #check to see if this was a click and drag, in which case, don't draw point        
    #    distance = ((event.xdata-self.xs[-1])**2 + (event.ydata-self.ys[-1])**2)**0.5
    #    if distance > 10:
    #        self.deleteLastAnnotation()
    
    #def keypress(self, event):
    #    """we only want to delete points when the key press is in the copy image and a point on the other image will be deleted"""
    #    if event.inaxes==self.copy_ax:
    #        self.deleteLastAnnotation()

def points_from_path(path, *args):
    log_str = 'Found more than 1 {} in {}, something might be wrong'
    npz_count = 0
    points = np.stack(([], [])).astype(np.float32).T
    if not(os.path.isdir(path)):
        path = os.path.split(path)[0]
    for filename in os.listdir(path):
        if os.path.splitext(filename)[1]=='.npz':
            npz_count += 1
            match_count = 0
            npz_file = np.load(os.path.join(path, filename))
            for array_name in npz_file.files:
                match = True
                for arg in args:
                    if not(arg in array_name):
                        match = False
                if match:
                    match_count += 1
                    logging.info('Found some points')
                    points = npz_file[array_name]
                    logging.info(points)
            if match_count>1:
                logging.warning(log_str.format('array', filename))
    if npz_count>1:
        logging.warning(log_str.format('npz file', path))
    return points
