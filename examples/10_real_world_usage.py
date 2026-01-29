"""
Exemple 10: Real-World Usage - Image Analysis Pipeline
Cas d'usage réel: Analyse automatisée d'images pour une application.
"""

import cv2
import sys
import json
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, asdict

sys.path.insert(0, str(Path(__file__).parent.parent))

from imgprocessor.visual_analysis import VisualAnalyzer
from imgprocessor.text_detection import TextDetector
from imgprocessor.shape_detection import ShapeDetector


@dataclass
class ImageAnalysisResult:
    """Résultat d'analyse d'une image."""
    filename: str
    timestamp: str
    
    # Propriétés visuelles
    brightness: float
    saturation: float
    contrast: float
    dominant_color: str  # Approximation
    
    # Contenu texte
    text_detected: bool
    text_content: str
    text_regions: int
    
    # Formes géométriques
    shapes_count: int
    shape_types: list
    
    # Métadonnées
    image_size: tuple
    status: str


class RealWorldImageAnalyzer:
    """
    Pipeline réelle pour analyser automatiquement des images.
    Cas d'usage: Application web d'upload d'images avec analyse.
    """
    
    def __init__(self):
        """Initialise les modules avec warmup."""
        print("🔧 Initialisation du pipeline d'analyse...")
        self.analyzer = VisualAnalyzer()
        self.text_detector = TextDetector(engine='easyocr')
        self.shape_detector = ShapeDetector()
        print("✅ Pipeline initialisé")
    
    def analyze_image(self, image_path: str) -> ImageAnalysisResult:
        """
        Analyse une image et retourne les résultats structurés.
        
        Args:
            image_path: Chemin vers l'image
            
        Returns:
            ImageAnalysisResult avec toutes les analyses
        """
        filename = Path(image_path).name
        timestamp = datetime.now().isoformat()
        
        try:
            # Charger l'image
            image = cv2.imread(image_path)
            if image is None:
                return ImageAnalysisResult(
                    filename=filename,
                    timestamp=timestamp,
                    brightness=0, saturation=0, contrast=0,
                    dominant_color="unknown",
                    text_detected=False, text_content="",
                    text_regions=0,
                    shapes_count=0, shape_types=[],
                    image_size=(0, 0),
                    status="error: image not loaded"
                )
            
            image_size = image.shape[:2]
            
            # ========================================
            # 1. ANALYSE VISUELLE (avec caching!)
            # ========================================
            visual = self.analyzer.analyze(image)
            
            brightness = visual.brightness
            saturation = visual.saturation
            contrast = visual.contrast
            
            # Approximer couleur dominante basée sur HSV
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            dominant_color = self._get_dominant_color_name(hsv)
            
            # ========================================
            # 2. DÉTECTION TEXTE (flexible API)
            # ========================================
            text_content = ""
            text_regions = 0
            text_detected = False
            
            try:
                # Mode 1: Juste les régions (pas besoin du texte OCR complet)
                text_regions_data = self.text_detector.extract_text(
                    image,
                    return_text=False,
                    return_coords=True
                )
                text_regions = len(text_regions_data) if text_regions_data else 0
                text_detected = text_regions > 0
                
                # Mode 2: Si texte détecté, récupérer le contenu
                if text_detected:
                    text_content = self.text_detector.extract_text(
                        image,
                        return_text=True,
                        return_coords=False
                    )
                    text_content = text_content[:200]  # Limiter à 200 chars
            except Exception as e:
                text_detected = False
                text_content = f"OCR unavailable: {str(e)[:50]}"
            
            # ========================================
            # 3. DÉTECTION FORMES
            # ========================================
            shapes = self.shape_detector.detect(image)
            shapes_count = len(shapes) if shapes else 0
            
            # Catégoriser les formes
            shape_types = []
            if shapes:
                for shape in shapes:
                    num_vertices = len(shape)
                    if num_vertices == 3:
                        shape_types.append("triangle")
                    elif num_vertices == 4:
                        shape_types.append("rectangle")
                    elif num_vertices > 4:
                        shape_types.append("polygon")
            
            shape_types = list(set(shape_types))  # Unique
            
            # ========================================
            # RÉSULTAT FINAL
            # ========================================
            result = ImageAnalysisResult(
                filename=filename,
                timestamp=timestamp,
                brightness=round(brightness, 2),
                saturation=round(saturation, 2),
                contrast=round(contrast, 2),
                dominant_color=dominant_color,
                text_detected=text_detected,
                text_content=text_content,
                text_regions=text_regions,
                shapes_count=shapes_count,
                shape_types=shape_types,
                image_size=image_size,
                status="success"
            )
            
            return result
            
        except Exception as e:
            return ImageAnalysisResult(
                filename=filename,
                timestamp=timestamp,
                brightness=0, saturation=0, contrast=0,
                dominant_color="unknown",
                text_detected=False, text_content="",
                text_regions=0,
                shapes_count=0, shape_types=[],
                image_size=(0, 0),
                status=f"error: {str(e)[:100]}"
            )
    
    def _get_dominant_color_name(self, hsv_image) -> str:
        """Approxime le nom de la couleur dominante."""
        # Calculer moyenne H (teinte)
        h_values = hsv_image[:, :, 0]
        mean_h = h_values.mean()
        
        # Mapper H vers nom couleur
        if mean_h < 10 or mean_h > 170:
            return "red"
        elif 10 <= mean_h < 25:
            return "orange"
        elif 25 <= mean_h < 45:
            return "yellow"
        elif 45 <= mean_h < 75:
            return "green"
        elif 75 <= mean_h < 105:
            return "cyan"
        elif 105 <= mean_h < 135:
            return "blue"
        elif 135 <= mean_h < 170:
            return "magenta"
        else:
            return "unknown"


