void setup() {
  // Seri iletişimi başlat
  Serial.begin(9600);
  pinMode(8, OUTPUT);

  // A1 pinini giriş olarak ayarla
  pinMode(A1, INPUT);
}

bool ledAcik = false; // Bayrak değişkeni

void loop() {
  // A1 pininden okunan değeri al
  int sensorValue = analogRead(A1);

  // Eşik değer
  int threshold = 614;  // Yaklaşık 3V

  // Eğer değer eşik değerden büyükse ve bayrak değişkeni false ise
  if (sensorValue > threshold && !ledAcik) {
    Serial.println(1);
    digitalWrite(8, HIGH); 
    ledAcik = true; // Bayrak değişkenini true yap
  }

  // Değer eşik değerden küçükse
  else if (sensorValue < threshold) {
    Serial.println(0);
    digitalWrite(8, LOW); 
    ledAcik = false; // Bayrak değişkenini false yap
  }

  // Biraz bekle
  delay(100);  // Daha sık veri göndermek için bekleme süresini azalttık
}
