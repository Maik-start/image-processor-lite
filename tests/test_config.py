"""Tests pour le module de configuration."""

import pytest
import json
import tempfile
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from imgprocessor.config import ImageProcessorConfig, ModuleConfig


class TestImageProcessorConfig:
    """Tests pour ImageProcessorConfig."""
    
    def test_initialization(self):
        """Test l'initialisation de la configuration."""
        config = ImageProcessorConfig()
        
        assert 'text_detection' in config.modules
        assert 'shape_detection' in config.modules
        assert 'distance_measurement' in config.modules
        assert 'visual_analysis' in config.modules
    
    def test_enable_disable_module(self):
        """Test l'activation/désactivation de modules."""
        config = ImageProcessorConfig()
        
        # Vérifier que tous les modules sont activés par défaut
        assert config.is_module_enabled('text_detection')
        
        # Désactiver un module
        config.enable_module('text_detection', False)
        assert not config.is_module_enabled('text_detection')
        
        # Réactiver un module
        config.enable_module('text_detection', True)
        assert config.is_module_enabled('text_detection')
    
    def test_enable_disable_all_modules(self):
        """Test l'activation/désactivation de tous les modules."""
        config = ImageProcessorConfig()
        
        # Tous activés par défaut
        for module in config.modules.values():
            assert module.enabled
        
        # Désactiver tous
        config.disable_all_modules()
        for module in config.modules.values():
            assert not module.enabled
        
        # Réactiver tous
        config.enable_all_modules()
        for module in config.modules.values():
            assert module.enabled
    
    def test_set_get_module_options(self):
        """Test la configuration des options de module."""
        config = ImageProcessorConfig()
        
        # Obtenir les options par défaut
        options = config.get_module_options('text_detection')
        assert 'language' in options
        assert 'engine' in options
        
        # Modifier les options
        new_options = {'language': ['eng'], 'engine': 'tesseract'}
        config.set_module_options('text_detection', new_options)
        
        # Vérifier les modifications
        updated_options = config.get_module_options('text_detection')
        assert updated_options['language'] == ['eng']
        assert updated_options['engine'] == 'tesseract'
    
    def test_save_load_config(self):
        """Test la sauvegarde et chargement de configuration."""
        config1 = ImageProcessorConfig()
        
        # Modifier la configuration
        config1.enable_module('text_detection', False)
        config1.set_module_options('shape_detection', {'detect_circles': False})
        
        # Sauvegarder dans un fichier temporaire
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_file = f.name
        
        try:
            config1.save_to_file(temp_file)
            
            # Charger la configuration dans une nouvelle instance
            config2 = ImageProcessorConfig(temp_file)
            
            # Vérifier que les modifications ont été chargées
            assert not config2.is_module_enabled('text_detection')
            options = config2.get_module_options('shape_detection')
            assert options['detect_circles'] == False
        finally:
            Path(temp_file).unlink()
    
    def test_invalid_module_name(self):
        """Test les erreurs avec des noms de module invalides."""
        config = ImageProcessorConfig()
        
        with pytest.raises(ValueError):
            config.enable_module('invalid_module', True)
        
        with pytest.raises(ValueError):
            config.is_module_enabled('invalid_module')
        
        with pytest.raises(ValueError):
            config.get_module_options('invalid_module')
    
    def test_get_status(self):
        """Test la récupération du statut."""
        config = ImageProcessorConfig()
        status = config.get_status()
        
        assert len(status) == 4
        assert all(isinstance(v, dict) for v in status.values())
        assert all('enabled' in v and 'options' in v for v in status.values())


class TestModuleConfig:
    """Tests pour ModuleConfig."""
    
    def test_module_config_creation(self):
        """Test la création d'une configuration de module."""
        config = ModuleConfig(enabled=True, options={'key': 'value'})
        
        assert config.enabled is True
        assert config.options == {'key': 'value'}
    
    def test_module_config_defaults(self):
        """Test les valeurs par défaut."""
        config = ModuleConfig()
        
        assert config.enabled is True
        assert config.options == {}


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
