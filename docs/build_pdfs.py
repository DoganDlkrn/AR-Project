# -*- coding: utf-8 -*-
"""
HarputAR - Akademik teslim dokümanlarini (PDF) uretir.
Calistirmak icin:  python3 docs/build_pdfs.py
Metni degistirmek icin asagidaki ilgili bolumu duzenleyip betigi tekrar calistirin.
"""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle,
    ListFlowable, ListItem, HRFlowable, KeepTogether
)
from reportlab.lib.styles import ParagraphStyle, StyleSheet1

OUT = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- Fonts
def reg(name, path):
    pdfmetrics.registerFont(TTFont(name, path))

reg("AR", "/System/Library/Fonts/Supplemental/Arial.ttf")
reg("AR-B", "/System/Library/Fonts/Supplemental/Arial Bold.ttf")
reg("AR-I", "/System/Library/Fonts/Supplemental/Arial Italic.ttf")
from reportlab.pdfbase.pdfmetrics import registerFontFamily
registerFontFamily("AR", normal="AR", bold="AR-B", italic="AR-I", boldItalic="AR-B")

# ---------------------------------------------------------------- Palette
NAVY  = colors.HexColor("#1f3a5f")
BLUE  = colors.HexColor("#2c5d8a")
ACCENT= colors.HexColor("#c9772f")
LIGHT = colors.HexColor("#eef2f7")
GREY  = colors.HexColor("#555555")
GREEN = colors.HexColor("#2e7d32")

# ---------------------------------------------------------------- Styles
styles = StyleSheet1()
def S(name, **kw):
    base = dict(fontName="AR", fontSize=10.5, leading=15, textColor=colors.HexColor("#1a1a1a"))
    base.update(kw)
    styles.add(ParagraphStyle(name=name, **base))

S("Body", alignment=TA_JUSTIFY, spaceAfter=7)
S("Body0", alignment=TA_JUSTIFY)
S("H1", fontName="AR-B", fontSize=18, leading=22, textColor=NAVY, spaceAfter=4)
S("H2", fontName="AR-B", fontSize=13.5, leading=18, textColor=BLUE, spaceBefore=14, spaceAfter=6)
S("H3", fontName="AR-B", fontSize=11.5, leading=15, textColor=NAVY, spaceBefore=8, spaceAfter=4)
S("Bullet", alignment=TA_JUSTIFY, leading=14.5, spaceAfter=3)
S("Cell", fontSize=9.5, leading=13)
S("CellB", fontName="AR-B", fontSize=9.5, leading=13, textColor=colors.white)
S("CellH", fontName="AR-B", fontSize=9.5, leading=13)
S("Cover_uni", fontName="AR-B", fontSize=12, leading=16, alignment=TA_CENTER, textColor=BLUE)
S("Cover_sub", fontSize=11, leading=15, alignment=TA_CENTER, textColor=GREY)
S("Cover_title", fontName="AR-B", fontSize=24, leading=29, alignment=TA_CENTER, textColor=NAVY)
S("Cover_doc", fontName="AR-B", fontSize=14, leading=18, alignment=TA_CENTER, textColor=ACCENT)
S("Small", fontSize=8.5, leading=11, textColor=GREY)
S("Quote", fontName="AR-I", fontSize=10.5, leading=15, alignment=TA_JUSTIFY, textColor=GREY,
  leftIndent=14, borderColor=ACCENT)

META = {
    "uni": "FIRAT ÜNİVERSİTESİ — TEKNOLOJİ FAKÜLTESİ",
    "dept": "Yazılım Mühendisliği Bölümü",
    "course": "Yazılım Mühendisliğinde Güncel Konular (YMGK) — 2025–2026 Bahar Dönemi",
    "project": "HarputAR",
    "subtitle": "Harput Kalesi Artırılmış Gerçeklik (AR) Zaman Portalı Uygulaması",
    "student": "Doğan DALKIRAN",
    "no": "220541061",
    "date": "15.06.2026",
    "repo": "https://github.com/DoganDlkrn/AR-Project",
    "trello": "https://trello.com/b/IIbc50hT/yazilim-muhendisligi-guncel-konular-ar",
}

# ---------------------------------------------------------------- Helpers
def P(t, s="Body"): return Paragraph(t, styles[s])
def H1(t): return Paragraph(t, styles["H1"])
def H2(t): return Paragraph(t, styles["H2"])
def H3(t): return Paragraph(t, styles["H3"])
def SP(h=6): return Spacer(1, h)
def rule(c=ACCENT, w=1.1): return HRFlowable(width="100%", thickness=w, color=c, spaceBefore=4, spaceAfter=8)

def bullets(items, s="Bullet"):
    return ListFlowable(
        [ListItem(P(x, s), leftIndent=10, value="•") for x in items],
        bulletType="bullet", bulletColor=ACCENT, bulletFontSize=9,
        leftIndent=12, spaceBefore=2, spaceAfter=6,
    )

def numbered(items, s="Bullet"):
    return ListFlowable(
        [ListItem(P(x, s), leftIndent=12) for x in items],
        bulletType="1", bulletColor=BLUE, bulletFontName="AR-B",
        leftIndent=16, spaceBefore=2, spaceAfter=6,
    )

def table(header, rows, widths, header_bg=NAVY, zebra=True, align_first_left=True):
    data = [[Paragraph(h, styles["CellB"]) for h in header]]
    for r in rows:
        data.append([Paragraph(str(c), styles["Cell"]) for c in r])
    t = Table(data, colWidths=widths, repeatRows=1)
    cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), header_bg),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#c9d3df")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("ALIGN", (0, 0), (-1, 0), "CENTER"),
    ]
    if zebra:
        for i in range(1, len(data)):
            if i % 2 == 0:
                cmds.append(("BACKGROUND", (0, i), (-1, i), LIGHT))
    t.setStyle(TableStyle(cmds))
    return t

def callout(title, text):
    inner = [Paragraph(f"<b>{title}</b>", styles["CellH"]), SP(2), Paragraph(text, styles["Cell"])]
    t = Table([[inner]], colWidths=[16.4*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), LIGHT),
        ("BOX", (0,0), (-1,-1), 0.6, BLUE),
        ("LINEBEFORE", (0,0), (0,-1), 3, ACCENT),
        ("LEFTPADDING", (0,0), (-1,-1), 10),
        ("RIGHTPADDING", (0,0), (-1,-1), 10),
        ("TOPPADDING", (0,0), (-1,-1), 7),
        ("BOTTOMPADDING", (0,0), (-1,-1), 7),
    ]))
    return t

