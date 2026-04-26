using System;
using System.Collections;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

/// <summary>
/// Harput Kalesi AR Zaman Portalı için UI yönetim sınıfı.
/// - Ana menü <-> AR modu panel geçişlerini CanvasGroup ile fade animasyonlu yapar.
/// - PlayerPrefs ile ziyaretçi sayısını tutar ve ekranda gösterir.
/// - AR yönlendirme metnini şık bir şekilde yanıp söndürür.
/// - Vuforia hedef durumuna göre yönlendirme metnini aç/kapat yapar.
/// </summary>
public class UIManager : MonoBehaviour
{
    [Header("Panel Referansları (CanvasGroup)")]
    [SerializeField] private CanvasGroup AnaMenuPaneli;
    [SerializeField] private CanvasGroup ARModuPaneli;

    [Header("Metin Referansları (TMP)")]
    [SerializeField] private TMP_Text ziyaretciSayaciText;
    [SerializeField] private TextMeshProUGUI yonlendirmeMetni;

    [Header("Geçiş Ayarları")]
    [SerializeField] private float panelFadeSuresi = 0.5f;

    [Header("Yönlendirme Metni Ayarları")]
    [SerializeField] private float pingPongHizi = 1.8f;   // Yanıp sönme hızı
    [SerializeField] private float minAlpha = 0.25f;      // En düşük görünürlük
    [SerializeField] private float maxAlpha = 1f;         // En yüksek görünürlük

    private Coroutine panelGecisCoroutine;
    private bool arModunda = false;
    private bool hedefBulundu = false;

    private void Start()
    {
        // Uygulama açılır açılmaz dinamik ziyaretçi sayısını ekrana yazdır.
        DinamikZiyaretciSayisiniYazdir();

        // Başlangıç UI durumunu güvenli şekilde kur.
        BaslangicPanelDurumlariniAyarla();

        // AR modu başlangıçta kapalı olduğundan yönlendirme metnini de kapalı başlat.
        YonlendirmeMetniGorunurluguAyarla(false);
    }

    private void Update()
    {
        // Yalnızca AR modundayken ve hedef bulunmamışken yönlendirme metnini yanıp söndür.
        if (arModunda && !hedefBulundu && yonlendirmeMetni != null)
        {
            // 0-1 arası pingpong üret, sonra min-max alpha aralığına taşı.
            float t = Mathf.PingPong(Time.time * pingPongHizi, 1f);
            float alpha = Mathf.Lerp(minAlpha, maxAlpha, t);

            Color c = yonlendirmeMetni.color;
            c.a = alpha;
            yonlendirmeMetni.color = c;
        }
    }

    /// <summary>
    /// "Oyuna Başla" butonunun OnClick event'ine bağlanır.
    /// Ana menüyü fade-out, AR modunu fade-in yapar.
    /// </summary>
    public void OyunaBasla()
    {
        arModunda = true;
        hedefBulundu = false; // AR moduna girildiğinde henüz hedef bulunmamış varsayılır.

        // Geçiş sırasında önce mevcut coroutine'i temizleyerek çakışmaları engelle.
        if (panelGecisCoroutine != null)
            StopCoroutine(panelGecisCoroutine);

        panelGecisCoroutine = StartCoroutine(PanellerArasiGecis(AnaMenuPaneli, ARModuPaneli));

        // AR moduna girince yönlendirme metnini göster.
        YonlendirmeMetniGorunurluguAyarla(true);
    }

    /// <summary>
    /// "Haritayı Aç" butonunun OnClick event'ine bağlanır.
    /// Harput Kalesi konumunu haritada açar.
    /// </summary>
    public void HaritayiAc()
    {
        const string url = "https://www.google.com/maps/search/?api=1&query=Harput+Kalesi";

        try
        {
            Application.OpenURL(url);
        }
        catch (Exception ex)
        {
            // Uygulamanın kırılmaması için hatayı yakalıyoruz.
            Debug.LogError($"[UIManager] Harita açılırken hata oluştu: {ex.Message}");
        }
    }

