import wx
from wx.lib.masked import NumCtrl

[wxID_COLUMNS, wxID_OK_BUTTON, wxID_CANCEL_BUTTON,
 wxID_COLUMNSSTATICTEXT1, wxIDCOLUMNS_FIELD, 
] = [wx.NewId() for i in range(5)]

class CanvasSizeDialog(wx.Dialog):
    def __init__(self, prnt, columns=16):
        '''
        Constructor
        @param columns
                 Number of columns to display in the dialog box. This is the
                 number of tile columns displayed on the canvas.
        '''
        wx.Dialog.__init__(self, id=wxID_COLUMNS, name='Columns', parent=prnt,
              pos=wx.Point(572, 355), size=wx.Size(255, 140),
              style=wx.DEFAULT_DIALOG_STYLE, title='Canvas Columns')
        self.SetClientSize(wx.Size(247, 106))

        self.columns = columns
        
        self.staticText1 = wx.StaticText(id=wxID_COLUMNSSTATICTEXT1,
              label='Columns', name='staticText1', parent=self, pos=wx.Point(64,
              28), size=wx.Size(40, 13), style=0)

        #self.textCtrl1 = wx.TextCtrl(id=wxID_COLUMNSTEXTCTRL1, name='textCtrl1',
              #parent=self, pos=wx.Point(120, 24), size=wx.Size(48, 21), style=0,
              #value='16')
        
        self.columnsField = NumCtrl( 
            self, id=wxIDCOLUMNS_FIELD, value = self.columns, pos=wx.Point(120, 24),
            size=wx.Size(48, 21), style = 0, validator = wx.DefaultValidator,
            name = "sizeField", integerWidth = 3, fractionWidth = 0, allowNone = False,
            allowNegative = False, useParensForNegatives = False, groupDigits = False,
            groupChar = ',', decimalChar = '.', min = 1, max = 128, limited = False,
            limitOnFieldChange = True, selectOnEntry = True, foregroundColour = "Black",
            signedForegroundColour = "Red", emptyBackgroundColour = "White",
            validBackgroundColour = "White", invalidBackgroundColour = "Yellow",
            autoSize = True
        )

        self.OkButton = wx.Button(id=wxID_OK_BUTTON, label='OK',
              name='OK', parent=self, pos=wx.Point(32, 64),
              size=wx.Size(75, 23), style=0)
        self.OkButton.Bind(wx.EVT_BUTTON, self.OnOk,
              id=wxID_OK_BUTTON)          

        self.CancelButton = wx.Button(id=wxID_CANCEL_BUTTON, label='Cancel',
              name='Cancel', parent=self, pos=wx.Point(136, 64),
              size=wx.Size(75, 23), style=0)
        self.CancelButton.Bind(wx.EVT_BUTTON, self.OnCancel,
              id=wxID_CANCEL_BUTTON)           
        
    def OnOk(self, event):
        self.columns = self.columnsField.GetValue()
        self.EndModal(wx.ID_OK)
        
    def OnCancel(self, event):
        self.EndModal(wx.ID_CANCEL)
        
    def GetColumns(self):
        return self.columnsField.GetValue()