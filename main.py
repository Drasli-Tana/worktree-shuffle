"""
The main file of this useless project

Mostly handles the graphical stuff
"""
try:
    import tkinter as TK
except ImportError:
    import Tkinter as TK

import os

class Main(TK.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.path = TK.StringVar(
            self,
            value=(
                os.getenv("HOMEDRIVE", "") +
                os.getenv("HOMEPATH", os.getenv("HOME", ""))
                ).replace(
                    "\\", "/"))
        
        self.newPath = TK.StringVar(self, value="")
        self.newName = TK.StringVar(self, value="")
        self.randomLength = TK.IntVar(self, value=1)
        self.randomRename = TK.BooleanVar(self, value=False)
        self.cursor = TK.IntVar(self, value=1)
        self.newPath.trace_add(
            "write", lambda *_: self.lockRandom())
        
        TK.Label(
            self, text="Path", font=("Courier New", 14)
            ).grid(row=0, column=0)
        TK.Entry(
            self, textvariable=self.path, width=80,
            font=("Courier New", 14)
            ).grid(row=0, column=1)
        
        TK.Button(
            self, text="Browse",font = ("Courier New", 14),
            command=lambda: print("Bouton!")).grid(
                row=0, column=2)
        
        self.setFields = TK.LabelFrame(self, text="Set")
        self.setFields.grid(
            row=2, column=0, columnspan=3, sticky="ew",
            padx=5)
        
        TK.Label(
            self.setFields, text=(
                "Input a sentence to crate a new path. " +
                "This will be cut on spaces, each word " + 
                "becoming a directory. Leave it blank " +
                "to enable the random fields."
                ), font=("Courier New", 14), wraplength=80*14
            ).grid(
                padx=5, row=0, column=0, sticky="ew")
            
        self.newPathField = TK.Entry(
            self.setFields, textvariable=self.newPath,
            font = ("Courier New", 14))
        self.newPathField.grid(
            row=1, column=0, sticky="ew", padx=5)
        
        temp = TK.Frame(self.setFields)
        temp.grid(row=2, column=0, sticky="ew", padx=5)
        TK.Label(
            temp, 
            text="New files name. Leave blank to keep existing ones.",
            font=("Courier New", 14)).grid(
            row=0, column=0, padx=5)
        
        self.newNamesFields = TK.Entry(
            temp, textvariable=self.newName,
            font=("Courier New", 14), width=45)
        self.newNamesFields.grid(
            row=0, column=1, sticky="ew", padx=5)
        
        self.randomFields = TK.LabelFrame(self, text="Random")
        self.randomFields.grid(
            row=3, column=0, columnspan=3, padx=5,
            sticky="ew")
        
        TK.Label(self.randomFields, text="Tree level:",
            font=("Courier New", 14)
            ).grid(
                row=0, column=0)
            
        TK.Spinbox(
            self.randomFields, textvariable=self.randomLength,
            from_=1, to=10
            ).grid(
                row=0, column=1)
            
        TK.Label(
            self.randomFields, text="Generate random file names?",
            font=("Courier New", 14)
            ).grid(
                row=0, column=2)
        TK.Checkbutton(
            self.randomFields, variable=self.randomRename
            ).grid(row=0, column=3)
        
        TK.Scale(
            self, variable=self.cursor, from_=1, to=5,
            orient=TK.HORIZONTAL, label="Mode:",
            font=("Courier New", 14), sliderlength=10,
            length=150
            ).grid(
                row=10, column=0, columnspan=3)
    
    def lockRandom(self, fulllock=False):
        for children in self.randomFields.children:
            widget = self.randomFields.nametowidget(children)
            try:
                widget.config(
                    state=(
                        "disabled" 
                        if self.newPath.get().strip() or fulllock
                        else "normal"))
            
            except AttributeError:
                continue
    
        
if __name__ == "__main__":
    Main().mainloop()

"""
Copyright (C) 2022 Thomas HAW

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
