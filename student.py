from tkinter import *
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import sqlite3

class Student:
    def __init__(self,root): #Constructor
        self.root=root #initialise root
        self.root.title("Evaluation Of Academic Performance") #title of window
        self.root.geometry("1350x700+0+0") #resizing window (l,w+start point(top,left))
        self.root.config(bg="white")
        self.root.focus_force()

        #title
        title=Label(self.root,text="Student Details",font=("Times New Roman",20,"bold"),bg="green",fg="white").place(x=0,y=0,relwidth=1,height=50) #label is a class, relwidth is 1 as the width is relative to parent window

        #vars
        self.sid=StringVar()
        self.name=StringVar()
        self.rollno=StringVar()
        self.gender=StringVar()
        self.email=StringVar()
        self.cname=StringVar()
        self.sem=StringVar()
        self.dob=StringVar()
        self.var_search=StringVar()

        #widgets
        lbl_sid=Label(self.root,text="Student ID",font=("Times New Roman",15,"bold"),bg="white")
        lbl_sid.place(x=10,y=60)
        lbl_name=Label(self.root,text="Name",font=("Times New Roman",15,"bold"),bg="white")
        lbl_name.place(x=10,y=100)
        lbl_rollno=Label(self.root,text="Roll No",font=("Times New Roman",15,"bold"),bg="white")
        lbl_rollno.place(x=10,y=140)
        lbl_email=Label(self.root,text="Email",font=("Times New Roman",15,"bold"),bg="white")
        lbl_email.place(x=10,y=180)
        lbl_gender=Label(self.root,text="Gender",font=("Times New Roman",15,"bold"),bg="white")
        lbl_gender.place(x=10,y=220)
        lbl_dob=Label(self.root,text="DOB",font=("Times New Roman",15,"bold"),bg="white")
        lbl_dob.place(x=10,y=260)
        lbl_cname=Label(self.root,text="Course",font=("Times New Roman",15,"bold"),bg="white")
        lbl_cname.place(x=10,y=300)
        lbl_sem=Label(self.root,text="Semester",font=("Times New Roman",15,"bold"),bg="white")
        lbl_sem.place(x=10,y=340)

        self.clist=[]
        self.fetch_cname()

        self.txt_sid=Entry(self.root,textvariable=self.sid,font=("Times New Roman",15,"bold"),bg="light gray") #to access these in fn, we make it self
        self.txt_sid.place(x=150,y=60,width=200)
        self.txt_name=Entry(self.root,textvariable=self.name,font=("Times New Roman",15,"bold"),bg="light gray")
        self.txt_name.place(x=150,y=100,width=200)
        txt_rollno=Entry(self.root,textvariable=self.rollno,font=("Times New Roman",15,"bold"),bg="light gray")
        txt_rollno.place(x=150,y=140,width=200)
        txt_email=Entry(self.root,textvariable=self.email,font=("Times New Roman",15,"bold"),bg="light gray")
        txt_email.place(x=150,y=180,width=300)
        txt_gender=ttk.Combobox(self.root,textvariable=self.gender,values=("Male","Female","Other"),font=("Times New Roman",15,"bold"))
        txt_gender.place(x=150,y=220,width=200)
        txt_gender.set("Select")
        txt_dob=Entry(self.root,textvariable=self.dob,font=("Times New Roman",15,"bold"),bg="light gray")
        txt_dob.place(x=150,y=260,width=200)
        self.txt_cname=ttk.Combobox(self.root,textvariable=self.cname,values=self.clist,font=("Times New Roman",15,"bold"))
        self.txt_cname.place(x=150,y=300,width=200)
        self.txt_cname.set("Select")
        txt_sem=ttk.Combobox(self.root,textvariable=self.sem,values=("1","2","3","4","5","6","7","8","9","10"),font=("Times New Roman",15,"bold"))
        txt_sem.place(x=150,y=340,width=200)
        txt_sem.set("Select")

        #buttons
        btn1=Button(self.root,text="Save",font=("Times New Roman",15,"bold"),bg="#68bb59",fg="white",cursor="hand2",command=self.add)
        btn1.place(x=150,y=400,width=110,height=40)
        btn2=Button(self.root,text="Update",font=("Times New Roman",15,"bold"),bg="#ffdd3c",fg="white",cursor="hand2",command=self.update)
        btn2.place(x=270,y=400,width=110,height=40)
        btn3=Button(self.root,text="Delete",font=("Times New Roman",15,"bold"),bg="#ed2939",fg="white",cursor="hand2",command=self.delete)
        btn3.place(x=390,y=400,width=110,height=40)
        btn4=Button(self.root,text="Clear",font=("Times New Roman",15,"bold"),bg="#73a5c6",fg="white",cursor="hand2",command=self.clear)
        btn4.place(x=510,y=400,width=110,height=40)
        
        #search records
        lbl_searchsid=Label(self.root,text="Search By | Student ID",font=("Times New Roman",15),bg="white")
        lbl_searchsid.place(x=720,y=60)
        txt_searchsid=Entry(self.root,textvariable=self.var_search,font=("Times New Roman",15,"bold"),bg="light gray")
        txt_searchsid.place(x=940,y=60,width=250) #to access these in fn, we make it self
        btn5=Button(self.root,text="Search",font=("Times New Roman",15,"bold"),bg="#73a5c6",fg="white",cursor="hand2",command=self.search)
        btn5.place(x=1200,y=60,width=110,height=28)

        self.Frame=Frame(self.root,bd=2,relief=RIDGE)
        self.Frame.place(x=720,y=100,width=600,height=540)
        
        scrollx=Scrollbar(self.Frame,orient=HORIZONTAL)
        scrolly=Scrollbar(self.Frame,orient=VERTICAL)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
    
        self.searchtable=ttk.Treeview(self.Frame,columns=("Sno","Sid","Name","RollNo","Email","G","DOB","CName","Sem"),xscrollcommand=scrollx.set,yscrollcommand=scrolly.set)
        
        scrollx.config(command=self.searchtable.xview)
        scrolly.config(command=self.searchtable.yview)

        #table
        self.searchtable.heading("Sno",text="SNo")
        self.searchtable.heading("Sid",text="Student ID")
        self.searchtable.heading("Name",text="Student Name")
        self.searchtable.heading("RollNo",text="Roll No")
        self.searchtable.heading("Email",text="Email ID")
        self.searchtable.heading("G",text="Sex")
        self.searchtable.heading("DOB",text="DOB")
        self.searchtable.heading("CName",text="Course")
        self.searchtable.heading("Sem",text="Sem")

        
        self.searchtable["show"]='headings'
        
        self.searchtable.column("Sno",width=50)
        self.searchtable.column("Sid",width=100)
        self.searchtable.column("Name",width=200)
        self.searchtable.column("RollNo",width=100)
        self.searchtable.column("Email",width=300)
        self.searchtable.column("G",width=100)
        self.searchtable.column("DOB",width=100)
        self.searchtable.column("CName",width=100)
        self.searchtable.column("Sem",width=50)
        self.searchtable.pack(fill=BOTH,expand=1)
        self.searchtable.bind("<ButtonRelease-1>",self.get_data)
        self.txt_sid.config(state='normal')
        self.show()

        btn6=Button(self.root,text="Back",font=("Times New Roman",15,"bold"),bg="light blue",fg="black",cursor='hand2',command=self.back)
        btn6.place(x=150,y=630,width=110,height=40)

        foot=Label(self.root,text="EAP - Evaluation of Academic Performance\t\tBy - Manvi Haritwal",font=("Times New Roman",10),bg="black",fg="white").pack(side=BOTTOM,fill=X)


    def get_data(self,ev):
        self.txt_sid.config(state='readonly')
        r=self.searchtable.focus()
        cont=self.searchtable.item(r)
        row=cont["values"]
        self.sid.set(row[1])
        self.name.set(row[2])
        self.rollno.set(row[3])
        self.email.set(row[4])
        self.gender.set(row[5])
        self.dob.set(row[6])
        self.cname.set(row[7])
        self.sem.set(row[8])
        

    def search(self):
        con=sqlite3.connect(database="rms.db")
        cur=con.cursor()
        try:
            cur.execute(f"Select * from student where sid LIKE '%{self.var_search.get()}%'")
            row=cur.fetchall()
            self.searchtable.delete(*self.searchtable.get_children())
            for r in row:
                self.searchtable.insert("",END,values=r)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to {str(ex)}")
        
    def delete(self):
        con=sqlite3.connect(database="rms.db")
        cur=con.cursor()
        try:
            if self.sid.get()=="":
                messagebox.showerror("Error","Student ID is required",parent=self.root)
            else:
                cur.execute("Select * from student where sid=?",(self.sid.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Select Student from list",parent=self.root)
                else:
                    op=messagebox.askyesno("Confirm","Do you really want to delete?",parent=self.root)
                    if op==True:
                        cur.execute("delete from student where sid=?",(self.sid.get(),))
                        con.commit()
                        messagebox.showinfo("Deleted","Student Deleted Successfully",parent=self.root)
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to {str(ex)}")


    def clear(self):
        self.show()
        self.sid.set("")
        self.name.set("")
        self.rollno.set("")
        self.email.set("")
        self.gender.set("")
        self.dob.set("")
        self.cname.set("")
        self.sem.set("")       
        self.txt_sid.config(state='normal')

    def add(self):
        con=sqlite3.connect(database="rms.db")
        cur=con.cursor()
        try:
            if self.sid.get()=="":
                messagebox.showerror("Error","Student ID is required",parent=self.root)
            else:
                cur.execute("Select * from student where sid=?",(self.sid.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","Student ID is already present",parent=self.root)
                else:
                    cur.execute("insert into student (sid,name,rollno,email,gender,dob,course,sem) values(?,?,?,?,?,?,?,?)",(self.sid.get(), self.name.get(), self.rollno.get(),self.email.get(),self.gender.get(),self.dob.get(),self.cname.get(),self.sem.get()))
                    con.commit()
                    messagebox.showinfo("Success","Student Added Successfully",parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to {str(ex)}")

    def back(self):
        self.root.destroy()

    def update(self):
        con=sqlite3.connect(database="rms.db")
        cur=con.cursor()
        try:
            if self.sid.get()=="":
                messagebox.showerror("Error","Student ID is required",parent=self.root)
            else:
                cur.execute("Select * from student where sid=?",(self.sid.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Select Student from list",parent=self.root)
                else:
                    cur.execute("update student set name=?, rollno=?, email=?,gender=?, dob=?, course=?, sem=? where sid=?",(self.name.get(), self.rollno.get(),self.email.get(),self.gender.get(),self.dob.get(),self.cname.get(),self.sem.get(),self.sid.get()))
                    con.commit()
                    messagebox.showinfo("Success","Student Updated Successfully",parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to {str(ex)}")

    def show(self):
        con=sqlite3.connect(database="rms.db")
        cur=con.cursor()
        try:
            cur.execute("Select * from student")
            row=cur.fetchall()
            self.searchtable.delete(*self.searchtable.get_children())
            for r in row:
                self.searchtable.insert("",END,values=r)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to {str(ex)}")
        
    def fetch_cname(self):
        con=sqlite3.connect(database="rms.db")
        cur=con.cursor()
        try:
            cur.execute("Select name from course")
            row=cur.fetchall()
            if len(row)>0:
                for r in row:
                    self.clist.append(r[0])
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to {str(ex)}")
        

if __name__=="__main__":
    root=Tk()
    obj=Student(root) #creating object of class
    root.mainloop() #Window stays for a long time and not disappear