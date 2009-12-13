# --------------------------------------------------------------------------- #
# CUBECOLOURDIALOG Widget wxPython IMPLEMENTATION
#
# Python Code By:
#
# Andrea Gavana, @ 16 Aug 2007
# Latest Revision: 15 Oct 2008, 10.00 GMT
#
#
# TODO List
#
# 1. Find A Way To Reduce Flickering On The 2 ColourPanels;
#
# 2. See Why wx.GCDC Doesn't Work As I Thought (!). It Looks Slow As A Turtle,
#    But Probably I Am Doing Something Wrong While Painting The Alpha Textures.
#
#
# For All Kind Of Problems, Requests Of Enhancements And Bug Reports, Please
# Write To Me At:
#
# andrea.gavana@gmail.com
# gavana@kpo.kz
#
# Or, Obviously, To The wxPython Mailing List!!!
#
#
# End Of Comments
# --------------------------------------------------------------------------- #

"""
The CubeColourDialog is an alternative implementation of wx.ColourDialog, and it
offers different functionalities with respect to the default wxPython one. It
can be used as a replacement of wx.ColourDialog with exactly the same syntax and
methods.

Some features:

  - RGB components may be controlled using spin controls or with mouse gestures
    on a 3D RGB cube, with the 3 components laying on the X, Y, Z axes;
  - HSB components may be controlled using spin controls or with mouse gestures
    on a 2D colour wheel;
  - Brightness has its own vertical slider to play with;
  - The colour alpha channel can be controlled using another vertical slider, or
    via spin control;
  - The colour alpha channel controls can be completely hidden at startup or the
    choice to use the alpha channel can be left to the user while playing with the
    dialog, via a simple wx.CheckBox;
  - The "old colour" and "new colour" are displayed in two small custom panel,
    which support alpha transparency and texture;
  - CubeColourDialog displays also the HTML colour code in hexadecimal format;
  - When available, a corresponding "Web Safe" colour is generated using a 500
    web colours "database" (a dictionary inside the widget source code). Web Safe
    colours are recognized by all the browsers;
  - When available, a corresponding "HTML name" for the selected colour is displayed,
    by using the same 500 web colours "database";
  - When available, a corresponding "Microsoft Access Code" for the selected colour
    is displayed, by using the same 500 web colours "database".
    
And much more.


License And Version:

CubeColourDialog is freeware and distributed under the wxPython license. 

Latest Revision: Andrea Gavana @ 15 Oct 2008, 10.00 GMT

Version 0.2.


@undocumented: Vertex, Left, Top, Right, colourAttributes, colourMaxValues,
               checkColour, HTMLCodes
               

"""

__docformat__ = "epytext"


#----------------------------------------------------------------------
# Beginning Of CUBECOLOURDIALOG wxPython Code
#----------------------------------------------------------------------

import wx
import colorsys

from math import pi, sin, cos, sqrt, atan2

from wx.lib.embeddedimage import PyEmbeddedImage

# Show the alpha control in the dialog
CCD_SHOW_ALPHA = 1
""" Show the alpha control in the dialog. """

# Radius of the HSB colour wheel
RADIUS = 100
""" Radius of the HSB colour wheel. """

# Width of the mouse-controlled colour pointer
RECT_WIDTH = 5
""" Width of the mouse-controlled colour pointer. """

# Dictionary keys for the RGB colour cube
RED, GREEN, BLUE = 0, 1, 2
""" Dictionary keys for the RGB colour cube. """

Vertex = wx.Point(95, 109)
Top = wx.Point(95, 10)
Left = wx.Point(16, 148)
Right = wx.Point(174, 148)

colourAttributes = ["r", "g", "b", "h", "s", "v"]
colourMaxValues = [255, 255, 255, 359, 255, 255]
checkColour = wx.Colour(200, 200, 200)


HSVWheelImage = PyEmbeddedImage(
    "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"
    "YII=")

#----------------------------------------------------------------------
RGBCubeImage = PyEmbeddedImage(
    "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"
    "RK5CYII=")


def rad2deg(x):
    """ Transforms radians into degrees. """
    return 180.0*x/pi

def deg2rad(x):
    """ Transforms degrees into radians. """
    return x*pi/180.0

def toscale(x):
    """ Normalize a value as a function of the radius. """ 
    return x*RADIUS/255.0

def scaletomax(x):
    """ Normalize a value as a function of the radius. """ 
    return x*255.0/RADIUS

def rgb2html(colour):
    """ Transforms a RGB triplet into an html hex string. """
    hexColour = "#%02x%02x%02x"%(colour.r, colour.g, colour.b)
    return hexColour.upper()

    
def Slope(pt1, pt2):
    """ Calculates the slope of the line connecting 2 points. """

    y = float(pt2.y - pt1.y)
    x = float(pt2.x - pt1.x)

    if x:
        return y/x
    else:
        return None


def Intersection(line1, line2):
    """ Calculates the intersection point between 2 lines. """

    if line1.slope == line2.slope:
    
        # Parallel lines, no intersection
        return wx.Point(0, 0)
    
    elif line1.slope is None:
    
        # First Line is vertical, eqn is x=0
        # Put x = 0 in second line eqn to get y
        x = line1.x
        y = line2.slope*x + line2.c
    
    elif line2.slope is None:
    
        # second line is vertical Equation of line is x=0
        # Put x = 0 in first line eqn to get y
        x = line2.x
        y = line1.slope*line2.x + line1.c
    
    else:
    
        y = ((line1.c*line2.slope) - (line2.c*line1.slope))/(line2.slope - line1.slope)
        x = (y - line1.c)/line1.slope
    

    return wx.Point(int(x), int(y))


def FindC(line):
    """ Internal function. """

    if line.slope is None:
        c = line.y
    else:
        c = line.y - line.slope*line.x
    
    return c


def PointOnLine(pt1, pt2, length, maxLen):
    """ Internal function. """

    a = float(length)

    if pt2.x != pt1.x:
    
        m = float((pt2.y - pt1.y))/(pt2.x - pt1.x)
        m2 = m*m
        a2 = a*a
        c = pt1.y - m*pt1.x
        c2 = c*c

        A = 1.0
        
        x = pt1.x

        B = 2.0 * pt1.x

        x *= x
        C = x - a2/(m2 + 1)
        
        x = (B + sqrt(B*B - (4.0*A*C)))/(2.0*A)
        y = m*x + c
        pt = wx.Point(int(x), int(y))

        if Distance(pt, pt1) > maxLen or Distance(pt, pt2) > maxLen:
        
            x = (B - sqrt(B*B - (4.0*A*C)))/(2.0*A)
            y = m*x + c
            pt = wx.Point(int(x), int(y))
        
    
    else:
    
        a2 = a*a
        y = sqrt(a2)
        x = 0.0
        pt = wx.Point(int(x), int(y))
        pt.x += pt1.x
        pt.y += pt1.y
        
        if Distance(pt, pt1) > maxLen or Distance(pt, pt2) > maxLen:

            y = -1.0*y        
            pt = wx.Point(int(x), int(y))
            pt.x += pt1.x
            pt.y += pt1.y
    
    return pt


def Distance(pt1, pt2):
    """ Returns the distance between 2 points. """

    distance = sqrt((pt1.x - pt2.x)**2.0 + (pt1.y - pt2.y)**2.0)
    return int(distance)


def AngleFromPoint(pt, center):
    """
    Returns the angle between the x-axis and the line connecting the center and
    the point pt.
    """

    y = -1*(pt.y - center.y)
    x = pt.x - center.x
    if x == 0 and y == 0:
    
        return 0.0
    
    else:
    
        return atan2(y, x)
    

def PtFromAngle(angle, sat, center):
    """
    Given the angle with respect to the x-axis, returns the point based on
    the saturation value.
    """

    angle = deg2rad(angle)
    sat = toscale(sat)

    x = sat*cos(angle)
    y = sat*sin(angle)

    pt = wx.Point(int(x), -int(y))
    pt.x += center.x
    pt.y += center.y
    
    return pt


def RestoreOldDC(dc, oldPen, oldBrush, oldMode):
    """ Restores the old settings for a wx.DC. """

    dc.SetPen(oldPen)
    dc.SetBrush(oldBrush)
    dc.SetLogicalFunction(oldMode)


