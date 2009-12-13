import wx
import random
#import wx.lib
#from cubecolourdialog import CubeColourDialog

from dialogs.newPaletteDialog import NewPaletteDialog



from cubecolourdialog import CubeColourDialog
from wx.lib.agw.flatnotebook import FlatNotebook

from wx.lib.buttons import GenButton

from utils.enthoughtSizer import FlowSizer

[ID_Self, ID_NewPalette, ID_ImportSaveState, ID_ImportFromThisFile, 
 ID_Randomize, ID_MenuBar] = [wx.NewId() for num in range(6)]

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

FRAME_SIZE = wx.Size(275, 325)

bppSelections = ['4bpp CGA', '6bpp NES', '8bpp EGA', '9bpp RGB(333)', '15bpp RGB(555)', 
	                           '16bpp RGB(565)', '24bpp RGB(888)', '32bpp ARGB(8888)']
# -----------------------------------------------------------------------------

class PaletteFrame(wx.MiniFrame):
    """

    """
    def __init__(self, prnt):
        wx.MiniFrame.__init__(self, prnt, id=ID_Self, title='Color Palette', 
                              size=FRAME_SIZE, style=wx.DEFAULT_FRAME_STYLE | wx.FRAME_TOOL_WINDOW | wx.FRAME_NO_TASKBAR )

        self.palettes = {"default":defaultPalette, "nes":nesPalette, "cga":cgaPalette, "ega":egaPalette}
        self.numPalettes = 1
	
        # setup menubar
        menubar = wx.MenuBar()
        menubar.Append(self.CreatePaletteMenu(), "Palette")
        self.SetMenuBar(menubar)

        self.book = ColoringBook(self)
        
	toolBar = wx.ToolBar(id=-1, name='toolBar1', parent=self, pos=wx.DefaultPosition,
	                     size=wx.Size(275, 28), style=wx.TB_HORIZONTAL | wx.NO_BORDER | wx.TB_BOTTOM )		    

	toolBar.colorEncodings = wx.ComboBox(choices=bppSelections,
	    id=-1, name='zoom', parent=toolBar, pos=wx.Point(2, 1), size=wx.Size(120, 20),
	    style=wx.CB_READONLY, value='4bpp CGA')
	
	#change hard coded value
	toolBar.NumColors = wx.TextCtrl(parent = toolBar, id=-1, value='512', size=wx.Size(50, 20), style=0,
	                                pos=wx.Point(140, 1))
	toolBar.NumColors.SetMaxLength(5)
        toolBar.NumColors.SetInsertionPoint(0)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.book, 1, wx.EXPAND)
	sizer.Add(toolBar, 0, wx.EXPAND)
        self.SetSizer(sizer)
        #self.SetSizeHintsSz(FRAME_SIZE, FRAME_SIZE)
        self.Show(True)

    def CreatePaletteMenu(self):
        """
        Creates the 'Palette' menu on the menu bar
        """
        paletteMenu = wx.Menu()

        newPaletteMenuItem = wx.MenuItem(paletteMenu, ID_NewPalette, "New", wx.EmptyString, wx.ITEM_NORMAL)
        paletteMenu.AppendItem(newPaletteMenuItem)
        self.Bind(wx.EVT_MENU, self.OnNew, newPaletteMenuItem)

        randomizeMenuItem = wx.MenuItem(paletteMenu, ID_Randomize, "Randomize", wx.EmptyString, wx.ITEM_NORMAL)
        paletteMenu.AppendItem(randomizeMenuItem)
        self.Bind(wx.EVT_MENU, self.OnRandomize, randomizeMenuItem)

        importMenu = wx.Menu()
        thisFileMenuItem = wx.MenuItem(importMenu, ID_ImportFromThisFile, "This File", wx.EmptyString, wx.ITEM_NORMAL)
        importMenu.AppendItem(thisFileMenuItem)
        self.Bind(wx.EVT_MENU, self.OnImportLocal, thisFileMenuItem)

        saveStateMenuItem = wx.MenuItem(importMenu, ID_ImportSaveState, "Save State", wx.EmptyString, wx.ITEM_NORMAL)
        importMenu.AppendItem(saveStateMenuItem)
        self.Bind(wx.EVT_MENU, self.OnImportSaveState, saveStateMenuItem)

        paletteMenu.AppendMenu(-1, "Import", importMenu)

        return paletteMenu
    
    def GetPalettes(self):
        return self.palettes

    def OnNew(self, evt):
	
	paletteDlg = NewPaletteDialog(self)
	
	if paletteDlg.ShowModal() == wx.ID_OK:
	    self.size = paletteDlg.GetSize()
	    self.style = paletteDlg.GetFormat()
	    self.book.AddPage(ColoringPage(self, self.size, self.style))

    def OnRandomize(self, evt):
        colorEntries = self.book.GetCurrentPage().GetColorEntries()

	makeSureDlg = wx.MessageDialog(None, 'Randomize current palette?', 'Question', 
	                       wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)	
		
	if makeSureDlg.ShowModal() == wx.ID_YES:
	    for button in colorEntries:
		red = random.randint(0, 255)
		green = random.randint(0, 255)
		blue = random.randint(0, 255)
		button.SetBackgroundColour((red, green, blue))
		

    def OnImportLocal(self, evt):
        pass

    def OnImportSaveState(self, evt):
        pass

