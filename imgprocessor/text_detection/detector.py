"""
Module de détection et extraction de texte.
Supporte plusieurs moteurs (EasyOCR, Tesseract).
"""

import cv2
import numpy as np
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass


@dataclass
class TextRegion:
    """Représente une région de texte détectée."""
    text: str
    confidence: float
    bbox: Tuple[int, int, int, int]  # (x, y, width, height)
    language: str
    
    def to_dict(self) -> Dict:
        """Convertit en dictionnaire."""
        return {
            'text': self.text,
            'confidence': self.confidence,
            'bbox': self.bbox,
            'language': self.language
        }


class TextDetector:
    """
    Détecteur de texte utilisant EasyOCR ou Tesseract.
    """
    
    def __init__(self, languages: List[str] = None, engine: str = 'easyocr'):
        """
        Initialise le détecteur de texte.
        
        Args:
            languages: Liste des langues à reconnaître (ex: ['fra', 'eng'])
            engine: Moteur OCR à utiliser ('easyocr' ou 'tesseract')
        """
        self.languages = languages or ['fra', 'eng']
        self.engine = engine
        self.reader = None
        
        if engine == 'easyocr':
            try:
                import easyocr
                self.reader = easyocr.Reader(self.languages, gpu=False)
            except ImportError:
                raise ImportError("easyocr non installé. Installez avec: pip install easyocr")
        elif engine == 'tesseract':
            try:
                import pytesseract
                self.pytesseract = pytesseract
            except ImportError:
                raise ImportError("pytesseract non installé. Installez avec: pip install pytesseract")
        else:
            raise ValueError(f"Moteur OCR inconnu: {engine}")
    
    def detect(self, image: np.ndarray, min_confidence: float = 0.5) -> List[TextRegion]:
        """
        Détecte le texte dans une image.
        
        Args:
            image: Image en format numpy array (BGR ou RGB)
            min_confidence: Seuil de confiance minimum
        
        Returns:
            Liste des régions de texte détectées
        """
        if self.engine == 'easyocr':
            return self._detect_easyocr(image, min_confidence)
        elif self.engine == 'tesseract':
            return self._detect_tesseract(image, min_confidence)
    
    def _detect_easyocr(self, image: np.ndarray, min_confidence: float) -> List[TextRegion]:
        """Détection avec EasyOCR."""
        results = self.reader.readtext(image)
        
        text_regions = []
        for detection in results:
            bbox_points = detection[0]
            text = detection[1]
            confidence = detection[2]
            
            if confidence >= min_confidence:
                # Convertir les points du bbox en coordonnées (x, y, w, h)
                x_coords = [p[0] for p in bbox_points]
                y_coords = [p[1] for p in bbox_points]
                x = int(min(x_coords))
                y = int(min(y_coords))
                w = int(max(x_coords) - x)
                h = int(max(y_coords) - y)
                
                region = TextRegion(
                    text=text,
                    confidence=float(confidence),
                    bbox=(x, y, w, h),
                    language='mixed'
                )
                text_regions.append(region)
        
        return text_regions
    
    def _detect_tesseract(self, image: np.ndarray, min_confidence: float) -> List[TextRegion]:
        """Détection avec Tesseract."""
        # Prétraitement optionnel
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        data = self.pytesseract.image_to_data(gray, output_type=self.pytesseract.Output.DICT)
        
        text_regions = []
        for i in range(len(data['text'])):
            text = data['text'][i].strip()
            confidence = float(data['conf'][i]) / 100.0
            
            if text and confidence >= min_confidence:
                x = data['left'][i]
                y = data['top'][i]
                w = data['width'][i]
                h = data['height'][i]
                
                region = TextRegion(
                    text=text,
                    confidence=confidence,
                    bbox=(x, y, w, h),
                    language='unknown'
                )
                text_regions.append(region)
        
        return text_regions
    
    def extract_text(self, image: np.ndarray, min_confidence: float = 0.5) -> str:
        """
        Extrait tout le texte d'une image.
        
        Args:
            image: Image en format numpy array
            min_confidence: Seuil de confiance minimum
        
        Returns:
            Chaîne contenant tout le texte détecté
        """
        regions = self.detect(image, min_confidence)
        return '\n'.join([region.text for region in regions])
    
    def get_regions_with_coords(self, image: np.ndarray, min_confidence: float = 0.5) -> List[Dict]:
        """Retourne les régions de texte avec leurs coordonnées."""
        regions = self.detect(image, min_confidence)
        return [region.to_dict() for region in regions]