def DrawCheckerBoard(dc, rect, checkColour, box=5):
    """
    Draws a checkerboard on a wx.DC.
    Used for the Alpha channel control and the colour panels.
    """

    y = rect.y
    checkPen = wx.Pen(checkColour)
    checkBrush = wx.Brush(checkColour)

    dc.SetPen(checkPen) 
    dc.SetBrush(checkBrush)
    dc.SetClippingRect(rect)
    
    while y < rect.height: 
        x = box*((y/box)%2) + 2
        while x < rect.width: 
            dc.DrawRectangle(x, y, box, box) 
            x += box*2 
        y += box
        


class Colour(wx.Colour):
    """
    This is a subclass of wx.Colour, which adds Hue, Saturation and Brightness
    capability to the base class. It contains also methods to convert RGB triplets
    into HSB triplets and vice-versa.
    """

    def __init__(self, colour):
        """
        Default class constructor.

        colour is a standard wxPython colour.
        """

        wx.Colour.__init__(self)
        
        self.r = colour.Red()
        self.g = colour.Green()
        self.b = colour.Blue()
        #self.alpha = colour.Alpha()
        
        self.ToHSV()

        
    def ToRGB(self):
        """ Converts a HSV triplet into a RGB triplet. """
    
        maxVal = self.v
        delta = (maxVal*self.s)/255.0
        minVal = maxVal - delta

        hue = float(self.h)

        if self.h > 300 or self.h <= 60:
        
            self.r = maxVal
            
            if self.h > 300:
            
                self.g = int(minVal)
                hue = (hue - 360.0)/60.0
                self.b = int(-(hue*delta - minVal))
            
            else:
            
                self.b = int(minVal)
                hue = hue/60.0
                self.g = int(hue*delta + minVal)
            
        elif self.h > 60 and self.h < 180:
        
            self.g = int(maxVal)
            
            if self.h < 120:
            
                self.b = int(minVal)
                hue = (hue/60.0 - 2.0)*delta
                self.r = int(minVal - hue)
            
            else:
            
                self.r = int(minVal)
                hue = (hue/60.0 - 2.0)*delta
                self.b = int(minVal + hue)
            
        
        else:
        
            self.b = int(maxVal)
            
            if self.h < 240:
            
                self.r = int(minVal)
                hue = (hue/60.0 - 4.0)*delta
                self.g = int(minVal - hue)
            
            else:
            
                self.g = int(minVal)
                hue = (hue/60.0 - 4.0)*delta
                self.r = int(minVal + hue)
        

    def ToHSV(self):
        """ Converts a RGB triplet into a HSV triplet. """

        minVal = float(min(self.r, min(self.g, self.b)))
        maxVal = float(max(self.r, max(self.g, self.b)))
        delta = maxVal - minVal
        
        self.v = int(maxVal)
        
        if abs(delta) < 1e-6:
        
            self.h = self.s = 0
        
        else:
        
            temp = delta/maxVal
            self.s = int(temp*255.0)

            if self.r == int(maxVal):
            
                temp = float(self.g-self.b)/delta
            
            elif self.g == int(maxVal):
            
                temp = 2.0 + (float(self.b-self.r)/delta)
            
            else:
            
                temp = 4.0 + (float(self.r-self.g)/delta)
            
            temp *= 60
            if temp < 0:
            
                temp += 360
            
            elif temp >= 360.0:
            
                temp = 0

            self.h = int(temp)


    def GetPyColour(self):
        """ Returns the wxPython wx.Colour associated with this instance. """

        return wx.Colour(self.r, self.g, self.b, self.alpha)

    
        
class LineDescription(object):
    """ Simple class to store description and constants for a line in 2D space. """

    def __init__(self, x=0, y=0, slope=None, c=None):
        """
        Default class constructor.
        Used internally. Do not call it in your code!
        """

        self.x = x
        self.y = y
        self.slope = slope
        self.c = c

        

class BasePyControl(wx.PyControl):
    """
    Base class used to hold common code for the HSB colour wheel and the RGB
    colour cube.
    """

    def __init__(self, parent, bitmap=None):
        """
        Default class constructor.
        Used internally. Do not call it in your code!
        """

        wx.PyControl.__init__(self, parent, style=wx.NO_BORDER)
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)

        self._bitmap = bitmap
        mask = wx.Mask(self._bitmap, wx.Colour(192, 192, 192))
        self._bitmap.SetMask(mask)
        
        self._mainDialog = wx.GetTopLevelParent(self)

        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_MOTION, self.OnMotion)


    def OnPaint(self, event):
        """ Handles the wx.EVT_PAINT for L{BasePyControl}. """

        dc = wx.AutoBufferedPaintDC(self)
        dc.SetBackground(wx.Brush(self.GetParent().GetBackgroundColour()))
        
        dc.Clear()
        dc.DrawBitmap(self._bitmap, 0, 0, True)

        if self._mainDialog._initOver:
            self.DrawMarkers(dc)
        

    def OnEraseBackground(self, event):
        """ Handles the wx.EVT_ERASE_BACKGROUND for L{BasePyControl}. """

        pass

    
    def DrawMarkers(self, dc=None):
        """ Empty method. Must be overridden in subclasses. """

        pass


    def DrawLines(self, dc):
        """ Empty method. Must be overridden in subclasses. """

        pass
    

    def AcceptsFocusFromKeyboard(self):
        """ We do not accept focus from keyboard. """

        return False


    def AcceptFocus(self):
        """ We do not accept mouse focus. """

        return False

    
    def OnLeftDown(self, event):
        """
        Handles the wx.EVT_LEFT_DOWN for L{BasePyControl}.
        Must be overridden in subclasses.
        """

        pass


    def OnLeftUp(self, event):
        """
        Handles the wx.EVT_LEFT_UP for L{BasePyControl}.
        Must be overridden in subclasses.
        """

        pass


    def OnMotion(self, event):
        """
        Handles the wx.EVT_MOTION for L{BasePyControl}.
        Must be overridden in subclasses.
        """

        pass
    
    
    def OnSize(self, event):
        """ Handles the wx.EVT_SIZE event for L{BasePyControl}. """

        self.Refresh()
        

    def DoGetBestSize(self):
        """ Returns the custom control best size (used by sizers). """

        return wx.Size(self._bitmap.GetWidth(), self._bitmap.GetHeight())        

        

