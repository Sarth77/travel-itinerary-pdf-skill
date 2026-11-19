"""Download hotel photos (Booking.com photo_url from the booking-com search results).
usage: python -I fetch_hotel_photos.py <img_dir> key=URL [key=URL ...]  -> <img_dir>/h_<key>.webp
Tries the larger max1024x768 rendition first, falls back to the given URL.
"""
import os, sys, urllib.request
out = sys.argv[1]; os.makedirs(out, exist_ok=True)
for arg in sys.argv[2:]:
    k, u = arg.split("=", 1)
    for v in [u.replace("square600", "max1024x768").replace("square240", "max1024x768"), u]:
        try:
            d = urllib.request.urlopen(urllib.request.Request(v, headers={"User-Agent": "Mozilla/5.0"}), timeout=30).read()
            open(os.path.join(out, f"h_{k}.webp"), "wb").write(d); print(k, len(d)); break
        except Exception as ex:
            print(k, "fail", ex)
