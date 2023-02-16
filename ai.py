import tkinter as tk
from tkinter import *
from tkinter import messagebox, ttk, Menu
import ttkbootstrap as boottk
from ttkbootstrap.constants import *
import os
import openai
import threading
import pyperclip

global frame_on_off
frame_on_off = "off"
tag = "tag-left"
justify_to = "left"
global is_on
is_on = 0

def ask_ai():
    global is_on
    if is_on == 0:
        pb01 = boottk.Floodgauge(frame01,
            font=(None, 24, 'bold'),
            mask='Open AI', mode = 'indeterminate', length = '140'
            )
        pb01.grid(row = 0, column = 0)
        is_on = 1
        pb01.start()

    max_tokens = 1000
    top_p_value = 0
    temperature_value = 0

    print("wait, I am thinking about it...")
    with open("my_key.txt", "r") as file:
        openai.api_key = file.readlines()[0].strip()
#    print(openai.api_key)
#    openai.api_key = my_key.api_key

    my_prompt = entry01.get("1.0", tk.END)
    code_checkbox_value = var1.get()
    imagination_value = var2.get()
    if code_checkbox_value == 0:
        model = "text-davinci-003"
    elif code_checkbox_value == 1:
        model = "text-davinci-002"
    if imagination_value == 0:
        temperature_value = 0
    elif imagination_value == 1:
        print("imagine")
        temperature_value = 0.8
        top_p_value = 0.7
    try:
        response = openai.Completion.create(engine=model, prompt=my_prompt, max_tokens=max_tokens, n=1, top_p=top_p_value, stop=None, temperature=temperature_value)
        answer01 = response["choices"][0]["text"].strip()
    except:
        answers.delete("1.0", tk.END)
        answers.tag_configure(tag, justify=justify_to)
        answers.insert(tk.END, "Somthing went wrong :-(\nTry Again)", tag)

    if is_on == 1:
        pb01.destroy()
        is_on = 0
    lan = check_language(answer01[0:10])
    if lan == "heb":
        tag = 'tag-right'
        justify_to = "right"
    else:
        tag = "tag-left"
        justify_to = "left"
    answers.delete("1.0", tk.END)
    answers.tag_configure(tag, justify=justify_to)
    answers.insert(tk.END, f"{answer01}", tag)
    with open ("ai_answer.txt", "a", encoding = 'utf-8-sig') as file:
        file.write(f"your question: {my_prompt}\n--------------------------\n")
        file.write(f"\nAI Response: {answer01}")
        file.write("\n\n------------------------------------------------\n\n")


def ask_ai_thread():
    global thread01
    thread01 =  threading.Thread(target = ask_ai)
    print("start thread")
    thread01.start()
    answers.delete("1.0", tk.END)
    answers.insert(tk.END, "Wait, I am thinking about it....")


def check_language(string_to_analize):
    heb = "אבגדהוזחטיכלמנסעפצקרשת"
    eng = "abcdefghijklmnopqrstuvwxvz"
    for char in string_to_analize:
        if char.lower() in eng:
            lan = "eng"
            break
    else: lan = "heb"
    return lan

def change_theme():
    global frame_on_off, frame05
    print(frame_on_off)
    if frame_on_off == "on":
        print(frame05, "hello")
        frame05.destroy()
        frame_on_off = "off"
    else:
        frame_on_off = "on"
        frame05 = boottk.Frame(window)
        frame05.grid(row = 4, column = 0)
        my_themes = window.style.theme_names()  # List of available themes
        my_str = boottk.StringVar(value=window.style.theme_use())  # default selection of theme

        r, c = 0, 0  # row=0 and column =0
        for values in my_themes:  # List of available themes
            b = boottk.Radiobutton(
            frame05, text=values, variable=my_str, value=values, command=lambda: my_upd()
            )    # Radio buttons with themes as values
            b.grid(row=r, column=c, padx=5, pady=20)
            c = c + 1  # increase column by 1
            if c > 8:  # One line complete so change the row and column values
                r, c = r + 1, 0

        def my_upd():
            window.style.theme_use(my_str.get())
            print(my_str.get())
