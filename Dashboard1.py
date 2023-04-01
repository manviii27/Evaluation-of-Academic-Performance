from tkinter import *
from PIL import Image,ImageTk
from course import Course
from result import Result
from student import Student
from tkinter import ttk,messagebox
import sqlite3
from subject import Subject
class EAP:
    def __init__(self,root): #Constructor
        self.root=root #initialise root
        self.root.title("Evaluation Of Academic Performance") #title of window
        self.root.geometry("1350x700+0+0") #resizing window (l,w+start point(top,left))
        self.root.config(bg="white")

        #bg
        lbl_img=Image.open("img/geu.jpg")
        lbl_img=ImageTk.PhotoImage(lbl_img)
        lbl_img.img=lbl_img
        lbl_bg=Label(self.root,image=lbl_img.img).place(x=0,y=50)

        #title
        title=Label(self.root,text="Dashboard",font=("Times New Roman",20,"bold"),bg="green",fg="white")
        title.place(x=0,y=0,relwidth=1,height=50) #label is a class, relwidth is 1 as the width is relative to parent window

        #menu
        Menu_F=LabelFrame(self.root,text=" Menu ",font=("Times New Roman",20),bg="white",fg="black")
        Menu_F.place(x=10,y=65,width=1340,height=80)

        #button
        btn1=Button(Menu_F,text="Course",font=("Times New Roman",15,"bold"),command=self.add_course,bg="green",fg="white",cursor='hand2').place(x=20,y=5,width=150,height=30)
        btn2=Button(Menu_F,text="Student",font=("Times New Roman",15,"bold"),command=self.add_student,bg="green",fg="white",cursor='hand2').place(x=200,y=5,width=150,height=30)
        btn3=Button(Menu_F,text="Subjects",font=("Times New Roman",15,"bold"),command=self.add_subject,bg="green",fg="white",cursor='hand2').place(x=380,y=5,width=150,height=30)
        btn4=Button(Menu_F,text="Results",font=("Times New Roman",15,"bold"),command=self.add_result,bg="green",fg="white",cursor='hand2').place(x=560,y=5,width=150,height=30)
        btn5=Button(Menu_F,text="LogOut",font=("Times New Roman",15,"bold"),command=self.back,bg="green",fg="white",cursor='hand2').place(x=1150,y=5,width=150,height=30)

        #update detail
        self.lbl_course=Label(self.root,text="Total Courses\n[ 0 ]",font=("Times New Roman",20),bd=10,bg="red",fg="white",relief=RIDGE)
        self.lbl_course.place(x=300,y=500,width=300,height=100)
        self.lbl_student=Label(self.root,text="Total Students\n[ 0 ]",font=("Times New Roman",20),bd=10,bg="#FF4500",fg="white",relief=RIDGE)
        self.lbl_student.place(x=800,y=500,width=300,height=100)
        
        self.updatedet()
        
        #footer
        foot=Label(self.root,text="EAP - Evaluation of Academic Performance\t\tBy - Manvi Haritwal",font=("Times New Roman",10),bg="black",fg="white").pack(side=BOTTOM,fill=X)
    
    #functions
    def add_course(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=Course(self.new_win)

    def add_student(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=Student(self.new_win)

    def add_result(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=Result(self.new_win)

    def add_subject(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=Subject(self.new_win)

    def updatedet(self):
        con=sqlite3.connect(database="rms.db")
        cur=con.cursor()
        try:
            cur.execute("Select * from course")
            row=cur.fetchall()
            self.lbl_course.config(text=f"Total Courses\n[{str(len(row))}]")
            
            cur.execute("Select * from student")
            row=cur.fetchall()
            self.lbl_student.config(text=f"Total Students\n[{str(len(row))}]")
            
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to {str(ex)}")

    def back(self):
        self.root.destroy()

#main
if __name__=="__main__":
    root=Tk()
    obj=EAP(root) #creating object of class
    root.mainloop() #Window stays for a long time and not disappear