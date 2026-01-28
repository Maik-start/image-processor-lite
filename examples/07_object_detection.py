"""
Exemple 07: Détection d'objets visuels cohérents
Démontre la détection et l'analyse des objets visuels cohérents.
"""

import cv2
import numpy as np
import sys
sys.path.insert(0, '..')

from imgprocessor.visual_analysis.analyzer import VisualAnalyzer


def main():
    # Créer une image de test avec différents objets visuels
    image = create_test_image()
    
    # Initialiser l'analyseur avec détection d'objets activée
    analyzer = VisualAnalyzer(
        analyze_brightness=True,
        analyze_contrast=True,
        analyze_hue=True,
        detect_objects=True,
        min_object_size=100,
        max_object_size=None
    )
    
    # Analyser l'image
    print("Analyse de l'image en cours...")
    analysis = analyzer.analyze(image)
    
    # Afficher les résultats
    print("\n" + "="*60)
    print("ANALYSE VISUELLE COMPLÈTE")
    print("="*60)
    
    print(f"\nPropriétés globales:")
    print(f"  - Luminosité: {analysis.brightness:.2f}")
    print(f"  - Contraste: {analysis.contrast:.2f}")
    print(f"  - Saturation: {analysis.saturation:.2f}")
    print(f"  - Densité de contours: {analysis.edge_density:.2f}%")
    
    print(f"\nDétection d'objets:")
    print(f"  - Nombre d'objets détectés: {len(analysis.objects)}")
    print(f"  - Densité d'objets: {analysis.object_density:.2f}")
    
    # Afficher les détails de chaque objet
    print(f"\nDétails des objets détectés:")
    print("-"*60)
    
    for obj in analysis.objects:
        print(f"\nObjet #{obj.object_id}")
        print(f"  Type: {obj.label}")
        print(f"  Aire: {obj.area} pixels")
        print(f"  Périmètre: {obj.perimeter:.2f} pixels")
        print(f"  Centroid: ({obj.centroid[0]:.1f}, {obj.centroid[1]:.1f})")
        print(f"  Couleur dominante (B,G,R): {obj.dominant_color}")
        print(f"  Luminosité moyenne: {obj.mean_brightness:.2f}")
        print(f"  Stabilité chromatique: {obj.chromatic_stability:.2f}")
        print(f"  Régularité de contour: {obj.contour_regularity:.2f}")
        print(f"  Solidité: {obj.solidity:.2f}")
        print(f"  Ratio aspect: {obj.aspect_ratio:.2f}")
    
    # Créer une visualisation
    visualization = visualize_objects(image, analysis)
    
    # Sauvegarder la visualisation
    output_path = 'detected_objects.jpg'
    cv2.imwrite(output_path, visualization)
    print(f"\n✓ Visualisation sauvegardée dans {output_path}")
    
    # Afficher les résultats JSON
    print("\n" + "="*60)
    print("RÉSULTATS EN FORMAT JSON")
    print("="*60)
    import json
    print(json.dumps(analysis.to_dict(), indent=2, default=str))


def create_test_image():
    """Crée une image de test avec différents objets."""
    image = np.ones((400, 600, 3), dtype=np.uint8) * 200
    
    # Rectangle rouge (objet artificiel)
    cv2.rectangle(image, (50, 50), (200, 150), (0, 0, 255), -1)
    
    # Cercle bleu (objet géométrique)
    cv2.circle(image, (450, 100), 50, (255, 0, 0), -1)
    
    # Zone verte irrégulière (objet naturel)
    pts = np.array([[100, 250], [200, 200], [250, 280], [150, 350]], np.int32)
    cv2.polylines(image, [pts], True, (0, 255, 0), -1)
    
    # Tache jaune (objet abstrait)
    cv2.circle(image, (400, 300), 40, (0, 255, 255), -1)
    
    return image


def visualize_objects(image, analysis):
    """Crée une visualisation avec les objets détectés."""
    visualization = image.copy()
    
    # Couleurs pour chaque type d'objet
    colors = {
        'geometric': (255, 0, 0),      # Bleu
        'artificial': (0, 255, 0),     # Vert
        'natural': (0, 165, 255),      # Orange
        'abstract': (255, 255, 0),     # Cyan
        'unknown': (128, 128, 128)     # Gris
    }
    
    # Dessiner chaque objet
    for obj in analysis.objects:
        color = colors.get(obj.label, (0, 0, 255))
        
        # Bounding box
        x, y, w, h = obj.bounding_box
        cv2.rectangle(visualization, (x, y), (x+w, y+h), color, 2)
        
        # Centroid
        centroid = (int(obj.centroid[0]), int(obj.centroid[1]))
        cv2.circle(visualization, centroid, 5, color, -1)
        
        # Label avec confiance
        label_text = f"{obj.label} (area:{obj.area})"
        cv2.putText(visualization, label_text, (x, y-5),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.4, color, 1)
    
    return visualization


if __name__ == '__main__':
    main()
