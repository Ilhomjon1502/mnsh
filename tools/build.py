"""Static site generator for the Muhammad Amin Naziraliyev official site.

Usage:  python tools/build.py [https://your-domain.uz]

Writes index.html, galereya/, blog/, 404.html, robots.txt, sitemap.xml,
llms.txt, llms-full.txt, feed.xml and site.webmanifest into the project root.
Content lives in this file and in tools/data/*.json.
"""
import json
import os
import re
import sys
from datetime import date
from urllib.parse import urlparse
from html import escape as e

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = (sys.argv[1] if len(sys.argv) > 1 else "https://SITE_DOMAIN").rstrip("/")
TODAY = date.today().isoformat()
# Sayt domen ildizida bo'lmasa (masalan github.io/mnsh), ichki havolalarga shu yo'l qo'shiladi.
BASE = urlparse(SITE).path.rstrip("/")

DATA = json.load(open(os.path.join(ROOT, "tools", "data", "gallery.json"), encoding="utf8"))
OWNER, GALLERY = DATA["owner"], DATA["gallery"]
BLOG = json.load(open(os.path.join(ROOT, "tools", "data", "blog.json"), encoding="utf8"))

NAME = "Muhammad Amin Naziraliyev"
FULL_NAME = "Muhammad Amin Naziraliyev Shukurulloh o'g'li"
ALT_NAMES = ["Muhammadamin Naziraliyev", "Muhammad Amin", "MNSH", "Muhammad Amin Naziraliyev Shukurulloh o'g'li",
             "Мухаммад Амин Назиралиев", "Muhammad Amin ustoz"]
TAGLINE = "Codial akademiyasi va Safo bog'chasi asoschisi, SayyidSafo arab tili markazi menejeri"

LINKS = {
    "tg_personal": "https://t.me/IUTMNSH",
    "tg_blog": "https://t.me/mnshuz",
    "codial": "https://www.codialinfo.uz",
    "codial_tg": "https://t.me/codialuz",
    "codial_admin": "https://t.me/codial_admin",
    "safo": "https://safouyi.uz",
    "safo_tg": "https://t.me/safouyiuz",
    "safo_admin": "https://t.me/safouyi_admin",
    "sayyid_tg": "https://t.me/SayyidSafo",
}
SAME_AS = [LINKS["tg_blog"], LINKS["tg_personal"], LINKS["codial"], LINKS["safo"], LINKS["sayyid_tg"]]
PHONE_CODIAL, PHONE_SAFO = "+998 99 820 44 32", "+998 94 423 53 59"

ICON = {
    "tg": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M21.9 4.3 18.6 20c-.2 1-.9 1.3-1.7.8l-4.7-3.5-2.3 2.2c-.3.3-.5.5-1 .5l.4-4.8 8.7-7.9c.4-.3-.1-.5-.6-.2L6.7 13.9 2.1 12.5c-1-.3-1-1 .2-1.5L20.2 4c.9-.3 1.6.2 1.7.3z"/></svg>',
    "phone": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/></svg>',
    "arrow": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
    "link": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M10 13a5 5 0 0 0 7 0l3-3a5 5 0 0 0-7-7l-1 1M14 11a5 5 0 0 0-7 0l-3 3a5 5 0 0 0 7 7l1-1"/></svg>',
    "moon": '<svg class="theme-moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>',
    "sun": '<svg class="theme-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>',
    "menu": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>',
}

MONTHS = ["yanvar", "fevral", "mart", "aprel", "may", "iyun", "iyul", "avgust", "sentabr", "oktabr", "noyabr", "dekabr"]


def uzdate(iso):
    y, m, d = iso.split("-")
    return f"{int(d)}-{MONTHS[int(m) - 1]}, {y}"


def uzmonth(iso):
    y, m, _ = iso.split("-")
    return f"{y}-yil {MONTHS[int(m) - 1]}"


# ---------------------------------------------------------------- structured data
def person_ld():
    return {
        "@type": "Person",
        "@id": f"{SITE}/#person",
        "name": NAME,
        "givenName": "Muhammad Amin",
        "familyName": "Naziraliyev",
        "additionalName": "Shukurulloh o'g'li",
        "alternateName": ALT_NAMES,
        "url": f"{SITE}/",
        "image": {"@type": "ImageObject", "url": f"{SITE}/{OWNER['hero']['file']}", "width": OWNER["hero"]["w"], "height": OWNER["hero"]["h"], "caption": OWNER["hero"]["alt"]},
        "description": "Marg'ilonlik ta'lim tadbirkori va ustoz. Codial akademiyasi va Safo bog'chasi asoschisi, SayyidSafo arab tili markazi menejeri, Inha universiteti bitiruvchisi.",
        "jobTitle": ["Codial akademiyasi asoschisi", "Safo bog'chasi asoschisi", "SayyidSafo arab tili markazi menejeri"],
        "gender": "Male",
        "nationality": {"@type": "Country", "name": "O'zbekiston"},
        "birthPlace": {"@type": "Place", "name": "Marg'ilon, Farg'ona viloyati, O'zbekiston"},
        "homeLocation": {"@type": "Place", "name": "Marg'ilon, Farg'ona viloyati, O'zbekiston"},
        "alumniOf": {"@type": "CollegeOrUniversity", "name": "Inha universiteti Toshkentda (Inha University in Tashkent)", "sameAs": "https://inha.uz"},
        "knowsLanguage": ["uz", "en"],
        "knowsAbout": ["Ta'lim", "Ta'lim tadbirkorligi", "IT ta'limi", "Maktabgacha ta'lim", "Dasturlash", "Boshqaruv", "Arab tili ta'limi"],
        "worksFor": [{"@id": f"{SITE}/#codial"}, {"@id": f"{SITE}/#safo"}, {"@id": f"{SITE}/#sayyidsafo"}],
        "sameAs": SAME_AS,
        "mainEntityOfPage": f"{SITE}/",
    }


