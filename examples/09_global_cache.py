"""
Exemple 6: Cache Global et Optimisations
Démontre comment le caching global optimise les performances
"""

import cv2
import sys
import time
import numpy as np
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from imgprocessor.text_detection import TextDetector


def create_sample_image_with_text():
    """Crée une image simple."""
    image = np.full((300, 400, 3), 255, dtype=np.uint8)
    cv2.putText(image, "CACHE TEST", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 0), 2)
    cv2.putText(image, "Same image", (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (100, 0, 0), 1)
    return image


def example_global_cache():
    """Exemple montrant l'efficacité du cache global."""
    print("=" * 70)
    print("Exemple 6: Cache Global et Optimisations")
    print("=" * 70)
    
    print("""
    Le cache global fonctionne à deux niveaux:
    1. Cache du modèle: Chaque moteur OCR est chargé une seule fois
    2. Cache des résultats: Les images identiques retournent le résultat immédiatement
    """)
    
    # Créer image
    print("\n✓ Création d'une image de test...")
    image = create_sample_image_with_text()
    
    # Sauvegarder
    sample_path = Path(__file__).parent / "sample_cache_test.jpg"
    cv2.imwrite(str(sample_path), image)
    
    print("\n" + "=" * 70)
    print("TEST 1: Cache du Modèle (première instance)")
    print("=" * 70)
    
    start = time.time()
    detector1 = TextDetector(engine='easyocr', mode='balanced')
    elapsed1 = (time.time() - start) * 1000
    print(f"⏱️  Initialisation: {elapsed1:.2f}ms")
    
    stats1 = detector1.get_cache_stats()
    print(f"   Modèle chargé: {stats1['model_cached']}")
    
    print("\n" + "=" * 70)
    print("TEST 2: Réutilisation du Cache du Modèle (deuxième instance)")
    print("=" * 70)
    
    start = time.time()
    detector2 = TextDetector(engine='easyocr', mode='balanced')
    elapsed2 = (time.time() - start) * 1000
    print(f"⏱️  Initialisation: {elapsed2:.2f}ms")
    
    stats2 = detector2.get_cache_stats()
    print(f"   Modèle chargé: {stats2['model_cached']}")
    
    if elapsed1 > 0:
        speedup = elapsed1 / elapsed2 if elapsed2 > 0 else float('inf')
        print(f"\n✅ Accélération avec cache modèle: {speedup:.1f}x")
    
    print("\n" + "=" * 70)
    print("TEST 3: Cache des Résultats (même image)")
    print("=" * 70)
    
    # Première détection
    print("  Première détection:")
    start = time.time()
    regions1 = detector1.detect(image)
    elapsed_first = (time.time() - start) * 1000
    print(f"    ⏱️  Temps: {elapsed_first:.2f}ms")
    print(f"    📊 Régions: {len(regions1)}")
    
    # Deuxième détection (même image)
    print("\n  Deuxième détection (même image):")
    start = time.time()
    regions2 = detector1.detect(image)
    elapsed_cached = (time.time() - start) * 1000
    print(f"    ⏱️  Temps: {elapsed_cached:.2f}ms")
    print(f"    📊 Régions: {len(regions2)}")
    
    if elapsed_first > 0:
        cache_speedup = elapsed_first / elapsed_cached if elapsed_cached > 0 else float('inf')
        print(f"\n✅ Accélération avec cache résultats: {cache_speedup:.1f}x")
    
    print("\n" + "=" * 70)
    print("STATISTIQUES FINALES")
    print("=" * 70)
    
    stats = detector1.get_cache_stats()
    print(f"\n  Moteur OCR: {stats['engine']}")
    print(f"  Mode: {stats['mode']}")
    print(f"  Cache activé: {stats['result_cache_enabled']}")
    print(f"  Résultats en cache: {stats['cached_results']}")
    print(f"  Taille cache global: {stats['global_model_cache_size']}")
    
    print("\n" + "=" * 70)
    print("BONNES PRATIQUES")
    print("=" * 70)
    
    print("""
    ✅ FAIRE:
    • Réutiliser la même instance de TextDetector pour plusieurs images
    • Activez le cache pour les images qui se répètent
    • Utilisez 'balanced' ou 'speed' pour usage général
    
    ❌ NE PAS FAIRE:
    • Créer une nouvelle instance pour chaque image
    • Désactiver le cache pour chaque image
    • Ignorer les logs de cache pour optimiser
    
    💡 CONSEIL:
    detector = TextDetector(engine='easyocr')  # Une seule fois!
    for image in images:
        text = detector.extract_text(image)  # Réutiliser
    """)


if __name__ == "__main__":
    example_global_cache()