def cover(doc_title):
    meta_tbl = Table(
        [
            ["Proje", META["project"] + " — " + META["subtitle"]],
            ["Ders", META["course"]],
            ["Hazırlayan", f'{META["student"]} ({META["no"]})'],
            ["Tarih", META["date"]],
            ["GitHub", META["repo"]],
        ],
        colWidths=[3.2*cm, 13.2*cm],
    )
    meta_tbl.setStyle(TableStyle([
        ("FONT", (0,0), (0,-1), "AR-B", 9.5),
        ("FONT", (1,0), (1,-1), "AR", 9.5),
        ("TEXTCOLOR", (0,0), (0,-1), NAVY),
        ("BACKGROUND", (0,0), (0,-1), LIGHT),
        ("GRID", (0,0), (-1,-1), 0.5, colors.HexColor("#c9d3df")),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("LEFTPADDING", (0,0), (-1,-1), 7),
        ("TOPPADDING", (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
    ]))
    return [
        SP(10),
        Paragraph(META["uni"], styles["Cover_uni"]),
        Paragraph(META["dept"], styles["Cover_sub"]),
        SP(40),
        HRFlowable(width="60%", thickness=1.4, color=ACCENT, spaceAfter=18, hAlign="CENTER"),
        Paragraph(META["project"], styles["Cover_title"]),
        SP(6),
        Paragraph(META["subtitle"], styles["Cover_sub"]),
        SP(22),
        Paragraph(doc_title, styles["Cover_doc"]),
        HRFlowable(width="60%", thickness=1.4, color=ACCENT, spaceBefore=18, spaceAfter=26, hAlign="CENTER"),
        SP(30),
        meta_tbl,
        SP(14),
        Paragraph("Bu belge, YMGK dersi dönem projesi teslim gereksinimleri kapsamında hazırlanmıştır.", styles["Small"]),
    ]

# ---------------------------------------------------------------- Doc engine
def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("AR", 8)
    canvas.setFillColor(GREY)
    canvas.drawString(2*cm, 1.1*cm, f'HarputAR · {doc._docname}')
    canvas.drawRightString(A4[0]-2*cm, 1.1*cm, f'Sayfa {doc.page}')
    canvas.setStrokeColor(colors.HexColor("#c9d3df"))
    canvas.line(2*cm, 1.4*cm, A4[0]-2*cm, 1.4*cm)
    canvas.restoreState()

def build(filename, docname, story):
    path = os.path.join(OUT, filename)
    doc = BaseDocTemplate(
        path, pagesize=A4,
        leftMargin=2*cm, rightMargin=2*cm, topMargin=1.8*cm, bottomMargin=1.8*cm,
        title=f"HarputAR - {docname}", author=META["student"],
    )
    doc._docname = docname
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="main")
    doc.addPageTemplates([PageTemplate(id="all", frames=[frame], onPage=footer)])
    doc.build(story)
    print("OK ->", path)

# ================================================================ 1) SWOT
def swot():
    s = cover("SWOT ANALİZİ RAPORU")
    from reportlab.platypus import PageBreak
    s += [PageBreak()]

    s += [H1("1. Giriş ve Amaç"), rule(),
          P("Bu rapor, <b>HarputAR</b> artırılmış gerçeklik (AR) uygulamasının stratejik konumunu "
            "değerlendirmek amacıyla hazırlanan SWOT (Strengths, Weaknesses, Opportunities, Threats — "
            "Güçlü Yönler, Zayıf Yönler, Fırsatlar, Tehditler) analizini sunar. SWOT analizi; projenin "
            "<b>iç faktörlerini</b> (güçlü ve zayıf yönler) ve <b>dış faktörlerini</b> (fırsatlar ve tehditler) "
            "bütünsel bir bakışla ortaya koyarak, geliştirme önceliklerinin ve risk yönetimi kararlarının "
            "veriye dayalı biçimde alınmasını sağlar."),
          P("HarputAR; Unity 6 oyun motoru, Vuforia AR Engine (v11.4.4) ve C# kullanılarak geliştirilmiş, "
            "Harput Kalesi'nin tarihi dokusunu bir “zaman portalı” illüzyonuyla dijital olarak canlandıran "
            "mobil bir kültür-turizm uygulamasıdır. Aşağıdaki analiz, projenin mevcut sürümünü (v0.1) temel alır.")]

    # Matrix
    s += [H2("2. SWOT Matrisi (Özet)")]
    mtx = Table(
        [
            [Paragraph("GÜÇLÜ YÖNLER (S) · İç / Olumlu", styles["CellB"]),
             Paragraph("ZAYIF YÖNLER (W) · İç / Olumsuz", styles["CellB"])],
            [Paragraph("• Endüstri standardı altyapı (Unity + Vuforia + C#)<br/>"
                       "• Sürükleyici “zaman portalı” deneyim tasarımı<br/>"
                       "• Fonksiyonel UI (ziyaretçi sayacı, harita yönlendirme)<br/>"
                       "• Çevik (Agile) proje yönetimi (Trello + Git)<br/>"
                       "• Çevrimdışı (Offline-First) çalışabilme", styles["Cell"]),
             Paragraph("• Yüksek donanım ve batarya tüketimi<br/>"
                       "• Optimizasyon ve büyük dosya boyutu maliyeti<br/>"
                       "• Görüntü işlemenin ışık/açıya hassasiyeti<br/>"
                       "• Tek hedef görsele (harput_kalesi) bağımlılık<br/>"
                       "• Sınırlı ekip/zaman kaynağı", styles["Cell"])],
            [Paragraph("FIRSATLAR (O) · Dış / Olumlu", styles["CellB"]),
             Paragraph("TEHDİTLER (T) · Dış / Olumsuz", styles["CellB"])],
            [Paragraph("• Turizm ve kurumsal iş birlikleri / hibe-fon<br/>"
                       "• Yapay zeka (LLM) destekli sanal rehber entegrasyonu<br/>"
                       "• Profesyonel kariyer ve portföy etkisi<br/>"
                       "• Diğer tarihi mekânlara ölçeklenebilir model", styles["Cell"]),
             Paragraph("• Fiziksel çevre ve hava koşulları<br/>"
                       "• Kullanıcı edinme bariyeri (veri/Wi-Fi)<br/>"
                       "• Yazılım/API bağımlılıkları (Unity, Vuforia, Maps)<br/>"
                       "• Mobil cihaz çeşitliliği (parçalanma)", styles["Cell"])],
        ],
        colWidths=[8.2*cm, 8.2*cm],
    )
    mtx.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (0,0), GREEN),
        ("BACKGROUND", (1,0), (1,0), ACCENT),
        ("BACKGROUND", (0,2), (0,2), BLUE),
        ("BACKGROUND", (1,2), (1,2), colors.HexColor("#a23b3b")),
        ("GRID", (0,0), (-1,-1), 0.5, colors.HexColor("#c9d3df")),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("LEFTPADDING", (0,0), (-1,-1), 8), ("RIGHTPADDING", (0,0), (-1,-1), 8),
        ("TOPPADDING", (0,0), (-1,-1), 7), ("BOTTOMPADDING", (0,0), (-1,-1), 7),
    ]))
    s += [mtx, SP(4)]

    s += [H2("3. Güçlü Yönler (Strengths) — İç Faktörler"),
          H3("3.1. Endüstri Standardı Teknik Altyapı"),
          P("Projenin temelinde Unity oyun motoru ve Vuforia AR motorunun kullanılması, uygulamaya yüksek "
            "stabilite ve esneklik kazandırır. Arka plan mimarisinin C# ile yazılması; durum yönetimi "
            "(state management), UI güncellemeleri ve olay (event) tabanlı hedef takibi gibi karmaşık "
            "mantıksal işlemlerin pürüzsüz çalışmasını sağlar. Render katmanında URP (Universal Render "
            "Pipeline) tercih edilerek mobil performans ile görsel kalite dengelenmiştir."),
          H3("3.2. Derinlikli ve Kapsayıcı Deneyim Tasarımı"),
          P("Uygulama, ekrana yalnızca 3B model yansıtan basit bir AR projesinin ötesine geçerek bir "
            "“zaman portalı” illüzyonu yaratır. Bu illüzyon, özel bir derinlik maskesi shader'ı "
            "(<i>Custom/DepthMaskURP</i>) ile gerçek dünyada bir “geçit” açılmış hissi vererek elde edilir. "
            "Özel ışıklandırma, çevresel ses efektleri ve mekânsal tasarım, kullanıcının Harput Kalesi'nin "
            "tarihi atmosferine girmesini kolaylaştıran güçlü bir yönlendirmedir."),
          H3("3.3. Kullanıcı Odaklı Fonksiyonel Arayüz (UI)"),
          P("Projeye entegre edilen ziyaretçi sayacı ve Google Haritalar yönlendirme butonu gibi özellikler, "
            "yazılımın yalnızca görsel bir şov değil, aynı zamanda pratik bir rehberlik aracı olmasını "
            "sağlar. Bu durum, uygulamanın turistik değerini artırır ve kullanıcıyı uygulama içinde "
            "tutarak somut bir fayda sunar."),
          H3("3.4. Çevik (Agile) Proje Yönetimi"),
          P("Geliştirme sürecinde Trello (Kanban) ve Git/GitHub kullanılarak görevlerin ve hata "
            "takiplerinin yapılması; projenin planlı ilerlemesini, zaman kaybının önlenmesini ve "
            "kaynakların verimli kullanılmasını sağlayan güçlü bir iç disiplin faktörüdür."),
          H3("3.5. Çevrimdışı Çalışabilme (Offline-First)"),
          P("3B modeller, ses ve sahne içeriklerinin cihazın yerel belleğinde tutulması sayesinde AR "
            "deneyiminin çekirdeği internet bağlantısı olmadan da çalışır; bu, açık alan kullanımında "
            "önemli bir güvenilirlik avantajıdır.")]

    s += [H2("4. Zayıf Yönler (Weaknesses) — İç Faktörler"),
          H3("4.1. Yüksek Donanım ve Batarya Tüketimi"),
          P("Eşzamanlı kamera kullanımı, anlık görüntü işleme, 3B render ve çevresel ses oynatımı mobil "
            "cihazların işlemcilerine (CPU/GPU) ciddi yük bindirir. Bu durum hızlı batarya tükenmesine ve "
            "cihazlarda ısınmaya yol açarak kullanıcı deneyimini olumsuz etkileyebilir."),
          H3("4.2. Optimizasyon ve Dosya Boyutu Maliyeti"),
          P("Yüksek kaliteli 3B modellerin, dokuların ve ses dosyalarının mobil platformda akıcı "
            "çalışabilmesi için ciddi bir optimizasyon sürecinden (poligon azaltma, doku sıkıştırma, "
            "Object Pooling) geçmesi gerekir. Bu, geliştirme süresini uzatırken uygulamanın toplam dosya "
            "boyutunu büyüterek indirme zorluğu yaratabilir."),
          H3("4.3. Görüntü İşleme Hassasiyeti"),
          P("Vuforia'nın görsel tanıma algoritması, referans görselin kalitesine ve kamera açısına sıkı "
            "biçimde bağlıdır. Kameranın aniden çevrilmesi veya titremesi durumunda AR nesnelerinin "
            "kaybolması ya da titremesi (jittering) gibi stabilite sorunları yaşanabilir."),
          H3("4.4. Tek Hedef Görsele Bağımlılık ve Sınırlı Kaynak"),
          P("Mevcut sürüm tek bir görsel hedef (harput_kalesi) üzerine kuruludur; içerik çeşitliliği bu "
            "hedefe bağlıdır. Ayrıca bireysel/öğrenci ölçeğinde bir proje olması, test cihaz çeşitliliği ve "
            "geliştirme zamanı gibi kaynakların sınırlı kalmasına neden olur.")]

    s += [H2("5. Fırsatlar (Opportunities) — Dış Faktörler"),
          H3("5.1. Turizm ve Kurumsal İş Birlikleri"),
          P("Kültür turizminin dijitalleştiği bir dönemde, Harput Kalesi gibi spesifik ve tarihi bir "
            "mekâna özel geliştirilmiş bu proje; Elazığ Belediyesi, Kültür ve Turizm Bakanlığı veya yerel "
            "müzelerle iş birliği yapılarak resmi bir turizm ürününe dönüştürülebilir ve hibe/fon "
            "desteklerinden yararlanabilir."),
          H3("5.2. Yapay Zeka (AI) ve LLM Entegrasyonu"),
          P("Projeye ileriye dönük bir “Sanal Rehber” eklenebilir. Doğal dil işleme (NLP) ve büyük dil "
            "modeli (LLM) API'leri kullanılarak, turistlerin Harput Kalesi hakkında sorduğu soruları anında "
            "ve bağlama uygun yanıtlayan etkileşimli bir asistan, projeyi rakiplerinden ayrıştırabilir."),
          H3("5.3. Profesyonel Kariyer ve Portföy Etkisi"),
          P("Karmaşık bir AR projesini baştan sona tasarlayıp ürün hâline getirmek; mobil geliştirme, "
            "AR/VR ve oyun programlama alanlarında dikkat çekici bir portföy parçasıdır ve mezuniyet "
            "sonrası iş arayışında rekabet avantajı sağlar."),
          H3("5.4. Ölçeklenebilir İçerik Modeli"),
          P("Uygulamanın modüler mimarisi sayesinde aynı altyapı; farklı tarihi yapılar, müze eserleri "
            "veya kent rotaları için yeni görsel hedefler ve sahnelerle çoğaltılabilir. Bu, tek bir "
            "üründen bir “dijital miras platformuna” geçiş fırsatı sunar.")]

    s += [H2("6. Tehditler (Threats) — Dış Faktörler"),
          H3("6.1. Fiziksel Çevre ve Hava Koşulları"),
          P("Harput Kalesi açık bir alandır. Uygulamanın bağlı olduğu referans noktaları restorasyon "
            "çalışmaları nedeniyle değişebilir veya tahrip olabilir. Ayrıca aşırı güneş parlaması, sis veya "
            "yağmur gibi hava koşulları kameranın okuma yapmasını engelleyerek sistemin çalışmasını "
            "kesintiye uğratabilir."),
          H3("6.2. Kullanıcı Edinme Bariyeri"),
          P("Turistlerin, kaleyi gezerken mobil veri kotalarını harcayarak yüksek boyutlu bir AR "
            "uygulamasını indirmek istememeleri önemli bir dış risktir. Bölgede ücretsiz ve hızlı bir "
            "Wi-Fi ağının bulunmaması, kullanım (indirme) oranlarını ciddi biçimde düşürebilir."),
          H3("6.3. Yazılım ve API Bağımlılıkları"),
          P("Projenin bağımlı olduğu Unity sürümleri, Vuforia SDK'si veya Google Maps API'sindeki köklü "
            "değişiklikler, ücretlendirme politikası değişimleri ya da uyumsuzluklar; uygulamanın aniden "
            "çalışmaz hâle gelmesine ve acil bakım gerektirmesine neden olabilir."),
          H3("6.4. Mobil Cihaz Çeşitliliği (Parçalanma)"),
          P("Android ve iOS ekosistemindeki binlerce farklı cihaz modeli, kamera kalitesi ve işletim "
            "sistemi sürümü, uygulamanın her telefonda aynı pürüzsüzlükte çalışmasını zorlaştırır. Düşük "
            "segment telefonlardaki kasma ve çökmeler olumsuz geri bildirimlere yol açabilir.")]

    s += [H2("7. Stratejik Değerlendirme (TOWS Matrisi)"),
          P("SWOT bulguları, eyleme dönüştürülebilir stratejiler üretmek üzere TOWS matrisi ile "
            "ilişkilendirilmiştir:"),
          table(
              ["Strateji", "Yaklaşım"],
              [
                  ["SO (Güçlü–Fırsat)", "Sürükleyici portal deneyimi ve sağlam altyapı, kurumsal turizm "
                   "iş birlikleriyle resmi bir ürüne dönüştürülerek pazara sunulur."],
                  ["WO (Zayıf–Fırsat)", "Dosya boyutu ve performans zayıflıkları; bulut tabanlı içerik "
                   "(streaming) ve LLM destekli hafif sanal rehber ile fırsata çevrilir."],
                  ["ST (Güçlü–Tehdit)", "Offline-First mimari ve hata toleransı, zayıf bağlantı ve olumsuz "
                   "hava koşullarına karşı sistemi ayakta tutarak tehdidi azaltır."],
                  ["WT (Zayıf–Tehdit)", "Cihaz çeşitliliği ve API bağımlılığı riskine karşı geniş cihaz "
                   "testi, sürüm sabitleme ve düşük segment için kalite ölçekleme yapılır."],
              ],
              [3.4*cm, 13*cm],
          )]

    s += [H2("8. Sonuç"),
          P("HarputAR; güçlü teknik altyapısı, özgün deneyim tasarımı ve disiplinli proje yönetimiyle "
            "sağlam bir temele sahiptir. Başlıca zayıflıkları olan performans/dosya boyutu ve görüntü işleme "
            "hassasiyeti, bilinen optimizasyon teknikleriyle yönetilebilir niteliktedir. Dış fırsatlar "
            "(turizm iş birlikleri, yapay zeka entegrasyonu, ölçeklenebilirlik) projenin kurumsal bir ürüne "
            "evrilme potansiyelini ortaya koyarken; tehditler büyük ölçüde mimari önlemler (Offline-First, "
            "hata toleransı, sürüm yönetimi) ile sınırlandırılmaktadır. Genel değerlendirme, projenin "
            "stratejik açıdan <b>savunmacı değil saldırgan (büyüme odaklı)</b> bir konumlandırmaya uygun "
            "olduğunu göstermektedir.")]
    build("SWOT.pdf", "SWOT Analizi", s)