def orgs_ld():
    founder = {"@id": f"{SITE}/#person"}
    return [
        {"@type": ["EducationalOrganization", "LocalBusiness"], "@id": f"{SITE}/#codial", "name": "Codial akademiyasi",
         "alternateName": ["Codial", "Codial — Zamonaviy Kasblar Akademiyasi", "Codial o'quv markazi"],
         "url": LINKS["codial"], "telephone": "+998998204432", "foundingDate": "2021-01-18", "founder": founder,
         "description": "Farg'onadagi IT va zamonaviy kasblar o'quv markazi: kompyuter savodxonligi, Vibe Coding (sun'iy intellekt), kiberxavfsizlik va SMM yo'nalishlari. 2021-yildan beri 500 ga yaqin bitiruvchi.",
         "address": {"@type": "PostalAddress", "addressLocality": "Farg'ona", "addressRegion": "Farg'ona viloyati", "addressCountry": "UZ"},
         "sameAs": [LINKS["codial_tg"], LINKS["codial"]]},
        {"@type": ["Preschool", "LocalBusiness"], "@id": f"{SITE}/#safo", "name": "Safo bog'chasi",
         "url": LINKS["safo"], "telephone": "+998944235359", "founder": founder,
         "description": "3–6 yoshli bolalar uchun bog'cha: tabiiy uy taomlari, milliy tarbiya, 5 yoshdan ingliz tili va mental arifmetika. 3 ta filial.",
         "address": {"@type": "PostalAddress", "addressRegion": "Farg'ona viloyati", "addressCountry": "UZ"},
         "sameAs": [LINKS["safo_tg"], LINKS["safo"]]},
        {"@type": "EducationalOrganization", "@id": f"{SITE}/#sayyidsafo", "name": "SayyidSafo arab tili markazi",
         "alternateName": ["SayyidSafo akademiyasi", "SayyidSafo"], "url": LINKS["sayyid_tg"],
         "description": "Arab tili o'rgatuvchi ta'lim markazi. Muhammad Amin Naziraliyev markazda menejer.",
         "address": {"@type": "PostalAddress", "addressRegion": "Farg'ona viloyati", "addressCountry": "UZ"},
         "sameAs": [LINKS["sayyid_tg"]]},
    ]


FAQ = [
    ("Muhammad Amin Naziraliyev kim?",
     "Muhammad Amin Naziraliyev Shukurulloh o'g'li (MNSH) — Marg'ilon shahrida tug'ilib o'sgan o'zbekistonlik ta'lim tadbirkori va ustoz. U Farg'onadagi Codial IT akademiyasi hamda Safo bog'chasi asoschisi, SayyidSafo arab tili markazida menejer. Toshkentdagi Inha universiteti bitiruvchisi."),
    ("Codial akademiyasiga kim va qachon asos solgan?",
     "Codial akademiyasiga 2021-yil 18-yanvarda Muhammad Amin Naziraliyev asos solgan. Akademiya Farg'ona shahrida joylashgan, kompyuter savodxonligi, Vibe Coding (sun'iy intellekt), kiberxavfsizlik va SMM yo'nalishlarida o'qitadi. Hozirgacha 500 ga yaqin o'quvchi bitirgan, 2 ta filiali bor (iTeach bilan)."),
    ("Safo bog'chasi nima va uni kim asos solgan?",
     "Safo bog'chasi — 3–6 yoshli bolalar uchun bog'cha. Unda tabiiy uy taomlari beriladi, bolalar milliy odob-axloq ruhida tarbiyalanadi, 5 yoshdan ingliz tili va mental arifmetika o'rgatiladi. Bog'chaga Muhammad Amin Naziraliyev asos solgan; hozir 3 ta filiali bor. Ma'lumot: safouyi.uz."),
    ("Muhammad Amin Naziraliyev qayerda yashaydi va qayerda o'qigan?",
     "U Marg'ilon shahrida (Farg'ona viloyati, O'zbekiston) tug'ilib o'sgan va hozir ham shu yerda yashaydi. Toshkentdagi Inha universitetida IT va boshqaruv sohasida o'qigan (2020-yilda bitirgan). Ingliz tilini biladi. Ta'limga qiziqishi 6-sinfdan boshlangan, maktab va litseyda matematikadan dars bergan."),
    ("SayyidSafo arab tili markazida u qanday vazifada?",
     "Muhammad Amin Naziraliyev SayyidSafo arab tili markazida menejer sifatida faoliyat yuritadi. Markaz haqidagi yangiliklar Telegramdagi t.me/SayyidSafo sahifasida e'lon qilinadi."),
    ("Uning blogi qayerda?",
     "Muhammad Amin Naziraliyevning shaxsiy bloggi Telegramdagi @mnshuz kanalida (t.me/mnshuz). Unda sayohat, tarbiya, tadbirkorlik va hayotiy xulosalar haqida muntazam yoziladi. So'nggi yozuvlar bu saytning «Blog» sahifasida ham ko'rsatilgan."),
    ("U bilan qanday bog'lansa bo'ladi?",
     f"Shaxsiy Telegram: @IUTMNSH (t.me/IUTMNSH). Blog kanali: @mnshuz. Codial akademiyasi: {PHONE_CODIAL}, @codial_admin. Safo bog'chasi: {PHONE_SAFO}, @safouyi_admin."),
    ("Muhammad Amin Naziraliyevning qiziqishlari qanday?",
     "Suv bo'yida yurish va yozish, kitob o'qish, do'stlar bilan suhbat qurish. U hazilkash, tog'ga chiqish (hiking) va sayohatni yaxshi ko'radi, 5 ta davlatda bo'lgan. Ustozlari ham, shogirdlari ham bor."),
]


def jsonld(*graph):
    return '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@graph": list(graph)}, ensure_ascii=False, separators=(",", ":")) + "</script>"


def website_ld():
    return {"@type": "WebSite", "@id": f"{SITE}/#website", "url": f"{SITE}/", "name": f"{NAME} — rasmiy sayt",
            "inLanguage": "uz", "publisher": {"@id": f"{SITE}/#person"}, "about": {"@id": f"{SITE}/#person"}}


def crumbs_ld(items):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + p} for i, (n, p) in enumerate(items)]}


# ---------------------------------------------------------------- layout
NAV = [("Haqida", "/#haqida"), ("Faoliyat", "/#faoliyat"), ("Yo'l", "/#yol"), ("Galereya", "/galereya/"), ("Blog", "/blog/"), ("Savollar", "/#savollar")]


