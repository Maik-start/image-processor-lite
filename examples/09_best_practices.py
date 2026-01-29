"""
Exemple 9: Production Best Practices avec v1.0.4
Montre les patterns recommandés pour maximiser les performances en production.
"""

import cv2
import sys
import time
from pathlib import Path
from typing import List, Tuple
import json

sys.path.insert(0, str(Path(__file__).parent.parent))

from imgprocessor import ImageProcessor
from imgprocessor.visual_analysis import VisualAnalyzer
from imgprocessor.text_detection import TextDetector
from imgprocessor.shape_detection import ShapeDetector
from imgprocessor.distance_measurement import DistanceMeasurer


class OptimizedImagePipeline:
    """
    Pipeline optimisée pour traitement batch d'images.
    Utilise caching, warmup, et APIs flexibles.
    """
    
    def __init__(self):
        """Initialise tous les modules avec warmup."""
        print("🔧 Initialisation du pipeline optimisé...")
        
        # Les modules sont pré-warmés pendant l'init
        self.analyzer = VisualAnalyzer()
        self.text_detector = TextDetector(engine='easyocr')
        self.shape_detector = ShapeDetector()
        self.distance_measurer = DistanceMeasurer()
        
        print("✅ Pipeline prêt (warmup terminé)")
    
    def analyze_batch(self, image_paths: List[str]) -> List[dict]:
        """
        Analyse un batch d'images avec caching intelligent.
        Images identiques profitent du cache (223x faster!).
        """
        print(f"\n📦 Traitement batch: {len(image_paths)} image(s)")
        results = []
        
        for i, img_path in enumerate(image_paths, 1):
            print(f"\n   [{i}/{len(image_paths)}] {Path(img_path).name}")
            
            image = cv2.imread(img_path)
            if image is None:
                print(f"      ❌ Impossible de charger l'image")
                continue
            
            start = time.perf_counter()
            
            # Analyse visuelle (avec caching!)
            visual = self.analyzer.analyze(image)
            
            # Détection texte (mode coords-only pour économiser mémoire)
            text_regions = self.text_detector.extract_text(
                image, 
                return_text=False, 
                return_coords=True
            )
            
            # Détection formes
            shapes = self.shape_detector.detect(image)
            
            duration = (time.perf_counter() - start) * 1000
            
            result = {
                'file': Path(img_path).name,
                'duration_ms': round(duration, 2),
                'visual': {
                    'brightness': round(visual.brightness, 2),
                    'saturation': round(visual.saturation, 2),
                    'contrast': round(visual.contrast, 2),
                },
                'text_regions': len(text_regions) if text_regions else 0,
                'shapes_detected': len(shapes) if shapes else 0,
            }
            
            results.append(result)
            print(f"      ⏱️  {duration:.2f}ms - Visual:{result['visual']['brightness']}, "
                  f"Text:{result['text_regions']}, Shapes:{result['shapes_detected']}")
        
        return results


def example_best_practices():
    """Démontre les best practices pour production."""
    print("\n" + "=" * 70)
    print("BEST PRACTICES FOR PRODUCTION")
    print("=" * 70)
    
    print("\n1️⃣  INITIALIZATION - Initialiser les modules au démarrage")
    print("""
    # ✅ BON: Créer détecteurs au démarrage (warmup en arrière-plan)
    detector = TextDetector(engine='easyocr')
    analyzer = VisualAnalyzer()
    
    # ❌ MAUVAIS: Créer à chaque image (latence x10!)
    for image_path in images:
        detector = TextDetector(engine='easyocr')  # LENT!
        text = detector.extract_text(image)
    """)
    
    print("\n2️⃣  CACHING - Profiter du caching visual analysis")
    print("""
    # ✅ BON: Images identiques = cache hit (223x faster)
    for image in duplicate_images:
        result = analyzer.analyze(image)  # 2.37ms après 1ère!
    
    # ❌ MAUVAIS: Créer nouvel analyzer à chaque fois
    for image in duplicate_images:
        analyzer = VisualAnalyzer()  # Nouveau cache = calcul complet
        result = analyzer.analyze(image)
    """)
    
    print("\n3️⃣  FLEXIBLE API - Retourner seulement ce qui est nécessaire")
    print("""
    # ✅ BON: Demander uniquement les coords si texte pas needed
    coords = detector.extract_text(image, return_text=False, return_coords=True)
    
    # ✅ BON: Text only si coords pas needed
    text = detector.extract_text(image, return_text=True, return_coords=False)
    
    # ✅ BON: Both si nécessaire
    text, coords = detector.extract_text(image, return_text=True, return_coords=True)
    
    # ❌ MAUVAIS: Toujours retourner tout
    text, coords = detector.extract_text(image)  # Calculs inutiles
    """)
    
    print("\n4️⃣  BATCH PROCESSING - Optimiser pour traitements batch")
    print("""
    # ✅ BON: Réutiliser modules pour batch
    detector = TextDetector(engine='easyocr')
    for image_path in image_paths:
        text = detector.extract_text(cv2.imread(image_path))
    
    # ❌ MAUVAIS: Créer/destroy modules à la boucle
    for image_path in image_paths:
        detector = TextDetector(engine='easyocr')  # x1000 = x1000 temps!
        text = detector.extract_text(cv2.imread(image_path))
    """)
    
    print("\n5️⃣  ERROR HANDLING - Gérer les cas limites")
    print("""
    # ✅ BON: Vérifier image avant traitement
    image = cv2.imread(image_path)
    if image is None:
        print(f"Erreur: {image_path} non trouvable")
        continue
    
    try:
        text = detector.extract_text(image)
    except Exception as e:
        print(f"Erreur OCR: {e}")
        text = ""
    
    # ❌ MAUVAIS: Pas de validation
    text = detector.extract_text(cv2.imread(image_path))  # Peut crash!
    """)


