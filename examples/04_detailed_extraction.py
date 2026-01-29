"""
Exemple 4: Extraction Détaillée avec Coordonnées (v1.0.5)
Récupérer le texte avec localisation et confiance
"""

import cv2
from imgprocessor.text_detection import TextDetector

image = cv2.imread('mon_image.jpg')

# Détecteur BALANCED (bon compromis)
detector = TextDetector(mode='balanced')

# Extraire texte avec coordonnées
regions = detector.detect(image)

print(f"Régions détectées: {len(regions)}")
print("=" * 60)

for i, region in enumerate(regions, 1):
    print(f"\n{i}. Texte: {region.text}")
    print(f"   Confiance: {region.confidence:.1%}")
    
    # Coordonnées (si disponibles)
    if hasattr(region, 'bbox'):
        x1, y1, x2, y2 = region.bbox
        width = x2 - x1
        height = y2 - y1
        print(f"   Position: ({x1}, {y1}) - Taille: {width}x{height}")
    
    if hasattr(region, 'center'):
        cx, cy = region.center
        print(f"   Centre: ({cx:.0f}, {cy:.0f})")

print("\n" + "=" * 60)
