#!/usr/bin/env python3
"""
Tests pour le module VisualAnalyzer.
Valide les fonctionnalités d'analyse visuelle et de détection d'objets.
"""

import cv2
import numpy as np
from imgprocessor.visual_analysis import VisualAnalyzer, VisualAnalysis, VisualObject


def create_test_image_with_objects():
    """Crée une image de test avec des objets visuels distincts."""
    image = np.ones((480, 640, 3), dtype=np.uint8) * 200  # Fond gris clair
    
    # Objet 1: Cercle bleu (géométrique)
    cv2.circle(image, (150, 150), 80, (255, 100, 0), -1)
    
    # Objet 2: Rectangle rouge (géométrique)
    cv2.rectangle(image, (350, 100), (500, 250), (0, 0, 255), -1)
    
    # Objet 3: Zone verte (naturelle)
    pts = np.array([[100, 350], [250, 300], [280, 400], [200, 450]], np.int32)
    cv2.fillPoly(image, [pts], (0, 200, 0))
    
    return image


class TestVisualAnalyzer:
    """Tests pour VisualAnalyzer."""
    
    def test_initialization(self):
        """Test l'initialisation de l'analyseur."""
        analyzer = VisualAnalyzer(
            analyze_brightness=True,
            analyze_contrast=True,
            analyze_hue=True,
            detect_objects=True,
            bins=256,
            min_object_size=100
        )
        
        assert analyzer.analyze_brightness == True
        assert analyzer.analyze_contrast == True
        assert analyzer.analyze_hue == True
        assert analyzer.detect_objects == True
        assert analyzer.bins == 256
        assert analyzer.min_object_size == 100
        print("✅ Test 1: Initialisation OK")
    
    def test_basic_analysis(self):
        """Test l'analyse visuelle basique."""
        image = create_test_image_with_objects()
        analyzer = VisualAnalyzer(
            analyze_brightness=True,
            analyze_contrast=True,
            analyze_hue=True,
            detect_objects=False  # Pas de détection pour ce test
        )
        
        analysis = analyzer.analyze(image)
        
        assert isinstance(analysis, VisualAnalysis)
        assert 0 <= analysis.brightness <= 255
        assert analysis.contrast >= 0
        assert len(analysis.hue_distribution) > 0
        assert 0 <= analysis.saturation <= 255
        assert 0 <= analysis.value <= 255
        assert isinstance(analysis.color_histogram, dict)
        assert analysis.edge_density >= 0
        
        print("✅ Test 2: Analyse basique OK")
        print(f"   Luminosité: {analysis.brightness:.2f}")
        print(f"   Contraste: {analysis.contrast:.2f}")
        print(f"   Densité contours: {analysis.edge_density:.4f}")
    
    def test_object_detection(self):
        """Test la détection d'objets visuels."""
        image = create_test_image_with_objects()
        analyzer = VisualAnalyzer(
            detect_objects=True,
            min_object_size=50
        )
        
        analysis = analyzer.analyze(image)
        
        assert isinstance(analysis.objects, list)
        assert len(analysis.objects) > 0  # Devrait détecter les 3 objets
        assert analysis.object_density >= 0
        
        print(f"✅ Test 3: Détection d'objets OK")
        print(f"   Objets détectés: {len(analysis.objects)}")
        print(f"   Densité d'objets: {analysis.object_density:.2f}")
        
        # Analyser chaque objet
        for i, obj in enumerate(analysis.objects):
            print(f"\n   Objet {i+1}:")
            print(f"     - Label: {obj.label}")
            print(f"     - Area: {obj.area}")
            print(f"     - Couleur dominante: {obj.dominant_color}")
            print(f"     - Stabilité chromatique: {obj.chromatic_stability:.3f}")
            print(f"     - Régularité contour: {obj.contour_regularity:.3f}")
            print(f"     - Solidité: {obj.solidity:.3f}")
    
    def test_visual_object_properties(self):
        """Test les propriétés d'un objet visuel."""
        image = create_test_image_with_objects()
        analyzer = VisualAnalyzer(detect_objects=True, min_object_size=50)
        
        analysis = analyzer.analyze(image)
        
        if len(analysis.objects) > 0:
            obj = analysis.objects[0]
            
            # Vérifier les propriétés
            assert obj.object_id >= 0
            assert obj.label in ['geometric', 'artificial', 'natural', 'abstract', 'unknown']
            assert obj.area > 0
            assert obj.perimeter > 0
            assert len(obj.centroid) == 2
            assert len(obj.bounding_box) == 4
            assert len(obj.dominant_color) == 3
            assert 0 <= obj.mean_brightness <= 255
            assert 0 <= obj.chromatic_stability <= 1
            assert 0 <= obj.contour_regularity <= 1
            assert 0 <= obj.solidity <= 1
            assert obj.aspect_ratio > 0
            
            print("✅ Test 4: Propriétés des objets OK")
    
    def test_to_dict(self):
        """Test la conversion en dictionnaire."""
        image = create_test_image_with_objects()
        analyzer = VisualAnalyzer(detect_objects=True)
        
        analysis = analyzer.analyze(image)
        analysis_dict = analysis.to_dict()
        
        assert isinstance(analysis_dict, dict)
        assert 'brightness' in analysis_dict
        assert 'contrast' in analysis_dict
        assert 'objects' in analysis_dict
        assert isinstance(analysis_dict['objects'], list)
        
        if len(analysis_dict['objects']) > 0:
            obj_dict = analysis_dict['objects'][0]
            assert 'label' in obj_dict
            assert 'area' in obj_dict
            assert 'chromatic_stability' in obj_dict
        
        print("✅ Test 5: Conversion en dictionnaire OK")
    
    def test_brightness_analysis(self):
        """Test l'analyse de luminosité."""
        # Image sombre
        dark_image = np.zeros((100, 100, 3), dtype=np.uint8)
        # Image claire
        bright_image = np.ones((100, 100, 3), dtype=np.uint8) * 255
        
        analyzer = VisualAnalyzer(analyze_brightness=True)
        
        dark_analysis = analyzer.analyze(dark_image)
        bright_analysis = analyzer.analyze(bright_image)
        
        assert dark_analysis.brightness < bright_analysis.brightness
        
        print("✅ Test 6: Analyse de luminosité OK")
        print(f"   Image sombre: {dark_analysis.brightness:.2f}")
        print(f"   Image claire: {bright_analysis.brightness:.2f}")
    
    def test_contrast_analysis(self):
        """Test l'analyse du contraste."""
        # Image uniforme (peu de contraste)
        uniform_image = np.ones((100, 100, 3), dtype=np.uint8) * 128
        # Image avec variation (contraste)
        contrast_image = np.zeros((100, 100, 3), dtype=np.uint8)
        contrast_image[:50, :] = 255
        
        analyzer = VisualAnalyzer(analyze_contrast=True)
        
        uniform_analysis = analyzer.analyze(uniform_image)
        contrast_analysis = analyzer.analyze(contrast_image)
        
        assert uniform_analysis.contrast < contrast_analysis.contrast
        
        print("✅ Test 7: Analyse du contraste OK")
        print(f"   Image uniforme: {uniform_analysis.contrast:.2f}")
        print(f"   Image contrastée: {contrast_analysis.contrast:.2f}")
    
    def test_color_histogram(self):
        """Test l'histogramme des couleurs."""
        image = create_test_image_with_objects()
        analyzer = VisualAnalyzer(analyze_hue=True)
        
        analysis = analyzer.analyze(image)
        
        assert len(analysis.hue_distribution) == 7  # 7 catégories de couleur
        assert 'red' in analysis.hue_distribution
        assert 'green' in analysis.hue_distribution
        assert 'blue' in analysis.hue_distribution
        
        # Vérifier que les valeurs sont en pourcentage
        total_hue = sum(analysis.hue_distribution.values())
        assert 90 < total_hue <= 110  # Avec une marge pour arrondi
        
        print("✅ Test 8: Histogramme des couleurs OK")
        print(f"   Distribution de teinte:")
        for color, percentage in analysis.hue_distribution.items():
            print(f"     - {color}: {percentage:.2f}%")
    
    def test_disabled_modules(self):
        """Test les modules désactivés."""
        image = create_test_image_with_objects()
        analyzer = VisualAnalyzer(
            analyze_brightness=False,
            analyze_contrast=False,
            analyze_hue=False,
            detect_objects=False
        )
        
        analysis = analyzer.analyze(image)
        
        assert analysis.brightness == 0.0
        assert analysis.contrast == 0.0
        assert len(analysis.hue_distribution) == 0
        assert len(analysis.objects) == 0
        
        print("✅ Test 9: Modules désactivés OK")


def main():
    """Exécute tous les tests."""
    print("\n" + "="*70)
    print("🧪 TESTS DU MODULE VisualAnalyzer")
    print("="*70 + "\n")
    
    test_suite = TestVisualAnalyzer()
    
    try:
        test_suite.test_initialization()
        test_suite.test_basic_analysis()
        test_suite.test_object_detection()
        test_suite.test_visual_object_properties()
        test_suite.test_to_dict()
        test_suite.test_brightness_analysis()
        test_suite.test_contrast_analysis()
        test_suite.test_color_histogram()
        test_suite.test_disabled_modules()
        
        print("\n" + "="*70)
        print("✅ TOUS LES TESTS RÉUSSIS!")
        print("="*70)
        print("\n📊 Résumé:")
        print("   ✅ 9/9 tests passants")
        print("   ✅ Analyse visuelle fonctionnelle")
        print("   ✅ Détection d'objets validée")
        print("   ✅ Classification d'objets OK")
        print("   ✅ Conversion en dictionnaire OK")
        print("\n")
        
    except Exception as e:
        print(f"\n❌ ERREUR: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