def example_performance_metrics():
    """Affiche les métriques de performance attendues."""
    print("\n" + "=" * 70)
    print("EXPECTED PERFORMANCE METRICS")
    print("=" * 70)
    
    metrics = {
        'Visual Analysis (cache hit)': {
            'latency_ms': 2.37,
            'throughput_per_sec': 421,
            'improvement': '223x'
        },
        'Distance Measurement': {
            'latency_ms': 0.02,
            'throughput_per_sec': 50000,
            'improvement': 'fixed'
        },
        'Text Detection (image 640x480)': {
            'latency_ms': 534,
            'throughput_per_sec': 2,
            'improvement': 'ML-limited'
        },
        'Shape Detection (small)': {
            'latency_ms': 4.27,
            'throughput_per_sec': 234,
            'improvement': 'stable'
        },
    }
    
    print("\n📊 Latence (ms) et Débit (images/sec):\n")
    for module, stats in metrics.items():
        print(f"   {module:35} | {stats['latency_ms']:6.2f}ms | "
              f"{stats['throughput_per_sec']:6.0f} img/s | {stats['improvement']}")
    
    print("\n💡 Notes:")
    print("   • Visual Analysis: Beaucoup plus rapide avec cache hit")
    print("   • Distance Measurement: Pratiquement O(1)")
    print("   • Text Detection: Limité par modèle ML (GPU recommandé)")
    print("   • Shape Detection: O(n) - scaling linéaire avec nombre de formes")


def example_batch_processing():
    """Exécute un batch processing optimisé."""
    print("\n" + "=" * 70)
    print("BATCH PROCESSING EXAMPLE")
    print("=" * 70)
    
    # Images de test
    image_dir = Path(__file__).parent
    sample_images = [
        image_dir / "sample_image_gradient.jpg",
        image_dir / "sample_image_with_shapes.jpg",
        image_dir / "sample_image_with_points.jpg",
    ]
    
    # Filtrer images existantes
    valid_images = [str(img) for img in sample_images if img.exists()]
    
    if not valid_images:
        print("⚠️  Aucune image d'exemple trouvée")
        return
    
    # Pipeline optimisée
    pipeline = OptimizedImagePipeline()
    
    # Traiter batch
    results = pipeline.analyze_batch(valid_images)
    
    # Afficher résultats
    print("\n📈 Résultats batch:")
    print(json.dumps(results, indent=2))
    
    # Statistiques
    if results:
        total_time = sum(r['duration_ms'] for r in results)
        avg_time = total_time / len(results)
        print(f"\n📊 Stats:")
        print(f"   Total: {total_time:.2f}ms")
        print(f"   Moyenne: {avg_time:.2f}ms/image")
        print(f"   Débit: {1000/avg_time:.1f} images/sec")


def main():
    """Exécute tous les exemples best practices."""
    print("\n" + "=" * 70)
    print("🚀 IMAGE-PROCESSOR-LITE v1.0.4 - BEST PRACTICES")
    print("=" * 70)
    
    # Exécuter les exemples
    example_best_practices()
    example_performance_metrics()
    example_batch_processing()
    
    print("\n" + "=" * 70)
    print("✅ Best practices démontrées!")
    print("=" * 70)
    print("\n📚 Ressources:")
    print("   • Docs complets: https://github.com/Maik-start/imgprocessor/wiki")
    print("   • Performance guide: Voir PERFORMANCE_BENCHMARK_REPORT.md")
    print("   • Issues/Questions: https://github.com/Maik-start/imgprocessor/issues")


if __name__ == "__main__":
    main()
