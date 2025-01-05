import pandas as pd
from sqlalchemy import create_engine

# Bozuk karakterleri doğru Türkçe karakterlere çeviren bir fonksiyon
def temizle_turkce_karakterler(metin):
    if not isinstance(metin, str):
        return metin
    karakter_haritasi = {
        "Ã‡": "Ç", "Ã§": "ç",
        "Ã–": "Ö", "Ã¶": "ö",
        "Ãœ": "Ü", "Ã¼": "ü",
        "Ä°": "İ", "Ä±": "ı",
        "Åž": "Ş", "ÅŸ": "ş",
        "Äž": "Ğ", "ÄŸ": "ğ",
        "Ã‚": "Â", "Ã¢": "â"
    }
    for bozuk, dogru in karakter_haritasi.items():
        metin = metin.replace(bozuk, dogru)
    return metin

# Veritabanına bağlanma
engine = create_engine("postgresql+psycopg2://postgres:12345furkan@localhost:5432/FocusQuakeProject")

# Tabloyu pandas ile okuma
df = pd.read_sql("SELECT * FROM deprem_verileri", con=engine)

# Bozuk karakterlerin bulunduğu sütunda düzeltme (örnek: 'bolge' sütunu)
df['bolge'] = df['bolge'].apply(temizle_turkce_karakterler)

# Güncellenmiş veriyi tekrar veritabanına yazma
df.to_sql("deprem_verileri", con=engine, if_exists="replace", index=False)

print("Bozuk karakterler temizlenerek veritabanına kaydedildi.")
