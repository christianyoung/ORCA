import math, re

import pylab
import matplotlib.pyplot as plt
import networkx as nx

class AnnoteFinder:
  """
  callback for matplotlib to display an annotation when points are clicked on.  The
  point which is closest to the click and within xtol and ytol is identified.
    
  Register this function like this:
    
  scatter(xdata, ydata)
  af = AnnoteFinder(xdata, ydata, annotes)
  connect('button_press_event', af)
  """
  
  def __init__(self, xdata, ydata, annotes, axis=None, xtol=None, ytol=None):
    self.data = zip(xdata, ydata, annotes)
    if xtol is None:
      xtol = ((max(xdata) - min(xdata))/float(len(xdata)))/2
    if ytol is None:
      ytol = ((max(ydata) - min(ydata))/float(len(ydata)))/2
    self.xtol = xtol
    self.ytol = ytol
    if axis is None:
      self.axis = pylab.gca()
    else:
      self.axis= axis
    self.drawnAnnotations = {}
    self.links = []
    self.AnnoteSet = set()

  def distance(self, x1, x2, y1, y2):
    """
    return the distance between two points
    """
    return math.hypot(x1 - x2, y1 - y2)

  def __call__(self, event):
    if event.inaxes:
      clickX = event.xdata
      clickY = event.ydata
      if self.axis is None or self.axis==event.inaxes:
        annotes = []
        for x,y,a in self.data:
          if  clickX-self.xtol < x < clickX+self.xtol and  clickY-self.ytol < y < clickY+self.ytol :
            annotes.append((self.distance(x,clickX,y,clickY),x,y, a) )
        if annotes:
          annotes.sort()
          distance, x, y, annote = annotes[0]
          self.drawAnnote(event.inaxes, x, y, annote, False)
          for l in self.links:
            l.drawSpecificAnnote(annote)

  def drawAnnote(self, axis, x, y, annote, clearFlag):
    """
    Draw the annotation on the plot
    """
    inputs = axis, x, y, annote
    if (x,y) in self.drawnAnnotations:
      markers = self.drawnAnnotations[(x,y)]
      self.drawnAnnotations.pop((x,y))
      for m in markers:
        m.set_visible(not m.get_visible())
      if not clearFlag:
        self.AnnoteSet.remove(inputs)
        self.axis.figure.canvas.draw()
    else:
      #t = axis.text(x,y, "(%3.2f, %3.2f) - %s"%(x,y,annote), )
      t = axis.text(x,y,"  %s"%annote, )
      m = axis.scatter([x],[y], marker='d', c='r', zorder=100)
      self.drawnAnnotations[(x,y)] =(t,m)
      if not clearFlag:
        self.AnnoteSet.add(inputs)
        self.axis.figure.canvas.draw()

  def drawSpecificAnnote(self, annote):
    annotesToDraw = [(x,y,a) for x,y,a in self.data if re.sub(r'\([^)]*\)', '',a).lstrip('+') == annote]
    for x,y,a in annotesToDraw:
      self.drawAnnote(self.axis, x, y, a, False)

  def clear(self):
    for item in self.AnnoteSet:
      self.drawAnnote(self.axis,item[1],item[2],item[3],True)
    self.AnnoteSet = set()
    self.axis.figure.canvas.draw()

  def findIR(self, IRString):
    for i in str(IRString).split(','):
      self.drawSpecificAnnote(i.strip())
      
      
#fig = plt.figure(figsize=(6,6))
#ax = fig.add_subplot(111)
#ax = nx.Graph()
#x = range(11)
#y = range(11)
#try1=[]
#try2=[]
#annotes = []
#h =nx.path_graph(10)

#ax.add_nodes_from(h)
#pos = nx.spring_layout(ax)
#k = pos.iteritems()
#for node, posvalue in k:
#  try1.append(posvalue[0])
#  try2.append(posvalue[1])
#  annotes.append(node)
#nx.draw(ax,pos)
#af =  AnnoteFinder(try1,try2, annotes)
#fig.canvas.mpl_connect('button_press_event', af)
#plt.show()
