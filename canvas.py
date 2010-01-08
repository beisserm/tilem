import wx
import images
import os
import stat

import numpy
import math

from utils.enthoughtSizer import FlowSizer

# Standard 'pixel' size is 8x8
PIXEL_ZOOM = 8
zoomSelections = ['50%', '75%', '100%', '125%', '150%', '175%', '200%', '400%', '600%', '800%']
zoomMapping = { '50%':(4, 4),    '75%':(6, 6),   '100%':(8, 8),   '125%':(10, 10), '150%':(12, 12), 
               '175%':(14, 14), '200%':(16, 16), '400%':(32, 32), '600%':(48,48),  '800%':(64, 64)}

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
    def __init__(self, prnt, fileStr=None, fileSize=None):
	'''
	Constructor
	@param fileStr
	         The name of the file to open. Only used when opening an
		 existing file.
	@param fileSize
		 The size (in bytes) of a new file to create. Only used when
		 creating a new file.
	'''
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

	self.canvas = ScrolledCanvas(self, fileStr=fileStr, fileSize=fileSize)	

	vbox.Add(self.canvas, 1, wx.EXPAND)		
	vbox.Add(self.toolBar, 0, wx.EXPAND)

	self.SetSizer(vbox)
	self.Show(True)
	    
    def OnDecode(self, evt):
	selection = evt.GetString()
	self.canvas.UpdateBuffer(selection)

    def OnZoom(self, evt):
	zoom = evt.GetString()
	self.canvas.SetZoom(zoomMapping[zoom])

#####
# Passthrough functions
#####

    def SetCanvasSize(self, rows, columns):
	'''
	Passthrough function to set the number of rows and columns that should
	be in the viewable area. 
	'''
	self.canvas.SetCanvasSize(rows, columns)
    
    def GetCanvasSize(self):
	return self.canvas.GetCanvasSize()
    
#double a[2][4] = { { 1, 2, 3, 4 },
#                   { 5, 6, 7, 8 } };

