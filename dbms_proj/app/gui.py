import matplotlib
matplotlib.use('TkAgg')
from tkinter import StringVar, IntVar, ttk, Tk, BOTH, RIGHT, RAISED, LEFT, X, Listbox, Message, messagebox,  END
from tkinter.ttk import Frame, Radiobutton, Button, Style, Label, Entry, Treeview
import tkinter as tk
import dbmanager
import configreader
import chartmaker

class ResearchFrame(Frame):
    def __init__(self):
        super().__init__()
        self._initdb_()
        self.initUI()

    def _initdb_(self):
        config = configreader.ConfigReader()
        config.readconfig()
        self._dbman = dbmanager.DbManager(config.username, config.pw
                ,config.host ,config.db)
        self._dbman.connect()
        self._dbman.populatedb()
        self.tables_col = {'author': 'name', 'title':'title', 'field':'name', 'tag':'name'}
        self.tables = {'author': 'author', 'title':'research', 'field':'field', 'tag':'tag'}
        self.tables_list = ('author', 'title', 'tag', 'field')
    def initUI(self):
        self.style = Style()
        self.style.theme_use("clam")

        self.searchframe = Frame(self, relief=RAISED, borderwidth=1)
        self.searchframe.pack(fill=BOTH, expand=True)

        self.tableframe = Frame(self, relief=RAISED, borderwidth=1)
        self.tableframe.pack(fill=BOTH, expand=True)

        self.master.title("Research")
        self.pack(fill=BOTH, expand=1)

        self.CreateTV()
        self.LoadTable()
        self.CreateSearchButton()
        self.CreateCombo()

        createButton = Button(self, text="Add Entry", command=self.CreateWindow)
        createButton.pack(side=LEFT, padx=5, pady=5)
        deleteButton = Button(self, text="Delete Entry", command=self.DestroyWindow)
        deleteButton.pack(side=LEFT, padx=5, pady=5)
        reportButton = Button(self, text="Generate Report", command=self.CreateReport)
        reportButton.pack(side=LEFT, padx=5, pady=5)
        quitButton = Button(self, text="Quit",
                command=self.quit)
        quitButton.pack(side=RIGHT, padx = 5, pady = 5)

    def CreateReport(self):
        self.reportframe = tk.Toplevel()
        self.reportframe.title("Generate Report")
        row = 0
        col = 0
        self.radiovalue = IntVar()
        self.radiovalue2 = IntVar()
        self.lblSelect = Label(self.reportframe, text="Select Relationship")
        self.lblSelect.grid(row=row,column=0, columnspan=2)
        self.lblCond = Label(self.reportframe, text="Condition")
        self.lblCond.grid(row=row,column=2)
        row=row+1

        self.radioauthor = Radiobutton(self.reportframe,
                variable=self.radiovalue, value=1, text="Author")
        self.radioauthor.grid(row=row, column=0)
        self.radioauthor2 = Radiobutton(self.reportframe,
                variable=self.radiovalue2, value=1, text="Author")
        self.radioauthor2.grid(row=row, column=1)
        self.rptentauthor = Entry(self.reportframe)
        self.rptentauthor.grid(row=row, column=2)
        row=row+1

        self.radiotitle = Radiobutton(self.reportframe,
                variable=self.radiovalue, value=2, text="Title")
        self.radiotitle2 = Radiobutton(self.reportframe,
                variable=self.radiovalue2, value=2, text="Title")
        self.radiotitle.grid(row=row, column=0)
        self.radiotitle2.grid(row=row, column=1)
        self.rptenttitle = Entry(self.reportframe)
        self.rptenttitle.grid(row=row, column=2)
        row=row+1

        self.radiotag = Radiobutton(self.reportframe,
                variable=self.radiovalue, value=3, text="Tag")
        self.radiotag.grid(row=row, column=0)
        self.radiotag2 = Radiobutton(self.reportframe,
                variable=self.radiovalue2, value=3, text="Tag")
        self.radiotag2.grid(row=row, column=1)
        self.rptenttag = Entry(self.reportframe)
        self.rptenttag.grid(row=row, column=2)
        row=row+1

        self.radiofield = Radiobutton(self.reportframe,
                variable=self.radiovalue, value=4, text="Field")
        self.radiofield.grid(row=row, column=0)
        self.radiofield2 = Radiobutton(self.reportframe,
                variable=self.radiovalue2, value=4, text="Field")
        self.radiofield2.grid(row=row, column=1)
        self.rptentfield = Entry(self.reportframe)
        self.rptentfield.grid(row=row, column=2)
        row=row+1

        self.generateButton = Button(self.reportframe, text="Generate", command=self.GenerateReport)
        self.generateButton.grid(row=row, column=1)

    def GenerateReport(self, event=None):
        leftchoice = self.radiovalue.get()
        rightchoice = self.radiovalue2.get()

        if (leftchoice == rightchoice):
            messagebox.showinfo("Error!","Cannot have same choice!")
            return

        '''
        1 - Author
        2 - Title
        3 - Tag
        4 - Field
        '''
        cond1 = ""
        cond2 = ""
        tofind = ""
        tofind2 = ""
        if(1 == leftchoice):
            tofind="a.name"
            cond1 = self.rptentauthor.get()
        elif (2 == leftchoice):
            tofind="r.title"
            cond1 = self.rptenttitle.get()
        elif (3 == leftchoice):
            tofind="t.name"
            cond1 = self.rptenttag.get()
        elif (4 == leftchoice):
            tofind="f.name"
            cond1 = self.rptentfield.get()

        if(1 == rightchoice):
            tofind2="a.name"
            cond2 = self.rptentauthor.get()
        elif (2 == rightchoice):
            tofind2="r.title"
            cond2 = self.rptenttitle.get()
        elif (3 == rightchoice):
            tofind2="t.name"
            cond2 = self.rptenttag.get()
        elif (4 == rightchoice):
            tofind2="f.name"
            cond2 = self.rptentfield.get()

        query ="select count({}) as count, {} from ".format(tofind, tofind);

        _tables = ("author a", "research r", "tag t", "field f")
        query+= _tables[leftchoice-1]

        _partial = ( " left join research r on a.researchid=r.title ",
                    " left join tag t on t.name=r.tagid ",
                    " left join field f on f.name=t.fieldid ")

        _reverse = (" left join author a on a.researchid=r.title ",
                    " left join research r on t.name=r.tagid ",
                    " left join tag t on f.name=t.fieldid ")

        if(leftchoice < rightchoice):
            while(leftchoice < rightchoice):
                query+= _partial[leftchoice-1]
                leftchoice = leftchoice + 1
        else:
            while(rightchoice < leftchoice):
                query+= _reverse[leftchoice-2]
                leftchoice = leftchoice - 1


        if cond1:
            if(2 != leftchoice):
                query += " where {}=\"{}\" ".format(tofind, cond1)
            else:
                query += " where {} like \"%{}%\" ".format(tofind, cond1)

        if cond1 and cond2:
            query += " and "

        if cond2 and cond1:
            if(2 != leftchoice):
                query += " {}=\"{}\"".format(tofind2, cond2)
            else:
                query += "{} like \"%{}%\" ".format(tofind2, cond2)

        if cond2 and not cond1:
            if(2 != rightchoice):
                query += " where {}=\"{}\" ".format(tofind2, cond2)
            else:
                query += " where {} like \"%{}%\" ".format(tofind2, cond2)

        query += " group by {} ".format(tofind)
        print(query)
        result = self._dbman.executeCustomQuery(query)
        if(0 == result[0]):
            messagebox.showinfo("Report", "Query returned no results.")
        elif(0 < result[0]):
            rightchoice = self.radiovalue2.get()
            leftchoice = self.radiovalue.get()

            message = "This chart shows the number of {} for each {}".format(self.tables_list[rightchoice-1], self.tables_list[leftchoice-1])
            tofind = self.tables_list[leftchoice-1]
            tofind2 = self.tables_list[rightchoice-1]

            if cond1:
                if(2 != leftchoice):
                    message += "\n where {} is \"{}\" ".format(tofind, cond1)
                else:
                    message += "\n where {} has key word \"{}\" ".format(tofind, cond1)

            if cond1 and cond2:
                message += " and "

            if cond2 and cond1:
                if(2 != leftchoice and 2 != rightchoice):
                    message += " {} is \"{}\"".format(tofind2, cond2)
                else:
                    message += "{} has key word \"{}\" ".format(tofind2, cond2)

            if cond2 and not cond1:
                if(2 != rightchoice):
                    message += "\n where {} is \"{}\" ".format(tofind2, cond2)
                else:
                    message += "\n where {} has key word  \"{}\" ".format(tofind2, cond2)

            maker = chartmaker.ChartMaker()
            maker.plotPie(result[1], message)

        else:
            messagebox.showinfo("Report", "Query error!")

        print(result[1])

    def CreateSearchButton(self):
        self.searchlbl = Label(self.searchframe, text="Search", width=6)
        self.searchlbl.pack(side=LEFT, padx=5, pady=5)
        self.searchtext = Entry(self.searchframe)
        self.searchtext.pack(side=LEFT, padx=5, expand=True)
        self.searchButton = Button(self.searchframe, text="Search", command=self.Search)
        self.searchButton.pack(side=RIGHT, padx=5)

    def CreateCombo(self):
        self.box_value = StringVar()
        self.box = ttk.Combobox(self.searchframe, textvariable=self.box_value, state='readonly')
        self.box.bind("<<ComboboxSelected>>", self.ArrangeByComboSelection)
        self.box['values'] = ('field', 'tag', 'title', 'author')
        self.box.current(0)
        self.box.pack(side=RIGHT, padx=5,expand=True)

    def Search(self,event=None):
        alllist = self._dbman.getAllWhere("{} like '%{}%'".format(self.box.get(), self.searchtext.get()))

        if(0 < alllist[0]):
            for i in self.tv.get_children():
                self.tv.delete(i)

            for item in alllist[1]:
                self.tv.insert('', 'end',  values=(item['Title'], item['Author'], item['Tag'], item['Field']))
        else:
            messagebox.showinfo('Search','{} not found in {}!'.format(self.searchtext.get(), self.box.get()))



    def ArrangeByComboSelection(self,event=None):
        alllist = self._dbman.getAll('order by {}'.format(self.box.get()))

        #put message here!
        if (0 < alllist[0]):
            for i in self.tv.get_children():
                self.tv.delete(i)

            for item in alllist[1]:
                self.tv.insert('', 'end',  values=(item['Title'], item['Author'], item['Tag'], item['Field']))

    def CreateWindow(self, event=None):
        self.newwin = tk.Toplevel()
        self.newwin.title("Add Entry")
        self.lbltitle = Label(self.newwin, text="Title", width=6)
        self.lbltitle.grid(row=0,column=0)
        self.enttitle = Entry(self.newwin)
        self.enttitle.grid(row=0, column=1)

        self.lblauthor = Label(self.newwin, text="Author", width=6)
        self.lblauthor.grid(row=1, column=0)
        self.authbox_value = StringVar()
        self.comboauthor= ttk.Combobox(self.newwin, textvariable=self.authbox_value)
        self.comboauthor.grid(row=1,column=1)
        self.comboauthor['values'] = self._createlist("select name from author group by name")

        self.lbltag = Label(self.newwin, text="Tag", width=6)
        self.lbltag.grid(row=2, column=0)
        self.tagbox_value = StringVar()
        self.combotag= ttk.Combobox(self.newwin, textvariable=self.tagbox_value)
        self.combotag.grid(row=2,column=1)
        self.combotag['values'] = self._createlist("select name from tag group by name")

        self.lblfield = Label(self.newwin, text="Field", width=6)
        self.lblfield.grid(row=3,column=0)
        self.fieldbox_value = StringVar()
        self.combofield= ttk.Combobox(self.newwin, textvariable=self.fieldbox_value)
        self.combofield.grid(row=3,column=1)
        self.combofield['values'] = self._createlist("select name from field group by name")

        self.addButton = Button(self.newwin, text="Add", command=self.Create)
        self.addButton.grid(row=4, column=1)

    def _createlist(self, srcquery):
        result = self._dbman.executeCustomQuery(srcquery)
        objlist = []
        if(0 < result[0]):
            for item in result[1]:
                for key in item.keys():
                    objlist.append(item[key])
        return objlist

    def PopulateComboBox(self, event=None):
        result = 0
        query = ""
        table = self.tablebox_value.get()
        query = "select {} from {} order by {} asc".format(self.tables_col[table], self.tables[table], self.tables_col[table])

        result = self._dbman.executeCustomQuery(query)

        if(0 < result[0]):
            self.lbltitle = Label(self.newwin, text=self.tablebox_value.get(), width=6)
            self.lbltitle.grid(row=1,column=0)
            self.titlebox_value = StringVar()
            self.combolist= ttk.Combobox(self.newwin, textvariable=self.titlebox_value, state='readonly')
            self.combolist.grid(row=1,column=1)
            self.combolist['values'] = self._createlist(query)

            self.destroyButton = Button(self.newwin, text="Delete", command=self.Destroy)
            self.destroyButton.grid(row=4, column=1)

    def DestroyWindow(self, event=None):
        self.newwin = tk.Toplevel()
        self.newwin.title("Delete Entry")
        self.lbldestroyfrom = Label(self.newwin, text='Entity:', width=6)
        self.lbldestroyfrom.grid(row=0,column=0)
        self.tablebox_value = StringVar()
        self.combotable= ttk.Combobox(self.newwin, textvariable=self.tablebox_value, state='readonly')
        self.combotable.grid(row=0,column=1)
        self.combotable.bind("<<ComboboxSelected>>", self.PopulateComboBox)
        self.combotable['values'] = ('field', 'tag', 'title')
        self.combotable.current(0)



    def Destroy(self, event=None):
        result = 0;

        if(-1 != self.combolist.current()):
            if('title' == self.combotable.get()):
                result = self._dbman.deleteFromTable('author','researchid', self.combolist.get())
            else:
                result = (1,())

            if(1 == result[0]):
                result = self._dbman.deleteFromTable(self.tables[self.combotable.get()],self.tables_col[self.combotable.get()], self.combolist.get())

            if(1 != result[0]):
                messagebox.showinfo('Destroy Notice', "Deleting {} failed!\r\n {}".format(self.combolist.get(), result[1]))
            else:
                messagebox.showinfo('Destroy Notice', "Delete success!")
                self.newwin.destroy()
                self.LoadTable()



    def Create(self, event=None):
        field = dbmanager.FieldDict();
        result = 0;
        if(-1 ==self.combofield.current()):
            field = dbmanager.FieldDict()
            field['name'] = self.combofield.get()
            field['description'] = 'a field on {}'.format(self.combofield.get())
            result = self._dbman.AddToTable('field',field)

        tag = dbmanager.TagDict()
        if(-1 ==self.combotag.current()):
            tag['name'] = self.combotag.get()
            tag['fieldid'] = self.combofield.get()
            tag['description'] = 'a tag on {}'.format(self.combotag.get())
            result = self._dbman.AddToTable('tag',tag)

        research = dbmanager.ResearchDict()
        research['title'] = self.enttitle.get()
        research['tagid'] = self.combotag.get()
        result = self._dbman.AddToTable('research', research)

        author = dbmanager.AuthorDict()
        author['name'] = self.comboauthor.get()
        author['researchid'] = self.enttitle.get()
        result = self._dbman.AddToTable('author',author)

        if(-1 == result):
            messagebox.showinfo('Create Notice', "Create one or more items failed!")
        else:
            messagebox.showinfo('Create Notice', "Create success!")
            self.newwin.destroy()
            self.LoadTable()





    def CreateTV(self):
        self.tv = Treeview(self.tableframe)
        self.tv['show'] = 'headings'
        self.tv['columns'] = ('Title', 'Author', 'Tag', 'Field')
        self.tv.heading("Title", text='Title', anchor='w')
        self.tv.column("Title", anchor="w")
        self.tv.heading('Author', text='Author')
        self.tv.column('Author', anchor='center', width=100)
        self.tv.heading('Tag', text='Tag')
        self.tv.column('Tag', anchor='center', width=100)
        self.tv.heading('Field', text='Field')
        self.tv.column('Field', anchor='center', width=100)
        self.tv.pack(fill=X, side='left', expand=True)
        vsb = ttk.Scrollbar(self.tableframe, orient="vertical", command=self.tv.yview)
        vsb.pack(side='right', fill='y')

    def LoadTable(self):
        alllist = self._dbman.getAll()[1]

        for i in self.tv.get_children():
            self.tv.delete(i)

        for item in alllist:
            self.tv.insert('', 'end',  values=(item['Title'], item['Author'], item['Tag'], item['Field']))

def main():
    root = Tk()
    root.geometry("750x300+300+300")
    app = ResearchFrame()
    root.mainloop()

if __name__ == '__main__':
    main()

