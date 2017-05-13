import Tkinter
import tkFileDialog
from Tkinter import BOTH, END, BooleanVar, StringVar
import ttk
class simpleapp_tk(Tkinter.Tk):
    def __init__(self,parent):
        Tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()
        
    def initialize(self):
        self.grid()

        #ENTRY CELL
        self.entryVariable = StringVar()
        self.entry = Tkinter.Entry(self,textvariable=self.entryVariable)
        self.entry.grid(column=0,row=0,sticky='EW')
        self.entry.bind("<Return>", self.OnPressEnter)
        self.entryVariable.set(u"Enter text here.") 

        #CLICK BUTTON
        button = Tkinter.Button(self,text=u"Click me !",command=self.OnButtonClick) 
        button.grid(column=1,row=0)

        #CHECK BOX
        self.var = BooleanVar()
        cb = Tkinter.Checkbutton(self, text="Show title",variable=self.var, command=self.onClick)
        cb.select()
        cb.grid(column=0,row=5,sticky='W')

##        #COMBO BOX
##        self.combo = StringVar()
##        self.box = ttk.Combobox(self.parent, textvariable=self.box)
##        self.box['values'] = ('X', 'Y', 'Z')
##        self.box.current(0)
##        self.box.grid(column=0, row=4,sticky='W')

        #LABEL
        self.labelVariable = Tkinter.StringVar() 
        label = Tkinter.Label(self,textvariable=self.labelVariable,anchor="w",fg="white",bg="blue")
        label.grid(column=0,row=1,columnspan=2,sticky='EW')
        self.labelVariable.set(u"Hello !")

        # MENU
        menubar = Tkinter.Menu(self.parent) # level0: -- menubar--
        self.config(menu=menubar)
        
        fileMenu = Tkinter.Menu(menubar) #level1: filemenu 
        menubar.add_cascade(label="File", menu=fileMenu) # add to menubar

        submenu = Tkinter.Menu(menubar) #level2: submenu
        fileMenu.add_cascade(label='Import', menu=submenu) # add to filemenu
  
        submenu.add_command(label="test1",command=self.test1)# level3: add under submenu
        submenu.add_command(label="test2",command=self.test2)  
        fileMenu.add_separator()
        
        fileMenu.add_command(label="Exit", command=self.destroy)# level2: under filemenu


        self.grid_columnconfigure(0,weight=1) # just formatting
        self.resizable(True,False)
        self.update()
        self.geometry(self.geometry())       
        self.entry.focus_set()
        self.entry.selection_range(0, Tkinter.END)

        #QUIT
        quitButton = Tkinter.Button(self, text="Quit",command=self.destroy)
        quitButton.grid(column=1,row=5,sticky='E')

        
    def OnButtonClick(self):
        self.labelVariable.set(self.entryVariable.get()+" (TEST)" )
        self.entry.focus_set()
        self.entry.selection_range(0, Tkinter.END)

    def OnPressEnter(self,event):
        self.labelVariable.set(self.entryVariable.get()+" (TEST)")
        self.entry.focus_set()
        self.entry.selection_range(0, Tkinter.END)

    def onClick(self):
        if self.var.get() == True:
            a=1
        else:
            a=1

    def test1(self):
        ftypes = [('Python files', '*.py'), ('All files', '*')]
        dlg = tkFileDialog.Open(self, filetypes = ftypes)
        fl = dlg.show()
        if fl != '':
            text = self.readFile(fl) # get "text"
            self.labelVariable.set(text) # display in label
            
    def test2(self):
        a=1
        
    def readFile(self, filename):
        f = open(filename, "r")
        text = f.read()
        return text
    

if __name__ == "__main__":
    app = simpleapp_tk(None)
    app.title('my application')
    app.geometry("250x150+300+300")
    app.mainloop()