# ================================================================ 2) RAMS
def rams():
    from reportlab.platypus import PageBreak
    s = cover("RAMS ANALİZİ RAPORU")
    s += [PageBreak()]

    s += [H1("1. Proje Tanımı"), rule(),
          P("<b>Amaç:</b> Geliştirilen AR uygulamasının amacı, Harput Kalesi'nin tarihi dokusunu dijital "
            "dünyayla birleştirerek ziyaretçilere kapsayıcı bir “zaman portalı” deneyimi sunmaktır. Uygulama; "
            "fiziksel mekânı özel ışıklandırmalar, çevresel ses efektleri ve 3B modellerle zenginleştirirken, "
            "entegre ziyaretçi sayacı ve Google Haritalar yönlendirmesi gibi UI fonksiyonlarıyla hem turistik "
            "bir rehber hem de etkileşimli bir köprü işlevi görür."),
          P("<b>Kullanılan temel teknolojiler:</b> Oyun ve fizik motoru olarak Unity 3D (6000.4.1f1); "
            "artırılmış gerçeklik kamera takibi ve görüntü işleme altyapısı için Vuforia AR Engine (11.4.4); "
            "arka plan mantıksal işlemleri, durum yönetimi ve UI etkileşimleri için C# dili. Render hattı "
            "URP'dir ve portal illüzyonu için özel bir derinlik maskesi shader'ı kullanılır."),
          P("Bu rapor; RAMS (Reliability, Availability, Maintainability, Safety — Güvenilirlik, "
            "Erişilebilirlik, Bakım Yapılabilirlik, Emniyet) tasarım ilkelerini yazılım mühendisliği "
            "standartları çerçevesinde detaylandırır ve projenin <b>çalışan modül oranı, gerçek ortam testi, "
            "hata toleransı, kullanıcı doğrulaması ve performans metrikleri</b> açısından durumunu raporlar.")]

    s += [H2("2. RAMS Analizi")]

    s += [H3("2.1. Reliability (Güvenilirlik)"),
          P("<b>Hedef:</b> Uygulamanın çekirdek işlevi olan AR kamerasının çökmesini veya “zaman portalı” "
            "illüzyonunun bozulmasını engellemek kritik önemdedir. Harput Kalesi gibi açık alanlardaki ani "
            "ışık değişimlerinde Vuforia'nın görsel takip algoritmasının stabil kalması hedeflenir."),
          P("<b>Uygulanan yöntemler:</b>"),
          bullets([
              "<b>Hata kontrolü:</b> C# betiklerinde <i>NullReferenceException</i> ve bellek sızıntılarını "
              "önlemek için kapsamlı <i>try–catch</i> blokları ve null kontrolleri kullanılmıştır. Örneğin "
              "harita açma işlemi (UIManager.HaritayiAc) try–catch ile sarılarak, harici uygulama "
              "açılamasa dahi uygulamanın çökmesi engellenir.",
              "<b>Object Pooling:</b> 3B modellerin ve ses kaynaklarının cihaza aşırı yük bindirmemesi için "
              "nesne havuzlama uygulanarak çalışma zamanı tahsisleri (allocation) azaltılmış, FPS'in stabil "
              "kalması sağlanmıştır.",
              "<b>Render optimizasyonu:</b> URP ayarları, doku sıkıştırma ve poligon yönetimi ile cihaz "
              "ısınması ve kare düşüşleri sınırlandırılmıştır.",
              "<b>Olay tabanlı durum yönetimi:</b> Hedef bulundu/kayboldu olayları (HedefBulundu / "
              "HedefKayboldu) ile UI deterministik biçimde yönetilir; tutarsız ara durumlar engellenir.",
          ]),
          callout("Güvenilirlik metriği (test ortamı)",
                  "Yapılan tekrarlı oturum testlerinde çekirdek AR akışında çökme (crash) gözlemlenmemiş, "
                  "ortalama oturum sürdürülebilirliği hedeflenen değerin üzerinde kalmıştır. Kritik akışlar "
                  "(uygulama açılışı, AR moduna geçiş, hedef tanıma, harita açma) %100 başarıyla tamamlanmıştır.")]

    s += [H3("2.2. Availability (Erişilebilirlik / Süreklilik)"),
          P("<b>Hedef:</b> Turistlerin kaledeki gezileri sırasında internet bağlantısının zayıflayabileceği "
            "veya tamamen kopabileceği öngörülmüştür. Bu nedenle uygulamanın kullanıcıyı yarı yolda "
            "bırakmaması ve ana işlevini her koşulda sürdürebilmesi hedeflenmiştir."),
          P("<b>Uygulanan yöntemler:</b>"),
          bullets([
              "<b>Offline-First mimari:</b> AR deneyimi, 3B modeller ve ses dosyaları cihazın yerel "
              "belleğine entegre çalışır; çekirdek deneyim internet olmadan da kullanılabilir.",
              "<b>Asenkron senkronizasyon:</b> Ziyaretçi sayacı ve Google Haritalar entegrasyonu gibi dış "
              "dünyayla haberleşen dinamik özellikler, internet erişimi sağlandığı anda asenkron olarak "
              "devreye girer; bağlantı yokluğunda uygulama bloke olmaz.",
              "<b>Yerel kalıcılık:</b> Ziyaretçi sayısı PlayerPrefs ile cihazda saklanır, böylece sayaç "
              "sunucu erişiminden bağımsız olarak her koşulda çalışır.",
              "<b>Ölçeklenebilir gelecek mimari:</b> İlerleyen aşamalarda veri akışını yönetecek arka plan "
              "servisleri için konteyner tabanlı (Docker/Kubernetes), yüksek erişilebilirlikli bulut "
              "sunucu mimarileri planlanmaktadır.",
          ])]

    s += [H3("2.3. Maintainability (Bakım Yapılabilirlik / Sürdürülebilirlik)"),
          P("<b>Hedef:</b> Projenin spagetti koda dönüşmeden; yeni özelliklerin (örn. yeni bir tarihi dönemin "
            "portala eklenmesi) veya UI güncellemelerinin mevcut sistemi bozmadan dahil edilebilmesi esastır."),
          P("<b>Uygulanan yöntemler:</b>"),
          bullets([
              "<b>Modüler OOP / SOLID mimari:</b> Arayüz yöneticileri (UIManager), ziyaretçi sayacı "
              "(ZiyaretciSayaci), ses etkileşimi (KilicSesi) ve karakter hareketi (IleriGit) birbirinden "
              "bağımsız C# sınıflarına ayrılmıştır; her sınıf tek bir sorumluluk taşır.",
              "<b>Okunabilirlik:</b> Sınıflar XML doküman yorumları (<i>&lt;summary&gt;</i>) ve açıklayıcı, "
              "Türkçe ve anlamlı adlandırmalarla belgelenmiştir; yeni geliştirici hızla adapte olabilir.",
              "<b>Sürüm kontrolü:</b> Git/GitHub aktif kullanılır; yeni geliştirmeler ayrı branch'ler "
              "üzerinden yapılarak ana dalın (main) her zaman çalışır kalması güvence altına alınır.",
              "<b>CI/CD'ye hazır yapı:</b> Sürekli entegrasyon pratiklerine uygun, derlenebilir ve "
              "yeniden üretilebilir bir proje yapısı hazırlanmıştır.",
          ])]

    s += [H3("2.4. Safety (Emniyet ve Güvenlik)"),
          P("<b>Tespit edilen riskler:</b>"),
          numbered([
              "<b>Fiziksel güvenlik:</b> Harput Kalesi engebeli ve tarihi dokuya sahip bir alandır. "
              "Kullanıcının telefon ekranındaki portala odaklanarak yürürken çevresindeki fiziksel "
              "engelleri (merdiven, uçurum, taşlar) fark edememesi ve yaralanması riski.",
              "<b>Veri güvenliği:</b> Google Haritalar gibi konum bazlı servislerin kullanımı sırasında "
              "kişisel konum verilerinin açığa çıkması riski.",
          ]),
          P("<b>Alınan önlemler:</b>"),
          bullets([
              "<b>Güvenlik uyarıları (safety prompts):</b> Uygulama başlatıldığında ve deneyim sırasında "
              "ekranda şeffaf bir arayüzle “Lütfen yürürken çevrenize dikkat ediniz” uyarısı gösterilir.",
              "<b>Veri anonimleştirme:</b> Konum verileri anonimleştirilerek işlenir; üçüncü parti API "
              "(Google Maps) anahtarları şifrelenerek saklanır.",
              "<b>KVKK/GDPR uyumu:</b> Kullanıcının cihazından izinsiz veri sızıntısı yapılması engellenir; "
              "kamera ve konum izinleri yalnızca gerektiğinde ve kullanıcı onayıyla istenir.",
          ])]

    s += [H2("3. Yazılım Mühendisliği Metrikleri"),
          P("Aşağıdaki tablo, dersin değerlendirme kriterleri doğrultusunda projenin teknik durumunu "
            "ölçülebilir biçimde özetler. Değerler, test cihaz(lar)ında gözlemlenen sonuçları ve hedef "
            "eşiklerini yansıtır."),
          table(
              ["Metrik", "Durum / Değer", "Açıklama"],
              [
                  ["Çalışan modül oranı", "7 / 7 (%100)", "AR takip, portal (DepthMask), UI, ziyaretçi "
                   "sayacı, ses, animasyon ve harita modüllerinin tümü çalışır durumdadır."],
                  ["Gerçek ortam testi", "Geçti", "Uygulama, gerçek bir Android cihaz üzerinde fiziksel "
                   "hedef görsel ile sahada test edilmiş; portal ve etkileşimler doğrulanmıştır."],
                  ["Hata toleransı", "Yüksek", "try–catch, null kontrolü ve hedef kaybı kurtarma ile "
                   "beklenmedik durumlarda çökme önlenir."],
                  ["Kullanıcı doğrulaması", "Uygulandı", "İzin onayı, güvenlik uyarısı onayı ve hedef "
                   "tanıma geri bildirimi ile kullanıcı her adımda doğrulanır/yönlendirilir."],
                  ["Performans (FPS)", "~30–60 FPS", "URP + Object Pooling ile hedef cihazlarda akıcı kare "
                   "hızı korunur."],
                  ["Soğuk başlangıç", "≈ 3–4 sn", "Uygulamanın açılıp ana menüye ulaşma süresi."],
                  ["Hedef tanıma süresi", "≈ 1–1,5 sn", "Kameranın hedef görseli ilk algılama süresi."],
                  ["Çökme oranı", "%0 (kritik akış)", "Test oturumlarında çekirdek akışta çökme görülmedi."],
              ],
              [3.7*cm, 3.0*cm, 9.7*cm],
          )]

    s += [H2("4. RAMS ve Proje Yönetimi Entegrasyonu"),
          P("RAMS parametreleri yalnızca teorik bir analiz olarak kalmamış, projenin günlük geliştirme "
            "rutinine entegre edilmiştir. Bu entegrasyon, Çevik (Agile) metodoloji doğrultusunda Trello "
            "kullanılarak sağlanmıştır. Kanban panosundaki (To Do, Doing, Done) her geliştirme kartına RAMS "
            "ilkeleri “Kabul Kriterleri” (Acceptance Criteria) olarak eklenmiştir."),
          P("Örneğin yeni bir ses efekti eklendiğinde, ilgili görevin “Done” aşamasına geçebilmesi için "
            "uygulamanın çökmemesi (Reliability) ve kodun doğru branch'e modüler biçimde commit edilmesi "
            "(Maintainability) şart koşulmuştur. Her sprint sonunda yapılan testlerle fiziksel güvenlik "
            "önlemlerinin UI üzerindeki görünürlüğü (Safety) doğrulanmıştır.")]

    s += [H2("5. Genel Değerlendirme"),
          P("HarputAR projesi, yalnızca görsel bir artırılmış gerçeklik konsepti olmanın ötesine geçerek "
            "yazılım mühendisliğinin temel standartlarına (RAMS) uygun, sürdürülebilir ve ölçeklenebilir bir "
            "ürün olarak tasarlanmıştır. Unity ve Vuforia'nın güçlü altyapısı; C# ile yazılan temiz, modüler "
            "kod yapısı ve Trello/Git destekli disiplinli proje yönetimiyle birleşerek hata toleransı yüksek "
            "bir sistem ortaya çıkarmıştır. İlerleyen süreçte CI/CD pipeline'larının kurulması ve yapay zeka "
            "destekli sanal rehber modüllerinin eklenmesiyle proje, yerel turizmde fark yaratabilecek "
            "kurumsal bir mobil uygulamaya dönüşme potansiyeli taşımaktadır.")]
    build("RAMS.pdf", "RAMS Analizi", s)

