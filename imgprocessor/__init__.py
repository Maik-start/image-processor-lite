"""
imgprocessor - Package modulaire de traitement et d'analyse d'images.

Un package permettant d'effectuer indépendamment les opérations suivantes:
- Détection et extraction de texte (OCR)
- Détection de formes géométriques
- Mesure de distances entre objets
- Analyse visuelle (luminosité, contraste, teinte)

Chaque module peut être activé/désactivé indépendamment selon les besoins.
"""

import cv2
import numpy as np
from typing import Optional, Dict, List
from pathlib import Path

from .config import ImageProcessorConfig
from .text_detection import TextDetector, TextRegion
from .shape_detection import ShapeDetector, Shape
from .distance_measurement import DistanceMeasurer, Distance
from .visual_analysis import VisualAnalyzer, VisualAnalysis

__version__ = "1.0.0"
__author__ = "ImageProcessor Team"


class ImageProcessor:
    """
    Gestionnaire central pour le traitement modulaire d'images.
    
    Permet d'utiliser indépendamment chaque module selon les besoins.
    
    Exemple:
        >>> processor = ImageProcessor()
        >>> 
        >>> # Désactiver certains modules
        >>> processor.config.enable_module('text_detection', True)
        >>> processor.config.enable_module('distance_measurement', False)
        >>> 
        >>> # Charger une image
        >>> image = cv2.imread('image.jpg')
        >>> 
        >>> # Utiliser les modules activés
        >>> if processor.config.is_module_enabled('text_detection'):
        >>>     texts = processor.detect_text(image)
        >>> 
        >>> if processor.config.is_module_enabled('shape_detection'):
        >>>     shapes = processor.detect_shapes(image)
    """
    
    def __init__(self, config_file: Optional[str] = None):
        """
        Initialise le processeur d'images.
        
        Args:
            config_file: Chemin optionnel vers un fichier de configuration JSON
        """
        self.config = ImageProcessorConfig(config_file)
        
        # Initialiser les modules selon la configuration
        self._init_modules()
    
    def _init_modules(self) -> None:
        """Initialise les modules selon la configuration."""
        # Text Detection
        if self.config.is_module_enabled('text_detection'):
            try:
                options = self.config.get_module_options('text_detection')
                self.text_detector = TextDetector(
                    languages=options.get('language', ['fra', 'eng']),
                    engine=options.get('engine', 'easyocr')
                )
            except Exception as e:
                print(f"Avertissement: Module texte non initialisé - {e}")
                self.text_detector = None
        else:
            self.text_detector = None
        
        # Shape Detection
        if self.config.is_module_enabled('shape_detection'):
            options = self.config.get_module_options('shape_detection')
            self.shape_detector = ShapeDetector(
                min_contour_area=options.get('min_contour_area', 50),
                detect_circles=options.get('detect_circles', True),
                detect_rectangles=options.get('detect_rectangles', True),
                detect_polygons=options.get('detect_polygons', True)
            )
        else:
            self.shape_detector = None
        
        # Distance Measurement
        if self.config.is_module_enabled('distance_measurement'):
            options = self.config.get_module_options('distance_measurement')
            self.distance_measurer = DistanceMeasurer(
                unit=options.get('unit', 'pixels'),
                precision=options.get('precision', 2)
            )
        else:
            self.distance_measurer = None
        
        # Visual Analysis
        if self.config.is_module_enabled('visual_analysis'):
            options = self.config.get_module_options('visual_analysis')
            self.visual_analyzer = VisualAnalyzer(
                analyze_brightness=options.get('analyze_brightness', True),
                analyze_contrast=options.get('analyze_contrast', True),
                analyze_hue=options.get('analyze_hue', True),
                bins=options.get('bins', 256)
            )
        else:
            self.visual_analyzer = None
    
    def detect_text(self, image: np.ndarray, min_confidence: float = 0.5) -> Optional[List[TextRegion]]:
        """
        Détecte le texte dans l'image.
        
        Args:
            image: Image en format numpy array
            min_confidence: Seuil de confiance minimum
        
        Returns:
            Liste des régions de texte ou None si module désactivé
        """
        if not self.config.is_module_enabled('text_detection') or self.text_detector is None:
            return None
        return self.text_detector.detect(image, min_confidence)
    
    def extract_text(self, image: np.ndarray, min_confidence: float = 0.5) -> Optional[str]:
        """
        Extrait tout le texte d'une image.
        
        Args:
            image: Image en format numpy array
            min_confidence: Seuil de confiance minimum
        
        Returns:
            Texte extrait ou None si module désactivé
        """
        if not self.config.is_module_enabled('text_detection') or self.text_detector is None:
            return None
        return self.text_detector.extract_text(image, min_confidence)
    
    def detect_shapes(self, image: np.ndarray) -> Optional[List[Shape]]:
        """
        Détecte les formes géométriques.
        
        Args:
            image: Image en format numpy array
        
        Returns:
            Liste des formes détectées ou None si module désactivé
        """
        if not self.config.is_module_enabled('shape_detection') or self.shape_detector is None:
            return None
        return self.shape_detector.detect_shapes(image)
    
    def detect_circles(self, image: np.ndarray) -> Optional[List[Shape]]:
        """Détecte les cercles."""
        if not self.config.is_module_enabled('shape_detection') or self.shape_detector is None:
            return None
        return self.shape_detector.detect_circles(image)
    
    def detect_rectangles(self, image: np.ndarray) -> Optional[List[Shape]]:
        """Détecte les rectangles."""
        if not self.config.is_module_enabled('shape_detection') or self.shape_detector is None:
            return None
        return self.shape_detector.detect_rectangles(image)
    
    def measure_distance(self, point1: tuple, point2: tuple) -> Optional[Distance]:
        """
        Mesure la distance entre deux points.
        
        Args:
            point1: Coordonnées du premier point
            point2: Coordonnées du deuxième point
        
        Returns:
            Objet Distance ou None si module désactivé
        """
        if not self.config.is_module_enabled('distance_measurement') or self.distance_measurer is None:
            return None
        return self.distance_measurer.euclidean_distance(point1, point2)
    
    def analyze_visual_properties(self, image: np.ndarray) -> Optional[VisualAnalysis]:
        """
        Analyse les propriétés visuelles de l'image.
        
        Args:
            image: Image en format numpy array
        
        Returns:
            Objet VisualAnalysis ou None si module désactivé
        """
        if not self.config.is_module_enabled('visual_analysis') or self.visual_analyzer is None:
            return None
        return self.visual_analyzer.analyze(image)
    
    def process_image(self, image_path: str) -> Dict:
        """
        Traite une image avec tous les modules activés.
        
        Args:
            image_path: Chemin vers l'image
        
        Returns:
            Dictionnaire avec les résultats de tous les modules
        """
        image = cv2.imread(image_path)
        if image is None:
            raise FileNotFoundError(f"Image non trouvée: {image_path}")
        
        results = {}
        
        # Texte
        if self.config.is_module_enabled('text_detection') and self.text_detector:
            results['text'] = [r.to_dict() for r in self.detect_text(image) or []]
        
        # Formes
        if self.config.is_module_enabled('shape_detection') and self.shape_detector:
            results['shapes'] = [s.to_dict() for s in self.detect_shapes(image) or []]
        
        # Analyse visuelle
        if self.config.is_module_enabled('visual_analysis') and self.visual_analyzer:
            analysis = self.analyze_visual_properties(image)
            if analysis:
                results['visual_analysis'] = analysis.to_dict()
        
        return results
    
    def get_status(self) -> Dict:
        """Retourne le statut de tous les modules."""
        return self.config.get_status()
    
    def __repr__(self) -> str:
        status = {name: config.enabled for name, config in self.config.modules.items()}
        return f"ImageProcessor(modules={status})"


__all__ = [
    'ImageProcessor',
    'ImageProcessorConfig',
    'TextDetector',
    'ShapeDetector',
    'DistanceMeasurer',
    'VisualAnalyzer',
    'TextRegion',
    'Shape',
    'Distance',
    'VisualAnalysis'
]
