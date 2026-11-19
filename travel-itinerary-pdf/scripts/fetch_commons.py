"""Download destination photos from Wikimedia Commons and record credits.
usage: python -I fetch_commons.py <img_dir> <queries.json>
queries.json = {"key": "search text", ...}  -> saves <img_dir>/d_<key>.jpg
Skips keys already downloaded. Backs off on HTTP 429. Merges credits into <img_dir>/credits.json.
"""
import json, os, sys, time, urllib.parse, urllib.request, urllib.error
out, qfile = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
Q = json.load(open(qfile))
UA = {"User-Agent": "itinerary-builder/1.0 (personal use)"}
cpath = os.path.join(out, "credits.json")
credits = json.load(open(cpath)) if os.path.exists(cpath) else {}

def get(url, tries=4):
    for i in range(tries):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40).read()
        except urllib.error.HTTPError as ex:
            if ex.code == 429 and i < tries - 1:
                time.sleep(15 * (i + 1)); continue
            raise

for k, q in Q.items():
    if os.path.exists(os.path.join(out, f"d_{k}.jpg")):
        continue
    try:
        p = {"action": "query", "format": "json", "generator": "search", "gsrsearch": q + " filetype:bitmap",
             "gsrnamespace": 6, "gsrlimit": 5, "prop": "imageinfo", "iiprop": "url|extmetadata|size", "iiurlwidth": 1200}
        r = json.loads(get("https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(p)))
        pages = sorted(r.get("query", {}).get("pages", {}).values(), key=lambda x: x.get("index", 9))
        for pg in pages:
            ii = pg["imageinfo"][0]
            if ii.get("width", 0) < 800:
                continue
            open(os.path.join(out, f"d_{k}.jpg"), "wb").write(get(ii["thumburl"]))
            em = ii.get("extmetadata", {})
            credits[k] = {"title": pg["title"], "artist": em.get("Artist", {}).get("value", ""),
                          "license": em.get("LicenseShortName", {}).get("value", "")}
            print(k, "<-", pg["title"]); break
        else:
            print(k, "NONE", [x["title"] for x in pages])
    except Exception as ex:
        print(k, "ERR", ex)
    json.dump(credits, open(cpath, "w"), indent=1)
    time.sleep(3)
