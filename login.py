from tkinter import *
from math import *
import pymysql
from tkinter import messagebox
from PIL import Image,ImageTk
from Dashboard1 import EAP
from Dashboard2 import EAP2

class Login:
    def __init__(self,root):
        self.root=root
        self.root.title("Evaluation Of Academic Performance") #title of window
        self.root.geometry("1350x700+0+0") #resizing window (l,w+start point(top,left))
        self.root.config(bg="white")
        
        #bg
        bg_lbl=Label(self.root,bg="#1c4966",bd=0)
        bg_lbl.place(x=0,y=0,relheight=1,relwidth=1)

        #Frame
        lg_frame=Frame(self.root,bg="white").place(x=250,y=100,width=800,height=500)
        title=Label(lg_frame,text="LOGIN HERE",font=("Times New Roman",30,"bold"),bg="white",fg="black")
        title.place(x=525,y=150)
        
        user=Label(lg_frame,text="Username",font=("Times New Roman",20),bg="white",fg="black")
        user.place(x=325,y=250)
        self.user=Entry(lg_frame,font=("Times New Roman",15),bg="white",fg="black")
        self.user.place(x=330,y=290)
        psswd=Label(lg_frame,text="Password",font=("Times New Roman",20),bg="white",fg="black")
        psswd.place(x=325,y=340)
        self.psswd=Entry(lg_frame,font=("Times New Roman",15),bg="white",fg="black")
        self.psswd.place(x=330,y=380)

        btn_lg=Button(lg_frame,text="Login",command=self.login,font=("Times New Roman",20),bg="black",fg="white",cursor='hand2')
        btn_lg.place(x=325,y=430,width=100,height=40)
        
        #image
        lbl_img=Image.open("img/geu.png")
        lbl_img=lbl_img.resize((300,300),Image.ANTIALIAS) #resolution doesn't go bad
        lbl_img=ImageTk.PhotoImage(lbl_img) #display image
        lbl_img.img=lbl_img
        lbl_bg=Label(self.root,image=lbl_img.img)
        lbl_bg.place(x=650,y=250,width=300,height=300)
        
        #footer
        foot=Label(self.root,text="EAP - Evaluation of Academic Performance\t\tBy - Manvi Haritwal",font=("Times New Roman",10),fg="white")
        foot.pack(side=BOTTOM,fill=X)#sizes the frame
    
    #functions
    def login(self):
        nuser=self.user.get()
        type=StringVar()
        npsswd=self.psswd.get()
        if nuser=="" or npsswd=="":
            messagebox.showerror("Error","All fields are required",parent=self.root)
        else:
            try:
                con=pymysql.connect(host="localhost",user="root",password="",database="eap")
                cur=con.cursor()
                cur.execute("select type from login where user=%s and psswd=%s",(nuser,npsswd))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Username or password",parent=self.root)
                else:
                    messagebox.showinfo("Success","Your login was successful",parent=self.root)
                    for r in row:
                        type=r
                    if type=="A":
                        self.add_dashb1()
                    if type=="S":
                        self.add_dashb2()
                con.close()
            except Exception as es:
                messagebox.showerror("Error",f"Error due to {str(es)}",parent=self.root)

    def add_dashb1(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=EAP(self.new_win)

    def add_dashb2(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=EAP2(self.new_win)

#main
if __name__=="__main__":
    root=Tk() #display the root window
    obj=Login(root) #creating object of class
    root.mainloop() #Window stays for a long time and not disappear