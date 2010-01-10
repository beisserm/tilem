
import wx

ID_ABOUT = 1

class AboutDialog():
    '''
    Simple about Tilem dialog box.
    '''

    def __init__(self):
        description = """
Tilem is free software: you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

        info = wx.AboutDialogInfo()
        info.SetIcon(wx.Icon('icons/about.png', wx.BITMAP_TYPE_PNG))
        info.SetName('Tilem')
        info.SetVersion('.10a')
        info.SetDescription(description)
        info.SetCopyright('(C) 2010 Matt Beisser')
        info.SetWebSite('http://kenai.com/projects/tilem/')

        wx.AboutBox(info)
