from tkinter import *
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import sqlite3
class Result:
    def __init__(self,root): #Constructor
        self.root=root #initialise root
        self.root.title("Evaluation Of Academic Performance") #title of window
        self.root.geometry("1350x700+0+0") #resizing window (l,w+start point(top,left))
        self.root.config(bg="white")
        self.root.focus_force()

        #title
        title=Label(self.root,text="Add Results",font=("Times New Roman",20,"bold"),bg="#02a8b6",fg="white").place(x=0,y=0,relwidth=1,height=50) #label is a class, relwidth is 1 as the width is relative to parent window

        #vars
        self.name=StringVar()
        self.course=StringVar()
        self.select=StringVar()
        self.sub=StringVar()
        self.marks=StringVar()
        self.rlist=[]
        self.fetch_rollno()
        self.slist=[]
        self.fetch_sname()
        self.var_search=StringVar()

        #label
        lbl_select=Label(self.root,text="Select Student",font=("Times New Roman",15,"bold"),bg="white")
        lbl_select.place(x=10,y=60)
        lbl_name=Label(self.root,text="Name",font=("Times New Roman",15,"bold"),bg="white")
        lbl_name.place(x=10,y=100)
        lbl_course=Label(self.root,text="Course",font=("Times New Roman",15,"bold"),bg="white")
        lbl_course.place(x=10,y=140)
        lbl_sub=Label(self.root,text="Subject",font=("Times New Roman",15,"bold"),bg="white")
        lbl_sub.place(x=10,y=180)
        lbl_marks=Label(self.root,text="Marks Obtained",font=("Times New Roman",15,"bold"),bg="white")
        lbl_marks.place(x=10,y=220)

        #buttons
        btn1=Button(self.root,text="Search",font=("Times New Roman",15,"bold"),bg="#73a5c6",fg="black",cursor="hand2",command=self.search)
        btn1.place(x=400,y=60,width=90,height=30)
        btn2=Button(self.root,text="Submit",font=("Times New Roman",15,"bold"),bg="#68bb59",fg="black",cursor="hand2",command=self.add)
        btn2.place(x=180,y=300,width=80,height=40)
        btn3=Button(self.root,text="Update",font=("Times New Roman",15,"bold"),bg="#ffdd3c",fg="black",cursor="hand2",command=self.update)
        btn3.place(x=270,y=300,width=80,height=40)
        btn4=Button(self.root,text="Delete",font=("Times New Roman",15,"bold"),bg="#ed2939",fg="black",cursor="hand2",command=self.delete)
        btn4.place(x=360,y=300,width=80,height=40)
        btn5=Button(self.root,text="Clear",font=("Times New Roman",15,"bold"),bg="light blue",fg="black",cursor="hand2",command=self.clear)
        btn5.place(x=450,y=300,width=80,height=40)

        self.txt_select=ttk.Combobox(self.root,textvariable=self.select,values=self.rlist,font=("Times New Roman",15,"bold"))
        self.txt_select.place(x=180,y=60,width=200)
        self.txt_name=Entry(self.root,textvariable=self.name,font=("Times New Roman",15,"bold"),state='readonly',bg="light gray") #to access these in fn, we make it self
        self.txt_name.place(x=180,y=100,width=200)
        self.txt_course=Entry(self.root,textvariable=self.course,font=("Times New Roman",15,"bold"),state='readonly',bg="light gray")
        self.txt_course.place(x=180,y=140,width=200)
        txt_sub=ttk.Combobox(self.root,textvariable=self.sub,values=self.slist,font=("Times New Roman",15,"bold"))
        txt_sub.place(x=180,y=180,width=200)
        txt_marks=Entry(self.root,textvariable=self.marks,font=("Times New Roman",15,"bold"),bg="light gray")
        txt_marks.place(x=180,y=220,width=200)

        lbl_searchcoursenm=Label(self.root,text="Search By | Roll No",font=("Times New Roman",15),bg="white")
        lbl_searchcoursenm.place(x=720,y=60)
        txt_searchcoursenm=Entry(self.root,textvariable=self.var_search,font=("Times New Roman",15,"bold"),bg="light gray")
        txt_searchcoursenm.place(x=900,y=60,width=200) #to access these in fn, we make it self
        btn6=Button(self.root,text="Search",font=("Times New Roman",15,"bold"),bg="#73a5c6",fg="black",cursor="hand2",command=self.search1)
        btn6.place(x=1150,y=60,width=90,height=30)

        self.Frame=Frame(self.root,bd=2,relief=RIDGE)
        self.Frame.place(x=720,y=100,width=600,height=540)
        
        scrollx=Scrollbar(self.Frame,orient=HORIZONTAL)
        scrolly=Scrollbar(self.Frame,orient=VERTICAL)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
    
        self.searchtable=ttk.Treeview(self.Frame,columns=("Sno","RNo","Name","Sub","Course","Marks"),xscrollcommand=scrollx.set,yscrollcommand=scrolly.set)
        
        scrollx.config(command=self.searchtable.xview)
        scrolly.config(command=self.searchtable.yview)

        #table
        self.searchtable.heading("Sno",text="Sno")
        self.searchtable.heading("RNo",text="Roll No")
        self.searchtable.heading("Name",text="Student Name")
        self.searchtable.heading("Sub",text="Subject Code")
        self.searchtable.heading("Course",text="Course")
        self.searchtable.heading("Marks",text="Marks")
        
        self.searchtable["show"]='headings'
        
        self.searchtable.column("Sno",width=50)
        self.searchtable.column("RNo",width=100)
        self.searchtable.column("Name",width=200)
        self.searchtable.column("Sub",width=100)
        self.searchtable.column("Course",width=100)
        self.searchtable.column("Marks",width=50)
        self.searchtable.pack(fill=BOTH,expand=1)
        self.searchtable.bind("<ButtonRelease-1>",self.get_data)
        self.show()
        btn7=Button(self.root,text="Back",font=("Times New Roman",15,"bold"),bg="light blue",fg="black",cursor='hand2',command=self.back)
        btn7.place(x=180,y=480,width=110)

        self.foot=Label(self.root,text="EAP - Evaluation of Academic Performance\t\tBy - Manvi Haritwal",font=("Times New Roman",10),bg="black",fg="white").pack(side=BOTTOM,fill=X)
        
    #functions
    def search1(self):
        con=sqlite3.connect(database="rms.db")
        cur=con.cursor()
        try:
            cur.execute(f"Select * from result where rollno LIKE '%{self.var_search.get()}%'")
            row=cur.fetchall()
            self.searchtable.delete(*self.searchtable.get_children())
            for r in row:
                self.searchtable.insert("",END,values=r)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to {str(ex)}")

    def back(self):
        self.root.destroy()

    def get_data(self,ev):
        self.txt_select.config(state='readonly')
        r=self.searchtable.focus()
        cont=self.searchtable.item(r)
        row=cont["values"]
        self.select.set(row[1])
        self.name.set(row[2])
        self.sub.set(row[3])
        self.course.set(row[4])
        self.marks.set(row[5])

    def update(self):
        con=sqlite3.connect(database="rms.db")
        cur=con.cursor()
        try:
            if self.select.get()=="":
                messagebox.showerror("Error","Select Result from list",parent=self.root)
            else:
                cur.execute("Select * from result where rollno=? and subid=?",(self.select.get(),self.sub.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Select Result from list",parent=self.root)
                else:
                    cur.execute("update result set name=?,cname=?,marks=? where rollno=? and subid=?",(self.name.get(),self.course.get(),self.marks.get(),self.select.get(),self.sub.get()))
                    con.commit()
                    messagebox.showinfo("Success","Result Updated Successfully",parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to {str(ex)}")

    def delete(self):
        con=sqlite3.connect(database="rms.db")
        cur=con.cursor()
        try:
            if self.sub.get()=="":
                messagebox.showerror("Error","Select Result from list",parent=self.root)
            else:
                cur.execute("Select * from result where rollno=? and subid=?",(self.select.get(),self.sub.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Select Result from list",parent=self.root)
                else:
                    op=messagebox.askyesno("Confirm","Do you really want to delete?",parent=self.root)
                    if op==True:
                        cur.execute("delete from result where rollno=? and subid=?",(self.select.get(),self.sub.get(),))
                        con.commit()
                        messagebox.showinfo("Deleted","Result Deleted Successfully",parent=self.root)
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to {str(ex)}")

    def show(self):
        con=sqlite3.connect(database="rms.db")
        cur=con.cursor()
        try:
            cur.execute("Select * from result")
            row=cur.fetchall()
            self.searchtable.delete(*self.searchtable.get_children())
            for r in row:
                self.searchtable.insert("",END,values=r)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to {str(ex)}")

    def fetch_rollno(self):
        con=sqlite3.connect(database="rms.db")
        cur=con.cursor()
        try:
            cur.execute("Select rollno from student")
            row=cur.fetchall()
            if len(row)>0:
                for r in row:
                    self.rlist.append(r[0])
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to {str(ex)}")
     
    def fetch_sname(self):
        con=sqlite3.connect(database="rms.db")
        cur=con.cursor()
        try:
            cur.execute("Select subid from subject")
            row=cur.fetchall()
            if len(row)>0:
                for r in row:
                    self.slist.append(r[0])
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to {str(ex)}")
     
    def search(self):
        con=sqlite3.connect(database="rms.db")
        cur=con.cursor()
        try:
            cur.execute("Select name,course from student where rollno=?",(self.select.get(),))
            row=cur.fetchone()
            if row!=None:
                self.name.set(row[0])
                self.course.set(row[1])
            else:
                messagebox.showerror("Error","No record found",parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to {str(ex)}")
    
    def add(self):
        con=sqlite3.connect(database="rms.db")
        cur=con.cursor()
        try:
            if self.name.get()=="":
                messagebox.showerror("Error","Search Student from list",parent=self.root)
            else:
                cur.execute("Select * from result where subid=? and rollno=?",(self.sub.get(),self.select.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","Result is already present",parent=self.root)
                else:
                    cur.execute("insert into result (rollno,name,subid,cname,marks) values(?,?,?,?,?)",(self.select.get(), self.name.get(), self.sub.get(), self.course.get(),self.marks.get(),))
                    con.commit()
                    messagebox.showinfo("Success","Result Added Successfully",parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to {str(ex)}")

    def clear(self):
        self.show()
        self.select.set("")
        self.name.set("")
        self.course.set("")
        self.sub.set("")
        self.marks.set("") 

if __name__=="__main__":
    root=Tk()
    obj=Result(root) #creating object of class
    root.mainloop() #Window stays for a long time and not disappear
