import wx
import wx.grid

class TestFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title="Grid Attributes",size=(600,300))
        self.grid = PaletteGrid(self)
        self.grid.CreateGrid(5,5)
        for row in range(5):
            for col in range(5):
                self.grid.SetCellValue(row, col, "(%s,%s)" % (row, col))
         
        self.grid.SetCellTextColour(1, 1, "red")
        self.grid.SetCellFont(1,1, wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.grid.SetCellBackgroundColour(2, 2, "light blue")
        
        attr = wx.grid.GridCellAttr()
        attr.SetTextColour("navyblue")
        attr.SetBackgroundColour("pink")
        attr.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD))

        self.grid.SetAttr(4, 0, attr)
        self.grid.SetAttr(5, 1, attr)
        self.grid.SetRowAttr(8, attr)

class PaletteGrid(wx.grid.Grid):
    def __init__(self, prnt):
        wx.grid.Grid.__init__(self, parent=prnt, id=-1)
        self.EnableEditing(False)
        self.DisableDragRowSize()
        self.DisableDragColSize()

        
class MyCustomRenderer(wx.grid.PyGridCellRenderer):
    
    def __init__(self):
        gridlib.PyGridCellRenderer.__init__(self)
        
    def Draw(self, grid, attr, dc, rect, row, col, isSelected):
        dc.SetBackgroundMode(wx.SOLID)
        dc.SetBrush(wx.Brush(wx.BLACK, wx.SOLID))
        dc.SetPen(wx.TRANSPARENT_PEN)
        dc.DrawRectangleRect(rect)
        dc.SetBackgroundMode(wx.TRANSPARENT)
        dc.SetFont(attr.GetFont())
        text = grid.GetCellValue(row, col)
        colors = ["RED", "WHITE", "SKY BLUE"]
        x = rect.x + 1
        y = rect.y + 1
        for ch in text:
            dc.SetTextForeground(random.choice(colors))
            dc.DrawText(ch, x, y)
            w, h = dc.GetTextExtent(ch)
            x = x + w
            if x > rect.right - 5:
                break
            
    def GetBestSize(self, grid, attr, dc, row, col):
        text = grid.GetCellValue(row, col)
        dc.SetFont(attr.GetFont())
        w, h = dc.GetTextExtent(text)
        return wx.Size(w, h)
    
    def Clone(self):
        return MyCustomRenderer()        
        
app = wx.PySimpleApp()
frame = TestFrame()
frame.Show()
app.MainLoop()