def head(title, desc, path, ld, og_image=None, og_type="website"):
    url = f"{SITE}{path}"
    img = og_image or f"{SITE}/assets/img/og-cover.jpg"
    return f"""<!doctype html>
<html lang="uz" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="author" content="{e(NAME)}">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
<meta name="theme-color" content="#f4f7f3">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="uz" href="{url}">
<link rel="alternate" hreflang="x-default" href="{url}">
<link rel="alternate" type="application/atom+xml" title="{e(NAME)} — blog" href="{SITE}/feed.xml">
<link rel="alternate" type="text/markdown" title="llms.txt" href="{SITE}/llms.txt">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="{e(NAME)}">
<meta property="og:locale" content="uz_UZ">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{img}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{e(NAME)} — {e(TAGLINE)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{img}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600;9..144,700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap">
<link rel="stylesheet" href="/assets/css/style.css">
<script>(function(){{var d=document.documentElement,t;d.classList.add('js');try{{t=localStorage.getItem('theme')}}catch(e){{}}if(t!=='dark'){{t='light'}}d.setAttribute('data-theme',t);setTimeout(function(){{if(!window.__ok)d.classList.remove('js')}},4000)}})()</script>
{jsonld(*ld)}
</head>
"""


def header(active=""):
    links = "".join(
        f'<a href="{h}"{" aria-current=\"page\"" if active and h == active else ""}>{t}</a>' for t, h in NAV)
    return f"""<body>
<a class="skip" href="#main">Asosiy kontentga o'tish</a>
<div class="aurora" aria-hidden="true"><i></i><i></i><i></i></div>
<div class="progress" aria-hidden="true"></div>
<header class="nav" role="banner">
  <a class="brand" href="/" aria-label="{e(NAME)} — bosh sahifa"><img class="brand-mark" src="/assets/img/favicon.svg" alt="" width="30" height="30"><span>Muhammad Amin<b>.</b></span></a>
  <nav class="nav-links" aria-label="Asosiy menyu">{links}</nav>
  <div class="nav-tools">
    <button class="icon-btn" type="button" data-theme-toggle aria-label="Mavzuni almashtirish (kunduzgi / tungi)">{ICON['moon']}{ICON['sun']}</button>
    <a class="btn btn-primary cta-nav" href="{LINKS['tg_personal']}" rel="noopener me">Bog'lanish</a>
    <button class="icon-btn menu-btn" type="button" data-menu-toggle aria-label="Menyuni ochish" aria-expanded="false">{ICON['menu']}</button>
  </div>
</header>
"""


def footer():
    return f"""<footer>
  <div class="wrap">
    <div class="foot">
      <div>
        <a class="brand" href="/"><img class="brand-mark" src="/assets/img/favicon.svg" alt="" width="30" height="30"><span>Muhammad Amin<b>.</b></span></a>
        <p style="margin-top:14px">{e(NAME)} — {e(TAGLINE)}. Marg'ilon, Farg'ona viloyati, O'zbekiston.</p>
      </div>
      <div>
        <h2>Sahifalar</h2>
        <ul>
          <li><a href="/">Bosh sahifa</a></li>
          <li><a href="/galereya/">Fotogalereya</a></li>
          <li><a href="/blog/">Blog</a></li>
          <li><a href="/#savollar">Ko'p so'raladigan savollar</a></li>
          <li><a href="/llms.txt">llms.txt</a></li>
        </ul>
      </div>
      <div>
        <h2>Rasmiy sahifalar</h2>
        <ul>
          <li><a href="{LINKS['tg_blog']}" rel="me noopener">Telegram blog — @mnshuz</a></li>
          <li><a href="{LINKS['tg_personal']}" rel="me noopener">Telegram — @IUTMNSH</a></li>
          <li><a href="{LINKS['codial']}" rel="noopener">Codial akademiyasi</a></li>
          <li><a href="{LINKS['safo']}" rel="noopener">Safo bog'chasi</a></li>
          <li><a href="{LINKS['sayyid_tg']}" rel="noopener">SayyidSafo (Telegram)</a></li>
        </ul>
      </div>
    </div>
    <div class="copy"><span>© 2026 {e(NAME)}. Barcha huquqlar himoyalangan.</span><span>Sayt ma'lumotlari rasmiy manbalar asosida tuzilgan.</span></div>
  </div>
</footer>
<script src="/assets/js/main.js" defer></script>
<script>window.__ok=1</script>
</body>
</html>
"""


def reveal(i=0):
    return f'data-reveal style="--d:{i}"'