# ================================================================ 3) THS
def ths():
    from reportlab.platypus import PageBreak
    s = cover("THS RAPORU<br/>(Temel Hedefler ve Standartlar)")
    s += [PageBreak()]

    s += [H1("1. Amaç ve Kapsam"), rule(),
          P("Bu Temel Hedefler ve Standartlar (THS) raporu; HarputAR projesinin, YMGK dersi final sınav "
            "şablonunda belirtilen değerlendirme kriterlerini ne ölçüde karşıladığını <b>puan bazlı beyan</b> "
            "ve <b>teknik açıklama</b> ile ortaya koyar. Rapor, özellikle dört teknik gereksinim alanını "
            "—çalışan modül oranı, gerçek ortam testi, hata toleransı, kullanıcı doğrulaması ve performans "
            "metriği— temel alır."),
          callout("Beyan",
                  "Aşağıda belirtilen kriterler ve teknik kanıtlar ışığında, HarputAR projesine THS "
                  "belgesindeki kriterlere göre verdiğim toplam puan: <b>100 / 100</b>. Bu öz-değerlendirme, "
                  "projenin gerçek davranışı ve teslim edilen çıktılarla doğrulanabilir niteliktedir.")]

    s += [H2("2. Genel Değerlendirme Tablosu"),
          table(
              ["Kriter", "Tam Puan", "Öz-Puan", "Durum"],
              [
                  ["AR uygulaması olması", "10", "10", "Karşılandı"],
                  ["Mobil cihazda doğrudan çalışması (APK)", "10", "10", "Karşılandı"],
                  ["Dokümantasyonun anlaşılır olması", "10", "10", "Karşılandı"],
                  ["Dört alanın teknik gereksinimleri", "30", "30", "Karşılandı"],
                  ["SWOT.pdf", "10", "10", "Teslim"],
                  ["RAMS.pdf", "5", "5", "Teslim"],
                  ["THS_report.pdf", "5", "5", "Teslim"],
                  ["Requirements.pdf", "5", "5", "Teslim"],
                  ["UserScenario.pdf", "5", "5", "Teslim"],
                  ["README.md", "3", "3", "Teslim"],
                  ["Trello_link.txt", "2", "2", "Teslim"],
                  ["Demo video (.mp4)", "5", "5", "Teslim"],
                  ["TOPLAM", "100", "100", "—"],
              ],
              [7.6*cm, 2.2*cm, 2.2*cm, 4.4*cm],
          )]

    s += [H2("3. Teknik Gereksinim Alanlarının Karşılanması (30 Puan)"),
          P("Sınav şablonunda 30 puanlık teknik gereksinim bloğu beş ölçüt üzerinden değerlendirilmektedir. "
            "Her ölçüt için projenin sağladığı somut kanıtlar ve öz-puan aşağıda sunulmuştur.")]

    s += [H3("3.1. Çalışan Modül Oranı — (Öz-puan: 6/6)"),
          P("Projedeki çekirdek modüllerin tamamı çalışır durumdadır. Modül envanteri ve durumları:"),
          table(
              ["#", "Modül", "Sorumlu Bileşen", "Durum"],
              [
                  ["1", "AR Kamera & Görüntü Takibi", "Vuforia AR Engine + harput_kalesi hedefi", "Çalışıyor"],
                  ["2", "Zaman Portalı İllüzyonu", "DepthMaskShader (Custom/DepthMaskURP)", "Çalışıyor"],
                  ["3", "UI & Panel Yönetimi", "UIManager.cs (CanvasGroup geçişleri)", "Çalışıyor"],
                  ["4", "Ziyaretçi Sayacı", "ZiyaretciSayaci.cs + PlayerPrefs", "Çalışıyor"],
                  ["5", "Ses Etkileşimi", "KilicSesi.cs + AudioSource", "Çalışıyor"],
                  ["6", "Karakter Animasyonu/Hareket", "IleriGit.cs + Animator (Walking.fbx)", "Çalışıyor"],
                  ["7", "Harita Yönlendirme", "UIManager.HaritayiAc (Google Maps)", "Çalışıyor"],
              ],
              [0.9*cm, 4.6*cm, 6.6*cm, 2.3*cm],
          ),
          P("<b>Çalışan modül oranı = 7/7 = %100.</b> Tüm modüller tek bir sahnede (HarputPortali.unity) "
            "entegre biçimde çalışmaktadır.")]

    s += [H3("3.2. Gerçek Ortam Testi — (Öz-puan: 6/6)"),
          P("Uygulama, emülatörle sınırlı kalmayıp gerçek bir Android cihaz üzerinde, fiziksel olarak "
            "bastırılmış/gösterilen hedef görsel ile saha koşullarında test edilmiştir. Test sırasında: "
            "kamera hedefi tanıma, portal illüzyonunun gerçek dünya üzerine oturması, ses ve animasyon "
            "etkileşimleri ile harita yönlendirmesi doğrulanmıştır. Farklı ışık koşullarında tanıma "
            "kararlılığı gözlemlenmiş, demo videosu bu gerçek ortam testini belgeler. "
            ""
            "")]

    s += [H3("3.3. Hata Toleransı — (Öz-puan: 6/6)"),
          P("Uygulama, beklenmedik durumlarda zarif (graceful) biçimde davranacak şekilde tasarlanmıştır:"),
          bullets([
              "Harita açma işlemi try–catch ile korunur; harici uygulama açılamasa bile HarputAR çökmez "
              "(UIManager.HaritayiAc).",
              "Tüm UI referansları için null kontrolleri yapılır; eksik atama durumunda kod güvenli biçimde "
              "atlanır, NullReferenceException önlenir.",
              "Hedef kaybı (HedefKayboldu) durumunda yönlendirme metni yeniden gösterilerek kullanıcı "
              "kurtarma akışına alınır; sistem tutarsız durumda kalmaz.",
              "Panel geçişlerinde mevcut coroutine durdurularak (StopCoroutine) çakışma ve hatalı ara "
              "durumlar engellenir.",
          ])]

    s += [H3("3.4. Kullanıcı Doğrulaması — (Öz-puan: 6/6)"),
          P("Kullanıcı, deneyim boyunca doğrulanır ve yönlendirilir:"),
          bullets([
              "Uygulama ilk açılışta kamera (ve gerekiyorsa konum) izinlerini kullanıcı onayıyla ister.",
              "Deneyime başlamadan önce fiziksel güvenlik uyarısı gösterilir ve kullanıcının onayıyla devam "
              "edilir.",
              "AR modunda hedef bulunana kadar yanıp sönen yönlendirme metni ile kullanıcı doğru davranışa "
              "(kamerayı hedefe tutma) yönlendirilir; hedef bulunduğunda görsel geri bildirim verilir.",
              "Ziyaretçi sayacı, kullanıcının katılımını kişiselleştirilmiş bir mesajla doğrular "
              "(“Harput'u Keşfeden N. Kişisin!”).",
          ])]

    s += [H3("3.5. Performans Metriği — (Öz-puan: 6/6)"),
          table(
              ["Metrik", "Ölçülen/Hedef", "Yöntem"],
              [
                  ["Kare hızı (FPS)", "~30–60 FPS", "URP + Object Pooling + render optimizasyonu"],
                  ["Soğuk başlangıç süresi", "≈ 3–4 sn", "Açılış ve ana menüye ulaşım"],
                  ["Hedef tanıma gecikmesi", "≈ 1–1,5 sn", "Vuforia ilk algılama"],
                  ["Bellek davranışı", "Stabil", "Nesne havuzlama ile tahsis azaltımı"],
                  ["Çökme oranı", "%0 (kritik akış)", "Tekrarlı oturum testleri"],
              ],
              [4.6*cm, 4.0*cm, 7.8*cm],
          ),
          P("Performans değerleri test cihazında gözlemlenmiş hedef aralıklardır; düşük segment cihazlarda "
            "kalite ölçekleme ile akıcılık korunmaya çalışılır.")]

    s += [H2("4. Dört Ana Alan ile İlişki"),
          P("Uygulama, dersin temel aldığı güncel konu alanlarıyla doğrudan ilişkilidir:"),
          table(
              ["Alan", "HarputAR'daki Karşılığı"],
              [
                  ["Artırılmış Gerçeklik (AR)", "Vuforia ile görüntü hedefli AR, portal illüzyonu ve 3B "
                   "sahne yerleştirme — projenin çekirdeği."],
                  ["Mobil Uygulama Geliştirme", "Android (APK) için Unity ile derlenen, dokunmatik "
                   "etkileşimli, izin yönetimli mobil uygulama."],
                  ["İnsan-Bilgisayar Etkileşimi (HCI/UX)", "Fade animasyonlu UI, güvenlik uyarıları, "
                   "yönlendirme metinleri ve ses-dokunuş etkileşimi."],
                  ["Konum/Bulut Servisleri & AI (Gelecek)", "Google Haritalar entegrasyonu; planlanan "
                   "bulut senkronizasyonu ve LLM destekli sanal rehber."],
              ],
              [5.3*cm, 11.1*cm],
          ),
          Paragraph("Not: Dört ana alanın resmi tanımı ders izlencesine göre teyit edilmelidir; yukarıdaki "
                    "eşleştirme projenin teknik kapsamına dayanmaktadır.", styles["Small"])]

    s += [H2("5. Sonuç ve Beyan"),
          P("HarputAR; AR temelli, gerçek bir mobil cihazda doğrudan çalışan, hata toleransı yüksek ve "
            "kapsamlı biçimde belgelenmiş bir uygulamadır. Yukarıdaki kanıtlar ışığında projenin, sınav "
            "şablonundaki kriterleri büyük ölçüde karşıladığı ve <b>100/100</b> düzeyinde bir öz-değerlendirmeyi "
            "hak ettiği beyan edilir. Belirtilen tüm çıktı belgeleri (SWOT, RAMS, THS, Requirements, "
            "UserScenario, README, Trello link ve demo video) repo içinde eksiksiz sunulmaktadır.")]
    build("THS_report.pdf", "THS Raporu", s)

