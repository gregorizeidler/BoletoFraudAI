import cv2
import pytesseract
import numpy as np
from app.utils import validate_boleto_code, check_common_fraud_patterns, detect_image_manipulation

def analyze_boleto(image):
    try:
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Apply OCR
        extracted_text = pytesseract.image_to_string(gray)

        # Validate barcode and fraud checks
        is_valid, message = validate_boleto_code(extracted_text)
        fraud_patterns = check_common_fraud_patterns(extracted_text)
        manipulation_detected = detect_image_manipulation(image)

        # Check fraud indicators
        if not is_valid or fraud_patterns or manipulation_detected:
            reasons = []
            if not is_valid:
                reasons.append(f"Invalid barcode: {message}")
            if fraud_patterns:
                reasons.append("Suspicious keywords found in text")
            if manipulation_detected:
                reasons.append("Potential image manipulation detected")

            return {"fraud_detected": True, "message": " | ".join(reasons)}
        
        return {"fraud_detected": False, "message": "Boleto appears to be valid."}
    
    except Exception as e:
        return {"fraud_detected": True, "message": f"Error processing boleto: {str(e)}"}
