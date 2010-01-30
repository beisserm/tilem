import images
import math
import numpy
import os
import stat
import wx

from threading import Thread
from pubsub import pub

import ToolPanel
import utils.flowSizer as FlowSizer

zoomSelections = ['0%', '25%', '50%', '75%', '100%', '125%', '150%', '175%', '200%']
#, '225%', 
#                  '250%', '275%', '300%', '350%', '400%', '450%', '500%', 
#                  '550%', '600%']

zoomMapping = { '0%':1, '25%':2, '50%':4,   '75%':6,  '100%':8,  '125%':10, '150%':12, 
                '175%':14, '200%':16}

#, '225%':18, '250%':20, '275%':22,
#                 '300%':24, '350%':28, '400%':32, '450%':36, '500%':40,
#                 '550%':44, '600%':48}

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
	"""
	Constructor
	@param fileStr
	         The name of the file to open. Only used when opening an
		 existing file.
	@param fileSize
		 The size (in bytes) of a new file to create. Only used when
		 creating a new file.
	"""
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

    def OnZoom(self, evt):
	zoom = evt.GetString()
	self.canvas.SetZoom(zoomMapping[zoom])
	self.canvas.DoDrawing()
	self.canvas.Refresh()

    def OnDecode(self, evt):
	selection = evt.GetString()
	if (selection.find(',') == -1) and (selection.find('linear') != -1):
	    #linear
	    bpp = selection[0]
	    self.canvas.SetBpp(bpp)
	    self.canvas.UpdateIndexedBitmap()
	elif (selection.find(',') != -1) and (selection.find('linear') != -1):
	    # linear reveresed order
	    bpp = selection[0]
	    self.canvas.SetBpp(bpp)
	    self.canvas.UpdateIndexedBitmap(reversedOrder = True)
	elif selection.find('planar') != -1:
	    #self.canvas.CreatePlanarBitmap()
	    pass
	else:
	    #self.canvas.CreatedBitmap()
	    pass
	
	self.canvas.DoDrawing()
	self.canvas.Refresh()	

#####
# Passthrough functions
#####

    def SetTileGrid(self, val=False):
	"""
	Passthrough function that turns the tile grid on/off
	"""	
	self.canvas.SetTileGrid(val)
	self.canvas.DoDrawing()
	self.canvas.Refresh()	
	
    def SetPixelGrid(self, val=False):
	"""
	Passthrough function that turns the pixel grid on/off
	"""
	self.canvas.SetPixelGrid(val)
	self.canvas.DoDrawing()
	self.canvas.Refresh()	

    def SetCanvasSize(self, rows, columns):
	"""
	Passthrough function to set the number of rows and columns that should
	be in the viewable area. 
	"""
	self.canvas.SetCanvasSize(rows, columns)
	self.canvas.UpdateIndexedBitmap()
	self.canvas.DoDrawing()
	self.canvas.Refresh()	 
	
    def SetTileSize(self, width, height):
	"""
	Passthrough function to set the width and height of the tile (sprite)
	size
	"""
	self.canvas.SetTileSize(width, height)
	self.canvas.UpdateIndexedBitmap()
	self.canvas.DoDrawing()
	self.canvas.Refresh()	
    
    def GetCanvasSize(self):
	"""
	Passthrough function to ge the current canvas size.
	"""
	return self.canvas.GetCanvasSize()
    
    def GetTileSize(self):
	"""
	Passthrough function to get the current tile size.
	"""
	return self.canvas.GetTileSize()
    
#double a[2][4] = { { 1, 2, 3, 4 },
#                   { 5, 6, 7, 8 } };

#---------------------------------------------------------------------------

