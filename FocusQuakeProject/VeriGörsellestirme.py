import messagebox
import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt
import folium
from folium.plugins import HeatMap, HeatMapWithTime, MiniMap, MarkerCluster
import os

class TemelGorsellestirme:
    def __init__(self, data):
        self.data = data

    def veri_kontrol(self):
        if self.data.empty:
            raise ValueError("Veri seti boş!")
        print("Veri kontrolü başarılı.")

class Analiz:
    def analiz_yap(self, data):
        """
        Analiz yapmak için temel metod. Alt sınıflar bu metodu geçersiz kılmalıdır.
        :param data: Analiz yapılacak veri.
        """
        raise NotImplementedError("Bu metod alt sınıfta tanımlanmalıdır.")


class BolgeselAnaliz(Analiz):
    def analiz_yap(self, data):
        """
        Bölgesel analiz yapar.
        :param data: Pandas DataFrame, deprem verisi.
        """
        bolgeler = data['bolge'].value_counts().head(5)
        print("Bölgesel Analiz: En çok deprem olan 5 bölge")
        print(bolgeler)


class ZamanSerisiAnalizi(Analiz):
    def analiz_yap(self, data):
        """
        Zaman serisi analizi yapar.
        :param data: Pandas DataFrame, deprem verisi.
        """
        yillar = data.groupby('yil').size()
        print("Zaman Serisi Analizi: Yıllara göre deprem sayısı")
        print(yillar)

