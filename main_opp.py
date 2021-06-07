import tkinter as tk
from tkinter.filedialog import askopenfilename

class Application:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('luongvanquyen')
        self.root.geometry('1300x800')

        self.menubar = tk.Menu(self.root)
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label='open image', command=self.open_image)
        self.filemenu.add_command(label='save image', command=self.save_image)
        self.operate = tk.Menu(self.menubar, tearoff=0)
        self.operate.add_command(label='Histogram equalization', command=self.hst_eql)
        self.operate.add_command(label='edge detection', command=self.edge)
        self.menubar.add_cascade(label='file menu', menu=self.filemenu)
        self.menubar.add_cascade(label='operate', menu=self.operate)
        self.frm = tk.Frame(self.root)
        self.frm.pack()
        self.frm_left = tk.Frame(self.frm).pack(side='left')
        self.frm_right = tk.Frame(self.frm).pack(side='right')
        self.root.mainloop()

    def open_image(self):
        pass

    def save_image(self):
        pass

    def hst_eql(self):
        pass

    def edge(self):
        pass



if __name__ == '__main__':
    app = Application()