# ---------------------------------------------------------------- pages
def page_index():
    title = f"{NAME} — Codial va Safo bog'chasi asoschisi | Rasmiy sayt"
    desc = (f"{NAME} (MNSH) — Marg'ilonlik ta'lim tadbirkori va ustoz. Codial IT akademiyasi va Safo bog'chasi asoschisi, "
            "SayyidSafo arab tili markazi menejeri. Biografiya, faoliyat, fotogalereya va blog.")
    ld = [person_ld(), *orgs_ld(), website_ld(),
          {"@type": "ProfilePage", "@id": f"{SITE}/#profilepage", "url": f"{SITE}/", "name": title, "inLanguage": "uz",
           "dateModified": TODAY, "mainEntity": {"@id": f"{SITE}/#person"}, "isPartOf": {"@id": f"{SITE}/#website"},
           "primaryImageOfPage": {"@type": "ImageObject", "url": f"{SITE}/{OWNER['hero']['file']}"}},
          {"@type": "FAQPage", "@id": f"{SITE}/#faq", "mainEntity": [
              {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}]
    h = OWNER["hero"]
    marquee = ["Codial akademiyasi", "Safo bog'chasi", "SayyidSafo arab tili markazi", "Inha universiteti bitiruvchisi",
               "Marg'ilon · Farg'ona", "Ta'lim tadbirkori", "Ustoz va bloger"]
    marq = "".join(f"<span>{e(m)}</span>" for m in marquee) * 2
    strip = "".join(
        f'<a href="/galereya/" aria-label="{e(g["caption"])}"><img src="/{g["small"]}" width="{g["sw"]}" height="{g["sh"]}" alt="{e(g["alt"])}" loading="lazy"></a>'
        for g in GALLERY[:4])
    posts = "".join(post_card(p, i) for i, p in enumerate(BLOG[:3]))
    faq = "".join(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in FAQ)
    timeline = [
        ("Bolalik · 6-sinf", "Ta'limga qiziqish boshlandi", "Maktabda va litseyda matematikadan dars bergan: ta'lim bilan yo'li shu yerdan boshlangan."),
        ("2020", "Inha universiteti bitiruvchisi", "Toshkentdagi Inha universitetida IT va boshqaruv sohasida o'qib, 2020-yilda bitirgan."),
        ("2020", "MNSH Android-Academy", "Marg'ilon Raqamli texnologiyalar markazida Android dasturlashdan dars bergan, frilanserlik qilgan. 2020-yil oktyabrida marg'ilonlik o'quvchilar bilan kursning birinchi bosqichi yakunlangan."),
        ("2021-yil 18-yanvar", "Codial akademiyasiga asos solindi", "Farg'ona shahrida zamonaviy kasblar akademiyasi ochildi. Keyinchalik Marg'ilonda ham filial yo'lga qo'yildi; Codial IT-Park rezidenti bo'ldi."),
        ("2021-yil noyabr", "#100Maktab: IT haqida tushuncha", "Farg'ona yoshlariga IT kasblari haqida maktablarda seminarlar boshlandi. 100 ta maktab marrasidan keyin ham taklif qilingan maktablarda davom etdi."),
        ("2023-yil may", "Inha rektori Marg'ilonda", "Inha universiteti rektori Marg'ilonga kelib, Codial filialida universitetga qiziqqan yoshlar bilan uchrashdi."),
        ("Hozir", "Codial, Safo bog'chasi, SayyidSafo", "Safo bog'chasi (3 filial) va Codial (2 filial) rahbari, SayyidSafo arab tili markazi menejeri. Telegramdagi blogida sayohat, tarbiya va tadbirkorlik xulosalarini yozib boradi."),
    ]
    tl = "".join(f'<div class="tl-item" {reveal()}><time>{e(t)}</time><h3>{e(h3)}</h3><p>{e(p)}</p></div>' for t, h3, p in timeline)
    body = f"""<main id="main">
<section class="hero" aria-labelledby="top-title">
  <div class="wrap hero-grid">
    <div>
      <p class="pill"><span class="dot" aria-hidden="true"></span>Marg'ilon, Farg'ona viloyati · O'zbekiston</p>
      <h1 id="top-title" class="split">Muhammad Amin <span class="grad">Naziraliyev</span></h1>
      <p class="lead"><strong>{e(FULL_NAME)}</strong> — ta'lim sohasidagi tadbirkor va ustoz. <strong>Codial akademiyasi</strong> hamda <strong>Safo bog'chasi</strong> asoschisi, <strong>SayyidSafo arab tili markazi</strong> menejeri. Marg'ilon shahrida tug'ilib o'sgan, hozir ham shu yerda yashaydi.</p>
      <div class="hero-cta">
        <a class="btn btn-primary" href="{LINKS['tg_personal']}" rel="me noopener">{ICON['tg']} Telegramda yozish</a>
        <a class="btn btn-ghost" href="/blog/">Blogni o'qish {ICON['arrow']}</a>
      </div>
      <div class="chips" aria-label="Rasmiy havolalar">
        <a class="chip" href="{LINKS['tg_blog']}" rel="me noopener">{ICON['tg']} @mnshuz</a>
        <a class="chip" href="{LINKS['codial']}" rel="noopener">{ICON['link']} Codial</a>
        <a class="chip" href="{LINKS['safo']}" rel="noopener">{ICON['link']} Safo bog'chasi</a>
        <a class="chip" href="{LINKS['sayyid_tg']}" rel="noopener">{ICON['tg']} SayyidSafo</a>
      </div>
    </div>
    <div class="portrait">
      <div class="portrait-glow" aria-hidden="true"></div>
      <div class="portrait-frame"><img src="/{h['file']}" width="{h['w']}" height="{h['h']}" alt="{e(h['alt'])}" fetchpriority="high"></div>
      <div class="float-badge fb-1" aria-hidden="true"><span class="ico">C</span><span>Codial<small>asoschisi · 2021</small></span></div>
      <div class="float-badge fb-2" aria-hidden="true"><span class="ico">S</span><span>Safo bog'chasi<small>3 ta filial</small></span></div>
    </div>
  </div>
</section>

<div class="marquee" aria-hidden="true"><div class="marquee-track">{marq}</div></div>

<section aria-labelledby="raqamlar" style="padding-bottom:0">
  <div class="wrap">
    <h2 id="raqamlar" class="sr-only">Raqamlarda</h2>
    <div class="stats">
      <div class="card stat spot" {reveal(0)}><b data-count="500" data-suffix="+">500+</b><span>Codial bitiruvchilari (2021-yildan)</span></div>
      <div class="card stat spot" {reveal(1)}><b data-count="2021" data-plain>2021</b><span>Codial asos solingan yil (18-yanvar)</span></div>
      <div class="card stat spot" {reveal(2)}><b data-count="100" data-suffix="+">100+</b><span>maktabda IT seminarlari (#100Maktab)</span></div>
      <div class="card stat spot" {reveal(3)}><b data-count="3">3</b><span>Safo bog'chasi filiallari</span></div>
      <div class="card stat spot" {reveal(4)}><b data-count="2">2</b><span>Codial filiallari (iTeach bilan)</span></div>
    </div>
  </div>
</section>

<section id="haqida" aria-labelledby="haqida-t">
  <div class="wrap about-grid">
    <div class="about-photos" {reveal()}>
      <figure><img src="/{OWNER['speaker']['file']}" width="{OWNER['speaker']['w']}" height="{OWNER['speaker']['h']}" alt="{e(OWNER['speaker']['alt'])}" loading="lazy"></figure>
      <figure><img src="/{OWNER['reading']['file']}" width="{OWNER['reading']['w']}" height="{OWNER['reading']['h']}" alt="{e(OWNER['reading']['alt'])}" loading="lazy"></figure>
      <figure><img src="/{OWNER['class']['file']}" width="{OWNER['class']['w']}" height="{OWNER['class']['h']}" alt="{e(OWNER['class']['alt'])}" loading="lazy"></figure>
    </div>
    <div class="prose">
      <p class="eyebrow">Haqida</p>
      <h2 id="haqida-t" {reveal()}>Umrim bayoni</h2>
      <p {reveal()}><strong>{e(NAME)}</strong> 27 yoshda (2026-yil holatiga ko'ra), Marg'ilon shahrida tug'ilib o'sgan va hozir ham shu yerda yashaydi. Oilali, bir nafar o'g'li bor.</p>
      <p {reveal()}>Ta'limga qiziqish 6-sinfdan boshlangan: maktabda va litseyda <strong>matematikadan dars bergan</strong>. Keyin Toshkentdagi <strong>Inha universitetida</strong> IT va boshqaruv sohasida o'qigan (2020-yilda bitirgan). Ingliz tilini biladi.</p>
      <p {reveal()}>2020-yilda Marg'ilon Raqamli texnologiyalar markazida Android dasturlashdan dars bergan va frilanser sifatida ishlagan. <strong>2021-yil 18-yanvarda Farg'onada Codial akademiyasiga asos solgan</strong>; bugun akademiyani 500 ga yaqin o'quvchi bitirgan. Shuningdek, <strong>Safo bog'chasi</strong> asoschisi va <strong>SayyidSafo arab tili markazi</strong> menejeri.</p>
      <p {reveal()}>Ustozlari ham, shogirdlari ham bor. Suv bo'yida yurish va yozishni, kitob o'qishni, do'stlar bilan suhbatni yaxshi ko'radi. Hazilkash. Tog'ga chiqish (hiking) va sayohat qiladi, Telegramdagi blogida o'rgangan xulosalarini bo'lishib boradi.</p>
      <dl class="facts" {reveal()}>
        <div class="fact"><dt>To'liq ismi</dt><dd>{e(FULL_NAME)}</dd></div>
        <div class="fact"><dt>Taxallus</dt><dd>MNSH</dd></div>
        <div class="fact"><dt>Yashash joyi</dt><dd>Marg'ilon, Farg'ona viloyati</dd></div>
        <div class="fact"><dt>Ta'lim</dt><dd>Inha universiteti, Toshkent (IT va boshqaruv)</dd></div>
        <div class="fact"><dt>Tillar</dt><dd>O'zbek, ingliz</dd></div>
        <div class="fact"><dt>Oila</dt><dd>Oilali, bir nafar o'g'li bor</dd></div>
        <div class="fact"><dt>Lavozimlar</dt><dd>Codial va Safo bog'chasi asoschisi; SayyidSafo markazi menejeri</dd></div>
        <div class="fact"><dt>Qiziqishlar</dt><dd>Yozish, kitob, sayohat, hiking, suhbat</dd></div>
      </dl>
      <blockquote class="quote" {reveal()}>Blog'dan maqsad nima bo'lsa yozish emas xulosalarni yozish.<cite>— @mnshuz blogidan</cite></blockquote>
    </div>
  </div>
</section>

<section id="faoliyat" aria-labelledby="faoliyat-t">
  <div class="wrap">
    <div class="sec-head">
      <p class="eyebrow">Faoliyat</p>
      <h2 id="faoliyat-t" {reveal()}>Uch yo'nalishda ta'lim</h2>
      <p {reveal()}>IT ta'limi, maktabgacha tarbiya va arab tili: odamga bilim va tarbiya beradigan uch maskan.</p>
    </div>
    <div class="orgs">
      <article class="card org spot" {reveal(0)} id="codial">
        <div class="org-ico" aria-hidden="true">C</div>
        <p class="role">Asoschi</p>
        <h3>Codial akademiyasi</h3>
        <p>Farg'onadagi zamonaviy kasblar akademiyasi. 2021-yil 18-yanvarda {e(NAME)} tomonidan asos solingan.</p>
        <ul>
          <li>Yo'nalishlar: kompyuter savodxonligi, Vibe Coding (sun'iy intellekt), kiberxavfsizlik, SMM</li>
          <li>500 ga yaqin bitiruvchi, 2 ta filial (iTeach bilan)</li>
          <li>Bitiruvchilar 10 tadan 30 tagacha loyiha bilan bitiradi</li>
        </ul>
        <div class="links"><a href="{LINKS['codial']}" rel="noopener">codialinfo.uz</a><a href="{LINKS['codial_tg']}" rel="noopener">Telegram</a><a href="tel:+998998204432">{PHONE_CODIAL}</a></div>
      </article>
      <article class="card org spot" {reveal(1)} id="safo">
        <div class="org-ico" aria-hidden="true">S</div>
        <p class="role">Asoschi</p>
        <h3>Safo bog'chasi</h3>
        <p>3–6 yoshli bolalar uchun pokiza va mehrli tarbiya maskani. Hozir 3 ta filiali bor.</p>
        <ul>
          <li>100% tabiiy, uy sharoitida tayyorlangan taomlar</li>
          <li>Milliy qadriyatlar va odob-axloq ruhida tarbiya</li>
          <li>5 yoshdan ingliz tili va mental arifmetika</li>
        </ul>
        <div class="links"><a href="{LINKS['safo']}" rel="noopener">safouyi.uz</a><a href="{LINKS['safo_tg']}" rel="noopener">Telegram</a><a href="tel:+998944235359">{PHONE_SAFO}</a></div>
      </article>
      <article class="card org spot" {reveal(2)} id="sayyidsafo">
        <div class="org-ico" aria-hidden="true">Ś</div>
        <p class="role">Menejer</p>
        <h3>SayyidSafo arab tili markazi</h3>
        <p>Arab tilini o'rgatadigan ta'lim markazi. {e(NAME)} markazda menejer sifatida ishlaydi.</p>
        <ul>
          <li>Arab tili ta'limi</li>
          <li>Markaz yangiliklari Telegram sahifasida</li>
        </ul>
        <div class="links"><a href="{LINKS['sayyid_tg']}" rel="noopener">t.me/SayyidSafo</a></div>
      </article>
    </div>
  </div>
</section>

<section id="yol" aria-labelledby="yol-t">
  <div class="wrap">
    <div class="sec-head">
      <p class="eyebrow">Yo'l</p>
      <h2 id="yol-t" {reveal()}>Maktab partasidan o'z akademiyasigacha</h2>
    </div>
    <div class="timeline">{tl}</div>
  </div>
</section>

<section aria-labelledby="gal-t">
  <div class="wrap">
    <div class="sec-head">
      <p class="eyebrow">Fotogalereya</p>
      <h2 id="gal-t" {reveal()}>Lavhalar: seminarlar, uchrashuvlar, safarlar</h2>
      <p {reveal()}>Codial akademiyasi, maktablardagi IT seminarlari va tadbirlardan arxiv suratlar.</p>
    </div>
    <div class="strip" {reveal()}>{strip}</div>
    <div class="more"><a class="btn btn-ghost" href="/galereya/">Barcha suratlar {ICON['arrow']}</a></div>
  </div>
</section>

<section aria-labelledby="blog-t">
  <div class="wrap">
    <div class="sec-head">
      <p class="eyebrow">Blog</p>
      <h2 id="blog-t" {reveal()}>So'nggi yozuvlar</h2>
      <p {reveal()}>Sayohat, tarbiya, tadbirkorlik va hayotiy xulosalar. To'liq matnlar Telegramdagi @mnshuz kanalida.</p>
    </div>
    <div class="posts">{posts}</div>
    <div class="more"><a class="btn btn-ghost" href="/blog/">Barcha yozuvlar {ICON['arrow']}</a></div>
  </div>
</section>

<section id="savollar" aria-labelledby="faq-t">
  <div class="wrap">
    <div class="sec-head">
      <p class="eyebrow">Savol-javob</p>
      <h2 id="faq-t" {reveal()}>Ko'p so'raladigan savollar</h2>
    </div>
    <div class="faq" {reveal()}>{faq}</div>
  </div>
</section>

<section id="aloqa" aria-labelledby="aloqa-t">
  <div class="wrap">
    <div class="cta-box" {reveal()}>
      <h2 id="aloqa-t">Bog'lanish</h2>
      <p>Hamkorlik, ta'lim yoki tadbirlarga taklif bo'yicha Telegram orqali yozing. Farzandingizni o'qitish masalasi bo'lsa, tegishli markazga murojaat qiling.</p>
      <div class="contacts">
        <div class="contact"><small>Telegram (shaxsiy)</small><a href="{LINKS['tg_personal']}" rel="me noopener">@IUTMNSH</a></div>
        <div class="contact"><small>Telegram blog</small><a href="{LINKS['tg_blog']}" rel="me noopener">@mnshuz</a></div>
        <div class="contact"><small>Codial akademiyasi</small><a href="tel:+998998204432">{PHONE_CODIAL}</a></div>
        <div class="contact"><small>Safo bog'chasi</small><a href="tel:+998944235359">{PHONE_SAFO}</a></div>
      </div>
    </div>
  </div>
</section>
</main>
"""
    return head(title, desc, "/", ld) + header("/") + body + footer()


def post_card(p, i=0):
    return (f'<article class="card post spot" {reveal(i)}><time datetime="{p["date"]}">{uzdate(p["date"])}</time>'
            f'<h3>{e(p["title"])}</h3><p>{e(p["excerpt"])}</p>'
            f'<a class="read" href="{p["url"]}" rel="noopener" aria-label="{e(p["title"])} — Telegramda o\'qish">Telegramda o\'qish</a></article>')


def page_gallery():
    title = f"Fotogalereya — {NAME}"
    desc = (f"{NAME} fotogalereyasi: Codial akademiyasi, Inha universiteti, maktablardagi IT seminarlari, "
            "uchrashuvlar va sayohatlardan suratlar (2020–2026).")
    ld = [person_ld(), website_ld(), crumbs_ld([("Bosh sahifa", "/"), ("Fotogalereya", "/galereya/")]),
          {"@type": "ImageGallery", "@id": f"{SITE}/galereya/#gallery", "url": f"{SITE}/galereya/", "name": title,
           "inLanguage": "uz", "about": {"@id": f"{SITE}/#person"}, "isPartOf": {"@id": f"{SITE}/#website"},
           "image": [{"@type": "ImageObject", "contentUrl": f"{SITE}/{g['large']}", "thumbnailUrl": f"{SITE}/{g['small']}",
                      "caption": g["caption"], "name": g["alt"], "datePublished": g["date"], "width": g["lw"], "height": g["lh"],
                      "creator": {"@id": f"{SITE}/#person"}, "acquireLicensePage": f"{SITE}/galereya/"} for g in GALLERY]}]
    years = {}
    for g in GALLERY:
        years.setdefault(g["date"][:4], []).append(g)
    sections = ""
    for y in sorted(years, reverse=True):
        shots = "".join(
            f'<figure class="shot" {reveal(i % 3)}><a class="zoom" href="/{g["large"]}" data-caption="{e(g["caption"])}">'
            f'<img src="/{g["small"]}" width="{g["sw"]}" height="{g["sh"]}" alt="{e(g["alt"])}" loading="lazy"></a>'
            f'<figcaption><time datetime="{g["date"]}">{uzdate(g["date"])}</time>{e(g["caption"])} '
            f'<a href="{g["url"]}" rel="noopener">Telegramda</a></figcaption></figure>' for i, g in enumerate(years[y]))
        sections += f'<h2 class="gal-year">{y}</h2><div class="masonry">{shots}</div>'
    body = f"""<main id="main">
<div class="page-head"><div class="wrap">
  <p class="crumbs"><a href="/">Bosh sahifa</a> / Fotogalereya</p>
  <p class="eyebrow">Arxiv</p>
  <h1 class="split">Fotogalereya</h1>
  <p class="lead">{e(NAME)} faoliyatidan lavhalar: Inha universiteti, Codial akademiyasi, maktablardagi IT seminarlari, uchrashuvlar va sayohatlar. Suratlar rasmiy Telegram kanali (@mnshuz) arxividan.</p>
</div></div>
<section style="padding-top:20px"><div class="wrap">{sections}</div></section>
</main>
<div class="lightbox" role="dialog" aria-modal="true" aria-label="Surat" aria-hidden="true"><button type="button" aria-label="Yopish">×</button><div style="text-align:center"><img alt=""><p></p></div></div>
"""
    return head(title, desc, "/galereya/", ld, f"{SITE}/{GALLERY[0]['large']}") + header("/galereya/") + body + footer()


def page_blog():
    posts = BLOG[:36]
    title = f"Blog — {NAME}"
    desc = (f"{NAME} blogi: sayohat, tarbiya, tadbirkorlik va hayotiy xulosalar. "
            "So'nggi yozuvlar sarlavhalari va qisqacha mazmuni, to'liq matn Telegramda (@mnshuz).")
    ld = [person_ld(), website_ld(), crumbs_ld([("Bosh sahifa", "/"), ("Blog", "/blog/")]),
          {"@type": "Blog", "@id": f"{SITE}/blog/#blog", "url": f"{SITE}/blog/", "name": f"{NAME} blogi", "inLanguage": "uz",
           "author": {"@id": f"{SITE}/#person"}, "isPartOf": {"@id": f"{SITE}/#website"},
           "sameAs": LINKS["tg_blog"],
           "blogPost": [{"@type": "BlogPosting", "headline": p["title"], "description": p["excerpt"], "url": p["url"],
                         "datePublished": p["date"], "inLanguage": "uz", "author": {"@id": f"{SITE}/#person"},
                         "mainEntityOfPage": p["url"]} for p in posts]}]
    cards = "".join(post_card(p, i % 3) for i, p in enumerate(posts))
    body = f"""<main id="main">
<div class="page-head"><div class="wrap">
  <p class="crumbs"><a href="/">Bosh sahifa</a> / Blog</p>
  <p class="eyebrow">Blog</p>
  <h1 class="split">Xulosalar bloggi</h1>
  <p class="lead">«Blog'dan maqsad nima bo'lsa yozish emas, xulosalarni yozish.» Sayohat, voqea, ibrat va nasihat. To'liq matnlar Telegramdagi <a href="{LINKS['tg_blog']}" rel="me noopener">@mnshuz</a> kanalida; bu yerda so'nggi {len(posts)} ta yozuvning qisqacha mazmuni.</p>
  <p class="hero-cta" style="margin-bottom:0"><a class="btn btn-primary" href="{LINKS['tg_blog']}" rel="me noopener">{ICON['tg']} Kanalga obuna bo'lish</a><a class="btn btn-ghost" href="/feed.xml">RSS / Atom</a></p>
</div></div>
<section style="padding-top:40px"><div class="wrap"><div class="posts">{cards}</div></div></section>
</main>
"""
    return head(title, desc, "/blog/", ld) + header("/blog/") + body + footer()


def page_404():
    return (head("Sahifa topilmadi — " + NAME, "Bunday sahifa mavjud emas.", "/404.html", [website_ld()]).replace(
        'content="index, follow', 'content="noindex, follow').replace("max-image-preview:large", "max-image-preview:none") +
            header() + f"""<main id="main"><div class="page-head"><div class="wrap" style="min-height:50vh">
<p class="eyebrow">404</p><h1>Sahifa topilmadi</h1>
<p class="lead">Siz izlagan sahifa mavjud emas yoki ko'chirilgan.</p>
<p class="hero-cta"><a class="btn btn-primary" href="/">Bosh sahifaga qaytish</a><a class="btn btn-ghost" href="/blog/">Blog</a></p>
</div></div></main>""" + footer())


# ---------------------------------------------------------------- machine-readable files
def robots():
    bots = ["Googlebot", "Bingbot", "Applebot", "DuckDuckBot", "YandexBot", "GPTBot", "OAI-SearchBot", "ChatGPT-User",
            "ClaudeBot", "Claude-User", "Claude-SearchBot", "anthropic-ai", "PerplexityBot", "Perplexity-User",
            "Google-Extended", "Gemini-Deep-Research", "Applebot-Extended", "Meta-ExternalAgent", "CCBot", "cohere-ai",
            "MistralAI-User", "Bytespider", "Amazonbot", "DuckAssistBot"]
    s = "# Barcha qidiruv tizimlari va sun'iy intellekt botlariga ruxsat.\nUser-agent: *\nAllow: /\n\n"
    s += "".join(f"User-agent: {b}\nAllow: /\n\n" for b in bots)
    s += f"Sitemap: {SITE}/sitemap.xml\n# LLM uchun qisqa tavsif: {SITE}/llms.txt\n"
    return s


def sitemap():
    pages = [("/", "weekly", "1.0", [OWNER["hero"]["file"]]), ("/galereya/", "monthly", "0.8", [g["large"] for g in GALLERY]), ("/blog/", "weekly", "0.8", [])]
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">']
    for p, freq, prio, imgs in pages:
        out.append(f"<url><loc>{SITE}{p}</loc><lastmod>{TODAY}</lastmod><changefreq>{freq}</changefreq><priority>{prio}</priority>")
        for im in imgs:
            cap = next((g["caption"] for g in GALLERY if g["large"] == im), OWNER["hero"]["alt"])
            out.append(f"<image:image><image:loc>{SITE}/{im}</image:loc><image:caption>{e(cap)}</image:caption></image:image>")
        out.append("</url>")
    out.append("</urlset>")
    return "\n".join(out) + "\n"


def facts_md():
    return f"""## Qisqacha ma'lumot

- To'liq ismi: {FULL_NAME} (boshqa yozilishlari: Muhammadamin Naziraliyev, Muhammad Amin, MNSH)
- Kasbi: ta'lim tadbirkori, ustoz, bloger
- Lavozimlari: Codial akademiyasi asoschisi; Safo bog'chasi asoschisi; SayyidSafo arab tili markazi menejeri
- Yoshi: 27 (2026-yil holatiga ko'ra)
- Tug'ilgan va yashaydigan joyi: Marg'ilon shahri, Farg'ona viloyati, O'zbekiston
- Ta'lim: Inha universiteti, Toshkent (IT va boshqaruv sohasi), 2020-yilda bitirgan
- Tillar: o'zbek, ingliz
- Oila: oilali, bir nafar o'g'li bor
- Qiziqishlar: yozish, kitob o'qish, suv bo'yida yurish, do'stlar bilan suhbat, sayohat, hiking
- Blog: {LINKS['tg_blog']} (Telegram, @mnshuz)
- Shaxsiy Telegram: {LINKS['tg_personal']} (@IUTMNSH)

## Biografiya

{NAME} Marg'ilon shahrida tug'ilib o'sgan. Ta'limga qiziqishi 6-sinfdan boshlangan; maktabda va litseyda matematikadan dars bergan. Toshkentdagi Inha universitetida IT va boshqaruv sohasida o'qigan (2020). 2020-yilda Marg'ilon Raqamli texnologiyalar markazida Android dasturlashdan dars bergan va frilanser sifatida ishlagan. 2021-yil 18-yanvarda Farg'onada Codial akademiyasiga asos solgan. 2021-yil noyabridan Farg'ona maktablarida «#100Maktab» IT seminarlarini o'tkazgan. Hozir Safo bog'chasi (3 filial) va Codial akademiyasi (2 filial, iTeach bilan) rahbari, SayyidSafo arab tili markazi menejeri.

## Tashkilotlar

- Codial akademiyasi (asoschisi): Farg'ona. 2021-yil 18-yanvarda asos solingan. Yo'nalishlar: kompyuter savodxonligi, Vibe Coding (sun'iy intellekt), kiberxavfsizlik, SMM. 500 ga yaqin bitiruvchi. Sayt: {LINKS['codial']}. Telefon: {PHONE_CODIAL}. Telegram: {LINKS['codial_tg']}
- Safo bog'chasi (asoschisi): 3–6 yoshli bolalar uchun bog'cha; tabiiy uy taomlari, milliy tarbiya, 5 yoshdan ingliz tili va mental arifmetika; 3 ta filial. Sayt: {LINKS['safo']}. Telefon: {PHONE_SAFO}. Telegram: {LINKS['safo_tg']}
- SayyidSafo arab tili markazi (menejer): Arab tili ta'limi. Telegram: {LINKS['sayyid_tg']}
"""


def llms():
    s = f"""# {NAME}

> {NAME} ({FULL_NAME}, MNSH) — Marg'ilonlik ta'lim tadbirkori va ustoz. Codial IT akademiyasi va Safo bog'chasi asoschisi, SayyidSafo arab tili markazi menejeri, Inha universiteti bitiruvchisi. Bu — uning rasmiy sayti.

{facts_md()}
## Sahifalar

- [Bosh sahifa]({SITE}/): biografiya, faoliyat, yo'l, savol-javob
- [Fotogalereya]({SITE}/galereya/): 2020–2026 yillardagi suratlar
- [Blog]({SITE}/blog/): so'nggi blog yozuvlari (to'liq matn Telegramda)
- [To'liq ma'lumot (llms-full.txt)]({SITE}/llms-full.txt)

## Rasmiy manbalar

- [Telegram blog @mnshuz]({LINKS['tg_blog']})
- [Telegram @IUTMNSH]({LINKS['tg_personal']})
- [Codial akademiyasi]({LINKS['codial']})
- [Safo bog'chasi]({LINKS['safo']})
- [SayyidSafo Telegram]({LINKS['sayyid_tg']})
"""
    return s


def llms_full():
    s = f"# {NAME} — to'liq ma'lumot\n\n> Rasmiy sayt: {SITE}/ · Yangilangan: {TODAY} · Til: o'zbek (lotin)\n\n{facts_md()}\n## Savol-javob\n\n"
    s += "".join(f"### {q}\n\n{a}\n\n" for q, a in FAQ)
    s += "## So'nggi blog yozuvlari\n\n" + "".join(f"- {p['date']} — [{p['title']}]({p['url']}): {p['excerpt']}\n" for p in BLOG[:36])
    s += "\n## Fotogalereya\n\n" + "".join(f"- {g['date']} — {g['caption']} ({SITE}/{g['large']})\n" for g in GALLERY)
    return s


def feed():
    items = "".join(
        f'<entry><title>{e(p["title"])}</title><link href="{p["url"]}"/><id>{p["url"]}</id><updated>{p["date"]}T00:00:00Z</updated>'
        f'<summary>{e(p["excerpt"])}</summary><author><name>{e(NAME)}</name></author></entry>' for p in BLOG[:36])
    return (f'<?xml version="1.0" encoding="UTF-8"?>\n<feed xmlns="http://www.w3.org/2005/Atom" xml:lang="uz"><title>{e(NAME)} — blog</title>'
            f'<link href="{SITE}/blog/"/><link rel="self" href="{SITE}/feed.xml"/><id>{SITE}/</id><updated>{TODAY}T00:00:00Z</updated>'
            f'<author><name>{e(NAME)}</name></author>{items}</feed>\n')


def manifest():
    return json.dumps({"name": NAME, "short_name": "Muhammad Amin", "lang": "uz", "start_url": BASE + "/", "display": "standalone",
                       "background_color": "#f4f7f3", "theme_color": "#0b7d62",
                       "icons": [{"src": BASE + "/assets/img/icon-192.png", "sizes": "192x192", "type": "image/png"},
                                 {"src": BASE + "/assets/img/icon-512.png", "sizes": "512x512", "type": "image/png"}]},
                      ensure_ascii=False, indent=2)


def write(path, text):
    if BASE and path.endswith(".html"):
        text = re.sub(r'(href|src)="/(?!/)', rf'\1="{BASE}/', text)
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf8", newline="\n") as f:
        f.write(text)


write("index.html", page_index())
write("galereya/index.html", page_gallery())
write("blog/index.html", page_blog())
write("404.html", page_404())
write("robots.txt", robots())
write("sitemap.xml", sitemap())
write("llms.txt", llms())
write("llms-full.txt", llms_full())
write("feed.xml", feed())
write("site.webmanifest", manifest())
print("built for", SITE)
