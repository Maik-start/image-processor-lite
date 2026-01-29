"""
Exemple 2: Détection de texte et extraction (v1.0.4)
Démontre l'utilisation du module de détection de texte avec flexible API
"""

import cv2
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from imgprocessor.text_detection import TextDetector


def example_text_detection():
    """Exemple de détection de texte."""
    print("=" * 60)
    print("Exemple 2: Détection de Texte (v1.0.4)")
    print("=" * 60)
    
    # Créer détecteur
    detector = TextDetector(engine='easyocr')
    
    print("\n📝 3 modes d'extraction texte disponibles:")
    print("  1. Text only (défaut)")
    print("  2. Coordinates only")
    print("  3. Text + Coordinates")
    
    # Charger une image
    image_path = Path(__file__).parent / "sample_image_with_points.jpg"
    
    if not image_path.exists():
        print(f"\n⚠️  Image d'exemple non trouvée: {image_path}")
        print("    Créez une image test ou utilisez votre propre image.")
        return
    
    image = cv2.imread(str(image_path))
    
    if image is None:
        print(f"\n❌ Erreur: Impossible de charger l'image")
        return
    
    print(f"\n✅ Image chargée: {image_path.name}")
    
    # ========================================
    # MODE 1: Text only
    # ========================================
    print("\n" + "=" * 60)
    print("MODE 1: Text Only")
    print("=" * 60)
    try:
        text = detector.extract_text(image, return_text=True, return_coords=False)
        if text:
            print(f"Texte détecté:\n{text[:200]}...")
        else:
            print("⚠️  Aucun texte détecté")
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    # ========================================
    # MODE 2: Coordinates only
    # ========================================
    print("\n" + "=" * 60)
    print("MODE 2: Coordinates Only")
    print("=" * 60)
    try:
        coords = detector.extract_text(image, return_text=False, return_coords=True)
        if coords:
            print(f"Régions de texte détectées: {len(coords)}")
            for i, region in enumerate(coords[:3]):  # Afficher premiers 3
                print(f"\n  Région {i+1}:")
                print(f"    Text: {region.get('text', 'N/A')[:30]}")
                print(f"    Confiance: {region.get('confidence', 0):.2%}")
                print(f"    Position: {region.get('bbox', 'N/A')}")
            if len(coords) > 3:
                print(f"\n  ... et {len(coords)-3} autres régions")
        else:
            print("⚠️  Aucune région de texte détectée")
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    # ========================================
    # MODE 3: Text + Coordinates
    # ========================================
    print("\n" + "=" * 60)
    print("MODE 3: Text + Coordinates")
    print("=" * 60)
    try:
        result = detector.extract_text(image, return_text=True, return_coords=True)
        if isinstance(result, tuple):
            text, coords = result
            print(f"Texte complet:")
            print(f"  {text[:100]}...")
            print(f"\nRégions avec coordonnées: {len(coords)}")
        else:
            print("⚠️  Mode non supporté par ce moteur")
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    # ========================================
    # RÉSUMÉ
    # ========================================
    print("\n" + "=" * 60)
    print("RÉSUMÉ")
    print("=" * 60)
    print("""
✅ Flexible API Features:
  • Économise mémoire (retourner uniquement ce dont vous avez besoin)
  • Performance optimisée (pas de calculs inutiles)
  • 100% backward compatible

📚 Utilisation recommandée:
  • Mode 1 (text only): Extraction texte simple
  • Mode 2 (coords only): Localisation des régions
  • Mode 3 (both): Analyse complète
""")


if __name__ == "__main__":
    example_text_detection()
