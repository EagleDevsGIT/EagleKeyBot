import tkinter as tk
import sqlite3
import random
import string
import pyperclip
import traceback

def generate_and_register_key(user_id):
    c.execute("SELECT key FROM keys WHERE user_id=?", (user_id,))
    result = c.fetchone()
    if result:
        return result[0]
    key = ''.join(random.choices(string.ascii_uppercase + string.digits, k=25))
    c.execute("INSERT INTO keys VALUES (?, ?)", (user_id, key))
    conn.commit()
    traceback.print_exc()
    return key

def generate_key():
    user_id = user_id_entry.get()
    key = generate_and_register_key(user_id)
    key_label.config(text=f'Your key is: {key}')
    copy_button.config(state=tk.NORMAL)
    user_id_entry.delete(0, tk.END)
    update_keys_listbox()

def remove_key():
    user_id = user_id_entry.get()
    c.execute("DELETE FROM keys WHERE user_id=?", (user_id,))
    conn.commit()
    status_label.config(text=f'Removed key for user {user_id}')
    key_label.config(text='')
    copy_button.config(state=tk.DISABLED)
    user_id_entry.delete(0, tk.END)
    update_keys_listbox()

def copy_key():
    key = key_label.cget("text")
    pyperclip.copy(key)

def update_keys_listbox():
    keys_listbox.delete(0, tk.END)
    c.execute("SELECT user_id, key FROM keys")
    rows = c.fetchall()
    for row in rows:
        keys_listbox.insert(tk.END, f"{row[0]}: {row[1]}")

def delete_key():
    selection = keys_listbox.curselection()
    if selection:
        user_id = keys_listbox.get(selection[0]).split(":")[0]
        c.execute("DELETE FROM keys WHERE user_id=?", (user_id,))
        conn.commit()
        update_keys_listbox()
        status_label.config(text=f"Removed key for user {user_id}")
    else:
        status_label.config(text="Please select a key to delete")

conn = sqlite3.connect('generatedKeys.db')

c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS keys
             (user_id INTEGER PRIMARY KEY, key TEXT NOT NULL)''')

root = tk.Tk()
root.configure(bg='red')
root.title('Key Generator')
root.geometry('600x250')

left_frame = tk.Frame(root, width=200)
left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

user_id_label = tk.Label(left_frame, text='User ID:')
user_id_label.pack()

user_id_entry = tk.Entry(left_frame)
user_id_entry.pack()

generate_button = tk.Button(left_frame, text='Generate Key', command=generate_key)
generate_button.pack()

key_label = tk.Label(left_frame, text='')
key_label.pack()

copy_button = tk.Button(left_frame, text='Copy Key', command=copy_key, state=tk.DISABLED)
copy_button.pack()

remove_button = tk.Button(left_frame, text='Remove Key', command=remove_key)
remove_button.pack()

status_label = tk.Label(left_frame, text='')
status_label.pack()

right_frame = tk.Frame(root, width=400)
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

keys_label = tk.Label(right_frame, text='Keys:')
keys_label.pack()

delete_button = tk.Button(right_frame, text="Delete Key", command=delete_key)
delete_button.pack(side=tk.BOTTOM, pady=10)

keys_listbox = tk.Listbox(right_frame)
keys_listbox.pack(fill=tk.BOTH, expand=True)

update_keys_listbox()

root.mainloop()
