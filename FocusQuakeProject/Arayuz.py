import tkinter as tk
from tkinter import messagebox
from tkinter import PhotoImage
from tkinter import font
from VeriTabani import VeriTabani
from VeriGörsellestirme import VeriGorsellestirme
import webbrowser
import os


class Arayuz:
    def __init__(self, root):
        self.root = root
        self.root.title("FocusQuake")  # Başlık
        self.root.geometry("800x1000")  # Pencere boyutu
        self.root.config(bg="#2E2E2E")  # Siyah gri arka plan rengi

        self.selected_year = 2023

        # Font yolları
        # Fontun tam dosya yolunu belirleyin
        self.title_font_path = os.path.abspath("BebasNeue-Regular.ttf")
        self.button_font_path = os.path.abspath("Poppins-Regular.ttf")

        # Fontları yükleyin
        self.title_font = font.Font(family="Bebas Neue", size=50)
        self.button_font = font.Font(family="Poppins", size=16)

        # Logo ekle ve küçült
        self.logo = PhotoImage(file="logo.png")  # Logo dosyasını ekle
        self.logo = self.logo.subsample(2)  # Logoyu 4 kat küçültüyoruz
        self.logo_label = tk.Label(self.root, image=self.logo, bg="#2E2E2E")
        self.logo_label.pack(pady=30)

        # Başlık kısmı
        self.title_label = tk.Label(self.root, text="FocusQuake", font=self.title_font,fg="white", bg="#2E2E2E")
        self.title_label.pack(pady=20)

        # VeriTabani ve VeriGorsellestirme sınıflarını başlatıyoruz
        self.veritabani = VeriTabani("postgresql+psycopg2://postgres:12345furkan@localhost:5432/FocusQuakeProject")
        self.gorsellestirme = VeriGorsellestirme()

        # Butonlar
        self.create_buttons()

        # İkon
        self.root.iconbitmap("logo.ico")

    def create_buttons(self):
        # Ortak buton ayarları olmadan eski haline döndürüldü
        # Başlat butonu
        self.start_button = tk.Button(
            self.root, text="Başlat", bg="#CD7F32", fg="#2E2E2E", font=self.button_font,
            command=self.show_second_panel, relief="flat", cursor="hand2"
        )
        self.start_button.pack(pady=15, fill='x', padx=80)
        self.add_hover_effect(self.start_button, "#D89A4E", "#CD7F32")

        # Ayarlar butonu
        self.settings_button = tk.Button(
            self.root, text="Ayarlar", bg="#CD7F32", fg="#2E2E2E", font=self.button_font,
            command=self.show_settings_panel, relief="flat", cursor="hand2"
        )
        self.settings_button.pack(pady=15, fill='x', padx=80)
        self.add_hover_effect(self.settings_button, "#D89A4E", "#CD7F32")

        # Hakkımızda butonu
        self.about_button = tk.Button(
            self.root, text="Hakkımızda", bg="#CD7F32", fg="#2E2E2E", font=self.button_font,
            command=self.about_click, relief="flat", cursor="hand2"
        )
        self.about_button.pack(pady=15, fill='x', padx=80)
        self.add_hover_effect(self.about_button, "#D89A4E", "#CD7F32")

        # Arayuz sınıfı içinde, show_second_panel fonksiyonunda
        self.improved_animated_heatmap_button = tk.Button(
            self.root, text="Geliştirilmiş Animasyonlu Harita", bg="#CD7F32", fg="#2E2E2E",
            font=("Poppins", 16),
            command=self.show_animated_heatmap, relief="flat", cursor="hand2"
        )
        self.improved_animated_heatmap_button.pack(pady=15, fill='x', padx=80)
        self.add_hover_effect(self.improved_animated_heatmap_button, "#D89A4E", "#CD7F32")

        # Çıkış butonu
        self.exit_button = tk.Button(
            self.root, text="Çıkış", bg="#E91E63", fg="#2E2E2E", font=self.button_font,
            command=self.exit_app, relief="flat", cursor="hand2"
        )
        self.exit_button.pack(pady=15, fill='x', padx=80)
        self.add_hover_effect(self.exit_button, "#C2185B", "#E91E63")

    def show_settings_panel(self):
        # Ayarlar penceresi oluştur
        self.settings_window = tk.Toplevel(self.root)
        self.settings_window.title("Ayarlar")
        self.settings_window.geometry("400x300")
        self.settings_window.config(bg="#2E2E2E")
        self.settings_window.iconbitmap("logo.ico")

        # Ayarlar başlığı
        settings_title = tk.Label(
            self.settings_window,
            text="Ayarlar",
            font=("Bebas Neue", 20),
            fg="#FFA500",
            bg="#2E2E2E"
        )
        settings_title.pack(pady=15)

        # Kullanıcıdan yıl girişi için açıklama
        info_label = tk.Label(
            self.settings_window,
            text="Bir yıl giriniz (1915 - 2023):",
            font=("Open Sans", 14),
            fg="#EDEDED",
            bg="#2E2E2E"
        )
        info_label.pack(pady=10)

        # Yıl giriş kutusu
        self.year_entry = tk.Entry(
            self.settings_window,
            font=("Poppins", 14),
            justify="center",
            bg="#3E3E3E",
            fg="#FFA500",
            insertbackground="#FFA500"  # İmleç rengini de uyumlu yapalım
        )
        self.year_entry.pack(pady=10, ipady=5, ipadx=10)

        # Kaydet butonu
        self.save_button = tk.Button(
            self.settings_window,
            text="Kaydet",
            bg="#CD7F32",
            fg="#2E2E2E",
            font=("Poppins", 14),
            command=self.save_year,
            relief="flat",
            cursor="hand2"
        )
        self.save_button.pack(pady=20, ipadx=20, ipady=15)
        self.add_hover_effect(self.save_button, "#D89A4E", "#CD7F32")

    def about_click(self):
        # Hakkımızda penceresi oluştur
        about_window = tk.Toplevel(self.root)
        about_window.title("Hakkımızda")
        about_window.geometry("600x520")
        about_window.config(bg="#2E2E2E")
        about_window.iconbitmap("logo.ico")

        # Proje hakkında başlık
        about_title = tk.Label(
            about_window,
            text="FocusQuake Hakkında",
            font=("Bebas Neue", 24),  # Daha modern bir font
            fg="#FFA500", bg="#2E2E2E"
        )
        about_title.pack(pady=20)

        # Proje açıklaması
        project_description = tk.Label(
            about_window,
            text=(
                "FocusQuake, Türkiye'deki 1915-2023 arasındaki depremleri görselleştirip kullanıcıya sunan bir projedir.\n\n"
                "Bu proje, Python kullanılarak geliştirilmiştir ve PostgreSQL, Tkinter, "
                "Matplotlib, Pandas gibi teknolojilerden faydalanmıştır."
            ),
            font=("Open Sans", 12),
            fg="#EDEDED", bg="#2E2E2E", wraplength=550, justify="left"
        )
        project_description.pack(pady=10)

        # Ekip bilgileri başlığı
        team_label = tk.Label(
            about_window,
            text="Projeyi Geliştirenler",
            font=("Bebas Neue", 19),
            fg="#FFA500", bg="#2E2E2E"
        )
        team_label.pack(pady=10)

        # Furkan Akdağ bilgileri
        furkan_frame = tk.Frame(about_window, bg="#2E2E2E")
        furkan_frame.pack(pady=5, anchor="w", padx=30)
        furkan_icon = PhotoImage(file="linkedin.png").subsample(10)
        furkan_icon_label = tk.Label(furkan_frame, image=furkan_icon, bg="#2E2E2E")
        furkan_icon_label.image = furkan_icon
        furkan_icon_label.pack(side="left", padx=10)
        furkan_info = tk.Label(
            furkan_frame,
            text="Furkan Akdağ -->",
            font=("Poppins", 14),
            fg="#FFA500", bg="#2E2E2E"
        )
        furkan_info.pack(side="left", padx=10)
        furkan_link = tk.Label(
            furkan_frame,
            text="linkedin.com/in/furkanakdag",
            font=("Poppins", 12, "underline"),
            fg="cyan", bg="#2E2E2E", cursor="hand2"
        )
        furkan_link.pack(side="left", padx=10)
        furkan_link.bind("<Button-1>", lambda e: self.open_url("https://www.linkedin.com/in/furkannakdag"))

        # İbrahim Taç bilgileri
        ibrahim_frame = tk.Frame(about_window, bg="#2E2E2E")
        ibrahim_frame.pack(pady=5, anchor="w", padx=30)
        ibrahim_icon = PhotoImage(file="linkedin.png").subsample(10)
        ibrahim_icon_label = tk.Label(ibrahim_frame, image=ibrahim_icon, bg="#2E2E2E")
        ibrahim_icon_label.image = ibrahim_icon
        ibrahim_icon_label.pack(side="left", padx=10)
        ibrahim_info = tk.Label(
            ibrahim_frame,
            text="İbrahim Taç -->",
            font=("Poppins", 14),
            fg="#FFA500", bg="#2E2E2E"
        )
        ibrahim_info.pack(side="left", padx=10)
        ibrahim_link = tk.Label(
            ibrahim_frame,
            text="linkedin.com/in/ibrahimtac",
            font=("Poppins", 12, "underline"),
            fg="cyan", bg="#2E2E2E", cursor="hand2"
        )
        ibrahim_link.pack(side="left", padx=10)
        ibrahim_link.bind("<Button-1>", lambda e: self.open_url("https://www.linkedin.com/in/ibrahim-taç-70470b294"))

        # Pencereyi kapatma butonu
        close_button = tk.Button(
            about_window,
            text="Kapat",
            bg="#FF0066", fg="#2E2E2E",
            cursor="hand2",
            relief="flat",
            font=self.button_font,
            command=about_window.destroy
        )
        close_button.pack(pady=15, fill='x', padx=50)
        self.add_hover_effect(close_button, "#C2185B", "#E91E63")

    def open_url(self, url):
        webbrowser.open_new(url)


    def save_year(self):
        # Kullanıcıdan alınan yıl değerini kontrol et ve kaydet
        try:
            year = int(self.year_entry.get())
            if 1915 <= year <= 2023:
                self.selected_year = year
                messagebox.showinfo("Başarılı", f"Yıl başarıyla {year} olarak ayarlandı!")
                self.settings_window.destroy()  # Ayarlar penceresini kapat
            else:
                messagebox.showerror("Hata", "Lütfen 1915 ile 2023 arasında bir yıl girin.")
        except ValueError:
            messagebox.showerror("Hata", "Lütfen geçerli bir yıl girin! (Sadece sayı).")

    def add_hover_effect(self, button, hover_color, default_color):
        # Hover efekti için işlev
        button.bind("<Enter>", lambda e: button.config(bg=hover_color))
        button.bind("<Leave>", lambda e: button.config(bg=default_color))

    def show_second_panel(self):
        # Ana paneli gizle
        self.hide_main_panel()

        # 2. panelin görselini ekle
        self.logo_second = PhotoImage(file="prize.png").subsample(3)
        self.logo_label_second = tk.Label(self.root, image=self.logo_second, bg="#2E2E2E")
        self.logo_label_second.pack(pady=20)


        # Harita Gösterimi Butonu
        self.map_button = tk.Button(
            self.root, text="  Harita Gösterimi", bg="#CD7F32", fg="#2E2E2E",
            font=("Poppins", 16), compound="left",
            command=self.show_map, relief="flat", cursor="hand2"
        )
        self.map_button.pack(pady=15, fill='x', padx=80)
        self.add_hover_effect(self.map_button, "#D89A4E", "#CD7F32")

        # Sütun Grafiği Butonu
        self.chart_button = tk.Button(
            self.root, text="  Sütun Grafiği", bg="#CD7F32", fg="#2E2E2E",
            font=("Poppins", 16),compound="left",
            command=self.show_bar_chart, relief="flat", cursor="hand2"
        )
        self.chart_button.pack(pady=15, fill='x', padx=80)
        self.add_hover_effect(self.chart_button, "#D89A4E", "#CD7F32")

        # Pasta Grafiği Butonu
        self.pie_chart_button = tk.Button(
            self.root, text="  Pasta Grafiği", bg="#CD7F32", fg="#2E2E2E",
            font=("Poppins", 16),compound="left",
            command=self.show_pie_chart, relief="flat", cursor="hand2"
        )
        self.pie_chart_button.pack(pady=15, fill='x', padx=80)
        self.add_hover_effect(self.pie_chart_button, "#D89A4E", "#CD7F32")

        # Isı Haritası Butonu
        self.heatmap_button = tk.Button(
            self.root, text="  Isı Haritası", bg="#CD7F32", fg="#2E2E2E",
            font=("Poppins", 16),compound="left",
            command=self.show_heatmap, relief="flat", cursor="hand2"
        )
        self.heatmap_button.pack(pady=15, fill='x', padx=80)
        self.add_hover_effect(self.heatmap_button, "#D89A4E", "#CD7F32")

        # Histogram Grafiği Butonu
        self.histogram_button = tk.Button(
            self.root, text="  Histogram Grafiği", bg="#CD7F32", fg="#2E2E2E",
            font=("Poppins", 16), compound="left",
            command=self.show_histogram_chart, relief="flat", cursor="hand2"
        )
        self.histogram_button.pack(pady=15, fill='x', padx=80)
        self.add_hover_effect(self.histogram_button, "#D89A4E", "#CD7F32")

        # Dağılım Grafiği Butonu
        self.scatter_button = tk.Button(
            self.root, text="  Dağılım Grafiği", bg="#CD7F32", fg="#2E2E2E",
            font=("Poppins", 16), compound="left",
            command=self.show_scatter_chart, relief="flat", cursor="hand2"
        )
        self.scatter_button.pack(pady=15, fill='x', padx=80)
        self.add_hover_effect(self.scatter_button, "#D89A4E", "#CD7F32")

        # Ağaç Grafiği Butonu
        self.treemap_button = tk.Button(
            self.root, text="  Ağaç Haritası", bg="#CD7F32", fg="#2E2E2E",
            font=("Poppins", 16), compound="left",
            command=self.show_treemap_chart, relief="flat", cursor="hand2"
        )
        self.treemap_button.pack(pady=15, fill='x', padx=80)
        self.add_hover_effect(self.treemap_button, "#D89A4E", "#CD7F32")

        # Geriye Dön Butonu
        self.back_button = tk.Button(
            self.root, text="  Geriye Dön", bg="#FF0066", fg="#2E2E2E",
            font=("Poppins", 16),compound="left",
            command=self.show_main_panel, relief="flat", cursor="hand2"
        )
        self.back_button.pack(pady=15, fill='x', padx=80)
        self.add_hover_effect(self.back_button, "#C2185B", "#FF0066")


    def hide_main_panel(self):
        # Birinci paneldeki öğeleri gizle
        self.logo_label.pack_forget()
        self.title_label.pack_forget()
        self.start_button.pack_forget()
        self.settings_button.pack_forget()
        self.about_button.pack_forget()
        self.exit_button.pack_forget()
        self.improved_animated_heatmap_button.pack_forget()

    def show_main_panel(self):
        # İkinci paneldeki öğeleri gizle
        self.logo_label_second.pack_forget()
        self.map_button.pack_forget()
        self.chart_button.pack_forget()
        self.back_button.pack_forget()
        self.pie_chart_button.pack_forget()
        self.heatmap_button.pack_forget()
        self.histogram_button.pack_forget()
        self.treemap_button.pack_forget()
        self.scatter_button.pack_forget()

        # Birinci paneldeki öğeleri tekrar göster
        self.logo_label.pack(pady=20)
        self.title_label.pack(pady=20)
        self.start_button.pack(pady=15, fill='x', padx=80)
        self.settings_button.pack(pady=15, fill='x', padx=80)
        self.about_button.pack(pady=15, fill='x', padx=80)
        self.improved_animated_heatmap_button.pack(pady=15, fill='x', padx=80)
        self.exit_button.pack(pady=15, fill='x', padx=80)


    def show_map(self):
        # Harita gösterimi için çağrı
        data = self.veritabani.veriyi_getir(self.selected_year, self.selected_year)
        self.gorsellestirme.turkiye_haritasi(data)

    def show_heatmap(self):
        """
        Isı haritasını oluşturur ve kaydeder.
        """
        try:
            # Veriyi al
            data = self.veritabani.veriyi_getir(self.selected_year, self.selected_year)

            # Isı haritası oluştur
            self.gorsellestirme.create_heatmap(data, "heatmap.html")

            # Haritayı varsayılan tarayıcıda aç
            import webbrowser
            webbrowser.open("heatmap.html")

        except Exception as e:
            messagebox.showerror("Hata", f"Isı haritası gösterilirken bir hata oluştu: {e}")

    def show_bar_chart(self):
        # Sütun grafiği için çağrı
        data = self.veritabani.veriyi_getir(self.selected_year, self.selected_year)
        self.gorsellestirme.sutun_grafik(data)

    def show_pie_chart(self):
        # Retrieve data and call the pie_chart function
        data = self.veritabani.veriyi_getir(self.selected_year, self.selected_year)  # Adjust year range as needed
        self.gorsellestirme.pie_chart(data)

    def show_histogram_chart(self):
        # Histogram grafiği için çağrı
        try:
            data = self.veritabani.veriyi_getir(self.selected_year, self.selected_year)
            self.gorsellestirme.histogram_deprem_siddeti(data)
        except Exception as e:
            messagebox.showerror("Hata", f"Histogram grafiği oluşturulurken bir hata meydana geldi: {e}")

    def show_scatter_chart(self):
        try:
            data = self.veritabani.veriyi_getir(self.selected_year, self.selected_year)
            self.gorsellestirme.create_3d_scatter(data)

        except Exception as e:
            messagebox.showerror("Hata", f"3D dağılım grafiği oluşturulurken bir hata meydana geldi: {e}")

    def show_treemap_chart(self):
        try:
            data = self.veritabani.veriyi_getir(self.selected_year, self.selected_year)
            self.gorsellestirme.create_treemap(data)
        except Exception as e:
            messagebox.showerror("Hata", f"Ağaç haritası grafiği oluşturulurken bir hata meydana geldi: {e}")

    def show_animated_heatmap(self):
        self.gorsellestirme.create_animated_heatmap(self.veritabani, 1915, 2023, "heatmap_with_time.html")
        import webbrowser
        webbrowser.open("heatmap_with_time.html")

    def settings_click(self):
        messagebox.showinfo("Ayarlar", "Ayarlar kısmı tıklandı!")

    def exit_app(self):
        self.root.quit()

# Ana uygulama
if __name__ == "__main__":
    root = tk.Tk()
    app = Arayuz(root)
    root.mainloop()