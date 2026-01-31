"""
Exemple 3: Performance Modes - Comparaison des Modes de Performance
Démontre comment choisir le bon mode selon vos besoins
"""

import cv2
import sys
import time
import numpy as np
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from imgprocessor.text_detection import TextDetector


def create_complex_text_image():
    """Crée une image avec plusieurs textes de tailles différentes."""
    image = np.full((500, 700, 3), 255, dtype=np.uint8)
    
    # Texte gros
    cv2.putText(image, "BIG TEXT", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 3)
    
    # Texte moyen
    cv2.putText(image, "Medium sized text here", (50, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 100, 200), 2)
    
    # Petit texte
    cv2.putText(image, "Small text", (50, 350), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (100, 0, 0), 1)
    
    # Paragraphe
    cv2.putText(image, "This is a longer paragraph with", (50, 430), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 100, 0), 1)
    cv2.putText(image, "multiple lines of text", (50, 460), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 100, 0), 1)
    
    return image


def example_performance_modes():
    """Exemple comparant les différents modes de performance."""
    print("=" * 60)
    print("Exemple 3: Comparaison des Modes de Performance")
    print("=" * 60)
    
    # Créer image
    print("\n✓ Création d'une image de test...")
    image = create_complex_text_image()
    
    # Sauvegarder
    sample_path = Path(__file__).parent / "sample_text_complex.jpg"
    cv2.imwrite(str(sample_path), image)
    
    modes = ['speed', 'balanced', 'quality']
    results = {}
    
    print("\n" + "=" * 60)
    print("COMPARAISON DES MODES")
    print("=" * 60)
    
    for mode in modes:
        print(f"\n🔄 Mode: {mode.upper()}")
        print("-" * 40)
        
        detector = TextDetector(engine='easyocr', mode=mode)
        
        # Chronomètre
        start = time.time()
        regions = detector.detect(image)
        elapsed = (time.time() - start) * 1000
        
        stats = detector.get_cache_stats()
        
        print(f"  ⏱️  Temps: {elapsed:.2f}ms")
        print(f"  📊 Régions détectées: {len(regions)}")
        
        if regions:
            confidence = sum(r.confidence for r in regions) / len(regions)
            print(f"  🎯 Confiance moyenne: {confidence:.1%}")
        
        results[mode] = {
            'time': elapsed,
            'regions': len(regions),
            'confidence': confidence if regions else 0
        }
    
    # Résumé
    print("\n" + "=" * 60)
    print("RÉSUMÉ DES PERFORMANCES")
    print("=" * 60)
    
    fastest = min(results.items(), key=lambda x: x[1]['time'])
    slowest = max(results.items(), key=lambda x: x[1]['time'])
    
    print(f"\n⚡ Plus rapide: {fastest[0].upper()} ({fastest[1]['time']:.2f}ms)")
    print(f"🐢 Plus lent: {slowest[0].upper()} ({slowest[1]['time']:.2f}ms)")
    
    speedup = slowest[1]['time'] / fastest[1]['time']
    print(f"📈 Accélération: {speedup:.1f}x")
    
    print("\n" + "=" * 60)
    print("RECOMMANDATIONS")
    print("=" * 60)
    print("""
    ⚡ SPEED (Rapide):
       - Utiliser pour: Texte gros/clair uniquement
       - Résolution réduite = plus rapide mais moins précis
       
    ⚙️  BALANCED (Équilibré):
       - Utiliser pour: Usage général, cas d'usage standards
       - Bon compromis vitesse/précision
       
    🎯 QUALITY (Qualité):
       - Utiliser pour: Petit texte, haute précision requise
       - Plus lent mais résultats meilleurs
    """)


if __name__ == "__main__":
    example_performance_modes()
