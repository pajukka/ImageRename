#PLEASE READ BELOW!

#THIS CODE IS INCOMPLETE AND HAS FAULTS.
#CODE IS FREE TO USE BUT NEEDS SOME FIXING
#I DO NOT GIVE SUPPORT

import os
from datetime import datetime
from tkinter import Tk, Button, Label, filedialog
from PIL import Image
from PIL.ExifTags import TAGS

def get_creation_date(path):
    try:
        image = Image.open(path)
        exif = image._getexif()
        if exif is not None:
            for tag, value in exif.items():
                tag_name = TAGS.get(tag, tag)
                if tag_name == 'DateTimeOriginal':
                    return datetime.strptime(value, "%Y:%m:%d %H:%M:%S")
                elif tag_name == 'CreateDate':
                    return datetime.strptime(value, "%Y:%m:%d %H:%M:%S")
    except (AttributeError, KeyError, IndexError, ValueError):
        pass
    return None

def rename_images_by_creation_date(directory):
    files = os.listdir(directory)
    total_files = len(files)
    progress_label.config(text=f"Progress: 0/{total_files}")
    
    for idx, filename in enumerate(files, 1):
        if filename.endswith(('.jpg', '.jpeg', '.png', '.gif')):
            file_path = os.path.join(directory, filename)
            creation_date = get_creation_date(file_path)
            if creation_date:
                new_name = creation_date.strftime("%Y-%m-%d_%H-%M-%S") + os.path.splitext(filename)[1]
                os.rename(file_path, os.path.join(directory, new_name))
                progress_label.config(text=f"Progress: {idx}/{total_files}")
                print(f"Renamed {filename} to {new_name}")
            else:
                file_modify_date = datetime.fromtimestamp(os.path.getmtime(file_path))
                new_name = file_modify_date.strftime("%Y-%m-%d_%H-%M-%S") + os.path.splitext(filename)[1]
                os.rename(file_path, os.path.join(directory, new_name))
                progress_label.config(text=f"Progress: {idx}/{total_files}")
                print(f"Renamed {filename} to {new_name}")
    progress_label.config(text=f"Progress: {total_files}/{total_files}")

def select_directory():
    directory = filedialog.askdirectory()
    if directory:
        directory_label.config(text=f"Selected Directory: {directory}")
        rename_images_by_creation_date(directory)

# Tkinter setup
root = Tk()
root.title("Image Renamer")

select_button = Button(root, text="Select Directory", command=select_directory)
select_button.pack(pady=10)

directory_label = Label(root, text="Selected Directory: None")
directory_label.pack()

progress_label = Label(root, text="Progress: 0/0")
progress_label.pack()

root.mainloop()
