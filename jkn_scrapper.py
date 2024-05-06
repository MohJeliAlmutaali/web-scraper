from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time

# Inisialisasi WebDriver (pastikan Anda telah menginstal browser driver yang sesuai)
driver = webdriver.Firefox()

url = "https://play.google.com/store/apps/details?id=app.bpjs.mobile&hl=id&gl=US"

# Buka halaman web yang mengandung elemen yang ingin diekstrak
driver.get(url)

# Temukan dan klik elemen yang Anda sebutkan
elemen_klik = driver.find_element_by_xpath('/html/body/c-wiz[2]/div/div/div[1]/div/div[2]/div/div[1]/div[1]/c-wiz[4]/section/div/div[2]/div[5]/div/div/button')
elemen_klik.click()

# Menunggu beberapa detik setelah mengklik tombol "Lihat Selengkapnya"
time.sleep(5)

# Mendefinisikan JavaScript untuk melakukan scroll ke bawah
scroll_script = """
    var elements = document.querySelectorAll('.RHo1pe');
    var last_element = elements[elements.length - 1];
    last_element.scrollIntoView();
"""

# Melakukan scroll ke bawah hingga semua elemen dimua3
while True:
    # Eksekusi script untuk scroll
    driver.execute_script(scroll_script)
    # Tunggu sejenak agar konten tambahan dimuat
    time.sleep(1)
    # Cek apakah semua elemen yang diinginkan sudah dimuat
    semua_elemen = driver.find_elements(By.CLASS_NAME, "RHo1pe")
    print(len(semua_elemen))
    if len(semua_elemen) >= 3000:
        break

# Cetak semua elemen yang telah diekstrak
import csv

# Menyimpan data ke dalam list of dictionaries
data = []
semua_elemen = driver.find_elements(By.CLASS_NAME, "RHo1pe")
for elemen in semua_elemen:
    nama = elemen.find_element(By.CLASS_NAME, "X5PpBb").text
    tanggal_ulasan = elemen.find_element(By.CLASS_NAME, "bp9Aid").text
    ulasan = elemen.find_element(By.CLASS_NAME, "h3YV2d").text
    try:
        terbantu_element = elemen.find_element(By.CLASS_NAME, "AJTPZc")
        terbantu = terbantu_element.text
    except NoSuchElementException:
        terbantu = None
        continue

    # Rating
    container_rating = elemen.find_element(By.CLASS_NAME, "c1bOId")
    rating = container_rating.find_element(By.CSS_SELECTOR, "div.Jx4nYe > div.iXRFPc")
    rating = rating.get_attribute('aria-label')
    
    try:
        # balasan
        balasan = elemen.find_element(By.CLASS_NAME,'ras4vb').text

        # tanggal balasan
        tanggal_balasan = elemen.find_element(By.CLASS_NAME, "I9Jtec").text
    except NoSuchElementException:
        balasan = "Null"
        tanggal_balasan = "Null"

    data.append({"Nama": nama,  "Ulasan": ulasan, "Tanggal Ulasan": tanggal_ulasan, "Terbantu": terbantu, "Rating": rating, "Balasan": balasan, "Tanggal Balasan": tanggal_balasan})

# Menyimpan data ke dalam file CSV
with open('review_jkn.csv', mode='w', newline='', encoding='utf-8') as file:
    fieldnames = ['Nama', 'Ulasan', 'Tanggal Ulasan','Terbantu', 'Rating', 'Balasan', 'Tanggal Balasan']
    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()
    for item in data:
        writer.writerow(item)

print("Data ulasan telah disimpan dalam file 'review_jkn.csv'.")


# Tutup browser
driver.quit()
