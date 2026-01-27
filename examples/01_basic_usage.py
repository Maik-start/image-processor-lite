"""
Exemple 1: Utilisation basique du package ImageProcessor
Démontre l'activation/désactivation des modules
"""

import cv2
import sys
from pathlib import Path

# Ajouter le dossier parent au chemin
sys.path.insert(0, str(Path(__file__).parent.parent))

from imgprocessor import ImageProcessor


def example_basic_usage():
    """Exemple d'utilisation basique."""
    print("=" * 60)
    print("Exemple 1: Utilisation Basique")
    print("=" * 60)
    
    # Créer une instance du processeur avec optimisation équilibrée
    processor = ImageProcessor(optimization="balanced")
    
    # Afficher le statut de tous les modules
    status = processor.get_status()
    print("\nStatut des modules:")
    for module_name, config in status.items():
        enabled = "✓ Activé" if config['enabled'] else "✗ Désactivé"
        print(f"  {module_name}: {enabled}")
    
    # Désactiver le module de texte
    print("\nDésactivation du module de texte...")
    processor.config.enable_module('text_detection', False)
    
    # Activer le module de détection de formes
    print("Activation du module de détection de formes...")
    processor.config.enable_module('shape_detection', True)
    
    # Afficher le nouveau statut
    status = processor.get_status()
    print("\nNouveau statut:")
    for module_name, config in status.items():
        enabled = "✓ Activé" if config['enabled'] else "✗ Désactivé"
        print(f"  {module_name}: {enabled}")
    
    # Sauvegarder la configuration
    config_file = Path(__file__).parent / "config_example.json"
    processor.config.save_to_file(str(config_file))
    print(f"\nConfiguration sauvegardée dans: {config_file}")
    
    # Charger la configuration
    processor2 = ImageProcessor(str(config_file))
    print("Configuration chargée avec succès!")
    print(f"Module texte activé: {processor2.config.is_module_enabled('text_detection')}")


if __name__ == "__main__":
    example_basic_usage()
