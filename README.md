Automaton-WAF 🛡️️
Deterministik Sonlu Otomat (DFA - Deterministic Finite Automata) ve Biçimsel Dil Teorisi mantığıyla geliştirilmiş, hafif ve yüksek performanslı ters vekil (reverse-proxy) Web Uygulama Güvenlik Duvarı (WAF).

Bu proje, gelen HTTP trafiğini klasik ve hantal RegEx kuralları yerine doğrusal zaman karmaşıklığıyla (O(n)) analiz ederek SQL Injection (SQLi) saldırılarını engeller.

📌 Proje Özellikleri
DFA Tabanlı Durum Makinesi: Kurallar JSON formatında tanımlanır; girdi sembolleri üzerinde durum geçişleri yapılarak kabul durumuna (q_attack) ulaşılıp ulaşılmadığı denetlenir.

Sözcüksel Ayrıştırıcı (Lexical Tokenizer): Ham URL parametrelerini ve POST istek gövdelerini anlamsal belirteçlere (QUOTE, LOGIC_OP, EQUALS, LITERAL) dönüştürür.

Asenkron Ters Vekil (Reverse Proxy): Temiz istekleri httpx üzerinden arkadaki web sunucusuna iletirken, tespit edilen saldırıları doğrudan 403 Forbidden ile bloklar.

Alt Dizi Tarama Desteği (Subsequence Inspection): URL veya parametre içerisindeki herhangi bir konuma gizlenmiş zararlı dizilimleri yakalayabilir.

📐 DFA Durum Geçiş Mimarisi
SQL Injection tespitinde kullanılan durum zinciri:

Plaintext
[q0] -- QUOTE --> [q1] -- LOGIC_OP --> [q2] -- LITERAL --> [q3] -- EQUALS --> [q4] -- LITERAL --> ((q_attack))
q0: Başlangıç durumu (temiz akış)

q1: Tırnak (' veya ") açıldı

q2: Mantıksal operatör (OR, AND, XOR) geldi

q3: Değer/Literatür (1, admin vb.) geldi

q4: Eşittir (=) operatörü geldi

q_attack: Kabul durumu — Saldırı algılandı, istek engellenir!

📁 Proje Dosya Yapısı
Plaintext
automaton-waf/
├── config/
│   └── rules.json          # DFA durumları ve geçiş kuralları
├── core/
│   ├── __init__.py
│   ├── dfa_engine.py       # Durum makinesi yürütme motoru
│   └── tokenizer.py        # Girdi ayrıştırıcı (Lexer)
├── main.py                 # FastAPI reverse proxy ve WAF middleware katmanı
├── requirements.txt        # Gerekli Python paketleri
├── .gitignore              # Git dışlama kuralları
└── README.md               # Proje dokümantasyonu
🚀 Kurulum ve Çalıştırma
1. Depoyu Klonlayın
Bash
git clone https://github.com/keremd0/automaton-waf.git
cd automaton-waf
2. Sanal Ortamı Kurun ve Paketleri Yükleyin
Bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
3. WAF'ı Başlatın
Bash
uvicorn main:app --port 8000
(Varsayılan olarak arkasında [http://127.0.0.1:5000](http://127.0.0.1:5000) portundaki sunucuyu korur).

🧪 Test ve Doğrulama
Test 1: Güvenli İstek (İzin Verilir)
Bash
curl -i "http://127.0.0.1:8000/?id=123"
Yanıt: HTTP/1.1 200 OK (İstek arkadaki sunucuya başarıyla iletilir).

Test 2: SQL Injection Saldırısı (Engellenir)
Bash
curl -i "http://127.0.0.1:8000/?id=%27%20OR%201=1"
Yanıt: HTTP/1.1 403 Forbidden

[!] WAF: Saldiri tespit edildi, gecemezsin!
