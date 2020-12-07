#! /usr/bin/env python3

#
# Copyright (c) 2019-20 Dan Trickey.
# 
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
# 
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

from pathlib import Path
import re

status = True

print("Verifying minutes filenames.")

repo = Path(".")

filename_regex = re.compile("^20\d{2}-\d{2}-\d{2}-srawn-\d{2}\.md$")
folder_regex = re.compile("^SR20\d{2}$")

year_folders = [f for f in repo.iterdir() if f.is_dir()]

for folder in year_folders:
    result = re.match(folder_regex, folder.name)

    if result is not None:
        print(f"Found valid folder name: {folder.name}")

        for f in folder.iterdir():
           # Test if there are any nested folders

           if f.is_dir():
               print(f"\tFound nested directory: {folder.stem}/{f.stem}")
               status = False
       
           # Verify file name
       
           file_result =  re.match(filename_regex, f.name)

           if file_result is None:
               print(f"\tFound bad file name: {f.name}")
               status = False
           else:
               print(f"\tFound valid file name: {f.name}")

if status:
    print("All tests passed.")
else:
    print("Some tests failed.")
    exit(1)
