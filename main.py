import os
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter.ttk import Progressbar, Style
from PIL import Image


def select_images():
    global selected_images
    selected_images = filedialog.askopenfilenames(
        filetypes=(("JPEG files", "*.jpg;*.jpeg"),
                   ("PNG files", "*.png"), ("All files", "*.*")))
    image_listbox.delete(0, END)
    for filename in selected_images:
        image_listbox.insert(END, filename)
    if selected_images:
        convert_button['state'] = 'normal'
    else:
        convert_button['state'] = 'disabled'
    download_button['state'] = 'disabled'


def convert_to_webp(filename):
    img = Image.open(filename)
    webp_filename = os.path.splitext(filename)[0] + ".webp"
    img.save(webp_filename, "WebP", lossless=True)


def convert_images():
    global converted_images
    converted_images = []
    progress_bar["maximum"] = len(selected_images)
    for i, filename in enumerate(selected_images, start=1):
        convert_to_webp(filename)
        progress_bar["value"] = i
        root.update_idletasks()
        converted_images.append(os.path.splitext(filename)[0] + ".webp")
    messagebox.showinfo("Success", "Conversion complete")
    download_button['state'] = 'normal'


def download_images():
    filetypes = (("WebP files", "*.webp"), ("All files", "*.*"))
    filename = filedialog.asksaveasfilename(
        title="Save Images", filetypes=filetypes)
    if filename:
        for image in converted_images:
            webp_filename = os.path.join(".", image)
            with open(webp_filename, "rb") as f:
                with open(filename, "ab") as out_file:
                    out_file.write(f.read())


selected_images = []
converted_images = []

root = Tk()
root.title("Image Converter")
root.geometry("400x400")

style = Style()
style.configure("TButton", font=("Helvetica", 12), padding=10)

select_button = Button(root, text="Select Images", command=select_images)
select_button.pack(padx=10, pady=10)

image_listbox = Listbox(root, selectmode=MULTIPLE, height=10)
image_listbox.pack(padx=10, pady=10)

convert_button = Button(root, text="Convert to WebP",
                        command=convert_images, state='disabled')
convert_button.pack(padx=10, pady=10)

progress_bar = Progressbar(root, orient=HORIZONTAL,
                           length=300, mode='determinate')
progress_bar.pack(padx=10, pady=10)

download_button = Button(root, text="Download WebP Images",
                         command=download_images, state='disabled')
download_button.pack(padx=10, pady=10)

root.mainloop()
