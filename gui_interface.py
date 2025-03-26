import tkinter as tk
from tkinter import messagebox
import subprocess
import os
from object_detection_audio import run_object_detection
from PIL import Image, ImageTk

class ObjectDetectionGUI:
    def __init__(self, master):
        self.master = master
        master.title("Object Detection GUI")
        master.geometry("500x400")

        # Load and set background image
        self.bg_image = Image.open("bg.jpg")  # Replace with your background image path
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        self.bg_label = tk.Label(master, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.create_widgets()

    def create_widgets(self):
        # Detect button
        self.detect_button = tk.Button(self.master, text="Detect", command=self.detect, height=2, width=20, bg='orange')
        self.detect_button.place(relx=0.5, rely=0.4, anchor='center')

        # Quit button
        self.quit_button = tk.Button(self.master, text="Quit", command=self.quit, height=2, width=20, bg='orange')
        self.quit_button.place(relx=0.5, rely=0.6, anchor='center')

    def detect(self):
        self.detect_button.config(state=tk.DISABLED)
        self.quit_button.config(state=tk.DISABLED)
        
        try:
            run_object_detection()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
        
        self.detect_button.config(state=tk.NORMAL)
        self.quit_button.config(state=tk.NORMAL)

        if os.path.exists('detected_objects.txt'):
            subprocess.Popen(['notepad.exe', 'detected_objects.txt'])
        else:
            messagebox.showinfo("Info", "No objects were detected.")

    def quit(self):
        self.master.quit()

if __name__ == "__main__":
    root = tk.Tk()
    gui = ObjectDetectionGUI(root)
    root.mainloop()

