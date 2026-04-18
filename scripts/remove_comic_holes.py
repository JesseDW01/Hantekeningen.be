import cv2
import numpy as np
import os
import argparse
import re
from pathlib import Path
from PIL import Image

def get_hole_templates():
    templates = []
    template_path = Path(r"D:\GIT\Web\Hantekeningen.be\albums\holes")
    clahe = cv2.createCLAHE(clipLimit=1.5, tileGridSize=(4,4))
    if template_path.exists():
        for f in template_path.iterdir():
            if f.suffix.lower() in ['.png', '.jpg', '.jpeg']:
                t = cv2.imread(str(f), cv2.IMREAD_GRAYSCALE)
                if t is not None:
                    t = clahe.apply(t)
                    templates.append(t)
    return templates

def find_precise_holes(img, templates, page_num=None):
    h, w = img.shape[:2]
    # Scan area: 350px from either edge
    margin_w = min(350, int(w * 0.15)) 
    
    gray = cv2.cvtColor(img[:,:,:3], cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=1.5, tileGridSize=(8,8))
    
    all_hits = []
    
    # SCAN BOTH SIDES: Left (0) and Right (w - margin_w)
    for x_offset in [0, w - margin_w]:
        roi = gray[:, x_offset:x_offset+margin_w]
        roi_enhanced = clahe.apply(roi)
        
        # MIRROR THE SAMPLES for the left side to account for shadow direction
        current_templates = templates
        if x_offset == 0:
            current_templates = [cv2.flip(t, 1) for t in templates]
            
        for t in current_templates:
            for scale in [0.9, 1.0, 1.1]:
                ts = cv2.resize(t, (int(t.shape[1]*scale), int(t.shape[0]*scale)))
                res = cv2.matchTemplate(roi_enhanced, ts, cv2.TM_CCOEFF_NORMED)
                loc = np.where(res >= 0.45)
                for pt in zip(*loc[::-1]):
                    all_hits.append((pt[0] + x_offset, pt[1], ts.shape[1], ts.shape[0], res[pt[1], pt[0]]))

    # Cluster potential holes
    clusters = []
    for hit in all_hits:
        cx, cy = hit[0] + hit[2]//2, hit[1] + hit[3]//2
        if not ((h*0.05 < cy < h*0.45) or (h*0.55 < cy < h*0.95)):
            continue
        found = False
        for c in clusters:
            if np.linalg.norm(np.array([cx, cy]) - np.array(c['center'])) < 50:
                c['score'] = max(c['score'], hit[4])
                found = True
                break
        if not found:
            clusters.append({'center': (cx, cy), 'score': hit[4], 'size': hit[2]})

    # Find the BEST pair anywhere on the page edges
    final_pair = []
    max_combined_score = 0
    for i in range(len(clusters)):
        for j in range(i + 1, len(clusters)):
            p1, p2 = clusters[i]['center'], clusters[j]['center']
            # Alignment check (same X)
            if abs(p1[0] - p2[0]) < 50: 
                dist = abs(p1[1] - p2[1])
                if (h * 0.25) < dist < (h * 0.65):
                    combined = clusters[i]['score'] + clusters[j]['score']
                    if combined > max_combined_score:
                        max_combined_score = combined
                        final_pair = [clusters[i], clusters[j]]

    output = []
    alpha = img[:,:,3]
    for v in final_pair:
        ax, ay = v['center']
        win = 80
        x1, x2, y1, y2 = max(0, ax-win), min(w, ax+win), max(0, ay-win), min(h, ay+win)
        local_alpha = alpha[y1:y2, x1:x2]
        _, m = cv2.threshold(local_alpha, 10, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            cnt = max(contours, key=cv2.contourArea)
            M = cv2.moments(cnt)
            if M["m00"] != 0:
                cx, cy = int(M["m10"]/M["m00"])+x1, int(M["m01"]/M["m00"])+y1
                _, r = cv2.minEnclosingCircle(cnt)
                output.append((cx, cy, int(r) + 5))

    return output

# ... [Everything else remains same] ...
def process_image(img_path, output_dir, templates, debug=False):
    import re
    try:
        pil_img = Image.open(img_path)
        img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGBA2BGRA)
    except: return
    holes = find_precise_holes(img, templates) # No longer need page_num hint
    if holes:
        if debug:
            overlay = img.copy()
            for h in holes: cv2.circle(overlay, (h[0], h[1]), h[2], (0, 255, 0, 150), -1)
            cv2.addWeighted(overlay, 0.5, img, 0.5, 0, img)
        else:
            for h in holes:
                mask = np.zeros(img.shape[:2], dtype=np.uint8)
                cv2.circle(mask, (h[0], h[1]), h[2], 255, -1)
                img[:,:,:3] = cv2.inpaint(img[:,:,:3], mask, 3, cv2.INPAINT_TELEA)
                img[:,:,3] = cv2.inpaint(img[:,:,3], mask, 3, cv2.INPAINT_TELEA)
    final_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGRA2RGBA))
    filename = f"verify_{img_path.name}" if debug else img_path.name
    final_pil.save(output_dir / filename)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("input_folder", nargs="?", default=r"D:\GIT\Web\Hantekeningen.be\albums\Spooky & Sara_processed")
    args = parser.parse_args()
    input_path = Path(args.input_folder)
    templates = get_hole_templates()
    if not templates: return
    images = sorted([f for f in input_path.iterdir() if f.suffix.lower() == '.png' and not f.name.startswith('verify_')])
    print(f"Double-Sided Scan with Mirrored Vision | Samples: {len(templates)}")
    for path in images: process_image(path, input_path, templates, args.debug)

if __name__ == "__main__": main()
