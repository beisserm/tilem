#from __future__ import with_statemen
import csv
import itertools
import math
import numpy
import os
import random
import re
import wx

#from cubecolourdialog import CubeColourDialog

from cubecolourdialog import CubeColourDialog
from dialogs.newPaletteDialog import NewPaletteDialog
from dialogs.paletteNameDialog import PaletteNameDialog
from utils.flowSizer import FlowSizer
from pubsub import pub
from wx.lib.agw.flatnotebook import FlatNotebook
from wx.lib.buttons import GenButton
from wx.lib.scrolledpanel import ScrolledPanel

[ID_Self, ID_NewPalette, ID_ImportSaveState, ID_ImportFromThisFile, 
 ID_Randomize, ID_MenuBar, ID_MENU_EDIT_RENAME_PAGE] = [wx.NewId() for num in range(7)]

# the default 256-color palette. Taken from the GBA game Gauntlet/Rampart
defaultPalette = [
    '#000000', '#000000', '#5858A0', '#6868B0', '#7878D0', '#B8B8F8', '#606060', '#000000',
    '#606060', '#804880', '#080880', '#683810', '#784020', '#F08060', '#00F800', '#F8B8B8',
    '#000000', '#000000', '#804820', '#905030', '#B06020', '#005828', '#F82000', '#F88820',
    '#F8C800', '#F8F8F8', '#682000', '#089050', '#F08080', '#6880E0', '#0850B0', '#0000B0',
    '#000000', '#000000', '#000000', '#383838', '#505058', '#606068', '#787878', '#787878',
    '#909090', '#000000', '#909090', '#783078', '#B068B0', '#683838', '#682820', '#781818',
    '#000000', '#000000', '#F8F8F8', '#484848', '#707078', '#787880', '#909090', '#A0A0A0',
    '#C0C0C0', '#000000', '#F8F8F8', '#A040A0', '#D078D0', '#784848', '#783028', '#901818',
    '#000000', '#000000', '#F80000', '#686868', '#888890', '#A8A8B0', '#D0D0D0', '#E0E0E0',
    '#F8F8F8', '#000000', '#F80000', '#F860F8', '#F898F8', '#A06060', '#783028', '#D02828',
    '#000000', '#000000', '#505878', '#686890', '#8080C0', '#B0A0E0', '#D8D8F8', '#F8F8F8',
    '#683030', '#784848', '#906060', '#A07878', '#B09090', '#D0B0B0', '#484868', '#F80000',
    '#000000', '#000000', '#383010', '#683818', '#683828', '#784030', '#B09000', '#785808',
    '#784850', '#781800', '#900000', '#782828', '#280018', '#580000', '#780808', '#B0B0B0',
    '#000000', '#000000', '#483818', '#804820', '#805030', '#905038', '#D0A800', '#A07808',
    '#A06068', '#A02000', '#D00000', '#A03030', '#380020', '#780000', '#900808', '#D0D0D0',
    '#000000', '#000000', '#584818', '#A05828', '#C07048', '#E07858', '#F8C800', '#F8B810',
    '#F898A8', '#F83000', '#F80000', '#F85050', '#480028', '#A00000', '#E00808', '#F8F8F8',
    '#000000', '#000000', '#000000', '#000000', '#A06068', '#B06878', '#200020', '#500040',
    '#580040', '#505050', '#8080A0', '#581010', '#683838', '#804818', '#C07030', '#A00808',
    '#000000', '#000000', '#F8F8F8', '#000000', '#A06068', '#D07888', '#300030', '#680058',
    '#700050', '#505050', '#9090B0', '#681010', '#784048', '#804818', '#C07030', '#C00808',
    '#000000', '#000000', '#F80000', '#000000', '#A06068', '#F090A0', '#480048', '#880070',
    '#880060', '#505050', '#9898C0', '#781818', '#804850', '#804818', '#C07030', '#E00808',
    '#000000', '#000000', '#901828', '#B03830', '#C07048', '#C07048', '#C08848', '#784848',
    '#F898A8', '#C00000', '#F83000', '#F8B830', '#782028', '#A04848', '#60F8F8', '#F8F8F8',
    '#000000', '#000000', '#784818', '#A05828', '#D07028', '#F86060', '#D0A870', '#906878',
    '#F898A8', '#2050F8', '#4088F8', '#88B8F8', '#000080', '#E0E0E0', '#080808', '#F8F8F8',
    '#000000', '#000000', '#784818', '#A05828', '#E07858', '#F898A8', '#A08860', '#D0A870',
    '#F8F860', '#E0E0E0', '#F8F8F8', '#000000', '#000000', '#000000', '#802018', '#000000',
    '#000000', '#000000', '#784818', '#A05828', '#E07858', '#F898A8', '#A08860', '#D0A870',
    '#F8F860', '#E0E0E0', '#F8F8F8', '#007808', '#00A000', '#00D050', '#802018', '#383058']

