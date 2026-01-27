# GitHub Instructions

Pour pousser ce projet vers GitHub, suivez ces étapes:

## 1. Créer un repository sur GitHub

1. Allez sur https://github.com/new
2. Entrez le nom: `imgprocessor`
3. Description: "Package modulaire de traitement et d'analyse d'images"
4. Sélectionnez "Public" ou "Private"
5. Ne cochez pas "Initialize this repository with:"
6. Cliquez sur "Create repository"

## 2. Connecter le repository local

```bash
# Remplacez USERNAME par votre nom d'utilisateur GitHub
git remote add origin https://github.com/USERNAME/imgprocessor.git

# Ou si vous utilisez SSH:
git remote add origin git@github.com:USERNAME/imgprocessor.git
```

## 3. Pousser les branches

```bash
# Pousser la branche master
git push -u origin master

# Pousser la branche develop
git push -u origin develop

# Vérifier
git branch -a
```

## 4. Configuration recommandée

### Protéger la branche master

Sur GitHub:
1. Settings → Branches
2. Cliquez sur "Add rule"
3. Branch name pattern: `master`
4. Cochez "Require pull request reviews before merging"
5. Cliquez sur "Create"

### Configuration locale

```bash
# Pour faciliter les futurs push
git config --global push.default current
```

## État actuel

```
Branches:
  - master (commit initial)
  - develop (branche actuelle)

Status:
✅ Tous les tests passent (17/17)
✅ Code structure et documenté
✅ Environnement virtuel configuré
✅ Package installable (pip install -e .)
```

## Commandes utiles

```bash
# Voir l'état
git status

# Voir l'historique
git log --oneline

# Voir les branches
git branch -a

# Changer de branche
git checkout master
git checkout develop

# Créer une nouvelle branche de feature
git checkout -b feature/ma-feature

# Commiter les changements
git add .
git commit -m "Description du changement"

# Pousser
git push

# Pousser une nouvelle branche
git push -u origin ma-branche
```

## Pour des contributions futures

```bash
# Créer une branche de feature
git checkout -b feature/mon-amelioration

# Faire les changements
# Tester
pytest tests/ -v

# Commiter
git add .
git commit -m "Ajouter mon amélioration"

# Pousser
git push origin feature/mon-amelioration

# Sur GitHub, créer une Pull Request vers develop
# Une fois approvée, merger dans develop
# Puis merger develop dans master pour release
```

## Commandes d'aide

```bash
# Voir les remotes
git remote -v

# Supprimer un remote
git remote remove origin

# Renommer une branche locale
git branch -m ancien-nom nouveau-nom

# Renommer et pousser
git branch -m ancien-nom nouveau-nom
git push origin nouveau-nom
git push origin --delete ancien-nom
```
