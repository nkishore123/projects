import math
from tkinter import *
from math import *

window  = Tk()
window.title('Scientific Calculator')
e = Entry(window,borderwidth=5,width=45,justify='right',bg='black',fg='white')
e.grid(row=0,column=0,columnspan=5)

button_list = ['C','CE','sinθ','cosθ','tanθ',
               'e','n!','sinh','cosh','tanh',
               '√',chr(8731),'(',')','1/x',
               'x\u00B2','x\u00B3','x\u02b8','𝝅','/',    #'x\u02b8' = x^y, 'x\u00B3' = x^3, 'x\u00B2' = x^2
               'deg','1','2','3','+',
               'rad','4','5','6','-',
               'lg','7','8','9','*',
               'ln','.','0','%','='
               ]

row,col = 1,0
for i in button_list:
    button = Button(window,width=7,height=2,bd=2,relief='raised',text = i,bg='#28282B',fg='white',command = lambda button = i :button_click(button))
    button.grid(row = row,column=col)
    col+=1
    if col>4:
        row+=1
        col=0

def button_click(value):
    ex = e.get()
    ans=''
    try:
        if value == 'C':
            ex = ex[:-1]
            e.delete(0, END)
            e.insert(0, ex)
            return

        elif value == 'CE':
            e.delete(0, END)

        elif value == 'sinθ':
            ans = math.sin(math.radians(eval(ex)))

        elif value == 'cosθ':
            ans = math.cos(math.radians(eval(ex)))

        elif value == 'tanθ':
            ans = math.tan(math.radians(eval(ex)))

        elif value == 'sinh':
            ans = math.sinh(math.radians(eval(ex)))

        elif value == 'cosh':
            ans = math.cosh(math.radians(eval(ex)))

        elif value == 'tanh':
            ans = math.tanh(math.radians(eval(ex)))

        elif value == 'e':
            ans = math.e

        elif value == 'n!':
            x = eval(ex)
            ans = math.factorial(int(eval(ex)))

        elif value == '√':
            ans = math.sqrt(eval(ex))

        elif value == chr(8731):
            ans = math.cbrt(eval(ex))

        elif value == '1/x':
            ans = 1/eval(ex)

        elif value == 'x\u00B2':
            ans = eval(ex) ** 2

        elif value == 'x\u00B3':
            ans = eval(ex) ** 3

        elif value == '𝝅':
            ans = math.pi

        elif value == 'x\u02b8':
            e.insert(END, '**')
            return

        elif value == 'deg':
            ans = math.degrees(eval(ex))

        elif value == 'rad':
            ans = math.radians(eval(ex))

        elif value == 'ln':
            if eval(ex)>=0:
                ans = math.log2(eval(ex))
            else:
                ans = 'Error'

        elif value == 'lg':
            if eval(ex) >= 0:
                ans = math.log10(eval(ex))
            else:
                ans = 'Error'

        elif value == '=':
            e.delete(0, END)
            e.insert(0, eval(ex))
            return

        else:
            e.insert(END, value)
            return

        e.delete(0, END)
        e.insert(0, ans)
    except SyntaxError:
        pass


mainloop()
