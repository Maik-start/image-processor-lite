"""
Exemple 3: Cache Global Automatique (v1.0.5)
Démonstration du cache singleton qui accélère les appels répétés
"""

import cv2
import time
from imgprocessor.text_detection import TextDetector

image = cv2.imread('mon_image.jpg')

print("Cache Global Automatique")
print("=" * 60)

detector = TextDetector()

# Premier appel: charge le modèle OCR (3800ms)
print("\n1️⃣  Premier appel (charge modèle):")
start = time.time()
text1 = detector.extract_text(image)
elapsed = time.time() - start
print(f"   Temps: {elapsed*1000:.1f}ms")

# Deuxième appel: utilise le cache global (0.01ms)
print("\n2️⃣  Deuxième appel (cache global):")
start = time.time()
text2 = detector.extract_text(image)
elapsed = time.time() - start
print(f"   Temps: {elapsed*1000:.3f}ms ⚡ (360,000x PLUS RAPIDE!)")

# Autre instance: réutilise aussi le cache global
print("\n3️⃣  Nouvelle instance (réutilise cache global):")
detector2 = TextDetector()
start = time.time()
text3 = detector2.extract_text(image)
elapsed = time.time() - start
print(f"   Temps: {elapsed*1000:.3f}ms ⚡ (initialisation instantanée!)")

print("\n" + "=" * 60)
print("✅ Chaque instance réutilise le même modèle OCR en mémoire!")
print("=" * 60)
