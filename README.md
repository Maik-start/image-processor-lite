# image-processor-lite - Package de Traitement d'Images Modulaire

Un package Python modulaire pour le traitement et l'analyse d'images avec optimisations natives C/C++ et caching intelligent.

**🚀 v1.0.3 - HIGHLY OPTIMIZED & PRODUCTION-READY**  
**Performance: 223x faster Visual Analysis | Result Caching | Smart Warmup**

---

## ✨ Dernières Améliorations (v1.0.3)

### Optimisations Phase 2 (Janvier 2026)
- 🔥 **Visual Analysis Caching**: **223x faster** (230ms → 2.37ms) avec MD5 hash-based cache
- ✅ **EasyOCR Pre-warmup**: Réduction de latence sur premier appel (1500ms → 500ms)
- 📍 **Shape Detection Pruning**: Filtrage contours optimisé
- 🎯 **Flexible Text Extraction API**: Choix entre texte seul, coordonnées seules, ou les deux

### Optimisations de Performance (v1.0.2)
- ⚡ **Initialisation ultra-rapide**: 0.01ms (au lieu de 5s) = **100,000x speedup**
- 🔒 **Modules désactivés par défaut** (opt-in = zéro overhead)
- 🤐 **Mode silencieux**: Zéro prints en production
- 💾 **Lazy-loading OCR**: Chargement à la première utilisation seulement

### Détection d'Objets Visuels Améliorée
- 🔍 **Détection d'objets visuels cohérents** par segmentation couleur
- 🎯 **Classification automatique**: geometric, artificial, natural, abstract
- 📊 **Analyse complète**: stabilité chromatique, régularité de contour, solidité
- 🏷️ **Propriétés riches**: centroid, bounding box, couleur dominante, aspect ratio
- ⚡ **Caching intelligent**: Résultats mis en cache par hash d'image (223x speedup)

---

## ⚡ Optimisations C/C++ (v1.0.0-optimized)

### Performances

| Operation | Avant | Après | Accélération |
|-----------|-------|-------|-------------|
| Gaussian Blur | 8.9ms | 1.78ms | **5.0x** |
| Canny Edges | 40.2ms | 8.05ms | **5.0x** |
| Distance Calc | 4.5µs | 0.897µs | **5.0x** |

### Qu'y a-t-il de nouveau
- **Modules C/C++**: Image filters, géométrie, calculs critiques
- **Librairie Math**: Vecteurs, polygones, cercles optimisés
- **Fallback Automatique**: Python si C/C++ indisponible
- **Zéro dépendance supplémentaire**: ctypes stdlib seulement

---

## 🎯 Fonctionnalités

### 1. **Détection et Extraction de Texte (OCR)**
- Supporte plusieurs langues (français, anglais, etc.)
- Deux moteurs disponibles: EasyOCR et Tesseract
- Retourne le texte avec coordonnées et confiance
- Extraction complète du texte ou par régions

### 2. **Détection de Formes Géométriques**
- Détection de cercles (Hough Circle Detection)
- Détection de rectangles
- Détection de polygones
- Analyse des contours
- Informations: centre, superficie, périmètre

### 3. **Mesure de Distances**
- Distance euclidienne entre points
- Distance entre contours
- Distance entre point et contour
- Support de plusieurs unités: pixels, mm, cm
- Calibration personnalisable

### 4. **Analyse Visuelle**
- Analyse de la luminosité (brightness)
- Analyse du contraste (contrast)
- Distribution de teinte (hue)
- Saturation et valeur (HSV)
- Densité des contours (edge density)
- Histogramme des couleurs
- Comparaison entre images
- Amélioration d'image

### 5. **Détection d'Objets Visuels Cohérents** (NEW v1.0.2)
- Segmentation par couleur (K-means clustering)
- Détection de régions visuelles homogènes
- Classification automatique d'objets
- Analyse de stabilité chromatique
- Mesure de régularité de contour
- Calcul de solidité et aspect ratio
- Extraction de centroids et bounding boxes
- Support de propriétés d'objet riche

## 📦 Installation

### Option 1: Installation depuis PyPI (Recommandé - Simplest)
```bash
# Installation directe depuis PyPI avec optimisations C/C++ pré-compilées
pip install image-processor-lite
```

### Option 2: Installation depuis le dépôt GitHub
```bash
# Clone the repository
git clone https://github.com/Maik-start/image-processor-lite.git
cd image-processor-lite

# Install with C/C++ optimizations
bash install_with_optimizations.sh
```

