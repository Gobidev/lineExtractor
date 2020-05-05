import tkinter as tk
from tkinter import filedialog
import threading


def get_lines_of_file(first_line, last_line, filename):
    target_file_lines = open(filename, "r").readlines()
    return target_file_lines[first_line-1:last_line]


def join_lines(lines):
    final_string = ""
    for line in lines:
        final_string += str(line)
    return final_string


def write_lines_to_file(filename, lines_str):
    target_file = open(filename, "w")
    target_file.write(lines_str)
    target_file.close()


def request_open_file_path():
    prev_path = read_path_file("in")
    file_path = filedialog.askopenfilename(initialdir=prev_path, title="Select Input File")
    return file_path


def request_save_file_path():
    prev_path = read_path_file("out")
    file_path = filedialog.asksaveasfilename(initialdir=prev_path, title="Select Output File")
    return file_path


def save_path_to_file(path, path_type):
    if path_type == "in":
        path_file = open(".path_in", "w")
    else:
        path_file = open(".path_out", "w")
    path_file.write(path)
    path_file.close()


def read_path_file(path_type):
    if path_type == "in":
        path_file = open(".path_in", "r")
    else:
        path_file = open(".path_out", "r")
    return path_file.read()


def refresh_in_path_lbl():
    global selected_in_path_lbl
    new_path = read_path_file("in")
    selected_in_path_lbl.config(text=new_path)


def refresh_out_path_lbl():
    global selected_out_path_lbl
    new_path = read_path_file("out")
    selected_out_path_lbl.config(text=new_path)


def set_status(status):
    global status_lbl
    status_lbl.config(text=status)


def open_in_button_press():
    path = request_open_file_path()
    if path != "":
        save_path_to_file(path, "in")
    refresh_in_path_lbl()


def open_out_button_press():
    path = request_save_file_path()
    if path != "":
        save_path_to_file(path, "out")
    refresh_out_path_lbl()


def run():
    set_status("Checking Inputs..")
    first_line = first_line_entry.get()
    last_line = last_line_entry.get()
    try:
        first_line = int(first_line)
        last_line = int(last_line)
    except ValueError:
        set_status("Invalid Input")
        return False

    set_status("Reading Input File..")
    lines = get_lines_of_file(first_line, last_line, read_path_file("in"))
    set_status("Joining Lines..")
    final_string = join_lines(lines)
    set_status("Writing to Output File..")
    write_lines_to_file(read_path_file("out"), final_string)
    set_status("Done!")


def run_button_press():
    threading.Thread(target=run).start()


if __name__ == '__main__':

    root = tk.Tk()
    root.title("lineExtractor")
    root.resizable(False, False)

    # Row 0
    open_in_file_lbl = tk.Label(root, text="Input File:")
    open_in_file_lbl.grid(row=0, column=0, padx=3, pady=3, sticky="w")

    open_in_file_button = tk.Button(root, text="Open", command=open_in_button_press)
    open_in_file_button.grid(row=0, column=1, padx=3, pady=3, sticky="w")

    selected_in_path_lbl = tk.Label(root, text="")
    selected_in_path_lbl.grid(row=0, column=3, padx=3, pady=3, sticky="e")

    try:
        refresh_in_path_lbl()
    except FileNotFoundError:
        save_path_to_file("/", "in")

    # Row 1
    line_range_label = tk.Label(root, text="Line Range:")
    line_range_label.grid(row=1, column=0, padx=3, pady=3, sticky="w")

    first_line_entry = tk.Entry(root)
    first_line_entry.grid(row=1, column=1, padx=3, pady=3, sticky="w")

    hyphen_lbl = tk.Label(root, text="-")
    hyphen_lbl.grid(row=1, column=2, padx=3, pady=3)

    last_line_entry = tk.Entry(root)
    last_line_entry.grid(row=1, column=3, padx=3, pady=3, sticky="w")

    # Row 2
    open_out_file_lbl = tk.Label(root, text="Output File:")
    open_out_file_lbl.grid(row=2, column=0, padx=3, pady=3, sticky="w")

    open_out_file_button = tk.Button(root, text="Open", command=open_out_button_press)
    open_out_file_button.grid(row=2, column=1, padx=3, pady=3, sticky="w")

    selected_out_path_lbl = tk.Label(root, text="")
    selected_out_path_lbl.grid(row=2, column=3, padx=3, pady=3, sticky="e")

    try:
        refresh_out_path_lbl()
    except FileNotFoundError:
        save_path_to_file("/", "out")

    # Row 3
    run_button = tk.Button(root, text="Run", command=run_button_press)
    run_button.grid(row=3, column=0, padx=3, pady=3, sticky="w")

    status_text_lbl = tk.Label(root, text="Status:")
    status_text_lbl.grid(row=3, column=2, padx=3, pady=3, sticky="w")

    status_lbl = tk.Label(root, text="")
    status_lbl.grid(row=3, column=3, padx=3, pady=3, sticky="w")

    root.mainloop()
