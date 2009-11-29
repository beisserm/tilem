
import  wx
import  images

from bitbuffer import BitBuffer

BUFFERED = 1

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
	def __init__(self, prnt, romFile=None): 
		wx.MDIChildFrame.__init__(self, parent=prnt)
		
		vbox = wx.BoxSizer(wx.VERTICAL)
	
		self.toolBar = toolBar = wx.ToolBar(id=-1, name='toolBar1', parent=self, pos=wx.DefaultPosition,
			            size=wx.Size(455, 28), style=wx.TB_HORIZONTAL | wx.NO_BORDER | wx.TB_BOTTOM )		    

		toolBar.zoomSelect = wx.ComboBox(choices=zoomSelections,
		        id=-1, name='zoom',
		        parent=toolBar, pos=wx.Point(2, 1), size=wx.Size(70, 20),
		        style=wx.CB_READONLY, value='100%')
		
		toolBar.decoderSelect = wx.ComboBox(choices=decoderSelections,
		        id=-1, name='decoder',
		        parent=toolBar, pos=wx.Point(90, 1), size=wx.Size(180, 20),
		        style=wx.CB_READONLY)

		toolBar.Realize()		
		toolBar.Raise()

		canvas = ScrolledCanvas(self, openFile=romFile)	
		
		vbox.Add(canvas, 1, wx.EXPAND)		
		vbox.Add(toolBar, 0, wx.EXPAND)
	
		self.SetSizer(vbox)
		self.Show(True)

		#self.SetToolBar(toolBar)
		

		
		self.Show(True)	
	

class ScrolledCanvas(wx.ScrolledWindow):	
	"""
	
	"""	
	def __init__(self, parent, id = -1, size = wx.DefaultSize, openFile = None):
		wx.ScrolledWindow.__init__(self, parent, id, (0, 0), size=size, style=wx.SUNKEN_BORDER)	
		
		if openFile:
			self.pixels = pixels = []			
			self.fileBytes = fileBytes = BitBuffer(openFile.read())				
			#for _8bits in fileBytes:
				#pixels.append(fileBytes.readbits(8))

			pixels.append(fileBytes.readbits(8))
			pixels.append(fileBytes.readbits(8))
			pixels.append(fileBytes.readbits(8))
			
			for color in pixels:
				print `hex(color)`
				
			print 'bits= ' + `hex(fileBytes.len)`
			#print pixels[1]
			#print pixels[2]	
		
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

		if BUFFERED:
			# Initialize the buffer bitmap.  No real DC is needed at this point.
			self.buffer = wx.EmptyBitmap(self.maxWidth, self.maxHeight)
			dc = wx.BufferedDC(None, self.buffer)
			dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
			dc.Clear()
			self.DoDrawing(dc)

		self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftButtonEvent)
		self.Bind(wx.EVT_LEFT_UP,   self.OnLeftButtonEvent)
		self.Bind(wx.EVT_MOTION,	self.OnLeftButtonEvent)
		self.Bind(wx.EVT_PAINT, self.OnPaint)


	def getWidth(self):
		return self.maxWidth

	def getHeight(self):
		return self.maxHeight


	def OnPaint(self, event):
		if BUFFERED:
			# Create a buffered paint DC.  It will create the real
			# wx.PaintDC and then blit the bitmap to it when dc is
			# deleted.  Since we don't need to draw anything else
			# here that's all there is to it.
			dc = wx.BufferedPaintDC(self, self.buffer, wx.BUFFER_VIRTUAL_AREA)
		else:
			dc = wx.PaintDC(self)
			self.PrepareDC(dc)
			# since we're not buffering in this case, we have to
			# paint the whole window, potentially very time consuming.
			self.DoDrawing(dc)
			parent.toolBar.Raise()


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

##		 dc.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL, wx.NORMAL))
##		 dc.SetTextForeground("BLACK")
##		 dc.DrawText("TEST this STRING", 10, 200)
##		 print dc.GetFullTextExtent("TEST this STRING")

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
			if BUFFERED:
				# If doing buffered drawing we'll just update the
				# buffer here and then refresh that portion of the
				# window, then that portion of the buffer will be
				# redrawn in the EVT_PAINT handler.
				dc = wx.BufferedDC(None, self.buffer)
			else:
				# otherwise we'll draw directly to a wx.ClientDC
				dc = wx.ClientDC(self)
				self.PrepareDC(dc)

			dc.SetPen(wx.Pen('MEDIUM FOREST GREEN', 4))
			coords = (self.x, self.y) + self.ConvertEventCoords(event)
			self.curLine.append(coords)
			dc.DrawLine(*coords)
			self.SetXY(event)

			if BUFFERED:
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


## This is an example of what to do for the EVT_MOUSEWHEEL event,
## but since wx.ScrolledWindow does this already it's not
## necessary to do it ourselves. You would need to add an event table 
## entry to __init__() to direct wheelmouse events to this handler.

##	 wheelScroll = 0
##	 def OnWheel(self, evt):
##		 delta = evt.GetWheelDelta()
##		 rot = evt.GetWheelRotation()
##		 linesPer = evt.GetLinesPerAction()
##		 print delta, rot, linesPer
##		 ws = self.wheelScroll
##		 ws = ws + rot
##		 lines = ws / delta
##		 ws = ws - lines * delta
##		 self.wheelScroll = ws
##		 if lines != 0:
##			 lines = lines * linesPer
##			 vsx, vsy = self.GetViewStart()
##			 scrollTo = vsy - lines
##			 self.Scroll(-1, scrollTo)

