# 📌 **BoletoFraudAI - Fake Boleto Detector** 🚀  

BoletoFraudAI is an **AI-powered fraud detection system** that analyzes **boletos bancários** (Brazilian payment slips) to identify **fake, tampered, or manipulated documents** before payment. Using **OCR (Tesseract), OpenCV, and FastAPI**, it detects:  
✅ **Fake boletos** with invalid barcodes  
✅ **Altered boletos** (e.g., edited text, different fonts)  
✅ **Tampered barcodes** (manually modified digits)  
✅ **Pasted elements** (text or layout inconsistencies)  

---

## 🛠 **Technologies Used**
- **Python** 🐍  
- **FastAPI** 🚀 (for API)  
- **OpenCV** 📷 (for image processing)  
- **Tesseract OCR** 🧐 (for text extraction)  
- **Pydantic** 📦 (data validation)  
- **Docker** 🐳 (for deployment)  

---

## 📂 **Project Structure**
```
BoletoFraudAI/
│── app/
│   ├── main.py             # FastAPI application
│   ├── services.py         # Boleto fraud detection logic
│   ├── utils.py            # Helper functions (image processing, text validation)
│── tests/
│   ├── test_services.py    # Unit tests for fraud detection
│── requirements.txt        # Dependencies
│── README.md               # Documentation
│── Dockerfile              # Containerization setup
│── examples/               # Sample valid and fake boletos
```

---

## 🚀 **Installation & Usage**
### 1️⃣ **Clone the Repository**
```bash
git clone https://github.com/your-username/BoletoFraudAI.git
cd BoletoFraudAI
```

### 2️⃣ **Create a Virtual Environment & Install Dependencies**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3️⃣ **Run the API Server**
```bash
uvicorn app.main:app --reload
```

### 4️⃣ **Use the API**
- Open **Swagger UI**: [`http://127.0.0.1:8000/docs`](http://127.0.0.1:8000/docs)  
- Upload a **boleto image** via the `/detect/` endpoint.  
- The response will indicate whether the boleto is **valid** or **fraudulent**.

---

## 🔍 **Example API Response**
### ✅ **Valid Boleto**
```json
{
    "fraud_detected": false,
    "message": "Boleto appears to be valid."
}
```

### ❌ **Fake or Edited Boleto**
```json
{
    "fraud_detected": true,
    "message": "Potential fraud detected: Invalid barcode | Potential image manipulation detected"
}
```

---

## 🧪 **Running Tests**
```bash
pytest tests/
```

---

## 📦 **Docker Deployment**
### 🏗 **Build & Run**
```bash
docker build -t boletofraudai .
docker run -p 8000:8000 boletofraudai
```

---

## 🎯 **Features**
✅ **Detects altered boletos** (e.g., different fonts, pasted text)  
✅ **Edge detection & contrast analysis** to find manipulated areas  
✅ **Validates barcode & format** against official patterns  
✅ **Easy API integration** for payment systems  
✅ **Fast & lightweight** (built with FastAPI & OpenCV)  

---

## ⚖️ **License**
This project is **open-source** under the **MIT License**. Feel free to use, modify, and contribute!  

📢 **Contributions are welcome!** If you have ideas or improvements, submit a pull request. 🚀  

