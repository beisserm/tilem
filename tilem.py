#!/usr/bin/env python

__author__="Matt Beisser"
__date__ ="$Oct 16, 2009 6:33:40 PM$"

import canvas
import images
import numpy
import palette
import wx

from dialogs.gotoAddressDialog import GotoDialog
from dialogs.canvasSizeDialog import CanvasSizeDialog
from dialogs.tileSizeDialog import TileSizeDialog
from dialogs.newFileDialog import NewFileDialog
from dialogs.aboutDialog import AboutDialog
from ToolPanel import ToolPanel
from cubecolourdialog import CubeColourDialog

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
ID_CanvasSizeMenuItem = wx.NewId()
ID_SelectionSizeMenuItem = wx.NewId()
ID_TileSizeMenuItem = wx.NewId()
ID_TileGridMenuItem = wx.NewId()
ID_PixelGridMenuItem = wx.NewId()

# Image Menu Ids
ID_FlipHorizontalMenuItem = wx.NewId()
ID_FlipVerticalMenuItem = wx.NewId()
ID_RotateClockwiseMenuItem = wx.NewId()
ID_RotateCounterClockwiseMenuItem = wx.NewId()

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

ID_SidePanel = wx.NewId()
#----------------------------------------------------------------------

romFileTypes = "All supported formats|*.chr;*.fds;*.fig;*.gb;*.gba;*.gbc;*.gg;*.md;*.n64;*.nes;\
*.ngp;*.ngpc;*.pce;*.sfc;*.sgb;*.smc;*.smd;*.sms;*.v64;*.vb;*.ws;*.wsc;*.xdf;*.z64|\
Famicon (*.fds)|*.fds|\
Game Gear (*.gg)|*.gg|\
GameBoy (*.gb, *.gbc, *.sgb)|*.gb;*.gbc;*.sgb|\
GameBoy Advance (*.gba)|*.gba|\
NeoGeo Pocket (*.ngp, *.ngpc)|*.ngp;*.ngpc|\
Nintendo (*.nes, *.chr)|*.nes;*.chr|\
Nintendo 64 (*.n64, *.v64, *.z64)|*.n64;*.v64;*.z64|\
Sega Genesis (*.smd, *.md)|*.smd;*.md|\
Sega Master System (*.sms)|*.sms|\
Super Nintendo (*.fig, *.sfc, *.smc)|*.fig;*.sfc;*.smc|\
Turbo Grafx-16 (*.pce)|*.pce|\
Virtual Boy (*.vb)|*.vb|\
WonderSwan (*.ws, *.wsc)|*.ws;*.wsc|\
X68000 (*.xdf)|*.xdf|\
All files (*.*)|*.*"
#--------------


