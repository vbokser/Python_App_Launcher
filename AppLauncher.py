# App Launcher using tkinter
# Developer: Vitaly Bokser
# License: MIT License

import tkinter as tk
from tkinter import filedialog, Text
import os
import subprocess
from subprocess import Popen, PIPE
import SaveData as SD


class AppLauncher:
    def __init__(self):
        self.width = 600
        self.height = 500
        self.heightEntireFrame = 550

        self.data = SD.SaveData()
        self.apps_to_open = self.data.readData()
        print(f"apps to open = {self.apps_to_open}")

        self.root = tk.Tk()
        self.root.title("App Opener")
        self.root.resizable(width=False, height=False)
        self.canvas = tk.Canvas(
            self.root, width=self.width, height=self.heightEntireFrame, bg="#263d42")
        self.canvas.pack()

        self.frame = tk.Frame(self.root, bg="white")
        # self.frame.place(relwidth=0.95, relheight=.84, relx=0.025, rely=0.025)
        self.offset = 10
        self.frame.place(x=self.offset, y=self.offset, width=(self.width-(2*self.offset)),
                         height=(self.height - (2*self.offset)))

        self.listbox = tk.Listbox(self.frame)
        self.listbox.place(x=10, y=10, width=self.width -
                           (4*self.offset), height=(self.height-(4*self.offset)))

        self.addButtons()

        if len(self.apps_to_open) >= 1:
            # self.addTextToCanvas()
            self.addListBoxToCanvas()

    def __repr__(self):
        return f"Opener App"

    def openFileDialog(self):
        print("opening file dialog")
        filename = filedialog.askopenfilename(
            initialdir="~/Desktop/", title="Select File", filetypes=(("All Files", "*.*"), ("Executables", "*.exe")))
        # print(filename)

        if len(filename) > 1:
            self.apps_to_open.append([filename, "NOT_ADDED_YET"])
            # self.addTextToCanvas()
            self.addListBoxToCanvas()
            self.data.saveData(self.apps_to_open)

    def deleteSelectedListButtonPressed(self):
        if len(self.apps_to_open) == 0:
            return

        selected_item = self.listbox.get(tk.ANCHOR)
        # self.listbox.delete(ANCHOR)
        # index = self.apps_to_open.index(selected_item)
        # [self.apps_to_open.remove(index) for index, app in enumerate(
        #     self.apps_to_open) if app[0] == selected_item]

        # update data model
        for i, app in enumerate(self.apps_to_open):
            # print(f"{i} and {app[0]}")
            if app[0] == selected_item:
                print(f"we found selected item = {i}")
                del self.apps_to_open[i]

        # update UI
        self.listbox.delete(tk.ANCHOR)

        # print(f"apps to open = {self.apps_to_open}")
        # print(f"selected item to delete = {selected_item}")
        if len(self.apps_to_open) == 0:
            self.deleteSelectedListItemButton.pack_forget()

        self.data.saveData(self.apps_to_open)

    def runAppsNow(self):
        print("run apps now")
        for app_loc, _ in self.apps_to_open:
            # os.open(app_loc)
            # subprocess.call(
            #     ["/usr/bin/open", "-W", "-n", "-a", app_loc]
            # )

            process = Popen(['/usr/bin/open', app_loc],
                            stdout=PIPE, stderr=PIPE)
            # stdout, stderr = process.communicate()
            # print stdout  # import csv

    def addButtons(self):
        self.openFile = tk.Button(
            self.root, text="Open File", padx=5, pady=5, fg="#27ae60", bg="#2980b9", command=self.openFileDialog)
        # activebackground="red", background="blue"
        self.runAppsButton = tk.Button(
            self.root, text="Run Apps", padx=5, pady=5, bd='5', fg="#27ae60", bg="#2980b9", command=self.runAppsNow)
        # self.runAppsButton.pack()
        self.deleteSelectedListItemButton = tk.Button(
            self.root, text="Delete Selected Item", padx=5, pady=5, bd='5', fg="#27ae60", bg="#2980b9", command=self.deleteSelectedListButtonPressed)

        button_offset = 10
        self.openFile.place(x=button_offset, y=(self.height+button_offset))
        self.canvas.update()
        openFileWidth = self.openFile.winfo_width()
        runAppsButton_x = button_offset + openFileWidth + button_offset
        self.runAppsButton.place(
            x=runAppsButton_x, y=(self.height+button_offset))
        self.canvas.update()

        if len(self.apps_to_open) >= 1:
            # self.deleteSelectedListItemButton.pack()
            self.deleteSelectedListItemButton.place(
                x=(self.width-170), y=(self.height+button_offset), width=160)

    def addListBoxToCanvas(self):
        # listbox1 = tk.Listbox(self.root)
        self.listbox.delete(0, tk.END)
        for i, app in enumerate(self.apps_to_open):
            app_loc = app[0].strip("\n")
            self.listbox.insert(i, app_loc)
        # listbox1.place(x=10, y=10, width=100)
        if len(self.apps_to_open) == 1:
            self.deleteSelectedListItemButton.pack()

    def addTextToCanvas(self):
        start_x = 10
        start_y = 10
        label_height = 1
        for i, app in enumerate(self.apps_to_open):
            # and added yet? {added}
            app_location = app[0]
            app_added = app[1]
            print(
                f"index = {i} appname = {app_location} and added yet? {app_added}")
            if app_added == "NOT_ADDED_YET":
                self.apps_to_open[i][1] = "ADDED"
                text_to_output = f"{i}) {app_location}"
                label = tk.Label(self.frame, fg="black",
                                 text=text_to_output)

                label.place(x=start_x, y=(start_y + label_height*i))
                self.canvas.update()
                # get the actual label height after update only
                label_height = label.winfo_height()
                print(f"label_height = {label_height}")


if __name__ == "__main__":
    app = AppLauncher()
    print(app)
    app.root.mainloop()
