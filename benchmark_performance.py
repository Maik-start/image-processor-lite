"""
Benchmark de Performance - image-processor-lite
Mesure les améliorations apportées par le lazy-loading
"""

import time
import cv2
import numpy as np
from imgprocessor import ImageProcessor
from imgprocessor.text_detection import TextDetector

class PerformanceBenchmark:
    """Classe pour benchmarker les performances"""
    
    def __init__(self):
        self.results = {}
    
    def benchmark_function(self, name, func, iterations=3):
        """Benchmarker une fonction et enregistrer les résultats"""
        print(f"\n📊 Benchmarking: {name}")
        print("-" * 60)
        
        times = []
        for i in range(iterations):
            start = time.time()
            func()
            elapsed = time.time() - start
            times.append(elapsed)
            print(f"   Itération {i+1}: {elapsed*1000:.2f}ms")
        
        avg_time = sum(times) / len(times)
        min_time = min(times)
        max_time = max(times)
        
        self.results[name] = {
            'avg': avg_time,
            'min': min_time,
            'max': max_time,
            'times': times
        }
        
        print(f"   Moyenne: {avg_time*1000:.2f}ms")
        print(f"   Min/Max: {min_time*1000:.2f}ms / {max_time*1000:.2f}ms")
        
        return avg_time
    
    def print_summary(self):
        """Afficher un résumé des résultats"""
        print("\n" + "="*70)
        print("📈 RÉSUMÉ DES BENCHMARKS")
        print("="*70)
        
        for name, data in self.results.items():
            avg_ms = data['avg'] * 1000
            print(f"\n{name}:")
            print(f"  Moyenne: {avg_ms:.2f}ms")
            print(f"  Min: {data['min']*1000:.2f}ms")
            print(f"  Max: {data['max']*1000:.2f}ms")

def test_imageprocessor_init():
    """Test d'initialisation de ImageProcessor"""
    print("\n" + "╔" + "="*68 + "╗")
    print("║" + " "*15 + "🚀 BENCHMARK PERFORMANCE" + " "*30 + "║")
    print("╚" + "="*68 + "╝")
    
    benchmark = PerformanceBenchmark()
    
    # Test 1: Initialisation simple
    print("\n" + "="*70)
    print("TEST 1: Initialisation ImageProcessor (lazy-loading)")
    print("="*70)
    
    benchmark.benchmark_function(
        "ImageProcessor() init",
        lambda: ImageProcessor(),
        iterations=5
    )
    
    # Test 2: Initialisation avec configuration
    print("\n" + "="*70)
    print("TEST 2: Configuration avec text_detection")
    print("="*70)
    
    def init_with_text():
        processor = ImageProcessor()
        processor.config.disable_all_modules()
        processor.config.enable_module('text_detection', True)
        processor.config.set_module_options('text_detection', {
            'engine': 'easyocr',
            'language': ['fra', 'eng']
        })
        return processor
    
    benchmark.benchmark_function(
        "ImageProcessor() + text_detection config",
        init_with_text,
        iterations=3
    )
    
    # Test 3: TextDetector initialization
    print("\n" + "="*70)
    print("TEST 3: TextDetector initialization")
    print("="*70)
    
    benchmark.benchmark_function(
        "TextDetector(engine='easyocr') init",
        lambda: TextDetector(engine='easyocr'),
        iterations=5
    )
    
    # Test 4: Création d'image de test
    print("\n" + "="*70)
    print("TEST 4: Création d'images de test")
    print("="*70)
    
    benchmark.benchmark_function(
        "Création image 100x100x3",
        lambda: np.ones((100, 100, 3), dtype=np.uint8),
        iterations=5
    )
    
    benchmark.benchmark_function(
        "Création image 640x480x3",
        lambda: np.ones((640, 480, 3), dtype=np.uint8),
        iterations=5
    )
    
    # Print summary
    benchmark.print_summary()

