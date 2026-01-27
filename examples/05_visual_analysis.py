"""
Exemple 5: Analyse visuelle
Démontre l'utilisation du module d'analyse visuelle
"""

import cv2
import numpy as np
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from imgprocessor import ImageProcessor


def create_sample_image_with_gradient():
    """Crée une image d'exemple avec gradient et variations visuelles."""
    image = np.zeros((300, 400, 3), dtype=np.uint8)
    
    # Gradient horizontal (luminosité)
    for x in range(400):
        value = int(255 * x / 400)
        image[:, x, :] = [value, value, value]
    
    # Ajouter du bruit pour augmenter le contraste
    noise = np.random.randint(-30, 31, image.shape, dtype=np.int16)
    image = cv2.add(image, noise.astype(np.uint8))
    
    # Ajouter du texte
    cv2.putText(image, "Image d'exemple", (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    
    return image


def example_visual_analysis():
    """Exemple d'analyse visuelle."""
    print("=" * 60)
    print("Exemple 5: Analyse Visuelle")
    print("=" * 60)
    
    # Créer une instance du processeur avec optimisation équilibrée
    processor = ImageProcessor(optimization="balanced")
    
    # Désactiver les modules inutiles
    processor.config.enable_module('text_detection', False)
    processor.config.enable_module('shape_detection', False)
    processor.config.enable_module('distance_measurement', False)
    
    # Configurer l'analyse visuelle
    processor.config.set_module_options('visual_analysis', {
        'analyze_brightness': True,
        'analyze_contrast': True,
        'analyze_hue': True,
        'bins': 256
    })
    
    print("\nConfiguration:")
    print("  ✗ Détection de texte: DÉSACTIVÉE")
    print("  ✗ Détection de formes: DÉSACTIVÉE")
    print("  ✗ Mesure de distances: DÉSACTIVÉE")
    print("  ✓ Analyse visuelle: ACTIVÉE")
    
    print("\nOptions du module d'analyse visuelle:")
    options = processor.config.get_module_options('visual_analysis')
    for key, value in options.items():
        print(f"  {key}: {value}")
    
    # Créer une image d'exemple
    print("\nCréation d'une image d'exemple avec gradient...")
    image = create_sample_image_with_gradient()
    
    # Analyser les propriétés visuelles
    print("\nAnalyse des propriétés visuelles:")
    if processor.config.is_module_enabled('visual_analysis'):
        analysis = processor.analyze_visual_properties(image)
        
        print(f"\n  Luminosité: {analysis.brightness:.2f} (0-255)")
        brightness_level = processor.visual_analyzer.get_brightness_level(image)
        print(f"    Niveau: {brightness_level}")
        
        print(f"\n  Contraste: {analysis.contrast:.2f}")
        contrast_level = processor.visual_analyzer.get_contrast_level(image)
        print(f"    Niveau: {contrast_level}")
        
        print(f"\n  Saturation: {analysis.saturation:.2f} (0-255)")
        print(f"  Valeur (HSV): {analysis.value:.2f} (0-255)")
        
        print(f"\n  Distribution de teinte (%):")
        for color, percentage in analysis.hue_distribution.items():
            print(f"    {color}: {percentage:.1f}%")
        
        print(f"\n  Densité des contours: {analysis.edge_density:.2f}%")
        
        print(f"\n  Histogramme des couleurs:")
        for channel, hist_info in analysis.color_histogram.items():
            print(f"    {channel.upper()}:")
            print(f"      Moyenne: {hist_info['mean']:.2f}")
            print(f"      Écart-type: {hist_info['std']:.2f}")
        
        # Couleur dominante
        dominant = processor.visual_analyzer.get_dominant_color(image)
        print(f"\n  Couleur dominante (BGR): {dominant}")
    
    # Sauvegarder l'image
    output_path = Path(__file__).parent / "sample_image_gradient.jpg"
    cv2.imwrite(str(output_path), image)
    print(f"\nImage d'exemple sauvegardée: {output_path}")
    
    # Créer deux images pour la comparaison
    print("\n" + "=" * 60)
    print("Comparaison entre deux images:")
    
    # Image 1: Sombre
    dark_image = np.zeros((300, 400, 3), dtype=np.uint8)
    dark_image[:, :, :] = 50
    
    # Image 2: Lumineuse
    bright_image = np.ones((300, 400, 3), dtype=np.uint8) * 200
    
    comparison = processor.visual_analyzer.compare_images(dark_image, bright_image)
    print(f"\n  Image 1 (sombre) vs Image 2 (lumineuse):")
    print(f"    Différence de luminosité: {comparison['brightness_diff']:.2f}")
    print(f"    Niveau Image 1: {comparison['image1_brightness_level']}")
    print(f"    Niveau Image 2: {comparison['image2_brightness_level']}")
    
    print("\n" + "=" * 60)
    print("Code d'exemple pour utiliser l'analyse visuelle:")
    print("""
import cv2
from imgprocessor import ImageProcessor

processor = ImageProcessor()
image = cv2.imread('mon_image.jpg')

# Analyser les propriétés visuelles
if processor.config.is_module_enabled('visual_analysis'):
    analysis = processor.analyze_visual_properties(image)
    
    print(f"Luminosité: {analysis.brightness:.1f}")
    print(f"Contraste: {analysis.contrast:.1f}")
    print(f"Distribution de teinte: {analysis.hue_distribution}")
    
    # Obtenir le niveau de luminosité
    brightness_level = processor.visual_analyzer.get_brightness_level(image)
    print(f"Niveau de luminosité: {brightness_level}")
    
    # Obtenir la couleur dominante
    dominant = processor.visual_analyzer.get_dominant_color(image)
    print(f"Couleur dominante: {dominant}")
""")


if __name__ == "__main__":
    example_visual_analysis()
