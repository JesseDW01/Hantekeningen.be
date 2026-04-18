import cv2
import numpy as np
from PIL import Image
from pathlib import Path

TEST_FILE = r"D:\GIT\Web\Hantekeningen.be\albums\Spooky & Sara_processed\Gaan naar de bergen - p02.png"
DATABANK = r"D:\GIT\Web\Hantekeningen.be\albums\holes"
OUTPUT_FILE = r"D:\GIT\Web\Hantekeningen.be\scripts\verify_p02.png"

def test_tight_precision():
    print(f"Loading page: {TEST_FILE}")
    try:
        pil_img = Image.open(TEST_FILE)
        img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGBA2BGRA)
    except Exception as e:
        print(f"Error: {e}")
        return

    h, w = img.shape[:2]
    templates = []
    for f in Path(DATABANK).iterdir():
        if f.suffix.lower() in ['.png', '.jpg']:
            t = cv2.imread(str(f), cv2.IMREAD_GRAYSCALE)
            if t is not None: templates.append(t)
    
    gray = cv2.cvtColor(img[:,:,:3], cv2.COLOR_BGR2GRAY)
    margin_w = int(w * 0.15)
    roi_gray = gray[:, w-margin_w:]
    
    hits = []
    for t in templates:
        for scale in [0.85, 1.0, 1.15]:
            ts = cv2.resize(t, (int(t.shape[1]*scale), int(t.shape[0]*scale)))
            res = cv2.matchTemplate(roi_gray, ts, cv2.TM_CCOEFF_NORMED)
            loc = np.where(res >= 0.45)
            for pt in zip(*loc[::-1]):
                hits.append((pt[0] + (w - margin_w), pt[1], ts.shape[1], ts.shape[0]))

    clusters = []
    for h_item in hits:
        cx, cy = h_item[0] + h_item[2]//2, h_item[1] + h_item[3]//2
        found = False
        for c in clusters:
            if np.linalg.norm(np.array([cx, cy]) - np.array(c['center'])) < 60:
                c['count'] += 1
                found = True
                break
        if not found:
            clusters.append({'center': (cx, cy), 'count': 1, 'size': h_item[2]})

    target_spots = sorted(clusters, key=lambda x: x['count'], reverse=True)[:2]

    # PRECISION STAGE: Shrink-wrap the hole shadow
    alpha = img[:,:,3]
    debug_overlay = img.copy()
    
    for spot in target_spots:
        ax, ay = spot['center']
        win = 100
        x1, x2 = max(0, ax-win), min(w, ax+win)
        y1, y2 = max(0, ay-win), min(h, ay+win)
        
        local_alpha = alpha[y1:y2, x1:x2]
        # Find the actual shadow pixels
        _, local_mask = cv2.threshold(local_alpha, 20, 255, cv2.THRESH_BINARY)
        
        # Draw a tight circle based on the actual shadow extent
        contours, _ = cv2.findContours(local_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            # Pick the largest blob (the hole shadow) inside our candidate window
            main_cnt = max(contours, key=cv2.contourArea)
            (lx, ly), l_radius = cv2.minEnclosingCircle(main_cnt)
            
            final_x = int(lx) + x1
            final_y = int(ly) + y1
            # Narrow radius: only 15 pixels padding
            final_r = int(l_radius) + 15
            
            print(f"  [Tight-Fit] Located shadow with precision radius: {final_r}")
            cv2.circle(debug_overlay, (final_x, final_y), final_r, (0, 255, 0, 160), -1)

    cv2.addWeighted(debug_overlay, 0.5, img, 0.5, 0, img)
    final_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGRA2RGBA))
    final_pil.save(OUTPUT_FILE)
    print(f"Tight-Fit verification created: {OUTPUT_FILE}")

if __name__ == "__main__":
    test_tight_precision()
