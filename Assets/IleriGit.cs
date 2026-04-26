using UnityEngine;

public class IleriGit : MonoBehaviour
{
    public float hiz = 0.5f;
    public float maxMesafe = 0.3f;
    private float yurumulenMesafe = 0f;
    private Animator animator;

    void Start()
    {
        animator = GetComponent<Animator>();
    }

    void Update()
    {
        if (yurumulenMesafe < maxMesafe)
        {
            float adim = hiz * Time.deltaTime;
            transform.Translate(Vector3.forward * adim);
            yurumulenMesafe += adim;
        }
        else
        {
            if (animator != null)
            {
                animator.enabled = false;
            }

            enabled = false;
        }
    }
}