class TilemFrame(wx.MDIParentFrame):
    def __init__(self):

	wx.MDIParentFrame.__init__(self, None, -1, "Tilem", size=(640, 480))

	self.winCount = 0
	self.paletteFrame = palette.PaletteFrame(self)
	#self.Bind(pue.EVT_PALETTE_UPDATE, self.OnUpdateColorPaletteEntry, id=self.GetId())
	self.toolPanel = ToolPanel(self)	
	
	self.tb1 = self.CreateTopToolBar()
	
	# Setup our menubar
	menubar = wx.MenuBar()
	menubar.Append(self.CreateFileMenu(), "File")
	menubar.Append(self.CreateEditMenu(), "Edit")
	menubar.Append(self.CreateViewMenu(), "View")
	menubar.Append(self.CreateImageMenu(), "Image")
	menubar.Append(self.CreateNavigateMenu(), "Navigate")
	self.SetMenuBar(menubar)
	menubar.Append(self.CreateHelpMenu(), "Help")

	self.SetClientSize(wx.Size(400, 400))

	#Show background
	self.bg_bmp = images.GridBG.GetBitmap()
	self.GetClientWindow().Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)

    def CreateTopToolBar(self):
	toolbar = self.CreateToolBar()
	
	entries = [["New",  "icons/new-16.png",    self.OnNew],
                   ["Open", "icons/open-16.png",   self.OnOpen],
                   ["Save", "icons/saveAs-16.png", self.OnSaveAs],
                   ["", "", ""],
                   ["Cut",   "icons/cut-16.png",   self.OnCut],
                   ["Copy",  "icons/copy-16.png",  self.OnCopy],
                   ["Paste", "icons/paste-16.png", self.OnPaste],
                   ["", "", "", ""],
                   ["Undo", "icons/undo-16.png", self.OnUndo],
                   ["Redo", "icons/redo-16.png", self.OnRedo],
                   ["", "", ""]]	
		
	for item in entries:
		
	    label = item[0]
	    icon = item[1]
	    handler = item[2]
	    
	    if not label:
		toolbar.AddSeparator()
	    else:
		bmp = wx.Bitmap(icon, wx.BITMAP_TYPE_PNG)
		tool = toolbar.AddSimpleTool(id=-1, bitmap=bmp, shortHelpString=label)
		self.Bind(wx.EVT_MENU, handler, tool)
		    
	toolbar.Realize()

	return toolbar


    def CreateFileMenu(self):
	"""
	Creates the 'File' menu on the menu bar
	"""
	fileMenu = wx.Menu()

	newMenuItem = wx.MenuItem(fileMenu, ID_NewMenuItem, "New...\tCtrl+N", "New...", wx.ITEM_NORMAL)
	newMenuItem.SetBitmap(wx.Bitmap("icons/new-16.png", wx.BITMAP_TYPE_PNG))
	fileMenu.AppendItem(newMenuItem)
	self.Bind(wx.EVT_MENU, self.OnNew, newMenuItem)

	openMenuItem = wx.MenuItem(fileMenu, ID_OpenMenuItem, "Open...\tCtrl+O", "Open...", wx.ITEM_NORMAL)
	openMenuItem.SetBitmap(wx.Bitmap("icons/open-16.png", wx.BITMAP_TYPE_PNG))
	fileMenu.AppendItem(openMenuItem)
	self.Bind(wx.EVT_MENU, self.OnOpen, openMenuItem)

	reOpenMenuItem = wx.MenuItem(fileMenu, ID_ReopenMenuItem, "Reopen", "", wx.ITEM_NORMAL)
	fileMenu.AppendItem(reOpenMenuItem)
	self.Bind(wx.EVT_MENU, self.OnReopen, reOpenMenuItem)

	importImageMenuItem = wx.MenuItem(fileMenu, ID_ImportImageMenuItem, "Import Image", "", wx.ITEM_NORMAL)
	fileMenu.AppendItem(importImageMenuItem)
	self.Bind(wx.EVT_MENU, self.OnImportImage, importImageMenuItem)

	fileMenu.AppendSeparator()

	saveMenuItem = wx.MenuItem(fileMenu, ID_SaveMenuItem, "Save\tCtrl+S", "New...", wx.ITEM_NORMAL)
	saveMenuItem.SetBitmap(wx.Bitmap("icons/save-16.png", wx.BITMAP_TYPE_PNG))
	fileMenu.AppendItem(saveMenuItem)		
	self.Bind(wx.EVT_MENU, self.OnSave, saveMenuItem)

	saveAsMenuItem = wx.MenuItem(fileMenu, ID_SaveAsMenuItem, "Save As...\tCtrl+Shift+S", "Save As", wx.ITEM_NORMAL)
	saveAsMenuItem.SetBitmap(wx.Bitmap("icons/saveAs-16.png", wx.BITMAP_TYPE_PNG))
	fileMenu.AppendItem(saveAsMenuItem)
	self.Bind(wx.EVT_MENU, self.OnSaveAs, saveAsMenuItem)

	saveSelectionMenuItem = wx.MenuItem(fileMenu, ID_SaveSelectionMenuItem, "Save Selection", "", wx.ITEM_NORMAL)
	fileMenu.AppendItem(saveSelectionMenuItem)
	self.Bind(wx.EVT_MENU, self.OnSaveSelection, saveSelectionMenuItem)

	fileMenu.AppendSeparator()

	closeMenuItem = wx.MenuItem(fileMenu, ID_CloseMenuItem, "Close", "", wx.ITEM_NORMAL)
	closeMenuItem.SetBitmap(wx.Bitmap("icons/close-16.png", wx.BITMAP_TYPE_PNG))
	fileMenu.AppendItem(closeMenuItem)
	self.Bind(wx.EVT_MENU, self.OnClose, closeMenuItem)

	closeAllMenuItem = wx.MenuItem(fileMenu, ID_CloseAllMenuItem, "Close All", "", wx.ITEM_NORMAL)
	fileMenu.AppendItem(closeAllMenuItem)
	self.Bind(wx.EVT_MENU, self.OnCloseAll, closeAllMenuItem)

	exitMenuItem = wx.MenuItem(fileMenu, ID_ExitMenuItem, "Exit\tCtrl+Q", "", wx.ITEM_NORMAL)
	fileMenu.AppendItem(exitMenuItem)
	self.Bind(wx.EVT_MENU, self.OnExit, exitMenuItem)

	return fileMenu

    def CreateEditMenu(self):
	"""
	Creates the 'Edit' menu on the menu bar
	"""		
	editMenu = wx.Menu()
	
	undoMenuItem = wx.MenuItem(editMenu, ID_UndoMenuItem, "Undo", "", wx.ITEM_NORMAL)
	undoMenuItem.SetBitmap(wx.Bitmap("icons/undo-16.png", wx.BITMAP_TYPE_PNG))
	editMenu.AppendItem(undoMenuItem)
	self.Bind(wx.EVT_MENU, self.OnUndo, undoMenuItem)

	redoMenuItem = wx.MenuItem(editMenu, ID_RedoMenuItem, "Redo", "", wx.ITEM_NORMAL)
	redoMenuItem.SetBitmap(wx.Bitmap("icons/redo-16.png", wx.BITMAP_TYPE_PNG))
	editMenu.AppendItem(redoMenuItem)
	self.Bind(wx.EVT_MENU, self.OnRedo, redoMenuItem)

	editMenu.AppendSeparator()

	cutMenuItem = wx.MenuItem(editMenu, ID_CutMenuItem, "Cut", "", wx.ITEM_NORMAL)
	cutMenuItem.SetBitmap(wx.Bitmap("icons/cut-16.png", wx.BITMAP_TYPE_PNG))
	editMenu.AppendItem(cutMenuItem)
	self.Bind(wx.EVT_MENU, self.OnCut, cutMenuItem)

	copyMenuItem = wx.MenuItem(editMenu, ID_CopyMenuItem, "Copy", "", wx.ITEM_NORMAL)
	copyMenuItem.SetBitmap(wx.Bitmap("icons/copy-16.png", wx.BITMAP_TYPE_PNG))
	editMenu.AppendItem(copyMenuItem)
	self.Bind(wx.EVT_MENU, self.OnCopy, copyMenuItem)

	pasteMenuItem = wx.MenuItem(editMenu, ID_PasteMenuItem, "Paste", "", wx.ITEM_NORMAL)
	pasteMenuItem.SetBitmap(wx.Bitmap("icons/paste-16.png", wx.BITMAP_TYPE_PNG))
	editMenu.AppendItem(pasteMenuItem)
	self.Bind(wx.EVT_MENU, self.OnPaste, pasteMenuItem)

	deleteMenuItem = wx.MenuItem(editMenu, ID_DeleteMenuItem, "Delete", "", wx.ITEM_NORMAL)
	deleteMenuItem.SetBitmap(wx.Bitmap("icons/delete-16.png", wx.BITMAP_TYPE_PNG))
	editMenu.AppendItem(deleteMenuItem)
	self.Bind(wx.EVT_MENU, self.OnDelete, deleteMenuItem)
	
	return editMenu

    def CreateViewMenu(self):
	"""
	Creates the 'View' menu on the menu bar
	"""		
	viewMenu = wx.Menu()

	modeMenu = wx.Menu()
	oneDimensionalMenuItem = wx.MenuItem(modeMenu, ID_1dModeMenuItem, "1 Dimensional", "", wx.ITEM_RADIO)
	modeMenu.AppendItem(oneDimensionalMenuItem)
	twoDimensionalMenuItem = wx.MenuItem(modeMenu, ID_2dModeMenuItem, "2 Dimensional", "", wx.ITEM_RADIO)
	modeMenu.AppendItem(twoDimensionalMenuItem)
	#self.Bind(wx.EVT_MENU, self., )
	viewMenu.AppendMenu(-1, "Mode", modeMenu)

	viewMenu.AppendSeparator()

	blockSizeMenu = wx.Menu()
	fullCanvasMenuItem = wx.MenuItem(blockSizeMenu, ID_FullCanvasBlockSizeMenuItem, "Full Canvas", "", wx.ITEM_RADIO)
	blockSizeMenu.AppendItem(fullCanvasMenuItem)
	customCanvasMenuItem = wx.MenuItem(blockSizeMenu, ID_CustomBlockSizeMenuItem, "Custom", "", wx.ITEM_RADIO)
	blockSizeMenu.AppendItem(customCanvasMenuItem)
	#self.Bind(wx.EVT_MENU, self.OnBlockSize, fullCanvasMenuItem)
	self.Bind(wx.EVT_MENU, self.OnBlockSize, customCanvasMenuItem)
	viewMenu.AppendMenu(-1, "Block Size", blockSizeMenu)

	rowInterleavedBlocksMenuItem = wx.MenuItem(viewMenu, ID_RowInterleaveBlocksMenuItem, "Row-interleave Blocks", "", wx.ITEM_CHECK)
	viewMenu.AppendItem(rowInterleavedBlocksMenuItem)
	self.Bind(wx.EVT_MENU, self.OnRowInterleaveBlocks, rowInterleavedBlocksMenuItem)
	rowInterleavedBlocksMenuItem.Enable(False)
	
	viewMenu.AppendSeparator()

	canvasSizeMenuItem = wx.MenuItem(viewMenu, ID_CanvasSizeMenuItem, "Canvas Size...", "", wx.ITEM_NORMAL)
	viewMenu.AppendItem(canvasSizeMenuItem)
	self.Bind(wx.EVT_MENU, self.OnCanvasSize, canvasSizeMenuItem)

	tileSizeMenuItem = wx.MenuItem(viewMenu, ID_TileSizeMenuItem, "Tile Size...", "", wx.ITEM_NORMAL)
	viewMenu.AppendItem(tileSizeMenuItem)
	self.Bind(wx.EVT_MENU, self.OnTileSize, tileSizeMenuItem)	

	selectionSizeMenuItem = wx.MenuItem(viewMenu, ID_SelectionSizeMenuItem, "Selection Size...", "", wx.ITEM_NORMAL)
	viewMenu.AppendItem(selectionSizeMenuItem)
	self.Bind(wx.EVT_MENU, self.OnSelectionSize, selectionSizeMenuItem)
	selectionSizeMenuItem.Enable(False)
	
	viewMenu.AppendSeparator()

	blockGridMenuItem = wx.MenuItem(modeMenu, ID_BlockGridMenuItem, "Block Grid", "", wx.ITEM_CHECK)
	viewMenu.AppendItem(blockGridMenuItem)
	self.Bind(wx.EVT_MENU, self.OnShowBlockGrid, blockGridMenuItem)
	blockGridMenuItem.Enable(False)

	tileGridMenuItem = wx.MenuItem(modeMenu, ID_TileGridMenuItem, "Tile Grid", "", wx.ITEM_CHECK)
	viewMenu.AppendItem(tileGridMenuItem)
	self.Bind(wx.EVT_MENU, self.OnShowTileGrid, tileGridMenuItem)

	pixelGridMenuItem = wx.MenuItem(modeMenu, ID_PixelGridMenuItem, "Pixel Grid", "", wx.ITEM_CHECK)
	viewMenu.AppendItem(pixelGridMenuItem)
	self.Bind(wx.EVT_MENU, self.OnShowPixelGrid, pixelGridMenuItem)

	return viewMenu

    def CreateImageMenu(self):
	"""
	Creates the 'Image' menu on the menu bar
	"""		
	imageMenu = wx.Menu()

	flipHorizontalMenuItem = wx.MenuItem(imageMenu, ID_FlipHorizontalMenuItem, "Flip Horizontal", "", wx.ITEM_NORMAL)
	flipHorizontalMenuItem.SetBitmap(wx.Bitmap("icons/horizontal-flip-16.png", wx.BITMAP_TYPE_PNG))
	imageMenu.AppendItem(flipHorizontalMenuItem)
	self.Bind(wx.EVT_MENU, self.OnFlipHorizontal, flipHorizontalMenuItem)

	flipVerticalMenuItem = wx.MenuItem(imageMenu, ID_FlipVerticalMenuItem, "Flip Vertical", "", wx.ITEM_NORMAL)
	flipVerticalMenuItem.SetBitmap(wx.Bitmap("icons/vertical-flip-16.png", wx.BITMAP_TYPE_PNG))
	imageMenu.AppendItem(flipVerticalMenuItem)
	self.Bind(wx.EVT_MENU, self.OnFlipVertical, flipVerticalMenuItem)

	imageMenu.AppendSeparator()

	rotateRightMenuItem = wx.MenuItem(imageMenu, ID_RotateClockwiseMenuItem, "Rotate 90 Degrees Clockwise", "", wx.ITEM_NORMAL)
	rotateRightMenuItem.SetBitmap(wx.Bitmap("icons/rotate-right-16.png", wx.BITMAP_TYPE_PNG))
	imageMenu.AppendItem(rotateRightMenuItem)
	self.Bind(wx.EVT_MENU, self.OnRotateClockwise, rotateRightMenuItem)

	rotateLeftMenuItem = wx.MenuItem(imageMenu, ID_RotateCounterClockwiseMenuItem, "Rotate 90 Degrees Counter-Clockwise", "", wx.ITEM_NORMAL)
	rotateLeftMenuItem.SetBitmap(wx.Bitmap("icons/rotate-left-16.png", wx.BITMAP_TYPE_PNG))
	imageMenu.AppendItem(rotateLeftMenuItem)
	self.Bind(wx.EVT_MENU, self.OnRotateCounterClockwise, rotateLeftMenuItem)

	return imageMenu

    def CreateNavigateMenu(self):
	"""
	Creates the 'Navigate' menu on the menu bar
	"""		
	navigateMenu = wx.Menu()

	gotoMenuItem = wx.MenuItem(navigateMenu, ID_GotoAddressMenuItem, "Goto Address\tCtrl+G", "", wx.ITEM_NORMAL)
	navigateMenu.AppendItem(gotoMenuItem)
	self.Bind(wx.EVT_MENU, self.OnGoto, gotoMenuItem)

	navigateMenu.AppendSeparator()

	addBookmarkMenuItem = wx.MenuItem(navigateMenu, ID_AddBookMarkMenuItem, "Add Bookmark", "", wx.ITEM_NORMAL)
	navigateMenu.AppendItem(addBookmarkMenuItem)
	self.Bind(wx.EVT_MENU, self.OnAddBookmark, addBookmarkMenuItem)
	addBookmarkMenuItem.Enable(False)

	organizeBookmarksMenuItem = wx.MenuItem(navigateMenu, ID_OrganizeBookmarksMenuItem, "Organize Bookmarks", "", wx.ITEM_NORMAL)
	navigateMenu.AppendItem(organizeBookmarksMenuItem)
	self.Bind(wx.EVT_MENU, self.OnOrganizeBookmarks, organizeBookmarksMenuItem)
	organizeBookmarksMenuItem.Enable(False)

	return navigateMenu

    def CreateHelpMenu(self):
	"""
	Creates the 'Help' menu on the menu bar
	"""		
	helpMenu = wx.Menu()

	helpTopicsItem = wx.MenuItem(helpMenu, ID_HelpTopicsMenuItem, "Help Topics\tF1", "", wx.ITEM_NORMAL)
	helpMenu.AppendItem(helpTopicsItem)
	self.Bind(wx.EVT_MENU, self.OnHelpTopics, helpTopicsItem)
	helpTopicsItem.Enable(False)

	aboutTopicsItem = wx.MenuItem(helpMenu, ID_AboutMenuItem, "About Tilem", "", wx.ITEM_NORMAL)
	helpMenu.AppendItem(aboutTopicsItem)
	self.Bind(wx.EVT_MENU, self.OnAbout, aboutTopicsItem)

	return helpMenu