class ScrolledCanvas(wx.ScrolledWindow):	
    """

    """	
    def __init__(self, parent, id = -1, size = wx.DefaultSize, fileStr = None, fileSize=None):
	wx.ScrolledWindow.__init__(self, parent, id, (0, 0), size=size, style=wx.SUNKEN_BORDER)	
	
	pub.subscribe(self.OnCanvasArrangementMsg, 'canvasArrangement')
	pub.subscribe(self.OnCanvasShiftMsg, 'canvasShift')
	pub.subscribe(self.OnCanvasToolMsg, 'canvasTool')
	pub.subscribe(self.OnPaletteUpdateMsg, 'paletteUpdate')
	
	# This will only be updated through messaging
	self.paletteColors = []
	pub.subscribe(self.OnPaletteResponseMsg, 'paletteResponse')
	pub.sendMessage('paletteRequest', msg=True)
	
	# filesize in bytes
	self.fileSize = fileSize
	self.fileHandle = None
	
	self.columns = 16
	self.rows = 16
	
	# This is in 'logical units', that is the desired tile size is w x h.
	# The actual size on the screen is dependant on the zoom level
	self.tileWidth = 8
	self.tileHeight = 8
	
	self.bpp = 8
	
	self.beginAddress = 0x00
	self.currentAddress = 0x00	
	self.endAddress = self.bpp * self.tileWidth * self.tileHeight * self.columns * self.rows

	self.tileGrid = False
	self.pixelGrid = False
	
	# How many actual pixels to multiple the logical size of the 
	# pixel/tile/bitmap by. The default value of 8, means that every 
	# logical pixel in the bitmap will be 8x8
	self.zoomConstant = zoomMapping['100%']
	
	# Column matrix of the raw rom file. n x 1, where n is the number of
	# bits in the file.
	self.cachedBits = None

	# We keep track of 2 bitmaps. 1 is the logical 1-1 pixel mapping, and
	# the display incorporates the zoom factor on the image
	self.logicalBmp = None
	self.displayBmp	= None
	
	self.numTiles = 0
	
	if fileStr:
	    try:
		self.fileHandle = open(fileStr, 'rb')
		
		fileStats = os.stat(fileStr)
		self.fileSize = fileStats[stat.ST_SIZE]
		
		# Read a file one byte per element into an array. We read it 
		# little endian, (right most bit being the LSB), but once it's
		# in the buffer we can change it
		bytesArray = numpy.fromfile(self.fileHandle, dtype=numpy.uint8)
		
		# Create column vector of bytes, so when we unpack a byte we will have 
		# a nice (n x 8) vector to work with where each element is a single 
		# bit. 
		unpackedBits = numpy.unpackbits(bytesArray)		
		_shape = (int(math.ceil(unpackedBits.size)), 1)
		
		# Decode into 1 bits per pixel.
		unpackedBits = unpackedBits.reshape(_shape)
		packedBits = numpy.packbits(unpackedBits, axis=1)
		shiftedBits = numpy.right_shift(packedBits, 7)
		
		# We cache the bits here in 1bpp form so that future operations
		# (with the current encoding scheme, ie linear) will be much 
		# faster
		self.cachedBits = shiftedBits
		
		self.UpdateIndexedBitmap(self.bpp)
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

	self.x = self.y = 0
	self.curLine = []
	self.drawing = False

	self.SetBackgroundColour("WHITE")
	self.SetCursor(wx.StockCursor(wx.CURSOR_PENCIL))

	self.SetScrollRate(20,20)

	self.DoDrawing()

	self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftButtonEvent)
	self.Bind(wx.EVT_LEFT_UP, self.OnLeftButtonEvent)
	self.Bind(wx.EVT_MOTION, self.OnLeftButtonEvent)
	self.Bind(wx.EVT_PAINT, self.OnPaint)
	
    def UpdateIndexedBitmap(self, reversedOrder=False):
	"""
	Creates/updates a bitmap image from a numpy array. Each entry in the 
	array is assumed to be the index into the palette of the color that is 
	suppose	to be displayed.
	
	The width and height of the bitmap is based upon the tile (sprite) size 
	specified by the user.
	"""
	workingBits = self.cachedBits[self.beginAddress:self.endAddress]
	
	shape = (int(math.ceil(workingBits.size / self.bpp)), self.bpp)	
	workingBits = workingBits.reshape(shape)
	
	packedBits = numpy.packbits(workingBits, axis=1)

	shiftFactor = (8-self.bpp)
	shiftedBits = numpy.right_shift(packedBits, shiftFactor)
	
	if reversedOrder == True:
	    original = numpy.array(shiftedBits)

	    oddEntries = numpy.array(original)
	    oddEntries[::2] = 0

	    evenEntries = numpy.roll(original, 1)
	    evenEntries[::2] = 0

	    shiftedBits = evenEntries + numpy.roll(oddEntries, -1)

	#self.paletteColors = self._getPalette()
	
	# Figure out how big our bitmap should be
	# Fixme: This chops off partial rows and partial tiles
	logicalWidth, logicalHeight = self._calcLogicalBmpSize(len(packedBits))
	displayLength = logicalWidth * logicalHeight
	
	# Get the actual entry then lookup the entry in the palette table and
	# copy the corresponding color entry into a new array.
	rgbArray = list(map(lambda x: self.paletteColors[x], shiftedBits[:displayLength].flatten()))
	rgbArray2 = numpy.array(rgbArray[:displayLength], dtype=numpy.uint8)

	# 5-D array. Think color pixel cube in a grid
	rgbArray2 = rgbArray2.reshape(self.rows, self.columns, self.tileHeight, self.tileWidth, 3)
	
	# We don't want to display the tiles only vertically. We want them
	# to be next to one another and wrap around in rows. This takes each
	# tile out of our column matrix and 'stacks' (puts) them into a 
	# row matrix
	ordered = numpy.hstack(rgbArray2)
	orderedAgain = numpy.hstack(ordered)
	
	#Test procedure:
	#for i in range(72):
	    #foo.append([i,i,i])
	## canvas = 4 rows, 3 cols, 
	## tile = 3w x 2h
	#normal = foo.reshape(4,3,3,2,3)
	#almost = numpy.hstack(normal)
	#correct = numpy.hstack(almost)

	bmp = wx.EmptyBitmap(logicalWidth, logicalHeight, 24)
	bmp.CopyFromBuffer(orderedAgain.tostring(), wx.BitmapBufferFormat_RGB)
	self.logicalBmp = bmp
	
	# We're done, account for the scaling factor and draw the bitmap
	self._scaleImage()
	
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

    def DoDrawing(self, dc=None):
	dc = dc
	virtualWidth = self.displayBmp.GetWidth() + 1
	virtualHeight = self.displayBmp.GetHeight() + 1
	
	if dc is None:
	    self.buffer = wx.EmptyBitmap(virtualWidth, virtualHeight)
	    dc = wx.BufferedDC(None, self.buffer)
	    dc.Clear()	

	self.SetVirtualSize((virtualWidth, virtualHeight))   
	dc.DrawBitmap(self.displayBmp, 0, 0, False)
	    
	if self.pixelGrid:
	    self._drawPixelGrid(dc)

	if self.tileGrid:
	    self._drawTileGrid(dc)

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
# Message handlers
#####

    def OnCanvasArrangementMsg(self, actionId):
	"""
	Handles a canvas arrangement message as posted from the toolpanel.
	@param actionId
	         The id of action that should be taken (Byteback, row forward,
		 etc).
	"""
	
	# If we don't have focus don't bother with the rest
	childFrame = self.GetParent()
	currentSelectedFrame = self.GetParent().GetParent().GetActiveChild()
	if childFrame != currentSelectedFrame:	
	    return
	
	pixelSize = self.bpp
	tileSize = self.tileWidth * self.tileHeight * pixelSize
	rowSize = self.columns * tileSize
	pageSize = rowSize * self.rows
	
	#def calcEndAddress():
	    #_bitsInByte = 8
	    #totalPixels = (self.fileSize * _bitsInByte) / self.bpp
	    #if totalPixels
	    #totalPages = 0
	    #if totalPixels % pageSize == 0:
		#totalPages = totalPixels / pageSize
	    #else:
		#totalPages = totalPixels / pageSize + 1
		
	    #if bytesLeft >= pageSize:
		#self.endAddress = self.endAddress + pageSize
	    #else:
		#self.endAddress = self.endAddress + byte
	addressOffset = 0	    	
	
	if actionId == ToolPanel.ID_ScrollUp:	    
	    if self.beginAddress - pageSize < 0:
		addressOffset = -self.beginAddress
	    else:
		addressOffset = -pageSize
	    
	elif actionId == ToolPanel.ID_ScrollDown:	    
	    addressOffset = +pageSize
	    
	elif actionId == ToolPanel.ID_RowBack:
	    if self.beginAddress - rowSize < 0:
		addressOffset = -self.beginAddress
	    else:
		addressOffset = -rowSize
	
	elif actionId == ToolPanel.ID_RowForward:
	    addressOffset = +rowSize
	
	elif actionId == ToolPanel.ID_TileBack:
	    if self.beginAddress - tileSize < 0:
		addressOffset = -self.beginAddress
	    else:
		addressOffset = -tileSize	    
	
	elif actionId == ToolPanel.ID_TileForward:
	    addressOffset = +tileSize
	
	elif actionId == ToolPanel.ID_ByteBack:
	    if self.beginAddress - pixelSize < 0:
		addressOffset = -self.beginAddress
	    else:
		addressOffset = -pixelSize
	    
	elif actionId == ToolPanel.ID_ByteForward:
	    addressOffset = +pixelSize
	
	else:
	    print 'Invalid canvas arrangement message'

	self.beginAddress = self.beginAddress + addressOffset
	self.endAddress = self.endAddress + addressOffset

	self.UpdateIndexedBitmap()
	self.DoDrawing()
	self.Refresh()
	
    def OnCanvasShiftMsg(self, shiftId):
	"""
	TODO: This isn't going to be easy...
	Handles a Canvas Shift message as posted from the toolpanel.
	@param shiftId
	         The id of the action that should be taken (shift left, right,
		 down, etc).
	"""
	childFrame = self.GetParent()
	currentSelectedFrame = self.GetParent().GetParent().GetActiveChild()
	if childFrame == currentSelectedFrame:
	    {ToolPanel.ID_ShiftLeft:   self._onShiftLeft,
	     ToolPanel.ID_ShiftRight:  self._onShiftRight,
	     ToolPanel.ID_ShiftUp:     self._onShiftUp,
	     ToolPanel.ID_ShiftDown:   self._onShiftDown,}[shiftId]()
	
    def OnCanvasToolMsg(self, toolId):
	"""
	Handles a Canvas Tool message as posted from the toolpanel.
	@param toolId
	         The id of action that should be taken (Pencil, pick color,
		 etc).
	"""
	{ToolPanel.ID_Selection:    self._onSelect,
        ToolPanel.ID_MoveSelection: self._onMoveSelection,
        ToolPanel.ID_ColorPicker:   self._onColorSelector,
        ToolPanel.ID_PencilDraw:    self._onPencilDraw,
        #ToolPanel.ID_DrawLine:     self._onDrawLine,
        ToolPanel.ID_FloodFill:     self._onFloodFill,
        ToolPanel.ID_Recolor:       self._onColorReplace,}[toolId]()
	
    def OnPaletteUpdateMsg(self, msg):
	"""
	
	"""
	childFrame = self.GetParent()
	currentSelectedFrame = self.GetParent().GetParent().GetActiveChild()
	if childFrame != currentSelectedFrame:	
	    return
	
	self.paletteColors = msg
	self.UpdateIndexedBitmap()
	self.DoDrawing()
	self.Refresh()
	
    def OnPaletteResponseMsg(self, msg):
	"""
	TODO: Do something if there are no palettes available?	
	Message is received when the canvas is first created. This is used as
	an initial handshake between a palette and it's corresponding canvas.
	"""
	self.paletteColors = msg
	

