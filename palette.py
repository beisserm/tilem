import wx

from utils.enthoughtSizer import FlowSizer

[ID_Self, ID_NewPalette, ID_ImportSaveState, ID_ImportFromThisFile, 
 ID_Randomize, ID_MenuBar] = [wx.NewId() for num in range(6)]

# the default 256-color palette. Taken from the GBA game Gauntlet/Rampart
defaultPalette = [
    '0x000000', '0x000000', '0x5858A0', '0x6868B0', '0x7878D0', '0xB8B8F8', '0x606060', '0x000000',
    '0x606060', '0x804880', '0x080880', '0x683810', '0x784020', '0xF08060', '0x00F800', '0xF8B8B8',
    '0x000000', '0x000000', '0x804820', '0x905030', '0xB06020', '0x005828', '0xF82000', '0xF88820',
    '0xF8C800', '0xF8F8F8', '0x682000', '0x089050', '0xF08080', '0x6880E0', '0x0850B0', '0x0000B0',
    '0x000000', '0x000000', '0x000000', '0x383838', '0x505058', '0x606068', '0x787878', '0x787878',
    '0x909090', '0x000000', '0x909090', '0x783078', '0xB068B0', '0x683838', '0x682820', '0x781818',
    '0x000000', '0x000000', '0xF8F8F8', '0x484848', '0x707078', '0x787880', '0x909090', '0xA0A0A0',
    '0xC0C0C0', '0x000000', '0xF8F8F8', '0xA040A0', '0xD078D0', '0x784848', '0x783028', '0x901818',
    '0x000000', '0x000000', '0xF80000', '0x686868', '0x888890', '0xA8A8B0', '0xD0D0D0', '0xE0E0E0',
    '0xF8F8F8', '0x000000', '0xF80000', '0xF860F8', '0xF898F8', '0xA06060', '0x783028', '0xD02828',
    '0x000000', '0x000000', '0x505878', '0x686890', '0x8080C0', '0xB0A0E0', '0xD8D8F8', '0xF8F8F8',
    '0x683030', '0x784848', '0x906060', '0xA07878', '0xB09090', '0xD0B0B0', '0x484868', '0xF80000',
    '0x000000', '0x000000', '0x383010', '0x683818', '0x683828', '0x784030', '0xB09000', '0x785808',
    '0x784850', '0x781800', '0x900000', '0x782828', '0x280018', '0x580000', '0x780808', '0xB0B0B0',
    '0x000000', '0x000000', '0x483818', '0x804820', '0x805030', '0x905038', '0xD0A800', '0xA07808',
    '0xA06068', '0xA02000', '0xD00000', '0xA03030', '0x380020', '0x780000', '0x900808', '0xD0D0D0',
    '0x000000', '0x000000', '0x584818', '0xA05828', '0xC07048', '0xE07858', '0xF8C800', '0xF8B810',
    '0xF898A8', '0xF83000', '0xF80000', '0xF85050', '0x480028', '0xA00000', '0xE00808', '0xF8F8F8',
    '0x000000', '0x000000', '0x000000', '0x000000', '0xA06068', '0xB06878', '0x200020', '0x500040',
    '0x580040', '0x505050', '0x8080A0', '0x581010', '0x683838', '0x804818', '0xC07030', '0xA00808',
    '0x000000', '0x000000', '0xF8F8F8', '0x000000', '0xA06068', '0xD07888', '0x300030', '0x680058',
    '0x700050', '0x505050', '0x9090B0', '0x681010', '0x784048', '0x804818', '0xC07030', '0xC00808',
    '0x000000', '0x000000', '0xF80000', '0x000000', '0xA06068', '0xF090A0', '0x480048', '0x880070',
    '0x880060', '0x505050', '0x9898C0', '0x781818', '0x804850', '0x804818', '0xC07030', '0xE00808',
    '0x000000', '0x000000', '0x901828', '0xB03830', '0xC07048', '0xC07048', '0xC08848', '0x784848',
    '0xF898A8', '0xC00000', '0xF83000', '0xF8B830', '0x782028', '0xA04848', '0x60F8F8', '0xF8F8F8',
    '0x000000', '0x000000', '0x784818', '0xA05828', '0xD07028', '0xF86060', '0xD0A870', '0x906878',
    '0xF898A8', '0x2050F8', '0x4088F8', '0x88B8F8', '0x000080', '0xE0E0E0', '0x080808', '0xF8F8F8',
    '0x000000', '0x000000', '0x784818', '0xA05828', '0xE07858', '0xF898A8', '0xA08860', '0xD0A870',
    '0xF8F860', '0xE0E0E0', '0xF8F8F8', '0x000000', '0x000000', '0x000000', '0x802018', '0x000000',
    '0x000000', '0x000000', '0x784818', '0xA05828', '0xE07858', '0xF898A8', '0xA08860', '0xD0A870',
    '0xF8F860', '0xE0E0E0', '0xF8F8F8', '0x007808', '0x00A000', '0x00D050', '0x802018', '0x383058']