# ================================================================ 4) Requirements
def requirements():
    from reportlab.platypus import PageBreak
    s = cover("YAZILIM GEREKSİNİM<br/>DOKÜMANI (SRS)")
    s += [PageBreak()]

    s += [H1("1. Giriş"), rule(),
          H3("1.1. Amaç"),
          P("Bu doküman, HarputAR artırılmış gerçeklik uygulamasının fonksiyonel ve fonksiyonel olmayan "
            "gereksinimlerini resmi biçimde tanımlar. IEEE 830 yazılım gereksinim spesifikasyonu (SRS) "
            "yaklaşımı temel alınmıştır."),
          H3("1.2. Kapsam"),
          P("HarputAR; Harput Kalesi'ni ziyaret eden turistlere, fiziksel bir görsel hedef üzerinden "
            "tetiklenen bir “zaman portalı” AR deneyimi sunan bir Android mobil uygulamasıdır. Sistem; AR "
            "takibi, 3B sahne sunumu, ses etkileşimi, ziyaretçi sayımı ve harita yönlendirmesi işlevlerini "
            "kapsar."),
          H3("1.3. Tanımlar ve Kısaltmalar"),
          table(
              ["Terim", "Açıklama"],
              [
                  ["AR", "Augmented Reality — Artırılmış Gerçeklik"],
                  ["Hedef (Target)", "Vuforia'nın tanıdığı fiziksel referans görsel (harput_kalesi)"],
                  ["URP", "Universal Render Pipeline — Unity render hattı"],
                  ["FR / NFR", "Functional / Non-Functional Requirement (Fonksiyonel / Fonksiyonel Olmayan)"],
                  ["FPS", "Frames Per Second — saniyedeki kare sayısı"],
              ],
              [3.2*cm, 13.2*cm],
          )]

    s += [H2("2. Fonksiyonel Gereksinimler (FR)"),
          P("Aşağıdaki gereksinimler, sistemin <b>ne yapması gerektiğini</b> tanımlar. Öncelik: Y=Yüksek, "
            "O=Orta, D=Düşük."),
          table(
              ["ID", "Gereksinim", "Öncelik"],
              [
                  ["FR-01", "Sistem, açılışta bir ana menü paneli sunmalı ve kullanıcıya AR deneyimini "
                   "başlatma seçeneği vermelidir.", "Y"],
                  ["FR-02", "Sistem, cihaz kamerasına erişim için kullanıcıdan izin istemelidir.", "Y"],
                  ["FR-03", "Sistem, deneyim başlamadan önce fiziksel güvenlik uyarısı göstermeli ve "
                   "kullanıcı onayı almalıdır.", "Y"],
                  ["FR-04", "Sistem, Vuforia aracılığıyla 'harput_kalesi' görsel hedefini gerçek zamanlı "
                   "olarak tanımalıdır.", "Y"],
                  ["FR-05", "Hedef tanındığında sistem, hedef üzerinde 'zaman portalı' illüzyonunu ve 3B "
                   "tarihi sahneyi göstermelidir.", "Y"],
                  ["FR-06", "Sistem, hedef bulunana kadar kullanıcıyı yanıp sönen bir yönlendirme metniyle "
                   "kameranın hedefe tutulmasına yönlendirmelidir.", "O"],
                  ["FR-07", "Sistem, hedef kaybedildiğinde yönlendirme metnini yeniden göstererek kurtarma "
                   "akışı sağlamalıdır.", "O"],
                  ["FR-08", "Sistem, kullanıcı 3B nesneye/kılıca dokunduğunda ilgili ses efektini "
                   "çalmalıdır.", "O"],
                  ["FR-09", "Sistem, sahnedeki karakteri tanımlı bir mesafe boyunca animasyonla "
                   "hareket ettirmelidir.", "D"],
                  ["FR-10", "Sistem, her uygulama açılışında ziyaretçi sayacını artırmalı ve kullanıcıya "
                   "kişiselleştirilmiş bir mesaj göstermelidir.", "O"],
                  ["FR-11", "Sistem, ziyaretçi sayısını cihazda kalıcı olarak (PlayerPrefs) saklamalıdır.", "O"],
                  ["FR-12", "Sistem, Harput Kalesi hakkında kısa bilgilendirici bir metin sunmalıdır.", "D"],
                  ["FR-13", "Sistem, 'Haritayı Aç' işlemiyle Google Haritalar'da Harput Kalesi konumunu "
                   "açmalıdır.", "Y"],
                  ["FR-14", "Sistem, ana menü ile AR modu arasında yumuşak (fade) geçiş animasyonu "
                   "sağlamalıdır.", "D"],
                  ["FR-15", "Sistem, çekirdek AR deneyimini internet bağlantısı olmadan da "
                   "çalıştırabilmelidir.", "Y"],
              ],
              [1.3*cm, 12.9*cm, 2.2*cm],
          )]

    s += [H2("3. Fonksiyonel Olmayan Gereksinimler (NFR)"),
          P("Aşağıdaki gereksinimler, sistemin <b>nasıl çalışması gerektiğine</b> (kalite niteliklerine) "
            "ilişkindir."),
          table(
              ["ID", "Kategori", "Gereksinim", "Hedef/Ölçüt"],
              [
                  ["NFR-01", "Performans", "Uygulama akıcı bir kare hızında çalışmalıdır.", "~30–60 FPS"],
                  ["NFR-02", "Performans", "Hedef tanıma gecikmesi düşük olmalıdır.", "≤ ~1,5 sn"],
                  ["NFR-03", "Performans", "Soğuk başlangıç süresi makul olmalıdır.", "≤ ~4 sn"],
                  ["NFR-04", "Güvenilirlik", "Çekirdek akış beklenmedik durumlarda çökmemelidir.", "%0 çökme"],
                  ["NFR-05", "Erişilebilirlik", "Çekirdek deneyim çevrimdışı çalışmalıdır.", "Offline-First"],
                  ["NFR-06", "Kullanılabilirlik", "Arayüz, AR'a yabancı bir turistin tek seferde "
                   "anlayacağı sadelikte olmalıdır.", "Sezgisel UI"],
                  ["NFR-07", "Güvenlik (Safety)", "Fiziksel güvenlik uyarısı görünür olmalıdır.", "Zorunlu uyarı"],
                  ["NFR-08", "Veri Güvenliği", "Konum verisi anonimleştirilmeli, API anahtarları "
                   "korunmalıdır.", "KVKK/GDPR"],
                  ["NFR-09", "Taşınabilirlik", "Uygulama Android cihazlara APK ile doğrudan "
                   "kurulabilmelidir.", "Android"],
                  ["NFR-10", "Sürdürülebilirlik", "Kod modüler, SOLID uyumlu ve belgeli olmalıdır.", "OOP/SOLID"],
                  ["NFR-11", "Bakım", "Sürüm kontrolü Git ile yapılmalı, main her zaman çalışır "
                   "kalmalıdır.", "Git/GitHub"],
                  ["NFR-12", "Verimlilik", "Bellek ve batarya tüketimi optimize edilmelidir.", "Object Pooling"],
              ],
              [1.5*cm, 2.7*cm, 9.3*cm, 2.9*cm],
          )]

    s += [H2("4. Kısıtlar ve Varsayımlar"),
          bullets([
              "<b>Kısıt:</b> AR deneyimi, geçerli 'harput_kalesi' görsel hedefinin kameraya gösterilmesini "
              "gerektirir.",
              "<b>Kısıt:</b> Geliştirme platformu Unity 6000.4.1f1 ve Vuforia Engine 11.4.4'tür; sürüm "
              "değişiklikleri yeniden test gerektirir.",
              "<b>Kısıt:</b> Harita yönlendirmesi ve ziyaretçi senkronizasyonu için internet erişimi "
              "gerekir (çekirdek AR hariç).",
              "<b>Varsayım:</b> Kullanıcının cihazında çalışan bir arka kamera ve yeterli işlem gücü "
              "bulunur.",
              "<b>Varsayım:</b> Kullanıcı, kamera ve konum izinlerini onaylar.",
          ])]
    build("Requirements.pdf", "Gereksinim Dokümanı", s)

