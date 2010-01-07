import wx
import wx.lib.intctrl

[wxID_COLUMNS, 
 wxID_COLUMNSSTATICTEXT1, wxIDCOLUMNS_FIELD, 
] = [wx.NewId() for i in range(3)]

class CanvasSizeDialog(wx.Dialog):
    def __init__(self, prnt, rows=16, columns=16):
        '''
        Constructor
        @param rows
                 Number of rows to display in the dialog box. This is the
                 number of tile rows displayed on the canvas.                 
        @param columns
                 Number of columns to display in the dialog box. This is the
                 number of tile columns displayed on the canvas.
        '''
        wx.Dialog.__init__(self, id=wxID_COLUMNS, name='Columns', parent=prnt,
              pos=wx.Point(572, 355), size=wx.Size(255, 140),
              style=wx.DEFAULT_DIALOG_STYLE, title='Canvas Size')
        self.SetClientSize(wx.Size(247, 106))

        self.rows = rows
        self.columns = columns
        
        self.columnsLabel = wx.StaticText(id=-1, label='Columns', name='columnsLabel',
                                parent=self, pos=wx.Point(64, 14), 
                                size=wx.Size(40, 13), style=0)
              
        self.columnsField = wx.lib.intctrl.IntCtrl(self, value = 1, min = 1,
                                max = 128, pos = wx.Point(120, 14), size=(48, -1))

        self.rowsLabel = wx.StaticText(id=-1, label='Rows', name='rowsLabel',
                                parent=self, pos=wx.Point(64, 28), 
                                size=wx.Size(40, 13), style=0)
              
        self.rowsField = wx.lib.intctrl.IntCtrl(self, value = 1, min = 1, 
                                max = 128, pos = wx.Point(120, 48), size=(48, -1))        
        
        self.OkButton = wx.Button(id=wx.ID_OK, label='OK',
              name='OK', parent=self, pos=wx.Point(32, 80),
              size=wx.Size(75, 23), style=0)     

        self.CancelButton = wx.Button(id=wx.ID_CANCEL, label='Cancel',
              name='Cancel', parent=self, pos=wx.Point(136, 80),
              size=wx.Size(75, 23), style=0)
    
    def GetCanvasSize(self):
        return [self.rowsField.GetValue(), self.columnsField.GetValue()]
