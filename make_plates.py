#!/usr/bin/env python3
"""Storyboard strips for BEING A SELF PUBLISHER.
Pencil on warm cream paper, in the BRAIN BRAKE hand. Three panels per chapter.
NOTE: these are LIGHT images. Do not run seat_plates.py on them — the paper
compositor dissolves bright paper into the page background and would erase
the entire drawing."""
import json, base64, os, sys, time, urllib.request
KEY = open('/home/claude/.secret/gemini_key').read().strip()
URL = ("https://generativelanguage.googleapis.com/v1beta/models/"
       "gemini-3-pro-image-preview:generateContent")
OUT = '/home/claude/SOAK_YOUR_NUTS/images'

STYLE = (
    "Loose watercolour on textured paper, warm and sunlit. Earth palette only: "
    "terracotta, ochre, warm clay, olive green, raw linen, honey and soft cream. "
    "One clear source of warm daylight coming in from one side, long soft shadows. "
    "Loose wet brushwork, visible paper grain, soft bleeding edges, generous empty "
    "space. Calm, unhurried, handmade, quietly abundant. Wooden tables, clay and "
    "ceramic vessels, linen cloth, glass jars, growing plants. "
    "The painting fills the entire frame edge to edge with no white paper border. "
    "Absolutely no text, no letters, no words, no numbers, no labels and no "
    "signage anywhere in the image. SCENE: "
)

SCENES = {
 "00_hero": "a wide shallow clay bowl of almonds submerged in clear water on a sunlit wooden table, morning light raking across the surface of the water, a linen cloth folded beside it",
 "01_practice": "a row of glass jars of different nuts soaking in water along a sunlit windowsill, a green plant beside them, soft shadows across the sill",
 "02_tradition": "two open hands cupping a small heap of nuts in warm daylight, seen from above over a wooden table",
 "03_water": "a clay jug pouring a clear stream of water into a wide bowl of nuts, sunlight catching the falling water",
 "04_dry": "wooden drying trays stacked in warm light with nuts spread evenly across them, warm air suggested by soft haze",
 "05_safe": "a clean sunlit kitchen counter with a scrubbed wooden board, a glass bowl and a folded white linen cloth, everything orderly and empty",
 "06_bynut": "many small clay dishes arranged in a grid on a sunlit table, each holding a different kind of nut, seen from above",
 "07_exception": "three clay dishes slightly apart from a larger group on a wooden table, sunlight picking out the three",
 "08_nutrition": "a single nut split open in cross section resting on warm linen, strong side light showing its inner structure",
 "09_storage": "sealed glass jars of dried nuts standing in a cool dim pantry, one shaft of warm daylight entering from the side",
 "10_butter": "a small kitchen blender on a sunlit wooden counter beside an open jar of thick pale nut butter and a wooden spoon, a linen cloth nearby",
 "11_seeds": "shallow woven baskets of pumpkin seeds, sunflower seeds and buckwheat on a sunlit table, seen from above",
 "12_kitchen": "a calm open kitchen doorway looking out onto green growing things in strong warm daylight, jars and bowls on the table in the foreground",
}

def paint(name, scene, retries=3):
    body = json.dumps({
        "contents": [{"parts": [{"text": STYLE + scene}]}],
        "generationConfig": {"responseModalities": ["IMAGE"],
                             "imageConfig": {"aspectRatio": "16:9"}},
    }).encode()
    for attempt in range(retries):
        req = urllib.request.Request(URL, data=body, headers={
            "x-goog-api-key": KEY, "Content-Type": "application/json",
            "User-Agent": "mantra-field-books/1.0"})
        try:
            with urllib.request.urlopen(req, timeout=240) as r:
                d = json.load(r)
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(20 * (attempt + 1)); continue
            print(f"  {name}: HTTP {e.code}"); return False
        for p in d["candidates"][0]["content"]["parts"]:
            if "inlineData" in p:
                raw = base64.b64decode(p["inlineData"]["data"])
                open(f"{OUT}/{name}.jpg", "wb").write(raw)
                print(f"  {name}: {len(raw)//1024} KB"); return True
        print(f"  {name}: no image part"); time.sleep(5)
    return False

if __name__ == "__main__":
    want = sys.argv[1:] or list(SCENES)
    ok = 0
    for n in want:
        if os.path.exists(f"{OUT}/{n}.jpg"):
            print(f"  {n}: already painted"); ok += 1; continue
        if paint(n, SCENES[n]): ok += 1
        time.sleep(2)
    print(f"painted {ok}/{len(want)}")
