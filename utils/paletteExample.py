import wx

from wx.lib.agw.flatnotebook import FlatNotebook
from wx.lib.scrolledpanel import ScrolledPanel

from wx.lib.buttons import GenButton

import wx

myEVT_BUTTON_CLICKPOS = wx.NewEventType()
EVT_BUTTON_CLICKPOS = wx.PyEventBinder(myEVT_BUTTON_CLICKPOS, 1)

class MyEvent(wx.PyCommandEvent):
    def __init__(self, evtType, id):
        wx.PyCommandEvent.__init__(self, evtType, id)
        self.myVal = None

    def GetMyVal(self):
        return self.myVal

# ---------------------------------------------------------------------------
class PaletteFrame(wx.MiniFrame):
    def __init__(self, prnt):
        wx.MiniFrame.__init__(self, prnt, id=-1, title='Color Palette', 
                              size=wx.Size(275, 325))

        book = ColoringBook(self)

	# Do I want to bind the book?
	self.Bind(EVT_BUTTON_CLICKPOS, self.CustomEventCatcher, book.GetCurrentPage())
	page = ColoringPage(self)
	book.AddPage(page)
	self.Refresh()
	
    def CustomEventCatcher(self, event):
	print 'Event reached destination: ', event.GetId()

# ---------------------------------------------------------------------------	
class ColoringBook(wx.lib.agw.flatnotebook.FlatNotebook):
    def __init__(self, prnt):
        wx.lib.agw.flatnotebook.FlatNotebook.__init__(self, prnt)
	page = ColoringPage(self)
	self.AddPage(page)

    def AddPage(self, page):
        wx.lib.agw.flatnotebook.FlatNotebook.AddPage(self, page, 'test')
	#self.Bind(EVT_BUTTON_CLICKPOS, self.PropogateMe, page)
	
    #def PropogateMe(self, event):
	#print 'Notebook got event with id: ', event.GetId()
	##So Far so good...
	#event.Skip()

# ---------------------------------------------------------------------------
class ColoringPage(ScrolledPanel):
    def __init__(self, prnt, size=1, title='Default'):
	ScrolledPanel.__init__(self, prnt)
	self.sizer = wx.GridSizer(16,16)
	self.SetSizer(self.sizer)	
        	
	colorBox = wx.Button(self, id=-1)
	colorBox.Bind(wx.EVT_RIGHT_UP, self.OnRightUp, colorBox)
	self.sizer.Add(colorBox, 0, wx.ALL, 1)
    
    def OnRightUp(self, event):
	evt = MyEvent(myEVT_BUTTON_CLICKPOS, id=self.GetId())
	print 'Got custom event id: ', evt.GetId()	
	self.GetEventHandler().ProcessEvent(evt)
	event.Skip()

# ---------------------------------------------------------------------------
if __name__ == '__main__':
    class MyApp(wx.App):
	def OnInit(self):
	    frame = PaletteFrame(None)
	    frame.Show(True)
	    self.SetTopWindow(frame)
	    return True


    app = MyApp(False)
    app.MainLoop()	