# TODO: Verify that each color does actually get mapped correctly to the nesdev one
#       and remove this
# There will always be some discrepancies as to the exact colors used by the NES due to
# the nature of TV's. Nesticle and subsequently fceultra use a lookup table in their
# exports of palettes. This palette sequence is directly from tile-molester and "it
# just works" (tm). Each color in this palette gets converted to the closest color in
# the nesdev palette anyways so it doesn't really matter.
nesticlePalette = [
    '#757575', '#271B8F', '#0000AB', '#47009F', '#8F0077', '#AB0013', '#A70000', '#7F0B00',
    '#432F00', '#004700', '#005100', '#003F17', '#1B3F5F', '#000000', '#000000', '#000000',
    '#BCBCBC', '#0073EF', '#233BEF', '#8300F3', '#BF00BF', '#E7005B', '#DB2B00', '#CB4F0F',
    '#8B7300', '#009700', '#00AB00', '#00933B', '#00838B', '#000000', '#000000', '#000000',
    '#FFFFFF', '#3FBFFF', '#5F97FF', '#A78BFD', '#F77BFF', '#FF77B7', '#FF7763', '#FF9B3B',
    '#F3BF3F', '#83D313', '#4FDF4B', '#58F898', '#00EBDB', '#000000', '#000000', '#000000',
    '#FFFFFF', '#ABE7FF', '#C7D7FF', '#D7CBFF', '#FFC7FF', '#FFC7DB', '#FFBFB3', '#FFDBAB',
    '#FFE7A3', '#E3FFA3', '#ABF3BF', '#B3FFCF', '#9FFFF3', '#000000', '#000000', '#000000']

#Thanks nesdev http://nesdev.parodius.com/nespal.txt
nesPalette = [
    '#808080', '#0000BB', '#3700BF', '#8400A6', '#BB006A', '#B7001E', '#B30000', '#912600',
    '#7B2B00', '#003E00', '#00480D', '#003C22', '#002F66', '#000000', '#050505', '#050505',
    '#C8C8C8', '#0059FF', '#443CFF', '#B733CC', '#FF33AA', '#FF375E', '#FF371A', '#D54B00',
    '#C46200', '#3C7B00', '#1E8415', '#009566', '#0084C4', '#111111', '#090909', '#090909',
    '#FFFFFF', '#0095FF', '#6F84FF', '#D56FFF', '#FF77CC', '#FF6F99', '#FF7B59', '#FF915F',
    '#FFA233', '#A6BF00', '#51D96A', '#4DD5AE', '#00D9FF', '#666666', '#0D0D0D', '#0D0D0D',
    '#FFFFFF', '#84BFFF', '#BBBBFF', '#D0BBFF', '#FFBFEA', '#FFBFCC', '#FFC4B7', '#FFCCAE',
    '#FFD9A2', '#CCE199', '#AEEEB7', '#AAF7EE', '#B3EEFF', '#DDDDDD', '#111111', '#111111']

cgaPalette = [
    '#000000', '#0000AA', '#00AA00', '#00AAAA', '#AA0000', '#AA00AA', '#AA5500', '#AAAAAA',
    '#555555', '#5555FF', '#55FF55', '#55FFFF', '#FF5555', '#FF55FF', '#FFFF55', '#FFFFFF']

#WTF was this used for in tile molestor
#String EGAString = 
#"000000 990000 009900 CC6600 000099 990099 009999 CCCCCC" +
#"666666 FF6666 66FF66 FFFF66 6666FF FF66FF 66FFFF FFFFFF";

