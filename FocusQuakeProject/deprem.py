class Deprem:
    def __init__(self, yil, bolge, siddet, enlem, boylam):
        """
        Deprem verilerini temsil eden sınıf.
        :param yil: Depremin meydana geldiği yıl.
        :param bolge: Depremin meydana geldiği bölge.
        :param siddet: Depremin şiddeti.
        :param enlem: Depremin enlemi.
        :param boylam: Depremin boylamı.
        """
        self.__yil = yil
        self.__bolge = bolge
        self.__siddet = siddet
        self.__enlem = enlem
        self.__boylam = boylam

    # Getter ve Setter metodları
    @property
    def yil(self):
        return self.__yil

    @yil.setter
    def yil(self, yil):
        self.__yil = yil

    @property
    def bolge(self):
        return self.__bolge

    @bolge.setter
    def bolge(self, bolge):
        self.__bolge = bolge

    @property
    def siddet(self):
        return self.__siddet

    @siddet.setter
    def siddet(self, siddet):
        self.__siddet = siddet

    @property
    def enlem(self):
        return self.__enlem

    @enlem.setter
    def enlem(self, enlem):
        self.__enlem = enlem

    @property
    def boylam(self):
        return self.__boylam

    @boylam.setter
    def boylam(self, boylam):
        self.__boylam = boylam

    def __str__(self):
        return f"Deprem: Yıl={self.__yil}, Bölge={self.__bolge}, Şiddet={self.__siddet}, Enlem={self.__enlem}, Boylam={self.__boylam}"
