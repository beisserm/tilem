import wx

[wxID_GOTODIALOG, wxID_ADDRESS_STATIC_BOX,
 wxID_ADDRESS_TEXTBOX, wxID_CANCEL_BUTTON,
 wxID_OFFSET_RADIO_BOX, wxID_OKBUTTON,
 wxID_RADIO_BOX,
] = [wx.NewId() for _init_ctrls in range(7)]

class GotoDialog(wx.Dialog):

	def __init__(self, prnt):
		# generated method, don't edit
		wx.Dialog.__init__(self, id=wxID_GOTODIALOG, name='GotoDialog',
			  parent=prnt, pos=wx.Point(453, 244), size=wx.Size(380, 182),
			  style=wx.CLOSE_BOX | wx.TAB_TRAVERSAL | wx.DEFAULT_DIALOG_STYLE,
			  title='Goto')
		self.SetClientSize(wx.Size(372, 148))
		self.Enable(True)
		self.SetHelpText('')
		self.SetToolTipString('')
		self.SetMinSize(wx.Size(100, 50))

		self.CancelButton = wx.Button(id=wx.ID_CANCEL,
			  label='Cancel', name='CancelButton', parent=self,
			  pos=wx.Point(200, 112), size=wx.Size(75, 23), style=0)
		
		self.OKButton = wx.Button(id=wx.ID_OK, label='OK',
			  name='OKButton', parent=self, pos=wx.Point(112, 112),
			  size=wx.Size(75, 23), style=0)

		self.AddressTextBox = wx.TextCtrl(id=wxID_ADDRESS_TEXTBOX,
			  name='AddressTextBox', parent=self, pos=wx.Point(16, 48),
			  size=wx.Size(112, 21), style=0, value='')
		self.AddressTextBox.SetMaxLength(10)
                
		self.RadixRadioBox = wx.RadioBox(choices=['Hex (16)', 'Dec (10)'],
			  id=wxID_RADIO_BOX, label='Radix', majorDimension=1,
			  name='RadixRadioBox', parent=self, pos=wx.Point(264, 24),
			  size=wx.Size(96, 64), style=wx.RA_SPECIFY_COLS)
		self.RadixRadioBox.SetToolTipString('')
		self.RadixRadioBox.SetThemeEnabled(False)
		self.RadixRadioBox.Bind(wx.EVT_RADIOBOX, self.OnRadixSelection,
			  id=wxID_RADIO_BOX)

		self.OffsetRadioBox = wx.RadioBox(choices=['Absolute', 'Relative'],
			  id=wxID_OFFSET_RADIO_BOX, label='Offset',
			  majorDimension=1, name='OffsetRadioBox', parent=self,
			  pos=wx.Point(152, 24), size=wx.Size(96, 64),
			  style=wx.RA_SPECIFY_COLS)
		self.OffsetRadioBox.SetToolTipString('')
		self.OffsetRadioBox.Bind(wx.EVT_RADIOBOX, self.OnOffsetSelection,
			  id=wxID_OFFSET_RADIO_BOX)

		self.AddressStaticBox = wx.StaticBox(id=wxID_ADDRESS_STATIC_BOX,
			  label='Address', name='AddressStaticBox', parent=self,
			  pos=wx.Point(8, 24), size=wx.Size(128, 64), style=0)
		self.AddressStaticBox.SetToolTipString('Address')
		self.AddressStaticBox.SetWindowVariant(wx.WINDOW_VARIANT_NORMAL)

		self.flexGridSizer2 = wx.FlexGridSizer(cols=0, hgap=0, rows=1, vgap=0)

	def OnOffsetSelection(self, event):
		index = self.OffsetRadioBox.GetSelection()
		s = "Selected " + str(index)
		print s

	def OnRadixSelection(self, event):
		index = self.RadixRadioBox.GetSelection()
		s = "Selected " + str(index)
		print s