class VeriGorsellestirme:
    def __init__(self):
        pass

    def turkiye_haritasi(self, data):
        """
        Veriyi alıp Türkiye haritası üzerinde harita üzerinde açıklama ekler.
        :param data: Görselleştirilecek veri DataFrame'i.
        """
        try:
            # NaN değerleri temizleyelim
            data = data.dropna(subset=['enlem', 'boylam', 'siddet'])

            # Enlem ve Boylam'ı float türüne dönüştürelim
            data['enlem'] = pd.to_numeric(data['enlem'], errors='coerce')
            data['boylam'] = pd.to_numeric(data['boylam'], errors='coerce')

            # Büyüklüğe göre renk ayarlaması yap
            data['renk'] = data['siddet'].apply(lambda x: 'red' if x > 6 else ('yellow' if x >= 4 else 'green'))

            # Plotly ile Türkiye haritası üzerinden veri görselleştirme
            fig = px.scatter_geo(
                data,
                lat='enlem',
                lon='boylam',
                hover_name='bolge',
                size='siddet',
                color='renk',
                color_discrete_map={'red': 'red', 'yellow': 'yellow', 'green': 'green'},
                title='Türkiye Deprem Haritası',
                scope='asia',
                center={'lat': 39.0, 'lon': 35.0},
                projection='natural earth'
            )

            # Layout düzenlemesi ve açıklama ekleme
            fig.update_layout(
                geo=dict(
                    showland=True, landcolor='lightgray',
                    showcountries=True, countrycolor='black',
                    lakecolor='white'
                ),
                title=dict(
                    text="Türkiye Deprem Haritası",
                    font=dict(size=24, color="#2E2E2E"),
                    x=0.5
                ),
                margin={"r": 10, "t": 50, "l": 10, "b": 150},  # Alt tarafta daha fazla boşluk
            )

            # Açıklama metni
            description = (
                "Bu harita, Türkiye'de meydana gelen depremleri göstermektedir.<br>"
                "Renkler deprem şiddetine göre farklılık göstermektedir:<br>"
                "<span style='color:red'><b>Kırmızı</b></span>: Şiddeti 6'nın üstündeki depremler<br>"
                "<span style='color:yellow'><b>Sarı</b></span>: Şiddeti 4-6 arasındaki depremler<br>"
                "<span style='color:green'><b>Yeşil</b></span>: Şiddeti 4'ün altındaki depremler."
            )

            # Açıklama ekleyelim
            fig.add_annotation(
                xref='paper',
                yref='paper',
                x=0.5,
                y=-0.1,  # Haritanın altına yerleştirmek için negatif y değeri
                showarrow=False,
                text=description,
                font=dict(size=14, color="black"),
                align='center'
            )

            # Haritayı göster
            fig.show()

        except Exception as e:
            print(f"Harita oluşturulurken bir hata oluştu: {e}")

    def sutun_grafik(self, data):
        """
        Deprem verilerine göre en sık deprem olan 10 yeri sütun grafiği ile gösterir.
        :param data: Pandas DataFrame, deprem verileri
        """
        try:
            # En sık deprem olan 10 yeri bul
            en_cok_deprem = data['bolge'].value_counts().head(10)

            # Uzun bölge isimlerini kesiyoruz
            en_cok_deprem.index = [name if len(name) <= 20 else name[:17] + '...' for name in en_cok_deprem.index]

            # Sütun grafiği oluştur
            fig, ax = plt.subplots(figsize=(12, 8))

            # Renk paleti
            colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22',
                      '#17becf']
            en_cok_deprem.plot(kind='bar', color=colors, ax=ax, edgecolor='black', alpha=0.9)

            # Başlık ve eksen etiketleri
            ax.set_title("En Sık Deprem Olan 10 Yer", fontsize=20, fontweight='bold', color='#1d3557', pad=20)
            ax.set_xlabel("Yer", fontsize=16, fontweight='bold', color='#457b9d', labelpad=10)
            ax.set_ylabel("Deprem Sayısı", fontsize=16, fontweight='bold', color='#457b9d', labelpad=10)

            # Eksen yazı tipleri ve renkleri
            ax.tick_params(axis='x', labelsize=12, labelrotation=45, labelcolor='#1d3557')
            ax.tick_params(axis='y', labelsize=12, labelcolor='#1d3557')

            # Izgara ayarları
            ax.grid(axis='y', linestyle='--', linewidth=0.5, alpha=0.7, color='#a8dadc')
            ax.set_axisbelow(True)

            # Açıklama metni
            explanation = (
                "Bu grafik, en çok depremin yaşandığı ve Türkiye'yi etkileyen 10 bölgeyi göstermektedir.\n"
                "Y ekseni, deprem sayısını temsil ederken X ekseni, bölgeleri temsil eder."
            )
            fig.text(
                0.5, 0.01, explanation, wrap=True, horizontalalignment='center',
                fontsize=12, color='#1d3557', fontweight='bold'
            )

            # Grafik arka planı
            ax.set_facecolor('#f1faee')
            fig.patch.set_facecolor('#f1faee')

            # Çerçeve çizgileri
            for spine in ax.spines.values():
                spine.set_edgecolor('#1d3557')
                spine.set_linewidth(1.2)

            # Sıkı yerleşim
            plt.tight_layout()

            # Grafiği göster
            plt.show()

        except Exception as e:
            print(f"Grafik oluşturulurken bir hata oluştu: {e}")

    def pie_chart(self, data):
        """
        Creates a pie chart showing the distribution of earthquakes by region.
        """
        try:
            # Group by region and calculate counts
            region_counts = data['bolge'].value_counts().head(5)

            # Create the pie chart
            fig, ax = plt.subplots(figsize=(8, 8))
            region_counts.plot.pie(
                autopct='%1.1f%%',
                startangle=90,
                colors=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd'],
                textprops={'color': 'black', 'fontsize': 12},
                ax=ax
            )

            # Başlık
            ax.set_title(
                "Deprem Bölge Dağılımı",
                fontsize=18,
                fontweight="bold",
                color="#1d3557",
                pad=20
            )

            # X ve Y ekseni etiketlerini kaldır
            ax.set_ylabel('')
            ax.set_xlabel('')

            # Açıklama metni (grafik altına yerleştirme)
            explanation = (
                "Bu grafik, Türkiye'de seçilen yıla göre en çok deprem yaşanan 5 bölgenin yüzdesel dağılımını göstermektedir.\n"
                "Her bir dilim, bölgedeki toplam deprem oranını temsil eder."
            )
            fig.text(
                0.5, 0.01, explanation, wrap=True, horizontalalignment='center',
                fontsize=12, color='#1d3557', fontweight='bold'
            )

            # Arka plan rengi
            ax.set_facecolor('#f1faee')
            fig.patch.set_facecolor('#f1faee')

            # Çerçeve çizgileri
            for spine in ax.spines.values():
                spine.set_edgecolor('#1d3557')
                spine.set_linewidth(1.2)

            # Layout düzenlemesi
            plt.tight_layout(rect=[0, 0.05, 1, 1])  # Alt metin için boşluk bırakıldı

            # Grafiği göster
            plt.show()

        except Exception as e:
            print(f"Pasta grafiği oluşturulurken bir hata oluştu: {e}")

    from tkinter import messagebox

    def create_heatmap(self, data, file_name="heatmap.html"):
        """
        Veriyi alıp Türkiye haritası üzerinde ısı haritası oluşturur ve HTML olarak kaydeder.
        """

        try:
            # NaN değerleri temizleyelim
            data = data.dropna(subset=['enlem', 'boylam', 'siddet'])

            # Harita oluştur
            m = folium.Map(location=[39.0, 35.0], zoom_start=6)

            # Isı haritası katmanı ekle
            heat_data = [[row['enlem'], row['boylam'], row['siddet']] for index, row in data.iterrows()]
            HeatMap(heat_data).add_to(m)

            # Haritayı UTF-8 kodlamasıyla kaydet
            with open(file_name, "w", encoding="utf-8") as f:
                f.write(m.get_root().render())
            print(f"Isı haritası {file_name} olarak kaydedildi.")

            # Açıklama mesajı
            messagebox.showinfo(
                "Isı Haritası Açıklaması",
                "Bu ısı haritası, Türkiye'deki seçilen yılın depremlerini gösterir. Yoğun bölgeler daha sıcak renklerle temsil edilir.\n"
                "HTML dosyası olarak kaydedildi ve tarayıcıda görüntülenebilir."
            )

        except Exception as e:
            messagebox.showerror("Hata", f"Isı haritası oluşturulurken bir hata meydana geldi: {e}")

    def histogram_deprem_siddeti(self, data):
        """
        Deprem şiddeti dağılımını histogram olarak görselleştirir.
        :param data: Görselleştirilecek veri DataFrame'i.
        """
        try:
            # Histogram oluştur
            fig, ax = plt.subplots(figsize=(12, 6))
            ax.hist(data['siddet'], bins=10, color='#69b3a2', edgecolor='#1d3557', alpha=0.9)

            # Başlık ve etiketler
            ax.set_title("Deprem Şiddeti Dağılımı", fontsize=20, fontweight='bold', color='#1d3557', pad=20)
            ax.set_xlabel("Deprem Şiddeti", fontsize=16, fontweight='bold', color='#457b9d')
            ax.set_ylabel("Frekans (Deprem Sayısı)", fontsize=16, fontweight='bold', color='#457b9d')

            # X ve Y ekseni yazı boyutu ve renkleri
            ax.tick_params(axis='x', labelsize=12, labelcolor='#1d3557')
            ax.tick_params(axis='y', labelsize=12, labelcolor='#1d3557')

            # Izgara ayarları
            ax.grid(axis='y', linestyle='--', linewidth=0.7, alpha=0.5, color='#a8dadc')
            ax.set_axisbelow(True)  # Izgarayı çubukların arkasına koyar

            # Açıklama metni
            explanation = (
                "Bu histogram, seçilen yıl içinde Türkiye'de gerçekleşen depremlerin şiddet dağılımını göstermektedir.\n"
                "Her bir çubuk, belirli bir şiddet aralığındaki deprem sayısını temsil eder."
            )
            fig.text(
                0.5, 0.02, explanation, wrap=True, horizontalalignment='center',
                fontsize=12, color='#1d3557', fontweight='bold'
            )

            # Grafik arka planını ayarla
            ax.set_facecolor('#f1faee')
            fig.patch.set_facecolor('#f1faee')

            # Çerçeve renklerini ve çizgilerini düzenle
            for spine in ax.spines.values():
                spine.set_edgecolor('#1d3557')
                spine.set_linewidth(1.2)

            # Görselleştirmeyi sıkıştır
            plt.tight_layout(rect=[0, 0.05, 1, 1])  # Alt tarafta açıklama için yer bırak

            # Histogramı göster
            plt.show()
        except Exception as e:
            print(f"Histogram oluşturulurken bir hata oluştu: {e}")

    def create_3d_scatter(self, data):
        """
        4 ve üzeri büyüklükteki depremleri gösteren 3D scatter plot oluşturur.
        En büyük depremler kırmızı renkle vurgulanır.
        :param data: Pandas DataFrame, deprem verisi
        """
        try:
            import plotly.express as px

            # 4 ve üzeri büyüklükteki depremleri filtrele
            filtered_data = data[data['siddet'] >= 4.0]

            # Renk skalasını ayarla (küçükler mavi, büyükler kırmızı)
            color_scale = [
                [0, "blue"],  # Minimum büyüklük: mavi
                [0.5, "orange"],  # Orta büyüklük: turuncu
                [1, "red"]  # Maksimum büyüklük: kırmızı
            ]

            # 3D Scatter Plot oluştur
            fig = px.scatter_3d(
                filtered_data,
                x='boylam',  # X ekseni: Longitude
                y='enlem',  # Y ekseni: Latitude
                z='siddet',  # Z ekseni: Deprem büyüklüğü
                color='siddet',  # Renk: Deprem büyüklüğüne göre
                size='siddet',  # Boyut: Deprem büyüklüğüne göre
                hover_name='bolge',  # Bölge bilgisi hover ile gösterilecek
                title='3D Deprem Haritası (4 ve Üzeri Depremler)',
                color_continuous_scale=color_scale  # Özel renk skalası
            )

            # Eksen isimlerini düzenle
            fig.update_layout(
                scene=dict(
                    xaxis_title='Boylam',
                    yaxis_title='Enlem',
                    zaxis_title='Büyüklük'  # Deprem büyüklüğü
                ),
                title=dict(font=dict(size=20)),
                margin=dict(t=50, l=250, r=10, b=10)  # Sol tarafa yer açıldı
            )

            # Açıklama metni
            description = ("a"

            )

            # Açıklamayı sol tarafa yerleştirme
            fig.add_annotation(
                xref="paper",
                yref="paper",
                x=-0.3,  # Grafiğin sol tarafına konumlandırıldı
                y=0.5,
                showarrow=False,
                text=description,
                font=dict(size=12, color="black"),
                align="left",
                xanchor="left",
                yanchor="middle"
            )

            # Grafik göster
            fig.show()
        except Exception as e:
            print(f"3D scatter plot oluşturulurken bir hata meydana geldi: {e}")

    def create_treemap(self, data):
        try:
            grouped_data = data['bolge'].value_counts().reset_index()
            grouped_data.columns = ['bolge', 'deprem_sayisi']

            # İlk 10 veriyi seç
            grouped_data = grouped_data.head(10)

            fig = px.treemap(
                grouped_data,
                path=['bolge'],
                values='deprem_sayisi',
                color='deprem_sayisi',
                color_continuous_scale='Viridis',
                title='Bölgelerdeki İlk 10 Deprem Sayısı (Treemap)'
            )

            fig.update_traces(
                textinfo="label+value",
                textfont_size=14
            )

            # Layout düzenlemesi
            fig.update_layout(
                title=dict(
                    text='Bölgelerdeki İlk 10 Deprem Sayısı (Treemap)',
                    font=dict(size=24, color='#2E2E2E'),
                    x=0.5
                ),
                margin=dict(t=50, l=10, r=10, b=120),  # Alt tarafta boşluk artırıldı
                coloraxis_colorbar=dict(
                    title="Deprem Sayısı",
                    thicknessmode="pixels",
                    thickness=15,
                    lenmode="pixels",
                    len=300,
                    yanchor="top",
                    y=1,
                    ticks="outside"
                )
            )

            # Açıklama metni
            explanation = (
                "Bu Treemap grafiği, Türkiye'de seçilen yıl içinde en fazla deprem yaşanan 10 bölgeyi göstermektedir. "
                "Her bölgenin alanı, o bölgede gerçekleşen deprem sayısını temsil eder. "
                "Renkler, deprem sayısına göre değişmektedir; daha koyu renkler daha fazla deprem sayısını işaret eder."
            )

            # Açıklama ekle
            fig.add_annotation(
                xref="paper",
                yref="paper",
                x=0.5,
                y=-0.15,  # Açıklama daha aşağıda olacak
                showarrow=False,
                text=explanation,
                font=dict(size=14, color="black"),
                align="center"
            )

            fig.show()
        except Exception as e:
            print(f"Treemap grafiği oluşturulurken bir hata meydana geldi: {e}")

    def create_animated_heatmap(self, veritabani, start_year=1915, end_year=2023, file_name="heatmap_with_time.html"):
        # Harita oluşturma (Görsel iyileştirme: CartoDB Positron stili)
        m = folium.Map(location=[39.0, 35.0], zoom_start=6, tiles='CartoDB Positron')

        all_data = []
        years = list(range(start_year, end_year + 1))

        # Yıllara göre veriyi çekip all_data listesine ekliyoruz
        for year in years:
            data = veritabani.veriyi_getir(year, year)
            data = data.dropna(subset=['enlem', 'boylam', 'siddet'])

            # Performans iyileştirme: Çok büyük veri varsa örnekleme (sampling)
            if len(data) > 1000:
                data = data.sample(1000, random_state=42)

            points = data[['enlem', 'boylam', 'siddet']].values.tolist()
            all_data.append(points)

        # Zaman serili ısı haritası ekleme
        HeatMapWithTime(
            data=all_data,
            index=years,
            name='Zaman Serili Isı Haritası',
            radius=20,  # Noktaların büyüklüğü
            max_opacity=0.8
        ).add_to(m)

        # MiniMap eklenmesi (Etkileşimli Özellik)
        minimap = MiniMap(toggle_display=True)
        minimap.add_to(m)

        # En büyük 5 depremi MarkerCluster kullanarak gösterme
        full_data = veritabani.veriyi_getir(start_year, end_year)
        full_data = full_data.dropna(subset=['enlem', 'boylam', 'siddet'])
        largest_quakes = full_data.nlargest(5, 'siddet')

        marker_cluster = MarkerCluster(name="En Büyük 5 Deprem").add_to(m)

        for idx, row in largest_quakes.iterrows():
            folium.Marker(
                location=[row['enlem'], row['boylam']],
                popup=f"Yer: {row['bolge']}\nŞiddet: {row['siddet']}\nYıl: {row['yil']}",
                icon=folium.Icon(color='red', icon='info-sign')
            ).add_to(marker_cluster)

        # LayerControl ekleme (Farklı katmanları yönetmek için)
        folium.LayerControl().add_to(m)

        # Haritayı kaydet
        m.save(file_name)
        print(f"{file_name} dosyası oluşturuldu ve harita kaydedildi.")