#-----------------------------------------------------------------------------
    def _onSelect(self):
        image = wx.Image(u"icons/tool-selection-16.png", wx.wx.BITMAP_TYPE_PNG)
        image.SetOptionInt(wx.IMAGE_OPTION_CUR_HOTSPOT_X, 6)
        image.SetOptionInt(wx.IMAGE_OPTION_CUR_HOTSPOT_Y, 6)   
        cursor = wx.CursorFromImage(image)
        self.SetCursor(cursor)
    
    def _onMoveSelection(self):
        cursor = wx.StockCursor(wx.CURSOR_ARROW)    
        self.SetCursor(cursor)
    
    def _onColorSelector(self):
        image = wx.Image(u"icons/tool-color-picker-16.png", wx.wx.BITMAP_TYPE_PNG)
        image.SetOptionInt(wx.IMAGE_OPTION_CUR_HOTSPOT_X, 1)
        image.SetOptionInt(wx.IMAGE_OPTION_CUR_HOTSPOT_Y, 12)
        cursor = wx.CursorFromImage(image)
        self.SetCursor(cursor)        
    
    def _onPencilDraw(self):
        print 'OnPencilDraw'
        image = wx.Image(u"icons/tool-pencil-16.png", wx.wx.BITMAP_TYPE_PNG)
        image.SetOptionInt(wx.IMAGE_OPTION_CUR_HOTSPOT_X, 3)
        image.SetOptionInt(wx.IMAGE_OPTION_CUR_HOTSPOT_Y, 15)   
        cursor = wx.CursorFromImage(image)
        self.SetCursor(cursor)
    
    #def _onDrawLine(self):
        #pass
    
    def _onFloodFill(self):
        image = wx.Image(u"icons/tool-bucket-fill-16.png", wx.wx.BITMAP_TYPE_PNG)
        image.SetOptionInt(wx.IMAGE_OPTION_CUR_HOTSPOT_X, 13)
        image.SetOptionInt(wx.IMAGE_OPTION_CUR_HOTSPOT_Y, 15)   
        cursor = wx.CursorFromImage(image)
        self.SetCursor(cursor)
    
    def _onColorReplace(self):
        cursor = wx.StockCursor(wx.CURSOR_ARROW)
        self.SetCursor(cursor)
    
