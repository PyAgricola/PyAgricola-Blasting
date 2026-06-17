###############################################################
#                                                             #
#          MEs Eren K Kısa 2014                               #
#                  İstanbul University                        #
#                          Mining Engineering Dep.            #
#                                                             #
#                                                             #
###############################################################
#                                                             #
#                pyAgricola - Blasting Module                 #
#                                                 2014        #
###############################################################

# sistem = Metrik & Imperial
# dil = Türkçe
# Gnu Public License altında yayınlanmaktadır.

# -----------------------------------------------------------------
# Güncelleme Notu (2024):
#   - Hata düzeltmeleri: qtottoplamsarj, b_Zeigler, b_PearseArioglu,
#     b_Atlas mantık hatası, b_maxLangefors tanımsız patlayıcı
#   - Eklenen burden metodları: b_Esen, b_Jimeno, b_Ash
#   - Tamamlanan şarj modülü: hb_TabanSarji, hc_KolonSarji,
#     ho_Sikilama, qt_ToplamSarj, q_OzgulSarj
#   - Yeni sınıf: Fragmantasyon (KUZ-RAM modeli)
# -----------------------------------------------------------------


class Patlatma:
    def __init__(self, S=None):
        if S == None:
            self.hassasiyet = 2
        else:
            self.hassasiyet = S
        self.bolofson = 0
        self.blangefors = 0
        self.bvutukuri = 0
        self.bAtlas = 0
        self.bgustaffson = 0
        self.bkonya = 0
        self.bzeigler = 0
        self.bpearse = 0
        self.besen = 0
        self.bjimeno = 0
        self.bash = 0
        self.dipdelgi = 0
        self.H = 0
        self.etamrock = 0
        self.eolofson = 0
        self.elangefors = 0
        self.bburden = 0
        self.sdelikmesafe = 0
        self.hbtabansarjboyu = 0
        self.hosikilamaboyu = 0
        self.hckolonsarjboyu = 0
        self.qtottoplamsarj = 0      
        self.qozgulsarj = 0

#-------------------------------Burden Üzerine-----------------------------

    def bmax_Olofson(self, d, p, s, c, f, SB=1.25):
        '''
            d  = Delik Çapı (mm)
            p  = Şarj Yoğunluğu (g/cm³)
            s  = Delik İçi Şarj (katsayı)
            c  = Kaya Katsayısı
            f  = Delik Eğim Faktörü
            SB = Delik Aralığı / Delik Yükü Oranı (varsayılan 1.25)
        '''
        self.bolofson = ((d / 33) * (((p * s) / (c * s * SB)) ** (1 / 2)))
        return str(round(self.bolofson, self.hassasiyet))


    def b_maxLangefors(self, d, p, R1=0.95, Explosive='ANFO'):  # R2 default değeri gerekli
        '''
            d         = Delik Çapı (mm)
            p         = Patlayıcı yoğunluğu (g/cm³)
            R1        = Delik Düzeltme faktörü (varsayılan 0.95)
            Explosive = Patlayıcı tipi: 'ANFO' veya 'Emülite'
        '''
        
        if Explosive == 'ANFO':
            e = 1.36
        elif Explosive == 'Emülite':
            e = 1.45
        else:
            raise ValueError("Bilinmeyen patlayıcı tipi: " + str(Explosive) + " | Geçerli: 'ANFO', 'Emülite'")
        self.l = ((7.85) * (d * d) * (p))
        self.blangefors = ((e) * (self.l ** (0.5)) * (R1))
        return round(self.blangefors, 2)


    def b_VutukuriArioglu(self, d):
        '''
            d = Delik Çapı (mm)
        '''
        self.bvutukuri = ((0.024 * d) + 0.85)
        return round(self.bvutukuri, 2)


    def b_Atlas(self, d, Aralik=30):
        '''
            d      = Delik Çapı (inç)
            Aralik = Değer aralığı, tercihen değiştirilebilir (25-35)
        '''
        )
        if Aralik < 25 or Aralik > 35:
            print("Aralık Dışına Çıkılamaz")
        else:
            self.bAtlas = ((Aralik - (12 * d)))
            return str(round(self.bAtlas, self.hassasiyet)) + ' metre'


    def b_Gustaffson(self, d):
        '''
            d = Delik Çapı (mm)
        '''
        self.bgustaffson = 0.045 * d
        return round(self.bgustaffson, 2)


    def b_Konya(self, de, SGE, SGR):  # İnç üzerine çalış
        '''
            de  = Delik çapı (inç)
            SGE = Patlayıcı maddenin özgül ağırlığı
            SGR = Kayanın özgül ağırlığı
        '''
        self.bkonya = 3.15 * de * ((SGE / SGR) ** (0.33))
        return str(round(self.bkonya, self.hassasiyet)) + ' inch'


    def b_Zeigler(self, K, Ktp, SB, Qb, Qp):
        '''
            K   = Basamak yüksekliği (m)
            Ktp = Teknik Şarj Faktörü
            SB  = Delik Aralığı / Delik Yükü Oranı
            Qb  = Dip şarj miktarı (kg)
            Qp  = Kolon şarj miktarı (kg)
        '''
        self.bzeigler = ((Qb + Qp)) / (SB * K * Ktp)
        
        return str(round(self.bzeigler, self.hassasiyet)) + ' metre'


    def b_PearseArioglu(self, d, Kr, Pp, Sigma_c):
        '''
            d       = Delik çapı (mm)
            Kr      = Kaya faktörü
            Pp      = Delikteki patlama basıncı (MPa)
            Sigma_c = Kayanın çekme dayanımı (MPa)
        '''
        self.bpearse = d * Kr * ((Pp / Sigma_c) ** (0.5)) * ((10) ** (-3))
        return str(round(self.bpearse, self.hassasiyet))


    def b_Kou(self, Ko, micron, n, tan, d, SGE, Qe, Qer, Sigma_n, Ed):  # Formülasyon bilgisi yetersiz.
        pass