#####
# Event handlers
#####

#File Menu Events
    def OnNew(self, evt):
	'''
	Handles the 'New File' menu option. This may go away in the future
	'''
	newFileDlg = NewFileDialog(self)
	if newFileDlg.ShowModal() == wx.ID_OK:
	    size = newFileDlg.GetSize()
	    win = canvas.CanvasFrame(self, fileSize=size)
	    win.Show(True)
	    self.winCount = self.winCount + 1
	
	newFileDlg.Destroy()

    def OnOpen(self, evt):
	openDialog = wx.FileDialog(self, "Choose a file", "", "", romFileTypes, wx.OPEN )
	if openDialog.ShowModal() == wx.ID_OK:
	    try:
		selectedFile = openDialog.GetPath() #= open(name=openDialog.GetPath(), mode='rb')
		win = canvas.CanvasFrame(self, fileStr=selectedFile)
		win.Show(True)
		self.winCount = self.winCount + 1
	    except IOError:
		pass
	    
	openDialog.Destroy()	    
    
    def OnReopen(self, evt):
	print "OnReopen"

    def OnImportImage(self, evt):
	print "OnImportImage"

    def OnSave(self, evt):
	print "OnSave"

    def OnSaveAs(self, evt):
	print "OnSaveAs"

    def OnSaveSelection(self, evt):
	print "OnSaveSelection"

    def OnClose(self, evt):
	print "OnClose"

    def OnCloseAll(self, evt):
	print "OnCloseAll"

    def OnExit(self, evt):
	self.Close(True)

