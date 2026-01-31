"""
Exemple 2: Détection de texte et extraction
Démontre l'utilisation avancée du module de détection de texte
"""

import cv2
import sys
import numpy as np
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from imgprocessor.text_detection import TextDetector


def create_sample_text_image_advanced():
    """Crée une image avec plusieurs textes."""
    image = np.full((400, 600, 3), 255, dtype=np.uint8)
    
    # Titre
    cv2.putText(image, "Detection Example", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 0), 2)
    
    # Textes de différentes tailles
    cv2.putText(image, "Large text here", (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 200), 2)
    cv2.putText(image, "Small text", (50, 250), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 0, 0), 1)
    cv2.putText(image, "Medium size", (50, 350), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 150, 0), 1)
    
    return image


def example_text_detection():
    """Exemple de détection de texte avancée."""
    print("=" * 60)
    print("Exemple 2: Détection de Texte - Utilisation Avancée")
    print("=" * 60)
    
    # Créer détecteur
    print("\n✓ Initialisation du détecteur...")
    detector = TextDetector(engine='easyocr', mode='balanced')
    
    print("\n📝 Modes disponibles:")
    print("  • detect() - Retourne les régions avec coordonnées")
    print("  • extract_text() - Retourne uniquement le texte")
    
    # Créer une image d'exemple
    print("\n✓ Création d'une image avec texte...")
    image = create_sample_text_image_advanced()
    
    # Sauvegarder l'image
    sample_path = Path(__file__).parent / "sample_image_with_points.jpg"
    cv2.imwrite(str(sample_path), image)
    print(f"✓ Image sauvegardée: {sample_path.name}")
    
    # ========================================
    # MODE 1: detect() - Régions avec coordonnées
    # ========================================
    print("\n" + "=" * 60)
    print("MODE 1: Détection avec Coordonnées")
    print("=" * 60)
    try:
        regions = detector.detect(image, min_confidence=0.5)
        if regions:
            print(f"✅ {len(regions)} région(s) détectée(s):\n")
            for i, region in enumerate(regions[:5], 1):
                print(f"  Région {i}:")
                print(f"    Texte: {region.text}")
                print(f"    Confiance: {region.confidence:.1%}")
                print(f"    Position: {region.bbox}")
            if len(regions) > 5:
                print(f"\n  ... et {len(regions)-5} autres régions")
        else:
            print("⚠️  Aucun texte détecté")
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    # ========================================
    # MODE 2: extract_text() - Texte simple
    # ========================================
    print("\n" + "=" * 60)
    print("MODE 2: Extraction Texte Simple")
    print("=" * 60)
    try:
        text = detector.extract_text(image, min_confidence=0.5)
        if text:
            print(f"✅ Texte extrait:")
            print(f"\n{text}")
        else:
            print("⚠️  Aucun texte détecté")
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    # ========================================
    # MODE 3: Filtrage par confiance
    # ========================================
    print("\n" + "=" * 60)
    print("MODE 3: Filtrage par Confiance")
    print("=" * 60)
    try:
        # Haute confiance (> 90%)
        regions_high = detector.detect(image, min_confidence=0.9)
        print(f"✓ Haute confiance (>90%): {len(regions_high)} région(s)")
        
        # Confiance normale (> 50%)
        regions_normal = detector.detect(image, min_confidence=0.5)
        print(f"✓ Confiance normale (>50%): {len(regions_normal)} région(s)")
        
        # Toute confiance (> 0%)
        regions_all = detector.detect(image, min_confidence=0.0)
        print(f"✓ Toute confiance (>0%): {len(regions_all)} région(s)")
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    # ========================================
    # RÉSUMÉ
    # ========================================
    print("\n" + "=" * 60)
    print("RÉSUMÉ")
    print("=" * 60)
    print("""
✅ Utilisation de TextDetector:
  
  1. detect(image) → List[TextRegion]
     • Retourne régions de texte avec coordonnées
     • Permet analyse détaillée
  
  2. extract_text(image) → str
     • Retourne texte brut combiné
     • Plus simple et rapide
  
  Paramètres:
  • min_confidence: Filtrer par confiance (0.0 à 1.0)
  • mode: 'speed', 'balanced', 'quality'
  • engine: 'easyocr' (par défaut)

📚 Bonnes pratiques:
  • Réutiliser la même instance pour plusieurs images
  • Mode 'speed' pour texte gros/clair
  • Mode 'quality' pour petit texte/haute précision
""")


if __name__ == "__main__":
    example_text_detection()