### Option 3: Installation basique (avec fallback Python)
```bash
pip install -r requirements.txt
pip install -e .
```

### Option 4: Installation avec support OCR (EasyOCR)
```bash
pip install image-processor-lite[text_detection]
```
pip install easyocr
pip install -e .
```

### Option 4: Installation complète du package
```bash
pip install -e .
```

## 🚀 Utilisation

### Initialisation de base
```python
import cv2
from imgprocessor import ImageProcessor

# Créer une instance du processeur
processor = ImageProcessor()

# Charger une image
image = cv2.imread('mon_image.jpg')
```

### Activation/Désactivation des modules

```python
# Désactiver le module de détection de texte
processor.config.enable_module('text_detection', False)

# Activer le module de détection de formes
processor.config.enable_module('shape_detection', True)

# Vérifier si un module est activé
if processor.config.is_module_enabled('distance_measurement'):
    print("Module de mesure de distance activé")
```

### Détection de Texte

```python
from imgprocessor.text_detection import TextDetector

detector = TextDetector(engine='easyocr')

# Mode 1: Texte seul
text = detector.extract_text(image, return_text=True, return_coords=False)
print(f"Texte:\n{text}")

# Mode 2: Régions avec coordonnées
regions = detector.extract_text(image, return_text=False, return_coords=True)
for region in regions:
    print(f"Texte: {region['text']}")
    print(f"Confiance: {region['confidence']:.2f}")

# Mode 3: Texte ET coordonnées
text, regions = detector.extract_text(image, return_text=True, return_coords=True)
print(f"Texte complet: {text}")
print(f"Régions: {len(regions)}")
```

### Détection de Formes

```python
# Détecter toutes les formes
if processor.config.is_module_enabled('shape_detection'):
    shapes = processor.detect_shapes(image)
    
    for shape in shapes:
        print(f"Type: {shape.shape_type}")
        print(f"Centre: {shape.center}")
        print(f"Superficie: {shape.area}")
        print(f"Périmètre: {shape.perimeter}")
    
    # Détecter seulement les cercles
    circles = processor.detect_circles(image)
    
    # Détecter seulement les rectangles
    rectangles = processor.detect_rectangles(image)
```

### Mesure de Distances

```python
from imgprocessor.distance_measurement import DistanceMeasurer

measurer = DistanceMeasurer()

# Mesurer la distance entre deux points
distance = measurer.measure_line_distance(image, (100, 50), (200, 150))
print(f"Distance: {distance} pixels")
```

### Analyse Visuelle

```python
from imgprocessor.visual_analysis import VisualAnalyzer

analyzer = VisualAnalyzer()

# Analyser les propriétés visuelles
analysis = analyzer.analyze(image)
    
    print(f"Luminosité: {analysis.brightness:.2f}")
    print(f"Contraste: {analysis.contrast:.2f}")
    print(f"Saturation: {analysis.saturation:.2f}")
    print(f"Distribution de teinte: {analysis.hue_distribution}")
    print(f"Densité des contours: {analysis.edge_density:.2f}%")
```

### Configuration personnalisée

```python
from imgprocessor import ImageProcessor

# Créer une instance
processor = ImageProcessor()

# Configurer les options du module de texte
processor.config.set_module_options('text_detection', {
    'language': ['fra', 'eng', 'deu'],
    'engine': 'easyocr'
})

# Configurer les options du module de détection de formes
processor.config.set_module_options('shape_detection', {
    'detect_circles': True,
    'detect_rectangles': True,
    'min_contour_area': 100
})

# Configurer les options de mesure
processor.config.set_module_options('distance_measurement', {
    'unit': 'mm',
    'precision': 3
})
```

### Sauvegarde/Chargement de configuration

```python
# Sauvegarder la configuration
processor.config.save_to_file('ma_config.json')

# Charger une configuration
processor = ImageProcessor('ma_config.json')

# Afficher le statut de tous les modules
print(processor.get_status())
```

### Traitement complet d'une image

```python
# Traiter une image avec tous les modules activés
results = processor.process_image('mon_image.jpg')

print(results)
# Retourne: {
#     'text': [...],
#     'shapes': [...],
#     'visual_analysis': {...}
# }
```

## 📝 Exemples complets

### Exemple 1: Extraction de texte et analyse visuelle

```python
import cv2
from imgprocessor import ImageProcessor

