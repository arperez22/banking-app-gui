from tkinter import Tk
from bank import Bank

def main():
    window = Tk()
    window.title('Bank')
    window.geometry('400x400')
    window.resizable(False, False)

    Bank(window)

    window.mainloop()

if __name__ == '__main__':
    main()