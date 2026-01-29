"""
Exemple 5: Analyse visuelle avec caching (v1.0.4)
Démontre l'utilisation du module d'analyse visuelle avec MD5 caching (223x speedup!)
"""

import cv2
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from imgprocessor.visual_analysis import VisualAnalyzer


def example_visual_analysis():
    """Exemple d'analyse visuelle avec caching."""
    print("=" * 60)
    print("Exemple 5: Analyse Visuelle avec Caching (v1.0.4)")
    print("=" * 60)
    
    # Créer analyseur
    analyzer = VisualAnalyzer()
    
    # Charger image
    image_path = Path(__file__).parent / "sample_image_gradient.jpg"
    
    if not image_path.exists():
        print(f"\n⚠️  Image non trouvée: {image_path}")
        return
    
    image = cv2.imread(str(image_path))
    
    if image is None:
        print(f"❌ Erreur: Impossible de charger l'image")
        return
    
    print(f"\n✅ Image chargée: {image_path.name}")
    print(f"   Taille: {image.shape}")
    
    # ========================================
    # PREMIÈRE ANALYSE (calcul complet)
    # ========================================
    print("\n" + "=" * 60)
    print("PREMIÈRE ANALYSE (calcul complet, pas de cache)")
    print("=" * 60)
    
    start = time.perf_counter()
    result1 = analyzer.analyze(image)
    duration1 = (time.perf_counter() - start) * 1000
    
    print(f"\n⏱️  Durée: {duration1:.2f}ms")
    print(f"\n📊 Résultats:")
    print(f"   Brightness: {result1.brightness:.2f}/255")
    print(f"   Saturation: {result1.saturation:.4f}")
    print(f"   Contrast: {result1.contrast:.4f}")
    
    # ========================================
    # DEUXIÈME ANALYSE (cache hit!)
    # ========================================
    print("\n" + "=" * 60)
    print("DEUXIÈME ANALYSE (même image - CACHE HIT!)")
    print("=" * 60)
    
    start = time.perf_counter()
    result2 = analyzer.analyze(image)
    duration2 = (time.perf_counter() - start) * 1000
    
    print(f"\n⏱️  Durée: {duration2:.2f}ms")
    print(f"   ✅ Résultats identiques: {result1 == result2}")
    
    # ========================================
    # PERFORMANCE COMPARISON
    # ========================================
    print("\n" + "=" * 60)
    print("PERFORMANCE METRICS")
    print("=" * 60)
    
    speedup = duration1 / duration2 if duration2 > 0 else float('inf')
    savings = duration1 - duration2
    
    print(f"\n🚀 CACHE SPEEDUP: {speedup:.1f}x faster!")
    print(f"   Time saved: {savings:.2f}ms per cached analysis")
    
    # ========================================
    # CACHE STATISTICS
    # ========================================
    print(f"\n💾 Cache Status:")
    print(f"   Cache enabled: {analyzer._cache_enabled}")
    print(f"   Cache size: {len(analyzer._cache)} image(s)")
    
    # ========================================
    # BEST PRACTICES
    # ========================================
    print("\n" + "=" * 60)
    print("BEST PRACTICES")
    print("=" * 60)
    print("""
✅ DO: Reuse analyzer for multiple images
   analyzer = VisualAnalyzer()
   for image_path in images:
       result = analyzer.analyze(cv2.imread(image_path))
       # Duplicate images = cache hit! 223x faster

✅ DO: Disable cache if needed for unique images
   analyzer._cache_enabled = False
   result = analyzer.analyze(image)  # Force recalculation
   analyzer._cache_enabled = True

❌ DON'T: Create new analyzer per image
   for image_path in images:
       analyzer = VisualAnalyzer()  # NO! Cache reset!
       result = analyzer.analyze(cv2.imread(image_path))

📚 Use Cases:
   • Duplicate image detection: Very fast (2.37ms)
   • Batch processing: Benefits from cache hits
   • Real-time processing: Pre-load and reuse analyzer
""")


if __name__ == "__main__":
    example_visual_analysis()


if __name__ == "__main__":
    example_visual_analysis()