def test_text_extraction():
    """Test d'extraction de texte"""
    print("\n" + "="*70)
    print("TEST 5: Extraction de texte")
    print("="*70)
    
    processor = ImageProcessor()
    processor.config.disable_all_modules()
    processor.config.enable_module('text_detection', True)
    processor.config.set_module_options('text_detection', {
        'engine': 'easyocr',
        'language': ['fra', 'eng']
    })
    
    image = np.ones((100, 100, 3), dtype=np.uint8) * 255
    
    print("\n📊 Benchmarking: Premier appel extract_text() (charge le moteur)")
    print("-" * 60)
    
    start = time.time()
    try:
        text = processor.extract_text(image)
        elapsed = time.time() - start
        print(f"   Temps: {elapsed*1000:.2f}ms")
        print(f"   Texte trouvé: {len(text)} caractères")
    except Exception as e:
        print(f"   ⚠️  Erreur: {e}")
        elapsed = time.time() - start
        print(f"   Temps jusqu'à l'erreur: {elapsed*1000:.2f}ms")

def test_multiple_calls():
    """Test avec plusieurs appels"""
    print("\n" + "="*70)
    print("TEST 6: Plusieurs appels successifs")
    print("="*70)
    
    benchmark = PerformanceBenchmark()
    
    processor = ImageProcessor()
    processor.config.disable_all_modules()
    processor.config.enable_module('shape_detection', True)
    
    image = np.zeros((100, 100, 3), dtype=np.uint8)
    cv2.circle(image, (50, 50), 20, (255, 255, 255), -1)
    cv2.rectangle(image, (10, 10), (90, 90), (200, 200, 200), -1)
    
    print("\n📊 Benchmarking: Détection de formes")
    print("-" * 60)
    
    def detect_shapes():
        shapes = processor.detect_shapes(image)
        return shapes
    
    benchmark.benchmark_function(
        "detect_shapes() (cercle + rectangle)",
        detect_shapes,
        iterations=5
    )
    
    benchmark.print_summary()

def compare_configurations():
    """Comparer différentes configurations"""
    print("\n" + "="*70)
    print("TEST 7: Comparaison des configurations")
    print("="*70)
    
    print("\n📊 Configuration 1: Module text_detection seul (lazy-loading)")
    print("-" * 60)
    
    start = time.time()
    p1 = ImageProcessor()
    p1.config.disable_all_modules()
    p1.config.enable_module('text_detection', True)
    time1 = time.time() - start
    print(f"Temps init: {time1*1000:.2f}ms")
    
    print("\n📊 Configuration 2: Modules shapes et distance")
    print("-" * 60)
    
    start = time.time()
    p2 = ImageProcessor()
    p2.config.disable_all_modules()
    p2.config.enable_module('shape_detection', True)
    p2.config.enable_module('distance_measurement', True)
    time2 = time.time() - start
    print(f"Temps init: {time2*1000:.2f}ms")
    
    print("\n📊 Configuration 3: Tous les modules activés")
    print("-" * 60)
    
    start = time.time()
    p3 = ImageProcessor()
    time3 = time.time() - start
    print(f"Temps init: {time3*1000:.2f}ms")
    
    print("\n📊 Résumé comparatif:")
    print("-" * 60)
    print(f"Config 1 (text): {time1*1000:.2f}ms")
    print(f"Config 2 (shapes + distance): {time2*1000:.2f}ms")
    print(f"Config 3 (tous): {time3*1000:.2f}ms")

def run_all_benchmarks():
    """Exécuter tous les benchmarks"""
    try:
        test_imageprocessor_init()
        test_text_extraction()
        test_multiple_calls()
        compare_configurations()
        
        print("\n" + "╔" + "="*68 + "╗")
        print("║" + " "*20 + "✅ BENCHMARKS TERMINÉS" + " "*25 + "║")
        print("╚" + "="*68 + "╝\n")
        
        return True
    except Exception as e:
        print(f"\n❌ ERREUR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = run_all_benchmarks()
    exit(0 if success else 1)
