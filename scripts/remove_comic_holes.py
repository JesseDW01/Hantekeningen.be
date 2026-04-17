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
    if template_path.exists():
        for f in template_path.iterdir():
            if f.suffix.lower() in ['.png', '.jpg', '.jpeg']:
                t = cv2.imread(str(f), cv2.IMREAD_GRAYSCALE)
                if t is not None: templates.append(t)
    return templates

def find_precise_holes(img, templates, page_num=None):
    h, w = img.shape[:2]
    margin_w = int(w * 0.15)
    is_right = (page_num % 2 == 0) if page_num is not None else True
    sides = [w - margin_w] if is_right else [0]
    
    gray = cv2.cvtColor(img[:,:,:3], cv2.COLOR_BGR2GRAY)
    all_hits = []
    
    for x_offset in sides:
        roi = gray[:, x_offset:x_offset+margin_w]
        for t in templates:
            for scale in [0.85, 1.0, 1.15]:
                tw, th = int(t.shape[1]*scale), int(t.shape[0]*scale)
                ts = cv2.resize(t, (tw, th))
                res = cv2.matchTemplate(roi, ts, cv2.TM_CCOEFF_NORMED)
                loc = np.where(res >= 0.45)
                for pt in zip(*loc[::-1]):
                    all_hits.append((pt[0] + x_offset, pt[1], tw, th))

    clusters = []
    for hit in all_hits:
        cx, cy = hit[0] + hit[2]//2, hit[1] + hit[3]//2
        found = False
        for c in clusters:
            if np.linalg.norm(np.array([cx, cy]) - np.array(c['center'])) < 60:
                c['count'] += 1
                found = True
                break
        if not found:
            clusters.append({'center': (cx, cy), 'count': 1, 'size': hit[2]})

    alpha = img[:,:,3]
    final_holes = []
    target_spots = sorted(clusters, key=lambda x: x['count'], reverse=True)[:2]
    
    for spot in target_spots:
        ax, ay = spot['center']
        win = 80
        x1, x2 = max(0, ax-win), min(w, ax+win)
        y1, y2 = max(0, ay-win), min(h, ay+win)
        
        local_alpha = alpha[y1:y2, x1:x2]
        _, local_mask = cv2.threshold(local_alpha, 20, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(local_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            main_cnt = max(contours, key=cv2.contourArea)
            M = cv2.moments(main_cnt)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"]) + x1
                cy = int(M["m01"] / M["m00"]) + y1
                _, radius = cv2.minEnclosingCircle(main_cnt)
                final_holes.append((cx, cy, int(radius) + 12))
            
    return final_holes

def process_image(img_path, output_dir, templates, debug=False):
    try:
        pil_img = Image.open(img_path)
        img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGBA2BGRA)
    except:
        return

    page_match = re.search(r'p(\d+)', img_path.name)
    page_num = int(page_match.group(1)) if page_match else None
    holes = find_precise_holes(img, templates, page_num)
    
    if holes:
        if debug:
            print(f"  [Debug] Found {len(holes)} holes on {img_path.name}")
            overlay = img.copy()
            for h in holes:
                cv2.circle(overlay, (h[0], h[1]), h[2], (0, 255, 0, 150), -1)
            cv2.addWeighted(overlay, 0.5, img, 0.5, 0, img)
        else:
            print(f"  [Healing & Reconstructing] {img_path.name}")
            for h in holes:
                mask = np.zeros(img.shape[:2], dtype=np.uint8)
                cv2.circle(mask, (h[0], h[1]), h[2], 255, -1)
                
                # ART-AWARE RECONSTRUCTION:
                # We inpaint BOTH the RGB and the Alpha channel.
                # This re-connects lines that pass through the hole.
                img[:,:,:3] = cv2.inpaint(img[:,:,:3], mask, 3, cv2.INPAINT_TELEA)
                img[:,:,3] = cv2.inpaint(img[:,:,3], mask, 3, cv2.INPAINT_TELEA)
    else:
        print(f"  [Skip] {img_path.name}")
        
    final_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGRA2RGBA))
    filename = f"verify_{img_path.name}" if debug else img_path.name
    final_pil.save(output_dir / filename)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true", help="Save green verification images instead of healing")
    parser.add_argument("input_folder", nargs="?", default=r"D:\GIT\Web\Hantekeningen.be\albums\Spooky & Sara_processed")
    args = parser.parse_args()
    
    input_path = Path(args.input_folder)
    templates = get_hole_templates()
    if not templates: return

    images = sorted([f for f in input_path.iterdir() if f.suffix.lower() == '.png' and not f.name.startswith('verify_')])
    print(f"Starting Art-Aware Hole Removal | Samples: {len(templates)} | Debug: {args.debug}")
    for path in images:
        process_image(path, input_path, templates, args.debug)

if __name__ == "__main__":
    main()