# The IBM Enhanced Graphics Adapter (EGA) was able to create a total of 64 colors
# by using 2 bits per channel. Of these 64 colors', 16 could be displayed on screen
# at any one time
egaPalette = [
    '#000000', '#0000AA', '#00AA00', '#00AAAA', '#AA0000', '#AA00AA', '#AAAA00', '#AAAAAA',
    '#000055', '#0000FF', '#00AA55', '#00AAFF', '#AA0055', '#AA00FF', '#AAAA55', '#AAAAFF',

    '#005500', '#0055AA', '#00FF00', '#00FFAA', '#AA5500', '#AA55AA', '#AAFF00', '#AAFFAA',
    '#005555', '#0055FF', '#00FF55', '#00FFFF', '#AA5555', '#AA55FF', '#AAFF55', '#AAFFFF',

    '#550000', '#5500AA', '#55AA00', '#55AAAA', '#FF0000', '#FF00AA', '#FFAA00', '#FFAAAA',
    '#550055', '#5500FF', '#55AA55', '#55AAFF', '#FF0055', '#FF00FF', '#FFAA55', '#FFAAFF',

    '#555500', '#5555AA', '#55FF00', '#55FFAA', '#FF5500', '#FF55AA', '#FFFF00', '#FFFFAA',
    '#555555', '#5555FF', '#55FF55', '#55FFFF', '#FF5555', '#FF55FF', '#FFFF55', '#FFFFFF']

bppSelections = ['4bpp CGA', '6bpp NES', '8bpp EGA', '9bpp RGB(333)', '15bpp RGB(555)', 
	                           '16bpp RGB(565)', '24bpp RGB(888)', '32bpp ARGB(8888)']

saveStateFilter = "All supported formats|*.fc*;*.gs*;*.st*;*.zs*|\
NESticle Save States (*.st)|*.st*|\
FCEUltra Save States (*.fc)|*.fc*|\
Genecyst/Kega/Gens Save States (*.gs)|*.gs*|\
ZSNES Save States (*.zs)|*.zs*|\
All files (*.*)|*.*"

FRAME_SIZE = wx.Size(240, 330)

# -----------------------------------------------------------------------------
class PaletteFrame(wx.MiniFrame):
    """

    """
    def __init__(self, prnt):
        wx.MiniFrame.__init__(self, prnt, id=ID_Self, title='Color Palette', 
                              size=FRAME_SIZE, style=wx.DEFAULT_FRAME_STYLE | wx.FRAME_TOOL_WINDOW | wx.FRAME_NO_TASKBAR )

        self.palettes = {'default':defaultPalette, '6bpp NES':nesPalette, '4bpp CGA':cgaPalette, '8bpp EGA':egaPalette}
	self.toolBar = self.__createToolBar()
        self.book = ColoringBook(self)	
	
	self.__createPaletteMenu()
	pub.subscribe(self.OnPalettePosMsg, 'palettePosition')

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.book, 1, wx.EXPAND)
	sizer.Add(self.toolBar, 0, wx.EXPAND)
        self.SetSizer(sizer)
        self.Show(True)
	
    def OnNew(self, evt):
	"""
	
	"""
	paletteDlg = NewPaletteDialog(self)
	
	if paletteDlg.ShowModal() == wx.ID_OK:
	    size = paletteDlg.GetSize()
	    colorEncoding = paletteDlg.GetColorEncoding()
	    title = paletteDlg.GetName()
	    page = ColoringPage(self, size, colorEncoding, title)
	    self.book.AddPage(page)
	    page.UpdateAll()
	    self.Refresh()
    
    def OnOpen(self, evt):
	"""
	"""
	openDialog = wx.FileDialog(self, "Choose a file", "", "", "All files (*.*)|*.*", wx.OPEN )
	if openDialog.ShowModal() == wx.ID_OK:
	    fileHandle = None
	    fileName = None
	    paletteStr = []
	    
	    try:
		path = openDialog.GetPath()
		fileHandle = open(path, mode='r')
		fileName = os.path.basename(path)
	    except IOError:
		pass
	    
	    if fileHandle:
		reader = csv.reader(fileHandle)
		
		# for every line in the file find every word on that line
		# for every word on that line, check if it is a string of 
		# the form '#RRGGBB'
		try:
		    for line in reader:
			for item in line:
			    temp = item.strip()[:7]
			    matches = re.match("\#[0-9A-Fa-f]{6}", temp)
			    if matches:
				paletteStr.append(temp)
		except csv.Error, e:
		    print ('Error loading palette: line %d: %s' % (reader.line_num, e))
		    
		title = fileName
		page = ColoringPage(self, size, '8bpp EGA', title, data=paletteStr)
		self.book.AddPage(page)
		page.UpdateAll()
		self.Refresh()
		    
	openDialog.Destroy()	 	
	    
    def OnRandomize(self, evt):
	"""
	
	"""
        colorEntries = self.book.GetCurrentPage().GetColorEntries()

	makeSureDlg = wx.MessageDialog(None, 'Randomize current palette?', 'Question', 
	                       wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)	
	
	page = self.book.GetCurrentPage()
	selection = self.toolBar.colorEncodings.GetValue()
	page.SetEncoding(selection)
	
	if makeSureDlg.ShowModal() == wx.ID_YES:
	    for button in colorEntries:
		red = random.randint(0, 255)
		green = random.randint(0, 255)
		blue = random.randint(0, 255)
		newColor = "#%02x%02x%02x" % (red, green, blue)
		button.UpdateColor(newColor.upper())
	
	self.Refresh()

