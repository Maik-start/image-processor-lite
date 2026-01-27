📦 STRUCTURE DU PACKAGE IMGPROCESSOR
=====================================

📂 package_dev/
├── 📂 imgprocessor/                    # Package principal
│   ├── __init__.py                     # Point d'entrée principal
│   │
│   ├── 📂 config/
│   │   ├── __init__.py
│   │   └── module_config.py            # 🔧 Gestion centralisée de la configuration
│   │                                   #    - Activation/désactivation des modules
│   │                                   #    - Configuration des options
│   │                                   #    - Sauvegarde/chargement JSON
│   │
│   ├── 📂 text_detection/
│   │   ├── __init__.py
│   │   └── detector.py                 # 🔤 Détection et extraction de texte (OCR)
│   │                                   #    - Support EasyOCR et Tesseract
│   │                                   #    - Multi-langues
│   │                                   #    - Coordonnées et confiance
│   │
│   ├── 📂 shape_detection/
│   │   ├── __init__.py
│   │   └── detector.py                 # 🔷 Détection de formes géométriques
│   │                                   #    - Cercles (Hough Circle Detection)
│   │                                   #    - Rectangles
│   │                                   #    - Polygones
│   │                                   #    - Analyse de contours
│   │
│   ├── 📂 distance_measurement/
│   │   ├── __init__.py
│   │   └── measurer.py                 # 📏 Mesure de distances
│   │                                   #    - Points à points
│   │                                   #    - Contours à contours
│   │                                   #    - Points à contours
│   │                                   #    - Support multi-unités
│   │
│   └── 📂 visual_analysis/
│       ├── __init__.py
│       └── analyzer.py                 # 👁️ Analyse visuelle
│                                       #    - Luminosité (brightness)
│                                       #    - Contraste (contrast)
│                                       #    - Teinte (hue)
│                                       #    - Saturation et valeur
│                                       #    - Histogrammes
│                                       #    - Comparaison d'images
│
├── 📂 examples/
│   ├── 01_basic_usage.py               # Activation/désactivation des modules
│   ├── 02_text_detection.py            # Détection de texte
│   ├── 03_shape_detection.py           # Détection de formes
│   ├── 04_distance_measurement.py      # Mesure de distances
│   └── 05_visual_analysis.py           # Analyse visuelle
│
├── 📂 tests/
│   ├── test_config.py                  # Tests de configuration
│   └── test_processor.py               # Tests du processeur
│
├── 📂 doc/                             # Documentation
│   ├── package_dev.pdf
│   ├── structure.odt
│   └── structure.pdf
│
├── setup.py                            # Configuration de l'installation
├── requirements.txt                    # Dépendances
├── MANIFEST.in                         # Manifest pour distribution
├── pytest.ini                          # Configuration pytest
├── .gitignore                          # Fichiers à ignorer Git
├── LICENSE                             # Licence MIT
├── README.md                           # Documentation complète
├── QUICKSTART.md                       # Guide de démarrage rapide
└── CONTRIBUTING.md                     # Guide de contribution

═══════════════════════════════════════════════════════════════════════════════

✨ FONCTIONNALITÉS PRINCIPALES
═══════════════════════════════════════════════════════════════════════════════

1. 🔤 DÉTECTION DE TEXTE
   ├── Moteur: EasyOCR / Tesseract
   ├── Langues: Français, Anglais, etc.
   ├── Sorties: Texte, régions, confiance
   └── Exemple: processor.detect_text(image)

2. 🔷 DÉTECTION DE FORMES
   ├── Cercles (Hough Transform)
   ├── Rectangles (approximation contours)
   ├── Polygones (multi-côtés)
   └── Exemple: processor.detect_shapes(image)

3. 📏 MESURE DE DISTANCES
   ├── Point à Point (Euclidienne)
   ├── Contour à Contour
   ├── Point à Contour
   ├── Unités: pixels, mm, cm
   └── Exemple: processor.measure_distance((x1, y1), (x2, y2))

4. 👁️ ANALYSE VISUELLE
   ├── Luminosité (0-255)
   ├── Contraste (écart-type)
   ├── Distribution de teinte (HSV)
   ├── Histogrammes RGB/HSV
   ├── Densité de contours
   ├── Couleur dominante
   ├── Comparaison d'images
   └── Exemple: processor.analyze_visual_properties(image)

═══════════════════════════════════════════════════════════════════════════════

⚙️ CONFIGURATION MODULAIRE
═══════════════════════════════════════════════════════════════════════════════

Le package permet l'activation/désactivation INDÉPENDANTE de chaque module:

# Désactiver tous les modules
processor.config.disable_all_modules()

# Activer seulement ceux dont on a besoin
processor.config.enable_module('text_detection', True)
processor.config.enable_module('shape_detection', True)

# Configurer les options
processor.config.set_module_options('text_detection', {
    'language': ['fra', 'eng'],
    'engine': 'easyocr'
})

# Sauvegarder la configuration
processor.config.save_to_file('config.json')

# Charger une configuration
processor = ImageProcessor('config.json')

═══════════════════════════════════════════════════════════════════════════════

🚀 UTILISATION RAPIDE
═══════════════════════════════════════════════════════════════════════════════

Installation:
    pip install -r requirements.txt

Exemple basique:
    from imgprocessor import ImageProcessor
    import cv2
    
    processor = ImageProcessor()
    image = cv2.imread('mon_image.jpg')
    
    # Utiliser les modules activés
    texts = processor.detect_text(image)
    shapes = processor.detect_shapes(image)
    analysis = processor.analyze_visual_properties(image)

Tests:
    pytest

Exemples:
    python examples/01_basic_usage.py
    python examples/02_text_detection.py
    python examples/03_shape_detection.py
    python examples/04_distance_measurement.py
    python examples/05_visual_analysis.py

═══════════════════════════════════════════════════════════════════════════════

📚 DÉPENDANCES
═══════════════════════════════════════════════════════════════════════════════

Requises:
  • opencv-python (>=4.5.0)
  • numpy (>=1.19.0)

Optionnelles:
  • easyocr (>=1.6.0)        - Pour détection de texte avec EasyOCR
  • pytesseract (>=0.3.10)   - Pour détection de texte avec Tesseract
  
Développement:
  • pytest (>=7.0)
  • pytest-cov (>=3.0)
  • black (>=22.0)
  • flake8 (>=4.0)
  • mypy (>=0.950)

═══════════════════════════════════════════════════════════════════════════════

📄 PRINCIPE FONDAMENTAL
═══════════════════════════════════════════════════════════════════════════════

✅ Le package ne doit pas exécuter toutes les fonctionnalités simultanément.
✅ Chaque module doit pouvoir être activé indépendamment selon le besoin.
✅ Configuration centralisée et flexible.
✅ Performance optimisée (pas de chargement des modules inutiles).

═══════════════════════════════════════════════════════════════════════════════