# -----------------------------------------------------------------------------
"""
A basic panel that's represents a tab on the color palette window.
"""
class ColoringPage(wx.Panel):
    def __init__(self, prnt, size=256, style='15bpp RGB(555)', title='Default'):    
	"""
	@param size
		  The number of colors contained in this palette (1-4096)
	@param style
		  A valid bpp Selection
	@param title 
		  The text displayed on the tab to identify this palette
	"""    	
	wx.Panel.__init__(self, prnt)
	self.size = size
	self.style = style
	self.title = title
	self.colorEntries = []
        self.flowSizer = FlowSizer()
	
        #self.colors = {}
        #BitmapFromBuffer(width, height, dataBuffer, alphaBuffer=None):
            #"""
            #Creates a `wx.Bitmap` from the data in dataBuffer.  The dataBuffer
            #parameter must be a Python object that implements the buffer
            #interface, such as a string, array, etc.  The dataBuffer object is
            #expected to contain a series of RGB bytes and be width*height*3
            #bytes long. 
            #"""        
	if (style == 'default' or style == '4bpp CGA' or style == '6bpp NES' or style == '8bpp EGA'):
	    for color in prnt.GetPalettes()[style]:
		#print 'color: ' + str(color)
		self.__CreateButton(color)
	else:
	    for color in range(size):
		#print 'colorNo: ' + str(color)
		self.__CreateButton()

        self.SetSizer(self.flowSizer)

    def __CreateButton(self, color=u'#FFFFFF'):
	bm = wx.EmptyBitmap(0, 0, -1)
	colorBox = wx.BitmapButton(bitmap=bm, id=-1, parent=self, size=wx.Size(12, 12), style=wx.BU_AUTODRAW | wx.NO_FULL_REPAINT_ON_RESIZE | wx.NO_BORDER)
	#colorBox = wx.Button(id=-1, parent=page1, size=wx.Size(12, 12), style=wx.NO_FULL_REPAINT_ON_RESIZE | wx.NO_BORDER | wx.NO_3D)
	colorBox.SetMargins(0, 0)     
	colorBox.SetBackgroundColour(color)
	colorBox.SetToolTipString(color)	
	self.Bind(wx.EVT_BUTTON, self.OnPickColor, colorBox) 		
	self.colorEntries.append(colorBox)
	self.flowSizer.Add(colorBox, 0, wx.ALL, 2)
	
	
    def OnPickColor(self, event):
	"""
	Changes the color in the current palette based upon user input
	"""
	buttonObject = event.GetEventObject()
	backgroundColor = buttonObject.GetBackgroundColour()
	colordlg = CubeColourDialog(self, prevColor=backgroundColor)
	
	if colordlg.ShowModal() == wx.ID_OK:
	    rgbColor = colordlg.GetRGBAColour() # (255, 34, 203, 255)
	    rgbTemp = str(rgbColor).replace('(', '')
	    rgbTemp = str(rgbTemp).replace(')', '')
	    colorList = rgbTemp.split(', ')
	    red = str(colorList[0])
	    green = str(colorList[1])
	    blue = str(colorList[2])
	    colorStr = str(int(red, 16)) + str(int(green, 16)) + str(int(blue, 16))
	    
	    buttonObject.SetBackgroundColour(rgbColor)
	    self.SetToolTip(buttonObject, colorStr)
	    colordlg.Destroy()
    
    def SetToolTip(self, button, color=u'#FFFFFF'):
	"""
	Updates the tooltip display for a color in the palette
	"""
	red = str(int(color[1:3],16)) #  str(int(red, 16)
	green =  str(int(color[3:5],16))
	blue = str(int(color[5:],16))	
	#print red + green + blue
	print 'fuck'
	button.SetToolTipString('(' + red + ', ' + green + ', ' + blue + ')' + '\n' + color)	
	
    def GetTitle(self):
	return self.title
    
    def GetColorEntries(self):
	return self.colorEntries
# -----------------------------------------------------------------------------
class ColoringBook(wx.lib.agw.flatnotebook.FlatNotebook):
    def __init__(self, prnt):
        wx.lib.agw.flatnotebook.FlatNotebook.__init__(self, prnt)
	page = ColoringPage(self)
	self.AddPage(page)
	
    def AddPage(self, page):
	"""
	Adds a page (tab) to this notebook	
	@param page
	         The page (tab) to add to this notebook
	"""
        wx.lib.agw.flatnotebook.FlatNotebook.AddPage(self, page, page.GetTitle())
	