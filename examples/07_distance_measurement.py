"""
Exemple 4: Mesure de Distances et Calibration
Démontre comment mesurer les distances entre les points dans une image
"""

import cv2
import sys
import numpy as np
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from imgprocessor import ImageProcessor
from imgprocessor.distance_measurement import DistanceMeasurer


def create_measurement_image():
    """Crée une image pour la mesure de distances."""
    image = np.full((400, 600, 3), 255, dtype=np.uint8)
    
    # Points de référence
    points = [
        (100, 100, (255, 0, 0), "Point A"),
        (200, 150, (0, 255, 0), "Point B"),
        (400, 100, (0, 0, 255), "Point C"),
        (300, 300, (255, 255, 0), "Point D"),
    ]
    
    # Dessiner les points
    for x, y, color, label in points:
        cv2.circle(image, (x, y), 8, color, -1)
        cv2.putText(image, label, (x+15, y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
    
    # Dessiner des lignes de connexion
    cv2.line(image, (100, 100), (200, 150), (100, 100, 100), 2)
    cv2.line(image, (200, 150), (400, 100), (100, 100, 100), 2)
    cv2.line(image, (100, 100), (300, 300), (150, 150, 150), 1)
    
    return image, points


def example_distance_measurement():
    """Exemple de mesure de distances."""
    print("=" * 60)
    print("Exemple 4: Mesure de Distances et Calibration")
    print("=" * 60)
    
    # Créer image
    print("\n✓ Création d'une image avec points de référence...")
    image, points = create_measurement_image()
    
    # Sauvegarder
    sample_path = Path(__file__).parent / "sample_measurement.jpg"
    cv2.imwrite(str(sample_path), image)
    print(f"✓ Image sauvegardée: {sample_path.name}")
    
    # Initialiser le processeur avec distance_measurement activé
    print("\n✓ Initialisation du processeur avec mesure de distances...")
    processor = ImageProcessor(optimization="quality")
    processor.config.enable_module('distance_measurement', True)
    processor.config.enable_module('text_detection', False)
    processor.config.enable_module('shape_detection', False)
    processor.config.enable_module('visual_analysis', False)
    
    # Créer un mesureur direct
    measurer = DistanceMeasurer(unit='pixels', precision=2)
    
    print("\n" + "=" * 60)
    print("MESURE DES DISTANCES EN PIXELS")
    print("=" * 60)
    
    # Mesurer les distances entre les points
    coords = [(100, 100), (200, 150), (400, 100), (300, 300)]
    labels = ["Point A", "Point B", "Point C", "Point D"]
    
    for i in range(len(coords)):
        for j in range(i+1, len(coords)):
            p1, p2 = coords[i], coords[j]
            distance = np.sqrt((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2)
            print(f"\n  {labels[i]} → {labels[j]}: {distance:.2f} pixels")
    
    # Calibration
    print("\n" + "=" * 60)
    print("CALIBRATION")
    print("=" * 60)
    
    print("""
    Pour convertir en millimètres:
    - 1. Mesurer une distance connue (ex: 100 pixels = 10 mm)
    - 2. Configurer: pixels_per_unit = 10 (10 pixels par mm)
    - 3. Mesurer des distances dans l'image
    """)
    
    # Exemple de calibration
    print("\n✓ Configuration: 10 pixels = 1 mm")
    measurer.set_calibration(pixels_per_mm=10)
    
    print("\nDistances en MILLIMÈTRES (après calibration):")
    for i in range(len(coords)):
        for j in range(i+1, len(coords)):
            p1, p2 = coords[i], coords[j]
            pixels = np.sqrt((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2)
            mm = pixels / 10  # pixels_per_mm = 10
            print(f"  {labels[i]} → {labels[j]}: {mm:.2f} mm ({pixels:.2f} px)")
    
    print("\n" + "=" * 60)
    print("UTILISATION DANS LE CODE")
    print("=" * 60)
    print("""
    from imgprocessor.distance_measurement import Measurer
    import numpy as np
    
    measurer = Measurer(unit='pixels')
    
    # Calibration
    measurer.set_calibration(pixels_per_mm=10)
    
    # Mesurer
    p1, p2 = (100, 100), (200, 150)
    distance = np.sqrt((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2)
    distance_mm = distance / 10
    """)


if __name__ == "__main__":
    example_distance_measurement()
