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
    suspicious_keywords = ["altered", "modified", "urgent payment", "pix boleto"]
    
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

# Function to highlight suspicious areas in an image
def highlight_suspicious_areas(image, text):
    """
    Highlights suspicious areas in the boleto image.
    Returns the marked image and a list of suspicious areas with explanations.
    """
    # Create a copy of the image to mark
    marked_image = image.copy()
    suspicious_areas = []
    
    # Convert to grayscale for processing
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # 1. Check regions with high contrast (possible image joins)
    # Use Sobel filter to detect abrupt changes
    sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
    sobel_magnitude = np.sqrt(sobelx**2 + sobely**2)
    
    # Normalize for visualization
    sobel_magnitude = cv2.normalize(sobel_magnitude, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    
    # Find areas with high contrast
    high_contrast_threshold = 150
    high_contrast_areas = sobel_magnitude > high_contrast_threshold
    
    if np.sum(high_contrast_areas) > 5000:
        # Find contours of high contrast areas
        high_contrast_areas = high_contrast_areas.astype(np.uint8) * 255
        contours, _ = cv2.findContours(high_contrast_areas, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Mark areas of larger size (ignore small artifacts)
        for contour in contours:
            if cv2.contourArea(contour) > 500:
                x, y, w, h = cv2.boundingRect(contour)
                # Draw semi-transparent red rectangle
                overlay = marked_image.copy()
                cv2.rectangle(overlay, (x, y), (x+w, y+h), (0, 0, 255), 2)
                cv2.addWeighted(overlay, 0.4, marked_image, 0.6, 0, marked_image)
                
                suspicious_areas.append({
                    "area": "High contrast region",
                    "explanation": "This area has abrupt contrast changes that may indicate pasted elements.",
                    "coordinates": (x, y, w, h),
                    "confidence": "High"
                })
    
    # 2. Check areas with potentially different fonts
    # This typically requires more advanced OCR, but we can simulate with text detection
    
    # Apply thresholding to isolate text
    _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
    
    # Find text regions
    kernel = np.ones((3, 3), np.uint8)
    binary = cv2.dilate(binary, kernel, iterations=1)
    
    # Find text contours
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Analyze uniformity of text regions
    text_heights = []
    for contour in contours:
        if 100 < cv2.contourArea(contour) < 5000:  # Filter by size to catch characters
            x, y, w, h = cv2.boundingRect(contour)
            text_heights.append(h)
    
    # Check inconsistency in heights (possible font mixing)
    if len(text_heights) > 10:  # Need minimum text for analysis
        text_heights = np.array(text_heights)
        mean_height = np.mean(text_heights)
        std_height = np.std(text_heights)
        
        if std_height / mean_height > 0.4:  # Arbitrary threshold for suspicious variation
            # Mark areas with height very different from mean
            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)
                if abs(h - mean_height) > 2 * std_height and cv2.contourArea(contour) > 100:
                    cv2.rectangle(marked_image, (x, y), (x+w, y+h), (255, 0, 0), 2)
                    
                    suspicious_areas.append({
                        "area": "Inconsistent text",
                        "explanation": "The fonts or text sizes in this area are inconsistent with the rest of the document.",
                        "coordinates": (x, y, w, h),
                        "confidence": "Medium"
                    })
    
    # 3. Look for suspicious words in the text
    fraud_keywords = [
        "pay urgently", "confidential", "urgent", "pay today", 
        "secret", "do not share", "restricted payment"
    ]
    
    for keyword in fraud_keywords:
        if keyword in text.lower():
            # Simple attempt to highlight the word in text
            # In practice, OCR with position would be needed to do this correctly
            suspicious_areas.append({
                "area": f"Suspicious term: '{keyword}'",
                "explanation": "This expression is often used in fraudulent boletos to create urgency.",
                "coordinates": None,
                "confidence": "High"
            })
    
    return marked_image, suspicious_areas
