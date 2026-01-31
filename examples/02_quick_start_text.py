"""
Exemple 2: Démarrage Rapide avec Détection de Texte
Démontre la façon la plus simple d'utiliser la détection de texte
"""

import cv2
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from imgprocessor.text_detection import TextDetector


def create_sample_text_image():
    """Crée une image simple avec du texte."""
    import numpy as np
    
    # Créer une image blanche
    image = np.full((300, 400, 3), 255, dtype=np.uint8)
    
    # Ajouter du texte
    cv2.putText(image, "HELLO WORLD", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0), 2)
    cv2.putText(image, "This is a test", (30, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
    
    return image


def example_quick_start():
    """Exemple de démarrage rapide avec détection texte."""
    print("=" * 60)
    print("Exemple 2: Démarrage Rapide - Détection de Texte")
    print("=" * 60)
    
    # Créer un détecteur
    print("\n✓ Initialisation du détecteur de texte...")
    detector = TextDetector(engine='easyocr')
    
    # Créer une image d'exemple
    print("✓ Création d'une image d'exemple avec du texte...")
    image = create_sample_text_image()
    
    # Sauvegarder l'image
    sample_path = Path(__file__).parent / "sample_text.jpg"
    cv2.imwrite(str(sample_path), image)
    print(f"✓ Image sauvegardée: {sample_path.name}")
    
    # Détecter le texte
    print("\n✓ Détection du texte en cours...")
    regions = detector.detect(image)
    
    if regions:
        print(f"\n✅ {len(regions)} région(s) de texte détectée(s):\n")
        for i, region in enumerate(regions, 1):
            print(f"  Région {i}:")
            print(f"    Texte: {region.text}")
            print(f"    Confiance: {region.confidence:.1%}")
            print(f"    Position: {region.bbox}")
    else:
        print("\n⚠️  Aucun texte détecté")
    
    # Extrait simplement le texte
    print("\n" + "=" * 60)
    print("TEXTE COMPLET EXTRAIT:")
    print("=" * 60)
    text = detector.extract_text(image)
    if text:
        print(text)
    else:
        print("(Aucun texte détecté)")
    
    # Cache stats
    print("\n" + "=" * 60)
    print("INFORMATIONS DE PERFORMANCE:")
    print("=" * 60)
    stats = detector.get_cache_stats()
    print(f"  Moteur OCR: {stats['engine']}")
    print(f"  Mode: {stats['mode']}")
    print(f"  Cache activé: {stats['result_cache_enabled']}")
    print(f"  Résultats en cache: {stats['cached_results']}")


if __name__ == "__main__":
    example_quick_start()
