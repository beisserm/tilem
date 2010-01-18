import math
import numpy
import random
import wx

#from cubecolourdialog import CubeColourDialog
import events.paletteUpdateEvent as pue

from dialogs.newPaletteDialog import NewPaletteDialog
from dialogs.paletteNameDialog import PaletteNameDialog

from cubecolourdialog import CubeColourDialog
from wx.lib.agw.flatnotebook import FlatNotebook
from wx.lib.scrolledpanel import ScrolledPanel

from wx.lib.buttons import GenButton

from utils.enthoughtSizer import FlowSizer


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

FRAME_SIZE = wx.Size(275, 325)

class bppEnum:
    """
    Unused Enum class
    """
    _4BPP_CGA  = 1
    _6BPP_NES  = 2
    _8BPP_EGA  = 3
    _9BPP_RGB  = 4
    _15BPP_RGB = 5
    _16BPP_RGB = 6
    _24BPP_RGB = 7
    _32BPP_ARGB = 8

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
        self.Bind(pue.EVT_BUTTON_CLICKPOS,  self.CatchBeginningPaletteItem, id=self.book.GetId())

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.book, 1, wx.EXPAND)
	sizer.Add(self.toolBar, 0, wx.EXPAND)
        self.SetSizer(sizer)
        self.Show(True)

    def CatchBeginningPaletteItem(self, evt):
	print 'Got it!'
	print evt
	
    def OnNew(self, evt):
	"""
	
	"""
	paletteDlg = NewPaletteDialog(self)
	
	if paletteDlg.ShowModal() == wx.ID_OK:
	    size = paletteDlg.GetSize()
	    colorEncoding = paletteDlg.GetColorEncoding()
	    self.Freeze()
	    page = ColoringPage(self, size, colorEncoding)
	    self.book.AddPage(page)   
	    page.UpdateAll()
	    self.Thaw()	 	    
	    self.Refresh()
	    
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

    def OnImportLocal(self, evt):
        pass

    def OnImportSaveState(self, evt):
        pass 
    
    def OnSelectEncoding(self, evt):
	selection = evt.GetString()
	page = self.book.GetCurrentPage()
	page.SetEncoding(selection)
	page.UpdateAll()
	self.Refresh()	
	
    def GetCurrentPalette(self):
	"""
	Returns a list of the colors in the current palette
	""" 
	page = self.book.GetCurrentPage()
	buttonList = page.GetColorEntries()
	rgbPalette = map(lambda button : button.GetBackgroundColour().Get(), buttonList)
	return rgbPalette
    
    # Was this here for a reason?
    #def GetPalettes(self):
        #return self.palettes    

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
        doBind(paletteMenu.Append(ID_NewPalette, "New", "Open a file"), self.OnNew)	
        doBind(paletteMenu.Append(ID_Randomize, "Randomize", "Open a file"), self.OnRandomize)
	
        importMenu = wx.Menu()
	paletteMenu.AppendMenu(-1, "Import", importMenu)	
        doBind(importMenu.Append(ID_ImportFromThisFile, "This File", "This File"), self.OnImportLocal)
        doBind(importMenu.Append(ID_ImportSaveState, "Save State", "Save State"), self.OnImportSaveState)
	
        menubar.Append(paletteMenu, "Palette")
        self.SetMenuBar(menubar)
	
    def __createToolBar(self):
	toolBar = wx.ToolBar(id=-1, name='toolBar1', parent=self, pos=wx.DefaultPosition,
	                     size=wx.Size(275, 28), style=wx.TB_HORIZONTAL | wx.NO_BORDER | wx.TB_BOTTOM )		    

	toolBar.colorEncodings = wx.ComboBox(choices=bppSelections,
	    id=-1, name='zoom', parent=toolBar, pos=wx.Point(2, 1), size=wx.Size(120, 20),
	    style=wx.CB_READONLY, value='8bpp EGA')
	self.Bind(wx.EVT_COMBOBOX, self.OnSelectEncoding, toolBar.colorEncodings)	
	
	# TODO: How should we handle setting the number of colors? Seems like we would always want at least
	#       256(?)
	toolBar.NumColors = wx.TextCtrl(parent = toolBar, id=-1, value='512', size=wx.Size(50, 20), style=wx.TE_READONLY,
	                                pos=wx.Point(140, 1))
	toolBar.NumColors.SetMaxLength(5)
        toolBar.NumColors.SetInsertionPoint(0)
	
	return toolBar

