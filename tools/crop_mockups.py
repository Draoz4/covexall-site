"""Crop reusable artwork out of the client mockups in creatives/template 1/.

Each entry: (name, box, mode) where box = (x0, y0, x1, y1) in mockup pixels and
mode is 'photo' (keep as-is), 'cut' (remove light background -> transparent) or
'glow' (transparent with glow preserved, for Cove).  Run: python tools/crop_mockups.py
"""
import os, sys, numpy as np, cv2
from PIL import Image, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, '..', 'creatives', 'template 1')
OUT = os.path.join(ROOT, 'assets', 'mk')
os.makedirs(OUT, exist_ok=True)

SPEC = {
 'homepage.png': [
   ('home-place-healthcare', (33,1030,236,1183), 'photo'),
   ('home-place-gyms', (258,1030,462,1183), 'photo'),
   ('home-place-facilities', (488,1030,692,1183), 'photo'),
   ('home-place-education', (714,1030,942,1183), 'photo'),
   ('fam-1', (168,1358,275,1475), 'photo'), ('fam-2', (290,1358,405,1475), 'photo'),
   ('fam-3', (420,1358,530,1475), 'photo'), ('fam-4', (548,1358,675,1475), 'photo'),
   ('fam-5', (688,1358,796,1475), 'photo'), ('fam-6', (818,1358,930,1475), 'photo'),
   ('step-1', (130,640,230,725), 'cut'), ('step-2', (335,640,435,725), 'cut'),
   ('step-3', (540,640,640,725), 'cut'), ('step-4', (740,640,840,725), 'cut'),
   ('proof-kills', (215,1235,270,1280), 'cut'), ('proof-clock', (345,1235,400,1280), 'cut'),
   ('proof-water', (480,1235,522,1280), 'cut'), ('proof-leaf', (596,1235,642,1280), 'cut'),
   ('proof-feather', (710,1235,757,1280), 'cut'), ('proof-shield', (828,1235,877,1280), 'cut'),
 ],
 'all products.png': [
   ('hero-products', (335,55,941,240), 'photo'),
   ('card-pocket', (202,335,410,492), 'photo'), ('card-daily', (426,335,634,492), 'photo'), ('card-family', (650,335,858,492), 'photo'),
   ('cat-pocket', (48,746,245,818), 'photo'), ('cat-daily', (262,746,460,818), 'photo'),
   ('cat-family', (480,746,675,818), 'photo'), ('cat-bundle', (695,746,890,818), 'photo'),
   ('why-1', (95,912,165,966), 'cut'), ('why-2', (265,912,330,966), 'cut'), ('why-3', (440,912,500,966), 'cut'),
   ('why-4', (608,912,672,966), 'cut'), ('why-5', (778,912,842,966), 'cut'),
   ('nl-cove', (45,1470,215,1560), 'glow'),
 ],
 'how it works.png': [
   ('hero-how', (450,60,972,400), 'photo'),
   ('hstep-1', (95,470,200,562), 'cut'), ('hstep-2', (315,470,420,562), 'cut'),
   ('hstep-3', (540,470,640,562), 'cut'), ('hstep-4', (760,470,870,562), 'cut'),
   ('action-video', (62,715,610,1000), 'photo'),
   ('compare-bottle', (68,1085,192,1345), 'cut'),
   ('cta-family', (62,1372,292,1492), 'cut'),
 ],
 'proof and efficacy.png': [
   ('hero-proof', (395,58,1086,392), 'photo'),
   ('pc-1', (100,422,162,466), 'cut'), ('pc-2', (268,422,332,466), 'cut'), ('pc-3', (435,422,500,466), 'cut'),
   ('pc-4', (593,422,657,466), 'cut'), ('pc-5', (748,422,812,466), 'cut'), ('pc-6', (908,422,972,466), 'cut'),
   ('eff-999', (62,578,146,662), 'cut'), ('eff-4h', (158,578,242,662), 'cut'), ('eff-water', (252,578,336,662), 'cut'),
   ('eff-leaf', (347,578,431,662), 'cut'), ('eff-feather', (442,578,526,662), 'cut'),
   ('eff-shield', (70,728,130,780), 'cut'),
   ('why-proof-1', (57,938,205,1072), 'photo'), ('why-proof-2', (385,938,530,1072), 'photo'), ('why-proof-3', (700,938,850,1072), 'photo'),
 ],
 'about us.png': [
   ('hero-about', (480,58,1122,398), 'photo'),
   ('story', (55,428,375,645), 'photo'),
   ('val-1', (118,712,182,778), 'cut'), ('val-2', (313,712,382,778), 'cut'), ('val-3', (508,712,577,778), 'cut'),
   ('val-4', (704,712,768,778), 'cut'), ('val-5', (898,712,963,778), 'cut'),
   ('fact-1', (805,445,850,485), 'cut'), ('fact-2', (805,498,850,538), 'cut'), ('fact-3', (805,548,850,592), 'cut'), ('fact-4', (805,605,850,645), 'cut'),
   ('mission-family', (57,1052,382,1215), 'photo'), ('mission-splash', (790,1052,1035,1215), 'photo'),
   ('strip-1', (55,1243,200,1336), 'photo'), ('strip-2', (222,1243,365,1336), 'photo'), ('strip-3', (390,1243,530,1336), 'photo'),
   ('strip-4', (555,1243,700,1336), 'photo'), ('strip-5', (720,1243,865,1336), 'photo'), ('strip-6', (885,1243,1040,1336), 'photo'),
 ],
 'contact us.png': [
   ('hero-contact', (330,55,1010,385), 'photo'),
   ('footer-splash', (1218,828,1372,990), 'cut'),
   ('contact-family', (1030,625,1315,800), 'cut'),
   ('trust-shield', (75,685,142,752), 'cut'), ('trust-drop', (318,685,385,752), 'cut'), ('trust-badge', (553,685,620,752), 'cut'),
   ('trust-flag', (762,688,818,745), 'cut'), ('trust-heart', (843,685,915,752), 'cut'),
 ],
 'daily defense.png': [
   ('daily-main', (125,65,573,625), 'photo'),
   ('daily-t1', (43,120,125,205), 'photo'), ('daily-t2', (43,220,125,300), 'photo'), ('daily-t3', (43,305,125,390), 'photo'), ('daily-t4', (43,400,125,480), 'photo'),
   ('badge-1', (605,296,662,342), 'cut'), ('badge-2', (688,296,746,342), 'cut'), ('badge-3', (768,296,826,342), 'cut'),
   ('badge-4', (850,296,908,342), 'cut'), ('badge-5', (930,296,988,342), 'cut'),
   ('cove-thumbs', (790,688,995,928), 'glow'),
   ('daily-villains', (55,1090,355,1258), 'cut'),
   ('cust-1', (410,985,505,1085), 'photo'), ('cust-2', (410,1110,505,1215), 'photo'),
   ('teddy', (805,1125,965,1255), 'cut'),
   ('cta-cove', (58,1272,250,1388), 'glow'), ('cta-kit', (468,1282,685,1388), 'cut'),
 ],
 'family size.png': [
   ('family-main', (150,60,640,562), 'photo'),
   ('family-t1', (50,110,135,195), 'photo'), ('family-t2', (50,200,135,285), 'photo'), ('family-t3', (50,290,135,375), 'photo'),
   ('family-t4', (50,380,135,465), 'photo'), ('family-t5', (50,470,135,552), 'photo'),
   ('big-1', (250,596,330,668), 'cut'), ('big-2', (352,596,432,668), 'cut'), ('big-3', (458,596,538,668), 'cut'), ('big-4', (562,596,642,668), 'cut'),
   ('family-photo', (680,585,975,745), 'photo'),
   ('video-thumb', (360,800,615,935), 'photo'),
   ('hiw-1', (718,802,772,852), 'cut'), ('hiw-2', (718,855,772,905), 'cut'), ('hiw-3', (718,905,772,955), 'cut'), ('hiw-4', (718,958,772,1010), 'cut'),
   ('seal-1', (55,935,112,968), 'cut'), ('seal-2', (123,935,182,968), 'cut'), ('seal-3', (193,935,247,968), 'cut'), ('seal-4', (263,935,317,968), 'cut'),
   ('mission-photo', (50,1208,322,1352), 'photo'), ('mission-crew', (658,1208,805,1352), 'cut'),
 ],
 'education.png': [
   ('hero-education', (355,60,1024,432), 'photo'),
   ('topic-1', (75,478,168,572), 'cut'), ('topic-2', (238,478,322,572), 'cut'), ('topic-3', (388,478,472,572), 'cut'),
   ('topic-4', (545,478,628,572), 'cut'), ('topic-5', (698,478,792,572), 'cut'), ('topic-6', (858,478,952,572), 'cut'),
   ('cove-reading', (42,735,250,942), 'glow'), ('chalkboard', (522,742,982,938), 'photo'),
   ('tip-1', (58,1003,142,1142), 'photo'), ('tip-2', (238,1003,322,1142), 'photo'), ('tip-3', (418,1003,502,1142), 'photo'),
   ('educators', (815,985,975,1145), 'cut'),
   ('dyk-1', (88,1230,152,1286), 'cut'), ('dyk-2', (215,1230,275,1286), 'cut'), ('dyk-3', (345,1230,412,1286), 'cut'), ('dyk-4', (480,1230,535,1286), 'cut'),
   ('cove-wave', (805,1183,985,1343), 'glow'),
 ],
 'pocket sanitizer.png': [
   ('pocket-main', (122,85,673,472), 'photo'),
   ('pocket-t1', (50,85,112,180), 'photo'), ('pocket-t2', (50,185,112,280), 'photo'), ('pocket-t3', (50,285,112,380), 'photo'), ('pocket-t4', (50,385,112,475), 'photo'),
   ('cove-bottle', (118,478,322,642), 'glow'),
   ('little-viro', (636,525,705,588), 'cut'), ('little-4h', (772,522,838,592), 'cut'), ('little-bac', (942,522,1012,588), 'cut'),
   ('ps-1', (85,696,148,750), 'cut'), ('ps-2', (208,696,272,750), 'cut'), ('ps-3', (328,696,392,750), 'cut'), ('ps-4', (453,696,517,750), 'cut'),
   ('pw-1', (583,694,643,740), 'cut'), ('pw-2', (688,694,748,740), 'cut'), ('pw-3', (793,694,853,740), 'cut'), ('pw-4', (898,694,958,740), 'cut'), ('pw-5', (1002,694,1060,740), 'cut'),
   ('moment-1', (175,855,355,992), 'photo'), ('moment-2', (490,855,712,992), 'photo'), ('moment-3', (845,855,1075,992), 'photo'),
   ('also-1', (488,1178,558,1252), 'cut'), ('also-2', (688,1178,758,1252), 'cut'), ('also-3', (885,1178,962,1252), 'cut'),
   ('pocket-nl-cove', (95,1255,230,1335), 'glow'),
 ],
 'faq.png': [
   ('hero-faq', (305,58,864,612), 'photo'),
   ('germ-1', (58,1198,122,1262), 'cut'), ('germ-2', (158,1198,220,1262), 'cut'), ('germ-3', (258,1198,320,1262), 'cut'),
   ('germ-4', (358,1198,420,1262), 'cut'), ('germ-5', (462,1198,525,1262), 'cut'),
   ('faq-cove', (560,1070,835,1385), 'glow'),
   ('faq-bottles', (662,1438,805,1545), 'cut'),
   ('ft-1', (48,1458,105,1522), 'cut'), ('ft-2', (270,1458,325,1522), 'cut'), ('ft-3', (508,1458,565,1522), 'cut'),
 ],
}

