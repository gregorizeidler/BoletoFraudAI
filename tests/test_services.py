from app.services import analyze_boleto
import cv2

def test_valid_boleto():
    image = cv2.imread("examples/valid_boleto.jpg")
    result = analyze_boleto(image)
    assert result["fraud_detected"] is False

def test_fake_boleto():
    image = cv2.imread("examples/fake_boleto.jpg")
    result = analyze_boleto(image)
    assert result["fraud_detected"] is True
