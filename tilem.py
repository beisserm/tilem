#!/usr/bin/env python

__author__="Matt Beisser"
__date__ ="$Oct 16, 2009 6:33:40 PM$"

import  wx

# Importing ScrolledWindow demo to make use of the MyCanvas
# class defined within.
import  ScrolledWindow
import  images

SHOW_BACKGROUND = 1

#----------------------------------------------------------------------
ID_New  = wx.NewId()
ID_Exit = wx.NewId()

# File Menu Ids
ID_NewMenuItem = wx.NewId()
ID_OpenMenuItem = wx.NewId()
ID_ReopenMenuItem = wx.NewId()
ID_ImportImageMenuItem = wx.NewId()
ID_SaveMenuItem = wx.NewId()
ID_SaveAsMenuItem = wx.NewId()
ID_SaveSelectionMenuItem = wx.NewId()
ID_CloseMenuItem = wx.NewId()
ID_CloseAllMenuItem = wx.NewId()
ID_ExitMenuItem = wx.NewId()

# Edit Menu Ids
ID_UndoMenuItem = wx.NewId()
ID_RedoMenuItem = wx.NewId()
ID_CutMenuItem = wx.NewId()
ID_CopyMenuItem = wx.NewId()
ID_PasteMenuItem = wx.NewId()
ID_DeleteMenuItem = wx.NewId()

# View Menu Ids
ID_1dModeMenuItem = wx.NewId()
ID_2dModeMenuItem = wx.NewId()
ID_FullCanvasBlockSizeMenuItem = wx.NewId()
ID_CustomBlockSizeMenuItem = wx.NewId()
ID_RowInterleaveBlocksMenuItem = wx.NewId()
ID_BlockGridMenuItem = wx.NewId()
ID_TileGridMenuItem = wx.NewId()
ID_PixelGridMenuItem = wx.NewId()

# Image Menu Ids
ID_FlipHorizontalMenuItem = wx.NewId()
ID_FlipVerticalMenuItem = wx.NewId()
ID_RotateClockwiseMenuItem = wx.NewId()
ID_RotateCounterClockwiseMenuItem = wx.NewId()
ID_CanvasSizeMenuItem = wx.NewId()
ID_SelectionSizeMenuItem = wx.NewId()

# Navigate Menu Ids
ID_GotoAddressMenuItem = wx.NewId()
ID_AddBookMarkMenuItem = wx.NewId()
ID_OrganizeBookmarksMenuItem = wx.NewId()

# Window Menu Ids
ID_TileMenuItem = wx.NewId()
ID_CascadeMenuItem = wx.NewId()
ID_ArrangeMenuItem = wx.NewId()
ID_ColorPaletteMenuItem = wx.NewId()
ID_StatusBarMenuItem = wx.NewId()
ID_ToolbarMenuItem = wx.NewId()

# Help Menu Ids
ID_HelpTopicsMenuItem = wx.NewId()
ID_AboutMenuItem = wx.NewId()
#----------------------------------------------------------------------