class RGBCube(BasePyControl):
    """
    Implements the drawing, mouse handling and sizing routines for the RGB
    cube colour.
    """

    def __init__(self, parent):
        """
        Default class constructor.
        Used internally. Do not call it in your code!
        """

        BasePyControl.__init__(self, parent, bitmap=RGBCubeImage.GetBitmap())
        self._index = -1


    def DrawMarkers(self, dc=None):
        """ Draws the square markers used with mouse gestures. """

        if dc is None:
            dc = wx.ClientDC(self)

        oldPen, oldBrush, oldMode = dc.GetPen(), dc.GetBrush(), dc.GetLogicalFunction()
        dc.SetPen(wx.WHITE_PEN)
        dc.SetBrush(wx.TRANSPARENT_BRUSH)
        dc.SetLogicalFunction(wx.XOR)

        rects = []
        blueLen = self._mainDialog._blueLen
        greenLen = self._mainDialog._greenLen
        redLen = self._mainDialog._redLen
        colour = self._mainDialog._colour

        pt = [wx.Point() for i in xrange(3)]
        pt[0] = PointOnLine(Vertex, Top, (colour.r*redLen)/255, redLen)
        pt[1] = PointOnLine(Vertex, Left, (colour.g*greenLen)/255, greenLen)
        pt[2] = PointOnLine(Vertex, Right, (colour.b*blueLen)/255, blueLen)

        for i in xrange(3):
            rect = wx.Rect(pt[i].x - RECT_WIDTH, pt[i].y - RECT_WIDTH, 2*RECT_WIDTH, 2*RECT_WIDTH)
            rects.append(rect)
            dc.DrawRectangleRect(rect)

        self.DrawLines(dc)
        RestoreOldDC(dc, oldPen, oldBrush, oldMode)

        self._rects = rects
        

    def DrawLines(self, dc):
        """ Draws lines connecting the markers. """
    
        cuboid = self._mainDialog._cuboid
        
        dc.DrawLinePoint(cuboid[1], cuboid[2])
        dc.DrawLinePoint(cuboid[2], cuboid[3])
        dc.DrawLinePoint(cuboid[3], cuboid[4])
        dc.DrawLinePoint(cuboid[4], cuboid[5])
        dc.DrawLinePoint(cuboid[5], cuboid[2])

        dc.DrawLinePoint(cuboid[5], cuboid[6])
        dc.DrawLinePoint(cuboid[6], cuboid[7])
        dc.DrawLinePoint(cuboid[7], cuboid[4])

        dc.DrawLinePoint(cuboid[1], cuboid[6])
        

    def OnLeftDown(self, event):
        """ Handles the wx.EVT_LEFT_DOWN event for L{RGBCube}. """

        point = wx.Point(event.GetX(), event.GetY())
        self._mouseIn = False

        if self._rects[RED].Contains(point):
            self.CaptureMouse()
            self._mouseIn = True
            self._index = RED
        
        elif self._rects[GREEN].Contains(point):
            self.CaptureMouse()
            self._mouseIn = True
            self._index = GREEN
        
        elif self._rects[BLUE].Contains(point):
            self.CaptureMouse()
            self._mouseIn = True
            self._index = BLUE

        

    def OnLeftUp(self, event):
        """ Handles the wx.EVT_LEFT_UP event for L{RGBCube}. """

        if self.GetCapture():
            self.ReleaseMouse()
            self._mouseIn = False
        

    def OnMotion(self, event):
        """ Handles the wx.EVT_MOTION event for L{RGBCube}. """

        point = wx.Point(event.GetX(), event.GetY())
        
        if not (self.GetCapture() and self._mouseIn):
            event.Skip()
            return

        bChange = False
        mainDialog = self._mainDialog
        colour = mainDialog._colour
        redLen, greenLen, blueLen = mainDialog._redLen, mainDialog._greenLen, mainDialog._blueLen

        dc = wx.ClientDC(self)
        self.DrawMarkers(dc)
        
        if self._index == RED:
        
            if point.y > Vertex.y:          
                point.y = Vertex.y
            
            point.x = Vertex.x
            val = Distance(point, Vertex)
            if val > redLen:
                val = redLen
            
            val = (float(val)/redLen)*255
            colour.r = int(val)

            pt = PointOnLine(Vertex, Top, (colour.r*redLen)/255, redLen)
            self._rects[RED] = wx.Rect(pt.x - RECT_WIDTH, pt.y - RECT_WIDTH,
                                       2*RECT_WIDTH, 2*RECT_WIDTH)

            bChange = True
        
        elif self._index == GREEN:
        
            if point.x > Vertex.x:          
                point.x = Vertex.x
            
            point.y = self._rects[GREEN].GetTop() + RECT_WIDTH
            val = Distance(point, Vertex)
            if val > greenLen:
                val = greenLen
            
            val = (float(val)/greenLen)*255
            colour.g = int(val)

            pt = PointOnLine(Vertex, Left, (colour.g*greenLen)/255, greenLen)
            self._rects[GREEN] = wx.Rect(pt.x - RECT_WIDTH, pt.y - RECT_WIDTH,
                                         2*RECT_WIDTH, 2*RECT_WIDTH)

            bChange = True
        
        elif self._index == BLUE:
        
            if point.x < Vertex.x:
                point.x = Vertex.x

            point.y = self._rects[BLUE].GetTop() + RECT_WIDTH
            val = Distance(point, Vertex)
            if val > blueLen:
                val = blueLen
            
            val = (float(val)/blueLen)*255
            colour.b = int(val)

            pt = PointOnLine(Vertex, Right, (colour.b*blueLen)/255, blueLen)
            self._rects[BLUE] = wx.Rect(pt.x - RECT_WIDTH, pt.y - RECT_WIDTH,
                                        2*RECT_WIDTH, 2*RECT_WIDTH)
            
            bChange = True
        
        if bChange:

            mainDialog.CalcCuboid()
            self.DrawMarkers(dc)
        
            colour.ToHSV()
            mainDialog.SetSpinVals()
            mainDialog.CalcRects()

            mainDialog.DrawHSB()
            mainDialog.DrawBright()
            #mainDialog.DrawAlpha()
        
    
class HSVWheel(BasePyControl):
    """
    Implements the drawing, mouse handling and sizing routines for the HSV
    colour wheel.
    """

    def __init__(self, parent):
        """
        Default class constructor.
        Used internally. Do not call it in your code!
        """

        BasePyControl.__init__(self, parent, bitmap=HSVWheelImage.GetBitmap())
        self._mouseIn = False


    def DrawMarkers(self, dc=None):
        """ Draws the square markers used with mouse gestures. """

        if dc is None:
            dc = wx.ClientDC(self)

        oldPen, oldBrush, oldMode = dc.GetPen(), dc.GetBrush(), dc.GetLogicalFunction()
        dc.SetPen(wx.WHITE_PEN)
        dc.SetBrush(wx.TRANSPARENT_BRUSH)
        dc.SetLogicalFunction(wx.XOR)
        
        dc.DrawRectangleRect(self._mainDialog._currentRect)
        RestoreOldDC(dc, oldPen, oldBrush, oldMode)
        

    def OnLeftDown(self, event):
        """ Handles the wx.EVT_LEFT_DOWN event for L{HSVWheel}. """

        point = wx.Point(event.GetX(), event.GetY())
        self._mouseIn = False

        if self.InCircle(point):
            self._mouseIn = True

        if self._mouseIn:
            self.CaptureMouse()
            self.TrackPoint(point)


    def OnLeftUp(self, event):
        """ Handles the wx.EVT_LEFT_UP event for L{HSVWheel}. """

        if self.GetCapture():
            self.ReleaseMouse()
            self._mouseIn = False


    def OnMotion(self, event):
        """ Handles the wx.EVT_MOTION event for L{HSVWheel}. """

        point = wx.Point(event.GetX(), event.GetY())

        if self.GetCapture() and self._mouseIn:
            self.TrackPoint(point)
        

    def InCircle(self, pt):
        """ Returns whether a point is inside the HSV wheel or not. """

        return Distance(pt, self._mainDialog._centre) <= RADIUS


    def TrackPoint(self, pt):
        """ Track a mouse event inside the HSV colour wheel. """

        if not self._mouseIn:
            return

        dc = wx.ClientDC(self)
        self.DrawMarkers(dc)
        mainDialog = self._mainDialog
        colour = mainDialog._colour
                
        colour.h = int(rad2deg(AngleFromPoint(pt, mainDialog._centre)))
        if colour.h < 0:
            colour.h += 360

        colour.s = int(scaletomax(Distance(pt, mainDialog._centre)))
        if colour.s > 255:
            colour.s = 255

        mainDialog.CalcRects()
        self.DrawMarkers(dc)
        colour.ToRGB()
        mainDialog.SetSpinVals()
        
        mainDialog.CalcCuboid()
        mainDialog.DrawRGB()
        mainDialog.DrawBright()
        #mainDialog.DrawAlpha()


class BaseLineCtrl(wx.PyControl):
    """
    Base class used to hold common code for the Alpha channel control and the
    brightness palette control.
    """

    def __init__(self, parent):
        """
        Default class constructor.
        Used internally. Do not call it in your code!
        """

        wx.PyControl.__init__(self, parent, size=(20, 200), style=wx.NO_BORDER)
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)    

        self._mainDialog = wx.GetTopLevelParent(self)
        
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_MOTION, self.OnMotion)


    def OnEraseBackground(self, event):
        """ Handles the wx.EVT_ERASE_BACKGROUND for L{BaseLineCtrl}. """

        pass

    
    def OnLeftDown(self, event):
        """ Handles the wx.EVT_LEFT_DOWN for L{BaseLineCtrl}. """

        point = wx.Point(event.GetX(), event.GetY())
        theRect = self.GetClientRect()

        if not theRect.Contains(point):
            event.Skip()
            return
        
        self.CaptureMouse()
        self.TrackPoint(point)


    def OnLeftUp(self, event):
        """ Handles the wx.EVT_LEFT_UP for L{BaseLineCtrl}. """

        if self.GetCapture():
            self.ReleaseMouse()
            

    def OnMotion(self, event):
        """ Handles the wx.EVT_MOTION for L{BaseLineCtrl}. """

        point = wx.Point(event.GetX(), event.GetY())

        if self.GetCapture():
            self.TrackPoint(point)


    def OnSize(self, event):
        """ Handles the wx.EVT_SIZE for L{BaseLineCtrl}. """

        self.Refresh()


    def DoGetBestSize(self):
        """ Returns the custom control best size (used by sizers). """

        return wx.Size(24, 208)    


    def BuildRect(self):
        """ Internal method. """

        brightRect = wx.Rect(*self.GetClientRect())
        brightRect.x += 2
        brightRect.y += 6
        brightRect.width -= 4
        brightRect.height -= 8

        return brightRect


    def AcceptsFocusFromKeyboard(self):
        """ We do not accept focus from keyboard. """

        return False


    def AcceptFocus(self):
        """ We do not accept mouse focus. """

        return False



