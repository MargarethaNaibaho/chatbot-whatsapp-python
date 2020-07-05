def dataIndonesia():
    from bs4 import BeautifulSoup
    import requests
    source = requests.get('https://www.kompas.com/covid-19')
    soup = BeautifulSoup(source.text, 'html5lib')

    data = soup.find_all('div', {'class':'covid__box2'})

    positif = data[0].text.split('i')[2].split(' ')[0]
    tambahan = data[0].i.text
    dirawat = data[1].text.split('t')[1].split(' ')[0]
    meninggal = data[2].text.split('l')[1].split(' ')[0]
    sembuh = data[3].text.split('h')[1].split(' ')[0]

    tgl_Update = soup.find('div', {'class':'covid__header'}).span.text.split(':')[1].split(',')[0]

    teks = "Data Covid-19 di Indonesia per" + tgl_Update + "\n"
    teks += "Positif : " + positif + "(" + tambahan + ")" + "\n"
    teks += "Dirawat : " + dirawat + "\n"
    teks += "Sembuh : " + sembuh + "\n"
    teks += "Meninggal dunia (Positif) : " + meninggal + "\n"
    
    return teks

def allKodeKecamatan():
    x = 22

    kode = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U"]

    kode1 = []
    for i in kode:
        kode1.append("B"+i)

    return kode1

def kecamatan():
    kecamatan = ["Medan Amplas","Medan Area","Medan Barat","Medan Baru","Medan Belawan","Medan Deli","Medan Denai","Medan Helvetia","Medan Johor","Medan Kota","Medan Labuhan","Medan Maimun","Medan Marelan","Medan Perjuangan","Medan Petisah","Medan Polonia","Medan Selayang","Medan Sunggal","Medan Tembung","Medan Timur","Medan Tuntungan"]
    return kecamatan

def tampilNamaKecamatan():
    kode_kecamatan = allKodeKecamatan()
    nama_kecamatan = kecamatan()

    teks = "Berikut kode dan nama kecamatan\n"
    for i in range(len(kode_kecamatan)):
        teks += "[" + kode_kecamatan[i] + "]" + " " + nama_kecamatan[i] + "\n"

    teks+= "\nSilahkan masukkan kode sesuai kecamatan yang tersedia"

    return teks

def cekKecamatan(kodekecamatan):
    allKodeKecamatan1 = allKodeKecamatan()
    
    allKodeKecamatan1 = [allKodeKecamatan2.lower() for allKodeKecamatan2 in allKodeKecamatan1]
    
    return kodekecamatan in allKodeKecamatan1

def hasilKecamatan(kodekecamatan):
    import requests
    from bs4 import BeautifulSoup
    import pandas as pd
    import numpy as np
    import time

    URL = "https://covid19.pemkomedan.go.id/index.php?page=stat_kec"
    r = requests.get(URL) 
    soup = BeautifulSoup(r.content, 'html5lib')
    table = soup.find('tbody') 

    No = []
    nama_kecamatan = []
    odp_kecamatan = []
    otg_kecamatan = []
    pp_kecamatan = []
    pdp_kecamatan = []
    positif_kecamatan = []
    meninggal_positif_kecamatan = []
    sembuh_kecamatan = []
    
    for i in range(len(table.findAll('tr'))):

        No.append(i+1)
        nama_kecamatan.append(table.findAll('tr')[i].findAll('td')[1].text)
        odp_kecamatan.append(table.findAll('tr')[i].findAll('td')[2].text)
        otg_kecamatan.append(table.findAll('tr')[i].findAll('td')[4].text)
        pp_kecamatan.append(table.findAll('tr')[i].findAll('td')[6].text)
        pdp_kecamatan.append(table.findAll('tr')[i].findAll('td')[10].text)
        positif_kecamatan.append(table.findAll('tr')[i].findAll('td')[13].text)
        sembuh_kecamatan.append(table.findAll('tr')[i].findAll('td')[11].text)
        meninggal_positif_kecamatan.append(table.findAll('tr')[i].findAll('td')[12].text)
   
    df_kecamatan = pd.DataFrame(No, columns =['No'])
    df_kecamatan = df_kecamatan.rename(columns={"0":"No"})
    df_kecamatan['Kecamatan'] = nama_kecamatan
    df_kecamatan['ODP'] = odp_kecamatan
    df_kecamatan['OTG'] = otg_kecamatan
    df_kecamatan['PP'] = pp_kecamatan
    df_kecamatan['PDP'] = pdp_kecamatan
    df_kecamatan['Positif'] = positif_kecamatan
    df_kecamatan['Sembuh'] = sembuh_kecamatan
    df_kecamatan['Meninggal positif'] = meninggal_positif_kecamatan

    df_kecamatan['Kode'] = allKodeKecamatan()
    is_kecamatan = df_kecamatan['Kode']==kodekecamatan.upper()
    df_cari = df_kecamatan[is_kecamatan]

    kecamatan = str(df_cari['Kecamatan'].to_string().split('    ')[1])
    odp = int(df_cari['ODP'])
    otg = int(df_cari['OTG'])
    pp = int(df_cari['PP'])
    pdp = int(df_cari['PDP'])
    positif = int(df_cari['Positif'])
    sembuh = int(df_cari['Sembuh'])
    meninggal_positif = int(df_cari['Meninggal positif'])
    
    bulan = ("Januari", "Februari", "Maret","April", "Mei", "Juni",
         "Juli", "Agustus", "September", "Oktober", "November", "Desember")
    hari = ("Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu")
    sekarang = time.time()
    infowaktu = time.localtime(sekarang)
    
    teks = "Data Covid-19 di Kecamatan " + kecamatan + " per " + hari[infowaktu[6]] + ", " + str(infowaktu[2]) + " " + bulan[infowaktu[1]-1] + " " + str(infowaktu[0]) + "\n"
    teks += "ODP : " + str(odp) + "\n"
    teks += "OTG : " + str(otg) + "\n"
    teks += "PP  : " + str(pp) + "\n"
    teks += "PDP : " + str(pdp) + "\n"
    teks += "Positif : " + str(positif) + "\n"
    teks += "Sembuh : " + str(sembuh) + "\n"
    teks += "Meninggal dunia (Positif) : " + str(meninggal_positif) + "\n"

    return teks