#####
# Event Handlers
#####

    def OnImportLocal(self, evt):
        pass

    def OnImportSaveState(self, evt):
	"""
	Handles loading a palette from a save state. 
	
	Currently supports:
	    NESticle
	    FCEUltra
	    Genecyst/Kega/Gens
	    ZSNES
	    
	Although it's trivial to add support for more
	"""	
	openDialog = wx.FileDialog(self, "Choose a file", "", "", saveStateFilter, wx.OPEN )
	if openDialog.ShowModal() == wx.ID_OK:
	    try:
		path = openDialog.GetPath()
		fileName = os.path.basename(path)
		ext = fileName.split('.')[-1]
		selectedFile = open(openDialog.GetPath(), mode='rb')		
		palette = ""
		page = None
		
#<palettefilter extensions="tpl" colorformat="CF01" size="256" offset="4" endianness="big">
#<description>Tile Layer Pro palette (*.tpl)</description>
#</palettefilter>
#<palettefilter extensions="pal" colorformat="RIFF" size="256" offset="24" endianness="big">
#<description>Windows Palette (*.pal)</description>		
		# seek is the position of where to start reading. ie start at 22791
		if ext.startswith('st'):
		    # NESticle, PalSize = 32, offset = 22791
		    palSize = 32
		    selectedFile.seek(22791)
		    palette = selectedFile.read(palSize)
		    paletteColors = map(lambda n: nesticlePalette[ord(n)], palette)
		    page = ColoringPage(self, palSize, '6bpp NES', 'Nesticle', data=paletteColors)
		    
		elif ext.startswith('fc'):
		    # FCEUltra, PalSize = 32, offset = 4276
		    palSize = 32
		    selectedFile.seek(4276)
		    palette = selectedFile.read(32)
		    paletteColors = map(lambda n: nesticlePalette[ord(n)], palette)
		    page = ColoringPage(self, palSize, '6bpp NES', 'Nesticle', data=paletteColors)		    
		    
		elif ext.startswith('gs'):
		    # Kega/Gens, Palsize = 64, offset = 274 
		    selectedFile.seek(274)
		    palette = selectedFile.read(64)
		    
		elif ext.startswith('zs'):
		    # ZSNES, Palsize = 256, offset = 52243
		    selectedFile.seek(52243)
		    palette = selectedFile.read(256)
		    
		else:
		    print 'Unsupported file'
		    
		self.book.AddPage(page)
		page.UpdateAll()
		self.Refresh()
	    except IOError:
		pass
	    
	openDialog.Destroy()		
    
    def OnSelectEncoding(self, evt):
	selection = evt.GetString()
	page = self.book.GetCurrentPage()
	page.SetEncoding(selection)
	page.UpdateAll()
	self.Refresh()
	
    def OnPalettePosMsg(self, msg):
	"""
	Sets where the palette should 'begin' on the bottom toolbar text field.
	@param msg
	        Where the palette should 'begin' on the bottom toolbar text field.
	"""
	self.toolBar.NumColors.ChangeValue(str(msg))	

    def __createPaletteMenu(self):
        """
        Creates the 'Palette' menu on the menu bar
        """
        def doBind(item, handler, updateUI=None):
            self.Bind(wx.EVT_MENU, handler, item)
            if updateUI is not None:
                self.Bind(wx.EVT_UPDATE_UI, updateUI, item)	
	
        menubar = wx.MenuBar()
		
        paletteMenu = wx.Menu()
        doBind(paletteMenu.Append(ID_NewPalette, "New", ""), self.OnNew)
	doBind(paletteMenu.Append(-1, "Open", ""), self.OnOpen)
        doBind(paletteMenu.Append(ID_Randomize, "Randomize", ""), self.OnRandomize)
	
        importMenu = wx.Menu()
	paletteMenu.AppendMenu(-1, "Import", importMenu)
        doBind(importMenu.Append(ID_ImportFromThisFile, "This File", ""), self.OnImportLocal)
        doBind(importMenu.Append(ID_ImportSaveState, "Save State", ""), self.OnImportSaveState)
	
        menubar.Append(paletteMenu, "Palette")
        self.SetMenuBar(menubar)
	
    def __createToolBar(self):
	toolBar = wx.ToolBar(id=-1, name='toolBar1', parent=self, pos=wx.DefaultPosition,
	                     size=wx.Size(275, 28), style=wx.TB_HORIZONTAL | wx.NO_BORDER | wx.TB_BOTTOM )		    

	toolBar.colorEncodings = wx.ComboBox(choices=bppSelections,
	    id=-1, name='zoom', parent=toolBar, pos=wx.Point(2, 1), size=wx.Size(120, 20),
	    style=wx.CB_READONLY, value='8bpp EGA')
	self.Bind(wx.EVT_COMBOBOX, self.OnSelectEncoding, toolBar.colorEncodings)	
	
	toolBar.NumColors = wx.TextCtrl(parent = toolBar, id=-1, value='1', size=wx.Size(50, 20), style=wx.TE_READONLY,
	                                pos=wx.Point(140, 1))
	toolBar.NumColors.SetMaxLength(5)
	
	return toolBar