class BrightCtrl(BaseLineCtrl):
    """
    Implements the drawing, mouse handling and sizing routines for the brightness
    palette control.
    """

    def __init__(self, parent):
        """
        Default class constructor.
        Used internally. Do not call it in your code!
        """

        BaseLineCtrl.__init__(self, parent)
        self.Bind(wx.EVT_PAINT, self.OnPaint)

        
    def OnPaint(self, event):
        """ Handles the wx.EVT_PAINT event for L{BrightCtrl}. """

        dc = wx.AutoBufferedPaintDC(self)
        dc.SetBackground(wx.Brush(self.GetParent().GetBackgroundColour()))
        dc.Clear()
        
        colour = self._mainDialog._colour.GetPyColour()
        brightRect = self.BuildRect()
        
        target_red = colour.Red()
        target_green = colour.Green()
        target_blue = colour.Blue()

        h, s, v = colorsys.rgb_to_hsv(target_red / 255.0, target_green / 255.0,
                                      target_blue / 255.0)
        v = 1.0
        vstep = 1.0/(brightRect.height-1)
        
        for y_pos in range(brightRect.y, brightRect.height+brightRect.y):
            r, g, b = [c * 255.0 for c in colorsys.hsv_to_rgb(h, s, v)]
            colour = wx.Colour(int(r), int(g), int(b))
            dc.SetPen(wx.Pen(colour, 1, wx.SOLID))
            dc.DrawRectangle(brightRect.x, y_pos, brightRect.width, 1)
            v = v - vstep

        dc.SetPen(wx.BLACK_PEN)
        dc.SetBrush(wx.TRANSPARENT_BRUSH)
        dc.DrawRectangleRect(brightRect)
        
        self.DrawMarkers(dc)
        
        
    def TrackPoint(self, pt):
        """ Tracks a mouse action inside the palette control. """

        brightRect = self.BuildRect()
        d = brightRect.GetBottom() - pt.y
        d *= 255
        d /= brightRect.height
        if d < 0:
            d = 0
        if d > 255:
            d = 255;
        
        mainDialog = self._mainDialog
        colour = mainDialog._colour

        mainDialog.DrawMarkers()        
        colour.v = int(d)

        colour.ToRGB()
        mainDialog.SetSpinVals()

        mainDialog.CalcRects()
        mainDialog.CalcCuboid()
        mainDialog.DrawMarkers()
        #mainDialog.DrawAlpha()


    def DrawMarkers(self, dc=None):
        """ Draws square markers used with mouse gestures. """

        if dc is None:
            dc = wx.ClientDC(self)
            
        colour = self._mainDialog._colour
        brightRect = self.BuildRect()
        
        y = int(colour.v/255.0*brightRect.height)
        y = brightRect.GetBottom() - y
        brightMark = wx.Rect(brightRect.x-2, y-4, brightRect.width+4, 8)

        oldPen, oldBrush, oldMode = dc.GetPen(), dc.GetBrush(), dc.GetLogicalFunction()
        dc.SetPen(wx.Pen(wx.WHITE, 2))
        dc.SetBrush(wx.TRANSPARENT_BRUSH)
        dc.SetLogicalFunction(wx.XOR)
        
        dc.DrawRectangleRect(brightMark)
        RestoreOldDC(dc, oldPen, oldBrush, oldMode)



class AlphaCtrl(BaseLineCtrl):
    """
    Implements the drawing, mouse handling and sizing routines for the alpha
    channel control. 
    """

    def __init__(self, parent):
        """
        Default class constructor.
        Used internally. Do not call it in your code!
        """

        BaseLineCtrl.__init__(self, parent)
        self.Bind(wx.EVT_PAINT, self.OnPaint)


    def OnPaint(self, event):
        """ Handles the wx.EVT_PAINT event for L{AlphaCtrl}. """

        pdc = wx.PaintDC(self)
        dc = wx.GCDC(pdc)

        mem_dc = wx.MemoryDC()
        fullRect = self.GetClientRect()
        bmp = wx.EmptyBitmap(fullRect.width, fullRect.height)
        mem_dc.SelectObject(bmp)
        
        rect = self.BuildRect()
        backBrush = wx.Brush(self.GetParent().GetBackgroundColour())
        mem_dc.SetBackground(backBrush)
        mem_dc.Clear()

        mem_dc.SetBrush(wx.WHITE_BRUSH)
        mem_dc.DrawRectangleRect(rect)

        DrawCheckerBoard(mem_dc, rect, checkColour)
        self.DrawAlphaShading(mem_dc, rect)
        mem_dc.DestroyClippingRegion()
        
        self.DrawMarkers(mem_dc)
        
        mem_dc.SetBrush(wx.TRANSPARENT_BRUSH)
        mem_dc.SetPen(wx.BLACK_PEN)
        mem_dc.DrawRectangleRect(rect)

        mem_dc.SelectObject(wx.NullBitmap)
        pdc.DrawBitmap(bmp, 0, 0)
        

    def DrawAlphaShading(self, dc, rect):
        """ Draws the alpha shading on top of the checkerboard. """

        gcdc = wx.GCDC(dc)
        
        colour = self._mainDialog._colour.GetPyColour()
        
        alpha = 255.0
        vstep = 255.0*2/(rect.height-1)
        r, g, b = colour.Red(), colour.Green(), colour.Blue()

        colour_gcdc = wx.Colour(r, g, b, alpha)
        gcdc.SetBrush(wx.TRANSPARENT_BRUSH)
        
        for y_pos in range(rect.y, rect.height+rect.y, 2):
            colour_gcdc = wx.Colour(r, g, b, int(alpha))
            gcdc.SetPen(wx.Pen(colour_gcdc, 1, wx.SOLID))
            gcdc.DrawRectangle(rect.x, y_pos, rect.width, 2)
            alpha = alpha - vstep


    def TrackPoint(self, pt):
        """ Tracks a mouse action inside the Alpha channel control. """

        alphaRect = self.BuildRect()
        d = alphaRect.GetBottom() - pt.y
        d *= 255
        d /= alphaRect.height
        if d < 0:
            d = 0
        if d > 255:
            d = 255

        self._mainDialog
        self._mainDialog._colour.alpha = int(d)
        self.Refresh()
        self._mainDialog.SetSpinVals()


    def DrawMarkers(self, dc=None):
        """ Draws square markers used with mouse gestures. """

        if dc is None:
            dc = wx.ClientDC(self)
            
        colour = self._mainDialog._colour
        alphaRect = self.BuildRect()
        
        y = int(colour.alpha/255.0*alphaRect.height)
        y = alphaRect.GetBottom() - y
        alphaMark = wx.Rect(alphaRect.x-2, y-4, alphaRect.width+4, 8)

        oldPen, oldBrush, oldMode = dc.GetPen(), dc.GetBrush(), dc.GetLogicalFunction()
        dc.SetPen(wx.Pen(wx.WHITE, 2))
        dc.SetBrush(wx.TRANSPARENT_BRUSH)
        dc.SetLogicalFunction(wx.XOR)
        
        dc.DrawRectangleRect(alphaMark)
        RestoreOldDC(dc, oldPen, oldBrush, oldMode)
        
        
