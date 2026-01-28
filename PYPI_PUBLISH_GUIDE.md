# Guide de Publication sur PyPI

## ✅ Publication Réussie

Votre package `image-processor-lite` est maintenant publié sur PyPI ! ✅

1. **Compte PyPI** : Créez-le sur https://pypi.org/account/register/
2. **Token d'authentification** : Générez-le depuis https://pypi.org/manage/account/

## 📋 Étapes pour publier

### 1. Installer les outils nécessaires

```bash
pip install build twine wheel
```

### 2. Mettre à jour votre version (si besoin)

Dans `setup.py`, modifiez la version (ex: 1.0.1, 1.1.0, etc.)

### 3. Créer les distributions

```bash
cd /home/virus-one/Documents/code/package_dev
python -m build
```

Cela crée :
- `dist/*.tar.gz` (source distribution)
- `dist/*.whl` (wheel distribution)

### 4. Vérifier les distributions

```bash
twine check dist/*
```

### 5. Publier sur PyPI

#### Option A : Avec token (recommandé)

```bash
twine upload dist/* --username __token__ --password pypi-YOUR_TOKEN_HERE
```

#### Option B : Interactif (demande username/password)

```bash
twine upload dist/*
```

### 6. Vérifier la publication

Votre package est maintenant visible sur :
- https://pypi.org/project/image-processor-lite/
- Installable via : `pip install image-processor-lite`

## 🔐 Configuration de ~/.pypirc (Optionnel mais recommandé)

Créez un fichier `~/.pypirc` pour stocker vos credentials de manière sécurisée :

```ini
[distutils]
index-servers =
    pypi

[pypi]
username = __token__
password = pypi-YOUR_TOKEN_HERE
```

Puis publiez simplement avec :
```bash
twine upload dist/*
```

## ⚠️ Points importants

1. **Nom unique** : `image-processor-lite` est maintenant publié sur PyPI ✅
2. **Versions sémantiques** : Respectez la versioning (1.0.0, 1.0.1, etc.)
3. **Nettoyage** : Supprimez les anciens `dist/` avant chaque build
4. **Métadonnées** : Assurez-vous que `author`, `description` et `url` sont corrects

## 🔄 Mises à jour futures

Pour chaque nouvelle version :
1. Augmentez `version` dans `setup.py`
2. `python -m build`
3. `twine upload dist/*`
