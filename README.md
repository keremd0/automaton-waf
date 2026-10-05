# Automaton-WAF 🛡️

Deterministik Sonlu Otomat (DFA - Deterministic Finite Automata) ve Biçimsel Dil Teorisi mantığıyla geliştirilmiş, hafif ve yüksek performanslı ters vekil (reverse-proxy) Web Uygulama Güvenlik Duvarı (WAF).

Bu proje, gelen HTTP trafiğini klasik ve hantal RegEx kuralları yerine doğrusal zaman karmaşıklığıyla (O(n)) analiz ederek SQL Injection (SQLi) saldırılarını engeller.

---

## 📌 Proje Özellikleri

- **DFA Tabanlı Durum Makinesi:** Kurallar JSON formatında tanımlanır; girdi sembolleri üzerinde durum geçişleri yapılarak kabul durumuna (`q_attack`) ulaşılıp ulaşılmadığı denetlenir.
- **Sözcüksel Ayrıştırıcı (Lexical Tokenizer):** Ham URL parametrelerini ve POST istek gövdelerini anlamsal belirteçlere (`QUOTE`, `LOGIC_OP`, `EQUALS`, `LITERAL`) dönüştürür.
- **Asenkron Ters Vekil (Reverse Proxy):** Temiz istekleri `httpx` üzerinden arkadaki web sunucusuna iletirken, tespit edilen saldırıları doğrudan `403 Forbidden` ile bloklar.
- **Alt Dizi Tarama Desteği (Subsequence Inspection):** URL veya parametre içerisindeki herhangi bir konuma gizlenmiş zararlı dizilimleri yakalayabilir.

---

## 📐 DFA Durum Geçiş Mimarisi

SQL Injection tespitinde kullanılan durum zinciri:

```text
[q0] -- QUOTE --> [q1] -- LOGIC_OP --> [q2] -- LITERAL --> [q3] -- EQUALS --> [q4] -- LITERAL --> ((q_attack))
