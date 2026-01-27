"""
Exemple 4: Mesure de distances
Démontre l'utilisation du module de mesure de distances
"""

import cv2
import numpy as np
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from imgprocessor import ImageProcessor


def create_sample_image_with_points():
    """Crée une image d'exemple avec des points."""
    image = np.ones((400, 500, 3), dtype=np.uint8) * 255
    
    # Définir des points
    points = [
        (50, 50, "Point A"),
        (450, 50, "Point B"),
        (50, 350, "Point C"),
        (450, 350, "Point D"),
        (250, 200, "Centre")
    ]
    
    # Dessiner les points
    for x, y, label in points:
        cv2.circle(image, (x, y), 8, (0, 0, 255), -1)
        cv2.putText(image, label, (x + 15, y + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
    
    return image, points


def example_distance_measurement():
    """Exemple de mesure de distances."""
    print("=" * 60)
    print("Exemple 4: Mesure de Distances")
    print("=" * 60)
    
    # Créer une instance du processeur
    processor = ImageProcessor()
    
    # Désactiver les modules inutiles
    processor.config.enable_module('text_detection', False)
    processor.config.enable_module('shape_detection', False)
    processor.config.enable_module('visual_analysis', False)
    
    # Configurer la mesure de distances
    processor.config.set_module_options('distance_measurement', {
        'unit': 'pixels',
        'precision': 2
    })
    
    print("\nConfiguration:")
    print("  ✗ Détection de texte: DÉSACTIVÉE")
    print("  ✗ Détection de formes: DÉSACTIVÉE")
    print("  ✓ Mesure de distances: ACTIVÉE")
    print("  ✗ Analyse visuelle: DÉSACTIVÉE")
    
    print("\nOptions du module de mesure de distances:")
    options = processor.config.get_module_options('distance_measurement')
    for key, value in options.items():
        print(f"  {key}: {value}")
    
    # Créer une image d'exemple
    print("\nCréation d'une image d'exemple...")
    image, points = create_sample_image_with_points()
    
    # Mesurer les distances
    print("\nMesure des distances entre les points:")
    if processor.config.is_module_enabled('distance_measurement'):
        # Distance entre Point A et Point B
        p1 = (points[0][0], points[0][1])
        p2 = (points[1][0], points[1][1])
        dist = processor.measure_distance(p1, p2)
        print(f"  {points[0][2]} -> {points[1][2]}: {dist.distance}{dist.unit}")
        
        # Distance entre Point A et Point C
        p1 = (points[0][0], points[0][1])
        p2 = (points[2][0], points[2][1])
        dist = processor.measure_distance(p1, p2)
        print(f"  {points[0][2]} -> {points[2][2]}: {dist.distance}{dist.unit}")
        
        # Distance diagonale
        p1 = (points[0][0], points[0][1])
        p2 = (points[3][0], points[3][1])
        dist = processor.measure_distance(p1, p2)
        print(f"  {points[0][2]} -> {points[3][2]}: {dist.distance}{dist.unit}")
        
        # Distance vers le centre
        p1 = (points[0][0], points[0][1])
        p2 = (points[4][0], points[4][1])
        dist = processor.measure_distance(p1, p2)
        print(f"  {points[0][2]} -> {points[4][2]}: {dist.distance}{dist.unit}")
    
    # Sauvegarder l'image
    output_path = Path(__file__).parent / "sample_image_with_points.jpg"
    cv2.imwrite(str(output_path), image)
    print(f"\nImage d'exemple sauvegardée: {output_path}")
    
    # Calibration personnalisée
    print("\n" + "=" * 60)
    print("Exemple avec calibration (mm):")
    processor.config.set_module_options('distance_measurement', {
        'unit': 'mm',
        'precision': 2
    })
    processor.distance_measurer.set_calibration(pixels_per_mm=10)  # 10 pixels = 1 mm
    
    p1 = (50, 50)
    p2 = (100, 100)
    dist = processor.measure_distance(p1, p2)
    print(f"Distance en mm: {dist.distance}{dist.unit}")
    
    print("\n" + "=" * 60)
    print("Code d'exemple pour utiliser la mesure de distances:")
    print("""
from imgprocessor import ImageProcessor

processor = ImageProcessor()

# Mesurer la distance entre deux points
if processor.config.is_module_enabled('distance_measurement'):
    distance = processor.measure_distance((100, 50), (200, 150))
    print(f"Distance: {distance.distance}{distance.unit}")
    
    # Définir une calibration en mm
    processor.distance_measurer.set_calibration(pixels_per_mm=10)
""")


if __name__ == "__main__":
    example_distance_measurement()
