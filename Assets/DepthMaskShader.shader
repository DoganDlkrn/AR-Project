Shader "Custom/DepthMaskURP" {
    SubShader {
        // Obje diğer her şeyden önce çizilmeli ve URP'ye tanıtılmalı
        Tags {"Queue" = "Geometry-10" "RenderType" = "Opaque" "RenderPipeline" = "UniversalPipeline" }
        
        Pass {
            // Renkleri yut, sadece derinlik (delik) bırak
            Blend Zero One
            ZWrite On
            ColorMask 0
        }
    }
}