#Thanks nesdev http://nesdev.parodius.com/nespal.txt
nesPalette = [
    '0x808080', '0x0000BB', '0x3700BF', '0x8400A6', '0xBB006A', '0xB7001E', '0xB30000', '0x912600',
    '0x7B2B00', '0x003E00', '0x00480D', '0x003C22', '0x002F66', '0x000000', '0x050505', '0x050505',
    '0xC8C8C8', '0x0059FF', '0x443CFF', '0xB733CC', '0xFF33AA', '0xFF375E', '0xFF371A', '0xD54B00',
    '0xC46200', '0x3C7B00', '0x1E8415', '0x009566', '0x0084C4', '0x111111', '0x090909', '0x090909',
    '0xFFFFFF', '0x0095FF', '0x6F84FF', '0xD56FFF', '0xFF77CC', '0xFF6F99', '0xFF7B59', '0xFF915F',
    '0xFFA233', '0xA6BF00', '0x51D96A', '0x4DD5AE', '0x00D9FF', '0x666666', '0x0D0D0D', '0x0D0D0D',
    '0xFFFFFF', '0x84BFFF', '0xBBBBFF', '0xD0BBFF', '0xFFBFEA', '0xFFBFCC', '0xFFC4B7', '0xFFCCAE',
    '0xFFD9A2', '0xCCE199', '0xAEEEB7', '0xAAF7EE', '0xB3EEFF', '0xDDDDDD', '0x111111', '0x111111']

cgaPalette = [
    '0x000000', '0x0000AA', '0x00AA00', '0x00AAAA', '0xAA0000', '0xAA00AA', '0xAA5500', '0xAAAAAA',
    '0x555555', '0x5555FF', '0x55FF55', '0x55FFFF', '0xFF5555', '0xFF55FF', '0xFFFF55', '0xFFFFFF']

# The IBM Enhanced Graphics Adapter (EGA) was able to create a total of 64 colors
# by using 2 bits per channel. Of these 64 colors', 16 could be displayed on screen
# at any one time
egaPalette = [
    '0x000000', '0x0000AA', '0x00AA00', '0x00AAAA', '0xAA0000', '0xAA00AA', '0xAAAA00', '0xAAAAAA',
    '0x000055', '0x0000FF', '0x00AA55', '0x00AAFF', '0xAA0055', '0xAA00FF', '0xAAAA55', '0xAAAAFF',

    '0x005500', '0x0055AA', '0x00FF00', '0x00FFAA', '0xAA5500', '0xAA55AA', '0xAAFF00', '0xAAFFAA',
    '0x005555', '0x0055FF', '0x00FF55', '0x00FFFF', '0xAA5555', '0xAA55FF', '0xAAFF55', '0xAAFFFF',

    '0x550000', '0x5500AA', '0x55AA00', '0x55AAAA', '0xFF0000', '0xFF00AA', '0xFFAA00', '0xFFAAAA',
    '0x550055', '0x5500FF', '0x55AA55', '0x55AAFF', '0xFF0055', '0xFF00FF', '0xFFAA55', '0xFFAAFF',

    '0x555500', '0x5555AA', '0x55FF00', '0x55FFAA', '0xFF5500', '0xFF55AA', '0xFFFF00', '0xFFFFAA',
    '0x555555', '0x5555FF', '0x55FF55', '0x55FFFF', '0xFF5555', '0xFF55FF', '0xFFFF55', '0xFFFFFF']

# -----------------------------------------------------------------------------

