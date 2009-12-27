import wx
import images
import os
import threading
import numpy

from dialogs.processFileDialog import ProcessFileDialog



from utils.bitbuffer import BitBuffer
from utils.enthoughtSizer import FlowSizer

zoomSelections = ['50%', '75%', '100%', '125%', '150%', '200%', '400%', '800%']

decoderSelections = ['1bpp linear', '1bpp linear, reverse-order', '1bpp planar',
                     '2bpp linear', '2bpp linear, reverse-order', '2bpp planar',
                     '3bpp planar',
                     '4bpp linear', '4bpp linear, reverse-order', '4bpp planar',
                     '5bpp planar',
                     '6bpp planar',
                     '7bpp planar',
                     '8bpp linear', '8bpp planar',
                     '15bpp RGB (555)', '15bpp BGR (555)', 
                     '16bpp RGB (565)', '16bpp BGR (565)', '16bpp ARGB (1555)', 
                     '16bpp ABGR (1555)', '16bpp RGBA (5551)', '16bpp BGRA (5551)',
                     '24bpp RGB (888)', '24bpp BGR (888)',
                     '32bpp ARGB (8888)', '32bpp ABGR (8888)', 
                     '32bpp RGBA (8888)', '32bpp BGRA (8888)']

#---------------------------------------------------------------------------
class CanvasFrame(wx.MDIChildFrame):
    """
    A simple frame that has a drawing area and its own toolbar
    TODO: Use a sizer for comboBoxes, add buttons?
    """
    def __init__(self, prnt, fileStr=None): 
	wx.MDIChildFrame.__init__(self, parent=prnt)

	vbox = wx.BoxSizer(wx.VERTICAL)

	self.toolBar = wx.ToolBar(id=-1, name='toolBar1', parent=self, pos=wx.DefaultPosition,
                                  size=wx.Size(455, 28), style=wx.TB_HORIZONTAL | wx.NO_BORDER | wx.TB_BOTTOM )		    

	self.toolBar.zoomSelect = wx.ComboBox(choices=zoomSelections,
                                         id=-1, name='zoom',
                                         parent=self.toolBar, pos=wx.Point(2, 1), size=wx.Size(70, 20),
                                         style=wx.CB_READONLY, value='100%')
	self.Bind(wx.EVT_COMBOBOX, self.OnZoom, self.toolBar.zoomSelect)			

	self.toolBar.decoderSelect = wx.ComboBox(choices=decoderSelections,
                                            id=-1, name='decoder',
                                            parent=self.toolBar, pos=wx.Point(90, 1), size=wx.Size(180, 20),
                                            style=wx.CB_READONLY, value=decoderSelections[0])
	self.Bind(wx.EVT_COMBOBOX, self.OnDecode, self.toolBar.decoderSelect)			

	self.toolBar.Realize()		
	self.toolBar.Raise()

	self.canvas = ScrolledCanvas(self, fileStr=fileStr)	

	vbox.Add(self.canvas, 1, wx.EXPAND)		
	vbox.Add(self.toolBar, 0, wx.EXPAND)

	self.SetSizer(vbox)
	self.Show(True)
	    
    def OnDecode(self, evt):
	selection = evt.GetString()
	self.canvas.UpdateBuffer(selection)

    def OnZoom(self, evt):
	pass

    
#double a[2][4] = { { 1, 2, 3, 4 },
#                   { 5, 6, 7, 8 } };

