from cryptography.fernet import Fernet
import ttkbootstrap as boottk
from ttkbootstrap.constants import *
import openai
import threading
import pyperclip

global frame_on_off
frame_on_off = "off"
global is_on
is_on = 0

try:
    with open("last_theme.txt", "r") as theme_file:
        last_theme = theme_file.readlines()[0].strip()
except:
    last_theme = "cyborg"


def encrypting(my_key):
    key = Fernet.generate_key()
    fernet = Fernet(key)
    with open("filekey.Key", "wb") as filekey:
        filekey.write(key)
    enc_key = fernet.encrypt(my_key.encode())
    return enc_key

def decrypting(enc_key):
    with open("filekey.Key", "rb") as filekey:
        key = filekey.read()
    fernet = Fernet(key)
    dec_key = fernet.decrypt(enc_key).decode()
    print(dec_key)
    return dec_key

def ask_ai():
    global is_on
    if is_on == 0:
        pb01 = boottk.Floodgauge(frame01,
            font=('Arial', 24, 'bold'),
            mask='Open AI Desktop', mode = 'indeterminate', length = '300'
            )
        pb01.grid(row = 0, column = 0, sticky=boottk.EW)
        is_on = 1
        pb01.start()

    max_tokens = 1000
    top_p_value = 0
    temperature_value = 0
    with open("my_key.txt", "rb") as file:
        encrypted_key = file.read()
    dec_key = decrypting(encrypted_key)

    openai.api_key = dec_key
    my_prompt = entry01.get("1.0", boottk.END)
    code_checkbox_value = var1.get()
    imagination_value = var2.get()
    if code_checkbox_value == 0:
        model = "text-davinci-003"
    elif code_checkbox_value == 1:
        model = "text-davinci-002"
    if imagination_value == 0:
        temperature_value = 0
    elif imagination_value == 1:
        temperature_value = 0.8
        top_p_value = 0.7
    try:
        response = openai.Completion.create(engine=model, prompt=my_prompt, max_tokens=max_tokens, n=1, top_p=top_p_value, stop=None, temperature=temperature_value)
        answer01 = response["choices"][0]["text"].strip()
        pb01.destroy()
        is_on = 0
        return answer01
    except Exception as e:
        print("no response!", str(e))
        pb01.destroy()
        is_on = 0
        return f"Somthing went wrong\n{str(e)}"

def check_key():
    try:
        with open("my_key.txt", "rb") as file:
            key_01 = file.read()
        return "key ok"
    except:
        return "no key"

def print_answer(answer01="", error_messege=0):
    key_ok = check_key()
    tag = "tag-left"
    justify_to = "left"
    if error_messege == 0:
        if check_key() == "key ok":
            answer01 = ask_ai()
            lan = check_language(answer01[0:])
            if lan == "heb":
                tag = 'tag-right'
                justify_to = "right"
            else:
                tag = "tag-left"
                justify_to = "left"

            my_prompt = entry01.get("1.0", boottk.END)
            with open ("ai_answer.txt", "a", encoding = 'utf-8-sig') as file:
                file.write(f"your question: {my_prompt}\n--------------------------\n")
                file.write(f"\nAI Response: {answer01}")
                file.write("\n\n------------------------------------------------\n\n")

        elif check_key() == "no key":
            tag = "tag-left"
            justify_to = "left"
            answer01 = "Something wend wrong! Check your key."


    answers.delete("1.0", boottk.END)
    answers.tag_configure(tag, justify=justify_to)
    answers.insert(boottk.END, f"{answer01}", tag)


def ask_ai_thread():
    thread01 =  threading.Thread(target = print_answer)
    thread01.start()
    print_answer("Wait, I am thinking about it....", 1)

def check_language(string_to_analize):
    heb = "????????????????????????????????????????????"
    eng = "abcdefghijklmnopqrstuvwxvz"
    for char in string_to_analize:
        if char.lower() in eng:
            lan = "eng"
            break
        elif char.lower() in heb:
            lan = "heb"
            break
    return lan

def change_theme():
    global frame_on_off, frame05
    if frame_on_off == "on":
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
            with open("last_theme.txt", "w") as theme_file:
                theme_file.write(my_str.get())

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

def update_key_window():
    def save_key():
        my_key = key_entry.get()
        if my_key == "" or my_key[0:2] != "sk":
            print_answer("This is not a valid OpenAI key", 1)
        else:
            enc_key = encrypting(my_key)
            with open("my_key.txt", "wb") as file:
                file.write(enc_key)
            print_answer("OpenAI Key Updated Successfully", 1)
            key_window.destroy()

    key_window = boottk.Toplevel(window)
    boottk.Label(key_window, text = "Enter Your Key").grid(row=0, column=0, padx = 10, pady = 10)
    key_entry = boottk.Entry(key_window, width = 20)
    key_entry.grid(row=0, column=1, pady = 10)
    boottk.Button(key_window, text = "Save", width = 10, command = save_key).grid(row=1, columnspan = 2, pady = 10)





window = boottk.Window()
window.style.theme_use(last_theme)
#window.geometry("2200x1500")
window.title("Open AI Desktop")
frame01 = boottk.Frame(window)
frame01.grid(row = 0, column = 0, columnspan = 2)
frame02 = boottk.Frame(window)
frame02.grid(row = 1, column = 0)
frame03 = boottk.Frame(window)
frame03.grid(row = 2, column = 0)
frame04 = boottk.Frame(window)
frame04.grid(row = 3, column = 0)

label01 = boottk.Label(frame01, text = "Open AI Desktop", font=("Arial", "20"))
label01.grid(row=0, column = 0, pady = 10)

label02 = boottk.Label(frame01, text = "Powered by openai.com API")
label02.grid(row = 1, column =0, pady=10, padx=10)

var1 = boottk.IntVar()
code_checkbox = boottk.Checkbutton(frame02, text="Code/Script     " ,variable=var1, onvalue=1, offvalue=0)
code_checkbox.grid(row=0, column = 0, padx = 10, pady = 20)

var2 = boottk.IntVar()
imagine_checkbox = boottk.Checkbutton(frame02, text="Imagination" ,variable=var2, onvalue=1, offvalue=0)
imagine_checkbox.grid(row=0, column = 1, padx = 10, pady = 20)

label01 = boottk.Label(frame03, text = "Question", font=("Arial", "9"))
label01.grid(row = 0, column = 0)
entry01 = boottk.Text(frame03, width=57,  height=18, wrap="word")
entry01.grid(row = 1, column = 0, pady = 3, padx = 10)
entry01.bind('<Button-3>',rClicker, add='')

label02 = boottk.Label(frame03, text = "Answer", font=("Arial", "9"))
label02.grid(row = 0, column = 1)
answers = boottk.Text(frame03, width=57,  height=18, wrap="word")
answers.grid(row = 1, column = 1, pady=5, padx=20)
answers.bind('<Button-3>',rClicker, add='')

button01 = boottk.Button(frame04, text = "Let's Go!", width = "20", command = ask_ai_thread)
button01.grid(row = 0, column = 0, pady=10, padx=5)

menu_bar = boottk.Menu(window)
theme_menu = boottk.Menu(menu_bar, tearoff=0)
theme_menu.add_command(label = 'Choose Theme', command = change_theme)
menu_bar.add_cascade(label="Theme ", menu=theme_menu)

save_key_menu = boottk.Menu(menu_bar, tearoff=0)
save_key_menu.add_command(label="Update/Save", command = update_key_window)
menu_bar.add_cascade(label="Update Key", menu=save_key_menu)

window.config(menu=menu_bar)

window.mainloop()