def flood(rgb, tol):
    h, w, _ = rgb.shape; img = rgb.copy(); mask = np.zeros((h+2, w+2), np.uint8)
    flags = 4 | (255 << 8) | cv2.FLOODFILL_MASK_ONLY | cv2.FLOODFILL_FIXED_RANGE
    for s in [(0,0),(w-1,0),(0,h-1),(w-1,h-1),(w//2,0),(0,h//2),(w-1,h//2),(w//2,h-1)]:
        cv2.floodFill(img, mask, s, (0,0,0), (tol,)*3, (tol,)*3, flags)
    return mask[1:-1, 1:-1] > 0

def cut(rgb, tol=30):
    bg = flood(rgb, tol)
    a = (~bg * 255).astype(np.uint8)
    a = cv2.morphologyEx(a, cv2.MORPH_OPEN, np.ones((3,3), np.uint8))
    a = cv2.GaussianBlur(a, (0,0), 1.0)
    return np.dstack([rgb, a])

def glow(rgb):
    f = rgb.astype(np.float32) / 255
    bg = flood(rgb, 16)
    body = cv2.GaussianBlur((~bg * 255).astype(np.uint8), (0,0), 2).astype(np.float32) / 255
    halo = cv2.GaussianBlur((~bg * 255).astype(np.uint8), (0,0), 25).astype(np.float32) / 255
    g = np.clip((1 - f.min(axis=2)) * 1.6, 0, 1) * np.clip(halo * 2, 0, 1)
    a = np.maximum(body, g)
    return np.dstack([rgb, (a * 255).astype(np.uint8)])

def upscale(im, factor=2):
    im = im.resize((im.width * factor, im.height * factor), Image.LANCZOS)
    return im.filter(ImageFilter.UnsharpMask(radius=1.2, percent=60, threshold=2))

only = sys.argv[1:]
for fname, items in SPEC.items():
    src = Image.open(os.path.join(SRC, fname)).convert('RGB')
    for name, box, mode in items:
        if only and not any(name.startswith(o) for o in only): continue
        crop = src.crop(box)
        if mode == 'photo':
            im = upscale(crop) if crop.width < 700 else crop
            im.save(os.path.join(OUT, name + '.webp'), quality=86, method=6)
        else:
            rgb = np.array(crop)
            rgba = cut(rgb) if mode == 'cut' else glow(rgb)
            im = Image.fromarray(rgba, 'RGBA')
            bbox = im.getchannel('A').point(lambda v: 255 if v > 8 else 0).getbbox()
            if bbox: im = im.crop(bbox)
            im = upscale(im) if im.width < 400 else im
            im.save(os.path.join(OUT, name + '.webp'), quality=90, method=6)
    print('done', fname)