class ScrolledCanvas(wx.ScrolledWindow):	
    """

    """	
    def __init__(self, parent, id = -1, size = wx.DefaultSize, fileStr = None):
	wx.ScrolledWindow.__init__(self, parent, id, (0, 0), size=size, style=wx.SUNKEN_BORDER)	

	self.pixels = None
	self.fileSize = None # filesize in bytes
	self.fileHandle = None
	
	# CanvasFrame (parent ->) TilemFrame (has the ->) PaletteFrame
	self.paletteColors = parent.GetParent().GetPalette()
	
	if fileStr:
	    try:
		self.fileHandle = open(fileStr, 'rb')
		fileStats = os.stat(fileStr)
		self.fileSize = fileStats[ST_SIZE]
		
		# Read a file one byte per element into a column array. We read
		# it little endian, (left most bit being the LSB). Because it's 
		# a column vector when we unpack a byte we will have a nice 
		# (n x 8) vector to work with where each element is a single 
		# bit. This allows us to decode arbitrary bits per pixel by 
		# having a single row be the number of bits needed for a single 
		# pixel
		bytesArray = numpy.fromfile(self.fileHandle, dtype=numpy.uint8)
		tempPixels = numpy.unpackbits(bytesArray)
		self.pixels = numpy.reshape(tempPixels, tempPixels.size, 1)
	    except IOError:
		print 'Unable to open file: ', fileStr
	else:
	    #Todo: Change to actual filesize
	    self.pixels = numpy.zeros(shape=(1,1))

	self.lines = []	

	self.maxWidth  = 1000
	self.maxHeight = 1000
	self.x = self.y = 0
	self.curLine = []
	self.drawing = False

	self.SetBackgroundColour("WHITE")
	self.SetCursor(wx.StockCursor(wx.CURSOR_PENCIL))
	bmp = images.Test2.GetBitmap()
	mask = wx.Mask(bmp, wx.BLUE)
	bmp.SetMask(mask)
	self.bmp = bmp

	self.SetVirtualSize((self.maxWidth, self.maxHeight))
	self.SetScrollRate(20,20)

	#if BUFFERED:
	# Initialize the buffer bitmap. No real DC is needed at this point.
	self.buffer = wx.EmptyBitmap(self.maxWidth, self.maxHeight)
	dc = wx.BufferedDC(None, self.buffer)
	dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
	dc.Clear()
	self.DoDrawing(dc)

	self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftButtonEvent)
	self.Bind(wx.EVT_LEFT_UP, self.OnLeftButtonEvent)
	self.Bind(wx.EVT_MOTION, self.OnLeftButtonEvent)
	self.Bind(wx.EVT_PAINT, self.OnPaint)


	
    def GetIndexedBitmap(self, npArray, width=8, height=8):
	"""
	Creates a bitmap image of the specified size from a numpy array. Each 
	entry in the array is assumed to be the index into the palette of the
	color that is suppose to be displayed.
	
	Example: Assume an 8 bit per pixel palette (EGA) color palette
	(http://en.wikipedia.org/wiki/Enhanced_Graphics_Adapter) 
	and that we wish to decode a ROM (array) 1bpp linearly. Given an
	array of ex[1 0 1 1] (notice the number of bits in the array correspond
	to our decoding scheme, i.e. 1bpp = 1 bit per entry in the array), then:
	ex[0] -> RGB: 0x0000AA
	ex[1] -> RGB: 0x000000
	ex[2] -> RGB: 0x0000AA
	ex[3] -> RGB: 0x0000AA
	
	so our bitmap would look like:
	(Blue) (Black) (Blue) (Blue) 
	
	The width and height of the bitmap can be arbitrarily chosen by the
	user and represent the desired tile (sprite) size.
	
	NOTE: NumPy uses reversed column-row ordering compared to wxPython, 
	so we generate images using height, width, not width, height 
	coordinates. We also assume 'uint8' data type for image data in RGB
	format. 
	
	Taken from: http://wiki.wxpython.org/index.cgi/WorkingWithImages	
	
	@param npArray
	         A 1bpp array of the file
	@param width (int)
	         The width of the desired bitmap in pixels
	@param height (int)
	         The height of the desired bitmaps in pixels
	""" 
	# Get the actual entry then lookup the entry in the palette table
	rgbArray = fromfunction(lambda x,y: self.paletteColors(npArray[x,y]), npArray.shape)
	array = numpy.zeros( (height, width, 3),'uint8')
	array[:,:,] = colour
	image = wx.EmptyImage(width, height)
	image.SetData(array.tostring())
	return image.ConvertToBitmap() # wx.BitmapFromImage(image)	

    def getWidth(self):
	return self.maxWidth

    def getHeight(self):
	return self.maxHeight


    def OnPaint(self, event):
	#if BUFFERED:
	    # Create a buffered paint DC.  It will create the real
	    # wx.PaintDC and then blit the bitmap to it when dc is
	    # deleted.  Since we don't need to draw anything else
	    # here that's all there is to it.
	dc = wx.BufferedPaintDC(self, self.buffer, wx.BUFFER_VIRTUAL_AREA)
	#else:
	    #dc = wx.PaintDC(self)
	    #self.PrepareDC(dc)
	    # since we're not buffering in this case, we have to
	    # paint the whole window, potentially very time consuming.
	    #self.DoDrawing(dc)
	    #parent.toolBar.Raise()


    def DoDrawing(self, dc, printing=False):
	#dc.BeginDrawing()

	dc.SetPen(wx.Pen('RED'))
	dc.DrawRectangle(5, 5, 50, 50)

	dc.SetBrush(wx.LIGHT_GREY_BRUSH)
	dc.SetPen(wx.Pen('BLUE', 4))
	dc.DrawRectangle(15, 15, 50, 50)

	dc.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL, wx.NORMAL))
	dc.SetTextForeground(wx.Colour(0xFF, 0x20, 0xFF))
	te = dc.GetTextExtent("Hello World")
	dc.DrawText("Hello World", 60, 65)

	dc.SetPen(wx.Pen('VIOLET', 4))
	dc.DrawLine(5, 65+te[1], 60+te[0], 65+te[1])

	lst = [(100,110), (150,110), (150,160), (100,160)]
	dc.DrawLines(lst, -60)
	dc.SetPen(wx.GREY_PEN)
	dc.DrawPolygon(lst, 75)
	dc.SetPen(wx.GREEN_PEN)
	dc.DrawSpline(lst+[(100,100)])

	dc.DrawBitmap(self.bmp, 200, 20, True)
	dc.SetTextForeground(wx.Colour(0, 0xFF, 0x80))
	dc.DrawText("a bitmap", 200, 85)

	#dc.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL, wx.NORMAL))
	#dc.SetTextForeground("BLACK")
	#dc.DrawText("TEST this STRING", 10, 200)
	#print dc.GetFullTextExtent("TEST this STRING")

	font = wx.Font(20, wx.SWISS, wx.NORMAL, wx.NORMAL)
	dc.SetFont(font)
	dc.SetTextForeground(wx.BLACK)

	for a in range(0, 360, 45):
	    dc.DrawRotatedText("Rotated text...", 300, 300, a)

	dc.SetPen(wx.TRANSPARENT_PEN)
	dc.SetBrush(wx.BLUE_BRUSH)
	dc.DrawRectangle(50,500, 50,50)
	dc.DrawRectangle(100,500, 50,50)

	dc.SetPen(wx.Pen('RED'))
	dc.DrawEllipticArc(200,500, 50,75, 0, 90)

	if not printing:
	    # This has troubles when used on a print preview in wxGTK,
	    # probably something to do with the pen styles and the scaling
	    # it does...
	    y = 20

	    for style in [wx.DOT, wx.LONG_DASH, wx.SHORT_DASH, wx.DOT_DASH, wx.USER_DASH]:
		pen = wx.Pen("DARK ORCHID", 1, style)
		if style == wx.USER_DASH:
		    pen.SetCap(wx.CAP_BUTT)
		    pen.SetDashes([1,2])
		    pen.SetColour("RED")
		dc.SetPen(pen)
		dc.DrawLine(300,y, 400,y)
		y = y + 10

	dc.SetBrush(wx.TRANSPARENT_BRUSH)
	dc.SetPen(wx.Pen(wx.Colour(0xFF, 0x20, 0xFF), 1, wx.SOLID))
	dc.DrawRectangle(450,50,  100,100)
	old_pen = dc.GetPen()
	new_pen = wx.Pen("BLACK", 5)
	dc.SetPen(new_pen)
	dc.DrawRectangle(470,70,  60,60)
	dc.SetPen(old_pen)
	dc.DrawRectangle(490,90, 20,20)

	dc.GradientFillLinear((20, 260, 50, 50),
                              "red", "blue")
	dc.GradientFillConcentric((20, 325, 50, 50),
                                  "red", "blue", (25,25))
	self.DrawSavedLines(dc)
	#dc.EndDrawing()

		    
    
    def UpateBuffer(self, encodingStr):
	pass
    
    def DrawTile(self):
	pass
			    
		    
    def DrawSavedLines(self, dc):
	dc.SetPen(wx.Pen('MEDIUM FOREST GREEN', 4))

	for line in self.lines:
	    for coords in line:
		apply(dc.DrawLine, coords)


    def SetXY(self, event):
	self.x, self.y = self.ConvertEventCoords(event)

    def ConvertEventCoords(self, event):
	newpos = self.CalcUnscrolledPosition(event.GetX(), event.GetY())
	return newpos

    def OnLeftButtonEvent(self, event):
	if event.LeftDown():
	    self.SetFocus()
	    self.SetXY(event)
	    self.curLine = []
	    self.CaptureMouse()
	    self.drawing = True

	elif event.Dragging() and self.drawing:
	    #if BUFFERED:
		    # If doing buffered drawing we'll just update the
		    # buffer here and then refresh that portion of the
		    # window, then that portion of the buffer will be
		    # redrawn in the EVT_PAINT handler.
	    dc = wx.BufferedDC(None, self.buffer)
	    #else:
		    # otherwise we'll draw directly to a wx.ClientDC
		    #dc = wx.ClientDC(self)
		    #self.PrepareDC(dc)

	    dc.SetPen(wx.Pen('MEDIUM FOREST GREEN', 4))
	    coords = (self.x, self.y) + self.ConvertEventCoords(event)
	    self.curLine.append(coords)
	    dc.DrawLine(*coords)
	    self.SetXY(event)

	    #if BUFFERED:
	    # figure out what part of the window to refresh
	    x1,y1, x2,y2 = dc.GetBoundingBox()
	    x1,y1 = self.CalcScrolledPosition(x1, y1)
	    x2,y2 = self.CalcScrolledPosition(x2, y2)
	    # make a rectangle
	    rect = wx.Rect()
	    rect.SetTopLeft((x1,y1))
	    rect.SetBottomRight((x2,y2))
	    rect.Inflate(2,2)
	    # refresh it
	    self.RefreshRect(rect)

	elif event.LeftUp() and self.drawing:
	    self.lines.append(self.curLine)
	    self.curLine = []
	    self.ReleaseMouse()
	    self.drawing = False


# This is an example of what to do for the EVT_MOUSEWHEEL event,
# but since wx.ScrolledWindow does this already it's not
# necessary to do it ourselves. You would need to add an event table 
# entry to __init__() to direct wheelmouse events to this handler.

#	 wheelScroll = 0
#	 def OnWheel(self, evt):
#		 delta = evt.GetWheelDelta()
#		 rot = evt.GetWheelRotation()
#		 linesPer = evt.GetLinesPerAction()
#		 print delta, rot, linesPer
#		 ws = self.wheelScroll
#		 ws = ws + rot
#		 lines = ws / delta
#		 ws = ws - lines * delta
#		 self.wheelScroll = ws
#		 if lines != 0:
#			 lines = lines * linesPer
#			 vsx, vsy = self.GetViewStart()
#			 scrollTo = vsy - lines
#			 self.Scroll(-1, scrollTo)
