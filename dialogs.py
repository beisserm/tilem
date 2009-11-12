
import  wx

class GoToDialog(wx.Dialog):
	def __init__(self, parent):
		wx.Dialog.__init__(self, parent, -1, 'Goto Dialog', size=(400, 300) )

		self.address = '0'

		offsetBox = wx.StaticBox(self, -1, 'Offset', (5, 5), size=(100, 50))
		basicText = wx.TextCtrl(self, -1, self.address, pos=(10, 25), size=(80, -1))
		basicText.SetMaxLength(10)

#		sampleList = ['zero', 'one', 'two', 'three', 'four', 'five','six', 'seven', 'eight']
#		wx.RadioBox(panel, -1, "A Radio Box", (10, 10), wx.DefaultSize,sampleList, 2, wx.RA_SPECIFY_COLS)
		wx.RadioBox(self, -1, "Radix", (150, 10), wx.DefaultSize, ['Hex (16)', 'Dec(10)'], 1, wx.RA_SPECIFY_COLS | wx.NO_BORDER)

#		offsetBox.add(basicText)

		#basicText.SetInsertionPoint(0)
		sizer = wx.FlexGridSizer(cols=3, hgap=6, vgap=6)
#		sizer.AddMany([basicLabel, basicText, pwdLabel, pwdText])
		self.SetSizer(sizer)

		

#		button = wx.Button(self, wx.ID_OK, "Okay")
#		sizer = wx.BoxSizer(wx.VERTICAL)
#		sizer.Add(button, 0, wx.ALIGN_CENTER|wx.ALL, 5)
#		self.SetSizer(sizer)
#		self.Layout()