#-------------------------------Ek Burden Metodları-----------------------------

    def b_Esen(self, d, UCS, RQD, roR):
        '''
            Esen & Karpuz (1993) — RQD ve UCS tabanlı burden
            Süreksizlikli, sert kayalar için uygundur.
            d   = Delik çapı (mm)
            UCS = Tek eksenli basınç dayanımı (MPa)
            RQD = Kaya Kalite Göstergesi (0-100 arası, %)
            roR = Kayanın yoğunluğu (g/cm³)
        '''
        self.besen = 0.012 * ((2 * UCS * RQD / roR) ** 0.5) * d
        return str(round(self.besen, self.hassasiyet)) + ' metre'


    def b_Jimeno(self, d, KayaSinifi=2):
        '''
            Jimeno vd. (1995) — pratik ampirik burden
            d          = Delik çapı (mm)
            KayaSinifi = 1: Yumuşak (katsayı 40)
                         2: Orta    (katsayı 32, varsayılan)
                         3: Sert    (katsayı 25)
        '''
        if KayaSinifi == 1:
            Kj = 40
        elif KayaSinifi == 2:
            Kj = 32
        elif KayaSinifi == 3:
            Kj = 25
        else:
            raise ValueError("KayaSinifi 1, 2 veya 3 olmalıdır.")
        self.bjimeno = (Kj * d) / 1000
        return str(round(self.bjimeno, self.hassasiyet)) + ' metre'


    def b_Ash(self, d, Kd=1.0):
        '''
            Ash (1973) — oransal burden, açık ocak referans formülü
            d  = Delik çapı (mm)
            Kd = Kaya katsayısı (yumuşak: 1.5 / orta: 1.0 / sert: 0.75)
        '''
        self.bash = Kd * d / 1000
        return str(round(self.bash, self.hassasiyet)) + ' metre'


#-------------------------------Dip Delgi(dipdelgi)----------------------------------

    def U(self, Bmax=None):
        '''
            Bmax = Burden uzunluğu (m)
        '''
        if Bmax != None:
            self.dipdelgi = 0.3 * Bmax
            return round(self.dipdelgi, 2)
        else:
            pass


#-------------------------------Delik Derinliği-(H-boy)----------------------------

    def Delikderinligi(self, DipDelgi=None, BasamakYuksekligi=None):
        '''
            DipDelgi          = Dip delgi uzunluğu (m)
            BasamakYuksekligi = Basamak yüksekliği (m)
        '''
        self.H = 1.05 * (DipDelgi + BasamakYuksekligi)
        return round(self.H, 2)


#-------------------------------Delik Hata Payı(E-hata)----------------------------

    def e_Langefors(self, BasamakYuksekligi):
        '''
            BasamakYuksekligi = Basamak yüksekliği (m)
        '''
        self.elangefors = ((BasamakYuksekligi * 0.03) + (0.05))
        return round(self.elangefors, 2)


    def e_Tamrock(self, DelikUzunlugu):
        '''
            DelikUzunlugu = Delik uzunluğu (m)
        '''
        self.etamrock = ((DelikUzunlugu * 0.03) + (0.05))
        return round(self.etamrock, 2)


    def e_Olofson(self, d, DelikUzunlugu):
        '''
            d             = Delik çapı (mm)
            DelikUzunlugu = Delik uzunluğu (m)
        '''
        self.eolofson = ((d / 1000) + (0.03 * DelikUzunlugu))
        return round(self.eolofson, 2)


