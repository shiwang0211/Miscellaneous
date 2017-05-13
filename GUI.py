# -*- coding: utf-8 -*-
"""
Created on Wed May 10 13:59:12 2017

@author: swang
"""
import sys
try:
    import wx
except:
    sys.path.append(r'C:/Program Files/PTV Vision/PTV Visum 15/Exe/PythonModules/wxPython')
    import wx

def errormsg(msg):
    wx.MessageBox(msg, "There is something wrong.....", style=wx.ICON_INFORMATION|wx.OK)
    
class NodeError(wx.Dialog):
    
    def __init__(self, *args, **kwargs):
        super(NodeError, self).__init__(*args, **kwargs) 
        self.InitUI(args[1])
        
    def InitUI(self,Node):    

        panel = wx.Panel(self)

        hbox = wx.BoxSizer()
        sizer = wx.GridSizer(5, 1, 10, 10)

        btn1 = wx.Button(panel, label='Replace Timing for this Node')
        btn2 = wx.Button(panel, label='Replace Timing for all Nodes')
        btn3 = wx.Button(panel, label='Keep Existing Timing for this Node')
        btn4 = wx.Button(panel, label='Keep Existing Timing for all Nodes')
        btn5 = wx.Button(panel, label='End Importing')

        sizer.AddMany([btn1, btn2, btn3, btn4, btn5])

        hbox.Add(sizer, 0, wx.ALL, 50)
        panel.SetSizer(hbox)

        btn1.Bind(wx.EVT_BUTTON, self.ShowMessage1)
        btn2.Bind(wx.EVT_BUTTON, self.ShowMessage2)
        btn3.Bind(wx.EVT_BUTTON, self.ShowMessage3)
        btn4.Bind(wx.EVT_BUTTON, self.ShowMessage4)

        self.SetSize((400, 400))
        self.SetTitle('Select action to address error' + str(Node))
        self.Centre()
        self.choice = 0
        self.Show(True)

    def ShowMessage1(self, event):
        self.choice = 1
        self.EndModal(wx.ID_OK)
        
    def ShowMessage2(self, event):
        self.choice = 2
        self.EndModal(wx.ID_OK)

    def ShowMessage3(self, event):
        self.choice = 3
        self.EndModal(wx.ID_OK)
        
    def ShowMessage4(self, event):
        self.choice = 4
        self.EndModal(wx.ID_OK)
        
def ShowDiag(Node):
    ex = wx.App()
    Diag = NodeError(None,Node)
    result = Diag.ShowModal()
    if result == wx.ID_OK:
        return Diag.choice
    ex.MainLoop()


