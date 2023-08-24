import tkinter
from tkinter import *
from tkinter import ttk,messagebox
import mysql.connector as mysql

mydb = mysql.connect(host="localhost",user="root",password="Kishore@95",database="db1")
cursor = mydb.cursor()

query = 'show columns from p18_project;'
cursor.execute(query)
cols = []
for i in cursor:
    cols.append(i[0])

window = Tk()
window.title('get_details')
window.geometry('480x360')
font = ('arial', 14)


label = Label(window,text = 'Select the column name and give a value to query',fg='green',pady=10,font = ('arial',16))
label.grid(row=0,column=1,columnspan=6)

option = ttk.Combobox(window,values=cols,state='r')
option.grid(row=1,column=2)

name_entry = Entry(window, width=20, font=font)
name_entry.grid(row=1,column=3)

get_button = Button(window,text='get',bg='teal',fg='white',font=font,command=lambda : get_details())
get_button.grid(row=1,column=4)

details = Text(window,height=10,width=40,font=font)
details.grid(row=3,column=2,columnspan=5)

def get_details():
    details.delete(1.0,END)
    query = f"SELECT * FROM P18_PROJECT WHERE {option.get()} = '{name_entry.get()}'"
    cursor.execute(query)
    for x in cursor:
        row = x
        final = f'''Salutation: {row[0]}
First Name: {row[1]}
Last Name: {row[2]}
Mobile : {row[3]}
Email : {row[4]}
City : {row[5]}
State : {row[6]}
Occupation : {row[7]}
Salary : {row[8]}

'''
        details.insert(1.0,final)


window.mainloop()