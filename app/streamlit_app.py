import streamlit as st
import requests
from PIL import Image
import io
import numpy as np
import cv2
import os
from PIL import Image as PILImage

# Title and application description
st.set_page_config(page_title="BoletoFraudAI - Fake Boleto Detector", page_icon="🔍")
st.title("🔍 BoletoFraudAI")
st.subheader("AI-powered Fake Boleto Detector")

# Function to analyze boleto directly (without calling external API)
def analyze_boleto_local(image_bytes):
    from app.services import analyze_boleto
    
    # Convert bytes to numpy array
    np_arr = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    
    # Analyze with existing function
    result = analyze_boleto(image)
    return result

# Function to convert from OpenCV to PIL (for display in Streamlit)
def cv2_to_pil(cv2_image):
    cv2_image_rgb = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB)
    return PILImage.fromarray(cv2_image_rgb)

# Function to display educational explanations about fraud types
def show_fraud_education():
    st.subheader("How Boleto Fraud Happens")
    
    fraud_types = {
        "Barcode Manipulation": {
            "description": "Fraudsters alter barcode digits to redirect payment to a different account.",
            "indicators": ["Irregular numbers", "Inconsistent spacing", "Varied print quality"],
            "prevention": "Always check the barcode against the printed number on the boleto."
        },
        "Payee Data Alteration": {
            "description": "The payee name and data are altered, usually with cut and paste of text.",
            "indicators": ["Different fonts in the same document", "Irregular alignment", "Areas with different resolutions"],
            "prevention": "Verify if the payee is indeed who you expect to make the payment to."
        },
        "Logo Counterfeiting": {
            "description": "Use of bank or company logos to give the appearance of legitimacy.",
            "indicators": ["Blurry logos", "Slightly different colors", "Non-standard positioning"],
            "prevention": "Compare with previous boletos from the same company or check the official website."
        },
        "Urgency and Psychological Pressure": {
            "description": "Use of terms that create a sense of urgency to induce payment without proper verification.",
            "indicators": ["'Pay today without fail'", "'Urgent'", "'Avoid severe penalties'", "'Final notice'"],
            "prevention": "Be suspicious of communications that pressure for immediate payment without chance for verification."
        }
    }
    
    for fraud_type, details in fraud_types.items():
        with st.expander(f"🔍 {fraud_type}"):
            st.markdown(f"**What it is:** {details['description']}")
            
            st.markdown("**Warning signs:**")
            for indicator in details['indicators']:
                st.markdown(f"- {indicator}")
                
            st.markdown(f"**How to protect yourself:** {details['prevention']}")

# Initialize session state to control when to clear
if 'analysis_complete' not in st.session_state:
    st.session_state.analysis_complete = False
if 'original_image' not in st.session_state:
    st.session_state.original_image = None

# Function to clear analysis and return to initial state
def clear_analysis():
    st.session_state.analysis_complete = False
    st.session_state.original_image = None
    st.rerun()

# Sidebar with information
with st.sidebar:
    st.title("About")
    st.info(
        "BoletoFraudAI is an AI-powered fraud detection system that analyzes "
        "Brazilian payment slips (boletos) to identify fake, tampered, or "
        "manipulated documents before payment."
    )
    
    st.title("How it Works")
    st.write("""
    1. Upload the boleto image
    2. Our system analyzes it using OCR and image processing
    3. Get the analysis results instantly
    """)
    
    # Show educational information about fraud
    show_fraud_education()

# Show upload or previous analysis result
if not st.session_state.analysis_complete:
    # File upload
    uploaded_file = st.file_uploader("Upload boleto image", type=["jpg", "jpeg", "png"])

    # Analyze when file is loaded
    if uploaded_file is not None:
        # Display uploaded image
        image = Image.open(uploaded_file)
        st.session_state.original_image = image  # Save original image
        st.image(image, caption="Uploaded boleto", use_container_width=True)
        
        # Button to start analysis
        if st.button("Analyze Boleto"):
            with st.spinner("Analyzing boleto..."):
                # Reset file pointer to beginning
                uploaded_file.seek(0)
                
                # Analyze locally without calling external API
                result = analyze_boleto_local(uploaded_file.read())
                
                # Mark analysis as complete and show results
                st.session_state.analysis_complete = True
                st.session_state.result = result
                st.rerun()
else:
    # Display previous analysis results
    result = st.session_state.result
    
    # Show general result
    if result["fraud_detected"]:
        st.error(f"⚠️ **FRAUD DETECTED!** ⚠️\n\n{result['message']}")
    else:
        st.success(f"✅ **Boleto appears to be valid**\n\n{result['message']}")
    
    # Create columns to show original image and marked image
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Original Image")
        st.image(st.session_state.original_image, use_container_width=True)
    
    with col2:
        st.subheader("Suspicious Areas Highlighted")
        # Convert marked image from OpenCV to PIL and display
        marked_pil = cv2_to_pil(result["marked_image"])
        st.image(marked_pil, use_container_width=True)
    
    # Show detailed explanations about suspicious areas
    if result["suspicious_areas"]:
        st.subheader("Suspicious Area Details")
        
        for i, area in enumerate(result["suspicious_areas"]):
            with st.expander(f"Suspicious area {i+1}: {area['area']} (Confidence: {area['confidence']})"):
                st.write(f"**Explanation:** {area['explanation']}")
                
                if area['coordinates']:
                    st.write(f"**Location:** x={area['coordinates'][0]}, y={area['coordinates'][1]}, "
                            f"width={area['coordinates'][2]}, height={area['coordinates'][3]}")
    
    # Analysis details
    with st.expander("View technical analysis details"):
        st.json(result["fraud_details"])
        
        st.subheader("Text extracted from boleto")
        st.text(result["extracted_text"])
    
    # Button to clear and analyze another boleto
    if st.button("Analyze another boleto", key="clear_button"):
        clear_analysis()

# Tips section
st.markdown("---")
st.subheader("Tips to verify a boleto")
tips = {
    "Check the issuer": "Verify if the boleto issuer is indeed the company you expect.",
    "Check the amount": "Verify if the amount matches what you expect for the service or product.",
    "Analyze the barcode": "Fraudulent boletos may have invalid or manipulated barcodes.",
    "Be wary of urgency": "Messages of urgency for immediate payment are warning signs."
}

for tip, desc in tips.items():
    st.markdown(f"**{tip}**: {desc}")

# Footer
st.markdown("---")
st.caption("BoletoFraudAI - Developed with Streamlit, FastAPI and OpenCV") 