def allKodeProvinsi():
    x = 35
    kode = []
    for i in range(1, x, 1):
        angka = str(i)
        kode.append("C"+angka)

    return kode

def nameprovinsi():
    from bs4 import BeautifulSoup
    import requests

    source = requests.get('https://www.kompas.com/covid-19')
    soup = BeautifulSoup(source.text, 'html5lib')

    nama_prov = soup.find_all('div', {'class':'covid__row'})
    nama_provinsi = []

    for i in range(len(nama_prov)-1):
        nama_provinsi.append(nama_prov[i].find_all('div')[0].text)

    return nama_provinsi

def cekProvinsi(kodeprovinsi):
    allKodeProvinsi1 = allKodeProvinsi()
    
    allKodeProvinsi1 = [allKodeProvinsi2.lower() for allKodeProvinsi2 in allKodeProvinsi1]
    
    return kodeprovinsi in allKodeProvinsi1

def tampilNamaProvinsi():
    kode_provinsi = allKodeProvinsi()
    nama_provinsi = nameprovinsi()

    teks = "Berikut kode dan nama provinsi\n"
    for i in range(len(kode_provinsi)):
        teks += "[" + kode_provinsi[i] + "]" + " " + nama_provinsi[i] + "\n"

    teks+= "\nSilahkan masukkan kode sesuai provinsi yang tersedia"

    return teks

def hasilProvinsi(kodeprovinsi):
    import requests
    from bs4 import BeautifulSoup
    import pandas as pd
    import numpy as np
    source = requests.get('https://www.kompas.com/covid-19')
    soup = BeautifulSoup(source.text, 'html5lib')
    
    nama_prov = soup.find_all('div', {'class':'covid__row'})
    tgl_Update = soup.find('div', {'class':'covid__header'}).span.text.split(':')[1].split(',')[0]

    No = []
    positif_provinsi = []
    meninggal_positif_provinsi = []
    sembuh_provinsi = []
    
    for i in range(len(nama_prov)-1):

        No.append(i+1)
        positif_provinsi.append(nama_prov[i].find('div', {'class':'covid__total'}).find('span', {'class':'-odp'}).find('strong').text)
        meninggal_positif_provinsi.append(nama_prov[i].find('div', {'class':'covid__total'}).find('span', {'class':'-gone'}).find('strong').text)
        sembuh_provinsi.append(nama_prov[i].find('div', {'class':'covid__total'}).find('span', {'class':'-health'}).find('strong').text)
   
    df_provinsi = pd.DataFrame(No, columns =['No'])
    df_provinsi = df_provinsi.rename(columns={"0":"No"})
    df_provinsi['Positif'] = positif_provinsi
    df_provinsi['Sembuh'] = sembuh_provinsi
    df_provinsi['Meninggal positif'] = meninggal_positif_provinsi

    df_provinsi['Nama Provinsi'] = nameprovinsi()
    df_provinsi['Kode'] = allKodeProvinsi()

    is_provinsi = df_provinsi['Kode']==kodeprovinsi.upper()
    df_cari = df_provinsi[is_provinsi]

    provinsi = str(df_cari['Nama Provinsi'].to_string().split('    ')[1])
    positif = int(df_cari['Positif'])
    sembuh = int(df_cari['Sembuh'])
    meninggal_positif = int(df_cari['Meninggal positif'])

    teks = "Data Covid-19 di Provinsi " + str(provinsi) + " per" + tgl_Update + "\n"
    teks += "Positif : " + str(positif) + "\n"
    teks += "Sembuh : " + str(sembuh) + "\n"
    teks += "Meninggal dunia (Positif) : " + str(meninggal_positif) + "\n"

    return teks

def allKodeKabupaten():
    x = 34

    kode = []
    for i in range(1, x, 1):
        angka = str(i)
        kode.append("D"+angka)

    return kode

def namekabupaten():
    from bs4 import BeautifulSoup
    import requests

    source = requests.get('http://covid19.sumutprov.go.id/')
    soup = BeautifulSoup(source.text, 'html5lib')

    nama_kab = soup.find_all('table',{'class':'table'})[1].find('tbody')
    nama_kabupaten = []

    for i in range(len(nama_kab.find_all('tr'))):
        nama_kabupaten.append(nama_kab.find_all('tr')[i].find_all('td')[1].text.title())

    return nama_kabupaten

def tampilNamaKabupaten():
    kode_kabupaten = allKodeKabupaten()
    nama_kabupaten = namekabupaten()

    teks = "Berikut kode dan nama kabupaten\n"
    for i in range(len(kode_kabupaten)):
        teks += "[" + kode_kabupaten[i] + "]" + " " + nama_kabupaten[i] + "\n"

    teks+= "\nSilahkan masukkan kode sesuai kabupaten yang tersedia"

    return teks

def cekKabupaten(kodekabupaten):
    allKodeKabupaten1 = allKodeKabupaten()
    
    allKodeKabupaten1 = [allKodeKabupaten2.lower() for allKodeKabupaten2 in allKodeKabupaten1]
    
    return kodekabupaten in allKodeKabupaten1

