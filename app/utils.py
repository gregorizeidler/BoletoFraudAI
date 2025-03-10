import cv2
import numpy as np
import re

def validate_boleto_code(text):
    """Validate boleto barcode format."""
    boleto_pattern = re.compile(r"\d{47,48}")
    match = boleto_pattern.search(text)
    
    if not match:
        return False, "Invalid barcode format"
    
    return True, "Valid boleto format"

def check_common_fraud_patterns(text):
    """Check for fraud patterns (e.g., altered boleto)."""
    suspicious_keywords = ["alterado", "modificado", "pagamento urgente", "pix boleto"]
    
    for keyword in suspicious_keywords:
        if keyword.lower() in text.lower():
            return True
    
    return False

def detect_image_manipulation(image):
    """Detects possible image manipulation (edited boleto)."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Edge detection
    edges = cv2.Canny(gray, 50, 150)

    # Pixel density variation analysis
    blurred = cv2.GaussianBlur(gray, (5,5), 0)
    diff = cv2.absdiff(gray, blurred)
    _, thresholded = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)

    # Calculate manipulation score
    manipulation_score = np.sum(thresholded) / np.sum(gray)

    # If manipulation score is too high, flag it as suspicious
    return manipulation_score > 0.1