class TilemFrame(wx.MDIParentFrame):
	def __init__(self):

		wx.MDIParentFrame.__init__(self, None, -1, "MDI Parent", size=(600,400))

		self.winCount = 0	

		menubar = wx.MenuBar()
		#fileMenu = self.CreateFileMenu()
		menubar.Append(self.CreateFileMenu(), "File")
		menubar.Append(self.CreateEditMenu(), "Edit")
		self.SetMenuBar(menubar)
		self.CreateStatusBar()
		menubar.Append(self.CreateHelpMenu(), "Help")
		
		#filemenu = wx.Menu()
		#editMenu = wx.Menu()
		#menu = wx.Menu()
		#menu.Append(ID_New, "&New Window")
		#menu.AppendSeparator()
		#menu.Append(ID_Exit, "E&xit")
		#
		#menubar = wx.MenuBar()
		#menubar.Append(menu, "&File")
		#self.SetMenuBar(menubar)
		#self.CreateStatusBar()

		self.Bind(wx.EVT_MENU, self.OnNewWindow, id=ID_New)
		self.Bind(wx.EVT_MENU, self.OnExit, id=ID_Exit)

		if SHOW_BACKGROUND:
			self.bg_bmp = images.GridBG.GetBitmap()
			self.GetClientWindow().Bind(
				wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground
			)
		

	def CreateMenus():
		#filemenu = wx.Menu()
		editMenu = wx.Menu()
		menu = wx.Menu()
		menu.Append(ID_New, "&New Window")
		menu.AppendSeparator()
		menu.Append(ID_Exit, "E&xit")
		
		menubar = wx.MenuBar()
		menubar.Append(menu, "&File")
		self.SetMenuBar(menubar)
		self.CreateStatusBar()
		self.winCount = self.winCount + 1		
		
	def CreateFileMenu(self):
		"""
		Creates the 'File' menu on the menu bar
		"""
		fileMenu = wx.Menu()

		newMenuItem = wx.MenuItem(fileMenu, ID_NewMenuItem, "New...\tCtrl+N", "New...", wx.ITEM_NORMAL)
		newMenuItem.SetBitmap(wx.Bitmap("icons/New-16.png", wx.BITMAP_TYPE_PNG))
		fileMenu.AppendItem(newMenuItem)

		openMenuItem = wx.MenuItem(fileMenu, ID_OpenMenuItem, "Open...\tCtrl+O", "Open...", wx.ITEM_NORMAL)
		openMenuItem.SetBitmap(wx.Bitmap("icons/Open-16.png", wx.BITMAP_TYPE_PNG))
		fileMenu.AppendItem(openMenuItem)

		reOpenMenuItem = wx.MenuItem(fileMenu, ID_ReopenMenuItem, "Reopen", "", wx.ITEM_NORMAL)
		fileMenu.AppendItem(reOpenMenuItem)

		importImageMenuItem = wx.MenuItem(fileMenu, ID_ImportImageMenuItem, "Import Image", "", wx.ITEM_NORMAL)
		fileMenu.AppendItem(importImageMenuItem)

		fileMenu.AppendSeparator()

		saveMenuItem = wx.MenuItem(fileMenu, ID_SaveMenuItem, "Save\tCtrl+S", "New...", wx.ITEM_NORMAL)
		saveMenuItem.SetBitmap(wx.Bitmap("icons/Save-16.png", wx.BITMAP_TYPE_PNG))
		fileMenu.AppendItem(saveMenuItem)

		saveAsMenuItem = wx.MenuItem(fileMenu, ID_SaveAsMenuItem, "Save As...\tCtrl+Shift+S", "Save As", wx.ITEM_NORMAL)
		saveAsMenuItem.SetBitmap(wx.Bitmap("icons/SaveAs-16.png", wx.BITMAP_TYPE_PNG))
		fileMenu.AppendItem(saveAsMenuItem)

		saveSelectionMenuItem = wx.MenuItem(fileMenu, ID_SaveSelectionMenuItem, "Save Selection", "", wx.ITEM_NORMAL)
		fileMenu.AppendItem(saveSelectionMenuItem)

		fileMenu.AppendSeparator()

		closeMenuItem = wx.MenuItem(fileMenu, ID_CloseMenuItem, "Close", "", wx.ITEM_NORMAL)
		closeMenuItem.SetBitmap(wx.Bitmap("icons/Close-16.png", wx.BITMAP_TYPE_PNG))
		fileMenu.AppendItem(closeMenuItem)

		closeAllMenuItem = wx.MenuItem(fileMenu, ID_CloseAllMenuItem, "Close All", "", wx.ITEM_NORMAL)
		fileMenu.AppendItem(closeAllMenuItem)

		exitMenuItem = wx.MenuItem(fileMenu, ID_ExitMenuItem, "Exit\tCtrl+Q", "", wx.ITEM_NORMAL)
		fileMenu.AppendItem(exitMenuItem)

		return fileMenu

	def CreateEditMenu(self):
		editMenu = wx.Menu()
		undoMenuItem = wx.MenuItem(editMenu, ID_CloseMenuItem, "Undo", "", wx.ITEM_NORMAL)
		undoMenuItem.SetBitmap(wx.Bitmap("icons/Undo-16.png", wx.BITMAP_TYPE_PNG))
		editMenu.AppendItem(undoMenuItem)

		redoMenuItem = wx.MenuItem(editMenu, ID_CloseMenuItem, "Redo", "", wx.ITEM_NORMAL)
		redoMenuItem.SetBitmap(wx.Bitmap("icons/Redo-16.png", wx.BITMAP_TYPE_PNG))
		editMenu.AppendItem(redoMenuItem)

		editMenu.AppendSeparator()

		cutMenuItem = wx.MenuItem(editMenu, ID_CloseMenuItem, "Cut", "", wx.ITEM_NORMAL)
		cutMenuItem.SetBitmap(wx.Bitmap("icons/Cut-16.png", wx.BITMAP_TYPE_PNG))
		editMenu.AppendItem(cutMenuItem)

		copyMenuItem = wx.MenuItem(editMenu, ID_CloseMenuItem, "Copy", "", wx.ITEM_NORMAL)
		copyMenuItem.SetBitmap(wx.Bitmap("icons/Copy-16.png", wx.BITMAP_TYPE_PNG))
		editMenu.AppendItem(copyMenuItem)

		pasteMenuItem = wx.MenuItem(editMenu, ID_CloseMenuItem, "Paste", "", wx.ITEM_NORMAL)
		pasteMenuItem.SetBitmap(wx.Bitmap("icons/Paste-16.png", wx.BITMAP_TYPE_PNG))
		editMenu.AppendItem(pasteMenuItem)

		deleteMenuItem = wx.MenuItem(editMenu, ID_CloseMenuItem, "Delete", "", wx.ITEM_NORMAL)
		deleteMenuItem.SetBitmap(wx.Bitmap("icons/Delete-16.png", wx.BITMAP_TYPE_PNG))
		editMenu.AppendItem(deleteMenuItem)
		return editMenu

	def CreateViewMenu(self):
		viewMenu = wx.Menu()
		modeMenu = wx.Menu()
		blockSize = wx.Menu()



		return viewMenu

	def CreateImageMenu(self):
		imageMenu = wx.Menu()
		return imageMenu

	def CreateNavigateMenu(self):
		navigateMenu = wx.Menu()
		return navigateMenu

	def CreateHelpMenu(self):
		helpMenu = wx.Menu()

		helpTopicsItem = wx.MenuItem(helpMenu, ID_HelpTopicsMenuItem, "Help Topics\tF1", "", wx.ITEM_NORMAL)
		helpMenu.AppendItem(helpTopicsItem)

		aboutTopicsItem = wx.MenuItem(helpMenu, ID_AboutMenuItem, "About Tilem", "", wx.ITEM_NORMAL)
		helpMenu.AppendItem(aboutTopicsItem)

		return helpMenu

#####
# Event handlers
#####
	def OnExit(self, evt):
		self.Close(True)


	def OnNewWindow(self, evt):
		
		self.winCount = self.winCount + 1
		win = wx.MDIChildFrame(self, -1, "Child Window: %d" % self.winCount)
		canvas = ScrolledWindow.MyCanvas(win)
		win.Show(True)


	def OnEraseBackground(self, evt):
		dc = evt.GetDC()
		evt.GetId()
		if not dc:
			dc = wx.ClientDC(self.GetClientWindow())

		# tile the background bitmap
		sz = self.GetClientSize()
		w = self.bg_bmp.GetWidth()
		h = self.bg_bmp.GetHeight()
		x = 0

		while x < sz.width:
			y = 0

			while y < sz.height:
				dc.DrawBitmap(self.bg_bmp, x, y)
				y = y + h

			x = x + w


#----------------------------------------------------------------------

if __name__ == '__main__':
	class MyApp(wx.App):
		def OnInit(self):
			wx.InitAllImageHandlers()
			frame = TilemFrame()
			frame.Show(True)
			self.SetTopWindow(frame)
			return True


	app = MyApp(False)
	app.MainLoop()

