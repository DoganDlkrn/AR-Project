using UnityEngine;
using TMPro;

public class ZiyaretciSayaci : MonoBehaviour
{
    public TextMeshProUGUI sayacText;
    public TextMeshProUGUI bilgiText;
    public GameObject arayuzPaneli;

    private const string ZiyaretciSayisiAnahtari = "ZiyaretciSayisi";

    private void Start()
    {
        int ziyaretciSayisi = PlayerPrefs.GetInt(ZiyaretciSayisiAnahtari, 0);
        ziyaretciSayisi++;
        PlayerPrefs.SetInt(ZiyaretciSayisiAnahtari, ziyaretciSayisi);
        PlayerPrefs.Save();

        if (sayacText != null)
        {
            sayacText.text = $"Harput'u Kesfeden {ziyaretciSayisi}. Kisisin!";
        }

        if (bilgiText != null)
        {
            bilgiText.text = "Harput Kalesi, Urartular tarafindan M.O. 8. yuzyilda insa edilmistir.";
        }

        if (arayuzPaneli != null)
        {
            arayuzPaneli.SetActive(false);
        }
    }

    public void HedefBulundu()
    {
        if (arayuzPaneli != null)
        {
            arayuzPaneli.SetActive(true);
        }
    }

    public void HedefKayboldu()
    {
        if (arayuzPaneli != null)
        {
            arayuzPaneli.SetActive(false);
        }
    }
}
