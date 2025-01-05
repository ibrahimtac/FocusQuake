import pandas as pd
from sqlalchemy import create_engine

class VeriTabani:
    def __init__(self, veritabani_url):
        """
        Veritabanı bağlantısını başlatan sınıf oluşturucu.
        :param veritabani_url: PostgreSQL veritabanı URL'si.
        """
        self.engine = create_engine(veritabani_url)

    def veriyi_getir(self, baslangic_yil, bitis_yil):
        """
        Veritabanından belirtilen yıllar arasındaki veriyi çeker.
        """
        query = f"SELECT * FROM deprem_verileri WHERE yil BETWEEN {baslangic_yil} AND {bitis_yil}"
        data = pd.read_sql(query, self.engine)
        return data