def example_single_image_analysis():
    """Analyse une seule image."""
    print("\n" + "=" * 70)
    print("SINGLE IMAGE ANALYSIS")
    print("=" * 70)
    
    pipeline = RealWorldImageAnalyzer()
    
    # Chercher une image d'exemple
    image_path = Path(__file__).parent / "sample_image_gradient.jpg"
    
    if not image_path.exists():
        print(f"⚠️  Image non trouvée: {image_path}")
        return
    
    print(f"\n📷 Analysing: {image_path.name}")
    result = pipeline.analyze_image(str(image_path))
    
    # Afficher résultats
    print(f"\n✅ Résultats d'analyse:\n")
    print(f"   📊 Propriétés visuelles:")
    print(f"      • Brightness: {result.brightness}/255")
    print(f"      • Saturation: {result.saturation:.2f}")
    print(f"      • Contrast: {result.contrast:.2f}")
    print(f"      • Couleur dominante: {result.dominant_color}")
    
    print(f"\n   📝 Texte détecté:")
    print(f"      • Trouvé: {'Oui' if result.text_detected else 'Non'}")
    print(f"      • Régions: {result.text_regions}")
    if result.text_content:
        print(f"      • Contenu: '{result.text_content}'")
    
    print(f"\n   🔷 Formes géométriques:")
    print(f"      • Nombre: {result.shapes_count}")
    if result.shape_types:
        print(f"      • Types: {', '.join(result.shape_types)}")
    
    print(f"\n   📐 Métadonnées:")
    print(f"      • Taille: {result.image_size}")
    print(f"      • Timestamp: {result.timestamp}")
    print(f"      • Status: {result.status}")


def example_batch_processing():
    """Traite un batch d'images et exporte les résultats en JSON."""
    print("\n" + "=" * 70)
    print("BATCH PROCESSING WITH JSON EXPORT")
    print("=" * 70)
    
    pipeline = RealWorldImageAnalyzer()
    
    # Trouver les images disponibles
    image_dir = Path(__file__).parent
    sample_images = [
        image_dir / "sample_image_gradient.jpg",
        image_dir / "sample_image_with_shapes.jpg",
        image_dir / "sample_image_with_points.jpg",
    ]
    
    valid_images = [str(img) for img in sample_images if img.exists()]
    
    if not valid_images:
        print("⚠️  Aucune image d'exemple trouvée")
        return
    
    print(f"\n📦 Traitement {len(valid_images)} image(s)...")
    
    results = []
    for i, image_path in enumerate(valid_images, 1):
        print(f"   [{i}/{len(valid_images)}] {Path(image_path).name}...", end=" ", flush=True)
        result = pipeline.analyze_image(image_path)
        results.append(asdict(result))
        print(f"✓ ({result.status})")
    
    # Exporter en JSON
    output_file = Path(__file__).parent / "analysis_results.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Résultats exportés: {output_file}")
    
    # Afficher résumé
    print(f"\n📊 Résumé batch:")
    print(f"   Images traitées: {len(results)}")
    
    success_count = sum(1 for r in results if r['status'] == 'success')
    print(f"   Réussies: {success_count}")
    
    text_count = sum(1 for r in results if r['text_detected'])
    print(f"   Avec texte: {text_count}")
    
    shapes_total = sum(r['shapes_count'] for r in results)
    print(f"   Formes détectées: {shapes_total}")
    
    # Afficher sample résultat
    if results:
        print(f"\n📄 Sample résultat (1er image):")
        sample = results[0]
        print(json.dumps(sample, indent=2)[:500] + "...")


def example_api_usage():
    """Montre l'utilisation API pour intégration web."""
    print("\n" + "=" * 70)
    print("API USAGE FOR WEB INTEGRATION")
    print("=" * 70)
    
    print("""
    Exemple: Django/FastAPI endpoint
    
    @app.post("/analyze")
    def analyze_image(file: UploadFile):
        # Sauvegarder upload temporaire
        temp_path = f"/tmp/{file.filename}"
        with open(temp_path, "wb") as f:
            f.write(file.file.read())
        
        # Analyser
        analyzer = RealWorldImageAnalyzer()
        result = analyzer.analyze_image(temp_path)
        
        # Retourner JSON
        return {
            "status": "success",
            "analysis": asdict(result)
        }
    
    Response:
    {
      "status": "success",
      "analysis": {
        "filename": "photo.jpg",
        "timestamp": "2026-01-29T18:30:45.123456",
        "brightness": 128.45,
        "saturation": 0.45,
        "contrast": 0.67,
        "dominant_color": "blue",
        "text_detected": true,
        "text_content": "Hello World",
        "text_regions": 1,
        "shapes_count": 3,
        "shape_types": ["rectangle", "circle"],
        "image_size": [640, 480],
        "status": "success"
      }
    }
    """)


def main():
    """Exécute tous les exemples d'utilisation réelle."""
    print("\n" + "=" * 70)
    print("🚀 REAL-WORLD IMAGE ANALYSIS - v1.0.4")
    print("=" * 70)
    print("Cas d'usage: Application web pour analyse d'images")
    
    # Exécuter les exemples
    example_single_image_analysis()
    example_batch_processing()
    example_api_usage()
    
    print("\n" + "=" * 70)
    print("✅ Exemples d'utilisation réelle terminés!")
    print("=" * 70)
    print("\n💡 Next steps:")
    print("   1. Intégrer dans votre application (FastAPI, Django, etc.)")
    print("   2. Ajuster les seuils/filtres selon vos besoins")
    print("   3. Monitorer les performances (voir 09_best_practices.py)")
    print("   4. Ajouter caching Redis pour batch processing")


if __name__ == "__main__":
    main()