def hasilKabupaten(kodekabupaten):
    import requests
    from bs4 import BeautifulSoup
    import pandas as pd
    import numpy as np
    import time

    URL = "http://covid19.sumutprov.go.id/"
    r = requests.get(URL) 
    soup = BeautifulSoup(r.content, 'html5lib')
    table = soup.find_all('table',{'class':'table'})[1].find('tbody')

    No = []
    pdp_kabupaten = []
    positif_kabupaten = []
    meninggal_positif_kabupaten = []
    sembuh_kabupaten = []
    
    for i in range(len(table.findAll('tr'))):

        No.append(i+1)
        pdp_kabupaten.append(table.find_all('tr')[i].find_all('td')[2].text)
        positif_kabupaten.append(table.find_all('tr')[i].find_all('td')[3].text)
        sembuh_kabupaten.append(table.find_all('tr')[i].find_all('td')[5].text)
        meninggal_positif_kabupaten.append(table.find_all('tr')[i].find_all('td')[4].text)
   
    df_kabupaten = pd.DataFrame(No, columns =['No'])
    df_kabupaten = df_kabupaten.rename(columns={"0":"No"})
    df_kabupaten['PDP'] = pdp_kabupaten
    df_kabupaten['Positif'] = positif_kabupaten
    df_kabupaten['Sembuh'] = sembuh_kabupaten
    df_kabupaten['Meninggal positif'] = meninggal_positif_kabupaten

    df_kabupaten['Nama Kabupaten'] = namekabupaten()
    df_kabupaten['Kode'] = allKodeKabupaten()
    is_kabupaten = df_kabupaten['Kode']==kodekabupaten.upper()
    df_cari = df_kabupaten[is_kabupaten]

    kabupaten = str(df_cari['Nama Kabupaten'].to_string().split('    ')[1])
    pdp = int(df_cari['PDP'])
    positif = int(df_cari['Positif'])
    sembuh = int(df_cari['Sembuh'])
    meninggal_positif = int(df_cari['Meninggal positif'])
    
    bulan = ("Januari", "Februari", "Maret","April", "Mei", "Juni",
         "Juli", "Agustus", "September", "Oktober", "November", "Desember")
    hari = ("Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu")
    sekarang = time.time()
    infowaktu = time.localtime(sekarang)
    
    teks = "Data Covid-19 di " + kabupaten + " per " + hari[infowaktu[6]] + ", " + str(infowaktu[2]) + " " + bulan[infowaktu[1]-1] + " " + str(infowaktu[0]) + "\n"
    teks += "PDP : " + str(pdp) + "\n"
    teks += "Positif : " + str(positif) + "\n"
    teks += "Sembuh : " + str(sembuh) + "\n"
    teks += "Meninggal dunia (Positif) : " + str(meninggal_positif) + "\n"

    return teks

def allKodeRumahSakit():
    x = 35

    kode = []
    for i in range(1, x, 1):
        angka = str(i)
        kode.append("E"+angka)

    return kode

def tampilNamaProvRS():
    kode_provinsi = allKodeRumahSakit()
    nama_provinsi = nameprovinsi()
    nama_provinsi1 = nama_provinsi.sort()
    teks = "Berikut kode dan nama provinsi\n\n"
    for i in range(len(kode_provinsi)):
        teks += "[" + kode_provinsi[i] + "]" + " " + nama_provinsi[i] + "\n"

    teks+= "\nSilahkan masukkan kode sesuai kode nama provinsi RS tujuan yang tersedia"

    return teks

def cekRumahSakit(koders):
    allKodeRumahSakit1 = allKodeRumahSakit()
    
    allKodeRumahSakit1 = [allKodeRumahSakit2.lower() for allKodeRumahSakit2 in allKodeRumahSakit1]
    
    return koders in allKodeRumahSakit1