#------------------------------------------------------------------------------    
    def _onShiftLeft(self):
        pass
    
    def _onShiftRight(self):
        pass
    
    def _onShiftUp(self):
        pass
    
    def _onShiftDown(self):
        pass
    
#------------------------------------------------------------------------------    	    
	    
#####
# Getters / Setters
#####

    def GetBpp(self):
	"""
	Returns the bpp for this canvas
	"""
	return self.bpp
    
    def SetBpp(self, bpp):
	"""
	Sets the bpp for this canvas
	"""
	self.bpp = int(bpp)    

    def GetTileSize(self):
	"""
	Returns the current tile size [width, height]
	"""
	return [self.tileWidth, self.tileHeight]
    
    def SetTileSize(self, width, height):
	"""
	Updates the canvas tile size
	@param width
	         int (1-128)
	@param height
	         int (1-128)
	"""
	self.tileWidth = width
	self.tileHeight = height

    def GetCanvasSize(self):
	"""
	Returns the current canvas size [rows, cols]
	"""
	return [self.rows, self.columns]	
    
    def SetCanvasSize(self, rows, columns):
	"""
	Updates the number of rows/columns that should be displayed on the 
	canvas (DC)
	@param rows
	         int (1-128)
	@param columns
	         int (1-128)
	"""
	self.rows = rows
	self.columns = columns
    
    def SetFileSize(self, byteSize=1):
	"""
	Sets the filesize. Only used when making a 'New' File.
	@param byteSize
	         Size of file in bytes
	"""
	self.fileSize = byteSize	
	    
    def SetTileGrid(self, val=False):
	"""
	Toggles the tile grid setting
	"""
	self.tileGrid = val
	    
    def SetPixelGrid(self, val=False):
	"""
	Toggles the pixel grid setting
	"""
	self.pixelGrid = val
	
    def SetZoom(self, zoomScale):
	"""
	Updates the zoom factor and redraws the image with the new scaling
	"""
	self.zoomConstant = zoomScale
	self._scaleImage()
    
