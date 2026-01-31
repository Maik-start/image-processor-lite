"""
Exemple 5: Workflow Complet - Traitement d'Image Complète
Démontre un workflow complet utilisant plusieurs modules
"""

import cv2
import sys
import numpy as np
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from imgprocessor import ImageProcessor


def create_complete_example_image():
    """Crée une image complexe avec texte et formes."""
    image = np.full((600, 800, 3), 245, dtype=np.uint8)
    
    # Ajouter du texte
    cv2.putText(image, "Document Scan Example", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0), 2)
    cv2.putText(image, "Project Report 2024", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (50, 50, 50), 1)
    cv2.line(image, (50, 120), (400, 120), (100, 100, 100), 1)
    
    # Contenu texte
    text_lines = [
        "Section 1: Introduction",
        "This document contains important information",
        "with various text sizes and styles.",
        "",
        "Section 2: Findings",
        "Key results are highlighted below:",
    ]
    
    y = 180
    for line in text_lines:
        if line:
            font_size = 0.6 if "Section" in line else 0.5
            color = (0, 0, 150) if "Section" in line else (50, 50, 50)
            cv2.putText(image, line, (50, y), cv2.FONT_HERSHEY_SIMPLEX, font_size, color, 1)
        y += 40
    
    # Ajouter des formes (diagramme simple)
    cv2.circle(image, (650, 150), 50, (0, 200, 0), -1)
    cv2.rectangle(image, (550, 300), (750, 450), (200, 0, 0), -1)
    
    # Ajouter des points de mesure
    cv2.circle(image, (100, 500), 5, (255, 0, 0), -1)
    cv2.circle(image, (300, 520), 5, (0, 255, 0), -1)
    cv2.line(image, (100, 500), (300, 520), (0, 0, 255), 2)
    cv2.putText(image, "Distance: X units", (150, 540), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
    
    return image


def example_complete_workflow():
    """Workflow complet avec tous les modules."""
    print("=" * 70)
    print("Exemple 5: Workflow Complet - Traitement Document")
    print("=" * 70)
    
    # Créer image
    print("\n✓ Création d'une image document d'exemple...")
    image = create_complete_example_image()
    
    # Sauvegarder
    sample_path = Path(__file__).parent / "sample_complete.jpg"
    cv2.imwrite(str(sample_path), image)
    print(f"✓ Image sauvegardée: {sample_path.name}")
    print(f"  Dimensions: {image.shape}")
    
    # Initialiser le processeur
    print("\n✓ Initialisation du processeur avec tous les modules...")
    processor = ImageProcessor(optimization="balanced")
    
    # Activer les modules pertinents
    processor.config.enable_module('text_detection', True)
    processor.config.enable_module('shape_detection', True)
    processor.config.enable_module('visual_analysis', True)
    processor.config.enable_module('distance_measurement', True)
    
    status = processor.get_status()
    print("\n  Modules activés:")
    for module_name, config in status.items():
        enabled = "✓" if config['enabled'] else "✗"
        print(f"    {enabled} {module_name}")
    
    # Analyse visuelle
    print("\n" + "=" * 70)
    print("ÉTAPE 1: Analyse Visuelle")
    print("=" * 70)
    
    try:
        if processor.visual_analyzer:
            analysis = processor.visual_analyzer.analyze(image)
            print(f"\n  ✓ Analyse terminée")
            print(f"    Luminosité: {analysis.get('brightness', 'N/A'):.2f}/255")
            print(f"    Saturation: {analysis.get('saturation', 'N/A'):.2f}")
            print(f"    Contraste: {analysis.get('contrast', 'N/A'):.2f}")
    except Exception as e:
        print(f"  ⚠️  Analyse visuelle non disponible: {e}")
    
    # Détection de formes
    print("\n" + "=" * 70)
    print("ÉTAPE 2: Détection de Formes")
    print("=" * 70)
    
    try:
        if processor.shape_detector:
            shapes = processor.shape_detector.detect(image)
            print(f"\n  ✓ {len(shapes)} forme(s) détectée(s)")
            for i, shape in enumerate(shapes[:5], 1):
                print(f"    Forme {i}: {shape.get('type', 'unknown')} "
                      f"@({shape.get('x', 'N/A')}, {shape.get('y', 'N/A')})")
            if len(shapes) > 5:
                print(f"    ... et {len(shapes)-5} autres formes")
    except Exception as e:
        print(f"  ⚠️  Détection formes non disponible: {e}")
    
    # Détection de texte
    print("\n" + "=" * 70)
    print("ÉTAPE 3: Détection de Texte")
    print("=" * 70)
    
    try:
        if processor.text_detector:
            regions = processor.text_detector.detect(image)
            print(f"\n  ✓ {len(regions)} région(s) de texte détectée(s)")
            
            text_preview = processor.text_detector.extract_text(image)
            lines = text_preview.split('\n')[:5]
            print(f"\n  Aperçu du texte extrait:")
            for line in lines:
                if line.strip():
                    preview = line[:50] + "..." if len(line) > 50 else line
                    print(f"    • {preview}")
    except Exception as e:
        print(f"  ⚠️  Détection texte non disponible: {e}")
    
    # Résumé et recommandations
    print("\n" + "=" * 70)
    print("RÉSUMÉ ET RECOMMANDATIONS")
    print("=" * 70)
    
    print("""
    ✅ Pipeline de traitement complété avec succès!
    
    Modules utilisés dans cet exemple:
    1. Analyse Visuelle - Pour évaluer la qualité de l'image
    2. Détection de Formes - Pour identifier les éléments graphiques
    3. Détection de Texte - Pour extraire le contenu textuel
    4. Mesure de Distances - Pour les annotations géométriques
    
    Cas d'usage:
    • Numérisation de documents
    • Analyse de photos de documents
    • Extraction d'informations automatisée
    • Vérification de qualité d'image
    """)


if __name__ == "__main__":
    example_complete_workflow()
