import pandas as pd


class VeriAyarlama:
    def __init__(self, dosya_yolu):
        """
        Veriyi temizlemek ve düzenlemek için sınıf oluşturucu.
        :param dosya_yolu: CSV dosyasının yolu.
        """
        self.dosya_yolu = dosya_yolu
        self.data = None

    def veriyi_temizle(self):
        """
        Veriyi temizler ve gerekli sütunları ekleyerek hazırlar.
        """
        self.data = pd.read_csv(self.dosya_yolu)
        print("Veri başarıyla yüklendi.")

        self.data['Yil'] = pd.to_datetime(self.data['Olus tarihi']).dt.year
        print("'Yil' sütunu oluşturuldu.")

        self.data['Siddet'] = self.data['Mw'].combine_first(self.data['ML']).combine_first(self.data['Ms'])
        print("'Siddet' sütunu oluşturuldu.")

        self.data = self.data[['Yil', 'Yer', 'Siddet', 'Enlem', 'Boylam']].rename(columns={'Yer': 'bolge'})
        print("Gerekli sütunlar seçildi ve 'Yer' sütunu 'Bolge' olarak yeniden adlandırıldı.")

        # Eksik verileri içeren satırları kaldırır.
        self.data = self.data.dropna(subset=['yil', 'bolge', 'siddet', 'enlem', 'boylam'])
        print("Eksik veriler kaldırıldı.")

        return self.data

    def csv_olarak_kaydet(self, cikti_dosya_yolu):
        self.data.to_csv(cikti_dosya_yolu, index=False)
        print(f"Temizlenmiş veri '{cikti_dosya_yolu}' dosyasına kaydedildi.")
