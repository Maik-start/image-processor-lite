#!/usr/bin/env python
"""
Installation et Configuration du Package image-processor-lite
"""

import os
import sys
from pathlib import Path

def print_header(text):
    """Affiche un en-tête."""
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70 + "\n")

def print_section(text):
    """Affiche une section."""
    print(f"\n📌 {text}")
    print("-" * 70)

def main():
    """Guide d'installation."""
    
    print_header("GUIDE D'INSTALLATION - image-processor-lite")
    
    print("Bienvenue dans imgprocessor!")
    print("Un package modulaire de traitement d'images.")
    
    print_section("Étape 1: Vérification des prérequis")
    print(f"Python version: {sys.version}")
    print(f"Répertoire: {os.getcwd()}")
    
    print_section("Étape 2: Installation des dépendances")
    print("""
    Option A - Installation basique:
    ┌─────────────────────────────────────┐
    │ pip install -r requirements.txt     │
    └─────────────────────────────────────┘
    
    Cette option installe:
      • opencv-python (traitement d'images)
      • numpy (calculs numériques)
      • easyocr (détection de texte)
    
    Option B - Installation complète (development):
    ┌──────────────────────────────────────────────┐
    │ pip install -e ".[dev]"                      │
    └──────────────────────────────────────────────┘
    
    Cette option inclut aussi:
      • pytest (tests)
      • pytest-cov (couverture de code)
      • black (formatage)
      • flake8 (linting)
      • mypy (type checking)
    """)
    
    print_section("Étape 3: Test de l'installation")
    print("""
    Vérifiez que l'installation s'est bien passée:
    
    ┌──────────────────────────────────────────────┐
    │ python -c "import imgprocessor; print(ok)"  │
    └──────────────────────────────────────────────┘
    """)
    
    print_section("Étape 4: Utilisation rapide")
    print("""
    Créez un fichier test.py:
    
    ╔════════════════════════════════════════════════════════════╗
    ║ import cv2                                                 ║
    ║ from imgprocessor import ImageProcessor                   ║
    ║                                                            ║
    ║ processor = ImageProcessor()                              ║
    ║ image = cv2.imread('votre_image.jpg')                    ║
    ║                                                            ║
    ║ # Utiliser les modules                                    ║
    ║ texts = processor.detect_text(image)                      ║
    ║ shapes = processor.detect_shapes(image)                   ║
    ║ analysis = processor.analyze_visual_properties(image)     ║
    ║                                                            ║
    ║ print("Traitement réussi!")                               ║
    ╚════════════════════════════════════════════════════════════╝
    
    Exécutez:
    ┌──────────────────────────┐
    │ python test.py           │
    └──────────────────────────┘
    """)
    
    print_section("Étape 5: Exemples et Tests")
    print("""
    Exécutez les exemples fournis:
    
    ┌──────────────────────────────────────────────────┐
    │ python examples/01_basic_usage.py                │
    │ python examples/02_text_detection.py             │
    │ python examples/03_shape_detection.py            │
    │ python examples/04_distance_measurement.py       │
    │ python examples/05_visual_analysis.py            │
    └──────────────────────────────────────────────────┘
    
    Lancez les tests:
    ┌──────────────────────────────────────────────────┐
    │ pytest tests/ -v                                 │
    └──────────────────────────────────────────────────┘
    """)
    
    print_section("Étape 6: Configuration personnalisée")
    print("""
    Exemple de configuration personnalisée:
    
    ╔════════════════════════════════════════════════════════════╗
    ║ from imgprocessor import ImageProcessor                   ║
    ║                                                            ║
    ║ processor = ImageProcessor()                              ║
    ║                                                            ║
    ║ # Désactiver les modules inutiles                         ║
    ║ processor.config.disable_all_modules()                    ║
    ║ processor.config.enable_module('text_detection', True)    ║
    ║ processor.config.enable_module('shape_detection', True)   ║
    ║                                                            ║
    ║ # Configurer les options                                  ║
    ║ processor.config.set_module_options('text_detection', {   ║
    ║     'language': ['fra'],                                  ║
    ║     'engine': 'easyocr'                                   ║
    ║ })                                                         ║
    ║                                                            ║
    ║ # Sauvegarder la configuration                            ║
    ║ processor.config.save_to_file('my_config.json')           ║
    ╚════════════════════════════════════════════════════════════╝
    """)
    
    print_section("Documentation")
    print("""
    📖 README.md - Documentation complète
    🚀 QUICKSTART.md - Démarrage rapide
    📊 STRUCTURE.md - Architecture détaillée
    🤝 CONTRIBUTING.md - Guide de contribution
    ✅ SUMMARY.md - Synthèse du projet
    """)
    
    print_section("Dépannage courants")
    print("""
    ❌ ImportError: No module named 'easyocr'
       → pip install easyocr
    
    ❌ ImportError: No module named 'cv2'
       → pip install opencv-python
    
    ❌ ImportError: No module named 'imgprocessor'
       → pip install -e .  (dans le répertoire du package)
    
    ❌ "Tesseract is not installed"
       → Installez Tesseract séparément:
         • Windows: https://github.com/UB-Mannheim/tesseract/wiki
         • Linux: sudo apt-get install tesseract-ocr
         • macOS: brew install tesseract
    """)
    
    print_section("Support")
    print("""
    Pour toute question ou problème:
    
    1. Consultez la documentation (README.md)
    2. Vérifiez les exemples (examples/)
    3. Lancez les tests (pytest)
    4. Lisez les issues existantes
    5. Ouvrez une nouvelle issue si nécessaire
    """)
    
    print_header("Installation terminée! 🎉")
    print("""
    Prochaines étapes:
    
    1. Lire QUICKSTART.md pour un premier contact
    2. Essayer les exemples (examples/)
    3. Consulter README.md pour la documentation complète
    4. Adapter la configuration selon vos besoins
    
    Bon traitement d'images! 🚀
    """)

if __name__ == "__main__":
    main()