def rClicker(e):
    ''' right click context menu for all Tk Entry and Text widgets
    '''

    try:
        def rClick_Copy(e, apnd=0):
            e.widget.event_generate('<Control-c>')

        def rClick_Cut(e):
            e.widget.event_generate('<Control-x>')

        def rClick_Paste(e):
            e.widget.event_generate('<Control-v>')
        def rClick_Select_all(e):
            e.widget.event_generate('<Control-a>')

        e.widget.focus()

        nclst=[
               (' Cut', lambda e=e: rClick_Cut(e)),
               (' Copy', lambda e=e: rClick_Copy(e)),
               (' Paste', lambda e=e: rClick_Paste(e)),
               (' Select All', lambda e=e: rClick_Select_all(e))
               ]

        rmenu = Menu(None, tearoff=0, takefocus=0)

        for (txt, cmd) in nclst:
            rmenu.add_command(label=txt, command=cmd)

        rmenu.tk_popup(e.x_root+40, e.y_root+10,entry="0")

    except TclError:
        print (' - rClick menu, something wrong')
        pass

    return "break"


def rClickbinder(r):

    try:
        for b in [ 'Text', 'Entry', 'Listbox', 'Label']: #
            r.bind_class(b, sequence='<Button-3>',
                         func=rClicker, add='')
    except TclError:
        print (' - rClickbinder, something wrong')
        pass


#right click menu for text box - copy, select all
def showMenu(event):
    global clickedWidget
    clickedWidget = event.widget
    popup.post(event.x_root, event.y_root)


window = boottk.Window()
window.style.theme_use("darkly")
#window.geometry("2200x1500")
window.title("Open AI")
frame01 = boottk.Frame(window)
frame01.grid(row = 0, column = 0)
frame02 = boottk.Frame(window)
frame02.grid(row = 1, column = 0)
frame03 = boottk.Frame(window)
frame03.grid(row = 2, column = 0)
frame04 = boottk.Frame(window)
frame04.grid(row = 3, column = 0)

label01 = boottk.Label(frame01, text = "Open AI", font=("Arial", "20"))
label01.grid(row=0, column = 0, columnspan = 2, pady = 10)

label02 = boottk.Label(frame01, text = "שאל אותי שאלה")
label02.grid(row = 1, column =0, pady=20, padx=20)

var1 = IntVar()
code_checkbox = Checkbutton(frame02, text="Code/Script" ,variable=var1, onvalue=1, offvalue=0)
code_checkbox.grid(row=0, column = 0, padx = 10, pady = 10)

var2 = IntVar()
imagine_checkbox = Checkbutton(frame02, text="Imagination" ,variable=var2, onvalue=1, offvalue=0)
imagine_checkbox.grid(row=0, column = 1, padx = 10, pady = 10)

label01 = boottk.Label(frame03, text = "Question", font=("Arial", "9"))
label01.grid(row = 0, column = 0)
entry01 = boottk.Text(frame03, width=57,  height=18, wrap="word")
entry01.grid(row = 1, column = 0, pady = 3, padx = 10)
entry01.bind('<Button-3>',rClicker, add='')

label02 = boottk.Label(frame03, text = "Answer", font=("Arial", "9"))
label02.grid(row = 0, column = 1)
answers = boottk.Text(frame03, width=57,  height=18, wrap="word")
answers.insert("1.0", "All answers are saved in a text file (ai_answer.txt) on your local directory")
answers.grid(row = 1, column = 1, pady=5, padx=20)
answers.bind('<Button-3>',rClicker, add='')

button01 = boottk.Button(frame04, text = "Let's Go!", width = "20", command = ask_ai_thread)
button01.grid(row = 0, column = 0, pady=10, padx=5)

menubar = Menu(window)
window.config(menu = menubar)
menubar.add_command(label = 'Choose Theme', command = lambda: change_theme())

window.mainloop()
