# Démarrage Rapide - imgprocessor

## Installation

```bash
# Installation basique
pip install -r requirements.txt

# Ou installation complète
pip install -e .
```

## Utilisation Minimale

```python
from imgprocessor import ImageProcessor
import cv2

# Créer une instance
processor = ImageProcessor()

# Charger une image
image = cv2.imread('mon_image.jpg')

# 1. Détecter du texte
texts = processor.detect_text(image)

# 2. Détecter des formes
shapes = processor.detect_shapes(image)

# 3. Mesurer des distances
distance = processor.measure_distance((100, 50), (200, 150))

# 4. Analyser les propriétés visuelles
analysis = processor.analyze_visual_properties(image)
```

## Configuration Personnalisée

```python
# Activer seulement certains modules
processor.config.disable_all_modules()
processor.config.enable_module('text_detection', True)
processor.config.enable_module('shape_detection', True)

# Configurer les options
processor.config.set_module_options('text_detection', {
    'language': ['fra', 'eng'],
    'engine': 'easyocr'
})

# Sauvegarder/charger la configuration
processor.config.save_to_file('ma_config.json')
processor2 = ImageProcessor('ma_config.json')
```

## Exécuter les Exemples

```bash
# Exemple 1: Utilisation basique
python examples/01_basic_usage.py

# Exemple 2: Détection de texte
python examples/02_text_detection.py

# Exemple 3: Détection de formes
python examples/03_shape_detection.py

# Exemple 4: Mesure de distances
python examples/04_distance_measurement.py

# Exemple 5: Analyse visuelle
python examples/05_visual_analysis.py
```

## Documentation Complète

Voir [README.md](README.md) pour la documentation détaillée.

## Tests

```bash
# Installer les dépendances de test
pip install pytest pytest-cov

# Exécuter les tests
pytest

# Avec couverture
pytest --cov=imgprocessor
```

## Architecture

- **config/** - Gestion centralisée de la configuration
- **text_detection/** - Module OCR
- **shape_detection/** - Détection de formes géométriques
- **distance_measurement/** - Mesure de distances
- **visual_analysis/** - Analyse visuelle (luminosité, contraste, teinte)

Chaque module peut être activé/désactivé indépendamment!

## Besoin d'aide?

1. Consultez le [README.md](README.md)
2. Explorez les [exemples](examples/)
3. Lisez les [tests](tests/) pour des cas d'usage

---

Bon traitement d'images! 🎉