def hasilRS(koders):
    resp = ""
    resp += "Rumah sakit rujukan di Provinsi "
    kode = str(koders)

    if kode=="e1":
        resp += "Aceh\n"
        resp += "\n"
        resp += "1. RSU Dr. Zainoel Abidin Banda Aceh - Jl. Teuku Moh. Daud Beureueh No.108, Banda Aceh. Telp: (0651) 34565, 22077, 28148\n\n"
        resp += "2. RSU Cut Meutia Lhokseumawe - Jl. Banda Aceh-Medan Km.6 Buket Rata, Lhokseumawe. Telp: (0645) 43012"
    elif kode=="e2":
        resp += "Bali\n"
        resp += "\n"
        resp += "1. RSUP Sanglah - Jl. Diponegoro, Denpasar, Bali. Telp: (0361) 227912\n\n"
        resp += "2. RSUD Sanjiwani Gianyar - Jl. Ciung Wanara-Gianyar No.2, Gianyar. Telp: (0361) 943020\n\n"
        resp += "3. RSUD Tabanan - Jl. Pahlawan No.14, Tabanan. Telp: (0361) 811027\n\n"
        resp += "4. RSUD Kabupaten Buleleng - Jl. Ngurah Rai No.30, Astina, Buleleng. Telp: (0362) 22046"
    elif kode=="e3":
        resp += "Banten\n"
        resp += "\n"
        resp += "1. RSUD Kabupaten Tangerang - Jl. Jend. Ahmad Yani No.9. Telp: (021) 5523507\n\n"
        resp += "2. RSUD dr. Drajat Prawiranegara Serang - Jl. Rumah Sakit Umum No.1, Serang."
    elif kode=="e4":
        resp += "Bengkulu\n"
        resp += "\n"
        resp += "1. RSUD M. Yunus Bengkulu - Jl. Bhayangkara, Sidomulyo, Bengkulu. Telp: (0736) 52004, 52008, 51111\n\n"
        resp += "2. RSUD Arga Makmur - Jl. Siti Khadijah No.8, Arga Makmur, Bengkulu Utara. Telp: (0737) 521118\n\n"
        resp += "3. RSUD Hasanuddin Damrah Manna - Raya Padang Panjang, Manna, Bengkulu Selatan. Telp: (0739) 22870"
    elif kode=="e5":
        resp += "Daerah Istimewa Yogyakarta\n"
        resp += "\n"
        resp += "1. RSUP dr. Sardjito - Jl. Kesehatan No.1, Yogyakarta. Telp: (0274) 631190\n\n"
        resp += "2. RSUD Panembahan Senopati Bantul - Jl. Dr. Wahidin Sudiro Husodo, Bantul. Telp: (0274) 367381\n\n"
        resp += "3. RSUD Kota Yogyakarta - Jl. Ki Ageng Pemanahan No.1, Yogyakarta. Telp: (0274) 371195\n\n"
        resp += "4. RSUD Wates - Jl. Tentara Pelajar Km. 1 No. 5, Kulon Progo. Telp: (0274) 773169"
    elif kode=="e6":
        resp += "DKI Jakarta\n"
        resp += "\n"
        resp += "1. RSPI Prof. Dr. Sulianti Saroso - Jl. Sunter Permai Raya, Tanjung Priok, Jakarta Utara. Telp: (021) 6506559\n\n"
        resp += "2. RSUP Persahabatan - Jl. Persahabatan Raya No.1, Jakarta Timur. Telp: (021) 4891708, 4891745\n\n"
        resp += "3. RSUP Fatmawati - Jl. TB Simatupang c No.18, Cilandak, Jakarta Selatan. Telp: (021) 7501524\n\n"
        resp += "4. RSUD Cengkareng - Jl. Bumi Cengkareng Indah No.1, Cengkareng, Jakarta Barat. Telp: (021) 54372882\n\n"
        resp += "5. RSUD Pasar Minggu - Jl. TB Simatupang No.1, RW.5, Pasar. Minggu, Jakarta Selatan. Telp: (021) 29059999\n\n"
        resp += "6. RS Bhayangkara TK. I R. Said Sukanto - Jl. Raya Jakarta-Bogor, Kramat Jati, Jakarta Timur. Telp: (021) 8093288\n\n"
        resp += "7. RSPAD Gatot Subroto - Jl. Abdul Rahman Saleh Raya No.24, Senen, Jakarta Pusat. Telp: (021) 3441008\n\n"
        resp += "8. RSAL dr. Mintoharjo - Jl. Bendungan Hilir No.17 A, Bendungan Hilir, Jakarta Pusat. Telp: (021) 5703081\n\n"
        resp += "9. RS Pertamina Jaya - Jl. Jenderal Ahmad Yani No.2, Cempaka Putih Tim, Jakarta Pusat. Telp: (021) 4211911"
    elif kode=="e7":
        resp += "Gorontalo\n"
        resp += "\n"
        resp += "1. RSUD Prof. dr. H. Aloei Saboe - Jl. S. Batutihe No.7, Gorontalo. Telp: (0435) 821019"
    elif kode=="e8":
        resp += "Jambi\n"
        resp += "\n"
        resp += "1. RSUD Raden Mattaher Jambi - Jl. Letjen Suprapto No.31, Telanaipura, Jambi. Telp: (0741) 61692"
    elif kode=="e9":
        resp += "Jawa Barat\n"
        resp += "\n"
        resp += "1. RSUD Kabupaten Bekasi - Jl. Raya Teuku Umar No.202, Bekasi. Telp: (021) 883 74 444\n\n"
        resp += "2. RS Hermina Grand Wisata - Jl. Festival Boulevard Blok JA I No. 1, Grand Wisata, Bekasi. Telp: (021) 826 512 12\n\n"
        resp += "3. RS Sentra Medika  - Jl. Raya Industri Pasir Gombong - Cikarang, Bekasi. Telp: (021) 890 416 064\n\n"
        resp += "4. RS Siloam Cikarang - Jl. MH. Thamrin No.Kav. 105, Cikarang, Bekasi. Telp: (021) 296 369 00\n\n"
        resp += "5. RS Omni Cikarang - Komp The Oasis Kav No.1, Jl. Raya Cikarang - Cibarusah, Bekasi. Telp: (021) 297 79 999\n\n"
        resp += "6. RS Mitra Keluarga Cikarang - Jl. Raya Industri No.100, Cikarang, Bekasi. Telp: (021) 898 40 900\n\n"
        resp += "7. RS Dokter Adam Thalib - Jl. Raya Teuku Umar No.25, Cikarang, Bekasi. Telp: (021) 883 32 305\n\n"
        resp += "8. RS Grha MM2100 - Jl. Kalimantan Blok CB-1 Kawasan Industri MM2100, Cikarang, Bekasi. Telp: (021) 505 70 911\n\n"
        resp += "9. RS Cibitung Medika - Jl. Bosih Raya No.117, Cibitung, Bekasi. Telp: (021) 883 23 444\n\n"
        resp += "10. RS Annisa - Jl. Cikarang Baru Raya No.31, Cikarang, Bekasi. Telp: (021) 890 4165\n\n"
        resp += "11. RSUP dr. Hasan Sadikin - Jl. Pasteur No.38, Pasteur, Bandung. Telp: (022) 2551111\n\n"
        resp += "12. RS Paru Dr. H. A. Rotinsulu - Jl. Bukit Jarian No.40, Bandung. Telp: (022) 2034446\n\n"
        resp += "13. RS Paru dr. M. Goenawan Partowidigdo - Jl. Puncak Raya Km. 83, Cisarua, Bogor. Telp: (0251) 8253630\n\n"
        resp += "14. RSUD Gunung Jati Cirebon - Jl. Kesambi Raya No.56, Cirebon. Telp: (0231) 206330\n\n"
        resp += "15. RSUD R. Syamsudin, SH Sukabumi - Jl. Rumah Sakit No.1, Sukabumi. Telp: (0266) 245703\n\n"
        resp += "16. RSUD dr. Slamet Garut - Jl. Rumah Sakit No.10, Garut. Telp: (0262) 232720\n\n"
        resp += "17. RSUD Kabupaten Indramayu - Jl. Murahnara No.7, Sindang, Indramayu. Telp: (0234) 272655\n\n"
        resp += "18. RSU Tk. II Dustira - Jl. Dustira No.1, Baros, Cimahi."
    elif kode=="e10":
        resp += "Jawa Tengah\n"
        resp += "\n"
        resp += "1. RSUP dr. Kariadi - Jl. Dr. Sutomo No.16, Semarang. Telp: (024) 8413993, 8413476\n\n"
        resp += "2. RS dr. Seoradji Tirtonegoro Klaten - Jl. Dr. Soeradji Tirtonegoro No.1, Klaten. Telp: (0272) 321041\n\n"
        resp += "3. RS Paru dr. Ario Wirawan - Jl. Hasanudin No.806, Mangunsari, Salatiga. Telp: (0298) 326130\n\n"
        resp += "4. RSUD Prof. Dr. Margono Soekarjo - Jl. Dr. Gumbreg No.1, Purwokerto. Telp: (0281) 632708\n\n"
        resp += "5. RSUD dr. Moewardi Surakarta - Jl. Kolonel Sutarto No.132, Surakarta. Telp: (0271) 634634\n\n"
        resp += "6. RSUD Tidar Magelang - Jl. Tidar No.30 A, Magelang. Telp: (0293) 36226\n\n"
        resp += "7. RSUD KRMT Wongsonegoro - Jl. Fatmawati No.1, Semarang. Telp: (024) 6711500\n\n"
        resp += "8. RSUD Kardinah Tegal - Jl. Aip. Ks. Tubun No. 4, Tegal. Telp: (0283) 356067\n\n"
        resp += "9. RSUD Banyumas - Jl. Rumah Sakit No.1, Karangpucung, Kabupaten Banyumas. Telp: (0281) 796031\n\n"
        resp += "10. RSU dr. Loekmonohadi - Jl. Dr. Lukmonohadi No.19, Kabupaten Kudus. Telp:  (0291) 444001\n\n"
        resp += "11. RSUD Kraton - Jl. Veteran No.31, Pekalongan. Telp: (0285) 421621\n\n"
        resp += "12. RSUD dr. Soeselo Slawi - Jl. Dr. Sutomo No.63, Slawi. Telp: (0283) 491016\n\n"
        resp += "13. RSUD RAA Soewondo Kendal - Jl. Laut No.21, Kendal. Telp: (0294) 381433"
    elif kode=="e11":
        resp += "Jawa Timur\n"
        resp += "\n"
        resp += "1. RSUD dr. Soetomo - Jl. Mayjen Prof. Dr. Moestopo No.6 – 8, Surabaya. Telp: (031) 5501078\n\n"
        resp += "2. RSUD dr. Soedono Madiun - Jl. Dr. Sutomo No.59, Madiun. Telp: (0351) 454657\n\n"
        resp += "3. RSUD dr. Saiful Anwar - Jl. Jaksa Agung Suprapto No.2, Malang. Telp: (0341) 362101\n\n"
        resp += "4. RSUD dr. Soebandi Jember - Jl. Dr. Soebandi No.124, Jember. Telp: 0823 0159 8557\n\n"
        resp += "5. RSUD Kabupaten Kediri Pare - Jl. Pahlawan Kusuma Bangsa No.1, Pare. Telp: (0354) 391718\n\n"
        resp += "6. RSUD dr. R. Koesma Tuban - Jl. Dr. Wahidin Sudirohusodo No.800, Tuban. Telp: (0356) 321010\n\n"
        resp += "7. RSUD Blambangan - Jl. Letkol Istiqlah No.49, Banyuwangi. Telp: (0333) 421118\n\n"
        resp += "8. RSUD Dr. R. Sosodoro Djatikoesoemo - Jl. Dr. Wahidin No.36, Bojonegoro. Telp: (0353) 881193\n\n"
        resp += "9. RSUD Dr. Iskak Tulungagung - Jl. Dr. Wahidin Sudiro Husodo, Kabupaten Tulungagung. Telp: (0355) 322609\n\n"
        resp += "10. RSUD Sidoarjo - Jl. Mojopahit No.667, Kabupaten Sidoarjo. Telp: (031) 8961649\n\n"
        resp += "11. RS Universitas Airlangga - Kampus C Unair, Jl. Mulyorejo, Surabaya. (031) 5961389"
    elif kode=="e12":
        resp += "Kalimantan Barat\n"
        resp += "\n"
        resp += "1. RSUD dr. Soedarso Pontianak - Jl. Dr. Soedarso No.1, Pontianak. Telp: (0561) 737701\n\n"
        resp += "2. RSUD dr. Abdul Azis Singkawang - Jl. Dr. Soetomo No.28, Singkawang. Telp: (0562) 631748\n\n"
        resp += "3. RSUD Ade Mohamad Djoen Sintang - Jl. Pattimura No.1, Sintang. Telp: (0565) 22022\n\n"
        resp += "4. RSUD dr. Agoesdjam Ketapang - Jl. DI Panjaitan No.51, Sampit, Kabupaten Ketapang. Telp: (0534) 3037239"
    elif kode=="e13":
        resp += "Kalimantan Selatan\n"
        resp += "\n"
        resp += "1. RSUD Ulin Banjarmasin - Jl. Ahmad Yani No.43, Banjarmasin. Telp: (0511) 3252229\n\n"
        resp += "2. RSUD H. Boejasin Pelaihari - Jl. A. Syahrani, Pelaihari. Telp: (0512) 21082"
    elif kode=="e14":
        resp += "Kalimantan Tengah\n"
        resp += "\n"
        resp += "1. RSUD dr. Doris Sylvanus Palangkaraya - Jl. Tambun Bungai No.4, Palangka Raya. Telp: (0536) 3221717\n\n"
        resp += "2. RSUD dr. Murjani Sampit - Jl. H. Muhammad Arsyad No.65, Kotawaringin Timur. Telp: (0531) 21010\n\n"
        resp += "3. RSUD Sultan Imanuddin Pangkalan Bun - Jl. Sutan Syahrir No.17, Kabupaten Kotawaringin Barat. Telp: (0532) 21404"
    elif kode=="e15":
        resp += "Kalimantan Timur\n"
        resp += "\n"
        resp += "1. RSUD Abdul Wahab Sjahrani - Jl. Palang Merah No.1, Samarinda. Telp: (0541) 738118\n\n"
        resp += "2. RSUD dr. Kanujoso Djatiwibowo - Jl. MT Haryono No.656, Balikpapan. Telp: (0542) 873901\n\n"
        resp += "3. RSU Taman Husada Bontang - Jl. Letjen S. Parman No.1, Bontang. Telp: (0548) 22111\n\n"
        resp += "4. RSUD Panglima Sebaya - Jl. Kusuma Bangsa Km.5, Paser. Telp: (0543) 21363\n\n"
        resp += "5. RSUD Aji Muhammad Parikesit - Jl. Ratu Agung No.1, Tlk. Dalam, Kutai Kartanegara. Telp: (0541) 661015"
    elif kode=="e16":
        resp += "Kalimantan Utara\n"
        resp += "\n"
        resp += "1. RSUD Kota Tarakan - Jl. Pulau Irian No.1, Kp. Satu Skip, Tarakan. Telp: (0551) 21166\n\n"
        resp += "2. RSUD Tanjung Selor - Jl. Cendrawasih - Tanjung Selor. Telp: (0552)- 21292"
    elif kode=="e17":
        resp += "Kepulauan Bangka Belitung\n"
        resp += "\n"
        resp += "1. RSUD Depati Hamzah - Jl. Soekarno Hatta, Bukitbesar, Pangkal Pinang. Telp: (0717) 422693\n\n"
        resp += "2. RSUD dr. H. Marsidi Judono - Air Raya, Tj. Pandan, Belitung. Telp: (0719) 21071"
    elif kode=="e18":
        resp += "Kepulauan Riau\n"
        resp += "\n"
        resp += "1. RSUD Provinsi Kepulauan Riau Tanjung Pinang - Jl. WR. Supratman No.100, Air Raja, Tanjung Pinang. Telp: (0771) 7335202\n\n"
        resp += "2. RSUD Embung Fatimah - Bukit Tempayan, Batu Aji, Batam. Telp: (0778) 364446\n\n"
        resp += "3. RSUD Muhammad Sani Kab. Karimun - Jl. Poros No.1, Tanjung Balai, Karimun. Fax: 29611\n\n"
        resp += "4. RS Badan Pengusahaan Batam - Jl. Cipto Mangunkusumo No.1, Sekupang, Batam. Telp: (0778) 322121"
    elif kode=="e19":
        resp += "Lampung\n"
        resp += "\n"
        resp += "1. RSUD Dr. H. Abdul Moeloek - Jl. Dr. Rivai No.6, Bandar Lampung. Telp: (0721) 703312\n\n"
        resp += "2. RSUD Ahmad Yani Metro - Jl. Jend. Ahmad Yani No.13, Imopuro, Metro, Lampung. Telp: (0725) 41820\n\n"
        resp += "3. RSUD Dr. H. Bob Bazar, SKM - Jl. Batin Tjindar Bumi No.14 B, Kab. Lampung Selatan. Telp: (0727) 322159\n\n"
        resp += "4. RSUD Mayjen H.M. Ryacudu - Jl. Jend. Sudirman No.24, Kotabumi, Kab. Lampung Utara. Telp: (0724) 22095"
    elif kode=="e20":
        resp += "Maluku\n"
        resp += "\n"
        resp += "1. RSUP dr. J. Leimena - Rumah Tiga, Tlk. Ambon, Ambon.\n\n"
        resp += "2. RSU Dr. M. Haulussy Ambon - Jl. Dr. Kayadoe, Benteng, Ambon. Telp: (0911) 343002\n\n"
        resp += "3. RSUD dr. P. P. Magrettti Saumlaki - Jl. Ir. Soekarno - Poros Utama, Kabupaten Maluku Tenggara Barat. Telp: (0918) 21113"
    elif kode=="e21":
        resp += "Maluku Utara\n"
        resp += "\n"
        resp += "1. RSUD dr. H. Chasan Boesoirie - Jl. Cempaka, Ternate. Telp: (0921) 3121281, 3127159"
    elif kode=="e22":
        resp += "Nusa Tenggara Barat\n"
        resp += "\n"
        resp += "1. RSUD NTB - Jl. Prabu Rangkasari, Dasan Cermen, Mataram. Telp: (0370) 7502424\n\n"
        resp += "2. RSUD Kota Bima - Jl. Langsat No.1, Raba, Bima. Telp: (0374) 43142\n\n"
        resp += "3. RSUD Dr. R. Sudjono - Jl. Prof. M. Yamin SH No.55, Selong. Telp: (0376) 21118\n\n"
        resp += "4. RSUD H. L. Manambai Abdul Kadir - Jl. Lintas Sumbawa-Bima Km 5, Seketeng, Kabupaten Sumbawa. Telp: (0371) 2628078"
    elif kode=="e23":
        resp += "Nusa Tenggara Timur\n"
        resp += "\n"
        resp += "1. RSUD Prof. dr. W. Z. Johannes - Jl. Dr. Moch. Hatta No.19, Kupang. Telp: (0380) 832892\n\n"
        resp += "2. RSU dr. TC. Hillers Maumere - Jl. Wairklau, No. 1, Kota Baru, Alok Timur, Kabupaten Sikka. (0382) 21314\n\n"
        resp += "3. RSUD Komodo Labuan Bajo - Jl. Trans Ruteng - Labuan Bajo, Desa Golo Bilas, Komodo."
    elif kode=="e24":
        resp += "Papua\n"
        resp += "\n"
        resp += "1. RSU Jayapura - Jl. Kesehatan No.1, Jayapura. Telp: (0967) 533616\n\n"
        resp += "2. RSU Nabire - Jl. R.E. Martadinata, Siriwini, Nabire. Telp: (0984) 21846\n\n"
        resp += "3. RSU Merauke - Jl. Soekarjo Wiryopranoto No.1, Maro, Merauke. Telp: (0971) 321124"
    elif kode=="e25":
        resp += "Papua Barat\n"
        resp += "\n"
        resp += "1. RSUD Sorong - Kp. Baru, Sorong. Telp: (0951) 321850\n\n"
        resp += "2. RSUD Manokwari - Jl. Siliwangi No.1, Manokwari Barat. Telp: (0986) 215133"
    elif kode=="e26":
        resp += "Riau\n"
        resp += "\n"
        resp += "1. RSU Arifin Achmad - Jl. Diponegoro No.2, Pekanbaru. Telp: (0761) 21618\n\n"
        resp += "2. RSUD Kota Dumai - Jl. Tanjung Jati No.4, Dumai. Telp: (0762) 38368, (0765) 440992\n\n"
        resp += "3. RSUD Puri Husada Tembilahan - Jl. Veteran No.52, Hilir Tembilahan. Telp: (0768) 22118"
    elif kode=="e27":
        resp += "Sulawesi Barat\n"
        resp += "\n"
        resp += "1. RSUD Provinsi Sulawesi Barat - Jl. RE Martadinata, Simboro, Kabupaten Mamuju. Telp: 0823 9621 2345"
    elif kode=="e28":
        resp += "Sulawesi Selatan\n"
        resp += "\n"
        resp += "1. RSUP dr. Wahidin Sudirohusodo - Jl. Perintis Kemerdekaan Km.11, Makassar. Telp: (0411) 510675\n\n"
        resp += "2. RS Dr. Tadjuddin Chalid MPH - Jl. Paccerakkang No.67, Makassar. Telp: (0411) 512902\n\n"
        resp += "3. RSUD Labuang Baji - Jl. Dr. Ratulangi No.81, Makassar. Telp: (0411) 873482\n\n"
        resp += "4. RSUD Andi Makkasau Parepare - Jl. Nurussamawati No.9, Bumi Harapan, Pare-Pare\n\n"
        resp += "5. RSU Lakipadada Toraja - Jl. Pongtiku No. 486, Kabupaten Tana Toraja. (0423) 22264\n\n"
        resp += "6. RSUD Kabupaten Sinjai - Jl. Jend. Sudirman No.47, Sinjai. Telp: (0482) 21132\n\n"
        resp += "7. RS Tk. II Pelamonia - Jl. Jend. Sudirman No.27, Makassar. Telp: 0811 1782 399"
    elif kode=="e29":
        resp += "Sulawesi Tengah\n"
        resp += "\n"
        resp += "1. RSUD Undata Palu - Jl. Trans Sulawesi Tondo, Palu. Telp: (0451) 4908020\n\n"
        resp += "2. RSU Anutapura Palu - Jl. Kangkung,  Donggala Kodi, Palu. Telp: (0451) 460570\n\n"
        resp += "3. RSUD Banggai Luwuk - Jl. lmam Bonjol No.14, Luwuk. Telp: (0461) 21820\n\n"
        resp += "4. RSU Mokopido Toli-Toli - Jl. Lanoni I No.37, Toli-Toli. Telp: (0453) 21300\n\n"
        resp += "5. RSUD Kolonedale - Jl. W. Monginsidi No.2, Kolonedale. Telp: (0465) 21010"
    elif kode=="e30":
        resp += "Sulawesi Tenggara\n"
        resp += "\n"
        resp += "1. RS Bahtera Mas Kendari - Jl. Kapten Piere Tendean, Watubangga, Kendari. Telp: (0401) 3195611"
    elif kode=="e31":
        resp += "Sulawesi Utara\n"
        resp += "\n"
        resp += "1. RSUP Prof. dr. R. D Kandou - Jl. Raya Tanawangko No.56, Manado. Telp: (0431) 8383058\n\n"
        resp += "2. RSU Ratatotok Buyat - Jl. J. W. Lasut Ratatotok II, Ratatotok,  Minahasa. Telp: (0431) 3177610\n\n"
        resp += "3. RSUD Kotamobagu - Pobundayan, Kotamobagu. Telp: (0435) 822816\n\n"
        resp += "4. RSUD dr. Sam Ratulangi - Jl. Suprapto No.123, Luaan, Kabupaten Minahasa. Telp: (0431) 321171"
    elif kode=="e32":
        resp += "Sumatera Barat\n"
        resp += "\n"
        resp += "1. RSUP Dr. M. Jamil Padang - Jl. Perintis Kemerdekaan, Padang. Telp. (0751) 32372, 37030\n\n"
        resp += "2. RSUD Dr. Achmad Mochtar Bukittinggi - Jl. Dr. Abdul Rivai No.1, Bukittinggi. Telp: (0752) 21720, 21831"
    elif kode=="e33":
        resp += "Sumatera Selatan\n"
        resp += "\n"
        resp += "1. RSUP M. Hoesin - Jl. Jend. Sudirman Km.3-5, Palembang. Telp: (0711) 30126, 354088\n\n"
        resp += "2. RS Dr. Rivai Abdullah - Jl. Sungai Kundur Kab. Banyu Asin. Telp: (0711) 7537201\n\n"
        resp += "3. RSUD Siti Fatimah Provinsi Sumatera Selatan - Jl. Kol. H. Burlian, Suka Bangun, Palembang. Telp: (0711) 5718883\n\n"
        resp += "4. RSUD Lahat - Jl. Mayor Ruslan No.29, Lahat. Telp: (0731) 321785, 21785\n\n"
        resp += "5. RSUD Kayuagung - Jl. Raya Lintas Timur, Kayuagung. Telp: (0712) 323889"
    elif kode=="e34":
        resp += "Sumatera Utara\n"
        resp += "\n"
        resp += "1. RSUP H. Adam Malik Medan - Jl. Bunga Lau No.17. Telp: (061) 8360381\n\n"
        resp += "2. RSU Kabanjahe - Jl. KS Ketaren 8, Kabanjahe. Telp: (0628) 20550\n\n"
        resp += "3. RSU Dr. Djasamen Saragih Pematang Siantar - Jl. Sutomo No.230, Pematang Siantar. Telp: (0622) 22959\n\n"
        resp += "4. RSUD Tarutung - Jl. H. Agus Salim No.1, Tapanuli Utara. Telp: (0633) 21303\n\n"
        resp += "5. RSU Padang Sidempuan - Jl. Dr. Ferdinand Lumban Tobing No.10, Padang Sidempuan. Telp: (0634) 21780, 21251"
        
    return resp

