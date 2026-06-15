# 🏰 HarputAR — Harput Kalesi Artırılmış Gerçeklik Zaman Portalı

> Harput Kalesi'nin tarihi dokusunu bir **"zaman portalı" illüzyonu** ile yeniden canlandıran,
> Unity + Vuforia + C# ile geliştirilmiş bir **mobil Artırılmış Gerçeklik (AR)** uygulaması.

<p align="left">
  <img alt="Platform" src="https://img.shields.io/badge/Platform-Android-3DDC84">
  <img alt="Engine" src="https://img.shields.io/badge/Unity-6000.4.1f1-000000">
  <img alt="AR" src="https://img.shields.io/badge/Vuforia-11.4.4-2C5D8A">
  <img alt="Language" src="https://img.shields.io/badge/C%23-Script-178600">
</p>

**Fırat Üniversitesi · Teknoloji Fakültesi · Yazılım Mühendisliği Bölümü**
Yazılım Mühendisliğinde Güncel Konular (YMGK) — 2025–2026 Bahar Dönemi Dönem Projesi

---

## 📑 İçindekiler

1. [Proje Hakkında](#-proje-hakkında)
2. [Özellikler](#-özellikler)
3. [Kullanılan Teknolojiler](#-kullanılan-teknolojiler)
4. [Demo Videosu](#-demo-videosu)
5. [Ekran Görüntüleri](#-ekran-görüntüleri)
6. [Hızlı Başlangıç — APK ile Telefona Kurulum](#-hızlı-başlangıç--apk-ile-telefona-kurulum-son-kullanıcı)
7. [Geliştirici Kurulumu (Unity'de Açma ve Derleme)](#-geliştirici-kurulumu-unityde-açma-ve-derleme)
8. [Proje Yapısı](#-proje-yapısı)
9. [Dokümantasyon](#-dokümantasyon)
10. [Proje Yönetimi (Trello)](#-proje-yönetimi-trello)
11. [Ekip ve Sorumluluklar](#-ekip-ve-sorumluluklar)
12. [İletişim](#-i̇letişim)

---

## 🎯 Proje Hakkında

**HarputAR**, Harput Kalesi'ni ziyaret eden turistlere, fiziksel bir görsel hedef (kale tanıtım
görseli) üzerinden tetiklenen sürükleyici bir AR deneyimi sunar. Kullanıcı kamerasını hedefe
tuttuğunda, gerçek dünyanın üzerinde bir **"zaman portalı"** açılır ve içeride kalenin tarihi
sahnesi belirir. Uygulama yalnızca görsel bir şov değildir; **ziyaretçi sayacı** ve **Google
Haritalar yönlendirmesi** gibi fonksiyonlarla aynı zamanda pratik bir dijital rehberdir.

Uygulamanın çekirdek deneyimi **internet bağlantısı olmadan (Offline-First)** çalışır; bu da onu
açık alandaki kale gezileri için güvenilir kılar.

## ✨ Özellikler

- 🕳️ **Zaman Portalı İllüzyonu** — Özel derinlik maskesi shader'ı (`Custom/DepthMaskURP`) ile
  gerçek duvarda açılmış bir geçit hissi.
- 🎯 **Görüntü Hedefli AR Takibi** — Vuforia ile `harput_kalesi` hedefinin gerçek zamanlı tanınması.
- 🏛️ **3B Tarihi Sahne** — Düşük poligonlu modeller, özel ışıklandırma ve animasyonlu karakter.
- 🔊 **Ses Etkileşimi** — Sahnedeki nesneye dokununca çalan efekt sesi.
- 👥 **Ziyaretçi Sayacı** — Cihazda kalıcı (PlayerPrefs) ziyaretçi sayımı ve kişiselleştirilmiş mesaj.
- 🗺️ **Google Haritalar Yönlendirmesi** — Tek dokunuşla Harput Kalesi konumuna yol tarifi.
- 🛡️ **Güvenlik Uyarıları** — Deneyim sırasında fiziksel güvenlik için ekran uyarıları.
- 📴 **Offline-First** — Çekirdek AR deneyimi internetsiz çalışır.

## 🧩 Kullanılan Teknolojiler

| Katman | Teknoloji |
|---|---|
| Oyun/Render Motoru | **Unity 6000.4.1f1** (Universal Render Pipeline – URP) |
| AR Altyapısı | **Vuforia Engine 11.4.4** (Image Target: `harput_kalesi`) |
| Programlama Dili | **C#** |
| 3B & Görsel | Düşük poligonlu modeller, özel `DepthMaskShader`, TextMeshPro |
| Konum Servisi | Google Haritalar (URL yönlendirme) |
| Sürüm Kontrol | Git / GitHub |
| Proje Yönetimi | Trello (Kanban: To Do / Doing / Done) |
| Hedef Platform | Android (APK) |

## 🎬 Demo Videosu

Uygulamanın gerçek bir cihazdaki tanıtımı, deponun ana dizinindeki demo videosundadır:

➡️ **[`Demo_video.mp4`](Demo_video.mp4)**  (alternatif ad: [`220541061_Doğan_DALKIRAN.mp4`](220541061_Do%C4%9Fan_DALKIRAN.mp4))

> 💡 Video veya APK dosyası 100 MB'ı aşıyorsa GitHub doğrudan yüklemeyi engeller. Bu durumda dosyayı
> **GitHub Releases** üzerinden ekleyin (aşağıdaki [Releases notuna](#-hızlı-başlangıç--apk-ile-telefona-kurulum-son-kullanıcı) bakın).

## 📸 Ekran Görüntüleri

> İsteğe bağlı: Aşağıdaki tabloya kendi ekran görüntülerinizi ekleyebilirsiniz.

| Ana Menü | Zaman Portalı | Harita Yönlendirme |
|---|---|---|
| _ekran görüntüsü_ | _ekran görüntüsü_ | _ekran görüntüsü_ |

---

## 📲 Hızlı Başlangıç — APK ile Telefona Kurulum (Son Kullanıcı)

> Bu bölüm, **konuyu hiç bilmeyen** bir kullanıcının bile uygulamayı adım adım çalıştırabilmesi
> için yazılmıştır. Yalnızca bir Android telefon yeterlidir.

1. **APK'yı indirin.** Bilgisayardan veya telefondan aşağıdaki bağlantıya tıklayın:
   - 👉 **Doğrudan indirme:** [`HarputAR.apk`](https://github.com/DoganDlkrn/AR-Project/raw/main/HarputAR.apk)
   - (Alternatif) GitHub deposundaki **`HarputAR.apk`** dosyasına tıklayıp **Download** deyin.
2. **Dosyayı telefona aktarın** (bilgisayardan indirdiyseniz USB kablo veya bir bulut ile telefona kopyalayın).
3. **"Bilinmeyen kaynaklar"a izin verin.** Telefonda APK'ya dokunduğunuzda Android, güvenlik için
   izin isteyecektir:
   `Ayarlar → Uygulamalar → Özel uygulama erişimi → Bilinmeyen uygulamaları yükle` yolundan,
   kullandığınız tarayıcıya/dosya yöneticisine izin verin.
4. **Kurulumu tamamlayın.** APK dosyasına dokunup **"Yükle"** deyin, kurulum bitince **"Aç"**a basın.
5. **Kamera iznini verin.** Uygulama ilk açılışta kamera izni isteyecektir; **"İzin Ver"**e dokunun.
6. **Güvenlik uyarısını onaylayın** ve **"Başla"** butonuna dokunun.
7. **Kameranızı hedef görsele tutun** (`harput_kalesi` tanıtım görseli). Birkaç saniye içinde
   **zaman portalı** açılacaktır. 🎉
8. Sahnedeki nesnelere dokunarak sesleri duyabilir, **harita butonu** ile kalenin konumuna yol
   tarifi alabilirsiniz.

> **Releases notu (büyük dosyalar için):** APK > 25 MB ise GitHub'ın `Releases` özelliğini kullanmanız
> önerilir: Depo sayfası → **Releases → Draft a new release → APK'yı sürükleyip bırakın → Publish**.
> Ardından buradaki indirme bağlantısını Release'teki dosyanın bağlantısıyla güncelleyin.

## 🛠️ Geliştirici Kurulumu (Unity'de Açma ve Derleme)

Kaynak koddan derlemek isteyenler için:

### Önkoşullar
- **Unity Hub** + **Unity 6000.4.1f1** (URP destekli)
- **Android Build Support** modülü (Unity kurulumunda işaretleyin)
- **Vuforia Engine 11.4.4** paketi *(lisans/boyut nedeniyle depoya dahil edilmemiştir)*

### Adımlar
```bash
# 1) Depoyu klonlayın
git clone https://github.com/DoganDlkrn/AR-Project.git
cd AR-Project
```
2. **Unity Hub → Add** ile klonladığınız klasörü ekleyin ve **6000.4.1f1** sürümüyle açın.
3. **Vuforia Engine paketini ekleyin** (depoya dahil değildir):
   - `Window → Package Manager → + → Add package from tarball...` ile
     `com.ptc.vuforia.engine-11.4.4.tgz` dosyasını seçin **veya**
   - Vuforia geliştirici portalından paketi indirip içe aktarın.
   - Gerekiyorsa `Assets/Resources/VuforiaConfiguration.asset` içine kendi **Vuforia lisans
     anahtarınızı** girin.
4. Ana sahneyi açın: **`Assets/Scenes/HarputPortali.unity`**.
5. **Android'e geçin:** `File → Build Settings → Android → Switch Platform`.
6. **Derleyin:** `Build` (veya `Build And Run`) ile `HarputAR.apk` üretin.

> Not: `Library/`, `Logs/`, `Build/` ve büyük Vuforia `.tgz` paketi `.gitignore` ile hariç
> tutulmuştur; bunlar Unity tarafından yeniden üretilir.

## 📁 Proje Yapısı

```
AR-Project/
├── Assets/
│   ├── Scenes/HarputPortali.unity      # Ana AR sahnesi
│   ├── UIManager.cs                    # Menü/AR panel geçişleri, harita, hedef olayları
│   ├── ZiyaretciSayaci.cs              # Ziyaretçi sayacı (PlayerPrefs)
│   ├── KilicSesi.cs                    # Dokunmatik ses etkileşimi
│   ├── IleriGit.cs                     # Karakter animasyon/hareketi
│   ├── DepthMaskShader.shader          # Zaman portalı derinlik maskesi (URP)
│   ├── StreamingAssets/Vuforia/        # Görsel hedef veritabanı (harput_kalesi)
│   └── LowPolyDungeonsLite/            # 3B tarihi sahne modelleri
├── docs/
│   ├── SWOT.pdf                        # SWOT analizi
│   ├── RAMS.pdf                        # RAMS analizi
│   ├── THS_report.pdf                  # Temel Hedefler ve Standartlar raporu
│   ├── Requirements.pdf                # Yazılım gereksinim dokümanı
│   ├── UserScenario.pdf                # Kullanıcı senaryosu
│   └── build_pdfs.py                   # Dokümanları yeniden üreten betik
├── HarputAR.apk                        # Kurulabilir uygulama (Android)
├── 220541061_Doğan_DALKIRAN.mp4        # Demo videosu
├── README.md
└── Trello_link.txt
```

## 📚 Dokümantasyon

| Belge | Açıklama |
|---|---|
| [SWOT.pdf](docs/SWOT.pdf) | Güçlü/zayıf yönler, fırsatlar, tehditler ve TOWS stratejileri |
| [RAMS.pdf](docs/RAMS.pdf) | Reliability, Availability, Maintainability, Safety analizi + metrikler |
| [THS_report.pdf](docs/THS_report.pdf) | Değerlendirme kriterlerinin puan bazlı karşılanması |
| [Requirements.pdf](docs/Requirements.pdf) | Fonksiyonel ve fonksiyonel olmayan gereksinimler (SRS) |
| [UserScenario.pdf](docs/UserScenario.pdf) | Turistin uçtan uca adım adım deneyimi |

## 📋 Proje Yönetimi (Trello)

Proje, Çevik (Agile) metodoloji ile Trello Kanban panosu üzerinden yönetilmiştir:

🔗 **https://trello.com/b/IIbc50hT/yazilim-muhendisligi-guncel-konular-ar**

## 👥 Ekip ve Sorumluluklar

| Öğrenci No | Ad Soyad | Rol / Sorumluluk | Katkı |
|---|---|---|---|
| 220541061 | **Doğan DALKIRAN** | AR geliştirme, Unity/Vuforia entegrasyonu, UI, ses ve harita modülleri, dokümantasyon | %100 |

> Proje bir ekip ile yapıldıysa, diğer üyelerin **öğrenci numarası, adı soyadı ve ölçülebilir
> sorumlulukları** bu tabloya eklenmelidir (ders kriteri gereği zorunludur).

## 📨 İletişim

- **GitHub:** [DoganDlkrn/AR-Project](https://github.com/DoganDlkrn/AR-Project)
- **Geliştirici:** Doğan DALKIRAN — 220541061

---

<p align="center"><i>Harput'un tarihini, geleceğin teknolojisiyle keşfedin.</i> 🏰✨</p>
