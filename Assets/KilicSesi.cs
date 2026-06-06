using UnityEngine;

public class KilicSesi : MonoBehaviour
{
    void OnMouseDown()
    {
        GetComponent<AudioSource>().Play();
    }
}