def Tentang():
    teks = "Chatbot oleh : Lit-Z 2020\n"
    teks += "Lit-Z adalah website berita dan layanan pengulasan plagiarism teks kajian pengguna\n"
    teks += "Lit-z.com"
    
    return teks

def Sumber():
    teks = "Sumber Data Covid-19 yang tersedia dalam bot adalah : \n"
    teks += "-| https://www.kompas.com/covid-19\n"
    teks += "-| https://covid19.pemkomedan.go.id/index.php?page=stat_kec\n"
    teks += "-| http://covid19.sumutprov.go.id\n"
    teks += "-| https://www.sehatq.com/artikel/daftar-rumah-sakit-untuk-penanganan-virus-corona-covid-19"
    
    return teks

def Menu():
    teks = "Apa yang ingin kamu ketahui?\n\n"
    teks += "A. Data Covid-19 di Indonesia\n"
    teks += "B. Data Covid-19 di tiap Kecamatan di Kota Medan\n"
    teks += "C. Data Covid-19 di tiap Provinsi di Indonesia\n"
    teks += "D. Data Covid-19 di tiap Kabupaten di Sumatera Utara\n"
    teks += "E. Rumah Sakit Rujukan\n"
    teks += "F. Sumber\n"
    teks += "G. Tentang\n\n"

    teks += "Ketik kode sesuai kode yang tersedia. Contoh : Ketik 'A' untuk melihat data Covid-19 di Indonesia"
    
    return teks

