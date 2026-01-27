"""
Exemple 2: Détection de texte et extraction
Démontre l'utilisation du module de détection de texte
"""

import cv2
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from imgprocessor import ImageProcessor


def example_text_detection():
    """Exemple de détection de texte."""
    print("=" * 60)
    print("Exemple 2: Détection de Texte")
    print("=" * 60)
    
    # Créer une instance du processeur
    processor = ImageProcessor()
    
    # Désactiver les modules inutiles
    processor.config.enable_module('shape_detection', False)
    processor.config.enable_module('distance_measurement', False)
    processor.config.enable_module('visual_analysis', False)
    
    print("\nConfiguration:")
    print("  ✓ Détection de texte: ACTIVÉE")
    print("  ✗ Détection de formes: DÉSACTIVÉE")
    print("  ✗ Mesure de distances: DÉSACTIVÉE")
    print("  ✗ Analyse visuelle: DÉSACTIVÉE")
    
    # Configurer les options du module de texte
    processor.config.set_module_options('text_detection', {
        'language': ['fra', 'eng'],
        'engine': 'easyocr'
    })
    
    print("\nOptions du module de texte:")
    options = processor.config.get_module_options('text_detection')
    for key, value in options.items():
        print(f"  {key}: {value}")
    
    print("\n" + "=" * 60)
    print("Note: Pour utiliser cet exemple, vous avez besoin:")
    print("  1. D'une image contenant du texte")
    print("  2. D'avoir installé easyocr: pip install easyocr")
    print("=" * 60)
    
    print("\nCode d'exemple pour utiliser la détection de texte:")
    print("""
import cv2
from imgprocessor import ImageProcessor

processor = ImageProcessor()

# Charger une image
image = cv2.imread('mon_image.jpg')

# Détecter le texte
if processor.config.is_module_enabled('text_detection'):
    # Obtenir les régions de texte
    regions = processor.detect_text(image)
    if regions:
        for region in regions:
            print(f"Texte: {region.text}")
            print(f"Confiance: {region.confidence:.2f}")
            print(f"Position: {region.bbox}")
    
    # Ou extraire tout le texte
    full_text = processor.extract_text(image)
    print(full_text)
""")


if __name__ == "__main__":
    example_text_detection()
