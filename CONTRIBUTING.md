# Guide de Contribution

Merci d'intéresser à la contribution au projet ImageProcessor!

## Comment contribuer

### Signaler des bugs
Veuillez utiliser la section "Issues" de GitHub pour signaler les bugs. Incluez:
- Une description claire du problème
- Les étapes pour reproduire le problème
- Votre système d'exploitation et version de Python
- Le message d'erreur complet (si applicable)

### Proposer des améliorations
Nous sommes ouverts aux suggestions! Ouvrez une issue avec:
- Une description claire de votre suggestion
- Les cas d'usage
- Les avantages potentiels

### Soumettre des modifications

1. **Fork** le dépôt
2. **Créez une branche** pour votre modification (`git checkout -b feature/AmazingFeature`)
3. **Committez** vos modifications (`git commit -m 'Add some AmazingFeature'`)
4. **Poussez** vers la branche (`git push origin feature/AmazingFeature`)
5. **Ouvrez une Pull Request**

## Standards de codage

- Suivez le style PEP 8
- Utilisez des noms de variables explicites
- Ajoutez des docstrings aux fonctions et classes
- Écrivez des tests pour vos modifications

## Tests

Avant de soumettre une Pull Request:

```bash
# Installer les dépendances de développement
pip install -e ".[dev]"

# Exécuter les tests
pytest

# Vérifier la couverture de code
pytest --cov=imgprocessor

# Vérifier la qualité du code
flake8 imgprocessor
mypy imgprocessor
```

## Structure du projet

```
imgprocessor/
├── config/              # Configuration et gestion des modules
├── text_detection/      # Détection de texte
├── shape_detection/     # Détection de formes
├── distance_measurement/ # Mesure de distances
└── visual_analysis/     # Analyse visuelle
```

## Questions?

N'hésitez pas à ouvrir une discussion ou une issue si vous avez des questions!

Merci d'avoir contribué! 🎉