#------------------------------- Burden (Gerçek)-----------------------------------

    def b_burden(self, Bmax, hata):
        '''
            Bmax = Maksimum burden (m)
            hata = Delik hata payı (m)
        '''
        self.bburden = (Bmax) - (hata)
        return round(self.bburden, 2)


#-------------------------Delikler Arası Mesafe-(sdelikler)------------------------

    def s_Delik(self, burden, sb=1.25):
        '''
            burden = Gerçek burden (m)
            sb     = Delik aralığı / burden oranı (varsayılan 1.25)
        '''
        self.sdelikmesafe = (sb * burden)
        return round(self.sdelikmesafe, 2)


#----------------------------Şarj Hesapları----------------------------------------

    def hb_TabanSarji(self, d, roE, TabanSarjBoyu=None, Burden=None):
        '''
            Taban (dip) şarj boyu ve kütlesini hesaplar.
            d             = Delik çapı (mm)
            roE           = Patlayıcı yoğunluğu (g/cm³)
            TabanSarjBoyu = Taban şarj boyu verilmişse doğrudan kullanılır (m)
            Burden        = Burden verilmişse taban şarj boyu = 1.3 * Burden
        '''
        import math
        if TabanSarjBoyu != None:
            self.hbtabansarjboyu = TabanSarjBoyu
        elif Burden != None:
            self.hbtabansarjboyu = 1.3 * Burden
        else:
            print("TabanSarjBoyu veya Burden girilmelidir.")
            return None
        delikAlani = math.pi / 4 * ((d / 1000) ** 2)  # m²
        qTabanSarj = delikAlani * self.hbtabansarjboyu * roE * 1000  # kg
        return str(round(self.hbtabansarjboyu, self.hassasiyet)) + ' m | ' + \
               str(round(qTabanSarj, self.hassasiyet)) + ' kg'


    def ho_Sikilama(self, Burden=None, SikilamaBoyu=None):
        '''
            Sıkılama (stemming) boyunu hesaplar veya alır.
            Burden      = Burden verilmişse sıkılama boyu = 0.7 * Burden
            SikilamaBoyu= Sıkılama boyu doğrudan verilmişse kullanılır (m)
        '''
        if SikilamaBoyu != None:
            self.hosikilamaboyu = SikilamaBoyu
        elif Burden != None:
            self.hosikilamaboyu = 0.7 * Burden
        else:
            print("Burden veya SikilamaBoyu girilmelidir.")
            return None
        return str(round(self.hosikilamaboyu, self.hassasiyet)) + ' metre'


    def hc_KolonSarji(self, DelikDerinligi, TabanSarjBoyu, SikilamaBoyu):
        '''
            Kolon şarj boyunu hesaplar.
            DelikDerinligi = Toplam delik derinliği (m)
            TabanSarjBoyu  = Taban şarj boyu (m)
            SikilamaBoyu   = Sıkılama boyu (m)
        '''
        self.hckolonsarjboyu = DelikDerinligi - TabanSarjBoyu - SikilamaBoyu
        if self.hckolonsarjboyu < 0:
            print("Uyarı: Kolon şarj boyu negatif çıktı — delik geometrisini kontrol edin.")
        return str(round(self.hckolonsarjboyu, self.hassasiyet)) + ' metre'


    def qt_ToplamSarj(self, d, roE, TabanSarjBoyu, KolonSarjBoyu, roE_Kolon=None):
        '''
            Bir delik için toplam şarj kütlesini hesaplar.
            d             = Delik çapı (mm)
            roE           = Taban şarj patlayıcı yoğunluğu (g/cm³)
            TabanSarjBoyu = Taban şarj boyu (m)
            KolonSarjBoyu = Kolon şarj boyu (m)
            roE_Kolon     = Kolon şarjı farklı patlayıcı ise yoğunluğu (g/cm³)
                            Verilmezse taban ile aynı kabul edilir.
        '''
        import math
        if roE_Kolon == None:
            roE_Kolon = roE
        delikAlani = math.pi / 4 * ((d / 1000) ** 2)  # m²
        qTaban  = delikAlani * TabanSarjBoyu  * roE       * 1000  # kg
        qKolon  = delikAlani * KolonSarjBoyu  * roE_Kolon * 1000  # kg
        self.qtottoplamsarj = qTaban + qKolon
        return str(round(self.qtottoplamsarj, self.hassasiyet)) + ' kg'


    def q_OzgulSarj(self, ToplamSarj, Burden, Aralik, DelikDerinligi):
        '''
            Özgül şarj miktarını hesaplar (kg/m³).
            ToplamSarj    = Bir delik toplam şarjı (kg)
            Burden        = Burden (m)
            Aralik        = Delikler arası mesafe (m)
            DelikDerinligi= Delik derinliği (m)
        '''
        hacim = Burden * Aralik * DelikDerinligi  # m³
        self.qozgulsarj = ToplamSarj / hacim
        return str(round(self.qozgulsarj, self.hassasiyet)) + ' kg/m³'


