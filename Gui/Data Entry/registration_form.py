import tkinter.ttk
from tkinter import *
import mysql.connector as mysql

window = Tk()
window.title('Registration Form')
font = ('arial', 14)
lf = LabelFrame(window,pady=20,border=5)
lf.grid(row = 0,column=0,columnspan=3)

l = Label(lf,text='Register Here',width=30,font = ('arial',18),justify='center')
l.grid(row=1,column=1)

labels = ['Title','First Name', 'Last Name', 'Mobile Number', 'Email address', 'City', 'State','Occupation', 'Salary']

row,col = 2,0
for label in labels:
    l1 = Label(lf, text=label,width=30,font=font,padx=10,pady=10)
    l1.grid(row=row, column=col)
    col+=1
    if col>2:
        row+=2
        col=0

# Entries

Title = tkinter.ttk.Combobox(lf, values=['Mr','Ms','Mrs'], width=30, font=font)
Title.grid(row=3, column=0)

First_Name =  Entry(lf, width=30, font=font)
First_Name.grid(row=3,column=1)

Last_Name = Entry(lf, width=30, font=font)
Last_Name.grid(row=3,column=2)

Mobile_Number = Entry(lf, width=30, font=font)
Mobile_Number.grid(row=5,column=0)

Email = Entry(lf, width=30, font=font)
Email.grid(row=5,column=1)

City = Entry(lf, width=30, font=font)
City.grid(row=5,column=2)

State = Entry(lf, width=30, font=font)
State.grid(row=7,column=0)

Occupation = Entry(lf, width=30, font=font)
Occupation.grid(row=7,column=1)

Salary = Entry(lf, width=30, font=font)
Salary.grid(row=7,column=2)

# Buttons

clear = Button(window,text='Clear',bg='red',fg='white',padx=20,pady=10,font=font,command=lambda:click('Clear'))
clear.grid(row=7,column=0)

mes = Label(text="")
mes.grid(row=7,column=1)

submit = Button(window,text='Submit',bg='green',fg='white',padx=20,pady=10,font=font,command=lambda:click('Submit'))
submit.grid(row=7,column=2)

Entries = [Title,First_Name, Last_Name, Mobile_Number, Email, City, State,Occupation, Salary]

# Establish a connection
mydb = mysql.connect(
    host='localhost',
    user='root',
    password='Kishore@95',
    database='db1')

# Cursor to execute the statements
cursor = mydb.cursor()

def click(val):
    if val == 'Clear':
        for entry in Entries:
            entry.delete(0,END)
        mes.config(text="your details are cleared")

    elif val == 'Submit':
        final = list()
        for entry in Entries:
            x = entry.get()
            final.append(x)
        final = tuple(final)
        query = 'INSERT INTO P18_PROJECT VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        values = final
        cursor.execute(query, values)
        mydb.commit()
        for entry in Entries:
            entry.delete(0,END)

        mes.config(text="your details are submitted")



window.mainloop()