class PaletteFrame(wx.MiniFrame):
    """

    """
    def __init__(self, prnt):
        wx.MiniFrame.__init__(self, prnt, id=ID_Self, title='Color Palette', 
                              size=wx.Size(275, 325), style=wx.DEFAULT_FRAME_STYLE | wx.FRAME_TOOL_WINDOW | wx.FRAME_NO_TASKBAR )

        self.palettes = {"default":defaultPalette, "nes":nesPalette, "cga":cgaPalette, "ega":egaPalette}
        # setup menubar
        menubar = wx.MenuBar()
        menubar.Append(self.CreatePaletteMenu(), "Palette")
        self.SetMenuBar(menubar)

        book = ColoringBook(self)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(book, 1, wx.EXPAND)
        self.SetSizer(sizer)
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
        pass

    def OnRandomize(self, evt):
        pass

    def OnImportLocal(self, evt):
        pass

    def OnImportSaveState(self, evt):
        pass

# -----------------------------------------------------------------------------
    
class ColoringBook(wx.Notebook):
    def __init__(self, prnt):
        wx.Notebook.__init__(self, parent=prnt)

        # create the page windows as children of the notebook
        page1 = wx.Panel(self, -1)

        flow = FlowSizer()

        #for word in words:
            #st = wx.StaticText(panel, -1,word)
            #flow.Add(st,0,wx.ALL,2)

        #page1.SetSizer(flow)
        #self.Layout()
        
        #wx.BitmapFromBuffer
        
        #BitmapFromBuffer(width, height, dataBuffer, alphaBuffer=None):
            #"""
            #Creates a `wx.Bitmap` from the data in dataBuffer.  The dataBuffer
            #parameter must be a Python object that implements the buffer
            #interface, such as a string, array, etc.  The dataBuffer object is
            #expected to contain a series of RGB bytes and be width*height*3
            #bytes long. 
            #"""
        
        
        for color in prnt.GetPalettes()['default']:

            buffer = ''
            
            for i in range(12*12):
                buffer += str(i)
                buffer += str(i)
                buffer += str(i)
            
            bm =  wx.BitmapFromBuffer(12, 12, buffer)
            red = color[2:4]
            green =  color[4:6]
            blue = color[6:]
            #colorBox = wx.BitmapButton(bitmap=bm, id=-1, name='bitmapButton1', parent=page1, size=wx.Size(12, 12), style=wx.BU_AUTODRAW)
            colorBox = wx.Button(id=-1, parent=page1, size=wx.Size(12, 12), style=wx.NO_FULL_REPAINT_ON_RESIZE | wx.SIMPLE_BORDER | wx.NO_3D | wx.NO_BORDER | wx.ALWAYS_SHOW_SB | wx.BU_EXACTFIT )
            #colorBox.SetInitialSize(wx.Size(12,12))
            #colorBox.SetVirtualSize(wx.Size(12,12))
            #colorBox.SetMaxSize(wx.Size(12,12))
            #colorBox.SetMinSize(wx.Size(12,12))     
            colorBox.SetBackgroundColour('#' + color[2:])
            colorBox.SetForegroundColour('#' + color[2:])
            colorBox.SetToolTipString('(' + red + ', ' + green + ', ' + blue + ')' + '\n' + color)
            flow.Add(colorBox, 0, wx.ALL, 2)
        
        page1.SetSizer(flow)
        self.Layout()
        #sizer.Add(page1, 1, wx.EXPAND)
        
        #scroll.SetFocusIgnoringChildren()
        
        # add the pages to the notebook with the label to show on the tab
        self.AddPage(page1, "Default")

    def AddPage(self, page, text):
        wx.Notebook.AddPage(self, page=page, text=text)


