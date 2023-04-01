from tkinter import *
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import sqlite3
class EAP2:
    def __init__(self,root): #Constructor
        self.root=root #initialise root
        self.root.title("Evaluation Of Academic Performance") #title of window
        self.root.geometry("1350x700+0+0") #resizing window (l,w+start point(top,left))
        self.root.config(bg="white")

        #title
        title=Label(self.root,text="View Results",font=("Times New Roman",20,"bold"),bg="#02a8b6",fg="white")
        title.place(x=0,y=0,relwidth=1,height=50) #label is a class, relwidth is 1 as the width is relative to parent window

        #button
        btn4=Button(self.root,text="LogOut",font=("Times New Roman",15,"bold"),bg="green",fg="white",cursor='hand2',command=self.back)
        btn4.place(x=1200,y=60,width=100,height=30)

        #vars
        self.var_search=StringVar()

        lbl_searchres=Label(self.root,text="Search By | Roll No",font=("Times New Roman",15),bg="white")
        lbl_searchres.place(x=380,y=60)
        txt_searchres=Entry(self.root,textvariable=self.var_search,font=("Times New Roman",15,"bold"),bg="light gray")
        txt_searchres.place(x=550,y=60,width=200,height=30) #to access these in fn, we make it self
        btn1=Button(self.root,text="Search",font=("Times New Roman",15,"bold"),bg="#73a5c6",fg="black",cursor="hand2",command=self.search)
        btn1.place(x=760,y=60,width=90,height=30)
        btn2=Button(self.root,text="Clear",font=("Times New Roman",15,"bold"),bg="light blue",fg="black",cursor="hand2",command=self.clear)
        btn2.place(x=860,y=60,width=90,height=30)

        lbl_rollno=Label(self.root,text="Roll No",font=("Times New Roman",15,"bold"),bg="white",bd=2,relief=GROOVE)
        lbl_rollno.place(x=180,y=140,width=100,height=50)
        lbl_name=Label(self.root,text="Name",font=("Times New Roman",15,"bold"),bg="white",bd=2,relief=GROOVE)
        lbl_name.place(x=280,y=140,width=200,height=50)
        lbl_course=Label(self.root,text="Course",font=("Times New Roman",15,"bold"),bg="white",bd=2,relief=GROOVE)
        lbl_course.place(x=480,y=140,width=100,height=50)
        lbl_sub=Label(self.root,text="Subject",font=("Times New Roman",15,"bold"),bg="white",bd=2,relief=GROOVE)
        lbl_sub.place(x=580,y=140,width=100,height=50)
        lbl_marks=Label(self.root,text="Marks Obtained",font=("Times New Roman",15,"bold"),bg="white",bd=2,relief=GROOVE)
        lbl_marks.place(x=680,y=140,width=200,height=50)
        lbl_tmarks=Label(self.root,text="Total Marks",font=("Times New Roman",15,"bold"),bg="white",bd=2,relief=GROOVE)
        lbl_tmarks.place(x=880,y=140,width=150,height=50)
        lbl_percent=Label(self.root,text="Percentage",font=("Times New Roman",15,"bold"),bg="white",bd=2,relief=GROOVE)
        lbl_percent.place(x=1030,y=140,width=150,height=50)

        #frame
        self.Frame=Frame(self.root,bd=2,relief=GROOVE)
        self.Frame.place(x=180,y=190,width=1000,height=460)
        
        scrolly=Scrollbar(self.Frame,orient=VERTICAL)
        scrolly.pack(side=RIGHT,fill=Y)
        self.searchtable=ttk.Treeview(self.Frame,columns=("RNo","Name","Sub","Course","Marks","TMarks","Percent"),yscrollcommand=scrolly.set)
        scrolly.config(command=self.searchtable.yview)

        #table
        self.searchtable.heading("RNo",text="")
        self.searchtable.heading("Name",text="")
        self.searchtable.heading("Sub",text="")
        self.searchtable.heading("Course",text="")
        self.searchtable.heading("Marks",text="")
        self.searchtable.heading("TMarks",text="")
        self.searchtable.heading("Percent",text="")
        
        self.searchtable["show"]='headings'

        self.searchtable.column("RNo",anchor=CENTER,width=100)
        self.searchtable.column("Name",anchor=CENTER,width=200)
        self.searchtable.column("Sub",anchor=CENTER,width=100)
        self.searchtable.column("Course",anchor=CENTER,width=100)
        self.searchtable.column("Marks",anchor=CENTER,width=200)
        self.searchtable.column("TMarks",anchor=CENTER,width=150)
        self.searchtable.column("Percent",anchor=CENTER,width=150)
        self.searchtable.pack(fill=BOTH,expand=1)

        self.foot=Label(self.root,text="EAP - Evaluation of Academic Performance\t\tBy - Manvi Haritwal",font=("Times New Roman",10),bg="black",fg="white").pack(side=BOTTOM,fill=X)

    #functions
    def back(self):
        self.root.destroy()

    def search(self):
        con=sqlite3.connect(database="rms.db")
        cur=con.cursor()
        try:
            if self.var_search.get()=="":
                messagebox.showerror("Error","Search a roll number")
            else:
                cur.execute("Select rollno,name,subid,cname,marks from result where rollno=?",(self.var_search.get(),))
                row=cur.fetchall()
                marks=StringVar()
                percent=StringVar()
                self.searchtable.delete(*self.searchtable.get_children())
                for r in row:
                    marks=100
                    percent=r[4]
                    self.searchtable.insert("",END,values=(r[0],r[1],r[2],r[3],r[4],marks,percent))
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to {str(ex)}")

    def clear(self):
        self.searchtable.delete(*self.searchtable.get_children())
        self.var_search.set("")

if __name__=="__main__":
    root=Tk()
    obj=EAP2(root) #creating object of class
    root.mainloop() #Window stays for a long time and not disappear