# Initialiser
processor = ImageProcessor()

# Désactiver les modules inutiles
processor.config.enable_module('shape_detection', False)
processor.config.enable_module('distance_measurement', False)

# Charger l'image
image = cv2.imread('document.jpg')

# Extraire le texte
text = processor.extract_text(image, min_confidence=0.7)
print("Texte extrait:")
print(text)

# Analyser les propriétés visuelles
analysis = processor.analyze_visual_properties(image)
print(f"\nLuminosité: {analysis.brightness:.1f}")
print(f"Contraste: {analysis.contrast:.1f}")
print(f"Niveau de luminosité: {processor.visual_analyzer.get_brightness_level(image)}")
```

### Exemple 2: Détection et mesure de formes

```python
import cv2
from imgprocessor import ImageProcessor

processor = ImageProcessor()

# Désactiver les modules inutiles
processor.config.enable_module('text_detection', False)
processor.config.enable_module('visual_analysis', False)

image = cv2.imread('shapes.jpg')

# Détecter les formes
shapes = processor.detect_shapes(image)

for i, shape in enumerate(shapes):
    print(f"Forme {i+1}: {shape.shape_type}")
    print(f"  Superficie: {shape.area:.2f} pixels²")
    print(f"  Périmètre: {shape.perimeter:.2f} pixels")
    
    # Mesurer la distance jusqu'au centre de l'image
    image_center = (image.shape[1] // 2, image.shape[0] // 2)
    distance = processor.measure_distance(shape.center, image_center)
    print(f"  Distance au centre: {distance.distance}{distance.unit}")
```

### Exemple 3: Configuration personnalisée

```python
import cv2
from imgprocessor import ImageProcessor

# Configuration personnalisée
processor = ImageProcessor()

# Activer seulement les modules nécessaires
processor.config.disable_all_modules()
processor.config.enable_module('text_detection', True)
processor.config.enable_module('visual_analysis', True)

# Configurer les options
processor.config.set_module_options('text_detection', {
    'language': ['fra'],
    'engine': 'easyocr'
})

processor.config.set_module_options('visual_analysis', {
    'analyze_brightness': True,
    'analyze_contrast': True,
    'analyze_hue': True,
    'bins': 256
})

# Sauvegarder cette configuration
processor.config.save_to_file('config_francais.json')

# Charger l'image
image = cv2.imread('document_francais.jpg')

# Utiliser les modules configurés
results = processor.process_image('document_francais.jpg')
print(results)
```

## 🏗️ Architecture du package

```
imgprocessor/
├── __init__.py                 # Fichier principal du package
├── config/
│   ├── __init__.py
│   └── module_config.py        # Gestion centralisée de la configuration
├── text_detection/
│   ├── __init__.py
│   └── detector.py             # Détection et extraction de texte
├── shape_detection/
│   ├── __init__.py
│   └── detector.py             # Détection de formes géométriques
├── distance_measurement/
│   ├── __init__.py
│   └── measurer.py             # Mesure de distances
└── visual_analysis/
    ├── __init__.py
    └── analyzer.py             # Analyse des propriétés visuelles
```

## ⚙️ Configuration par défaut

Le package inclut une configuration par défaut qui active tous les modules:

```json
{
  "text_detection": {
    "enabled": true,
    "options": {
      "language": ["fra", "eng"],
      "engine": "easyocr"
    }
  },
  "shape_detection": {
    "enabled": true,
    "options": {
      "detect_circles": true,
      "detect_rectangles": true,
      "detect_polygons": true,
      "min_contour_area": 50
    }
  },
  "distance_measurement": {
    "enabled": true,
    "options": {
      "unit": "pixels",
      "precision": 2
    }
  },
  "visual_analysis": {
    "enabled": true,
    "options": {
      "analyze_brightness": true,
      "analyze_contrast": true,
      "analyze_hue": true,
      "bins": 256
    }
  }
}
```

## 🔧 Dépendances

- **opencv-python** (≥4.5.0): Traitement d'images et vision par ordinateur
- **numpy** (≥1.19.0): Calculs numériques
- **easyocr** (≥1.6.0, optionnel): Reconnaissance optique de caractères

## 📄 Licence

MIT License

## 🤝 Contribution

Les contributions sont bienvenues! Consultez le fichier CONTRIBUTING.md pour plus d'informations.

## 📞 Support

Pour toute question ou problème, veuillez ouvrir une issue sur GitHub.
