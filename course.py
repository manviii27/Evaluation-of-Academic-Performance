from tkinter import *
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import sqlite3
class Course:
    def __init__(self,root): #Constructor
        self.root=root #initialise root
        self.root.title("Evaluation Of Academic Performance") #title of window
        self.root.geometry("1350x700+0+0") #resizing window (l,w+start point(top,left))
        self.root.config(bg="white")
        self.root.focus_force()

        #title
        title=Label(self.root,text="Course Details",font=("Times New Roman",20,"bold"),bg="green",fg="white").place(x=0,y=0,relwidth=1,height=50) #label is a class, relwidth is 1 as the width is relative to parent window

        #vars
        self.course=StringVar()
        self.sem=StringVar()
        self.charges=StringVar()
        self.var_search=StringVar()

        #widgets
        lbl_coursenm=Label(self.root,text="Course Name",font=("Times New Roman",15,"bold"),bg="white")
        lbl_coursenm.place(x=10,y=60)
        lbl_sem=Label(self.root,text="Semesters",font=("Times New Roman",15,"bold"),bg="white")
        lbl_sem.place(x=10,y=100)
        lbl_charges=Label(self.root,text="Charges",font=("Times New Roman",15,"bold"),bg="white")
        lbl_charges.place(x=10,y=140)
        lbl_desc=Label(self.root,text="Description",font=("Times New Roman",15,"bold"),bg="white")
        lbl_desc.place(x=10,y=180)

        self.txt_coursenm=Entry(self.root,textvariable=self.course,font=("Times New Roman",15,"bold"),bg="light gray") #to access these in fn, we make it self
        self.txt_coursenm.place(x=150,y=60,width=200)
        txt_sem=Entry(self.root,textvariable=self.sem,font=("Times New Roman",15,"bold"),bg="light gray")
        txt_sem.place(x=150,y=100,width=200)
        txt_charges=Entry(self.root,textvariable=self.charges,font=("Times New Roman",15,"bold"),bg="light gray")
        txt_charges.place(x=150,y=140,width=200)
        self.txt_desc=Text(self.root,font=("Times New Roman",15,"bold"),bg="light gray")
        self.txt_desc.place(x=150,y=180,width=500,height=130)
        
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
        lbl_searchcoursenm=Label(self.root,text="Search By | Course Name",font=("Times New Roman",15),bg="white")
        lbl_searchcoursenm.place(x=720,y=60)
        txt_searchcoursenm=Entry(self.root,textvariable=self.var_search,font=("Times New Roman",15,"bold"),bg="light gray")
        txt_searchcoursenm.place(x=940,y=60,width=250) #to access these in fn, we make it self
        btn5=Button(self.root,text="Search",font=("Times New Roman",15,"bold"),bg="#73a5c6",fg="white",cursor="hand2",command=self.search)
        btn5.place(x=1200,y=60,width=110,height=28)

        self.Frame=Frame(self.root,bd=2,relief=RIDGE)
        self.Frame.place(x=720,y=100,width=600,height=540)
        
        scrollx=Scrollbar(self.Frame,orient=HORIZONTAL)
        scrolly=Scrollbar(self.Frame,orient=VERTICAL)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
    
        self.searchtable=ttk.Treeview(self.Frame,columns=("Sno","Name","Semesters","Charges","Desc"),xscrollcommand=scrollx.set,yscrollcommand=scrolly.set)
        
        scrollx.config(command=self.searchtable.xview)
        scrolly.config(command=self.searchtable.yview)

        #table
        self.searchtable.heading("Sno",text="Sno")
        self.searchtable.heading("Name",text="Course Name")
        self.searchtable.heading("Semesters",text="Semesters")
        self.searchtable.heading("Charges",text="Charges")
        self.searchtable.heading("Desc",text="Description")
        
        self.searchtable["show"]='headings'
        
        self.searchtable.column("Sno",width=50)
        self.searchtable.column("Name",width=100)
        self.searchtable.column("Semesters",width=70)
        self.searchtable.column("Charges",width=150)
        self.searchtable.column("Desc",width=300)
        self.searchtable.pack(fill=BOTH,expand=1)
        self.searchtable.bind("<ButtonRelease-1>",self.get_data)
        self.show()
        btn6=Button(self.root,text="Back",font=("Times New Roman",15,"bold"),bg="light blue",fg="black",cursor='hand2',command=self.back)
        btn6.place(x=150,y=630,width=110,height=40)

        foot=Label(self.root,text="EAP - Evaluation of Academic Performance\t\tBy - Manvi Haritwal",font=("Times New Roman",10),bg="black",fg="white")
        foot.pack(side=BOTTOM,fill=X)

    #functions
    def get_data(self,ev):
        self.txt_coursenm.config(state='readonly')
        r=self.searchtable.focus()
        cont=self.searchtable.item(r)
        row=cont["values"]
        self.course.set(row[1])
        self.sem.set(row[2])
        self.charges.set(row[3])
        self.txt_desc.delete("1.0",END)
        self.txt_desc.insert(END,row[4])
        
    def search(self):
        con=sqlite3.connect(database="rms.db")
        cur=con.cursor()
        try:
            cur.execute(f"Select * from course where name LIKE '%{self.var_search.get()}%'")
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
            if self.course.get()=="":
                messagebox.showerror("Error","Course Name is required",parent=self.root)
            else:
                cur.execute("Select * from course where name=?",(self.course.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Select Course from list",parent=self.root)
                else:
                    op=messagebox.askyesno("Confirm","Do you really want to delete?",parent=self.root)
                    if op==True:
                        cur.execute("delete from course where name=?",(self.course.get(),))
                        con.commit()
                        messagebox.showinfo("Deleted","Course Deleted Successfully",parent=self.root)
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to {str(ex)}")

    def clear(self):
        self.show()
        self.course.set("")
        self.sem.set("")
        self.charges.set("")
        self.txt_desc.delete("1.0",END)
        self.txt_coursenm.config(state=NORMAL)        

    def add(self):
        con=sqlite3.connect(database="rms.db")
        cur=con.cursor()
        try:
            if self.course.get()=="":
                messagebox.showerror("Error","Course Name is required",parent=self.root)
            else:
                cur.execute("Select * from course where name=?",(self.course.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","Course Name is already present",parent=self.root)
                else:
                    cur.execute("insert into course (name,sem,charges,desc) values(?,?,?,?)",(self.course.get(), self.sem.get(), self.charges.get(),self.txt_desc.get("1.0",END)))
                    con.commit()
                    messagebox.showinfo("Success","Course Added Successfully",parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to {str(ex)}")

    def back(self):
        self.root.destroy()

    def update(self):
        con=sqlite3.connect(database="rms.db")
        cur=con.cursor()
        try:
            if self.course.get()=="":
                messagebox.showerror("Error","Course Name is required",parent=self.root)
            else:
                cur.execute("Select * from course where name=?",(self.course.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Select Course from list",parent=self.root)
                else:
                    cur.execute("update course set sem=?,charges=?,desc=? where name=?",(self.sem.get(), self.charges.get(),self.txt_desc.get("1.0",END),self.course.get()))
                    con.commit()
                    messagebox.showinfo("Success","Course Updated Successfully",parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to {str(ex)}")

    def show(self):
        con=sqlite3.connect(database="rms.db")
        cur=con.cursor()
        try:
            cur.execute("Select * from course")
            row=cur.fetchall()
            self.searchtable.delete(*self.searchtable.get_children())
            for r in row:
                self.searchtable.insert("",END,values=r)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to {str(ex)}")
        
#main
if __name__=="__main__":
    root=Tk()
    obj=Course(root) #creating object of class
    root.mainloop() #Window stays for a long time and not disappear

