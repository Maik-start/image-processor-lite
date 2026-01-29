#!/bin/bash
"""
Script de build et upload du package sur PyPI.
Utilisation: bash build_and_upload.sh [test|release]
"""

set -e

# Déterminer si c'est un test ou une release
UPLOAD_TYPE="${1:-test}"

if [ "$UPLOAD_TYPE" != "test" ] && [ "$UPLOAD_TYPE" != "release" ]; then
    echo "❌ Usage: bash build_and_upload.sh [test|release]"
    exit 1
fi

echo "============================================================"
echo "🚀 BUILD & UPLOAD SCRIPT - image-processor-lite"
echo "============================================================"
echo ""

# Vérifier les prérequis
echo "1️⃣  Vérification des prérequis..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 non trouvé"
    exit 1
fi

if ! python3 -m pip show build &> /dev/null; then
    echo "⚙️  Installation de build..."
    python3 -m pip install build --quiet
fi

if ! python3 -m pip show twine &> /dev/null; then
    echo "⚙️  Installation de twine..."
    python3 -m pip install twine --quiet
fi

echo "✅ Prérequis OK"
echo ""

# Nettoyer les builds précédents
echo "2️⃣  Nettoyage des builds précédents..."
rm -rf build/ dist/ *.egg-info image_processor_lite.egg-info 2>/dev/null
echo "✅ Nettoyage effectué"
echo ""

# Construire le package
echo "3️⃣  Construction du package..."
python3 -m build
echo "✅ Package construit"
echo ""

# Vérifier les fichiers générés
echo "4️⃣  Vérification des fichiers générés..."
if [ -f "dist/image-processor-lite-1.0.2.tar.gz" ]; then
    echo "✅ Archive source: dist/image-processor-lite-1.0.2.tar.gz"
fi

if [ -f "dist/image_processor_lite-1.0.2-py3-none-any.whl" ]; then
    echo "✅ Wheel: dist/image_processor_lite-1.0.2-py3-none-any.whl"
fi

echo ""

# Valider le package
echo "5️⃣  Validation du package..."
python3 -m twine check dist/*
echo "✅ Validation OK"
echo ""

# Upload
echo "6️⃣  Upload sur PyPI..."

if [ "$UPLOAD_TYPE" = "test" ]; then
    echo "   🧪 Mode TEST (TestPyPI)"
    python3 -m twine upload --repository testpypi dist/* --verbose
    echo ""
    echo "✅ Upload sur TestPyPI réussi!"
    echo "   Vous pouvez tester l'installation avec:"
    echo "   pip install -i https://test.pypi.org/simple/ image-processor-lite==1.0.2"
else
    echo "   📦 Mode RELEASE (PyPI)"
    echo ""
    echo "⚠️  ATTENTION: Ceci publiera la version 1.0.2 sur PyPI officiel"
    echo "   Les changements seront publics et permanents!"
    echo ""
    read -p "Êtes-vous sûr? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        python3 -m twine upload dist/* --verbose
        echo ""
        echo "✅ Upload sur PyPI réussi!"
        echo "   Le package est maintenant disponible à l'installation:"
        echo "   pip install image-processor-lite"
    else
        echo "❌ Upload annulé"
        exit 1
    fi
fi

echo ""
echo "============================================================"
echo "✅ BUILD & UPLOAD COMPLÉTÉ!"
echo "============================================================"
echo ""
