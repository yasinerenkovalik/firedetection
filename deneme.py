import serial
import time

def send_signal_to_arduino(arduino_port, baud_rate, signal):
    try:
        ser = serial.Serial(arduino_port, baud_rate, timeout=1)
        time.sleep(2)  # Arduino'nun başlaması için biraz bekle
        ser.write(signal.encode())
        print("Arduino'ya sinyal gönderildi:", signal)
        ser.close()
    except serial.SerialException as e:
        print("Arduino'ya bağlanırken bir hata oluştu:", e)

if __name__ == "__main__":
    arduino_port = "/dev/cu.usbserial-130"  # Arduino'nun bağlı olduğu portu belirtin
    baud_rate = 9600  # Arduino kodundaki baud oranı ile aynı olmalı
    signal = '0'  # Arduino'da lambayı yakmak için gönderilecek sinyal

    send_signal_to_arduino(arduino_port, baud_rate, signal)
