from tkinter import *
from tkinter import ttk
import uuid, json, os, io

global my_data_list
my_data_list = []

root = Tk()
root.title('Contact List')
root.geometry("800x600")
root.configure(bg='lightgray')

input_frame = LabelFrame(root,text='Info',bg="lightgray",font=('Consolas',14))
input_frame.grid(row=0,column=0,rowspan=5,columnspan=4)

l1 = Label(input_frame, anchor="w", width=24,
           height=1, relief="ridge", text="ID",          
           font=('Consolas',14)).grid(row=1, column=0)

l2 = Label(input_frame, anchor="w", width=24, 
           height=1, relief="ridge", text="First Name",       
           font=('Consolas',14)).grid(row=2, column=0)

l3 = Label(input_frame, anchor="w", width=24, 
           height=1, relief="ridge", text="Last Name", 
           font=('Consolas',14)).grid(row=3, column=0) 

l4 = Label(input_frame, anchor="w", width=24, 
           height=1, relief="ridge", text="Cell Phone", 
           font=('Consolas',14)).grid(row=4, column=0)

id_value = StringVar()
id_value.set(uuid.uuid4())

crm_id = Label(input_frame, anchor="w", height=1,
           relief="ridge", textvariable=id_value, font=('Consolas',14))
crm_id.grid(row=1, column=1)

crm_fn = Entry(input_frame,width=30,borderwidth=2,fg="black",font=('Consolas',14))
crm_fn.grid(row=2, column=1,columnspan=2)

crm_ln = Entry(input_frame,width=30,borderwidth=2,fg="black",font=('Consolas',14))
crm_ln.grid(row=3, column=1,columnspan=2)

crm_cellphone = Entry(input_frame,width=30,borderwidth=2,fg="black",font=('Consolas',14))
crm_cellphone.grid(row=4, column=1,columnspan=2)

trv = ttk.Treeview(root, columns=(1,2,3,4),show="headings",height="16")
trv.grid(row=11,column=0, rowspan=16,columnspan=4)

trv.heading(1,text="ID", anchor="center")
trv.heading(2,text="First Name", anchor="center")
trv.heading(3,text="Last Name", anchor="center")
trv.heading(4,text="Cell Phone", anchor="center")

trv.column("#1",anchor="w",width=270, stretch=True)
trv.column("#2",anchor="w", width=140, stretch=False)
trv.column("#3",anchor="w", width=140, stretch=False)
trv.column("#4",anchor="w", width=140, stretch=False)

def startup_check():
    if os.path.isfile('contact.json') and os.access('contact.json', os.R_OK):
        # checks if file exists
        print ("File exists and is readable")
    else:
        print ("Either file is missing or is not readable, creating file...")
        with io.open(os.path.join('contact.json'), 'w') as db_file:
            db_file.write(json.dumps([]))

def load_json_from_file():
    global my_data_list
    with open("contact.json","r") as file_handler:
        my_data_list = json.load(file_handler)
    file_handler.close
    print('File has been read and closed')

def save_json_to_file():
    global my_data_list
    with open("contact.json", "w") as file_handler:
        json.dump(my_data_list, file_handler, indent=4)
    file_handler.close
    print('File has been written to and closed')

def remove_all_data_from_trv():
    for item in trv.get_children():
        trv.delete(item)

def load_trv_with_json():
    global my_data_list

    remove_all_data_from_trv()

    rowIndex=1

    for key in my_data_list:
        guid_value = key["id"]
        first_name = key["first_name"]
        last_name = key["last_name"]
        cell_phone = key["cell_phone"]
        trv.insert('',index='end',iid=rowIndex,text="",
                        values=(guid_value,first_name, last_name, cell_phone))    
        rowIndex=rowIndex+1

def clear_all_fields():
    crm_fn.delete(0,END)
    crm_ln.delete(0,END)
    crm_cellphone.delete(0,END)
    crm_id.configure(text="")
    crm_fn.focus_set()
    id_value.set(uuid.uuid4())
    change_background_color("#FFFFFF")

def find_row_in_my_data_list(guid_value):
    global my_data_list
    row     = 0
    found   = False

    for rec in my_data_list:
        if rec["id"] == guid_value:
            found = True
            break
        row = row+1

    if(found==True):
        return(row)

    return(-1)