#####
# Private Methods
#####

    def _changeCanvasArrangement(self, shift=None, direction=1):
	"""
	@param shift
	         Size of the shift to make. Either 'byte', 'tile', 'row', or 'page'
	@param direction
	        
	"""
	pixelSize = self.bpp
	tileSize = self.tileWidth * self.tileHeight * pixelSize
	rowSize = self.cols * tileSize
	pageSize = rowSize * self.rows
	
	value = 0
	
	#def calcEndAddress():
	    #_bitsInByte = 8
	    #totalPixels = (self.fileSize * _bitsInByte) / self.bpp
	    #if totalPixels
	    #totalPages = 0
	    #if totalPixels % pageSize == 0:
		#totalPages = totalPixels / pageSize
	    #else:
		#totalPages = totalPixels / pageSize + 1
		
	    #if bytesLeft >= pageSize:
		#self.endAddress = self.endAddress + pageSize
	    #else:
		#self.endAddress = self.endAddress + byte

	
	# all sizes in pixels, a page is the current visible area
	if shift == None:
	    # Just update the beginning and end sizes, don't shift
	    pass
	elif shift == 'byte':
	    value = pixelSize
	elif shift == 'tile':
	    value = tileSize
	elif shift == 'row':
	    value = rowSize
	#elif shift == '':
	    #colSize = self.columns * tileSize
	elif shift == 'page':
	    value = pageSize
	    
	self.beginAddress = self.beginAddress + value
	self.endAddress = self.endAddress + value

    def _calcLogicalBmpSize(self, length):
	"""
	Figures out the logical size of the bitmap to be displayed. This is not
	the entire file and it is not adjusted for zoom/displaying purposes
	@param length
	         int length of the current working array
	"""
	fullBmpWidth = self.tileWidth * self.columns
	fullBmpHeight = self.tileHeight * self.rows
	fullBmpSize = fullBmpWidth * fullBmpHeight
	
	print 'length', length
	print 'full bitmap width: ', fullBmpWidth
	print 'full bitmap height: ', fullBmpHeight
	print 'full bitmapsize: ', fullBmpSize
	tileSize = self.tileWidth * self.tileHeight	
	logicalBmpSize = [0, 0]
	
	# FIXME: Currently we chop off any partial rows
	# Do we have a full screen of tiles?
	if length >= fullBmpSize:
	    logicalBmpSize = [fullBmpWidth, fullBmpHeight]
	    self.numTiles = int(fullBmpSize // tileSize)
	    print 'full bitmap'
	    print 'tiles: ', self.numTiles
	else:
	    # Ignore partial tiles
	    print 'partial bitmap'
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
    
    def _scaleImage(self):
	"""
	Resizes the current bitmap. Called by selecting a zoom size from the
	dropdown
	"""
	image = self.logicalBmp.ConvertToImage()
	width = self.tileWidth * self.columns * self.zoomConstant
	height = self.tileHeight * self.rows * self.zoomConstant
	
	img = image.Rescale(width, height)
	self.displayBmp = img.ConvertToBitmap()  
	
    def _drawTileGrid(self, dc):
	"""
	Draws the tile grid
	"""
	dc.SetPen(wx.Pen('RED', 1))
	dc.SetBrush(wx.TRANSPARENT_BRUSH)
	
	canvasWidth = self.tileWidth * self.columns * self.zoomConstant
	canvasHeight = self.tileHeight * self.rows * self.zoomConstant

	# Draw rows
	for i in range(self.rows + 1):
	    x0 = 0
	    y0 = i * self.tileHeight * self.zoomConstant
	    x1 = canvasWidth + 1
	    y1 = i * self.tileHeight * self.zoomConstant
	    dc.DrawLine(x0, y0, x1, y1)	
	    
	# Draw columns
	for i in range(self.columns + 1):
	    x0 = i * self.tileWidth * self.zoomConstant
	    y0 = 0
	    x1 = i * self.tileWidth * self.zoomConstant
	    y1 = canvasHeight + 1
	    dc.DrawLine(x0, y0, x1, y1)
	    
    def _drawPixelGrid(self, dc):
	"""
	Draws the pixel grid
	"""
	dc.SetPen(wx.Pen(wx.Colour(128, 128, 128), 1))
	dc.SetBrush(wx.TRANSPARENT_BRUSH)
	
	canvasWidth = self.tileWidth * self.columns * self.zoomConstant
	canvasHeight = self.tileHeight * self.rows * self.zoomConstant
	    
	# Draw rows
	for i in range((canvasHeight / self.zoomConstant) + 1):
	    x0 = 0
	    y0 = i * self.zoomConstant
	    x1 = canvasWidth + 1
	    y1 = i * self.zoomConstant
	    dc.DrawLine(x0, y0, x1, y1)	
	    
	# Draw columns
	for i in range((canvasWidth / self.zoomConstant) + 1):
	    x0 = i * self.zoomConstant
	    y0 = 0
	    x1 = i * self.zoomConstant
	    y1 = canvasHeight + 1
	    dc.DrawLine(x0, y0, x1, y1)	
	
    def _getPalette(self):
	"""
	Gets the palette from the palette frame.
	CanvasFrame (parent ->) TilemFrame (has the ->) PaletteFrame	
	"""
	return self.GetParent().GetParent().GetPalette()

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
