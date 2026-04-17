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
    """
    Finds the largest contour (the paper), creates a mask of it, 
    and returns both the mask and the 4 detected corners.
    """
    ratio = img.shape[0] / 500.0
    image = cv2.resize(img, (int(img.shape[1] / ratio), 500))
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Using Otsu's thresholding to find the paper against a darker background
    # This is often more robust than Canny for large solid objects
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    contours, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    
    if not contours:
        return None, None
    
    paper_cnt = contours[0]
    
    # Create the full-size mask of the paper
    mask = np.zeros(image.shape[:2], dtype=np.uint8)
    cv2.drawContours(mask, [paper_cnt], -1, 255, -1)
    
    # Erode the mask slightly to "eat" the physical paper edges from the inside.
    # This solves the "curved edge" problem because we follow the actual shape.
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.erode(mask, kernel, iterations=2)
    
    # Find the 4 corners for the perspective warp
    peri = cv2.arcLength(paper_cnt, True)
    approx = cv2.approxPolyDP(paper_cnt, 0.02 * peri, True)
    
    if len(approx) != 4:
        # If not 4 points, get the bounding box as fallback
        rect = cv2.minAreaRect(paper_cnt)
        box = cv2.boxPoints(rect)
        approx = np.int0(box)
    
    # Scale back to original image size
    full_mask = cv2.resize(mask, (img.shape[1], img.shape[0]))
    full_corners = approx.reshape(-1, 2) * ratio
    
    return full_mask, full_corners

def process_image(img_path, output_dir):
    img = cv2.imread(str(img_path))
    if img is None:
        print(f"  [ERROR] Failed to read {img_path.name}")
        return

    # 1. Detect paper, create an eroded mask (to kill edges), and find corners
    mask, pts = get_page_mask_and_corners(img)
    
    if pts is not None and mask is not None:
        # 2. Warp the image and the mask to a perfect rectangle
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
        
        # 3. Transparent Lineart Extraction (from the warped image)
        gray = cv2.cvtColor(warped_img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (99, 99), 0)
        
        # Normalize/Equalize lighting
        norm = gray.astype(np.float32) * 255.0 / (blur.astype(np.float32) + 1e-6)
        inv = 255.0 - norm
        
        # Ink Alpha (transparency of the drawing itself)
        ink_alpha = np.clip(inv * 3.0, 0, 255).astype(np.uint8)
        ink_alpha[ink_alpha < 35] = 0
        
        # 4. Final Alpha = Ink Alpha constrained by the eroded Paper Mask
        # This ensures that ANYTHING outside the "perfectly straight" page edges is 0 alpha.
        final_alpha = cv2.bitwise_and(ink_alpha, warped_mask)
        
        b, g, r = cv2.split(warped_img)
        final_art = cv2.merge((b, g, r, final_alpha))
    else:
        print(f"  [WARNING] Could not detect page boundaries for {img_path.name}, falling back.")
        # Fallback logic if detection fails
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (99, 99), 0)
        norm = gray.astype(np.float32) * 255.0 / (blur.astype(np.float32) + 1e-6)
        inv = 255.0 - norm
        ink_alpha = np.clip(inv * 3.0, 0, 255).astype(np.uint8)
        b, g, r = cv2.split(img)
        final_art = cv2.merge((b, g, r, ink_alpha))

    # Save as PNG
    output_file = output_dir / f"{img_path.stem}.png"
    cv2.imwrite(str(output_file), final_art)
    print("  [Done]")

def process_directory(input_dir, output_dir=None):
    input_path = Path(input_dir)
    if not input_path.exists():
        print(f"Error: Input directory '{input_dir}' does not exist.")
        return
        
    if output_dir is None:
        output_dir = input_path.parent / f"{input_path.name}_processed"
    else:
        output_dir = Path(output_dir)
        
    output_dir.mkdir(parents=True, exist_ok=True)
    images = [f for f in input_path.iterdir() if f.suffix.lower() in {'.jpg', '.jpeg', '.png', '.webp'} and f.is_file()]

    print(f"Directory established: {output_dir}")
    print(f"Found {len(images)} images. Processing with Curved-Edge Removal...\n")

    for count, img_path in enumerate(images, 1):
        print(f"[{count}/{len(images)}] Processing {img_path.name}...")
        process_image(img_path, output_dir)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_folder", nargs="?", default=r"D:\GIT\Web\Hantekeningen.be\albums\Spooky & Sara")
    parser.add_argument("-o", "--output", type=str)
    args = parser.parse_args()
    process_directory(args.input_folder, args.output)
