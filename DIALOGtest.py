import tkinter as tk

class ConfirmDeleteDialog(tk.Toplevel):
    def __init__(self, parent, on_confirm, del_button):
        super().__init__(parent)
        self.title("Confirm Deletion")
        self.transient(parent)
        self.grab_set()
        self.resizable(False, False)

        self.del_button = del_button
        self.on_confirm = on_confirm

        self.geometry("280x120")

        tk.Label(self, text="Are you sure you want to delete?").place(x=40, y=20)

        ok_btn = tk.Button(self, text="OK", width=10, command=self.ok)
        cancel_btn = tk.Button(self, text="Cancel", width=10, command=self.cancel)

        ok_btn.place(x=50, y=70)
        cancel_btn.place(x=150, y=70)

        cancel_btn.focus_set()

        self.bind("<Return>", lambda e: self.ok())
        self.bind("<Escape>", lambda e: self.cancel())
        self.protocol("WM_DELETE_WINDOW", self.cancel)

        self.wait_window()
    def ok(self):
        self.destroy()
        self.on_confirm()
        self.del_button.focus_set()

    def cancel(self):
        self.destroy()
        print("Deletion cancelled")
        self.del_button.focus_set()

def delete_action():
    print("Deletion confirmed!")  # Replace with your actual deletion logic

root = tk.Tk()
root.title("Delete Confirmation Demo")
root.geometry("300x150")

bDEL = tk.Button(root, text="DEL", width=10)
bDEL.place(x=110, y=50)

def on_del_pressed():
    ConfirmDeleteDialog(root, delete_action, bDEL)

bDEL.config(command=on_del_pressed)

root.mainloop()