def change_background_color(new_color):
    crm_fn.config(bg=new_color)
    crm_ln.config(bg=new_color)
    crm_cellphone.config(bg=new_color)

def change_enabled_state(state):

    if state == 'Edit':
        btnUpdate["state"]="normal"
        btnDelete["state"]="normal"
        btnAdd["state"]="disabled"
    elif state=='Cancel':
        btnUpdate["state"]="disabled"
        btnDelete["state"]="disabled"
        btnAdd["state"]="disabled"
    else:
        btnUpdate["state"]="disabled"
        btnDelete["state"]="disabled"
        btnAdd["state"]="normal"

def load_edit_field_with_row_data(_tuple):
    if len(_tuple)==0:
        return

    id_value.set(_tuple[0])
    crm_fn.delete(0,END)
    crm_fn.insert(0,_tuple[1])
    crm_ln.delete(0,END)
    crm_ln.insert(0,_tuple[2])
    crm_cellphone.delete(0,END)
    crm_cellphone.insert(0,_tuple[3])

def cancel():
    clear_all_fields()
    change_enabled_state('New')

def print_all_entries():
    global my_data_list

    for rec in my_data_list:
        print(rec)

    crm_fn.focus_set()

def add_entry():
    guid_value = id_value.get()
    first_name = crm_fn.get()
    last_name = crm_ln.get()
    cell_phone = crm_cellphone.get()

    if len(first_name)==0:
        change_background_color("#FFB2AE")
        return

    process_request('_INSERT_',guid_value,first_name,last_name,cell_phone)

def update_entry():
    guid_value = id_value.get()
    first_name = crm_fn.get()
    last_name = crm_ln.get()
    cell_phone = crm_cellphone.get()

    if len(first_name)==0:
        change_background_color("#FFB2AE")
        return

    process_request('_UPDATE_',guid_value,first_name,last_name,cell_phone)

def delete_entry():
    guid_value = id_value.get()
    process_request('_DELETE_',guid_value,None,None,None)

def process_request(command_type,guid_value,first_name,last_name, cell_phone):
    global my_data_list

    if command_type == "_UPDATE_":
        row = find_row_in_my_data_list(guid_value)
        if row >= 0:
            dict = {"id":guid_value, "first_name":first_name, 
                    "last_name":last_name, "cell_phone":cell_phone}
            my_data_list[row]=dict

    elif command_type == "_INSERT_":
        dict = {"id":guid_value, "first_name":first_name, 
                "last_name":last_name, "cell_phone":cell_phone}
        my_data_list.append(dict)

    elif command_type == "_DELETE_":
        row = find_row_in_my_data_list(guid_value)
        if row >= 0:
            del my_data_list[row]

    save_json_to_file()
    load_trv_with_json()
    clear_all_fields()

def MouseButtonUpCallBack(event):
    currentRowIndex = trv.selection()[0]
    lastTuple = (trv.item(currentRowIndex,'values'))
    load_edit_field_with_row_data(lastTuple)
    change_enabled_state('Edit')

trv.bind("<ButtonRelease>",MouseButtonUpCallBack)

ButtonFrame = LabelFrame(root,text='',bg="lightgray",font=('Consolas',14))
ButtonFrame.grid(row=5,column=0,columnspan=6)

btnShow=Button(ButtonFrame,text="Print",padx=20,pady=10,command=print_all_entries)
btnShow.pack(side=LEFT)

btnAdd=Button(ButtonFrame,text="Add",padx=20,pady=10,command=add_entry)
btnAdd.pack(side=LEFT)

btnUpdate=Button(ButtonFrame,text="Update",padx=20,pady=10,command=update_entry)
btnUpdate.pack(side=LEFT)

btnDelete=Button(ButtonFrame,text="Delete",padx=20,pady=10,command=delete_entry)
btnDelete.pack(side=LEFT)

btnClear=Button(ButtonFrame,text="Cancel",padx=18,pady=10,command=cancel)
btnClear.pack(side=LEFT)

btnExit=Button(ButtonFrame,text="Exit",padx=20,pady=10,command=root.quit)
btnExit.pack(side=LEFT)

startup_check()
load_json_from_file()
load_trv_with_json()
crm_fn.focus_set()
root.mainloop()
