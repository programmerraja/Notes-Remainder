import tkinter as t
from tkinter import filedialog,messagebox
from datetime import date as td
import datetime as date
from tkinter import scrolledtext as scroll
import sqlite3
import os


class Notes_remainder:
    def __init__(self,window):
        #if dir not present create it
        if (not os.path.isdir("database")):
            os.mkdir("database")
        window.destroy()
        self.remainderwindow=t.Tk()
        self.dir=os.getcwd()
        self.remainderwindow.title("Space Repetition")
        self.remainderwindow.geometry("500x500+400+80")
        self.remainderwindow.configure(bg="#292929")
        self.remainderwindow.resizable(0,0)
        #image
        try:
          self.image=t.PhotoImage(file=os.path.join(self.dir,"image","bgimg.png"))      
          self.label=t.Label(self.remainderwindow,image=self.image,width=500,bg="#292929").place(x=0,y=0)
        except:
            messagebox.showinfo("ERROR","image is missing ! ")
            
        self.label=t.Label(self.remainderwindow,text="Enter Your Task Here:",bg="#292929",fg="yellow").place(x=50,y=190)
        self.rmv_button=t.Button(self.remainderwindow,text="Remove",fg="red",relief="groove",command=lambda :self.remove_task(self.notes_var.get()))
        self.rmv_button.place(x=435,y=188)
        #var to store a user enter notes
        self.notes_var=t.StringVar()
        self.notes_var.set("")
        self.notes=t.Entry(self.remainderwindow,width=40,textvariable=self.notes_var,relief="groove")
        self.notes.place(x=180,y=190)
        #binding function for entry 
        self.notes.bind("<Return>",lambda e :self.add_notes([self.notes_var.get(),self.dates_var.get(),0],date.timedelta(days=7)))
        self.temp_notes=[]
        #input for date in format m/d/y
        self.label2=t.Label(self.remainderwindow,text="Date Here(y/m/d):",bg="#292929",fg="yellow").place(x=50,y=240)
        #var to store a user enter date
        self.dates_var=t.StringVar()
        self.dates=t.Entry(self.remainderwindow,width=40,textvariable=self.dates_var,relief="groove")
        self.dates.place(x=180,y=240)
        self.dates.bind("<Return>",lambda e :self.add_notes([self.notes_var.get(),self.dates_var.get(),0],date.timedelta(days=7)))
        self.dates_var.set(td.today())
        #for shwing on going notes remainder
        self.label2=t.Label(self.remainderwindow,text="On Going Remainder",fg="red",bg="#292929").place(x=50,y=280)
        self.text_word=scroll.ScrolledText(self.remainderwindow,width=42,height=10,wrap="word",relief="groove")
        self.text_word.place(x=50,y=300)
        
        self.text_word["state"]="disabled"
        #update task to interface 
        self.open_file()

    #adding notes from user to dbms
    def add_notes(self,task_list,add_date,):
        
        if(task_list[0]):
          try:
               a=date.datetime.strptime(task_list[1],"%Y-%m-%d")
               with sqlite3.connect(os.path.join("database","notes.db")) as self.conn:
                    cur=self.conn.cursor()
                    par=(task_list[0],str(a+add_date)[:11],task_list[2])
                    cur.execute("insert into task(tasks,date,blackmark) values(?,?,?)",par)
                    self.notes_var.set("")
                    self.dates_var.set(td.today())
                    self.conn.commit()
                    #updating the notes imedaitely in front end 
                    self.open_file()
          except:
                 messagebox.showinfo("ERROR","Enter a vaild date  ! ")
        else:
            messagebox.showinfo("ERROR","Enter your task   ! ")
    def open_file(self):        
            self.conn=sqlite3.connect(os.path.join(self.dir,"database","notes.db"))
            c=self.conn.cursor()
            temp_list=[]
            try:
              c.execute(" create table task(tasks varchar(20),date varchar(20),blackmark integer);")
            except sqlite3.OperationalError as e:
                pass
            for i in c.execute("select * from task"):
                temp_list.append(i)
            self.update(temp_list)
            self.conn.close()
         
    #adding task to the scrolled text            
    def update(self,notes):
         if(len(notes)>=1):
             self.text_word["state"]="normal"
             self.text_word.delete("1.0","end")
             #adding text 
             self.text_word.insert("1.0" ,"task             Date        Blackmark\n")
             self.text_word.insert("2.0","_________________________________________\n")
             for text in notes:
                 self.text_word.insert("3.0",str(text[0])+"\t\t"+str(text[1])+"\t\t"+str(text[2])+"\n")
                 self.check(str(text[0]),str(text[1]),str(text[2]))
             self.text_word.insert("end","_________________________________________\n")
             self.text_word["state"]="disabled"
             #if any task date need to update 
             if(len(self.temp_notes)>0):
                self.re_add()
    #checking the notes date
    def check(self,task,task_date,blackmark):
                        #converting str to data object for adding
                    try:
                       task_date=date.datetime.strptime(task_date[2:].strip(" "),"%y-%m-%d")
                       today_date=date.datetime.strptime(str(td.today())[2:],"%y-%m-%d")
                       
                        #if today is task day it return  empty
                       if(str(today_date-task_date)[0:2]=="0:"):
                            messagebox.showinfo("TASk","Today You Need To Revice "+task)
                            ans=messagebox.askquestion("Question","Did you revising ? ")
                            if(ans=="no"):
                                blackmark=int(blackmark)
                                blackmark+=1
                                task_date+=date.timedelta(days=7)
                                #add to temp notes list 
                                self.temp_notes.append([task,str(task_date)[:10],str(blackmark)])
                            else:
                                task_date+=date.timedelta(days=7)
                                self.temp_notes.append([task,str(task_date)[:10],str(blackmark)])
                        
                       elif(int(str(today_date-task_date)[0:2])>0):
                            messagebox.showinfo("TASk","You missed to Revice The "+task)
                            ans=messagebox.askquestion("question","Did you revise that ? ")
                            if(ans=="no"):
                                blackmark=int(blackmark)
                                blackmark+=1
                                task_date+=date.timedelta(days=7)
                                self.temp_notes.append([task,str(task_date)[:10],str(blackmark)])
                            else:
                                task_date+=date.timedelta(days=7)
                                self.temp_notes.append([task,str(task_date)[:10],str(blackmark)])

                    except:
                        messagebox.showinfo("ERROR","Enter a vaild date  ! ")
    #to re add data to database 
                                        
    def re_add(self):
                  for task_list in self.temp_notes:
                    with sqlite3.connect(os.path.join("database","notes.db")) as self.conn:
                        cur=self.conn.cursor()
                        par=(task_list[0],task_list[1],task_list[2])
                        #removing the task 
                        cur.execute("delete from task where tasks like '%"+task_list[0]+"%'")
                        #ADD NEW TASK 
                        cur.execute("insert into task(tasks,date,blackmark) values(?,?,?)",par)
                    cur.close()
              
    def remove_task(self,task):
                    self.notes_var.set("")
                    with sqlite3.connect(os.path.join("database","notes.db")) as self.conn:
                        cur=self.conn.cursor()
                        #removing the task
                        cur.execute("delete from task where tasks ='"+task+"'")
                        self.conn.commit()
                        #updating the notes imedaitely in front end 
                    
                        values=cur.execute("select * from task")
                        #to clear front end for last one delete
                        if(len(list(values))==0):
                            self.text_word["state"]="normal"
                            self.text_word.delete("1.0","end")
                            self.text_word["state"]="disabled"
                        else:
                             self.open_file()
                    cur.close()
        
                    
app=Notes_remainder(t.Tk())
