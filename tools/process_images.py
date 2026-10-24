"""Optimise owner + gallery photos into assets/img and write tools/data/gallery.json."""
import json, os
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TG = os.path.join(ROOT, "images", "telegram")
OUT = os.path.join(ROOT, "assets", "img")

OWNER = {
    "hero": ("owner-6.png", "Muhammad Amin Naziraliyev kostyumda, Codial akademiyasi o'quv xonasida"),
    "speaker": ("owner-5.png", "Muhammad Amin Naziraliyev minbarda so'zlamoqda"),
    "reading": ("owner-1.webp", "Muhammad Amin Naziraliyev kitob o'qimoqda"),
    "meeting": ("owner-2.png", "Muhammad Amin Naziraliyev majlisda"),
    "class": ("owner-3.png", "Muhammad Amin Naziraliyev seminar ishtirokchilari orasida"),
    "talk": ("owner-4.png", "Muhammad Amin Naziraliyev suhbat paytida"),
}

# (post id, photo no, caption, alt)
GALLERY = [
    (1022, 1, "Toshkentdagi Inha universiteti bitiruv marosimi", "Inha universiteti bitiruv marosimi, Toshkent"),
    (961, 1, "Marg'ilonlik o'quvchilar bilan Android kursining birinchi bosqichi yakuni", "Android dasturlash kursi o'quvchilari guruhi, Marg'ilon"),
    (1154, 1, "Yoshlar agentligi vakillarining Codial akademiyasiga tashrifi", "Codial akademiyasiga mehmonlar tashrifi, Farg'ona"),
    (1160, 1, "IT-Park tomonidan yoshlar bilan uchrashuv, Raqamli texnologiyalar markazi", "IT-Park yoshlar uchrashuvi ishtirokchilari"),
    (1196, 1, "Codial akademiyasida MeetUp: dasturlashni o'rganishning samarali usullari", "Codial akademiyasi MeetUp ishtirokchilari Farg'onada"),
    (1328, 1, "Yoshlar agentligida «Zamonaviy kasblarning o'rni» seminari", "Farg'ona viloyati Yoshlar agentligidagi seminar"),
    (1331, 1, "Codial akademiyasida seminar ishtirokchilari", "Codial akademiyasi seminari ishtirokchilari"),
    (1544, 1, "#100Maktab loyihasi: Toshloq tumani 2-maktabida IT seminari", "Maktab o'quvchilari uchun IT seminari, Toshloq tumani"),
    (2124, 1, "«Farg'ona yoshlariga IT haqida tushuncha» seminari, Farg'ona", "Maktabdagi IT seminari, Farg'ona"),
    (2400, 1, "Farg'ona shahar maktabida IT seminari", "Farg'ona shahar maktabidagi IT seminari"),
    (2205, 1, "Farg'onada «Biznes marafon 3.0» tadbiri", "Biznes marafon 3.0 tadbiri, Farg'ona"),
    (2241, 1, "Mohirdev platformasi vakillari Codial akademiyasida mehmon", "Mohirdev vakillari bilan suhbat, Codial akademiyasi"),
    (2273, 1, "DevFest 2022 dasturchilar tadbiri", "Google Developer Groups DevFest 2022"),
    (2494, 1, "Inha universiteti rektori Marg'ilonda: Codial filialidagi seminar", "Inha universiteti rektori bilan Marg'ilondagi uchrashuv"),
    (2516, 1, "Toshloq tumani yoshlari uchun tadbir", "Toshloq tumani yoshlari tadbiri"),
    (2523, 1, "Marg'ilonda IT seminari", "Marg'ilon shahridagi IT seminari"),
    (2866, 1, "So'qoq, Begistash: 8 km, 6 soatlik yurish (hiking)", "Tog'da hiking, So'qoq Begistash"),
    (2905, 1, "Qo'qon: O'rda ziyoratgohi", "Qo'qondagi O'rda ziyoratgohi"),
]


def save(im, path, w, q=82):
    im = im.convert("RGB")
    if im.width > w:
        im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    im.save(path, "WEBP", quality=q, method=6)
    return im.size


def main():
    index = {x["post"]: x for x in json.load(open(os.path.join(TG, "index.json"), encoding="utf8"))}
    owner = {}
    for key, (fn, alt) in OWNER.items():
        im = Image.open(os.path.join(ROOT, "images", "owner", fn))
        w, h = save(im, os.path.join(OUT, "owner", f"{key}.webp"), 1000, 86)
        owner[key] = {"file": f"assets/img/owner/{key}.webp", "w": w, "h": h, "alt": alt}
        if key == "hero":
            im.convert("RGB").save(os.path.join(OUT, "owner", "hero.jpg"), quality=88)
    items = []
    for post, no, cap, alt in GALLERY:
        p = index[post]
        src = os.path.join(TG, p["files"][no - 1].replace("/", os.sep))
        im = Image.open(src)
        base = f"{p['date']}-{post}"
        lw, lh = save(im, os.path.join(OUT, "gallery", f"{base}-l.webp"), 1400, 80)
        sw, sh = save(im, os.path.join(OUT, "gallery", f"{base}-s.webp"), 640, 78)
        items.append({
            "date": p["date"], "post": post, "caption": cap, "alt": alt,
            "small": f"assets/img/gallery/{base}-s.webp", "sw": sw, "sh": sh,
            "large": f"assets/img/gallery/{base}-l.webp", "lw": lw, "lh": lh,
            "url": p["url"],
        })
    items.sort(key=lambda x: x["date"], reverse=True)
    json.dump({"owner": owner, "gallery": items}, open(os.path.join(ROOT, "tools", "data", "gallery.json"), "w", encoding="utf8"), ensure_ascii=False, indent=1)
    print(len(items), "gallery items;", owner["hero"])


main()