def kataSalah():
    teks = "Keyword tidak tersedia"

    return teks

def kembali():
    teks = "Ketik 'MENU' untuk ke menu utama"

    return teks

from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"

@app.route("/sms", methods=['POST'])
def sms_reply():
    """Respond to incoming calls with a simple text message."""
    # Fetch the message
    msg = request.form.get('Body').lower().replace(" ","")

    resp = MessagingResponse()

    # Create reply
    if msg == "menu":
    	hasil = Menu()
    	resp.message(hasil)

    elif msg == "a":
    	hasil = dataIndonesia()
    	resp.message(hasil)

    elif msg == "b":
    	hasil = tampilNamaKecamatan()
    	resp.message(hasil)

    elif msg == "c":
    	hasil = tampilNamaProvinsi()
    	resp.message(hasil)

    elif msg == "d":
    	hasil = tampilNamaKabupaten()
    	resp.message(hasil)

    elif msg == "e":
    	hasil = tampilNamaProvRS()
    	resp.message(hasil)

    elif msg == "f":
    	kemenu = kembali()
    	hasil = Sumber()
    	hasil += "\n\n" + kemenu
    	resp.message(hasil)

    elif msg == "g":
    	kemenu = kembali()
    	hasil = Tentang()
    	hasil += "\n\n" + kemenu
    	resp.message(hasil)

    else:
    	if (cekKecamatan(msg)):
    		kemenu = kembali()
    		hasil = hasilKecamatan(msg)
    		hasil += "\n\n" + kemenu
    		resp.message(hasil)

    	elif (cekProvinsi(msg)):
    		kemenu = kembali()
    		hasil = hasilKecamatan(msg)
    		hasil += "\n\n" + kemenu
    		resp.message(hasil)

    	elif (cekKabupaten(msg)):
    		kemenu = kembali()
    		hasil = hasilKabupaten(msg)
    		hasil += "\n\n" + kemenu
    		resp.message(hasil)

    	elif (cekRumahSakit(msg)):
    		kemenu = kembali()
    		hasil = hasilRS(msg)
    		hasil += "\n\n" + kemenu
    		resp.message(hasil)

    	else:
    		kemenu = kembali()
    		hasil = kataSalah()
    		hasil += "\n\n" + kemenu
    		resp.message(hasil)

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)