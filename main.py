from Image_enc import ImageEncryptor
from database import Datas
import capture
import sys
from Face_detect.detect1 import FaceDetector
from tkinter import filedialog
import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog

class Main():
    def __init__(self):
        self.IE=ImageEncryptor()
        self.datas=Datas()
        self.detector=FaceDetector()
        
        self.menu=None
        self.name=None
        self.textbox=None
        self.entry=None
        self.n=None
        
        
    def Encrypt(self):
        file1 = filedialog.askopenfile(mode='r', filetypes=[('jpg file', '*.jpg')])
        file=self.IE.verify_image(file1)
        del file1
        if file:
            while True:
                messagebox.showwarning("Warning","Detecting Your Face")
                self.name=self.detector.face_detect()
                if self.name=="unknown":
                    while True:
                        self.show_textbox()
                        if not self.datas.search(self.name):
                            break
                        else:
                            messagebox.showwarning("Conflict","Entered username is already used. Try with different")
                    messagebox.showwarning("Warning","Capturing your face. Look at the camera")
                    capture.snip(self.name)
                    self.datas.insert(self.name)
                    break
                else:
                    result=messagebox.askyesno("Verification", "'Are you "+self.name+" ?")
                    if result:
                        break
                    else:
                        result=messagebox.askyesno("", "Do you want to try again?")
                        if result:
                            continue
                        else:
                            sys.exit(0)
            
            print('Encrypting...')
            key=int(self.datas.fetch(self.name))
            if self.IE._encrypt_file(file,key):
                messagebox.showinfo("Success","Encryption Success")
                sys.exit(0)
            else:
                messagebox.showerror("Error","An error occured")
                sys.exit(0)
        else:
            messagebox.showerror("Error", "Selected image is already Encrypted or Corrupted.")
            sys.exit(0)
    def Decrypt(self):
        file1 = filedialog.askopenfile(mode='r', filetypes=[('jpg file', '*.jpg')])
        file=self.IE.check_image(file1)
        del file1
        if file:
            while True:
                messagebox.showwarning("Warning","Detecting Your Face")
                self.name=self.detector.face_detect()
                if self.name!='unknown':
                    result=messagebox.askyesno("Verification", "'Are you "+self.name+" ?")
                    if result:
                        key=int(self.datas.fetch(self.name))
                        if self.IE._decrypt_file(file,key):
                            messagebox.showinfo("Success","Decryption Success")
                            sys.exit(0)
                        else:
                            messagebox.showerror("Error","Face doesn't match")
                            sys.exit(0)
                    else:
                        result=messagebox.askyesno("", "Do you want to try again?")
                        if result:
                            continue
                        else:
                            sys.exit(0)
                else:
                    messagebox.showerror("Error", "Can't Recognize your face!")
                    result=messagebox.askyesno("", "Do you want to try again?")
                    if result:
                        continue
                    else:
                        sys.exit(0)
        else:
            messagebox.showerror("Error", "Selected image is not encrypted.")
            sys.exit(0)
    
    def show_textbox(self):
        self.menu.withdraw()
        self.textbox=tk.Tk()
        self.textbox.geometry("250x125")
        #self.textbox=tk.Toplevel(self.menu)
        tk.Label(self.textbox,text="Enter your name:",height=1,width=15,bg="grey",fg="black").place(x=5,y=50)
        self.n=tk.Entry(self.textbox,width=15)
        self.n.place(x=150,y=50)
        
        self.button=tk.Button(self.textbox,text="Ok",command=self.get_text_and_destroy)
        self.button.place(x=75, y=80)
        #self.button.pack()
        self.textbox.wait_window()
        
    def get_text_and_destroy(self):
        self.name=self.n.get()
        self.textbox.destroy()
        self.menu.deiconify()
        

if __name__ == "__main__":
    m=Main()
    m.menu=tk.Tk()
    m.menu.geometry("250x125")
    m.menu.title("Image Encryption Decryption")
    m.menu.configure(bg='black')
    eb=tk.Button(m.menu,text="Encrypt",command=m.Encrypt)
    db=tk.Button(m.menu,text="Decrypt",command=m.Decrypt)
    eb.place(x=30,y=55)
    db.place(x=120,y=55)
    m.menu.mainloop()