import cv2
import numpy as np
import os
import csv
import sys
import logging
import time
from pathlib import Path
from PIL import Image

# Set up structured logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger("AuditBot")

# Add scripts folder to path
sys.path.append(str(Path(__file__).parent.parent / "scripts"))
try:
    import remove_comic_holes as production_det
except ImportError:
    logger.error("Could not find production script in ../scripts/remove_comic_holes.py")
    sys.exit(1)

def run_audit():
    test_dir = Path(__file__).parent
    data_dir = test_dir / "data"
    output_dir = test_dir / "verification"
    csv_path = test_dir / "hole_audit.csv"
    
    output_dir.mkdir(exist_ok=True)
    
    templates = production_det.get_hole_templates()
    if not templates:
        logger.error("No hole samples found in databank!")
        return

    images = sorted([f for f in data_dir.iterdir() if f.suffix.lower() == '.png'])
    total_imgs = len(images)
    
    logger.info(f"Starting Localization Audit | Files: {total_imgs} | Samples: {len(templates)}")
    start_time = time.time()
    
    audit_data = []
    processed_count = 0
    
    try:
        for idx, img_path in enumerate(images):
            percent = (idx + 1) / total_imgs * 100
            file_info = f"[{idx+1}/{total_imgs}] {img_path.name}"
            
            try:
                pil_img = Image.open(img_path)
                img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGBA2BGRA)
            except Exception as e:
                logger.error(f"{file_info} - Failed to read: {e}")
                continue
                
            import re
            page_match = re.search(r'p(\d+)', img_path.name)
            page_num = int(page_match.group(1)) if page_match else None
            
            # Run the production detection
            holes = production_det.find_precise_holes(img, templates, page_num)
            
            if holes:
                for h_idx, h in enumerate(holes):
                    audit_data.append({
                        'filename': img_path.name,
                        'hole_id': h_idx + 1,
                        'x': h[0],
                        'y': h[1],
                        'radius': h[2]
                    })
                
                # Visual Verification
                overlay = img.copy()
                for h in holes:
                    cv2.circle(overlay, (h[0], h[1]), h[2], (0, 255, 0, 150), -1)
                cv2.addWeighted(overlay, 0.5, img, 0.5, 0, img)
                final_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGRA2RGBA))
                final_pil.save(output_dir / f"audit_{img_path.name}")
                logger.info(f"{file_info} - OK ({len(holes)} holes found)")
            else:
                logger.warning(f"{file_info} - NO HOLES DETECTED")
            
            processed_count += 1

    except KeyboardInterrupt:
        logger.warning("\nAudit interrupted by user! Saving partial results...")

    # Always save what we found
    if audit_data:
        with open(csv_path, mode='w', newline='') as csvfile:
            fieldnames = ['filename', 'hole_id', 'x', 'y', 'radius']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(audit_data)
        
    duration = time.time() - start_time
    logger.info("=" * 40)
    logger.info(f"AUDIT COMPLETE")
    logger.info(f"Time Taken: {duration:.1f} seconds")
    logger.info(f"Pages Audited: {processed_count}")
    logger.info(f"CSV Report: {csv_path}")
    logger.info("=" * 40)

if __name__ == "__main__":
    run_audit()
