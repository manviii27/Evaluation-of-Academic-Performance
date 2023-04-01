from tkinter import *
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import sqlite3
class Subject:
    def __init__(self,root): #Constructor
        self.root=root #initialise root
        self.root.title("Evaluation Of Academic Performance") #title of window
        self.root.geometry("1350x700+0+0") #resizing window (l,w+start point(top,left))
        self.root.config(bg="white")
        self.root.focus_force()

        #title
        title=Label(self.root,text="Subject Details",font=("Times New Roman",20,"bold"),bg="green",fg="white").place(x=0,y=0,relwidth=1,height=50) #label is a class, relwidth is 1 as the width is relative to parent window

        #vars
        self.sid=StringVar()
        self.course=StringVar()
        self.sem=StringVar()
        self.var_search=StringVar()
        self.clist=[]

        #labels
        lbl_sid=Label(self.root,text="Subject Code",font=("Times New Roman",15,"bold"),bg="white")
        lbl_sid.place(x=10,y=60)
        lbl_name=Label(self.root,text="Subject Name",font=("Times New Roman",15,"bold"),bg="white")
        lbl_name.place(x=10,y=100)
        lbl_course=Label(self.root,text="Course",font=("Times New Roman",15,"bold"),bg="white")
        lbl_course.place(x=10,y=170)
        lbl_sem=Label(self.root,text="Semester",font=("Times New Roman",15,"bold"),bg="white")
        lbl_sem.place(x=10,y=210)

        self.fetch_cname()

        self.txt_sid=Entry(self.root,textvariable=self.sid,font=("Times New Roman",15,"bold"),bg="light gray") #to access these in fn, we make it self
        self.txt_sid.place(x=150,y=60,width=200)
        self.txt_name=Text(self.root,font=("Times New Roman",15,"bold"),bg="light gray")
        self.txt_name.place(x=150,y=100,width=500,height=60)
        txt_course=ttk.Combobox(self.root,textvariable=self.course,values=self.clist,font=("Times New Roman",15,"bold"))
        txt_course.place(x=150,y=170,width=200)
        txt_sem=ttk.Combobox(self.root,textvariable=self.sem,values=("1","2","3","4","5","6","7","8","9","10"),font=("Times New Roman",15,"bold"))
        txt_sem.place(x=150,y=210,width=200)

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
        lbl_searchcoursenm=Label(self.root,text="Search By | Subject Code",font=("Times New Roman",15),bg="white")
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
    
        self.searchtable=ttk.Treeview(self.Frame,columns=("Sno","SCode","SName","Course","Sem"),xscrollcommand=scrollx.set,yscrollcommand=scrolly.set)
        
        scrollx.config(command=self.searchtable.xview)
        scrolly.config(command=self.searchtable.yview)

        #table
        self.searchtable.heading("Sno",text="Sno")
        self.searchtable.heading("SCode",text="Subject Code")
        self.searchtable.heading("SName",text="Subject Name")
        self.searchtable.heading("Course",text="Course")
        self.searchtable.heading("Sem",text="Sem")
        
        self.searchtable["show"]='headings'
        
        self.searchtable.column("Sno",width=50)
        self.searchtable.column("SCode",width=100)
        self.searchtable.column("SName",width=300)
        self.searchtable.column("Course",width=100)
        self.searchtable.column("Sem",width=50)
        self.searchtable.pack(fill=BOTH,expand=1)
        self.searchtable.bind("<ButtonRelease-1>",self.get_data)
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
        self.course.set(row[4])
        self.sem.set(row[3])
        self.txt_name.delete("1.0",END)
        self.txt_name.insert(END,row[2])
        

    def search(self):
        con=sqlite3.connect(database="rms.db")
        cur=con.cursor()
        try:
            cur.execute(f"Select * from subject where subid LIKE '%{self.var_search.get()}%'")
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
                messagebox.showerror("Error","Subject ID is required",parent=self.root)
            else:
                cur.execute("Select * from subject where subid=?",(self.sid.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Select Subject from list",parent=self.root)
                else:
                    op=messagebox.askyesno("Confirm","Do you really want to delete?",parent=self.root)
                    if op==True:
                        cur.execute("delete from subject where subid=?",(self.sid.get(),))
                        con.commit()
                        messagebox.showinfo("Deleted","Subject Deleted Successfully",parent=self.root)
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to {str(ex)}")

    def clear(self):
        self.show()
        self.sid.set("")
        self.sem.set("")
        self.course.set("")
        self.txt_name.delete("1.0",END)
        self.txt_sid.config(state=NORMAL)        

    def add(self):
        con=sqlite3.connect(database="rms.db")
        cur=con.cursor()
        try:
            if self.sid.get()=="":
                messagebox.showerror("Error","Subject ID is required",parent=self.root)
            else:
                cur.execute("Select * from subject where subid=?",(self.sid.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","Subject Code is already present",parent=self.root)
                else:
                    cur.execute("insert into subject (subid,name,sem,course) values(?,?,?,?)",(self.sid.get(), self.txt_name.get("1.0",END),self.sem.get(), self.course.get()))
                    con.commit()
                    messagebox.showinfo("Success","Subject Added Successfully",parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to {str(ex)}")

    def back(self):
        self.root.destroy()

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

    def update(self):
        con=sqlite3.connect(database="rms.db")
        cur=con.cursor()
        try:
            if self.sid.get()=="":
                messagebox.showerror("Error","Subject Code is required",parent=self.root)
            else:
                cur.execute("Select * from subject where subid=?",(self.sid.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Select Subject from list",parent=self.root)
                else:
                    cur.execute("update subject set name=?,sem=?,course=? where subid=?",(self.txt_name.get("1.0",END),self.sem.get(), self.course.get(),self.sid.get()))
                    con.commit()
                    messagebox.showinfo("Success","Subject Updated Successfully",parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to {str(ex)}")

    def show(self):
        con=sqlite3.connect(database="rms.db")
        cur=con.cursor()
        try:
            cur.execute("Select * from subject")
            row=cur.fetchall()
            self.searchtable.delete(*self.searchtable.get_children())
            for r in row:
                self.searchtable.insert("",END,values=r)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to {str(ex)}")
        

if __name__=="__main__":
    root=Tk()
    obj=Subject(root) #creating object of class
    root.mainloop() #Window stays for a long time and not disappear

    