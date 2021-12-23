#!/usr/bin/python3
# Black-Notepad v1.0
#

from tkinter import *
import os,sys
from tkinter import font
from webbrowser import open_new_tab
from subprocess import getoutput
import tkinter.filedialog
import tkinter.messagebox

root = Tk()
title_ = "Black Notepad"
root.title(title_)
file_name = None
root.geometry('800x700+300+50')
root.iconphoto(False,PhotoImage(file='./Scr/blacknotepad-logo.png'))
def new_file(event=None):
    root.title("Untitled")
    global file_name
    file_name = None
    content_text.delete(1.0, END)
    on_content_changed()
def open_file(event=None):
    input_file_name = tkinter.filedialog.askopenfilename(defaultextension=".txt",filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt"),("HTML", "*.html"),("CSS", "*.css"),("JavaScript", "*.js")])
    if input_file_name:
        global file_name
        file_name = input_file_name
        root.title('{} - {}'.format(os.path.basename(file_name), title_))
        content_text.delete(1.0, END)
        with open(file_name) as _file:
            content_text.insert(1.0, _file.read())
    
    on_content_changed()
     
def write_to_file(file_name):
    try:
        content = content_text.get(1.0, 'end')
        with open(file_name, 'w') as the_file:
            the_file.write(content)
    except IOError:
        pass  
def save_as(event=None):
    input_file_name = tkinter.filedialog.asksaveasfilename(defaultextension=".txt",filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt"),("HTML", "*.html"),("CSS", "*.css"),("JavaScript", "*.js")])
    if input_file_name:
        global file_name
        file_name = input_file_name
        write_to_file(file_name)
        root.title('{} - {}'.format(os.path.basename(file_name), title_))
    return "break"
    
def save(event=None):
    global file_name
    if not file_name:
        save_as()
    else:
        write_to_file(file_name)
    return "break"

def cut():
    content_text.event_generate("<<Cut>>")
    on_content_changed()
    return "break"
def copy():
    content_text.event_generate("<<Copy>>")
    on_content_changed()
    return "break"
def paste():
    content_text.event_generate("<<Paste>>")
    on_content_changed()
    return "break"
def undo():
    content_text.event_generate("<<Undo>>")
    on_content_changed()
    return "break"
def redo(event=None):
    content_text.event_generate("<<Redo>>")
    on_content_changed()
    return "break"
def selectall(event=None):
    content_text.tag_add('sel','1.0','end')
    return "break"
   
def find_text(event=None):
    search_toplevel = Toplevel(root)
    search_toplevel.title('Find Text')
    search_toplevel.transient(root)
    search_toplevel.resizable(False, False)
    Label(search_toplevel, text="Find All:").grid(row=0, column=0, sticky='e')
    search_entry_widget = Entry(search_toplevel, width=25)
    search_entry_widget.grid(row=0, column=1, padx=2, pady=2, sticky='we')
    search_entry_widget.focus_set()
    ignore_case_value = IntVar()
    Checkbutton(search_toplevel, text='Ignore Case', variable=ignore_case_value).grid(row=1, column=1, sticky='e', padx=2, pady=2)
    Button(search_toplevel, text="Find All", underline=0,
           command=lambda: search_output(
               search_entry_widget.get(), ignore_case_value.get(),
               content_text, search_toplevel, search_entry_widget)
           ).grid(row=0, column=2, sticky='e' + 'w', padx=2, pady=2)
    def close_search_window():
        content_text.tag_remove('match', '1.0', END)
        search_toplevel.destroy()
    search_toplevel.protocol('WM_DELETE_WINDOW', close_search_window)
    return "break"
def search_output(needle,if_ignore_case, content_text, search_toplevel, search_box):
    content_text.tag_remove('match','1.0', END)
    matches_found=0
    if needle:
        start_pos = '1.0'
        while True:
            start_pos = content_text.search(needle,start_pos, nocase=if_ignore_case, stopindex=END)
            if not start_pos:
                break
            end_pos = '{} + {}c'. format(start_pos, len(needle))
            content_text.tag_add('match', start_pos, end_pos)
            matches_found +=1
            start_pos = end_pos
        content_text.tag_config('match', background='yellow', foreground='blue')
    search_box.focus_set()
    search_toplevel.title('{} matches found'.format(matches_found))

def display_about(event=None):
    tkinter.messagebox.showinfo(
        "About", title_ + "\nA simple Text Editor made in Python with Tkinter\n -Nabin Jaiswal")
def display_help(event=None):
    tkinter.messagebox.showinfo(
        "Help", "This Text Editor works similar to any other editors.",
        icon='question')
def exit_editor(event=None):
    if content_text.get(1.0,'end-1c') != '':
        try:
            q = tkinter.messagebox.askyesnocancel(title="Black-Notepad",message="Do you Want to Save Chaned Untitled? ")
            if q:
                file = tkinter.filedialog.asksaveasfile(title="Save File",mode="w")
                file.write(content_text.get(1.0,'end-1c'))
                file.close()
                root.destroy()
            elif q == None:
                pass
            else:
                root.destroy()
                
        except (Exception,):
            pass
    else:
        root.destroy()

def get_line_numbers():
    output = ''
    if show_line_number.get():
        row, col = content_text.index("end").split('.')
        for i in range(1, int(row)):
            output += str(i) + '\n'
    return output
def on_content_changed(event=None):
    update_line_numbers()
    update_cursor()
def update_line_numbers(event=None):
    line_numbers = get_line_numbers()
    line_number_bar.config(state='normal')
    line_number_bar.delete('1.0', 'end')
    line_number_bar.insert('1.0', line_numbers)
    line_number_bar.config(state='disabled')

def show_cursor():
    show_cursor_info_checked = show_cursor_info.get()
    if show_cursor_info_checked:
        cursor_info_bar.pack(expand='no', fill=None, side='right', anchor='se')
    else:
        cursor_info_bar.pack_forget()
def update_cursor(event=None):
    row, col = content_text.index(INSERT).split('.')
    line_num, col_num = str(int(row)), str(int(col) + 1)  
    infotext = "Line: {0} | Column: {1}".format(line_num, col_num)
    cursor_info_bar.config(text=infotext)

def highlight_line(interval=100):
    content_text.tag_remove("active_line", 1.0, "end")
    content_text.tag_add(
        "active_line", "insert linestart", "insert lineend+1c")
    content_text.after(interval, toggle_highlight)
def undo_highlight():
    content_text.tag_remove("active_line", 1.0, "end")
def toggle_highlight(event=None):
    if to_highlight_line.get():
        highlight_line()
    else:
        undo_highlight()

def change_theme(event=None):
    selected_theme = theme_choice.get()
    fg_bg_colors = color_schemes.get(selected_theme)
    foreground_color, background_color = fg_bg_colors.split('.')
    content_text.config(
        background=background_color, fg=foreground_color)

def show_popup_menu(event):
    popup_menu.tk_popup(event.x_root, event.y_root)
    
def new_window(event=None):
    getoutput("python black.py")
def print_paper(event=None):
    try:
        # content_text
        getoutput(f"")
    except (Exception,):
        print(False)
def delete(event=None):
    content_text.delete('1.0',END)
def reload(event=None):
    content_text.event_generate("<<Reload>>")
menu_bar = Menu(root) 
file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label='New', accelerator='Ctrl+N', compound='left', command=new_file)
file_menu.add_command(label="New Window",accelerator='Ctrl+Shift+N',compound='left',command=new_window)
file_menu.add_command(label='Open', accelerator='Ctrl+O', compound='left', command=open_file)
file_menu.add_command(label="Save", accelerator='Ctrl+S', compound='left',  command=save)
file_menu.add_command(label="Save As", accelerator='Ctrl+Shift+S', compound='left', underline=0, command=save_as)
file_menu.add_separator()
file_menu.add_command(label="Print",command=print_paper)
file_menu.add_separator()
file_menu.add_command(label="Exit", accelerator='Alt+F4', compound='left', underline=0, command=exit_editor)
menu_bar.add_cascade(label='File', menu=file_menu)

edit_menu = Menu(menu_bar, tearoff=0)
edit_menu.add_command(label='Undo', accelerator='Ctrl+Z', compound='left',  command=undo)
edit_menu.add_command(label='Redo', accelerator='Ctrl+Y', compound='left',command=redo)
edit_menu.add_separator()
edit_menu.add_command(label='Cut', accelerator='Ctrl+X', compound='left', command=cut) 
edit_menu.add_command(label='Copy', accelerator='Ctrl+C', compound='left',  command=copy)
edit_menu.add_command(label='Paste', accelerator='Ctrl+V', compound='left',    command=paste)
edit_menu.add_separator()
edit_menu.add_command(label='Find', accelerator='Ctrl+F', compound='left', command=find_text)
edit_menu.add_separator()
edit_menu.add_command(label="Reload",accelerator='Ctrl+R',command=reload)
edit_menu.add_command(label="Delete",accelerator='Delete',command=delete)
edit_menu.add_separator()
edit_menu.add_command(label='Select All', accelerator='Ctrl+A', compound='left',  command=selectall) 
menu_bar.add_cascade(label='Edit', menu=edit_menu)

view_menu = Menu(menu_bar, tearoff=0)
show_line_number=IntVar()
show_line_number.set(1)
view_menu.add_checkbutton(label="Show Line Number", variable=show_line_number)
show_cursor_info=IntVar()
show_cursor_info.set(1)
view_menu.add_checkbutton(label='Show Cursor Location at Bottom', variable=show_cursor_info, command=show_cursor)
to_highlight_line=IntVar()
view_menu.add_checkbutton(label='Highlight Current Line', variable=to_highlight_line, onvalue=1, offvalue=0,command=toggle_highlight)
themes_menu=Menu(menu_bar, tearoff=0)
view_menu.add_cascade(label='Themes', menu=themes_menu, command=change_theme)
''' THEMES OPTIONS'''
color_schemes = {
    'Hacker':'lightgreen.#111111',
    'Default': '#000000.#FFFFFF',
    'Greygarious': '#83406A.#D1D4D1',
    'Aquamarine': '#5B8340.#D1E7E0',
    'Bold Beige': '#4B4620.#FFF0E1',
    'Cobalt Blue': '#ffffBB.#3333aa',
    'Olive Green': '#D1E7E0.#5B8340',
    'Night Mode': '#FFFFFF.#000000',
}
theme_choice=StringVar()
theme_choice.set('Default')
for k in sorted(color_schemes):
    themes_menu.add_radiobutton(label=k, variable=theme_choice, command=change_theme)
fstyle = "None"
fsize = 10

def _10():
    global fsize
    fsize = 10
    content_text.configure(font=(fstyle,fsize))
def _20():
    global fsize
    fsize = 20
    content_text.configure(font=(fstyle,fsize))
def _30():
    global fsize
    fsize = 30
    content_text.configure(font=(fstyle,fsize))
def _40():
    global fsize
    fsize = 40
    content_text.configure(font=(fstyle,fsize))
def _50():
    global fsize
    fsize = 50
    content_text.configure(font=(fstyle,fsize))
def _60():
    global fsize
    fsize = 60
    content_text.configure(font=(fstyle,fsize))
def _70():
    global fsize
    fsize = 70
    content_text.configure(font=(fstyle,fsize))
def _80():
    global fsize
    fsize = 80
    content_text.configure(font=(fstyle,fsize))
def _90():
    global fsize
    fsize = 90
    content_text.configure(font=(fstyle,fsize))
def _100():
    global fsize
    fsize = 100
    content_text.configure(font=(fstyle,fsize))
def none_style():
    global fstyle
    fstyle = "None"
    content_text.configure(font=(fstyle,fsize))
def cooper_style():
    global fstyle
    fstyle = "Cooper"
    content_text.configure(font=(fstyle,fsize))
def Corbel_style():
    global fstyle
    fstyle = "Corbel"
    content_text.configure(font=(fstyle,fsize))
def Courier_style():
    global fstyle
    fstyle = "Courier"
    content_text.configure(font=(fstyle,fsize))
def Dubai_style():
    global fstyle
    fstyle = "Dubai"
    content_text.configure(font=(fstyle,fsize))
def Elephant_style():
    global fstyle
    fstyle = "Elephant"
    content_text.configure(font=(fstyle,fsize))
def E_style():
    global fstyle
    fstyle = "Edwardian Script ITC"
    content_text.configure(font=(fstyle,fsize))
def Footlight_style():
    global fstyle
    fstyle = "Footlight MT"
    content_text.configure(font=(fstyle,fsize))
def Gigi_style():
    global fstyle
    fstyle = "Gigi"
    content_text.configure(font=(fstyle,fsize))
def set_si(event=None):
    global fsize
    fsize = s_i.get()
    content_text.configure(font=(fstyle,fsize))

def set_st(event=None):
    global fstyle
    fstyle = ss_i.get()
    content_text.configure(font=(fstyle,fsize))

def set_size():
    global s_i
    root = Tk()
    root.title("Black-Notepad/Set-Size")
    root.geometry("300x200+500+100")
    s_i = Spinbox(root,from_=1,to=500)
    s_i.place(bordermode=INSIDE,x=80,y=15)
    set_b = Button(root,text="Set",width=5,height=2,command=set_si)
    set_b.place(bordermode=OUTSIDE,x=125,y=42)
    exit_b = Button(root,text="Exit",width=5,height=2,command=root.destroy)
    exit_b.place(bordermode=OUTSIDE,x=125,y=86)
    root.bind("<Return>",set_si)
    root.attributes('-toolwindow',True)
    root.mainloop()
def set_style():
    global ss_i
    root = Tk()
    root.title("Black-Notepad/Set-Style")
    root.geometry("300x200+500+100")
    ss_i = Entry(root,border=3)
    ss_i.place(bordermode=INSIDE,x=80,y=15)
    set_b = Button(root,text="Set",width=5,height=2,command=set_st)
    set_b.place(bordermode=OUTSIDE,x=125,y=42)
    exit_b = Button(root,text="Exit",width=5,height=2,command=root.destroy)
    exit_b.place(bordermode=OUTSIDE,x=125,y=86)
    root.bind("<Return>",set_st)
    root.attributes('-toolwindow',True)
    root.mainloop()
font_style = Menu(view_menu,tearoff=0)
font_size = Menu(view_menu,tearoff=0)
font_style.add_command(label="None",command=none_style)
font_style.add_command(label="Cooper",command=cooper_style)
font_style.add_command(label="Corbel",command=Corbel_style)
font_style.add_command(label="Courier",command=Courier_style)
font_style.add_command(label="Dubai",command=Dubai_style)
font_style.add_command(label="Edwardian Script ITC",command=E_style)
font_style.add_command(label="Elephant",command=Elephant_style)
font_style.add_command(label="Footlight MT",command=Footlight_style)
font_style.add_command(label="Gigi",command=Gigi_style)
font_style.add_separator()
font_style.add_command(label="Set Style",command=set_style)
font_size.add_command(label=10,command=_10)
font_size.add_command(label=20,command=_20)
font_size.add_command(label=30,command=_30)
font_size.add_command(label=40,command=_40)
font_size.add_command(label=50,command=_50)
font_size.add_command(label=60,command=_60)
font_size.add_command(label=70,command=_70)
font_size.add_command(label=80,command=_80)
font_size.add_command(label=90,command=_90)
font_size.add_command(label=100,command=_100)
font_size.add_separator()
font_size.add_command(label="Set Size",command=set_size)
view_menu.add_cascade(label="Font Style",menu=font_style)
view_menu.add_cascade(label="Font Size",menu=font_size)
menu_bar.add_cascade(label='View', menu=view_menu)
def help(event=None):
    open_new_tab('https://black-software-com.github.io/Black-Help/')
def feedback(event=None):
    open_new_tab('https://github.com/black-software-Com/Black-Notepad/issues')
def instagram():
    open_new_tab('https://instagram.com/black_software_company')
def license(event=None):
    open_new_tab('https://github.com/black-software-Com/Black-Help/blob/master/LICENSE')

about_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label='About', menu=about_menu)
about_menu.add_command(label='Help', accelerator='Ctrl+H',underline=0, command=help)
about_menu.add_command(label="Join On Instagram",command=instagram)
about_menu.add_separator()
about_menu.add_command(label="View License",accelerator='Ctrl+L',command=license)
about_menu.add_separator()
about_menu.add_command(label="Send Feedback",accelerator='Ctrl+F',command=feedback)
root.config(menu=menu_bar)
shortcut_bar=Frame(root, height=25)
shortcut_bar.pack(expand='no', fill='x')
line_number_bar = Text(root, width=4, padx=3, takefocus=0, fg='white', border=0, background='#282828', state='disabled',  wrap='none')
line_number_bar.pack(side='left', fill='y')
content_text = Text(root, wrap='word')
content_text.pack(expand='yes', fill='both')
scroll_bar = Scrollbar(content_text)
content_text.configure(yscrollcommand=scroll_bar.set)
scroll_bar.config(command=content_text.yview)
scroll_bar.pack(side='right', fill='y')
cursor_info_bar = Label(content_text, text='Line: 1 | Column: 1',background='white',foreground='black')
cursor_info_bar.pack(expand='no', fill=None, side='right', anchor='se')
popup_menu = Menu(content_text,tearoff=0)
popup_menu.add_command(label="Undo",accelerator='Ctrl+Z',underline=1,command=undo)
popup_menu.add_command(label="Redo",accelerator='Ctrl+Y',underline=2,command=redo)
popup_menu.add_separator()
popup_menu.add_command(label="Cut",accelerator='Ctrl+X',underline=3,command=cut)
popup_menu.add_command(label="Copy",accelerator='Ctrl+C',underline=4,command=copy)
popup_menu.add_command(label="Paste",accelerator='Ctrl+V',underline=5,command=paste)
popup_menu.add_separator()
popup_menu.add_command(label="Reload",accelerator='Ctrl+R',underline=6,command=reload)
popup_menu.add_command(label="Delete",accelerator='Delete',underline=7,command=delete)
popup_menu.add_separator()
popup_menu.add_command(label='Select All', accelerator='Ctrl+A',underline=8, command=selectall)
content_text.bind('<Button-3>', show_popup_menu)
content_text.bind('<Control-N>', new_file)
content_text.bind('<Control-n>', new_file)
content_text.bind('<Control-O>', open_file)
content_text.bind('<Control-o>', open_file)
content_text.bind('<Control-S>', save)
content_text.bind('<Control-s>', save)
content_text.bind('<Control-Y>',redo)
content_text.bind('<Control-y>',redo)
content_text.bind('<Control-A>',selectall)
content_text.bind('<Control-a>',selectall)
content_text.bind('<Control-F>',find_text)
content_text.bind('<Control-f>',find_text)
content_text.bind("<Control-r>",reload)
content_text.bind("<Control-R>",reload)
content_text.bind("<Control-h>",help)
content_text.bind("<Control-H>",help)
content_text.bind("<Control-f>",feedback)
content_text.bind("<Control-F>",feedback)
content_text.bind("<Control-l>",license)
content_text.bind("<Control-L>",license)
content_text.bind("<Delete>",delete)
content_text.bind('<Any-KeyPress>', on_content_changed)
content_text.tag_configure('active_line', background='ivory2')
content_text.bind('<Button-3>', show_popup_menu)
content_text.focus_set()
root.protocol('WM_DELETE_WINDOW', exit_editor)
root.mainloop()
