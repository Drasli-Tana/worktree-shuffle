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
            value=(
                os.getenv("HOMEDRIVE", "") +
                os.getenv("HOMEPATH", os.getenv("HOME", ""))
                ).replace(
                    "\\", "/"))
        
        TK.Label(self, text="Path").grid(row=0, column=0)
        TK.Entry(
            self, textvariable=self.path, width=80
            ).grid(row=0, column=1)
        
        
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
