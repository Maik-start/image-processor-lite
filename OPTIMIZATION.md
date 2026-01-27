# Optimisation et Gestion de Complexité

## Vue d'ensemble

Le package `imgprocessor` inclut un système d'optimisation avancé qui adapte automatiquement le traitement des images selon:
- **Profils d'optimisation** (speed, balanced, quality)
- **Complexité détectée** (low, medium, high)
- **Paramètres dynamiques** pour chaque opération

## Profils d'Optimisation

### 1. Speed (Vitesse)

**Utilisation**: Traitement rapide prioritaire
- Redimensionnement max: 640x480
- Blur kernel: 3x3 (minimal)
- Qualité JPEG: 70%
- **Résultat**: 2.75x plus rapide que Quality

```python
processor = ImageProcessor(optimization="speed")
shapes = processor.detect_shapes(image)  # Très rapide
```

**Cas d'usage**:
- Applications temps réel
- Stream vidéo
- Analyse sur mobile/serveurs limités

### 2. Balanced (Équilibre)

**Utilisation**: Équilibre vitesse/qualité (défaut recommandé)
- Redimensionnement max: 1024x768
- Blur kernel: 5x5
- Qualité JPEG: 85%
- **Résultat**: Performance optimale pour la plupart des cas

```python
processor = ImageProcessor(optimization="balanced")  # Défaut
```

**Cas d'usage**:
- Applications générales
- Batch processing
- Archivage

### 3. Quality (Qualité)

**Utilisation**: Précision maximale
- Redimensionnement max: 1920x1440
- Blur kernel: 7x7
- Qualité JPEG: 95%
- **Résultat**: Meilleure précision, plus lent

```python
processor = ImageProcessor(optimization="quality")
```

**Cas d'usage**:
- Analyse médical/scientifique
- Archivage haute résolution
- Quand la qualité > vitesse

## Détection Automatique de Complexité

Le système détecte automatiquement la complexité de chaque image:

```python
optimizer = ImageOptimizer("balanced")
complexity = optimizer.detect_complexity(image)
# Retourne: ImageComplexity.LOW, MEDIUM ou HIGH
```

### Critères de détection

| Niveau | Variance Laplacian | Ratio Pixels Uniques | Adaptation |
|--------|-------------------|----------------------|-----------|
| **LOW** | < 100 | < 10% | Paramètres agressifs |
| **MEDIUM** | 100-500 | 10-50% | Paramètres standards |
| **HIGH** | > 500 | > 50% | Paramètres conservateurs |

### Exemples

```python
# Image simple (uniforme) → LOW
simple_image = np.ones((400, 400, 3), dtype=np.uint8) * 200

# Image modérée (quelques formes) → MEDIUM  
moderate_image = create_sample_image()  # Quelques formes + bruit

# Image complexe (beaucoup de détails) → HIGH
complex_image = photo_naturelle  # Vraie photo
```

## Paramètres Adaptatifs

Les paramètres suivants s'ajustent selon le profil ET la complexité:

| Paramètre | Speed | Balanced | Quality |
|-----------|-------|----------|---------|
| blur_kernel | 3x3 | 5x5 | 7x7 |
| canny_threshold1 | 50 | 40 | 30 |
| canny_threshold2 | 150 | 120 | 100 |
| min_contour_area | 50-100 | 75 | 50 |
| hough_dp | 1.5 | 1.0 | 1.0 |

## Utilisation

### Configuration simple

```python
from imgprocessor import ImageProcessor

# Utilisation du profil par défaut (balanced)
processor = ImageProcessor()
shapes = processor.detect_shapes(image)
```

### Optimisation contrôlée

```python
# Spécifier le profil
processor = ImageProcessor(optimization="speed")

# Activer/désactiver l'optimisation par appel
shapes = processor.detect_shapes(image, optimize=True)   # Avec optimisation
shapes = processor.detect_shapes(image, optimize=False)  # Sans optimisation
```

### Analyse de complexité

```python
from imgprocessor.optimization import ImageOptimizer

optimizer = ImageOptimizer("balanced")

# Détecter la complexité
complexity = optimizer.detect_complexity(image)
print(f"Complexité: {complexity.value}")

# Obtenir l'image prétraitée et paramètres
preprocessed, info = optimizer.preprocess_image(image)
print(f"Redimensionnement: {info['scale']:.2f}x")
print(f"Paramètres: {info['params']}")
```

## Benchmarks

### Configuration de test
- Image: 1000x800 pixels avec formes et bruit
- Opération: Détection de formes

### Résultats

```
SPEED       0.016s (baseline 1.00x)
BALANCED    0.040s (2.45x)  
QUALITY     0.045s (2.75x)

Gain de vitesse (speed vs quality): 2.75x
```

### Performance réelle

```
Avec optimisation:   0.036s (formes: 63)
Sans optimisation:   0.024s (formes: 85)
```

**Note**: L'optimisation réduit les faux positifs en lissant les contours mineurs.

## Cas d'usage pratiques

### 1. Application mobile

```python
# Priorité à la vitesse
processor = ImageProcessor(optimization="speed")
camera_frame = capture_frame()
shapes = processor.detect_shapes(camera_frame, optimize=True)
```

### 2. Analyse scientifique

```python
# Priorité à la précision
processor = ImageProcessor(optimization="quality")
scientific_image = load_hdr_image()
analysis = processor.analyze_visual_properties(scientific_image)
```

### 3. Système batch

```python
# Équilibre optimal
processor = ImageProcessor(optimization="balanced")
for image_path in batch_images:
    image = cv2.imread(image_path)
    results = processor.process_image(image_path)  # Utilise tous les modules
```

## Cache et Performance

Le système `FastImageProcessor` supporte le cache:

```python
from imgprocessor.optimization import FastImageProcessor

processor = FastImageProcessor(profile="balanced", enable_cache=True)

# Premiers appels: traitement normal + cache
result1 = processor.detect_shapes(image)

# Appels suivants sur la même image: résultat du cache
result2 = processor.detect_shapes(image)  # Plus rapide!

# Voir les stats du cache
stats = processor.get_cache_stats()
print(f"Cache: {stats['size']} entrées")

# Vider le cache si besoin
processor.clear_cache()
```

## Recommandations

| Cas d'usage | Profil | Cache | Paramètres |
|-----------|--------|-------|-----------|
| Temps réel | speed | Non | Par défaut |
| Batch standard | balanced | Oui | Par défaut |
| API produit | balanced | Oui | Adapter par profil |
| Recherche | quality | Non | Affinage manuel |

## Limitations et notes

- L'optimisation fonctionne mieux avec des images typiques
- Images très bruitées: vérifier les seuils Canny
- Images très petites: optimize=False recommandé
- Le cache augmente l'usage mémoire