# -----------------------------------------------------------------------------	
class ColoringBook(wx.lib.agw.flatnotebook.FlatNotebook):
    def __init__(self, prnt):
        wx.lib.agw.flatnotebook.FlatNotebook.__init__(self, prnt)

	page = ColoringPage(self, data=defaultPalette)
	self.AddPage(page)

	style = self.GetWindowStyleFlag()
	style |= wx.lib.agw.flatnotebook.FNB_X_ON_TAB
	style |= wx.lib.agw.flatnotebook.FNB_MOUSE_MIDDLE_CLOSES_TABS
	style |= wx.lib.agw.flatnotebook.FNB_NO_X_BUTTON
	
        self.SetWindowStyleFlag(style)
	
	self.__createRightClickMenu()
	
    def AddPage(self, page):
	"""
	Adds a page (tab) to this notebook	
	@param page
	         The page (tab) to add to this notebook
	"""
        wx.lib.agw.flatnotebook.FlatNotebook.AddPage(self, page, page.GetTitle())
	
    def OnRenameTab(self, event):
	page = self.GetCurrentPage()
	pIndex = self.GetPageIndex(page)
	oldName = self.GetPageText(pIndex)
	dlg = PaletteNameDialog(self, name=oldName)
	if dlg.ShowModal() == wx.ID_OK:
	    newName = dlg.GetName()
	    self.SetPageText(pIndex, newName)
	dlg.Destroy()
	
    def __createRightClickMenu(self):
	"""
	Private method that creates a... right click menu
	"""
        rmenu = wx.Menu()
        item = wx.MenuItem(rmenu, ID_MENU_EDIT_RENAME_PAGE, "Rename Tab", "Rename Tab")
	self.Bind(wx.EVT_MENU, self.OnRenameTab, item)
        rmenu.AppendItem(item)
	self.SetRightClickMenu(rmenu)
	
# -----------------------------------------------------------------------------

