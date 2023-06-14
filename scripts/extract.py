import pytesseract
import cv2
import numpy as np

class PY_TESSERACT:
    def __init__(self) -> None:
        self.img: bytes = ''
        self.result: str = ''
        self.config: str = '--oem 3 --psm 6'

    def load_image_from_bytes(self, img='400.jpeg') -> None:
        img_np = np.frombuffer(img, dtype=np.uint8)
        self.img = cv2.imdecode(img_np, flags=1)
        self.img = cv2.resize(self.img, None, fx=2, fy=2)
        self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
    
    def extract(self) -> None:
        self.result = pytesseract.image_to_string(self.img, config=self.config, lang='eng')
        return self.result
