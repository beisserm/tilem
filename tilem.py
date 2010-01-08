#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

__author__="Matt Beisser"
__date__ ="$Oct 16, 2009 6:33:40 PM$"

from dialogs.gotoAddressDialog import GotoDialog
from dialogs.canvasSizeDialog import CanvasSizeDialog
from dialogs.newFileDialog import NewFileDialog
from ToolPanel import ToolPanel
from cubecolourdialog import CubeColourDialog

import wx
import numpy

#MDI child windows...
import canvas
import images

import palette

#EVT_ACTIVATE
#EVT_ACTIVATE_APP
#EVT_BUTTON
#EVT_CALCULATE_LAYOUT
#EVT_CHAR
#EVT_CHAR_HOOK
#EVT_CHECKBOX
#EVT_CHECKLISTBOX
#EVT_CHILD_FOCUS
#EVT_CHOICE
#EVT_CHOICEBOOK_PAGE_CHANGED
#EVT_CHOICEBOOK_PAGE_CHANGING
#EVT_CLOSE
#EVT_COLLAPSIBLEPANE_CHANGED
#EVT_COLOURPICKER_CHANGED
#EVT_COMBOBOX
#EVT_COMMAND
#EVT_COMMAND_ENTER
#EVT_COMMAND_FIND
#EVT_COMMAND_FIND_CLOSE
#EVT_COMMAND_FIND_NEXT
#EVT_COMMAND_FIND_REPLACE
#EVT_COMMAND_FIND_REPLACE_ALL
#EVT_COMMAND_KILL_FOCUS
#EVT_COMMAND_LEFT_CLICK
#EVT_COMMAND_LEFT_DCLICK
#EVT_COMMAND_RANGE
#EVT_COMMAND_RIGHT_CLICK
#EVT_COMMAND_RIGHT_DCLICK
#EVT_COMMAND_SCROLL
#EVT_COMMAND_SCROLL_BOTTOM
#EVT_COMMAND_SCROLL_CHANGED
#EVT_COMMAND_SCROLL_ENDSCROLL
#EVT_COMMAND_SCROLL_LINEDOWN
#EVT_COMMAND_SCROLL_LINEUP
#EVT_COMMAND_SCROLL_PAGEDOWN
#EVT_COMMAND_SCROLL_PAGEUP
#EVT_COMMAND_SCROLL_THUMBRELEASE
#EVT_COMMAND_SCROLL_THUMBTRACK
#EVT_COMMAND_SCROLL_TOP
#EVT_COMMAND_SET_FOCUS
#EVT_CONTEXT_MENU
#EVT_DATE_CHANGED
#EVT_DETAILED_HELP
#EVT_DETAILED_HELP_RANGE
#EVT_DIRPICKER_CHANGED
#EVT_DISPLAY_CHANGED
#EVT_DROP_FILES
#EVT_END_PROCESS
#EVT_END_SESSION
#EVT_ENTER_WINDOW
#EVT_ERASE_BACKGROUND
#EVT_FILEPICKER_CHANGED
#EVT_FIND
#EVT_FIND_CLOSE
#EVT_FIND_NEXT
#EVT_FIND_REPLACE
#EVT_FIND_REPLACE_ALL
#EVT_FONTPICKER_CHANGED
#EVT_HELP
#EVT_HELP_RANGE
#EVT_HIBERNATE
#EVT_HOTKEY
#EVT_HYPERLINK
#EVT_ICONIZE
#EVT_IDLE
#EVT_INIT_DIALOG
#EVT_JOYSTICK_EVENTS
#EVT_JOY_BUTTON_DOWN
#EVT_JOY_BUTTON_UP
#EVT_JOY_MOVE
#EVT_JOY_ZMOVE
#EVT_KEY_DOWN
#EVT_KEY_UP
#EVT_KILL_FOCUS
#EVT_LEAVE_WINDOW
#EVT_LEFT_DCLICK
#EVT_LEFT_DOWN
#EVT_LEFT_UP
#EVT_LISTBOOK_PAGE_CHANGED
#EVT_LISTBOOK_PAGE_CHANGING
#EVT_LISTBOX
#EVT_LISTBOX_DCLICK
#EVT_LIST_BEGIN_DRAG
#EVT_LIST_BEGIN_LABEL_EDIT
#EVT_LIST_BEGIN_RDRAG
#EVT_LIST_CACHE_HINT
#EVT_LIST_COL_BEGIN_DRAG
#EVT_LIST_COL_CLICK
#EVT_LIST_COL_DRAGGING
#EVT_LIST_COL_END_DRAG
#EVT_LIST_COL_RIGHT_CLICK
#EVT_LIST_DELETE_ALL_ITEMS
#EVT_LIST_DELETE_ITEM
#EVT_LIST_END_LABEL_EDIT
#EVT_LIST_INSERT_ITEM
#EVT_LIST_ITEM_ACTIVATED
#EVT_LIST_ITEM_DESELECTED
#EVT_LIST_ITEM_FOCUSED
#EVT_LIST_ITEM_MIDDLE_CLICK
#EVT_LIST_ITEM_RIGHT_CLICK
#EVT_LIST_ITEM_SELECTED
#EVT_LIST_KEY_DOWN
#EVT_MAXIMIZE
#EVT_MENU
#EVT_MENU_CLOSE
#EVT_MENU_HIGHLIGHT
#EVT_MENU_HIGHLIGHT_ALL
#EVT_MENU_OPEN
#EVT_MENU_RANGE
#EVT_MIDDLE_DCLICK
#EVT_MIDDLE_DOWN
#EVT_MIDDLE_UP
#EVT_MOTION
#EVT_MOUSEWHEEL
#EVT_MOUSE_CAPTURE_CHANGED
#EVT_MOUSE_CAPTURE_LOST
#EVT_MOUSE_EVENTS
#EVT_MOVE
#EVT_MOVING
#EVT_NAVIGATION_KEY
#EVT_NC_PAINT
#EVT_NOTEBOOK_PAGE_CHANGED
#EVT_NOTEBOOK_PAGE_CHANGING
#EVT_PAINT
#EVT_PALETTE_CHANGED
#EVT_POWER_RESUME
#EVT_POWER_SUSPENDED
#EVT_POWER_SUSPENDING
#EVT_POWER_SUSPEND_CANCEL
#EVT_QUERY_END_SESSION
#EVT_QUERY_LAYOUT_INFO
#EVT_QUERY_NEW_PALETTE
#EVT_RADIOBOX
#EVT_RADIOBUTTON
#EVT_RIGHT_DCLICK
#EVT_RIGHT_DOWN
#EVT_RIGHT_UP
#EVT_SASH_DRAGGED
#EVT_SASH_DRAGGED_RANGE
#EVT_SCROLL
#EVT_SCROLLBAR
#EVT_SCROLLWIN
#EVT_SCROLLWIN_BOTTOM
#EVT_SCROLLWIN_LINEDOWN
#EVT_SCROLLWIN_LINEUP
#EVT_SCROLLWIN_PAGEDOWN
#EVT_SCROLLWIN_PAGEUP
#EVT_SCROLLWIN_THUMBRELEASE
#EVT_SCROLLWIN_THUMBTRACK
#EVT_SCROLLWIN_TOP
#EVT_SCROLL_BOTTOM
#EVT_SCROLL_CHANGED
#EVT_SCROLL_ENDSCROLL
#EVT_SCROLL_LINEDOWN
#EVT_SCROLL_LINEUP
#EVT_SCROLL_PAGEDOWN
#EVT_SCROLL_PAGEUP
#EVT_SCROLL_THUMBRELEASE
#EVT_SCROLL_THUMBTRACK
#EVT_SCROLL_TOP
#EVT_SEARCHCTRL_CANCEL_BTN
#EVT_SEARCHCTRL_SEARCH_BTN
#EVT_SET_CURSOR
#EVT_SET_FOCUS
#EVT_SHOW
#EVT_SIZE
#EVT_SIZING
#EVT_SLIDER
#EVT_SPIN
#EVT_SPINCTRL
#EVT_SPIN_DOWN
#EVT_SPIN_UP
#EVT_SPLITTER_DCLICK
#EVT_SPLITTER_DOUBLECLICKED
#EVT_SPLITTER_SASH_POS_CHANGED
#EVT_SPLITTER_SASH_POS_CHANGING
#EVT_SPLITTER_UNSPLIT
#EVT_SYS_COLOUR_CHANGED
#EVT_TASKBAR_CLICK
#EVT_TASKBAR_LEFT_DCLICK
#EVT_TASKBAR_LEFT_DOWN
#EVT_TASKBAR_LEFT_UP
#EVT_TASKBAR_MOVE
#EVT_TASKBAR_RIGHT_DCLICK
#EVT_TASKBAR_RIGHT_DOWN
#EVT_TASKBAR_RIGHT_UP
#EVT_TEXT
#EVT_TEXT_COPY
#EVT_TEXT_CUT
#EVT_TEXT_ENTER
#EVT_TEXT_MAXLEN
#EVT_TEXT_PASTE
#EVT_TEXT_URL
#EVT_TIMER
#EVT_TOGGLEBUTTON
#EVT_TOOL
#EVT_TOOLBOOK_PAGE_CHANGED
#EVT_TOOLBOOK_PAGE_CHANGING
#EVT_TOOL_ENTER
#EVT_TOOL_RANGE
#EVT_TOOL_RCLICKED
#EVT_TOOL_RCLICKED_RANGE
#EVT_TREEBOOK_NODE_COLLAPSED
#EVT_TREEBOOK_NODE_EXPANDED
#EVT_TREEBOOK_PAGE_CHANGED
#EVT_TREEBOOK_PAGE_CHANGING
#EVT_TREE_BEGIN_DRAG
#EVT_TREE_BEGIN_LABEL_EDIT
#EVT_TREE_BEGIN_RDRAG
#EVT_TREE_DELETE_ITEM
#EVT_TREE_END_DRAG
#EVT_TREE_END_LABEL_EDIT
#EVT_TREE_GET_INFO
#EVT_TREE_ITEM_ACTIVATED
#EVT_TREE_ITEM_COLLAPSED
#EVT_TREE_ITEM_COLLAPSING
#EVT_TREE_ITEM_EXPANDED
#EVT_TREE_ITEM_EXPANDING
#EVT_TREE_ITEM_GETTOOLTIP
#EVT_TREE_ITEM_MENU
#EVT_TREE_ITEM_MIDDLE_CLICK
#EVT_TREE_ITEM_RIGHT_CLICK
#EVT_TREE_KEY_DOWN
#EVT_TREE_SEL_CHANGED
#EVT_TREE_SEL_CHANGING
#EVT_TREE_SET_INFO
#EVT_TREE_STATE_IMAGE_CLICK
#EVT_UPDATE_UI
#EVT_UPDATE_UI_RANGE
#EVT_VLBOX
#EVT_WINDOW_CREATE
#EVT_WINDOW_DESTROY

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

	#self.Bind(wx.EVT_MENU, self.OnExit, id=ID_Exit)

	#Show background
	self.bg_bmp = images.GridBG.GetBitmap()
	self.GetClientWindow().Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)

    def CreateTopToolBar(self):
	toolbar = self.CreateToolBar()
	
	entries = [["New",  "icons/New-16.png",    self.OnNew],
                   ["Open", "icons/Open-16.png",   self.OnOpen],
                   ["Save", "icons/SaveAs-16.png", self.OnSaveAs],
                   ["", "", ""],
                   ["Cut",   "icons/Cut-16.png",   self.OnCut],
                   ["Copy",  "icons/Copy-16.png",  self.OnCopy],
                   ["Paste", "icons/Paste-16.png", self.OnPaste],
                   ["", "", "", ""],
                   ["Undo", "icons/Undo-16.png", self.OnUndo],
                   ["Redo", "icons/Redo-16.png", self.OnRedo],
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
	newMenuItem.SetBitmap(wx.Bitmap("icons/New-16.png", wx.BITMAP_TYPE_PNG))
	fileMenu.AppendItem(newMenuItem)
	self.Bind(wx.EVT_MENU, self.OnNew, newMenuItem)

	openMenuItem = wx.MenuItem(fileMenu, ID_OpenMenuItem, "Open...\tCtrl+O", "Open...", wx.ITEM_NORMAL)
	openMenuItem.SetBitmap(wx.Bitmap("icons/Open-16.png", wx.BITMAP_TYPE_PNG))
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
	saveMenuItem.SetBitmap(wx.Bitmap("icons/Save-16.png", wx.BITMAP_TYPE_PNG))
	fileMenu.AppendItem(saveMenuItem)		
	self.Bind(wx.EVT_MENU, self.OnSave, saveMenuItem)

	saveAsMenuItem = wx.MenuItem(fileMenu, ID_SaveAsMenuItem, "Save As...\tCtrl+Shift+S", "Save As", wx.ITEM_NORMAL)
	saveAsMenuItem.SetBitmap(wx.Bitmap("icons/SaveAs-16.png", wx.BITMAP_TYPE_PNG))
	fileMenu.AppendItem(saveAsMenuItem)
	self.Bind(wx.EVT_MENU, self.OnSaveAs, saveAsMenuItem)

	saveSelectionMenuItem = wx.MenuItem(fileMenu, ID_SaveSelectionMenuItem, "Save Selection", "", wx.ITEM_NORMAL)
	fileMenu.AppendItem(saveSelectionMenuItem)
	self.Bind(wx.EVT_MENU, self.OnSaveSelection, saveSelectionMenuItem)

	fileMenu.AppendSeparator()

	closeMenuItem = wx.MenuItem(fileMenu, ID_CloseMenuItem, "Close", "", wx.ITEM_NORMAL)
	closeMenuItem.SetBitmap(wx.Bitmap("icons/Close-16.png", wx.BITMAP_TYPE_PNG))
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
	undoMenuItem.SetBitmap(wx.Bitmap("icons/Undo-16.png", wx.BITMAP_TYPE_PNG))
	editMenu.AppendItem(undoMenuItem)
	self.Bind(wx.EVT_MENU, self.OnUndo, undoMenuItem)

	redoMenuItem = wx.MenuItem(editMenu, ID_RedoMenuItem, "Redo", "", wx.ITEM_NORMAL)
	redoMenuItem.SetBitmap(wx.Bitmap("icons/Redo-16.png", wx.BITMAP_TYPE_PNG))
	editMenu.AppendItem(redoMenuItem)
	self.Bind(wx.EVT_MENU, self.OnRedo, redoMenuItem)

	editMenu.AppendSeparator()

	cutMenuItem = wx.MenuItem(editMenu, ID_CutMenuItem, "Cut", "", wx.ITEM_NORMAL)
	cutMenuItem.SetBitmap(wx.Bitmap("icons/Cut-16.png", wx.BITMAP_TYPE_PNG))
	editMenu.AppendItem(cutMenuItem)
	self.Bind(wx.EVT_MENU, self.OnCut, cutMenuItem)

	copyMenuItem = wx.MenuItem(editMenu, ID_CopyMenuItem, "Copy", "", wx.ITEM_NORMAL)
	copyMenuItem.SetBitmap(wx.Bitmap("icons/Copy-16.png", wx.BITMAP_TYPE_PNG))
	editMenu.AppendItem(copyMenuItem)
	self.Bind(wx.EVT_MENU, self.OnCopy, copyMenuItem)

	pasteMenuItem = wx.MenuItem(editMenu, ID_PasteMenuItem, "Paste", "", wx.ITEM_NORMAL)
	pasteMenuItem.SetBitmap(wx.Bitmap("icons/Paste-16.png", wx.BITMAP_TYPE_PNG))
	editMenu.AppendItem(pasteMenuItem)
	self.Bind(wx.EVT_MENU, self.OnPaste, pasteMenuItem)

	deleteMenuItem = wx.MenuItem(editMenu, ID_DeleteMenuItem, "Delete", "", wx.ITEM_NORMAL)
	deleteMenuItem.SetBitmap(wx.Bitmap("icons/Delete-16.png", wx.BITMAP_TYPE_PNG))
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
	
	viewMenu.AppendSeparator()

	blockGridMenuItem = wx.MenuItem(modeMenu, ID_BlockGridMenuItem, "Block Grid", "", wx.ITEM_CHECK)
	viewMenu.AppendItem(blockGridMenuItem)
	self.Bind(wx.EVT_MENU, self.OnShowBlockGrid, blockGridMenuItem)

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

	rotateRightMenuItem = wx.MenuItem(imageMenu, ID_RotateClockwiseMenuItem, "Rotate 90° Clockwise", "", wx.ITEM_NORMAL)
	rotateRightMenuItem.SetBitmap(wx.Bitmap("icons/rotate-right-16.png", wx.BITMAP_TYPE_PNG))
	imageMenu.AppendItem(rotateRightMenuItem)
	self.Bind(wx.EVT_MENU, self.OnRotateClockwise, rotateRightMenuItem)

	rotateLeftMenuItem = wx.MenuItem(imageMenu, ID_RotateCounterClockwiseMenuItem, "Rotate 90° Counter-Clockwise", "", wx.ITEM_NORMAL)
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

	organizeBookmarksMenuItem = wx.MenuItem(navigateMenu, ID_OrganizeBookmarksMenuItem, "Organize Bookmarks", "", wx.ITEM_NORMAL)
	navigateMenu.AppendItem(organizeBookmarksMenuItem)
	self.Bind(wx.EVT_MENU, self.OnOrganizeBookmarks, organizeBookmarksMenuItem)

	return navigateMenu

    def CreateHelpMenu(self):
	"""
	Creates the 'Help' menu on the menu bar
	"""		
	helpMenu = wx.Menu()

	helpTopicsItem = wx.MenuItem(helpMenu, ID_HelpTopicsMenuItem, "Help Topics\tF1", "", wx.ITEM_NORMAL)
	helpMenu.AppendItem(helpTopicsItem)
	self.Bind(wx.EVT_MENU, self.OnHelpTopics, helpTopicsItem)

	aboutTopicsItem = wx.MenuItem(helpMenu, ID_AboutMenuItem, "About Tilem", "", wx.ITEM_NORMAL)
	helpMenu.AppendItem(aboutTopicsItem)
	self.Bind(wx.EVT_MENU, self.OnAbout, aboutTopicsItem)

	return helpMenu

#####
# Passthrough getters
#####

    def GetPalette(self):
	"""
	Passthrough getter to allow a canvas to get the current palette
	"""
	return self.paletteFrame.GetCurrentPalette()
	
    
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
	print "OnTileSize"
	
    def OnShowBlockGrid(self, evt):
	print "OnShowBlockGrid"

    def OnShowTileGrid(self, evt):
	print "OnShowTileGrid"

    def OnShowPixelGrid(self, evt):
	print "OnShowPixelGrid"

    def OnShowColorPalette(self, evt):
	print "OnShowColorPalette"

    def OnShowStatusbar(self, evt):
	print "OnShowStatusbar"

    def OnShowToolbar(self, evt):
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
	print "OnAbout"
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
