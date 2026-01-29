"""
Exemple 6: Optimisations et Best Practices (v1.0.5)
Comment utiliser le package de manière optimale
"""

import cv2
from imgprocessor.text_detection import TextDetector

print("Best Practices - Optimisations")
print("=" * 60)

# 1️⃣  Réutiliser la même instance (important!)
print("\n1️⃣  Réutiliser l'instance du détecteur")
print("   ❌ MAUVAIS: Créer une nouvelle instance à chaque appel")
print("   ✅ BON: Réutiliser la même instance")

detector = TextDetector(mode='balanced')  # Une seule fois!
for i in range(5):
    image = cv2.imread(f'image_{i}.jpg')
    text = detector.extract_text(image)  # Rapide!

# 2️⃣  Choisir le bon mode selon ton cas d'usage
print("\n2️⃣  Choisir le bon mode")
print("   • SPEED (100ms):      Texte gros/clair")
print("   • BALANCED (100ms):   Production ✅")
print("   • QUALITY (1160ms):   Texte petit/complexe")
print("   • FastDetector (90ms): Temps réel")

# 3️⃣  Cache automatique par appel
print("\n3️⃣  Cache automatique")
print("   • Premier appel: 100-1000ms (selon mode)")
print("   • Appels suivants sur MÊME image: 0ms (cache)")

detector = TextDetector()
image = cv2.imread('mon_image.jpg')

text1 = detector.extract_text(image)  # 100ms (normal)
text2 = detector.extract_text(image)  # 0ms (cached)

print("   ✅ Appels répétés sur même image utilisent le cache")

# 4️⃣  Multi-threading sécurisé
print("\n4️⃣  Multi-threading")
print("   Le cache global est thread-safe")
print("   Créez une instance par thread pour éviter les contentions")

# 5️⃣  Mode production
print("\n5️⃣  Configuration production recommandée")
detector = TextDetector(mode='balanced')  # Bon compromis
# Le cache global est activé automatiquement
# Chaque instance réutilise le même modèle OCR

print("\n" + "=" * 60)
print("✅ Configuration optimale pour la production")
print("=" * 60)
