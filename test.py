import cv2

def kamera_goster():
    # Kamera yakalaması başlatılıyor
    cap = cv2.VideoCapture(1)

    # Kamera yakalaması başarılı mı kontrol ediliyor
    if not cap.isOpened():
        print("Kamera açılamadı")
        return

    # Kamera yakalaması devam ederken
    while True:
        # Kameradan bir kare yakalanıyor
        ret, frame = cap.read()

        # Kare başarılı bir şekilde yakalandı mı kontrol ediliyor
        if not ret:
            print("Kare alınamadı")
            break

        # Alınan kareyi göster
        cv2.imshow('Kamera', frame)

        # 'q' tuşuna basıldığında döngüyü sonlandır
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Pencereyi kapat
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    kamera_goster()