class ColourPanel(wx.PyPanel):
    """
    Simple custom class used to display "old" and "new" colour panels, with alpha
    blending capabilities.
    """

    def __init__(self, parent, style=wx.SIMPLE_BORDER):
        """
        Default class constructor.
        Used internally. Do not call it in your code!
        """

        wx.PyPanel.__init__(self, parent, style=style)
        self._mainDialog = wx.GetTopLevelParent(self)
        
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        self.Bind(wx.EVT_SIZE, self.OnSize)

        self._colour = Colour(wx.WHITE)
        

    def OnPaint(self, event):
        """ Handles the wx.EVT_PAINT event for L{ColourPanel}. """

        pdc = wx.PaintDC(self)
        dc = wx.GCDC(pdc)

        mem_dc = wx.MemoryDC()
        rect = self.GetClientRect()
        bmp = wx.EmptyBitmap(rect.width, rect.height)
        mem_dc.SelectObject(bmp)
        
        backBrush = wx.Brush(self.GetParent().GetBackgroundColour())
        mem_dc.SetBackground(backBrush)
        mem_dc.Clear()

        mem_dc.SetBrush(wx.WHITE_BRUSH)
        mem_dc.DrawRectangleRect(rect)

        DrawCheckerBoard(mem_dc, rect, checkColour, box=10)

        gcdc = wx.GCDC(mem_dc)
        colour_gcdc = wx.Colour(self._colour.r, self._colour.g, self._colour.b, self._colour.alpha)
        gcdc.SetBrush(wx.Brush(colour_gcdc))
        gcdc.SetPen(wx.Pen(colour_gcdc))
        gcdc.DrawRectangleRect(rect)

        mem_dc.SelectObject(wx.NullBitmap)
        dc.DrawBitmap(bmp, 0, 0)


    def OnEraseBackground(self, event):
        """ Handles the wx.EVT_ERASE_BACKGROUND event for L{ColourPanel}. """

        pass
    

    def OnSize(self, event):
        """ Handles the wx.EVT_SIZE event for L{ColourPanel}. """

        self.Refresh()

        
    def RefreshColour(self, colour):
        """ Refresh the panel after a colour/alpha change. """

        self._colour = colour
        self.Refresh()
        
        
    def AcceptsFocusFromKeyboard(self):
        """ We do not accept focus from keyboard. """

        return False


    def AcceptFocus(self):
        """ We do not accept mouse focus. """

        return False


class CustomPanel(wx.PyControl):

    def __init__(self, parent, colourData):

        wx.PyControl.__init__(self, parent, style=wx.NO_BORDER)
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)

        self._colourData = colourData
        #self._customColours = [None]*16
        self._mainDialog = wx.GetTopLevelParent(self)
        
        #self.InitializeColours()

        self._smallRectangleSize = wx.Size(20, 16)
        self._gridSpacing = 4
        self._customColourRect = wx.Rect(2, 2, (8*self._smallRectangleSize.x) + (7*self._gridSpacing),
                                         (2*self._smallRectangleSize.y) + (1*self._gridSpacing))

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        

    #def InitializeColours(self):

        #curr = self._colourData.GetColour()
        #self._colourSelection = -1
        
        #for i in xrange(16):
            #c = self._colourData.GetCustomColour(i)
            #if c.Ok():
                #self._customColours[i] = self._colourData.GetCustomColour(i)
            #else:
                #self._customColours[i] = wx.Colour(255, 255, 255)

            #if c == curr:
                #self._colourSelection = i


    def DoGetBestSize(self):

        return self._customColourRect.width+4, self._customColourRect.height+4


    def OnPaint(self, event):

        dc = wx.AutoBufferedPaintDC(self)
        dc.SetBackground(wx.Brush(self.GetParent().GetBackgroundColour()))
        dc.Clear()

        self.PaintCustomColours(dc)
##        PaintCustomColour(dc);
        self.PaintHighlight(dc, True)


    def OnEraseBackground(self, event):

        pass


    def OnSize(self, event):

        self.Refresh()
        

    def OnLeftDown(self, event):

        x, y = event.GetX(), event.GetY()
        
        selX = (x - self._customColourRect.x)/(self._smallRectangleSize.x + self._gridSpacing)
        selY = (y - self._customColourRect.y)/(self._smallRectangleSize.y + self._gridSpacing)
        ptr = selX + selY*8

        dc = wx.ClientDC(self)
        self.PaintHighlight(dc, False)
        self._colourSelection = ptr

        self._mainDialog._colour = Colour(self._customColours[self._colourSelection])
        
        self.PaintCustomColour(dc, selX, selY)
        self.PaintHighlight(dc, True)
        self._mainDialog.DrawAll()


    #def PaintCustomColours(self, dc):

        #for i in xrange(2):
            #for j in xrange(8):
            
                #ptr = i*8 + j
                #x = (j*(self._smallRectangleSize.x+self._gridSpacing)) + self._customColourRect.x
                #y = (i*(self._smallRectangleSize.y+self._gridSpacing)) + self._customColourRect.y

                #dc.SetPen(wx.BLACK_PEN)

                #brush = wx.Brush(self._customColours[ptr])
                #dc.SetBrush(brush)

                #dc.DrawRectangle(x, y, self._smallRectangleSize.x, self._smallRectangleSize.y)
    

    def PaintHighlight(self, dc, draw=True):

        if self._colourSelection < 0:
            return

        # Number of pixels bigger than the standard rectangle size
        # for drawing a highlight
        deltaX = deltaY = 2

        # User-defined colours
        y = self._colourSelection/8
        x = self._colourSelection - (y*8)

        x = (x*(self._smallRectangleSize.x + self._gridSpacing) + self._customColourRect.x) - deltaX
        y = (y*(self._smallRectangleSize.y + self._gridSpacing) + self._customColourRect.y) - deltaY

        if draw:
            dc.SetPen(wx.BLACK_PEN)
        else:
            dc.SetPen(wx.LIGHT_GREY_PEN)

        dc.SetBrush(wx.TRANSPARENT_BRUSH)
        dc.DrawRectangle(x, y, (self._smallRectangleSize.x + (2*deltaX)), (self._smallRectangleSize.y + (2*deltaY)))


    def PaintCustomColour(self, dc, selX, selY):

        dc.SetPen(wx.BLACK_PEN)

        brush = wx.Brush(self._customColours[self._colourSelection])
        dc.SetBrush(brush)

        ptr = selX*8 + selY
        x = (selX*(self._smallRectangleSize.x+self._gridSpacing)) + self._customColourRect.x
        y = (selY*(self._smallRectangleSize.y+self._gridSpacing)) + self._customColourRect.y

        dc.DrawRectangle(x, y, self._smallRectangleSize.x, self._smallRectangleSize.y)

        dc.SetBrush(wx.NullBrush)


    #def AddCustom(self, colour):

        #self._colourSelection += 1
        #self._colourSelection = self._colourSelection%16
            
        #dc = wx.ClientDC(self)
        #self._customColours[self._colourSelection] = colour.GetPyColour()
        #self._colourData.SetCustomColour(self._colourSelection, self._customColours[self._colourSelection])

        #self.PaintCustomColours(dc)
        

