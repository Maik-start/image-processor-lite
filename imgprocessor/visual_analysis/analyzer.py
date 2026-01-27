"""
Module d'analyse visuelle des images.
Analyse la luminosité, le contraste, la teinte et autres propriétés visuelles.
"""

import cv2
import numpy as np
from typing import Dict, Tuple, List
from dataclasses import dataclass


@dataclass
class VisualAnalysis:
    """Résultats de l'analyse visuelle."""
    brightness: float = 0.0
    contrast: float = 0.0
    hue_distribution: Dict = None
    saturation: float = 0.0
    value: float = 0.0
    color_histogram: Dict = None
    edge_density: float = 0.0
    
    def __post_init__(self):
        if self.hue_distribution is None:
            self.hue_distribution = {}
        if self.color_histogram is None:
            self.color_histogram = {}
    
    def to_dict(self) -> Dict:
        """Convertit en dictionnaire."""
        return {
            'brightness': float(self.brightness),
            'contrast': float(self.contrast),
            'hue_distribution': self.hue_distribution,
            'saturation': float(self.saturation),
            'value': float(self.value),
            'color_histogram': self.color_histogram,
            'edge_density': float(self.edge_density)
        }


class VisualAnalyzer:
    """
    Analyste des propriétés visuelles des images.
    """
    
    def __init__(self, 
                 analyze_brightness: bool = True,
                 analyze_contrast: bool = True,
                 analyze_hue: bool = True,
                 bins: int = 256):
        """
        Initialise l'analyseur visuel.
        
        Args:
            analyze_brightness: Analyser la luminosité
            analyze_contrast: Analyser le contraste
            analyze_hue: Analyser la teinte
            bins: Nombre de bandes pour les histogrammes
        """
        self.analyze_brightness = analyze_brightness
        self.analyze_contrast = analyze_contrast
        self.analyze_hue = analyze_hue
        self.bins = bins
    
    def analyze(self, image: np.ndarray) -> VisualAnalysis:
        """
        Analyse l'image complète.
        
        Args:
            image: Image en format numpy array (BGR)
        
        Returns:
            Objet VisualAnalysis avec tous les résultats
        """
        analysis = VisualAnalysis()
        
        # Conversion en niveaux de gris pour luminosité/contraste
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Analyse de la luminosité
        if self.analyze_brightness:
            analysis.brightness = float(np.mean(gray))
        
        # Analyse du contraste
        if self.analyze_contrast:
            analysis.contrast = float(np.std(gray))
        
        # Conversion en HSV pour teinte/saturation/valeur
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        # Analyse de la teinte
        if self.analyze_hue:
            analysis.hue_distribution = self._analyze_hue(hsv)
            analysis.saturation = float(np.mean(hsv[:, :, 1]))
            analysis.value = float(np.mean(hsv[:, :, 2]))
        
        # Histogramme des couleurs
        analysis.color_histogram = self._compute_color_histogram(image)
        
        # Densité des contours
        analysis.edge_density = self._compute_edge_density(gray)
        
        return analysis
    
    def _analyze_hue(self, hsv_image: np.ndarray) -> Dict:
        """
        Analyse la distribution de la teinte.
        
        Args:
            hsv_image: Image au format HSV
        
        Returns:
            Dictionnaire avec la distribution de teinte
        """
        hue = hsv_image[:, :, 0]
        hist = cv2.calcHist([hsv_image], [0], None, [self.bins], [0, 180])
        hist = hist.flatten()
        hist = hist / hist.sum()  # Normaliser
        
        # Catégoriser les teintes
        hue_categories = {
            'red': float(np.sum(hist[0:15]) + np.sum(hist[165:180])) * 100,
            'orange': float(np.sum(hist[15:30])) * 100,
            'yellow': float(np.sum(hist[30:45])) * 100,
            'green': float(np.sum(hist[45:90])) * 100,
            'cyan': float(np.sum(hist[90:105])) * 100,
            'blue': float(np.sum(hist[105:135])) * 100,
            'magenta': float(np.sum(hist[135:165])) * 100
        }
        
        return hue_categories
    
    def _compute_color_histogram(self, image: np.ndarray) -> Dict:
        """
        Calcule l'histogramme des couleurs.
        
        Args:
            image: Image BGR
        
        Returns:
            Dictionnaire avec les histogrammes B, G, R
        """
        colors = {'blue': 0, 'green': 1, 'red': 2}
        histogram = {}
        
        for color_name, channel_idx in colors.items():
            hist = cv2.calcHist([image], [channel_idx], None, [self.bins], [0, 256])
            hist = hist.flatten()
            # Retourner les 10 valeurs les plus importantes
            top_indices = np.argsort(hist)[-10:][::-1]
            histogram[color_name] = {
                'mean': float(np.mean(image[:, :, channel_idx])),
                'std': float(np.std(image[:, :, channel_idx])),
                'top_bins': [int(i) for i in top_indices]
            }
        
        return histogram
    
    def _compute_edge_density(self, gray_image: np.ndarray) -> float:
        """
        Calcule la densité des contours (edges).
        
        Args:
            gray_image: Image en niveaux de gris
        
        Returns:
            Densité des contours (0-100)
        """
        edges = cv2.Canny(gray_image, 100, 200)
        edge_count = np.count_nonzero(edges)
        total_pixels = gray_image.shape[0] * gray_image.shape[1]
        edge_density = (edge_count / total_pixels) * 100
        
        return float(edge_density)
    
    def get_brightness_level(self, image: np.ndarray) -> str:
        """
        Retourne le niveau de luminosité.
        
        Args:
            image: Image
        
        Returns:
            'very_dark', 'dark', 'normal', 'bright', 'very_bright'
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        brightness = np.mean(gray)
        
        if brightness < 50:
            return 'very_dark'
        elif brightness < 100:
            return 'dark'
        elif brightness < 150:
            return 'normal'
        elif brightness < 200:
            return 'bright'
        else:
            return 'very_bright'
    
    def get_contrast_level(self, image: np.ndarray) -> str:
        """
        Retourne le niveau de contraste.
        
        Args:
            image: Image
        
        Returns:
            'low', 'medium', 'high', 'very_high'
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        contrast = np.std(gray)
        
        if contrast < 30:
            return 'low'
        elif contrast < 60:
            return 'medium'
        elif contrast < 100:
            return 'high'
        else:
            return 'very_high'
    
    def get_dominant_color(self, image: np.ndarray) -> Tuple[int, int, int]:
        """
        Retourne la couleur dominante.
        
        Args:
            image: Image
        
        Returns:
            Tuple (B, G, R) de la couleur dominante
        """
        # Redimensionner pour accélération
        img_small = cv2.resize(image, (150, 150))
        img_flat = img_small.reshape((-1, 3))
        img_float = np.float32(img_flat)
        
        # K-means clustering
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        _, _, centers = cv2.kmeans(img_float, 1, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
        
        dominant_color = tuple(map(int, centers[0]))
        return dominant_color
    
    def compare_images(self, image1: np.ndarray, image2: np.ndarray) -> Dict:
        """
        Compare deux images.
        
        Args:
            image1: Première image
            image2: Deuxième image
        
        Returns:
            Dictionnaire avec les différences
        """
        analysis1 = self.analyze(image1)
        analysis2 = self.analyze(image2)
        
        comparison = {
            'brightness_diff': abs(analysis1.brightness - analysis2.brightness),
            'contrast_diff': abs(analysis1.contrast - analysis2.contrast),
            'saturation_diff': abs(analysis1.saturation - analysis2.saturation),
            'edge_density_diff': abs(analysis1.edge_density - analysis2.edge_density),
            'image1_brightness_level': self.get_brightness_level(image1),
            'image2_brightness_level': self.get_brightness_level(image2),
            'image1_contrast_level': self.get_contrast_level(image1),
            'image2_contrast_level': self.get_contrast_level(image2)
        }
        
        return comparison
    
    def enhance_image(self, image: np.ndarray, 
                     brightness_factor: float = 1.0,
                     contrast_factor: float = 1.0) -> np.ndarray:
        """
        Améliore une image.
        
        Args:
            image: Image
            brightness_factor: Facteur de luminosité (1.0 = pas de changement)
            contrast_factor: Facteur de contraste (1.0 = pas de changement)
        
        Returns:
            Image améliorée
        """
        # Appliquer le contraste
        enhanced = cv2.convertScaleAbs(image, alpha=contrast_factor, beta=0)
        
        # Appliquer la luminosité
        enhanced = cv2.convertScaleAbs(enhanced, alpha=1.0, beta=(brightness_factor - 1.0) * 255)
        
        return np.clip(enhanced, 0, 255).astype(np.uint8)