class PageOne(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        t = wx.StaticText(self, -1, "This is a PageOne object", (20,20))


# -----------------------------------------------------------------------------

#DEFAULT_GAP = 1
#DEFAULT_SCROLL_RATE = 20

#class FlowPanel(wx.ScrolledWindow):
    #"""
    #@Author: http://www.gooli.org/blog/snippets/
    
    #This panel uses a flow layout algorithm. 
    #I've tried implementing it using a custmo sizer, but flow layout
    #is too wierd to make it work corretly.
    #So this panel implements it by directly catching the EVT_SIZE event.
    #"""
    #def __init__(self, parent=None):
        ## Prepare for use both in XRC and in-code creation
        #if parent:
            #wx.ScrolledWindow.__init__(self, parent)
        #else:
            #pre = wx.PreScrolledWindow()
            #self.PostCreate(pre)
            
        #self.Bind(wx.EVT_SIZE, self.on_size)
        #self.Bind(wx.EVT_WINDOW_CREATE, self.on_create)
        #self.Bind(wx.EVT_WINDOW_DESTROY, self.on_destroy)

        #self.hgap = DEFAULT_GAP
        #self.vgap = DEFAULT_GAP
        
        #self.prevSize = None
        #self.destroyed = False

    #def set_gaps(self, hgap, vgap):
        #self.hgap = hgap
        #self.vgap = vgap
        #self.Layout()

    #def Layout(self):
        #"""
        #Layout the child controls of the window using the flow layout algorithm.
        #Current scroll location is taken into consideration.
        #"""
        #(windowWidth, windowHeight) = self.GetClientSize()
        #windowWidth -= self.hgap*2
        #windowHeight -= self.vgap*2
        #x = self.hgap
        #y = self.vgap
        #rightEnd = 0
        #bottomEnd = 0
        #currRowHeight = 0
        
        ## Move and resize each item
        #for item in self.GetChildren():
            ## All items get the size they need
            #(itemWidth, itemHeight) = item.GetBestSize()
            
            ## If the row has ended - move to the next row
            #if x + itemWidth >= windowWidth:
                #x = self.hgap
                #y += currRowHeight + self.vgap
                #currRowHeight = 0
                
            ## Move the child window
            #scrolledX, scrolledY = self.CalcScrolledPosition(x, y)
            #item.SetDimensions(scrolledX, scrolledY, itemWidth, itemHeight)
            
            ## Update maximum widht and height for use by SetVirtualSize at the end
            #rightEnd = max(rightEnd, x+itemWidth)
            #bottomEnd = max(bottomEnd, y+itemHeight)

            ## Calculate the position of the next child window
            #x = x + itemWidth + self.hgap
            #currRowHeight = max(currRowHeight, itemHeight)

        ## Adjust the virtual size of the window to the total size of all child windows
        #self.SetVirtualSize((rightEnd, bottomEnd))
        #self.AdjustScrollbars()
        #self.Update()
            
    #def on_create(self, event):
        #self.SetScrollRate(DEFAULT_SCROLL_RATE, DEFAULT_SCROLL_RATE)
        
    #def on_destroy(self, event):
        #self.destroyed = True
            
    #def on_size(self, event):
        #if self.prevSize != event.GetSize():
            #self.prevSize = event.GetSize()
            #self.Layout()

## -----------------------------------------------------------------------------

#class FlowSizer(wx.PySizer):
    #def __init__(self):
        #wx.PySizer.__init__(self)

    #def CalcMin(self):
        #width = 0
        #height = 0

        #for item in self.GetChildren():

            #item_width, item_height = item.GetSize()

            #width += item_width
            #height = max(height, item_height)

        #return wx.Size(width, height)

    #def RecalcSizes(self):
        #x = 0
        #y = 0
        #size_x, dummy = self.GetSize()
        #max_item_height = 0

        #for item in self.GetChildren():
            #item_width, item_height = item.GetSize()
            #max_item_height = max(max_item_height, item_height)

            #if x + item_width > size_x:
                #x = 0
                #y += item_height
                 
            #item.SetDimension(wx.Point(x,y),
                              #wx.Size(item_width, max_item_height))

            #x += item_width

#if __name__ == '__main__':
    #text ='''\
#wxPython is a GUI toolkit for the Python programming language. It allows Python programmers to create programs with a robust, highly functional graphical user interface, simply and easily. It is implemented as a Python extension module (native code) that wraps the popular wxWidgets cross platform GUI library, which is written in C++.
#'''

    #class Frame(wx.Frame):
        #def __init__(self):
            #wx.Frame.__init__(self, None, -1)
            #panel = wx.Panel(self, -1)
            #flow = FlowSizer()

            #words = text.split()
            #for word in words:
                #st = wx.StaticText(panel, -1,word)
                #flow.Add(st,0,wx.ALL,2)

            #panel.SetSizer(flow)
            #self.Layout()


    #app = wx.App()
    #Frame().Show()
    #app.MainLoop()
            