    /// <summary>
    /// Vuforia hedefi algıladığında çağır.
    /// Örn: Image Target Found event'inden bağlayabilirsin.
    /// </summary>
    public void HedefBulundu()
    {
        hedefBulundu = true;
        YonlendirmeMetniGorunurluguAyarla(false);
    }

    /// <summary>
    /// Vuforia hedefi kaybettiğinde çağır.
    /// Örn: Image Target Lost event'inden bağlayabilirsin.
    /// </summary>
    public void HedefKayboldu()
    {
        hedefBulundu = false;

        // Sadece AR modundayken uyarıyı tekrar aç.
        if (arModunda)
            YonlendirmeMetniGorunurluguAyarla(true);
    }

    #region Yardımcı Metotlar

    /// <summary>
    /// Başlangıçta dinamik bir ziyaretçi sayısı üretip metne yazar.
    /// İleride burası API/Firebase verisiyle değiştirilebilir.
    /// </summary>
    private void DinamikZiyaretciSayisiniYazdir()
    {
        int dinamikSayi = PlayerPrefs.GetInt("ZiyaretciSayisi", 0) + 1;
        PlayerPrefs.SetInt("ZiyaretciSayisi", dinamikSayi);

        if (ziyaretciSayaciText != null)
        {
            ziyaretciSayaciText.text = $"{dinamikSayi:N0} Ziyaretçi";
        }
    }

    /// <summary>
    /// Başlangıç panel görünürlük ve etkileşim ayarları.
    /// </summary>
    private void BaslangicPanelDurumlariniAyarla()
    {
        // Ana menü açık başlasın.
        CanvasGroupDurumAyarla(AnaMenuPaneli, 1f, true, true);

        // AR paneli kapalı başlasın.
        CanvasGroupDurumAyarla(ARModuPaneli, 0f, false, false);
    }

    /// <summary>
    /// İki panel arasında eşzamanlı fade geçiş yapar.
    /// </summary>
    private IEnumerator PanellerArasiGecis(CanvasGroup kapatilacak, CanvasGroup acilacak)
    {
        if (kapatilacak == null || acilacak == null)
            yield break;

        // Açılacak panel etkileşime geçiş sonrasında açılacağı için şimdilik etkileşimi kapalı.
        acilacak.blocksRaycasts = false;
        acilacak.interactable = false;

        float elapsed = 0f;
        float kapatBaslangic = kapatilacak.alpha;
        float acBaslangic = acilacak.alpha;

        while (elapsed < panelFadeSuresi)
        {
            elapsed += Time.deltaTime;
            float t = Mathf.Clamp01(elapsed / panelFadeSuresi);

            // SmoothStep ile daha profesyonel, yumuşak easing.
            float eased = Mathf.SmoothStep(0f, 1f, t);

            kapatilacak.alpha = Mathf.Lerp(kapatBaslangic, 0f, eased);
            acilacak.alpha = Mathf.Lerp(acBaslangic, 1f, eased);

            yield return null;
        }

        // Nihai durumları netleştir.
        CanvasGroupDurumAyarla(kapatilacak, 0f, false, false);
        CanvasGroupDurumAyarla(acilacak, 1f, true, true);

        panelGecisCoroutine = null;
    }

    /// <summary>
    /// CanvasGroup için alpha/etkileşim/raycast ayarlarını tek yerden yönetir.
    /// </summary>
    private void CanvasGroupDurumAyarla(CanvasGroup cg, float alpha, bool interactable, bool blocksRaycasts)
    {
        if (cg == null) return;

        cg.alpha = alpha;
        cg.interactable = interactable;
        cg.blocksRaycasts = blocksRaycasts;
    }

    /// <summary>
    /// Yönlendirme metnini aç/kapat ve alpha başlangıcını düzgün ayarla.
    /// </summary>
    private void YonlendirmeMetniGorunurluguAyarla(bool gorunsun)
    {
        if (yonlendirmeMetni == null) return;

        yonlendirmeMetni.gameObject.SetActive(gorunsun);

        if (gorunsun)
        {
            // Görünür olurken alpha'yı tavandan başlatıp pürüzsüz animasyon sağla.
            Color c = yonlendirmeMetni.color;
            c.a = maxAlpha;
            yonlendirmeMetni.color = c;
        }
    }

    #endregion
}