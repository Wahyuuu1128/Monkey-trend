import cv2
import mediapipe as mp
import math
import numpy as np
import os

# --- 1. KONFIGURASI FILE & THRESHOLD ---
# Pastikan nama file ini ada di folder
FILE_DIAM = "idle.jpg"
FILE_MIKIR = "aksi.jpg"
FILE_TUNJUK = "tunjuk.jpg"
FILE_MELET = "melet.jpg"

# Threshold (Batas Pemicu) - Boleh diutak-atik nanti
THRESH_MIKIR = 60   # Jarak telunjuk ke dagu (semakin kecil = makin nempel)
THRESH_MELET = 30   # Jarak bukaan mulut (semakin besar = harus mangap lebar)
THRESH_TUNJUK_Y = 50 # Jarak vertikal telunjuk di atas hidung

# Ukuran layar output
LEBAR_LAYAR = 640
TINGGI_LAYAR = 480

# --- 2. SETUP AI ---
print("Menyiapkan AI Multi-Pose...")
mp_hands = mp.solutions.hands
mp_face_mesh = mp.solutions.face_mesh

hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.6)
face_mesh = mp_face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.7, min_tracking_confidence=0.7)

# --- 3. LOAD SEMUA GAMBAR ---
def load_dan_resize(nama_file):
    if not os.path.exists(nama_file):
        print(f"\n[ERROR] File '{nama_file}' tidak ditemukan!")
        exit()
    img = cv2.imread(nama_file)
    return cv2.resize(img, (LEBAR_LAYAR, TINGGI_LAYAR))

print("Memuat galeri monyet...")
monyet_diam = load_dan_resize(FILE_DIAM)
monyet_mikir = load_dan_resize(FILE_MIKIR)
monyet_tunjuk = load_dan_resize(FILE_TUNJUK)
monyet_melet = load_dan_resize(FILE_MELET)

# --- 4. NYALAKAN WEBCAM ---
cap = cv2.VideoCapture(0)
cap.set(3, LEBAR_LAYAR)
cap.set(4, TINGGI_LAYAR)
print("Kamera siap! Coba pose: Mikir, Nunjuk, atau Mangap.")

while cap.isOpened():
    success, frame = cap.read()
    if not success: break

    frame = cv2.flip(frame, 1)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    h, w, _ = frame.shape

    hasil_tangan = hands.process(frame_rgb)
    hasil_wajah = face_mesh.process(frame_rgb)

    # Default Status
    tampilan_monyet = monyet_diam
    pesan_status = "MODE: SANTAI"
    warna_teks = (0, 255, 0)

    # --- LOGIKA DETEKSI MULTI-POSE ---
    # Kita butuh wajah untuk semua pose
    if hasil_wajah.multi_face_landmarks:
        wajah = hasil_wajah.multi_face_landmarks[0]
        
        # AMBIL TITIK-TITIK PENTING WAJAH
        # Dagu (152), Hidung (1), Bibir Atas (13), Bibir Bawah (14)
        pd = wajah.landmark[152]; cx_dagu, cy_dagu = int(pd.x*w), int(pd.y*h)
        ph = wajah.landmark[1];   cx_hidung, cy_hidung = int(ph.x*w), int(ph.y*h)
        pba = wajah.landmark[13]; cx_bibir_a, cy_bibir_a = int(pba.x*w), int(pba.y*h)
        pbb = wajah.landmark[14]; cx_bibir_b, cy_bibir_b = int(pbb.x*w), int(pbb.y*h)

        # Visualisasi Titik Wajah
        cv2.circle(frame, (cx_dagu, cy_dagu), 5, (255,0,0), -1) # Dagu Biru
        cv2.circle(frame, (cx_hidung, cy_hidung), 5, (255,255,0), -1) # Hidung Kuning
        cv2.line(frame, (cx_bibir_a, cy_bibir_a), (cx_bibir_b, cy_bibir_b), (0,255,255), 2) # Garis Mulut

        # 1. CEK POSE MELET (Buka Mulut) - Gak perlu tangan
        jarak_mulut = math.hypot(cx_bibir_a - cx_bibir_b, cy_bibir_a - cy_bibir_b)
        
        if jarak_mulut > THRESH_MELET:
            tampilan_monyet = monyet_melet
            pesan_status = "MODE: MELET! 😛"
            warna_teks = (0, 0, 255)
        
        # 2. CEK POSE TANGAN (Mikir / Nunjuk) - Kalau tangan ada
        elif hasil_tangan.multi_hand_landmarks:
            tangan = hasil_tangan.multi_hand_landmarks[0]
            pt = tangan.landmark[8]; cx_telunjuk, cy_telunjuk = int(pt.x*w), int(pt.y*h)
            
            cv2.circle(frame, (cx_telunjuk, cy_telunjuk), 8, (0,0,255), -1) # Telunjuk Merah

            # Hitung Jarak Telunjuk ke Dagu
            jarak_mikir = math.hypot(cx_dagu - cx_telunjuk, cy_dagu - cy_telunjuk)
            # Hitung Jarak Vertikal Telunjuk ke Hidung (Makin kecil Y = makin tinggi)
            jarak_ver_hidung = cy_hidung - cy_telunjuk

            if jarak_mikir < THRESH_MIKIR:
                tampilan_monyet = monyet_mikir
                pesan_status = "MODE: MIKIR 🤔"
                warna_teks = (0, 0, 255)
                cv2.line(frame, (cx_dagu, cy_dagu), (cx_telunjuk, cy_telunjuk), (255,255,0), 2)

            # Cek Nunjuk: Tangan jauh dari dagu DAN posisinya tinggi di atas hidung
            elif jarak_mikir >= THRESH_MIKIR and jarak_ver_hidung > THRESH_TUNJUK_Y:
                tampilan_monyet = monyet_tunjuk
                pesan_status = "MODE: NUNJUK! ☝️"
                warna_teks = (0, 0, 255)
                cv2.line(frame, (cx_hidung, cy_hidung), (cx_telunjuk, cy_telunjuk), (0,255,0), 2)

    # Tampilan Akhir
    cv2.putText(frame, pesan_status, (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 1.5, warna_teks, 3)
    layar_gabungan = np.hstack((frame, tampilan_monyet))
    cv2.imshow('Project Monyet AI V2', layar_gabungan)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()