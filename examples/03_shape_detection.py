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
    """Crée une image d'exemple avec des formes géométriques."""
    # Initialiser l'image blanche
    image = np.full((400, 500, 3), 255, dtype=np.uint8)
    
    # Formes principales
    cv2.circle(image, (100, 100), 50, (0, 0, 255), -1)  # Cercle rouge
    cv2.rectangle(image, (200, 50), (350, 150), (0, 255, 0), -1)  # Rectangle vert
    
    # Triangle rempli
    triangle = np.array([[400, 300], [450, 200], [300, 200]], np.int32)
    cv2.fillPoly(image, [triangle], (255, 0, 0))  # Triangle bleu
    
    # Formes supplémentaires
    cv2.circle(image, (100, 300), 30, (255, 0, 255), -1)  # Petit cercle magenta
    cv2.rectangle(image, (250, 250), (350, 350), (128, 128, 0), -1)  # Rectangle olive
    
    return image


def example_shape_detection():
    """Exemple de détection de formes géométriques."""
    print("=" * 60)
    print("Exemple 3: Détection de Formes Géométriques")
    print("=" * 60)
    
    # Initialiser le processeur avec qualité pour meilleure précision
    processor = ImageProcessor(optimization="quality")
    
    # Configuration optimisée: activer shape_detection, désactiver les autres
    modules_config = {
        'text_detection': False,
        'shape_detection': True,
        'distance_measurement': False,
        'visual_analysis': False
    }
    for module, enabled in modules_config.items():
        processor.config.enable_module(module, enabled)
    
    # Configurer les options de détection
    processor.config.set_module_options('shape_detection', {
        'detect_circles': True,
        'detect_rectangles': True,
        'detect_polygons': True,
        'min_contour_area': 50
    })
    
    # Afficher le statut
    print("\nConfiguration active:")
    for module, enabled in modules_config.items():
        status = "✓ ACTIVÉ" if enabled else "✗ DÉSACTIVÉ"
        print(f"  {module}: {status}")
    
    print("\nOptions du module shape_detection:")
    for key, value in processor.config.get_module_options('shape_detection').items():
        print(f"  {key}: {value}")
    
    # Traitement de l'image
    print("\nCréation et analyse de l'image...")
    image = create_sample_image()
    shapes = processor.detect_shapes(image) if processor.config.is_module_enabled('shape_detection') else []
    
    # Afficher les résultats
    if shapes:
        print(f"\n✓ {len(shapes)} forme(s) détectée(s):\n")
        for i, shape in enumerate(shapes, 1):
            center_x, center_y = shape.center
            print(f"  Forme {i}:")
            print(f"    Type: {shape.shape_type}")
            print(f"    Centre: ({center_x:.1f}, {center_y:.1f})")
            print(f"    Superficie: {shape.area:.2f} pixels²")
            print(f"    Périmètre: {shape.perimeter:.2f} pixels")
            if shape.properties:
                for key, value in shape.properties.items():
                    print(f"    {key}: {value}")
    else:
        print("✗ Aucune forme détectée")
    
    # Sauvegarder le résultat
    output_path = Path(__file__).parent / "sample_image_with_shapes.jpg"
    cv2.imwrite(str(output_path), image)
    print(f"\nImage sauvegardée: {output_path}")
    

    print("\n" + "=" * 60)
    print("Utilisation rapide:")
    print("""
import cv2
from imgprocessor import ImageProcessor

processor = ImageProcessor()
image = cv2.imread('image.jpg')

# Détecter toutes les formes
shapes = processor.detect_shapes(image)
for shape in shapes:
    print(f"{shape.shape_type} au centre {shape.center}")
""")


if __name__ == "__main__":
    example_shape_detection()