#Edit Menu Events
    def OnUndo(self, evt):
	print "OnUndo"

    def OnRedo(self, evt):
	print "OnRedo"

    def OnCut(self, evt):
	print "OnCut"

    def OnCopy(self, evt):
	print "OnCopy"

    def OnPaste(self, evt):
	print "OnPaste"

    def OnDelete(self, evt):
	print "OnDelete"

#View Menu Events
    def OnMode(self, evt):
	print "OnMode"

    def OnBlockSize(self, evt):
	print "OnBlockSize"

    def OnRowInterleaveBlocks(self, evt):
	print "OnRowInterleaveBlocks"

    def OnCanvasSize(self, evt):
	activeWindow = self.GetActiveChild()
	
	if activeWindow != None:
	    currentSize = activeWindow.GetCanvasSize()
	    dlg = CanvasSizeDialog(self, *currentSize)

	    if dlg.ShowModal() == wx.ID_OK:
		newSize = dlg.GetCanvasSize()
		activeWindow.SetCanvasSize(*newSize)
		
	    dlg.Destroy()

    def OnSelectionSize(self, evt):
	print "OnSelectionSize"	
	
    def OnTileSize(self, evt):
	'''
	Handles the tile size menu option
	'''
	activeWindow = self.GetActiveChild()
	
	if activeWindow != None:
	    currentSize = activeWindow.GetTileSize()
	    dlg = TileSizeDialog(self, *currentSize)

	    if dlg.ShowModal() == wx.ID_OK:
		newSize = dlg.GetTileSize()
		activeWindow.SetTileSize(*newSize)
		
	    dlg.Destroy()
	
    def OnShowBlockGrid(self, evt):
	value = evt.IsChecked()
	print value
	print "OnShowBlockGrid"

    def OnShowTileGrid(self, evt):
	value = evt.IsChecked()	
	activeWindow = self.GetActiveChild()
	
	if activeWindow != None:
	    currentSize = activeWindow.SetTileGrid(value)

    def OnShowPixelGrid(self, evt):
	value = evt.IsChecked()	
	activeWindow = self.GetActiveChild()
	
	if activeWindow != None:
	    currentSize = activeWindow.SetPixelGrid(value)

    def OnShowColorPalette(self, evt):
	print "OnShowColorPalette"

    def OnShowStatusbar(self, evt):
	print "OnShowStatusbar"

    def OnShowToolbar(self, evt):
	value = evt.IsChecked()	
	print "OnShowToolbar"

