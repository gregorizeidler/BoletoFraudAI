# 📌 **BoletoFraudAI - Fake Boleto Detector** 🚀  

BoletoFraudAI is an **AI-powered fraud detection system** that analyzes **boletos bancários** (Brazilian payment slips) to identify **fake, tampered, or manipulated documents** before payment. Using **OCR (Tesseract), OpenCV, and Streamlit**, it detects:  
✅ **Fake boletos** with invalid barcodes  
✅ **Altered boletos** (e.g., edited text, different fonts)  
✅ **Tampered barcodes** (manually modified digits)  
✅ **Pasted elements** (text or layout inconsistencies)  

---

## 🎬 **Demo Video**
Watch our [demonstration video](https://drive.google.com/file/d/1AVBRhWJO-8VydZOsajObe9PA5vIhllA2/view?usp=sharing) to see BoletoFraudAI in action!

---

## 🛠 **Technologies Used**
- **Python** 🐍  
- **Streamlit** 🌟 (for user interface)
- **OpenCV** 📷 (for image processing)  
- **Tesseract OCR** 🧐 (for text extraction)  
- **NumPy** 📊 (for numerical processing)

---

## 📂 **Project Structure**
```
BoletoFraudAI/
│── app/
│   ├── streamlit_app.py    # Streamlit user interface
│   ├── services.py         # Boleto fraud detection logic
│   ├── utils.py            # Helper functions (image processing, text validation)
│── requirements.txt        # Dependencies
│── README.md               # Documentation
```

---

## 🚀 **Installation & Usage**
### 1️⃣ **Clone the Repository**
```bash
git clone https://github.com/your-username/BoletoFraudAI.git
cd BoletoFraudAI
```

### 2️⃣ **Install Dependencies**
```bash
# Install Python if you don't have it
python3 -m pip install -r requirements.txt

# Install Tesseract OCR
# On macOS:
brew install tesseract
# On Ubuntu/Debian:
# sudo apt-get install tesseract-ocr
```

### 3️⃣ **Run the Application**
```bash
streamlit run app/streamlit_app.py
```
The Streamlit interface will open automatically in your browser.

---

## 🔍 **Features**
✅ **User-friendly Streamlit interface** for easy boleto analysis
✅ **Detects altered boletos** (e.g., different fonts, pasted text)  
✅ **Edge detection & contrast analysis** to find manipulated areas  
✅ **Validates barcode & format** against official patterns  
✅ **Visual highlighting** of suspicious areas with detailed explanations
✅ **Fast & lightweight** (built with Streamlit & OpenCV)  

---

## 🛣️ **Roadmap**
- [ ] Machine learning model for more accurate fraud detection
- [ ] Multi-language support (Portuguese/English)
- [ ] Improved image preprocessing for better OCR results
- [ ] Mobile-friendly responsive design
- [ ] User feedback collection

---

## 🤝 **How to Contribute**
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## ⚖️ **License**
This project is **open-source** under the **MIT License**. Feel free to use, modify, and contribute!  

📢 **Contributions are welcome!** If you have ideas or improvements, submit a pull request. 🚀