class CubeColourDialog(wx.Dialog):

    """
    This is the CubeColourDialog main class implementation.
    """

    def __init__(self, parent, prevColor, colourData=None, style=CCD_SHOW_ALPHA):
        """
        Default class constructor.
        
        @param prevColor: a wxPython wx.Color
        @param colourData: a wxPython wx.ColourData;
        @param style: can be either None or CCD_SHOW_ALPHA, depending if you want
                      to hide the alpha channel control or not.
        """

        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title="CubeColourDialog: Choose Colour",
                           pos=wx.DefaultPosition, size=(900, 900), style=wx.DEFAULT_DIALOG_STYLE|style)

        if colourData:
            self._colourData = colourData
            self._colour = Colour(self._colourData.GetColour())
            self._oldColour = Colour(self._colourData.GetColour())            
        else:
            self._colourData = wx.ColourData()
            self._colourData.SetColour(wx.Colour(255, 255, 255))
            self._colour = Colour(self._colourData.GetColour())
            self._oldColour = Colour(prevColor)
        
        self._inMouse = False
        self._initOver = False
        self._inDrawAll = False

        self.mainPanel = wx.Panel(self, -1)

        self.hsvSizer_staticbox = wx.StaticBox(self.mainPanel, -1, "HSB")
        self.rgbValueSizer_staticbox = wx.StaticBox(self.mainPanel, -1, "RGB Values")
        self.hsvValueSizer_staticbox = wx.StaticBox(self.mainPanel, -1, "HSB Values")
        self.rgbSizer_staticbox = wx.StaticBox(self.mainPanel, -1, "RGB")
        #self.alphaSizer_staticbox = wx.StaticBox(self.mainPanel, -1, "Alpha")
        #self.alphaValueSizer_staticbox = wx.StaticBox(self.mainPanel, -1, "Alpha")

        self.rgbBitmap = RGBCube(self.mainPanel)
        self.hsvBitmap = HSVWheel(self.mainPanel)
        self.brightCtrl = BrightCtrl(self.mainPanel)
        #self.alphaCtrl = AlphaCtrl(self.mainPanel)

        #self.showAlpha = wx.CheckBox(self.mainPanel, -1, "Show Alpha Control")
        #self.customColours = CustomPanel(self.mainPanel, self._colourData)
        #self.addCustom = wx.Button(self.mainPanel, -1, "Add to custom colours")
        
        self.okButton = wx.Button(self.mainPanel, -1, "Ok")
        self.cancelButton = wx.Button(self.mainPanel, -1, "Cancel")

        self.oldColourPanel = ColourPanel(self.mainPanel, style=wx.SIMPLE_BORDER)
        self.newColourPanel = ColourPanel(self.mainPanel, style=wx.SIMPLE_BORDER)
        
        self.redSpin = wx.SpinCtrl(self.mainPanel, -1, "180", min=0, max=255,
                                   style=wx.SP_ARROW_KEYS)
        self.greenSpin = wx.SpinCtrl(self.mainPanel, -1, "180", min=0, max=255,
                                     style=wx.SP_ARROW_KEYS)
        self.blueSpin = wx.SpinCtrl(self.mainPanel, -1, "180", min=0, max=255,
                                    style=wx.SP_ARROW_KEYS)
        self.hueSpin = wx.SpinCtrl(self.mainPanel, -1, "0", min=0, max=359,
                                   style=wx.SP_ARROW_KEYS)
        self.saturationSpin = wx.SpinCtrl(self.mainPanel, -1, "", min=0, max=255,
                                          style=wx.SP_ARROW_KEYS)
        self.brightnessSpin = wx.SpinCtrl(self.mainPanel, -1, "", min=0, max=255,
                                          style=wx.SP_ARROW_KEYS)
        #self.alphaSpin = wx.SpinCtrl(self.mainPanel, -1, "", min=0, max=255,
                                     #style=wx.SP_ARROW_KEYS)
        #self.accessCode = wx.TextCtrl(self.mainPanel, -1, "", style=wx.TE_READONLY)
        #self.htmlCode = wx.TextCtrl(self.mainPanel, -1, "", style=wx.TE_READONLY)
        #self.webSafe = wx.TextCtrl(self.mainPanel, -1, "", style=wx.TE_READONLY)
        #self.htmlName = wx.TextCtrl(self.mainPanel, -1, "", style=wx.TE_READONLY)
        
        self.SetProperties()
        self.DoLayout()

        self.spinCtrls = [self.redSpin, self.greenSpin, self.blueSpin,
                          self.hueSpin, self.saturationSpin, self.brightnessSpin]

        for spin in self.spinCtrls:
            spin.Bind(wx.EVT_SPINCTRL, self.OnSpinCtrl)

        #self.Bind(wx.EVT_SPINCTRL, self.OnAlphaSpin, self.alphaSpin)
        
        self.Bind(wx.EVT_BUTTON, self.OnOk, self.okButton)
        self.Bind(wx.EVT_BUTTON, self.OnCancel, self.cancelButton)
        #self.Bind(wx.EVT_BUTTON, self.OnAddCustom, self.addCustom)

        #self.Bind(wx.EVT_CHECKBOX, self.OnShowAlpha)
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
        self.Bind(wx.EVT_CHAR_HOOK, self.OnKeyUp)

        self.Centre(wx.BOTH)

        wx.CallAfter(self.InitDialog)
        
        
    def SetProperties(self):
        """ Sets some initial properties (sizes, values). """

        self.okButton.SetDefault()
        self.oldColourPanel.SetMinSize((-1, 50))
        self.newColourPanel.SetMinSize((-1, 50))
        self.redSpin.SetMinSize((60, -1))
        self.greenSpin.SetMinSize((60, -1))
        self.blueSpin.SetMinSize((60, -1))
        self.hueSpin.SetMinSize((60, -1))
        self.saturationSpin.SetMinSize((60, -1))
        self.brightnessSpin.SetMinSize((60, -1))
        #self.alphaSpin.SetMinSize((60, -1))
        #self.showAlpha.SetValue(1)
        #self.accessCode.SetInitialSize((80, -1))
        #self.webSafe.SetInitialSize((80, -1))
        #self.htmlCode.SetInitialSize((80, -1))


    def DoLayout(self):
        """ Layouts all the controls in the L{CubeColourDialog}. """

        dialogSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer = wx.GridBagSizer(10, 5)
        hsvValueSizer = wx.StaticBoxSizer(self.hsvValueSizer_staticbox, wx.VERTICAL)
        hsvGridSizer = wx.GridSizer(2, 3, 2, 10)
        rgbValueSizer = wx.StaticBoxSizer(self.rgbValueSizer_staticbox, wx.HORIZONTAL)
        rgbGridSizer = wx.GridSizer(2, 3, 2, 10)
        #alphaValueSizer = wx.StaticBoxSizer(self.alphaValueSizer_staticbox, wx.VERTICAL)
        #alphaGridSizer = wx.BoxSizer(wx.VERTICAL)
        customSizer = wx.BoxSizer(wx.VERTICAL)
        buttonSizer = wx.BoxSizer(wx.VERTICAL)
        accessSizer = wx.BoxSizer(wx.VERTICAL)
        panelSizer = wx.BoxSizer(wx.VERTICAL)
        #htmlSizer1 = wx.BoxSizer(wx.HORIZONTAL)
        #htmlSizer2 = wx.BoxSizer(wx.VERTICAL)
        #htmlSizer_a = wx.BoxSizer(wx.VERTICAL)
        #htmlSizer_b = wx.BoxSizer(wx.VERTICAL)
        
        hsvSizer = wx.StaticBoxSizer(self.hsvSizer_staticbox, wx.HORIZONTAL)
        rgbSizer = wx.StaticBoxSizer(self.rgbSizer_staticbox, wx.VERTICAL)
        #alphaSizer = wx.StaticBoxSizer(self.alphaSizer_staticbox, wx.VERTICAL)

        #mainSizer.Add(self.showAlpha, (0, 0), (1, 1), wx.LEFT|wx.TOP, 10)

        #htmlLabel1 = wx.StaticText(self.mainPanel, -1, "HTML Code")
        #htmlLabel2 = wx.StaticText(self.mainPanel, -1, "Web Safe")
        #htmlSizer_a.Add(htmlLabel1, 0, wx.TOP, 3)
        #htmlSizer_b.Add(htmlLabel2, 0, wx.TOP, 3)
        #htmlSizer_a.Add(self.htmlCode, 0, wx.TOP, 3)
        #htmlSizer_b.Add(self.webSafe, 0, wx.TOP, 3)

        #htmlSizer1.Add(htmlSizer_a, 0)
        #htmlSizer1.Add(htmlSizer_b, 0, wx.LEFT, 10)
        #mainSizer.Add(htmlSizer1, (1, 0), (1, 1), wx.LEFT|wx.RIGHT, 10)
        
        #htmlLabel3 = wx.StaticText(self.mainPanel, -1, "HTML Name")
        #htmlSizer2.Add(htmlLabel3, 0, wx.TOP|wx.BOTTOM, 3)
        #htmlSizer2.Add(self.htmlName, 0)
        
        #mainSizer.Add(htmlSizer2, (1, 1), (1, 1), wx.LEFT|wx.RIGHT, 10)

        #customLabel = wx.StaticText(self.mainPanel, -1, "Custom Colours")
        #customSizer.Add(customLabel, 0, wx.BOTTOM, 3)
        #customSizer.Add(self.customColours, 0)
        #customSizer.Add(self.addCustom, 0, wx.TOP|wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL, 5)
        #mainSizer.Add(customSizer, (0, 2), (2, 2), wx.ALIGN_CENTER|wx.LEFT|wx.RIGHT, 5)

        rgbSizer.Add(self.rgbBitmap, 0, wx.ALL, 15)
        mainSizer.Add(rgbSizer, (2, 0), (1, 1), wx.ALL|wx.EXPAND, 10)
        hsvSizer.Add(self.hsvBitmap, 0, wx.ALL, 15)
        hsvSizer.Add(self.brightCtrl, 0, wx.RIGHT|wx.TOP|wx.BOTTOM, 15)
        mainSizer.Add(hsvSizer, (2, 1), (1, 1), wx.ALL|wx.EXPAND, 10)
        #alphaSizer.Add(self.alphaCtrl, 0, wx.TOP|wx.ALIGN_CENTER, 15)
        #mainSizer.Add(alphaSizer, (2, 2), (1, 1), wx.ALL|wx.EXPAND, 10)
        
        oldLabel = wx.StaticText(self.mainPanel, -1, "Old Colour")
        panelSizer.Add(oldLabel, 0, wx.BOTTOM, 3)
        panelSizer.Add(self.oldColourPanel, 0, wx.BOTTOM|wx.EXPAND, 20)
        newLabel = wx.StaticText(self.mainPanel, -1, "New Colour")
        #accessLabel = wx.StaticText(self.mainPanel, -1, "MS Access Code")
        #accessSizer.Add(accessLabel, 0, wx.BOTTOM, 3)
        #accessSizer.Add(self.accessCode, 0)
        panelSizer.Add(newLabel, 0, wx.BOTTOM, 3)
        panelSizer.Add(self.newColourPanel, 0, wx.EXPAND)
        panelSizer.Add((0, 0), 1, wx.EXPAND)
        panelSizer.Add(accessSizer, 0, wx.TOP, 5)
        mainSizer.Add(panelSizer, (2, 3), (1, 1), wx.ALL|wx.EXPAND, 10)
        redLabel = wx.StaticText(self.mainPanel, -1, "Red")
        rgbGridSizer.Add(redLabel, 0)
        greenLabel = wx.StaticText(self.mainPanel, -1, "Green")
        rgbGridSizer.Add(greenLabel, 0)
        blueLabel = wx.StaticText(self.mainPanel, -1, "Blue")
        rgbGridSizer.Add(blueLabel, 0)
        rgbGridSizer.Add(self.redSpin, 0, wx.EXPAND)
        rgbGridSizer.Add(self.greenSpin, 0, wx.EXPAND)
        rgbGridSizer.Add(self.blueSpin, 0, wx.EXPAND)
        rgbValueSizer.Add(rgbGridSizer, 1, 0, 0)
        mainSizer.Add(rgbValueSizer, (3, 0), (1, 1), wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.EXPAND, 10)
        hueLabel = wx.StaticText(self.mainPanel, -1, "Hue")
        hsvGridSizer.Add(hueLabel, 0)
        saturationLabel = wx.StaticText(self.mainPanel, -1, "Saturation")
        hsvGridSizer.Add(saturationLabel, 0)
        brightnessLabel = wx.StaticText(self.mainPanel, -1, "Brightness")
        hsvGridSizer.Add(brightnessLabel, 0)
        hsvGridSizer.Add(self.hueSpin, 0, wx.EXPAND)
        hsvGridSizer.Add(self.saturationSpin, 0, wx.EXPAND)
        hsvGridSizer.Add(self.brightnessSpin, 0, wx.EXPAND)
        hsvValueSizer.Add(hsvGridSizer, 1, wx.EXPAND)
        mainSizer.Add(hsvValueSizer, (3, 1), (1, 1), wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.EXPAND, 10)
        #alphaLabel = wx.StaticText(self.mainPanel, -1, "Alpha")
        #alphaGridSizer.Add(alphaLabel, 0)
        #alphaGridSizer.Add(self.alphaSpin, 0, wx.EXPAND|wx.TOP, 10)
        #alphaValueSizer.Add(alphaGridSizer, 1, wx.EXPAND)
        #mainSizer.Add(alphaValueSizer, (3, 2), (1, 1), wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.EXPAND, 10)
        buttonSizer.Add(self.okButton, 0, wx.BOTTOM, 3)
        buttonSizer.Add(self.cancelButton, 0)
        mainSizer.Add(buttonSizer, (3, 3), (1, 1), wx.ALIGN_CENTER|wx.LEFT|wx.RIGHT, 5)

        self.mainPanel.SetAutoLayout(True)
        self.mainPanel.SetSizer(mainSizer)
        mainSizer.Fit(self.mainPanel)
        mainSizer.SetSizeHints(self.mainPanel)

        if self.GetWindowStyleFlag() & CCD_SHOW_ALPHA == 0:
            mainSizer.Hide(self.showAlpha)
            mainSizer.Hide(alphaSizer)
            mainSizer.Hide(alphaValueSizer)
        
        dialogSizer.Add(self.mainPanel, 1, wx.EXPAND)
        self.SetAutoLayout(True)
        self.SetSizer(dialogSizer)
        dialogSizer.Fit(self)
        dialogSizer.SetSizeHints(self)
        self.Layout()

        self.mainSizer = mainSizer
        self.dialogSizer = dialogSizer
        #self.alphaSizers = [alphaSizer, alphaValueSizer]
        

    def InitDialog(self):
        """ Initialize the L{CubeColourDialog}. """

        hsvRect = self.hsvBitmap.GetClientRect()
        self._centre = wx.Point(hsvRect.x + hsvRect.width/2, hsvRect.y + hsvRect.height/2)

        self._redLen = Distance(Vertex, Top)
        self._greenLen = Distance(Vertex, Left)
        self._blueLen = Distance(Vertex, Right)

        self.CalcSlopes()
        self.CalcCuboid()
        self.CalcRects()

        self.SetSpinVals()

        self._initOver = True
        wx.CallAfter(self.Refresh)
                        

    def CalcSlopes(self):
        """ Calculates the line slopes in the RGB colour cube. """

        self._lines = {RED: LineDescription(), GREEN: LineDescription(), BLUE: LineDescription}
        
        self._lines[RED].slope = Slope(Top, Vertex)
        self._lines[GREEN].slope = Slope(Left, Vertex)
        self._lines[BLUE].slope = Slope(Right, Vertex)

        for i in xrange(3):
            self._lines[i].x = Vertex.x
            self._lines[i].y = Vertex.y
            self._lines[i].c = FindC(self._lines[i])


    def CalcCuboid(self):
        """ Calculates the RGB colour cube vertices. """

        rLen = (self._colour.r*self._redLen)/255.0
        gLen = (self._colour.g*self._greenLen)/255.0
        bLen = (self._colour.b*self._blueLen)/255.0

        lines = [LineDescription() for i in xrange(12)]
        self._cuboid = [None]*8

        self._cuboid[0] = Vertex
        self._cuboid[1] = PointOnLine(Vertex, Top, int(rLen), self._redLen)
        self._cuboid[3] = PointOnLine(Vertex, Left, int(gLen), self._greenLen)
        self._cuboid[7] = PointOnLine(Vertex, Right, int(bLen), self._blueLen)

        lines[0] = self._lines[RED]
        lines[1] = self._lines[GREEN]
        lines[2] = self._lines[BLUE]

        lines[3].slope = self._lines[GREEN].slope
        lines[3].x = self._cuboid[1].x
        lines[3].y = self._cuboid[1].y
        lines[3].c = FindC(lines[3])

        lines[4].slope = self._lines[RED].slope
        lines[4].x = self._cuboid[3].x
        lines[4].y = self._cuboid[3].y
        lines[4].c = FindC(lines[4])

        lines[5].slope = self._lines[BLUE].slope
        lines[5].x = self._cuboid[3].x
        lines[5].y = self._cuboid[3].y
        lines[5].c = FindC(lines[5])

        lines[6].slope = self._lines[GREEN].slope
        lines[6].x = self._cuboid[7].x
        lines[6].y = self._cuboid[7].y
        lines[6].c = FindC(lines[6])

        lines[10].slope = self._lines[BLUE].slope
        lines[10].x = self._cuboid[1].x
        lines[10].y = self._cuboid[1].y
        lines[10].c = FindC(lines[10])

        lines[11].slope = self._lines[RED].slope
        lines[11].x = self._cuboid[7].x
        lines[11].y = self._cuboid[7].y
        lines[11].c = FindC(lines[11])

        self._cuboid[2] = Intersection(lines[3], lines[4])
        self._cuboid[4] = Intersection(lines[5], lines[6])
        self._cuboid[6] = Intersection(lines[10], lines[11])

        lines[7].slope = self._lines[RED].slope
        lines[7].x = self._cuboid[4].x
        lines[7].y = self._cuboid[4].y
        lines[7].c = FindC(lines[7])

        lines[8].slope = self._lines[BLUE].slope
        lines[8].x = self._cuboid[2].x
        lines[8].y = self._cuboid[2].y
        lines[8].c = FindC(lines[8])

        self._cuboid[5] = Intersection(lines[7], lines[8])
                

    def CalcRects(self):
        """ Calculates the brightness control user-selected rect. """

        pt = PtFromAngle(self._colour.h, self._colour.s, self._centre)
        self._currentRect = wx.Rect(pt.x - RECT_WIDTH, pt.y - RECT_WIDTH,
                                    2*RECT_WIDTH, 2*RECT_WIDTH)


    def DrawMarkers(self, dc=None):
        """ Draws the markers for all the controls. """

        if dc is None:
            dc = wx.ClientDC(self)

        self.hsvBitmap.DrawMarkers()
        self.rgbBitmap.DrawMarkers()
        self.brightCtrl.DrawMarkers()
        

    def DrawRGB(self):
        """ Refreshes the RGB colour cube. """

        self.rgbBitmap.Refresh()


    def DrawHSB(self):
        """ Refreshes the HSB colour wheel. """

        self.hsvBitmap.Refresh()
        

    def DrawBright(self):
        """ Refreshes the brightness control. """

        self.brightCtrl.Refresh()


    #def DrawAlpha(self):
        #""" Refreshes the alpha channel control. """

        #self.alphaCtrl.Refresh()        
        
        
    def SetSpinVals(self):
        """ Sets the values for all the spin controls. """

        self.redSpin.SetValue(self._colour.r)
        self.greenSpin.SetValue(self._colour.g)
        self.blueSpin.SetValue(self._colour.b)
        
        self.hueSpin.SetValue(self._colour.h)
        self.saturationSpin.SetValue(self._colour.s)
        self.brightnessSpin.SetValue(self._colour.v)

        #self.alphaSpin.SetValue(self._colour.alpha)        

        self.SetPanelColours()
        #self.SetCodes()
        

    def SetPanelColours(self):
        """ Assigns colours to the colour panels. """

        self.oldColourPanel.RefreshColour(self._oldColour)
        self.newColourPanel.RefreshColour(self._colour)
        

    #def SetCodes(self):
        #""" Sets the HTML/MS Access codes (if any) in the text controls. """

        #colour = rgb2html(self._colour)
        #self.htmlCode.SetValue(colour)
        #self.htmlCode.Refresh()

        #if colour in HTMLCodes:
        #    colourName, access, webSafe = HTMLCodes[colour]
        #    self.webSafe.SetValue(webSafe)
        #    self.accessCode.SetValue(access)
        #    self.htmlName.SetValue(colourName)
        #else:
        #    self.webSafe.SetValue("")
        #    self.accessCode.SetValue("")
        #    self.htmlName.SetValue("")
        
        
    def OnCloseWindow(self, event):
        """ User canceled the dialog. """

        self.EndModal(wx.ID_CANCEL)


    def OnKeyUp(self, event):

        if event.GetKeyCode() == wx.WXK_ESCAPE:
            self.EndModal(wx.ID_CANCEL)

        event.Skip()
        

    def ShowModal(self):
        """ Overridden wx.Dialog.ShowModal. """

        return wx.Dialog.ShowModal(self)


    def SetWindowStyleFlag(self, style):
        """ Sets the L{CubeColourDialog} window style flags. """

        wx.Dialog.SetWindowStyleFlag(self, style)

        show = self.GetWindowStyleFlag() & CCD_SHOW_ALPHA
        self.mainSizer.Show(self.alphaSizers[0], show)
        self.mainSizer.Show(self.alphaSizers[1], show)

        self.mainSizer.Fit(self.mainPanel)
        self.mainSizer.SetSizeHints(self.mainPanel)
        self.mainSizer.Layout()            
        self.dialogSizer.Fit(self)
        self.dialogSizer.SetSizeHints(self)
        self.Layout()

        self.Refresh()
        self.Update()
        
            
    def OnOk(self, event):
        """ Handles the Ok wx.EVT_BUTTON event for L{CubeColourDialog}. """

        self.EndModal(wx.ID_OK)


    def OnCancel(self, event):
        """ Handles the Cancel wx.EVT_BUTTON event for L{CubeColourDialog}. """

        self.OnCloseWindow(event)


    #def OnAddCustom(self, event):

        #self.customColours.AddCustom(self._colour)

  
    #def OnShowAlpha(self, event):
        #""" Shows/hides the alpha channel control in L{CubeColourDialog}. """

        #style = self.GetWindowStyleFlag()
        #show = event.IsChecked()

        #if show:
            #style |= CCD_SHOW_ALPHA
        #else:
            #style &= ~CCD_SHOW_ALPHA

        #self.SetWindowStyleFlag(style)
        

    def OnSpinCtrl(self, event):
        """ Handles the wx.EVT_SPINCTRL event for RGB and HSB colours. """

        obj = event.GetEventObject()
        position = self.spinCtrls.index(obj)
        colourVal = event.GetInt()

        attribute, maxVal = colourAttributes[position], colourMaxValues[position]

        self.AssignColourValue(attribute, colourVal, maxVal, position)


    #def OnAlphaSpin(self, event):
        #""" Handles the wx.EVT_SPINCTRL event for the alpha channel. """

        #colourVal = event.GetInt()
        #originalVal = self._colour.alpha
        #if colourVal != originalVal and self._initOver:
            #if colourVal < 0:
                #colourVal = 0
            #if colourVal > 255:
                #colourVal = 255

            #self._colour.alpha = colourVal
            #self.DrawAlpha()
            

    def AssignColourValue(self, attribute, colourVal, maxVal, position):
        """ Common code to handle spin control changes. """

        originalVal = getattr(self._colour, attribute)
        if colourVal != originalVal and self._initOver:
            
            if colourVal < 0:
                colourVal = 0
            if colourVal > maxVal:
                colourVal = maxVal

            setattr(self._colour, attribute, colourVal)
            if position < 3:
                self._colour.ToHSV()
            else:
                self._colour.ToRGB()

            self.DrawAll()
            

    def DrawAll(self):
        """ Draws all the custom controls after a colour change. """

        if self._initOver and not self._inDrawAll:
            self._inDrawAll = True

            dc1 = wx.ClientDC(self.hsvBitmap)
            self.hsvBitmap.DrawMarkers(dc1)
            
            dc2 = wx.ClientDC(self.rgbBitmap)
            self.rgbBitmap.DrawMarkers(dc2)
            self.rgbBitmap.DrawLines(dc2)

            dc3 = wx.ClientDC(self.brightCtrl)
            self.brightCtrl.DrawMarkers(dc3)

            #dc4 = wx.ClientDC(self.alphaCtrl)
            #self.alphaCtrl.DrawMarkers(dc4)
            
            self.CalcCuboid()
            self.CalcRects()

            self.DrawRGB()
            self.DrawHSB()
            self.DrawBright()
            #self.DrawAlpha()
            
            self.SetSpinVals()
            self._inDrawAll = False


    def GetColourData(self):
        """ Returns a wxPython compatible wx.ColourData. """

        self._colourData.SetColour(self._colour.GetPyColour())
        return self._colourData


    def GetRGBAColour(self):
        """ Returns a 4-elements tuple of red, green, blue, alpha components. """

        return (self._colour.r, self._colour.g, self._colour.b, self._colour.alpha)

    
    def GetHSVAColour(self):
        """ Returns a 4-elements tuple of hue, saturation, brightness, alpha components. """

        return (self._colour.h, self._colour.s, self._colour.v, self._colour.alpha)
