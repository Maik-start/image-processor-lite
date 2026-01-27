"""
Exemple 6: Optimisation et complexité d'images
Démontre l'utilisation des profils d'optimisation selon la complexité
"""

import cv2
import numpy as np
import time
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from imgprocessor import ImageProcessor, ImageOptimizer


def benchmark_processor(processor, image, name):
    """Benchmark un processeur."""
    print(f"\n  {name}:")
    
    start = time.time()
    shapes = processor.detect_shapes(image)
    text_time = time.time() - start
    
    print(f"    Temps: {text_time:.3f}s")
    if shapes:
        print(f"    Formes détectées: {len(shapes)}")
    return text_time


def example_optimization():
    """Exemple d'optimisation et gestion de complexité."""
    print("=" * 70)
    print("Exemple 6: Optimisation et Gestion de Complexité d'Images")
    print("=" * 70)
    
    # Créer une image de test
    print("\nCréation d'une image de test...")
    image = np.ones((800, 1000, 3), dtype=np.uint8) * 255
    
    # Ajouter des formes
    cv2.circle(image, (150, 150), 80, (0, 0, 255), -1)
    cv2.rectangle(image, (300, 100), (500, 250), (0, 255, 0), -1)
    cv2.circle(image, (750, 200), 60, (255, 0, 0), -1)
    
    # Ajouter du bruit pour augmenter la complexité
    noise = np.random.normal(0, 15, image.shape).astype(np.uint8)
    image = cv2.add(image, noise)
    
    print(f"  Dimensions: {image.shape[1]}x{image.shape[0]}")
    
    # Test 1: Analyse de complexité
    print("\n" + "-" * 70)
    print("ANALYSE DE COMPLEXITÉ")
    print("-" * 70)
    
    optimizer = ImageOptimizer("balanced")
    complexity = optimizer.detect_complexity(image)
    print(f"\n✓ Complexité détectée: {complexity.value}")
    
    # Test 2: Comparaison des profils d'optimisation
    print("\n" + "-" * 70)
    print("COMPARAISON DES PROFILS D'OPTIMISATION")
    print("-" * 70)
    
    profiles = ["speed", "balanced", "quality"]
    times = {}
    
    for profile in profiles:
        print(f"\nProfil: {profile.upper()}")
        processor = ImageProcessor(optimization=profile)
        processor.config.enable_module('text_detection', False)
        processor.config.enable_module('distance_measurement', False)
        processor.config.enable_module('visual_analysis', False)
        
        # Benchmark
        times[profile] = benchmark_processor(processor, image, f"Exécution")
    
    # Résumé des temps
    print("\n" + "-" * 70)
    print("RÉSUMÉ DES TEMPS D'EXÉCUTION")
    print("-" * 70)
    
    speed_time = times["speed"]
    for profile in profiles:
        ratio = times[profile] / speed_time
        print(f"  {profile.upper():10} - {times[profile]:7.3f}s (x{ratio:.2f})")
    
    print(f"\nGain de vitesse (speed vs quality): {times['quality']/times['speed']:.2f}x")
    
    # Test 3: Paramètres optimisés
    print("\n" + "-" * 70)
    print("PARAMÈTRES OPTIMISÉS PAR COMPLEXITÉ")
    print("-" * 70)
    
    resized, info = optimizer.preprocess_image(image)
    print(f"\nImage originale: {image.shape[1]}x{image.shape[0]}")
    print(f"Image redimensionnée: {resized.shape[1]}x{resized.shape[0]}")
    print(f"Facteur d'échelle: {info['scale']:.2f}x")
    print(f"Complexité: {info['complexity']}")
    
    print(f"\nParamètres appliqués:")
    for key, value in info['params'].items():
        print(f"  {key}: {value}")
    
    # Test 4: Traitement sans optimisation
    print("\n" + "-" * 70)
    print("AVEC/SANS OPTIMISATION")
    print("-" * 70)
    
    processor = ImageProcessor(optimization="balanced")
    processor.config.enable_module('text_detection', False)
    processor.config.enable_module('distance_measurement', False)
    processor.config.enable_module('visual_analysis', False)
    
    # Avec optimisation
    print("\n  Avec optimisation:")
    start = time.time()
    shapes_opt = processor.detect_shapes(image, optimize=True)
    time_opt = time.time() - start
    print(f"    Temps: {time_opt:.3f}s")
    print(f"    Formes: {len(shapes_opt) if shapes_opt else 0}")
    
    # Sans optimisation
    print("\n  Sans optimisation:")
    processor.optimization_enabled = False
    start = time.time()
    shapes_no_opt = processor.detect_shapes(image, optimize=False)
    time_no_opt = time.time() - start
    print(f"    Temps: {time_no_opt:.3f}s")
    print(f"    Formes: {len(shapes_no_opt) if shapes_no_opt else 0}")
    
    speedup = time_no_opt / time_opt if time_opt > 0 else 0
    print(f"\n  Accélération: {speedup:.2f}x plus rapide avec optimisation")
    
    print("\n" + "=" * 70)
    print("✓ Exemple terminé")
    print("=" * 70)


if __name__ == "__main__":
    example_optimization()
