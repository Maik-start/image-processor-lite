#!/bin/bash
# Script d'activation de l'environnement virtuel

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Vérifier si l'environnement virtuel existe
if [ ! -d "venv" ]; then
    echo "Création de l'environnement virtuel..."
    python3 -m venv venv
fi

# Activer l'environnement virtuel
source venv/bin/activate

echo "================================================"
echo "Environnement virtuel imgprocessor ACTIVE"
echo "================================================"
echo ""
echo "Commandes disponibles:"
echo "  - python examples/01_basic_usage.py"
echo "  - python examples/02_text_detection.py"
echo "  - python examples/03_shape_detection.py"
echo "  - python examples/04_distance_measurement.py"
echo "  - python examples/05_visual_analysis.py"
echo "  - pytest tests/"
echo ""
echo "Pour désactiver l'environnement: deactivate"
echo ""
