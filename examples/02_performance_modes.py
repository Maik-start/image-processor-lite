"""
Exemple 2: Choisir le bon mode de performance (v1.0.5)
Comparaison des 4 modes disponibles
"""

import cv2
import time
from imgprocessor.text_detection import TextDetector
from imgprocessor.text_detection.fast_detector import FastTextDetector

image = cv2.imread('mon_image.jpg')

print("Performance comparison:")
print("=" * 60)

# Mode 1: SPEED - 100ms, texte gros uniquement (20% résolution)
print("\n1️⃣  SPEED MODE (100ms, 20% résolution)")
print("   Utiliser pour: Texte gros/clair uniquement")
detector = TextDetector(mode='speed')
start = time.time()
text = detector.extract_text(image)
elapsed = time.time() - start
print(f"   Temps: {elapsed*1000:.1f}ms, Texte: {len(text)} chars")

# Mode 2: BALANCED - 100ms, bon compromis (75% résolution) ✅ RECOMMANDÉ
print("\n2️⃣  BALANCED MODE (100ms, 75% résolution) ✅ RECOMMANDÉ")
print("   Utiliser pour: Production (meilleur compromis)")
detector = TextDetector(mode='balanced')
start = time.time()
text = detector.extract_text(image)
elapsed = time.time() - start
print(f"   Temps: {elapsed*1000:.1f}ms, Texte: {len(text)} chars")

# Mode 3: QUALITY - 1160ms, meilleure qualité (100% résolution)
print("\n3️⃣  QUALITY MODE (1160ms, 100% résolution)")
print("   Utiliser pour: Haute précision requise")
detector = TextDetector(mode='quality')
start = time.time()
text = detector.extract_text(image)
elapsed = time.time() - start
print(f"   Temps: {elapsed*1000:.1f}ms, Texte: {len(text)} chars")

# Mode 4: FastTextDetector - 90-100ms, Tesseract (moins précis mais ultra-rapide)
print("\n4️⃣  FAST MODE (90-100ms, Tesseract)")
print("   Utiliser pour: Temps réel, moins de précision")
detector = FastTextDetector()
start = time.time()
text = detector.extract_text(image)
elapsed = time.time() - start
print(f"   Temps: {elapsed*1000:.1f}ms, Texte: {len(text)} chars")

print("\n" + "=" * 60)
