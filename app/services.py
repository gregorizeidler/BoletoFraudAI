import cv2
import pytesseract
import numpy as np
from app.utils import validate_boleto_code, check_common_fraud_patterns, detect_image_manipulation, highlight_suspicious_areas

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
        
        # New functionality: highlight suspicious areas and get explanations
        marked_image, suspicious_areas = highlight_suspicious_areas(image, extracted_text)

        # Check fraud indicators
        is_fraud = not is_valid or fraud_patterns or manipulation_detected
        reasons = []
        if not is_valid:
            reasons.append(f"Invalid barcode: {message}")
        if fraud_patterns:
            reasons.append("Suspicious keywords found in text")
        if manipulation_detected:
            reasons.append("Potential image manipulation detected")

        # Final result with more information
        return {
            "fraud_detected": is_fraud, 
            "message": " | ".join(reasons) if is_fraud else "Boleto appears to be valid.",
            "marked_image": marked_image,  # Image with suspicious areas highlighted
            "suspicious_areas": suspicious_areas,  # List of suspicious areas with explanations
            "extracted_text": extracted_text,  # Text extracted from boleto
            "fraud_details": {
                "invalid_barcode": not is_valid,
                "suspicious_keywords": fraud_patterns,
                "image_manipulation": manipulation_detected
            }
        }
    
    except Exception as e:
        return {
            "fraud_detected": True, 
            "message": f"Error processing boleto: {str(e)}",
            "marked_image": image,
            "suspicious_areas": [],
            "extracted_text": "",
            "fraud_details": {
                "invalid_barcode": False,
                "suspicious_keywords": False,
                "image_manipulation": False,
                "error": str(e)
            }
        }
