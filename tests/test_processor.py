"""Tests pour le module ImageProcessor."""

import pytest
import numpy as np
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from imgprocessor import ImageProcessor


class TestImageProcessor:
    """Tests pour ImageProcessor."""
    
    @pytest.fixture
    def processor(self):
        """Crée une instance du processeur."""
        return ImageProcessor()
    
    @pytest.fixture
    def sample_image(self):
        """Crée une image d'exemple."""
        return np.ones((100, 100, 3), dtype=np.uint8) * 128
    
    def test_initialization(self, processor):
        """Test l'initialisation du processeur."""
        assert processor is not None
        assert processor.config is not None
    
    def test_all_modules_initialized(self, processor):
        """Teste que tous les modules sont initialisés."""
        # Les modules devraient être None s'ils sont désactivés
        # ou avoir une instance s'ils sont activés
        for module_name in ['text_detector', 'shape_detector', 'distance_measurer', 'visual_analyzer']:
            # Au moins vérifions que les attributs existent
            assert hasattr(processor, module_name)
    
    def test_detect_shapes(self, processor, sample_image):
        """Test la détection de formes."""
        if processor.config.is_module_enabled('shape_detection'):
            shapes = processor.detect_shapes(sample_image)
            assert isinstance(shapes, list)
    
    def test_measure_distance(self, processor):
        """Test la mesure de distance."""
        if processor.config.is_module_enabled('distance_measurement'):
            distance = processor.measure_distance((0, 0), (100, 0))
            assert distance is not None
            assert distance.distance == 100
            assert distance.unit == 'pixels'
    
    def test_analyze_visual_properties(self, processor, sample_image):
        """Test l'analyse visuelle."""
        if processor.config.is_module_enabled('visual_analysis'):
            analysis = processor.analyze_visual_properties(sample_image)
            assert analysis is not None
            assert hasattr(analysis, 'brightness')
            assert hasattr(analysis, 'contrast')
    
    def test_get_status(self, processor):
        """Test la récupération du statut."""
        status = processor.get_status()
        assert isinstance(status, dict)
        assert len(status) == 4
    
    def test_module_disable_returns_none(self, processor):
        """Test que les modules désactivés retournent None."""
        processor.config.disable_all_modules()
        
        sample_image = np.ones((100, 100, 3), dtype=np.uint8)
        
        assert processor.detect_shapes(sample_image) is None
        assert processor.detect_circles(sample_image) is None
        assert processor.detect_rectangles(sample_image) is None
        assert processor.measure_distance((0, 0), (10, 10)) is None
        assert processor.analyze_visual_properties(sample_image) is None
    
    def test_repr(self, processor):
        """Test la représentation en chaîne."""
        repr_str = repr(processor)
        assert 'ImageProcessor' in repr_str


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
