import os
import platform
from urllib.parse import unquote, urlparse
from TkinterDnD2 import *
from tkinter import Label, Frame, Button, Listbox, Text, LEFT, END, TkVersion
from efectos import transporte_optimo

DEBUG_EVENT = True
def debug_event(*args):
    if DEBUG_EVENT:
        print(*args)

def convertir():
    source = carrier.get(0)
    target = objetivo.get(0)
    outfile = salida.get(0.0, END)
    print(f'CONVERTIR {source},{target},{outfile}')
    transporte_optimo(source,target,outfile)

root = TkinterDnD.Tk()
root.title('transporte_optimo i guess')
root.grid_rowconfigure(1, weight=1, minsize=250)
root.grid_columnconfigure(0, weight=1, minsize=300)
root.grid_columnconfigure(1, weight=1, minsize=300)

Label(root, text='¿Carrier?'
    ).grid(row=0, column=0, padx=10, pady=5)
Label(root, text='¿Objetivo?'
    ).grid(row=0, column=1, padx=10, pady=5)
lblSalida = Label(root, text='Salida', padx=10, pady=5
    ).grid(row=2, column=0, padx=10, pady=5)
buttonbox = Frame(root)
buttonbox.grid(row=3, column=0, columnspan=2, pady=5)
Button(buttonbox, text='Convertir', command=convertir
    ).pack(side=LEFT, padx=5)
Button(buttonbox, text='Salir', command=root.quit
    ).pack(side=LEFT, padx=5)

carrier = Listbox(root, selectmode='extended', width=1, height=1)
carrier.grid(row=1, column=0, padx=5, pady=5, sticky='news')
objetivo = Listbox(root, width=1, height=1)
objetivo.grid(row=1, column=1, pady=5, sticky='news')

salida = Text(root, wrap='word', undo=True, width=1, height=1)
salida.grid(row=2, column=1, padx=5, pady=5, sticky='news')

def drop_enter(event):
    event.widget.focus_force()
    debug_event('Entering widget: %s' % event.widget)
    return event.action

def drop_position(event):
    debug_event('Position: x %d, y %d' %(event.x_root, event.y_root))
    return event.action

def drop_leave(event):
    debug_event('Leaving %s' % event.widget)
    return event.action

def drop(event):
    if event.data:
        debug_event('Dropped data:\n', event.data)
        if event.widget == carrier:
            # event.data is a list of filenames as one string;
            # if one of these filenames contains whitespace characters
            # it is rather difficult to reliably tell where one filename
            # ends and the next begins; the best bet appears to be
            # to count on tkdnd's and tkinter's internal magic to handle
            # such cases correctly; the following seems to work well
            # at least with Windows and Gtk/X11
            files = carrier.tk.splitlist(event.data)
            for f in files:
                if os.path.exists(f):
                    debug_event('Dropped file: "%s"' % f)
                    carrier.insert('end', f)
                else:
                    print('Not dropping file "%s": file does not exist.' % f)
        elif event.widget == objetivo:
            files = objetivo.tk.splitlist(event.data)
            for f in files:
                if os.path.exists(f):
                    debug_event('Dropped file: "%s"' % f)
                    objetivo.insert('end', f)
                else:
                    print('Not dropping file "%s": file does not exist.' % f)
        elif event.widget == salida:
            salida.delete(0.0, END)
            salida.insert(0.0, event.data)
        else:
            print('Error: reported event.widget not known')
    return event.action

# now make the Listbox and Text drop targets
carrier.drop_target_register(DND_FILES, DND_TEXT)
objetivo.drop_target_register(DND_FILES)
salida.drop_target_register(DND_FILES)

for widget in (carrier, objetivo, salida):
    widget.dnd_bind('<<DropEnter>>', drop_enter)
    widget.dnd_bind('<<DropPosition>>', drop_position)
    widget.dnd_bind('<<DropLeave>>', drop_leave)
    widget.dnd_bind('<<Drop>>', drop)
    #widget.dnd_bind('<<Drop:DND_Files>>', drop)
    #widget.dnd_bind('<<Drop:DND_Text>>', drop)

root.update_idletasks()
root.deiconify()
root.mainloop()