#---------------------------------------------------------------------------------------
class Fragmantasyon:
    '''
        KUZ-RAM Modeli (Kuznetsov 1973 + Cunningham 1987)
        Patlatma sonrası ortalama parça boyutu (X50) ve
        Rosin-Rammler dağılım parametrelerini hesaplar.
    '''
    def __init__(self, S=None):
        if S == None:
            self.hassasiyet = 2
        else:
            self.hassasiyet = S
        self.X50 = 0
        self.n_tekduzelik = 0
        self.Xc = 0

#-------------------------------Kaya Faktörü (A)-----------------------------------

    def A_KayaFaktoru(self, KayaTipi=2):
        '''
            Kaya faktörü A — kaya sertliğine göre seçilir.
            KayaTipi = 1: Yumuşak / killi kaya        → A = 7
                       2: Orta sert kaya (varsayılan)  → A = 10
                       3: Sert, masif kaya             → A = 13
        '''
        if KayaTipi == 1:
            return 7
        elif KayaTipi == 2:
            return 10
        elif KayaTipi == 3:
            return 13
        else:
            raise ValueError("KayaTipi 1, 2 veya 3 olmalıdır.")

#-------------------------------Ortalama Parça Boyutu (X50)------------------------

    def X50_Kuznetsov(self, A, V0, Q, ANFO_Guc=100):
        '''
            Kuznetsov (1973) + enerji düzeltmesi
            A       = Kaya faktörü (A_KayaFaktoru() ile alınabilir)
            V0      = Delik başına düşen kaya hacmi (m³)
            Q       = Delik başına şarj kütlesi — ANFO eşdeğeri (kg)
            ANFO_Guc= Kullanılan patlayıcının göreli hacimsel gücü
                      ANFO = 100, Emülsiyon ≈ 115
        '''
        self.X50 = A * ((V0 / Q) ** 0.8) * (Q ** 0.167) * ((115 / ANFO_Guc) ** 0.633)
        return str(round(self.X50, self.hassasiyet)) + ' cm'

#-------------------------------Tekdüzelik Endeksi (n)-----------------------------

    def n_Cunningham(self, d, Burden, Aralik, DelikDerinligi, SikilamaBoyu, TabanSarjBoyu):
        '''
            Cunningham (1987) — Rosin-Rammler tekdüzelik endeksi
            d              = Delik çapı (mm)
            Burden         = Burden (m)
            Aralik         = Delikler arası mesafe (m)
            DelikDerinligi = Toplam delik derinliği (m)
            SikilamaBoyu   = Sıkılama boyu (m)
            TabanSarjBoyu  = Taban şarj boyu (m)
        '''
        d_m = d / 1000  # mm → m
        # Şarj boyu
        LsarjBoyu = DelikDerinligi - SikilamaBoyu
        # Tekdüzelik endeksi
        self.n_tekduzelik = (2.2 - (14 * (Burden / (d_m * 1000)))) * \
                            ((1 + (Aralik / Burden)) / 2) ** 0.5 * \
                            (1 - (SikilamaBoyu - TabanSarjBoyu) / LsarjBoyu)
        return round(self.n_tekduzelik, self.hassasiyet)

#-------------------------------Rosin-Rammler Karakteristik Boyut (Xc)-------------

    def Xc_KarakteristikBoy(self, X50, n):
        '''
            Rosin-Rammler eğrisinin karakteristik boyutu
            X50 = Ortalama parça boyutu (cm)
            n   = Tekdüzelik endeksi
        '''
        import math
        self.Xc = X50 / (math.log(2) ** (1 / n))
        return str(round(self.Xc, self.hassasiyet)) + ' cm'

#-------------------------------Geçen Yüzde (R-R Dağılımı)------------------------

    def RR_GecenYuzde(self, X, Xc, n):
        '''
            Rosin-Rammler: X boyutundan küçük malzeme yüzdesi
            X  = İstenen elek boyutu (cm)
            Xc = Karakteristik boy (cm)
            n  = Tekdüzelik endeksi
        '''
        import math
        R = 1 - math.exp(-((X / Xc) ** n))
        return str(round(R * 100, self.hassasiyet)) + ' %'


#---------------------------------------------------------------------------------------
class hesaplama:
    pass


if __name__ == "__main__":

    Blast = Patlatma()
    Frag  = Fragmantasyon()
