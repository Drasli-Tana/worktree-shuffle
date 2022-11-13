"""
The main file of this useless project

Mostly handles the graphical stuff
"""

import os

import json as JS
import random as RD
import tkinter as TK
import tkinter.filedialog as TF
import tkinter.messagebox as TM
import uuid as ID

class Main(TK.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.defaultPath = (os.getenv("HOMEDRIVE", "") +
                os.getenv("HOMEPATH", os.getenv("HOME", ""))
                ).replace("\\", "/") 
        self.path = TK.StringVar(self, value=self.defaultPath)
        self.resizable(False, False)
        
        self.newPath = TK.StringVar(self, value="")
        self.newName = TK.StringVar(self, value="")
        self.randomLength = TK.IntVar(self, value=1)
        self.randomRename = TK.BooleanVar(self, value=False)
        self.cursor = TK.IntVar(self, value=1)
        
        self.config = dict()
        self.description = TK.StringVar(self, value="")
        self.name = TK.StringVar(self, value="")
        
        
        self.newPath.trace_add("write", lambda *_: self.lockRandom())
        
        TK.Label(
            self, text="Path", font=("Courier New", 14)
            ).grid(row=0, column=0)
        TK.Entry(
            self, textvariable=self.path, width=80,
            font=("Courier New", 14)
            ).grid(row=0, column=1)
        
        TK.Button(
            self, text="Browse",font = ("Courier New", 14),
            command=lambda: self.changePath()
            ).grid(
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
            font=("Courier New", 14)
            ).grid(
            row=0, column=0, padx=5)
        
        self.newNamesFields = TK.Entry(
            temp, textvariable=self.newName, width=45, 
            font=("Courier New", 14))
        self.newNamesFields.grid(
            row=0, column=1, sticky="ew", padx=5)
        
        self.randomFields = TK.LabelFrame(self, text="Random")
        self.randomFields.grid(
            row=3, column=0, columnspan=3, padx=5,
            sticky="ew")
        
        TK.Label(
            self.randomFields, text="Tree level:", 
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
            font=("Courier New", 14), state="disabled"
            ).grid(
                row=0, column=2)
            
        TK.Checkbutton(
            self.randomFields, variable=self.randomRename,
            state="disabled"
            ).grid(row=0, column=3)
        
        temp2 = TK.Frame(self)
        temp2.grid(row=4, columnspan=3)
        
        TK.Label(
            temp2, text="Mode: ", font=("Courier New", 14), width=10
            ).grid(row=0, column=0)
        
        TK.Label(
            temp2, textvariable=self.name, font=("Courier New", 14),
            width=10
            ).grid(row=1, column=0)
        
        TK.Scale(
            temp2, variable=self.cursor, from_=1, to=5,
            orient=TK.HORIZONTAL, font=("Courier New", 14),
            sliderlength=10, length=150,
            command=lambda _:self.modeUpdate() 
            ).grid(
                row=0, column=1)
        
        TK.Label(
            temp2, textvariable=self.description, wraplength=60*14,
            width=75, font=("Courier New", 14), height=4
            ).grid(
            row=0, column=2, rowspan=2, padx=5)
        
        TK.Button(
            self, text="Let's go!", font=("Courier New", 14),
            bg="#FF0000", command=lambda: self.nuke()
            ).grid(
            row=5, column=0, columnspan=3, sticky="ew")
        
        self.loadConfig()
    
    def nuke(self):
        self.flattenOriginalTree(self.path.get())
        
        if self.cursor.get() == 1:
            # Simply move files at the end
            
            os.makedirs(
                os.path.join(
                    self.path.get(),
                    *self.newPath.get().split(" ")), 
                exists_ok=True)
            
            for file in os.listdir(self.path.get()):
                if self.isFile(file):
                    os.rename(
                        os.path.join(self.path.get(), file),
                        os.path.join(self.path.get(),
                                     *self.newPath.get().split(" "),
                                     file))
        
        elif self.cursor.get() >= 3:
            # The files should be renamed
            files = [
                file for file in os.listdir(self.path.get())
                if os.path.isfile(
                    os.path.join(self.path.get(), file))]
            extensions = dict() 
            for i in range(len(files)):
                file = files[i]
                fileSplitted = file.split(".")[-2:]
                
                if len(fileSplitted) == 2:
                    extensions[
                        fileSplitted[1]
                        if len(fileSplitted) == 2
                        else ""] = extensions.get(
                            fileSplitted[1]
                            if len(fileSplitted) == 2 
                            else "", 0) + os.path.getsize(
                            os.path.join(self.path.get(), file))/2
                         
                if self.newName.get() and self.cursor.get() < 5:
                    fileSplitted[0] = self.newName.get() + str(i)
                    
                elif (
                    self.randomRename.get() or
                    self.cursor.get() == 5):
                    fileSplitted[0] = str(ID.uuid4())
                    
                else:
                    fileSplitted = file.split(".")
                
                os.rename(
                    os.path.join(self.path.get(), file), 
                    os.path.join(self.path.get(), 
                                 ".".join(fileSplitted)))
            
            if self.cursor.get() >= 4:
                for i in range(RD.randrange(
                    50, 50 + 10 ** self.randomLength.get())):
                    filename = (
                        self.newName.get() + str(len(files))
                        if (self.newName.get() and
                            self.cursor.get() < 5) 
                        else str(ID.uuid4()))
                    
                    extension = RD.choice(list(extensions.keys()))
                    with open(
                        os.path.join(
                            self.path.get(),
                            filename + "." + extension),
                        mode="wb") as file:
                        file.write(os.urandom(
                            abs(RD.randint(-2000, 2000) +
                            int(extensions[extension]))))
        
        if self.cursor.get() < 5 and self.cursor.get() > 1:
            paths = ([
                os.path.join(
                    *[dirName
                      for dirName in self.newPath.get().split(" ")
                      if dirName])]
                if self.newPath.get().strip()
                else [str(ID.uuid4()) for _ in range(
                    self.randomLength.get())])
            os.makedirs(os.path.join(self.path.get(), *paths))
            
            for file in os.listdir(self.path.get()):
                pathList = ["."] + self.newPath.get().split(" ")
                level = RD.randrange(0, len(pathList))
                
                if self.isFile(file):
                    os.rename(
                        os.path.join(self.path.get(), file),
                        os.path.join(
                            self.path.get(),
                            *pathList[:level], file))
            
        elif self.cursor.get() == 5: 
            # Mode 5, répartition aléatoire
            self.subFolderTree(
                self.path.get(), self.randomLength.get())
            paths = self.folderLevel(
                self.path.get(),
                RD.randint(0, self.randomLength.get()))
            
            for file in os.listdir(self.path.get()):
                if self.isFile(file):
                    os.rename(
                        os.path.join(self.path.get(), file),
                        os.path.join(RD.choice(paths), file))
        
        TM.showinfo("Finished", "Operation successful")
        
    def isFile(self, *file):
        return os.path.isfile(os.path.join(
            self.path.get(), *file))
        
    def folderLevel(self, basePath, level):
        if level == 0:
            return [
                os.path.join(basePath, folder)
                for folder in os.listdir(basePath) 
                if not os.path.isfile(
                    os.path.join(basePath, folder))]
        
        else:
            paths = list()
            for folder in os.listdir(basePath):
                if not os.path.isfile(
                    os.path.join(basePath, folder)):
                    paths += self.folderLevel(
                        os.path.join(basePath, folder), level-1)
                    
            return paths
    
    def subFolderTree(self, basePath, level):
        if level > 0:
            for _ in range(10):
                folder = os.path.join(basePath, str(ID.uuid4()))
                os.makedirs(folder, exists_ok=True)
                self.subFolderTree(folder, level-1)
        
    def flattenOriginalTree(self, mainPath, path=""):
        try: 
            content = os.listdir(mainPath + "/" + path)
        
        except PermissionError:
            pass
        
        else:  
            for file in content:
                if os.path.isfile(
                    os.path.join(mainPath, path, file)):
                    os.rename(
                        os.path.join(mainPath, path, file),
                        os.path.join(mainPath, file))
                
                else:
                    self.flattenOriginalTree(
                        mainPath, os.path.join(path, file))
                    
                    try:
                        os.rmdir(os.path.join(mainPath, path, file))
                    
                    except PermissionError:
                        print("Permisison denied")
        
    def loadConfig(self):
        with open("config.json", mode="r") as file:
            self.config = JS.load(file).get("levels")
        self.modeUpdate()
        
    def lockRandom(self, hardcore=False):
        for children in self.randomFields.children:
            widget = self.randomFields.nametowidget(children)
            try:
                widget.config(
                    state=(
                        TK.DISABLED
                        if self.newPath.get().strip()
                        else TK.NORMAL))
            
            except AttributeError:
                continue
        
        if hardcore:
            for children in self.setFields.children:
                widget = self.setFields.nametowidget(children)
                try:
                    widget.config(state=TK.DISABLED)
            
                except TK.TclError:
                    for frameChildren in widget.children:
                        widget2 = widget.nametowidget(frameChildren)
                        try:
                            widget2.config(state=TK.DISABLED)
                        
                        except TK.TclError:
                            continue
        else:
            for children in self.setFields.children:
                widget = self.setFields.nametowidget(children)
                try:
                    widget.config(state=TK.NORMAL)
            
                except TK.TclError:
                    for frameChildren in widget.children:
                        widget2 = widget.nametowidget(frameChildren)
                        try:
                            widget2.config(state=TK.NORMAL)
                        
                        except TK.TclError:
                            continue
        
        self.randomFields.nametowidget("!checkbutton").config(
            state=(TK.DISABLED if self.cursor.get() < 3
                   else TK.NORMAL))
        self.randomFields.nametowidget("!label2").config(
                state=(TK.DISABLED if self.cursor.get() < 3
                       else TK.NORMAL))
    def modeUpdate(self):
        self.description.set(self.config.get(
            str(self.cursor.get())).get("description"))
        
        self.name.set(self.config.get(
            str(self.cursor.get())).get("name"))
        
        self.lockRandom(self.cursor.get() == 5)
    
    def changePath(self):
        path = TF.askdirectory()
        if path:
            self.path.set(path)
            
    
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