#Image
    def OnFlipHorizontal(self, evt):
	print "OnFlipHorizontal"

    def OnFlipVertical(self, evt):
	print "OnFlipVertical"

    def OnRotateClockwise(self, evt):
	print "OnRotateClockwise"

    def OnRotateCounterClockwise(self, evt):
	print "OnRotateCounterClockwise"

#Navigate
    def OnGoto(self, evt):
	dialog = GotoDialog(self)

	if dialog.ShowModal() == wx.ID_OK:
	    pass

	dialog.Destroy()
#		   selected = dialog.GetSelections()
#		   for selection in selected:
#			  print str ( selection ) + ': ' + choices [ selection ]

		# The user exited the dialog without pressing the "OK" button
#		else:
#                    print 'bye'
#                    dialog.Destroy()

    def OnAddBookmark(self, evt):
	print "OnAddBookmark"

    def OnOrganizeBookmarks(self, evt):
	print "OnOrganizeBookmarks"

    def OnHelpTopics(self, evt):
	print "OnHelpTopics"

    def OnAbout(self, evt):
	AboutDialog()
#Help

# Others
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

    def OnColorPaletteUpdate(self):
	'''
	TODO: Make actual event
	Event from the PaletteFrame. A color on the palette has been changed.
	Triggers a redraw
	'''
	activeWindow = self.GetActiveChild()
	
	if activeWindow != None:
	    currentSize = activeWindow.OnPaletteUpdate()

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