class ColoringPage(ScrolledPanel):
    """
    A basic panel that's represents a tab on the color palette window.
    """
    
    def __init__(self, prnt, size=256, encoding='8bpp EGA', title='Default', data=None):    
	"""
	@param size
		  The number of colors contained in this palette (1-512)
	@param encoding
		  A valid bpp Selection
	@param title 
		  The text displayed on the tab to identify this palette
	#param data
	          List of colors to be used for the palette '#RRGGBB'
	"""    	
	ScrolledPanel.__init__(self, prnt)
	self.sizer = FlowSizer()
	self.SetSizer(self.sizer)
	self.SetAutoLayout(1)
	self.SetupScrolling()    	
	
	self.size = size
	self.encoding = encoding
	self.title = title
	self.palettePos = 1
	
	pub.subscribe(self.OnPaletteRequest, 'paletteRequest')
	
	self.colorButtons = [] # Each button corresponds to 1 palette color

	if size > 512:
	    size = 512
	elif size < 256:
	    delta = 256 - size
	    for missing in xrange(delta):
		data.append('#000000')
	    size = 256
	
	if data:
	    for color in data:
		self._createButton(color)
	else:
	    for color in range(size):
		self._createButton()

    def OnPickColor(self, evt):
	"""
	Changes the color in the current palette based upon user input
	"""
	buttonObject = evt.GetEventObject()
	backgroundColor = buttonObject.GetBackgroundColour()
	colordlg = CubeColourDialog(self, prevColor=backgroundColor)
	
	if colordlg.ShowModal() == wx.ID_OK:
	    rgbColor = colordlg.GetHexColor()
	    buttonObject.UpdateColor(rgbColor)
	    self.OnPaletteUpdate()
	    colordlg.Destroy()  
    
    def OnPaletteUpdate(self):
	"""
	TODO: Indicates the user has changed a color in the palette. Post to
	the MDI Parent Frame.
	"""
	pass
	    
    def OnPalettePos(self, event):
	"""
	Indicates that the user wants to change where the palette should 
	'virtually' begin. Message is gotten by the PaletteFrame.
	"""
	try:
	    button = event.GetEventObject()
	    self.palettePos = self.colorButtons.index(button)
	    pub.sendMessage('palettePosition', msg=self.palettePos)
	    virtualPalette = self._updateVirtualPalette()
	    pub.sendMessage('paletteUpdate', msg=virtualPalette)
	except ValueError, exception:
	    print exception
	    
    def OnPaletteRequest(self, msg):
	"""
	Used to request the palette when a canvas is first drawn
	"""
	print 'Got palette request!'
	virtualPalette = self._updateVirtualPalette()
	pub.sendMessage('paletteResponse', msg=virtualPalette)

    def UpdateAll(self):
	for entry in self.colorButtons:
	    entry.UpdateSelf()	

    def GetTitle(self):
	return self.title

    def GetColorEntries(self):
	return self.colorButtons

    def GetEncoding(self):
	return self.encoding

    def SetEncoding(self, encoding):
	self.encoding = encoding

	
    def _updateVirtualPalette(self):
	"""
	
	""" 
	startIndex = self.palettePos - 1

	# Wrap around the end and fill with black
	virtualPalette = self.colorButtons[startIndex:]

	if startIndex != 0:
	    end = self.colorButtons[:(startIndex)]
	    begin = [virtualPalette, end]
	    flatList = list(itertools.chain(*begin))
	    virtualPalette = flatList

	mappedPalette = map(lambda button : button.GetBackgroundColour().Get(), virtualPalette)

	return mappedPalette	
	
    def _createButton(self, color=u'#FFFFFF'):
	"""
	@param color
	         6 digit RGB Hex string preceeded by a '#'
	"""
	colorBox = ColoringButton(prnt=self, colorStr=color)
	colorBox.Bind(wx.EVT_MIDDLE_UP, self.OnPickColor, colorBox)
	colorBox.Bind(wx.EVT_RIGHT_UP, self.OnPalettePos, colorBox)
	self.colorButtons.append(colorBox)
	self.sizer.Add(colorBox, 0, wx.ALL, 1)

