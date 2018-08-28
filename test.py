import sys

import wx
import wx.lib.agw.ultimatelistctrl as ULC

class MyFrame(wx.Frame):

    def __init__(self, parent, ID, title):

        wx.Frame.__init__(self, parent, ID, title)

        list = ULC.UltimateListCtrl(self, wx.ID_ANY, agwStyle=wx.LC_REPORT|wx.LC_VRULES|wx.LC_HRULES|wx.LC_SINGLE_SEL | ULC.ULC_HAS_VARIABLE_ROW_HEIGHT)

        list.InsertColumn(0, "Column 1")
        list.InsertColumn(1, "Column 2")

        index = list.InsertStringItem(0, "Item 1")
        list.SetStringItem(index, 1, "Sub-item 1")


        index = list.InsertStringItem(0, "Item 2")
        list.SetStringItem(index, 1, "Sub-item 2")

        choice = wx.Choice(list, -1, choices=["one", "two"])
        index = list.InsertStringItem(0, "A widget")

        list.SetItemWindow(index, 1, choice, expand=True)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(list, 1, wx.EXPAND)
        self.SetSizer(sizer)



app = wx.App(None)

frame = MyFrame(None, -1, "Loading")
app.SetTopWindow(frame)
frame.Show()

app.MainLoop()