# -----------------------------------------------------------------------------	
class ColoringBook(wx.lib.agw.flatnotebook.FlatNotebook):
    def __init__(self, prnt):
        wx.lib.agw.flatnotebook.FlatNotebook.__init__(self, prnt)

	page = ColoringPage(self)
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
    
    # TODO: Add 'title' option to create new palette dialog
    def __init__(self, prnt, size=256, encoding='8bpp EGA', title='Default'):    
	"""
	@param size
		  The number of colors contained in this palette (1-512)
	@param encoding
		  A valid bpp Selection
	@param title 
		  The text displayed on the tab to identify this palette
	"""    	
	ScrolledPanel.__init__(self, prnt)
	self.sizer = FlowSizer()
	self.SetSizer(self.sizer)
	self.SetAutoLayout(1)
	self.SetupScrolling()    	
	
	self.size = size
	self.encoding = encoding
	self.title = title
	self.colorEntries = [] # Buttons
        	
	for color in range(size):
	    self.__createButton()

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

    def OnLeftDown(self, event):
        pt = event.GetPosition()
        evt = MyEvent(myEVT_BUTTON_CLICKPOS, self.GetId())
        evt.SetMyVal(pt)
        #print id(evt), sys.getrefcount(evt)
        self.GetEventHandler().ProcessEvent(evt)
        #print id(evt), sys.getrefcount(evt)
        event.Skip()	    
	    
    def OnPaletteUpdate(self):
	'''
	Posts to the top level MDI Frame
	'''
	#self.GetParent().OnPaletteUpdate()
	evt = pue.MyEvent(pue.myEVT_BUTTON_CLICKPOS, id=self.GetId())
#	event = MyEvent(myEVT_CUSTOM, self.GetId())
#	event.SetMyVal('here is some custom data')
#	self.GetEventHandler().ProcessEvent(event)	
	
        #evt.SetMyVal(pt)
	print 'making it'
        print id(evt)
	#print self.GetParent().GetParent().GetParent()
	wx.PostEvent(self.GetParent().GetParent(), evt)	
	#self.GetEventHandler().ProcessEvent(evt)
        #self.GetEventHandler().ProcessEvent(evt)
        #print id(evt), sys.getrefcount(evt)
        #evt.Skip()
	evt.Skip()
	
    def OnSetBeginningColor(self, evt):
	buttonObject = evt.GetEventObject()
	buttonNum = self.colorEntries.index(buttonObject) + 1
	self.getTool

    def UpdateAll(self):
	for entry in self.colorEntries:
	    entry.UpdateSelf()	

    def GetTitle(self):
	return self.title

    def GetColorEntries(self):
	return self.colorEntries

    def GetEncoding(self):
	return self.encoding

    def SetEncoding(self, encoding):
	self.encoding = encoding

    def __createButton(self, color=u'#FFFFFF'):
	"""
	@param color
	         6 digit RGB Hex string preceeded by a '#'
	"""
	colorBox = ColoringButton(prnt=self, colorStr=color)
	colorBox.Bind(wx.EVT_BUTTON, self.OnPickColor, colorBox)
	colorBox.Bind(wx.EVT_RIGHT_UP, self.OnSetBeginningColor, colorBox)
	self.colorEntries.append(colorBox)
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
	self.__setToolTip()
    
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
    