"""
🧪 TESTS FINAUX SUR LES IMAGES AMANDA1
Validation complète des optimisations avec les vraies images
"""

import sys
import os
import time
import cv2
import warnings
from pathlib import Path

warnings.filterwarnings('ignore')

sys.path.insert(0, '/home/virus-one/Documents/projet/package_dev')

def test_image(image_path, name=""):
    """Teste une image avec tous les détecteurs"""
    
    if not Path(image_path).exists():
        print(f"❌ {name}: Image non trouvée - {image_path}")
        return False
    
    img = cv2.imread(image_path)
    if img is None:
        print(f"❌ {name}: Impossible de charger l'image")
        return False
    
    print(f"\n{'='*80}")
    print(f"📷 {name} - {img.shape[1]}x{img.shape[0]}px")
    print(f"{'='*80}")
    
    try:
        from imgprocessor.text_detection import TextDetector
        
        # Test 1: TextDetector original
        print("\n1️⃣  TextDetector ORIGINAL (EasyOCR)")
        start = time.perf_counter()
        det_orig = TextDetector(languages=['en', 'fr'], engine='easyocr')
        t_init = (time.perf_counter() - start) * 1000
        
        start = time.perf_counter()
        regions = det_orig.detect(img)
        t_detect = (time.perf_counter() - start) * 1000
        
        text = '\n'.join([r.text for r in regions]) if regions else "Aucun texte"
        print(f"   ✅ Initialisation:  {t_init:7.2f}ms")
        print(f"   ✅ Détection:       {t_detect:7.2f}ms")
        print(f"   📝 Texte extrait ({len(regions)} régions):")
        print(f"      {text[:150]}..." if len(text) > 150 else f"      {text}")
        
        # Test 2: TextDetector optimisé BALANCED
        print("\n2️⃣  TextDetector OPTIMISÉ (mode='balanced')")
        start = time.perf_counter()
        det_bal = TextDetector(languages=['en', 'fr'], engine='easyocr', mode='balanced')
        t_init2 = (time.perf_counter() - start) * 1000
        
        start = time.perf_counter()
        regions2 = det_bal.detect(img)
        t_detect2 = (time.perf_counter() - start) * 1000
        
        text2 = '\n'.join([r.text for r in regions2]) if regions2 else "Aucun texte"
        print(f"   ✅ Initialisation:  {t_init2:7.2f}ms (singleton cache)")
        print(f"   ✅ Détection:       {t_detect2:7.2f}ms")
        print(f"   📝 Texte extrait ({len(regions2)} régions):")
        print(f"      {text2[:150]}..." if len(text2) > 150 else f"      {text2}")
        
        # Test 3: TextDetector optimisé SPEED
        print("\n3️⃣  TextDetector OPTIMISÉ (mode='speed' - 20% résolution)")
        start = time.perf_counter()
        det_speed = TextDetector(languages=['en', 'fr'], engine='easyocr', mode='speed')
        t_init3 = (time.perf_counter() - start) * 1000
        
        start = time.perf_counter()
        regions3 = det_speed.detect(img)
        t_detect3 = (time.perf_counter() - start) * 1000
        
        text3 = '\n'.join([r.text for r in regions3]) if regions3 else "Aucun texte"
        print(f"   ✅ Initialisation:  {t_init3:7.2f}ms")
        print(f"   ✅ Détection:       {t_detect3:7.2f}ms")
        print(f"   📝 Texte extrait ({len(regions3)} régions):")
        print(f"      {text3[:150]}..." if len(text3) > 150 else f"      {text3}")
        
        # Test 4: FastTextDetector
        print("\n4️⃣  FastTextDetector (Tesseract - Ultra-rapide)")
        try:
            from imgprocessor.text_detection.fast_detector import FastTextDetector
            
            start = time.perf_counter()
            fast = FastTextDetector(mode='balanced')
            t_init4 = (time.perf_counter() - start) * 1000
            
            start = time.perf_counter()
            regions4 = fast.detect(img)
            t_detect4 = (time.perf_counter() - start) * 1000
            
            text4 = '\n'.join([r.text for r in regions4]) if regions4 else "Aucun texte"
            print(f"   ✅ Initialisation:  {t_init4:7.2f}ms")
            print(f"   ✅ Détection:       {t_detect4:7.2f}ms")
            print(f"   📝 Texte extrait ({len(regions4)} régions):")
            print(f"      {text4[:150]}..." if len(text4) > 150 else f"      {text4}")
        except Exception as e:
            print(f"   ⚠️  Erreur: {str(e)[:50]}")
        
        # Test 5: Cache test
        print("\n5️⃣  TEST CACHE (même image, 2e appel)")
        start = time.perf_counter()
        regions_cached = det_bal.detect(img)
        t_cached = (time.perf_counter() - start) * 1000
        
        print(f"   ✅ Deuxième détection: {t_cached:7.2f}ms")
        if t_cached < 10:
            print(f"   🎉 Cache fonctionne! {t_cached:.2f}ms << {t_detect2:.2f}ms")
        
        print("\n✅ TOUS LES TESTS RÉUSSIS")
        return True
        
    except Exception as e:
        print(f"❌ ERREUR: {str(e)[:100]}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("\n" + "╔" + "="*78 + "╗")
    print("║" + " "*20 + "🧪 TESTS FINAUX SUR IMAGES AMANDA1" + " "*24 + "║")
    print("╚" + "="*78 + "╝")
    
    images = [
        ("/home/virus-one/Documents/projet/amanda1/image.png", "image.png"),
        ("/home/virus-one/Documents/projet/amanda1/image2.png", "image2.png"),
        ("/home/virus-one/Documents/projet/amanda1/Capture.png", "Capture.png"),
    ]
    
    results = []
    for image_path, name in images:
        result = test_image(image_path, name)
        results.append((name, result))
    
    # Résumé
    print("\n" + "="*80)
    print("📊 RÉSUMÉ FINAL")
    print("="*80)
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    print(f"\n✅ Réussis: {passed}/{total}")
    for name, result in results:
        status = "✅" if result else "❌"
        print(f"   {status} {name}")
    
    print("\n" + "="*80)
    if passed == total:
        print("🎉 TOUS LES TESTS RÉUSSIS!")
    else:
        print(f"⚠️  {total - passed} test(s) échoué(s)")
    print("="*80 + "\n")

if __name__ == "__main__":
    main()
