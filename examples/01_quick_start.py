"""
Exemple 1: Démarrage rapide - TextDetector Optimisé (v1.0.5)
Le moyen le plus simple d'utiliser l'extraction de texte
"""

import cv2
from imgprocessor.text_detection import TextDetector

# Charger une image
image = cv2.imread('mon_image.jpg')

# Créer un détecteur (mode BALANCED par défaut = 100ms, très bon compromis)
detector = TextDetector()

# Extraire le texte
text = detector.extract_text(image)
print("Texte détecté:")
print(text)

# Ou avec coordonnées
regions = detector.detect(image)
for region in regions:
    print(f"  • {region.text} @ {region.confidence:.1%}")
