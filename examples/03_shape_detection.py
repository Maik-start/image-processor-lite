"""
Exemple 3: Détection de formes
Démontre l'utilisation du module de détection de formes géométriques
"""

import cv2
import numpy as np
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from imgprocessor import ImageProcessor


def create_sample_image():
    """Crée une image d'exemple avec des formes."""
    # Créer une image blanche
    image = np.ones((400, 500, 3), dtype=np.uint8) * 255
    
    # Dessiner un cercle
    cv2.circle(image, (100, 100), 50, (0, 0, 255), -1)
    
    # Dessiner un rectangle
    cv2.rectangle(image, (200, 50), (350, 150), (0, 255, 0), -1)
    
    # Dessiner un triangle
    triangle = np.array([[400, 300], [450, 200], [300, 200]], np.int32)
    cv2.polylines(image, [triangle], True, (255, 0, 0), -1)
    
    # Dessiner quelques contours
    cv2.circle(image, (100, 300), 30, (255, 0, 255), -1)
    cv2.rectangle(image, (250, 250), (350, 350), (128, 128, 0), -1)
    
    return image


def example_shape_detection():
    """Exemple de détection de formes."""
    print("=" * 60)
    print("Exemple 3: Détection de Formes Géométriques")
    print("=" * 60)
    
    # Créer une instance du processeur
    processor = ImageProcessor()
    
    # Désactiver les modules inutiles
    processor.config.enable_module('text_detection', False)
    processor.config.enable_module('distance_measurement', False)
    processor.config.enable_module('visual_analysis', False)
    
    # Configurer la détection de formes
    processor.config.set_module_options('shape_detection', {
        'detect_circles': True,
        'detect_rectangles': True,
        'detect_polygons': True,
        'min_contour_area': 50
    })
    
    print("\nConfiguration:")
    print("  ✗ Détection de texte: DÉSACTIVÉE")
    print("  ✓ Détection de formes: ACTIVÉE")
    print("  ✗ Mesure de distances: DÉSACTIVÉE")
    print("  ✗ Analyse visuelle: DÉSACTIVÉE")
    
    print("\nOptions du module de détection de formes:")
    options = processor.config.get_module_options('shape_detection')
    for key, value in options.items():
        print(f"  {key}: {value}")
    
    # Créer une image d'exemple
    print("\nCréation d'une image d'exemple avec des formes...")
    image = create_sample_image()
    
    # Détecter les formes
    print("Détection des formes en cours...")
    if processor.config.is_module_enabled('shape_detection'):
        shapes = processor.detect_shapes(image)
        
        if shapes:
            print(f"\n✓ {len(shapes)} formes détectées:")
            for i, shape in enumerate(shapes, 1):
                print(f"\n  Forme {i}:")
                print(f"    Type: {shape.shape_type}")
                print(f"    Centre: ({shape.center[0]:.1f}, {shape.center[1]:.1f})")
                print(f"    Superficie: {shape.area:.2f} pixels²")
                print(f"    Périmètre: {shape.perimeter:.2f} pixels")
                if shape.properties:
                    print(f"    Propriétés:")
                    for key, value in shape.properties.items():
                        print(f"      {key}: {value}")
        else:
            print("✗ Aucune forme détectée")
    
    # Sauvegarder l'image
    output_path = Path(__file__).parent / "sample_image_with_shapes.jpg"
    cv2.imwrite(str(output_path), image)
    print(f"\nImage d'exemple sauvegardée: {output_path}")
    
    print("\n" + "=" * 60)
    print("Code d'exemple pour utiliser la détection de formes:")
    print("""
import cv2
from imgprocessor import ImageProcessor

processor = ImageProcessor()

# Charger une image
image = cv2.imread('mon_image.jpg')

# Détecter toutes les formes
if processor.config.is_module_enabled('shape_detection'):
    shapes = processor.detect_shapes(image)
    for shape in shapes:
        print(f"Type: {shape.shape_type}")
        print(f"Centre: {shape.center}")
        print(f"Superficie: {shape.area}")
    
    # Ou détecter seulement les cercles
    circles = processor.detect_circles(image)
    
    # Ou détecter seulement les rectangles
    rectangles = processor.detect_rectangles(image)
""")


if __name__ == "__main__":
    example_shape_detection()
