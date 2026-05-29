# Project Monyet AI (Interactive Meme Mirroring)

Project ini adalah aplikasi Computer Vision sederhana berbasis Python. Aplikasi ini menggunakan webcam untuk melacak wajah dan pergerakan tangan secara real-time. Jika sistem mendeteksi pengguna menempelkan jari telunjuk ke bagian dagu (pose berpikir), gambar monyet di layar akan merespons dengan berubah dari pose diam menjadi pose berpikir.

## Prasyarat Sistem

* Python versi 3.11 (Wajib menggunakan versi 3.11, karena library MediaPipe belum didukung secara penuh di Python 3.12 atau 3.14).
* Webcam (Kamera laptop bawaan atau eksternal).
* OS Windows.

## Struktur Direktori

Pastikan file di dalam folder project Anda tersusun dengan struktur berikut sebelum menjalankan program. Nama file gambar harus sama persis.

ProjectMonyet/
|-- main.py
|-- idle.jpg
|-- aksi.jpg
|-- README.md

## Instalasi

1. Buka Terminal atau Command Prompt, lalu arahkan ke dalam folder project Anda.
2. Karena menggunakan Python 3.11 (spesifik), instal semua library pendukung menggunakan perintah berikut:

   py -3.11 -m pip install opencv-python mediapipe numpy

## Cara Menjalankan Program

1. Pastikan webcam tidak sedang digunakan oleh aplikasi lain (seperti Zoom, Google Meet, dll).
2. Buka terminal di dalam folder project.
3. Jalankan file utama dengan perintah spesifik versi Python berikut:

   py -3.11 main.py

4. Akan muncul satu jendela aplikasi yang menampilkan kamera Anda di sebelah kiri dan gambar monyet di sebelah kanan.
5. Angkat jari telunjuk Anda dan tempelkan ke dagu. Gambar monyet di kanan akan otomatis berganti.
6. Tekan tombol 'q' pada keyboard untuk mematikan kamera dan keluar dari aplikasi.

## Logika Cara Kerja

Program ini menggunakan library MediaPipe dari Google untuk mendeteksi koordinat (landmark) pada tubuh manusia:
* Landmark Dagu: Program melacak bagian bawah dagu menggunakan Face Mesh (Landmark ID 152).
* Landmark Jari: Program melacak ujung jari telunjuk menggunakan Hands (Landmark ID 8).

Sistem akan menghitung jarak Euclidean (Pythagoras) antara titik dagu dan titik jari telunjuk secara real-time. Jika jarak tersebut dalam piksel kurang dari nilai THRESHOLD_JARAK (default: 60), sistem menganggap ada sentuhan dan memicu perubahan gambar pada layar.

#by wahyuuu
