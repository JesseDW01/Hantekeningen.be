import cv2
import numpy as np
import os
import argparse
from pathlib import Path

def order_points(pts):
    rect = np.zeros((4, 2), dtype="float32")
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    return rect

def get_page_mask_and_corners(img):
    ratio = img.shape[0] / 500.0
    image = cv2.resize(img, (int(img.shape[1] / ratio), 500))
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    contours, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    if not contours: return None, None
    paper_cnt = contours[0]
    
    peri = cv2.arcLength(paper_cnt, True)
    approx = cv2.approxPolyDP(paper_cnt, 0.01 * peri, True)
    if len(approx) != 4:
        rect = cv2.minAreaRect(paper_cnt)
        approx = np.intp(cv2.boxPoints(rect))
    
    mask = np.zeros(image.shape[:2], dtype=np.uint8)
    cv2.drawContours(mask, [paper_cnt], -1, 255, -1)
    
    # Minimal 1px erosion for edge cleanup
    kernel = np.ones((3, 3), np.uint8)
    mask = cv2.erode(mask, kernel, iterations=1)
    
    full_mask = cv2.resize(mask, (img.shape[1], img.shape[0]))
    return full_mask, approx.reshape(-1, 2) * ratio

def process_image(img_path, output_dir, mode="color"):
    img = cv2.imread(str(img_path))
    if img is None: return

    mask, pts = get_page_mask_and_corners(img)
    if pts is not None and mask is not None:
        rect = order_points(pts)
        (tl, tr, br, bl) = rect
        width = int(max(np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2)),
                        np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))))
        height = int(max(np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2)),
                         np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))))
        
        dst = np.array([[0, 0], [width - 1, 0], [width - 1, height - 1], [0, height - 1]], dtype="float32")
        M = cv2.getPerspectiveTransform(rect, dst)
        warped_img = cv2.warpPerspective(img, M, (width, height))
        warped_mask = cv2.warpPerspective(mask, M, (width, height))
        
        gray_warped = cv2.cvtColor(warped_img, cv2.COLOR_BGR2GRAY)
        blur_gray = cv2.GaussianBlur(gray_warped, (99, 99), 0)
        blur_bgr = cv2.cvtColor(blur_gray, cv2.COLOR_GRAY2BGR).astype(np.float32) + 1e-6
        
        # Color normalization
        processed_rgb = warped_img.astype(np.float32) * 255.0 / blur_bgr
        processed_rgb = 255.0 - ((255.0 - processed_rgb) * 1.15)
        processed_rgb = np.clip(processed_rgb, 0, 255).astype(np.uint8)
        
        if mode == "bw":
            processed_rgb = cv2.cvtColor(processed_rgb, cv2.COLOR_BGR2GRAY)
            processed_rgb = cv2.cvtColor(processed_rgb, cv2.COLOR_GRAY2BGR)

        # Alpha Extraction
        norm_gray = gray_warped.astype(np.float32) * 255.0 / (blur_gray.astype(np.float32) + 1e-6)
        inv = 255.0 - norm_gray
        ink_alpha = np.clip(inv * 2.2, 0, 255).astype(np.uint8)
        final_alpha = cv2.bitwise_and(ink_alpha, warped_mask)
        
        b, g, r = cv2.split(processed_rgb)
        final_art = cv2.merge((b, g, r, final_alpha))
    else:
        final_art = img

    cv2.imwrite(str(output_dir / f"{img_path.stem}.png"), final_art)
    print(f"  [Done] {img_path.name}")

def process_directory(input_dir, output_dir=None, mode="color"):
    input_path = Path(input_dir)
    if not input_path.exists(): return
    out_dir = input_path.parent / f"{input_path.name}_processed" if output_dir is None else Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    images = [f for f in input_path.iterdir() if f.suffix.lower() in {'.jpg', '.jpeg', '.png', '.webp'} and f.is_file()]
    print(f"Target: {out_dir} | Mode: {mode.upper()}")
    for img_path in images:
        process_image(img_path, out_dir, mode=mode)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_folder", nargs="?", default=None, help="Folder to process. Defaults to all folders in 'albums/'")
    parser.add_argument("-o", "--output", type=str)
    parser.add_argument("--bw", action="store_true")
    args = parser.parse_args()

    albums_root = Path(r"D:\GIT\Web\Hantekeningen.be\albums")
    
    if args.input_folder:
        process_directory(args.input_folder, args.output, mode="bw" if args.bw else "color")
    else:
        print(f"No input folder specified. Scanning {albums_root}...")
        for folder in sorted(albums_root.iterdir()):
            if folder.is_dir() and folder.name != "holes" and not folder.name.endswith("_processed"):
                process_directory(folder, args.output, mode="bw" if args.bw else "color")
