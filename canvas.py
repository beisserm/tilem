import images
import math
import numpy
import os
import stat
import thread
import threading
import time
import wx

from utils.enthoughtSizer import FlowSizer
import utils.threadpool

#sers of the package can import individual modules from the package, for example:
#import sound.effects.echo
#This loads the submodule sound.effects.echo. It must be referenced with its full name.
#sound.effects.echo.echofilter(input, output, delay=0.7, atten=4)




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

    def SetCanvasColumns(self, columns):
	'''
	Passthrough setter to set the number of canvas columsn on the
	scrolled canvas.
	@param columns
	         integer (0-128)
	'''
	self.canvas.SetColumns(columns)
	
    def GetCanvasColumns(self):
	return self.canvas.GetColumns()
	
    
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
	
	self.columns = 16
	
	# This is in 'logical units', that is the desired tile size is w x h.
	# The actual size on the screen is dependant on the zoom level
	self.tileWidth = 3
	self.tileHeight = 3
	
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
	
	if fileStr:
	    try:
		self.fileHandle = open(fileStr, 'rb')
				
		fileStats = os.stat(fileStr)
		self.fileSize = fileStats[stat.ST_SIZE]
		#self.testImg = wx.Bitmap(fileStr, wx.BITMAP_TYPE_BMP)
		#print str(self.buff)
		#self.testImg.CopyToBuffer(self.buff, wx.BitmapBufferFormat_RGB32)
		#print map(ord, self.buff)
		
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

	
    def CreateIndexedBitmap(self, npArray, bpp=1):
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
	tempBits = numpy.reshape(tempBits, (math.ceil(tempBits.size / bpp), bpp))
	tempBits = numpy.packbits(tempBits, axis=-1)
	shiftedBits = None
	
	if bpp == 1:
	    shiftedBits = numpy.right_shift(tempBits, 7)
	elif bpp == 2:
	    shiftedBits = numpy.right_shift(tempBits, 6)
	elif bpp == 3:
	    shiftedBits = numpy.right_shift(tempBits, 5)
	elif bpp == 4:
	    shiftedBits = numpy.right_shift(tempBits, 4)
	elif bpp == 8:
	    shiftedBits = tempBits
	
	# Ok, we need to iterate through each entry in our array and get its
	# corresponding color in the palette table. This is potentially very
	# time consuming. A 64MB ROM displayed at 1bpp has 67,108,864 entries.
	# A threadpool is used. (TODO: should we block or not while waiting?)
	start = time.time()
	shiftedBits = self._entryToPaletteColor(shiftedBits)
	elapsed = (time.time() - start)	
	print 'Time: ', elapsed
	
	#rgbArray = numpy.empty(shape = revShape, dtype=numpy.dtype(object)).flatten()
	# rgbArray = numpy.array(theList)
	#for i in range(len(tempBits)):
	    #rgbArray[i] = self.paletteColors[tempBits[i]]
	
	logicalWidth, logicalHeight = self._calcLogicalBmpSize()
	print 'width: ', logicalWidth
	print 'height: ', logicalHeight
	print '!!!!!!!!!!!!!!!!!!!!!!!!'
	#logicalSize = self._calcLogicalBmpSize() # width, height

	#rgbArray2[i, j, 0] is the red component of the i, j pixel
	#rgbArray2[i, j, 1] is the green component of the i, j pixel
	#rgbArray2[i, j, 2] is the blue component of the i, j pixel
	rgbArray2 = numpy.array(shiftedBits, dtype=numpy.uint8).reshape(logicalWidth, logicalHeight, 3)

	# Now the tricky part. Shuffle the tiles so that they display horizontally
	#bmp = ordered.reshape(logicalSize[0], logicalSize[1], 3)
	#foo = numpy.arange(128).reshape(16,8)
	#temp = numpy.array_split(foo, 2)
	#correct = numpy.hstack((temp[0], temp[1]))
	#correct.flatten()
	#correct.reshape(16,8)	
	bmp = wx.EmptyBitmap(logicalWidth, logicalHeight, 24)
	temp = numpy.array_split(rgbArray2, self._calcTiles())
	ordered = numpy.hstack(list(temp)).reshape(logicalWidth, logicalHeight, 3)
	bmp.CopyFromBuffer(ordered.tostring(), wx.BitmapBufferFormat_RGB)

	# And we're done!
        image = bmp.ConvertToImage()
        image.Rescale(logicalWidth * 8, logicalHeight * 8)
	bmp = image.ConvertToBitmap()
	
	return bmp
    
    def _entryToPaletteColor(self, bitEntries):
	'''
	For every element in the specified numpyArray, the corresponding entry
	in the current pallette is looked up and stored in a new numpy Array
	@param bitEntries
	         The raw data adjusted for bpp of the ROM
	'''
	ROW_WIDTH = 1000000
	self.paletteColors = self.GetParent().GetParent().GetPalette()
	bitEntries = bitEntries.flatten()
	unevenEntries = None
	masterEntries = [[]]	
	#rgbArray = numpy.empty(shape = bitEntries.shape, dtype=numpy.dtype(object))
	
	length = len(bitEntries)
	rows = length / ROW_WIDTH
	remainder = length % ROW_WIDTH
	
	# Break up the odd shaped array into a rectangle and its remaining piece
	if length > ROW_WIDTH and remainder != 0:
	    newEndIndex = (length - remainder)
	    bitEntries = numpy.array(bitEntries[:newEndIndex]).reshape(rows, ROW_WIDTH)
	    unevenEntries = bitEntries[-remainder:]
	    #bitEntries = list(wholeEntries)
	    #bitEntries.append(list(unevenEntries))
	    print bitEntries
	else:
	    #print length
	    #print 'rows: ', rows
	    #print 'remainder: ', remainder
	    bitEntries = [list(bitEntries)]

	
	def combineResults(request, result):
	    '''
	    After each thread is finished this closure gets called. It simply
	    adds the list that the thread processed onto the master list.
	    @param request
	             The request id (long) that finished
	    @param result
	             The list that the thread created.
	    '''
	    masterEntries.append(result)
	    
	def processList(data):
	    '''
	    Every thread in the threadpool calls this closure. This is the
	    function that does the actual work of looking up each entry in
	    the 'raw' bpp adjusted numpy array and maps it to a color in the
	    current color palette.
	    @param data
	             List of bytes (already adjusted for bpp) that should be
		     mapped to colors in the color palette.
	    '''
	    result = []
    
	    for i in range(len(data)):
		result.append(self.paletteColors[data[i]])    				
		
	    return result
	
	def handleException(request, exc_info):
	    '''
	    Todo: Actually implement this closure and make it display a dialog 
	          box.
	    '''
	    if not isinstance(exc_info, tuple):
	        # Something is seriously wrong...
		print request
		print exc_info
		raise SystemExit
            print "Exception occured in request #%s: %s" % (request.requestID, exc_info)
	    
	# Figure out how big our poolsize should be. The number of threads is 
	# the number of rows that have our specified length
	poolsize = 20 # magic num
	
	if rows == 0:
	    poolsize = 1
	elif rows < 20:
	    poolsize = rows
	
	# Create a pool of worker threads
	print 'poolsize: ', poolsize
	threadPool = utils.threadpool.ThreadPool(2)	    
	    
	# Build a WorkRequest object for each row of data. Don't forget the
	# remainder!
	
	requests = utils.threadpool.makeRequests(processList, bitEntries, combineResults, None)

	#remainderReq = utils.threadpool.makeRequests(processList, unevenEntries, combineResults, handleException)
	

	# Put the work requests in the queue...
	for req in requests:
	    threadPool.putRequest(req)

	#threadPool.wait()
	#threadPool.putRequest(remainderReq)
	
	
	# TODO: Implement progress bar for this...
	# And wait for the results to arrive in the result queue. This blocks
	# until results for all work requests have arrived.
	begin = time.time()	
	while True:
	    try:
		time.sleep(0.1)
		threadPool.poll()
	    except utils.threadpool.NoResultsPending:
		print "**** No pending results."    
		break
	print 'Loop time', (time.time() - begin)		    
	if threadPool.dismissedWorkers:
	    print "Joining all dismissed worker threads..."
	    threadPool.joinAllDismissedWorkers()
	print 'Dismiss time', (time.time() - begin)	    

	begin = time.time()
	foo = numpy.array(masterEntries, dtype=numpy.dtype(object))
	print 'Creation time', (time.time() - begin)
	#print '#########'
	#print foo
	#print '#########'	
	return foo

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
    
    def SetColumns(self, columns):
	'''
	Updates the number of columns that should be displayed on the canvas
	(DC)
	@param columns
	         int (1-128)
	'''
	self.columns = columns
	# Todo Redraw canvas
    
    def SetFileSize(self, byteSize=1):
	'''
	Sets the filesize. Only used when making a 'New' File.
	@param byteSize
	         Size of file in bytes
	'''
	self.fileSize = byteSize
	
    def GetColumns(self):
	return self.columns
	
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

    def _calcLogicalBmpSize(self):
	'''
	Figures out the logical size of the bitmap to be displayed 
	(that is not adjusted for zoom/displaying purposes)
	@return Tuple containing the (width, height) of the bitmap to be
	        displayed
	'''
	# Just some initial values that make sense (1 tile)
	logicalBmpWidth = 8
	logicalBmpHeight = 8
	
	# Do we have less than 1 row of tiles?
	if self._calcTiles() < self.columns:
	    logicalBmpWidth = self.tileWidth * self._calcTiles()
	    logicalBmpHeight = self.tileHeight
	else:	
	    logicalBmpWidth = self.tileWidth * self.columns
	    logicalBmpHeight = self.fileSize / self.tileWidth # total / width = height
	    
	return (logicalBmpWidth, logicalBmpHeight)
    
    def _calcTiles(self):
	logicalTileSize = self.tileWidth * self.tileHeight
	
	# Do we have any partial tiles?
	if (self.fileSize % logicalTileSize) == 0:
	    return math.floor(self.fileSize // logicalTileSize)   
	else:
	    return math.floor(self.fileSize // logicalTileSize) + 1
	
    def _createTiles(self):
	'''
	foo = numpy.arange(128).reshape(16,8)
	temp = numpy.array_split(foo, 2)
	correct = numpy.hstack((temp[0], temp[1]))
	correct.flatten()
	correct.reshape(16,8)	
	'''
	pass
    
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
