# MNSH — Muhammad Amin Naziraliyev rasmiy sayti

Statik sayt (HTML/CSS/JS). Sahifalar `tools/build.py` orqali hosil bo'ladi:

```bash
python tools/build.py https://mnsh.uz
```

- `tools/process_images.py` — suratlarni optimallashtiradi (xom suratlar `images/` papkasida, repoga kiritilmagan)
- `tools/data/` — blog va galereya ma'lumotlari
- `llms.txt`, `robots.txt`, `sitemap.xml`, `feed.xml` — qidiruv tizimlari va sun'iy intellekt uchun

## Joylash

Sayt Hetzner serverida (nginx) `https://mnsh.uz` manzilida ishlaydi. Build qilgach fayllar `/var/www/mnsh.uz` ga ko'chiriladi.