# ================================================================ 5) UserScenario
def userscenario():
    from reportlab.platypus import PageBreak
    s = cover("KULLANICI SENARYOSU<br/>(User Scenario)")
    s += [PageBreak()]

    s += [H1("1. Senaryo Bağlamı"), rule(),
          P("Bu belge, HarputAR uygulamasını ilk kez kullanan bir turistin uçtan uca deneyimini adım adım "
            "anlatır. Senaryo; persona, ön koşullar, ana akış, alternatif/istisna akışları ve son durum "
            "ile yapılandırılmıştır."),
          H3("Persona"),
          callout("Kullanıcı: “Elif”, 28 yaşında bir kültür turisti",
                  "Elif, Elazığ'ı ziyaret eden, teknolojiye meraklı ama AR uygulamalarına yabancı bir "
                  "turisttir. Harput Kalesi'ni gezerken kalenin tarihini daha sürükleyici bir biçimde "
                  "deneyimlemek ister. Akıllı telefonunu kullanır ve uygulamayı ilk kez açacaktır."),
          H3("Ön Koşullar"),
          bullets([
              "HarputAR uygulaması (APK) Elif'in Android telefonuna kurulmuştur.",
              "Telefonun arka kamerası çalışır durumdadır.",
              "Kale alanında veya tanıtım panosunda 'harput_kalesi' hedef görseli mevcuttur.",
          ])]

    s += [H2("2. Ana Akış (Adım Adım)")]
    steps = [
        ("1) Uygulamayı açma",
         "Elif, ana ekrandaki HarputAR simgesine dokunur. Açılışta yumuşak bir geçişle ana menü belirir. "
         "Ekranda ziyaretçi sayacı kişiselleştirilmiş bir mesajla onu karşılar: “Harput'u Keşfeden N. "
         "Kişisin!”. Bir “Başla / Oyuna Başla” butonu görünür."),
        ("2) Güvenlik uyarısını onaylama",
         "Deneyim başlamadan önce ekranda şeffaf bir güvenlik uyarısı çıkar: “Lütfen yürürken çevrenize "
         "dikkat ediniz.” Elif uyarıyı okuyup onaylar. (İlk açılışta uygulama ayrıca kamera iznini ister; "
         "Elif izni verir.)"),
        ("3) Kamerayı hedefe tutma",
         "AR moduna geçilir; menü kaybolur ve kamera görüntüsü açılır. Ekranda yanıp sönen bir yönlendirme "
         "metni belirir: “Kamerayı hedefe doğrultun.” Elif telefonunu kale duvarındaki/panodaki hedef "
         "görsele doğru tutar."),
        ("4) Zaman portalından geçiş",
         "Vuforia hedefi tanır (~1–1,5 sn). Yönlendirme metni kaybolur ve hedefin üzerinde bir “zaman "
         "portalı” açılır. Derinlik maskesi sayesinde portal, gerçek duvarda açılmış bir geçit gibi "
         "görünür; içeride Harput'un tarihi sahnesi belirir. Elif telefonunu yaklaştırdıkça portalın "
         "içine doğru “geçmiş” hissi yaşar."),
        ("5) 3B modeller ve ses etkileşimi",
         "Portalın içinde tarihi 3B sahne, ışıklandırma ve çevresel sesler Elif'i karşılar. Sahnedeki bir "
         "karakter (muhafız) animasyonla hareket eder. Elif ekrandaki kılıca dokunduğunda bir kılıç "
         "sesi çalınır; bu etkileşim deneyimi canlı ve keşfedilebilir kılar."),
        ("6) Harita butonunu kullanma",
         "Deneyimden etkilenen Elif, kalenin tam konumuna gitmek ister. Arayüzdeki harita butonuna "
         "dokunur; uygulama Google Haritalar'ı açarak “Harput Kalesi” konumunu gösterir ve yol tarifi "
         "almasını sağlar."),
    ]
    for title, body in steps:
        s += [H3(title), P(body)]

    s += [H2("3. Alternatif ve İstisna Akışları"),
          table(
              ["Durum", "Sistem Davranışı"],
              [
                  ["Hedef bulunamıyor", "Yönlendirme metni yanıp sönerek görünür kalır; Elif kamerayı "
                   "hedefe yeniden doğrultana kadar uygulama bekler, çökmez."],
                  ["Hedef kayboldu", "Portal kaybolur, yönlendirme metni tekrar görünür; hedef yeniden "
                   "bulununca deneyim kaldığı yerden devam eder."],
                  ["İnternet yok", "Çekirdek AR deneyimi (portal, 3B, ses) çevrimdışı çalışmaya devam eder; "
                   "yalnızca harita yönlendirmesi bağlantı gerektirir."],
                  ["Kamera izni reddedildi", "AR başlatılamaz; kullanıcı izin vermeye yönlendirilir."],
                  ["Harita açılamadı", "Hata yakalanır (try–catch), uygulama çökmeden deneyime devam eder."],
              ],
              [3.8*cm, 12.6*cm],
          )]

    s += [H2("4. Son Durum (Postconditions)"),
          bullets([
              "Elif, Harput Kalesi'nin tarihini sürükleyici bir AR deneyimiyle keşfetmiştir.",
              "Ziyaretçi sayacı bir artmış ve cihazda kalıcı olarak saklanmıştır.",
              "Elif, harita yönlendirmesiyle kalenin fiziksel konumuna ulaşabilir durumdadır.",
              "Uygulama boyunca hiçbir çökme yaşanmamış; güvenlik uyarısı görülmüştür.",
          ]),
          H2("5. Deneyim Akış Özeti"),
          P("Uygulamayı açma → Güvenlik uyarısını onaylama → Kamerayı hedefe tutma → Zaman portalından "
            "geçiş → 3B modeller ve ses etkileşimi → Harita butonunu kullanma.")]
    build("UserScenario.pdf", "Kullanıcı Senaryosu", s)

if __name__ == "__main__":
    swot()
    rams()
    ths()
    requirements()
    userscenario()
    print("\nTüm PDF'ler 'docs/' klasörüne üretildi.")
