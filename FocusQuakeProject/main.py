import tkinter as tk
from Arayuz import Arayuz


def main():
    # Ana pencereyi oluşturuyoruz
    root = tk.Tk()

    # Arayüzü başlatıyoruz
    arayuz = Arayuz(root)

    # Ana pencereyi sürekli açık tutuyoruz
    root.mainloop()


if __name__ == "__main__":
    main()
