"""
Exemple 5: Utilisation Complète du Package (v1.0.5)
Tous les modules ensemble
"""

import cv2
from imgprocessor import ImageProcessor

# Charger une image
image = cv2.imread('mon_image.jpg')

# Créer un processeur
processor = ImageProcessor()

print("Image Processor - Exemple Complet")
print("=" * 60)

# 1. Détection de texte
print("\n1️⃣  TEXTE")
try:
    text = processor.extract_text(image)
    regions = processor.detect_text(image)
    print(f"   Texte détecté: {len(text)} caractères, {len(regions)} régions")
except Exception as e:
    print(f"   (Module désactivé ou non installé)")

# 2. Détection de formes
print("\n2️⃣  FORMES GÉOMÉTRIQUES")
try:
    shapes = processor.detect_shapes(image)
    circles = processor.detect_circles(image)
    print(f"   Formes détectées: {len(shapes)} (dont {len(circles)} cercles)")
except Exception as e:
    print(f"   (Module désactivé ou non installé)")

# 3. Analyse visuelle
print("\n3️⃣  ANALYSE VISUELLE")
try:
    analysis = processor.analyze_image(image)
    print(f"   Luminosité: {analysis.brightness:.1f}/255")
    print(f"   Contraste: {analysis.contrast:.2f}")
except Exception as e:
    print(f"   (Module désactivé ou non installé)")

# 4. Mesure de distances
print("\n4️⃣  DISTANCES")
try:
    # Exemple: distance entre deux points
    dist = processor.measure_distance((0, 0), (100, 100))
    print(f"   Distance calculée: {dist:.2f} pixels")
except Exception as e:
    print(f"   (Module désactivé ou non installé)")

print("\n" + "=" * 60)
