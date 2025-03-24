from tkinter import ttk, Tk, StringVar, PhotoImage, messagebox, IntVar
import os

def validate_input(action, value_if_allowed):
    if action == "1":
        if value_if_allowed.isdigit():
            if int(value_if_allowed) <= 315360000:
                return True
            else:
                return False
        else:
            return False
    else:
        return True

main = Tk()
main.title("Shutdown PC")
main.iconphoto(False, PhotoImage(file="_internal\\icon.png"))
main.geometry("240x110")
vcmd = main.register(validate_input)

label = ttk.Label(main, text="What do you want the computer to do?")
label.place(x=0, y=0)

action_value = StringVar()
action = ttk.OptionMenu(main, action_value, "Sign out", "Sign out", "Shut down", "Restart", "Hibernate")
action.place(x=0, y=22)

time_label_a = ttk.Label(main, text="in")
time_label_a.place(x=90, y=22)
time_box = ttk.Entry(main, validate="key", validatecommand=(vcmd, '%d', '%P'), width=9)
time_box.place(x=105, y=22)
time_label_b = ttk.Label(main, text="seconds")
time_label_b.place(x=165, y=22)

RE_checkbox_value = IntVar()
RE_checkbox = ttk.Checkbutton(main, text="Restart into WinRE", variable=RE_checkbox_value)
RE_checkbox.place(x=0, y=44)

BIOS_checkbox_value = IntVar()
BIOS_checkbox = ttk.Checkbutton(main, text="Restart into BIOS", variable=BIOS_checkbox_value)
BIOS_checkbox.place(x=123, y=44)

comment_label = ttk.Label(main, text="Comment:")
comment_label.place(x=0, y=66)

comment = ttk.Entry(main)
comment.place(x=60, y=66)

def shutdown():
    confirmation = messagebox.askyesno("Confirmation", "Are you sure?")
    if confirmation:
        match action_value.get():
            case "Sign out":
                main_switch = "/l"
            case "Shut down":
                main_switch = "/s"
            case "Restart":
                main_switch = "/r"
            case "Hibernate":
                main_switch = "/h"
        if RE_checkbox_value.get() and action_value.get() == "Restart":
            extra_switch = "/o"
        elif BIOS_checkbox_value.get() and action_value.get() == "Restart":
            extra_switch = "/fw"
        elif BIOS_checkbox_value.get() and action_value.get() == "Shut down":
            extra_switch = "/fw"
        else:
            extra_switch = None
        if RE_checkbox_value.get() and action_value.get() != "Restart":
            messagebox.showerror("Error", "Restart into WinRE only works with restarts.\nShutdown+ will ignore the checkbox.")
        elif BIOS_checkbox_value.get() and ["Restart", "Shut down"].count(action_value.get()) == 0:
            messagebox.showerror("Error", "Restart to BIOS only works with restarts and shutdowns.\nShutdown+ will ignore the checkbox.")
        time = f"/t {time_box.get() or 0}"
        if comment.get() != "":
            comment_command = f"/c \"{comment.get()}\""
        else:
            comment_command = None
        if extra_switch == None and comment_command == None:
            command = f"shutdown {main_switch} {time}"
        elif comment_command == None:
            command = f"shutdown {main_switch} {extra_switch} {time}"
        elif extra_switch == None:
            command = f"shutdown {main_switch} {comment_command} {time}"
        else:
            command = f"shutdown {main_switch} {extra_switch} {comment_command} {time}"
        os.system(command)
OK_button = ttk.Button(main, text="OK", command=shutdown)
OK_button.place(x=0, y=88)

def abort_shutdowns():
    os.system("shutdown /a")
abort_button = ttk.Button(main, text="Abort all current shutdowns", command=abort_shutdowns)
abort_button.place(x=80, y=88)

main.mainloop()