# -----------------------------------------------------------------------------
class ColoringButton(wx.lib.buttons.GenButton):
    def __init__(self, prnt, colorStr=u'#FFFFFF'):
	wx.lib.buttons.GenButton.__init__(self, parent = prnt, id=-1, size = wx.Size(12, 12),
	                                  style = wx.BU_AUTODRAW | wx.NO_FULL_REPAINT_ON_RESIZE | wx.SIMPLE_BORDER) 
	
	self.actualColor = colorStr
	self.perceivedColor = '#FFFFFF'
	#self.SetBezelWidth(0)
	
	self.__translateToClosestColor(colorStr)
	self.__setToolTip(colorStr)
    
    def GetActualColor(self):
	return self.actualColor
    
    def GetPerceivedColor(self):
	return self.perceivedColor    
    
    def UpdateSelf(self):
	"""
	Updates the button based upon the current encoding selection and the 
	current actualColor. This is used to update a button when the user 
	selects a different encoding scheme.
	"""
	self.__translateToClosestColor(self.actualColor)
	self.__setToolTip(self.perceivedColor)	
    
    def UpdateColor(self, colorStr):
	self.__translateToClosestColor(colorStr)
	self.__setToolTip(self.perceivedColor)

    def __translateToClosestColor(self, colorStr):
	translator = self.GetParent().GetEncoding()
	
	if(translator == '4bpp CGA'):
	    self.__translateClosestIndexedColor(colorStr, cgaPalette)
	elif(translator == '6bpp NES'):
	    self.__translateClosestIndexedColor(colorStr, nesPalette)
	elif(translator == '8bpp EGA'):
	    self.__translateClosestIndexedColor(colorStr, egaPalette)
	elif(translator == '9bpp RGB(333)'  or translator == '15bpp RGB(555)' or
	     translator == '16bpp RGB(565)' or translator == '16bpp RGB(565)' or
	     translator == '24bpp RGB(888)' or translator == '32bpp ARGB(8888)'):
	    self.__translateClosestRGBColor(colorStr)
        else:
	    print 'Failure updating apparent color!'
	
    def __translateClosestIndexedColor(self, colorStr, colorTable):
	"""
	Translates
	@param currentColor
	         The current color in the palette '#RRGGBB'
	@return 
	         Color adjusted for current bpp selection
	"""
	bestColor = '#FFFFFF'
	bestDiff = 765 # 255 * 3
	
	targetR = int(colorStr[1:3], 16)
	targetG = int(colorStr[3:5], 16)
	targetB = int(colorStr[5:], 16)
	
	for paletteColor in colorTable:
	    r = int(paletteColor[1:3], 16)
	    g = int(paletteColor[3:5], 16)
	    b = int(paletteColor[5:], 16)
	    diff = int(math.fabs(targetR - r) + math.fabs(targetG - g) + math.fabs(targetB - b))

	    if diff < bestDiff:
		bestDiff = diff
		bestColor = paletteColor
	
	self.actualColor = colorStr
	self.perceivedColor = str(bestColor)
	self.SetBackgroundColour(self.perceivedColor)

	# Old Java code example
        #public int encode(int argb) {
        #int targetR = (argb & 0x00FF0000) >> 16;
        #int targetG = (argb & 0x0000FF00) >> 8;
        #int targetB = (argb & 0x000000FF);
        #int bestEntry=0, bestDiff=1000000;
        #for (int i=0; i<colorTable.length; i++) {
            #int val = colorTable[i];
            #int r = (val & 0x00FF0000) >> 16;
            #int g = (val & 0x0000FF00) >> 8;
            #int b = (val & 0x000000FF);
            #int diff = Math.abs(targetR - r) + Math.abs(targetG - g) + Math.abs(targetB - b);
            #if (diff < bestDiff) {
                #bestDiff = diff;
                #bestEntry = i;
            #}
        #}
        #return bestEntry;
	
    def __translateClosestRGBColor(self, colorStr):
	self.SetBackgroundColour(colorStr)
	self.__setToolTip(colorStr)
    
    def __setToolTip(self, color=u'#FFFFFF'):
	"""
	Updates the tooltip display for a color in the palette. This should always
	be the perceived color
	@param color
	         6 digit RGB Hex string preceeded by a '#'
	"""
	red = str(int(color[1:3] , 16))
	green =  str(int(color[3:5], 16))
	blue = str(int(color[5:], 16))		
	self.SetToolTipString('(' + red + ', ' + green + ', ' + blue + ')' + '\n' + color)    		
    
    def __sanitizeColorString(self, color):
	red = (str(hex(color[0]))[2:]).upper()
	green = (str(hex(color[1]))[2:]).upper()
	blue = (str(hex(color[2]))[2:]).upper()
	colorStr = '#' + str(red) + str(green) + str(blue)
	
	return colorStr
    