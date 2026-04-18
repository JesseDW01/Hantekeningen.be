import unittest
import cv2
import numpy as np
from pathlib import Path
import remove_comic_holes as det

class TestComicHoleDetection(unittest.TestCase):
    """
    Unit tests to ensure the AI Vision doesn't regress when we update the code.
    """
    
    def setUp(self):
        # Path to our 'Ground Truth' test image
        self.test_img_path = Path(r"D:\GIT\Web\Hantekeningen.be\albums\Spooky & Sara_processed\Gaan naar de bergen - p02.png")
        self.templates = det.get_hole_templates()
        
    def test_page_02_localization(self):
        """
        Verify that holes on page 02 are found within a 50px tolerance of known coordinates.
        """
        # Load image via production fallback
        img = cv2.imread(str(self.test_img_path), cv2.IMREAD_UNCHANGED)
        
        # Run the production detector logic
        holes = det.find_precise_holes(img, self.templates, page_num=2)
        
        # KNOWN GROUND TRUTH for p02
        expected_holes = [
            (2735, 1426), # Top hole
            (2732, 2510)  # Bottom hole
        ]
        
        self.assertEqual(len(holes), 2, "Should find exactly 2 holes on page 02")
        
        for expected in expected_holes:
            # Check if any found hole matches the expected coordinate
            found_match = False
            for h in holes:
                dist = np.linalg.norm(np.array(expected) - np.array(h[:2]))
                if dist < 50: # 50 pixel tolerance
                    found_match = True
                    break
            self.assertTrue(found_match, f"Could not find expected hole at {expected}")

if __name__ == "__main__":
    unittest.main()
