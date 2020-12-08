# -*- coding: utf-8 -*-
"""
Created on Fri Jun 07 16:34:30 2019

@author: svc_ccg
"""

import numpy as np
from matplotlib import pyplot as plt
import os
import logging
import time
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
        self.marker_str = 'b+'
        self.last_click = None
        self.cid = im.figure.canvas.mpl_connect('button_press_event', self.onclick)
        self.cidrelease = im.figure.canvas.mpl_connect('button_release_event', self.onrelease)
        
        self.kid = im.figure.canvas.mpl_connect('key_press_event', self.keypress)

    def onclick(self, event):
        self.last_click = event
        print('registered click')
        #if event.inaxes==self.respond_in_ax:
        #    if event.button == 1:

            #Do this on the release instead else:
            #    idx = self.clicked_annotation(event)
            #    if idx:
            #        self.deleteAnnotation(idx)

                    
    def onrelease(self, event):
        #check to see if this was a click and drag, in which case, don't draw point
        if event.inaxes==self.respond_in_ax:
            distance = ((event.xdata-self.last_click.xdata)**2 + (event.ydata-self.last_click.ydata)**2)**0.5
            if event.button == 1:
                idx = self.clicked_annotation(self.last_click)
                if not(idx is None):
                    self.update_annotation(idx, event)
                else:
                    
                    if distance < 10:
                        print('x ' + str(event.xdata) + '\ty ' + str(event.ydata))
                        self.xs.append(event.xdata)
                        self.ys.append(event.ydata)

                        anno, = self.ax.plot(event.xdata, event.ydata, self.marker_str)
                        self.annos.append(anno)
                        lab = self.ax.text(event.xdata+6, event.ydata-4, str(len(self.annos)))
                        self.labels.append(lab)
                        self.im.figure.canvas.draw()  
            else:
                if (distance < 10) and not(self.clicked_annotation(self.last_click) is None):
                    self.deleteAnnotation(self.clicked_annotation(self.last_click))
                if (distance > 30) and self.clicked_annotation(self.last_click)==None and self.clicked_annotation(event)==None:
                    self.resetAnnotations()

    def update_annotation(self, idx, event):
        self.xs[idx] = event.xdata
        self.ys[idx] = event.ydata
        self.annos[idx].remove()
        anno, = self.ax.plot(event.xdata, event.ydata, self.marker_str)
        self.annos[idx] = anno                                                                          
        self.labels[idx].remove()
        lab = self.ax.text(event.xdata+6, event.ydata-4, str(idx+1))
        self.labels[idx] = lab
        self.im.figure.canvas.draw()                                                                                       
                                                                                        
                
    def clicked_annotation(self, event):
        for idx, (x,y) in enumerate(zip(self.xs, self.ys)):
            distance = ((event.xdata-x)**2 + (event.ydata-y)**2)**0.5
            if distance < 30:
                return idx
        return None

                
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
    
    def deleteAnnotation(self, idx):
        self.xs.pop(idx)
        xs = self.xs
        self.ys.pop(idx)
        ys = self.ys
        self.resetAnnotations()
        self.ys = ys
        self.xs = xs
        self.drawPoints()

        
        
    def deleteLastAnnotation(self):
        #self.deleteAnnotation(-1)
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
            time.sleep(.5)
            anno, = self.ax.plot(x,y, self.marker_str)
            self.annos.append(anno)
            lab = self.ax.text(x+6,y-4,str(i+1))
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
            print('found npz '+filename)
            try:
                npz_file = np.load(os.path.join(path, filename), allow_pickle=True)
                stored_points = npz_file#npz_file['imagePairCoordinates'][0]
                print(stored_points)
                for array_name in stored_points:
                    match = True
                    for arg in args:
                        if not(arg in array_name):
                            match = False
                    if match:
                        match_count += 1
                        logging.info('Found some points')
                        points = npz_file[array_name]
                        logging.info(points)
            except Exception as E:
                return points
            if match_count>1:
                logging.warning(log_str.format('array', filename))
    if npz_count>1:
        logging.warning(log_str.format('npz file', path))
    return points