RGB_LENGTH = 3
class ScrolledCanvas(wx.ScrolledWindow):	
    """

    """	
    def __init__(self, parent, id = -1, size = wx.DefaultSize, fileStr = None, fileSize=None):
	wx.ScrolledWindow.__init__(self, parent, id, (0, 0), size=size, style=wx.SUNKEN_BORDER)	

	# filesize in bytes
	self.fileSize = fileSize
	
	self.columns = 5
	self.rows = 16
	
	# This is in 'logical units', that is the desired tile size is w x h.
	# The actual size on the screen is dependant on the zoom level
	self.tileWidth = 8
	self.tileHeight = 10
	
	# The working copy of the pixels in our current bitmap, adjusted for 
	# the current bpp. Visually, the array is stored in 3D (x, y, z) with
	# the width of the sprite being x, the height y, and being stored in
	# the z axis. i.e., Each entry in the z-axis holds the tile (sprite) 
	# with the current size / shape as specified by the user. The index
	# into the x-y array holds a color value for the xth, yth element
	# in the current tile (sprite). 0, 0 represents the upper left element
	# in the bitmap.
	
	# The working copy of the pixels in our entire rom
	self.pixels = None
	
	# TODO: Should this be 1/2d?
	# This array holds the rom broken up into tiles of sizes specified by
	# the user. Standard sizes of tiles are 8x8 but can be of any size.
	self.tiles = None
	
	# Column matrix of the raw bytes from the rom file. n x 1, where n is
	# the number of bytes in the file.
	self.fileBytes = None
	
	self.fileHandle = None
	
	self.bmp = None
	
	# CanvasFrame (parent ->) TilemFrame (has the ->) PaletteFrame
	self.paletteColors = parent.GetParent().GetPalette()
	
	self.zoom = (8, 8)
	
	self.numTiles = 0
	
	if fileStr:
	    try:
		self.fileHandle = open(fileStr, 'rb')
				
		fileStats = os.stat(fileStr)
		self.fileSize = fileStats[stat.ST_SIZE]
		
		# Read a file one byte per element into a column array. We read
		# it little endian, (right most bit being the LSB).
		self.bytesArray = numpy.fromfile(self.fileHandle, dtype=numpy.uint8)
		#print self.bytesArray
		self.bmp = self.CreateIndexedBitmap(self.bytesArray)
	    except IOError:
		print 'Unable to open file: ', fileStr
	else:
	    #Todo: Change to actual filesize
	    empty = numpy.zeros(shape=(1,1), dtype=numpy.uint8)
	    rgbArray2 = numpy.array(rgbArray, dtype=numpy.uint8).reshape(width, height, 3)
	    bmp = wx.EmptyBitmap(width, height, 24)
	    bmp.CopyFromBuffer(rgbArray2.tostring(), wx.BitmapBufferFormat_RGB)	    
	    bmp = wx.EmptyBitmap(1, 1, 24)
	    image = bmp.ConvertToImage()
	    image.Rescale(1 * 8, 1 * 8)
	    self.bmp = image.ConvertToBitmap()	    

	self.lines = []	

	self.maxWidth  = 1000
	self.maxHeight = 1000
	self.x = self.y = 0
	self.curLine = []
	self.drawing = False

	self.SetBackgroundColour("GREEN")
	self.SetCursor(wx.StockCursor(wx.CURSOR_PENCIL))
	#self.bmp = self.bitmapData
	#bmp = images.Test2.GetBitmap()
	#mask = wx.Mask(bmp, wx.BLUE)
	#bmp.SetMask(mask)
	#self.bmp = bmp

	self.SetVirtualSize((self.maxWidth, self.maxHeight))
	self.SetScrollRate(20,20)

	#if BUFFERED:
	# Initialize the buffer bitmap. No real DC is needed at this point.
	self.buffer = wx.EmptyBitmap(self.maxWidth, self.maxHeight)
	dc = wx.BufferedDC(None, self.buffer)
	#dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
	dc.Clear()
	self.DoDrawing(dc)

	self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftButtonEvent)
	self.Bind(wx.EVT_LEFT_UP, self.OnLeftButtonEvent)
	self.Bind(wx.EVT_MOTION, self.OnLeftButtonEvent)
	self.Bind(wx.EVT_PAINT, self.OnPaint)

	
    def CreateIndexedBitmap(self, npArray, bpp=8):
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
	user and represents the desired tile (sprite) size.
	
	NOTE: NumPy uses reversed column-row ordering compared to wxPython, 
	so we generate images using height, width, not width, height 
	coordinates. We also assume 'uint8' data type for image data in RGB
	format. 
	
	Taken from: http://wiki.wxpython.org/index.cgi/WorkingWithImages	
	
	@param npArray
	         A numpy byte array of the file
	@param bpp (int)
	         The desired bpp's of the bitmap
	""" 
	# Create column vector of bytes, so when we unpack a byte we will have 
	# a nice (n x 8) vector to work with where each element is a single 
	# bit. This allows us to decode arbitrary bits per pixel by 
	# having a single row be the number of bits needed for a single 
	# pixel	
	tempBits = numpy.unpackbits(npArray)
	tempBits2 = numpy.reshape(tempBits, (math.ceil(tempBits.size / bpp), bpp))
	reversedOrder = numpy.packbits(tempBits2, axis=-1)
	shiftedBits = None
	
	if bpp == 1:
	    shiftedBits = numpy.right_shift(reversedOrder, 7)
	elif bpp == 2:
	    shiftedBits = numpy.right_shift(reversedOrder, 6)
	elif bpp == 3:
	    shiftedBits = numpy.right_shift(reversedOrder, 5)
	elif bpp == 4:
	    shiftedBits = numpy.right_shift(reversedOrder, 4)
	elif bpp == 8:
	    shiftedBits = reversedOrder
	
	# Get the actual entry then lookup the entry in the palette table
	#rgbArray = numpy.fromfunction(wtf, size)
	self.paletteColors = self.GetParent().GetParent().GetPalette()

	# Copy the corresponding color entry into a new array	
	rgbArray = list(map(lambda x: self.paletteColors[x], reversedOrder))
	
	logicalWidth, logicalHeight = self._calcLogicalBmpSize(len(rgbArray))
	print 'logicalWidth: ', logicalWidth, ' logicalHeight: ', logicalHeight
	displayLength = logicalWidth * logicalHeight
	print displayLength
	print rgbArray[:displayLength]
	#rgbArray2[i, j, 0] is the red component of the i, j pixel
	#rgbArray2[i, j, 1] is the green component of the i, j pixel
	#rgbArray2[i, j, 2] is the blue component of the i, j pixel
	
	rgbArray2 = numpy.array(rgbArray[:displayLength], dtype=numpy.uint8).reshape(logicalWidth, logicalHeight, 3)
	print rgbArray2
	
	bmp = wx.EmptyBitmap(logicalWidth, logicalHeight, 24)
	temp = numpy.array_split(rgbArray2, self.numTiles, axis=1)
	print list(temp)
	ordered = numpy.hstack(list(temp))
	ordered = ordered.flatten()
	ordered = ordered.reshape(logicalWidth, logicalHeight, 3)
	
	bmp.CopyFromBuffer(ordered.tostring(), wx.BitmapBufferFormat_RGB)

	#bmp = ordered.reshape(logicalSize[0], logicalSize[1], 3)
	#foo = numpy.arange(128).reshape(16,8)
	#temp = numpy.array_split(foo, 2)
	#correct = numpy.hstack((temp[0], temp[1]))
	#correct.flatten()
	#correct.reshape(16,8)
	
        image = bmp.ConvertToImage()
        image.Rescale(logicalWidth * 8, logicalHeight * 8)
	bmp = image.ConvertToBitmap()
	
	return bmp

    def ChangeIndexedImageBpp(self, bpp=1):
	pass
	
    def getWidth(self):
	return self.maxWidth

    def getHeight(self):
	return self.maxHeight

    def SetZoom(self, zoomSize):
	'''
	@param zoomSize
	         tuple (width, height) specifying the size of an indivual pixel
	'''
	self.zoom = zoomSize
	image = self.bmp.ConvertToImage()
        image.Rescale(zoomSize[0] * 2, 19 * zoomSize[1])
	self.bmp = image.ConvertToBitmap()
	
	self.buffer = wx.EmptyBitmap(self.maxWidth, self.maxHeight)
	dc = wx.BufferedDC(wx.ClientDC(self), self.buffer)
	dc.Clear()
	#self.DoDrawing(dc)
	#self.buffer = wx.EmptyBitmap(2, 19, 24 )
	#dc = wx.BufferedDC(wx.ClientDC(self), self.buffer)
	#dc.Clear()
	dc.DrawBitmap(self.bmp, 0, 0, False)

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

    def DoDrawing(self, dc):
	#dc.BeginDrawing()

	#dc.SetPen(wx.Pen('RED'))
	#dc.DrawRectangle(5, 5, 50, 50)

	#dc.SetBrush(wx.LIGHT_GREY_BRUSH)
	#dc.SetPen(wx.Pen('BLUE', 4))
	#dc.DrawRectangle(15, 15, 50, 50)

	#dc.SetPen(wx.GREEN_PEN)
	#dc.DrawSpline(lst+[(100,100)])

	dc.DrawBitmap(self.bmp, 0, 0, False)

	#dc.SetPen(wx.TRANSPARENT_PEN)
	#dc.SetBrush(wx.BLUE_BRUSH)
	#dc.DrawRectangle(50,500, 50,50)
	#dc.DrawRectangle(100,500, 50,50)

	#dc.SetPen(wx.Pen('RED'))
	#dc.DrawEllipticArc(200,500, 50,75, 0, 90)

	#if not printing:
	    ## This has troubles when used on a print preview in wxGTK,
	    ## probably something to do with the pen styles and the scaling
	    ## it does...
	    #y = 20

	    #for style in [wx.DOT, wx.LONG_DASH, wx.SHORT_DASH, wx.DOT_DASH, wx.USER_DASH]:
		#pen = wx.Pen("DARK ORCHID", 1, style)
		#if style == wx.USER_DASH:
		    #pen.SetCap(wx.CAP_BUTT)
		    #pen.SetDashes([1,2])
		    #pen.SetColour("RED")
		#dc.SetPen(pen)
		#dc.DrawLine(300,y, 400,y)
		#y = y + 10

	#dc.SetBrush(wx.TRANSPARENT_BRUSH)
	#dc.SetPen(wx.Pen(wx.Colour(0xFF, 0x20, 0xFF), 1, wx.SOLID))
	#dc.DrawRectangle(450,50,  100,100)
	#old_pen = dc.GetPen()
	#new_pen = wx.Pen("BLACK", 5)
	#dc.SetPen(new_pen)
	#dc.DrawRectangle(470,70,  60,60)
	#dc.SetPen(old_pen)
	#dc.DrawRectangle(490,90, 20,20)

	#dc.GradientFillLinear((20, 260, 50, 50),
                              #"red", "blue")
	#dc.GradientFillConcentric((20, 325, 50, 50),
                                  #"red", "blue", (25,25))
	#self.DrawSavedLines(dc)
	#dc.EndDrawing()

    def SetCanvasSize(self, rows, columns):
	'''
	Updates the number of rows/columns that should be displayed on the 
	canvas (DC)
	@param rows
	         int (1-128)		
	@param columns
	         int (1-128)	
	'''
	self.rows = rows
	self.columns = columns
	#Todo redraw canvas
	
    def GetCanvasSize(self):
	return [self.rows, self.columns]
    
    def SetFileSize(self, byteSize=1):
	'''
	Sets the filesize. Only used when making a 'New' File.
	@param byteSize
	         Size of file in bytes
	'''
	self.fileSize = byteSize
	
    def UpateBuffer(self, encodingStr):
	pass
    
    def DrawTile(self):
	pass

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

#####
# Private Methods
#####

    def _calcLogicalBmpSize(self, length):
	'''
	Figures out the logical size of the bitmap to be displayed. This is not
	the entire file and it is not adjusted for zoom/displaying purposes
	@param length
	         int length of the current working array
	@return Tuple containing the (width, height) of the bitmap to be
	        displayed
	'''
	fullBmpWidth = self.tileWidth * self.columns
	fullBmpHeight = self.tileHeight * self.rows
	fullBmpSize = fullBmpWidth * fullBmpHeight
	tileSize = self.tileWidth * self.tileHeight	
	logicalBmpSize = [0, 0]
	
	# FIXME: Currently we chop off any partial rows
	# Do we have a full screen of tiles?
	if length > fullBmpSize:
	    logicalBmpSize = [fullBmpWidth, fullBmpHeight]
	    self.numTiles = int(fullBmpSize // tileSize)
	    print 'tiles: ', self.numTiles
	else:
	    # Ignore partial tiles
	    self.numTiles = int(length // tileSize)
	    completeRows = int(self.numTiles // self.columns)
	    if completeRows > 0:
		logicalBmpHeight = completeRows * self.tileHeight
		logicalBmpSize = [fullBmpWidth, logicalBmpHeight]
		self.rows = completeRows
		self.numTiles =  completeRows * self.columns
		print 'tiles: ', self.numTiles
	    else:
		self.rows = 0
	    
	return logicalBmpSize
	
    def _createTiles(self, length):
	'''
	foo = numpy.arange(128).reshape(16,8)
	temp = numpy.array_split(foo, 2)
	correct = numpy.hstack((temp[0], temp[1]))
	correct.flatten()
	correct.reshape(16,8)	
	'''
	tileSize = self.tileWidth * self.tileHeight
	numTiles = 0
		
	#FIXME! Chop off partial tiles!
	numTiles = length // tileSize

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

