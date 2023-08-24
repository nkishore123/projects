import tkinter
from tkinter import *
from tkinter import ttk,messagebox
import googletrans
import textblob


window = Tk()
window.title('Language Translator')
window.geometry('720x480')
font = ('normal',12)

def translate():
    translated_text.delete(1.0,END)
    try:
        for k,v in languages.items():
            if(v==lang1.get()):
                from_key = k
        for k,v in languages.items():
            if(v==lang2.get()):
                to_key = k
        words = textblob.TextBlob(original_text.get(1.0,END))
        words = words.translate(from_lang=from_key,to=to_key)
        translated_text.insert(1.0,words)

    except Exception as e:
        messagebox.showerror('Error',e)

def clear():
    original_text.delete(1.0,END)
    translated_text.delete(1.0,END)

languages = googletrans.LANGUAGES
lang_values=list(languages.values())


l1 = Label(window,text="Welcome to Language Translator",width=30,font= ('arial',30),bg='grey',fg='yellow',justify='center')
l1.grid(row=0,column=0,columnspan=10)

l2 = Label(window,text='Select a language',pady=10,font=font)
l2.grid(row = 1,column=1)

l3 = Label(window,text='Select a language',pady=10,font=font)
l3.grid(row = 1,column=7)

lang1 = ttk.Combobox(window,values=lang_values,state='r')
lang1.set('You have')
lang1.grid(row = 2,column=1)

lang2 = ttk.Combobox(window,values=lang_values,state='r')
lang2.set('You need')
lang2.grid(row = 2,column=7)

original_text = Text(window,height=10,width=30,font=font)
original_text.grid(row=3,column=1)

translated_text = Text(window,height=10,width=30,font=font)
translated_text.grid(row=3,column=7)

b1 = Button(window,text='Translate',bg='teal',fg='white',font=font,command=translate)
b1.grid(row=3,column=4)

b2 = Button(window,text='Clear',bg='teal',fg='white',font=font,command=clear)
b2.grid(row=4,column=4)

window.mainloop()

