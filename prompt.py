system_prompt = """Le but est de réaliser une analyse qualitative par la méthode du codage déductif. Vous devez analyser l'extrait d'entretien suivant pour identifier si l'un des codes prédéfinis est présent. 1. **Réfléchissez dans le Carnet de notes** : Analysez l'extrait en identifiant les éléments qui pourraient correspondre à chaque code. Soyez attentif aux indices subtils ou implicites qui pourraient indiquer la présence d'un code. Justifiez votre décision avec des éléments concrets. Si le code est absent, expliquez pourquoi. 2. **Prise de décision** : Décidez si le code est présent (`true`) ou absent (`false`). Si l'information est ambiguë mais qu'il y a des éléments suggérant la présence du code, considérez-le comme présent (`true`). Si l'extrait ne contient aucune indication, alors la réponse doit être `false`. **Exigences de sortie** : - Retournez un JSON valide avec les clés suivantes pour chaque code : - **carnet_de_notes** : Explication textuelle. - **est_present** : Booléen (`true` ou `false`). - Ne retournez que du JSON valide, sans texte supplémentaire ou erreurs de formatage. **Les codes à évaluer (avec leurs descriptions)** : - **gain_de_temps** : L'extrait mentionne-t-il, même de manière implicite, une réduction du temps nécessaire pour préparer les cours grâce aux modèles de langage ? - **augmentation_productivite** : L'extrait indique-t-il, même indirectement, une augmentation de la productivité, comme la création de plus de matériel pédagogique ? - **autonomie** : L'extrait reflète-t-il, explicitement ou implicitement, un sentiment d'autonomie et de contrôle sur le contenu généré par l'enseignant ? - **propriete_du_contenu** : L'extrait mentionne-t-il, directement ou indirectement, un sentiment de propriété sur le contenu créé, malgré l'assistance des modèles de langage ? - **biais_culturels** : L'extrait mentionne-t-il des biais culturels ou des erreurs dans le contenu généré ? - **correction_des_biais** : L'extrait parle-t-il de corrections de biais ou d'erreurs dans le contenu généré ? - **engagement_des_etudiants** : L'extrait indique-t-il un engagement accru des étudiants grâce aux nouveaux outils ? - **amelioration_des_pratiques_d_enseignement** : L'extrait mentionne-t-il une amélioration des pratiques pédagogiques grâce aux modèles de langage ? - **innovation** : L'extrait évoque-t-il l'introduction de nouvelles idées ou méthodes pédagogiques grâce aux modèles de langage ? - **nouvelles_methodes_d_enseignement** : L'extrait mentionne-t-il des nouvelles méthodes d'enseignement adoptées suite à l'utilisation des modèles de langage ?"""

# Exemples
# Exemple 1 - Réduction du temps
user_prompt_1 = 'Extrait : "Depuis que j\'utilise cet outil, je trouve que le temps que je passe à préparer mes cours a considérablement diminué. Avant, je passais des heures à chercher des ressources, mais maintenant, tout est à portée de main. J\'ai vraiment l\'impression de gagner du temps."'
assistant_response_1 = """
{
    "gain_de_temps": {
        "carnet_de_notes": "L'utilisateur mentionne explicitement une réduction du temps consacré à la préparation des cours grâce à l'utilisation de l'outil.",
        "est_present": true
    },
    "augmentation_productivite": {
        "carnet_de_notes": "L'extrait ne fait pas mention de l'augmentation de la productivité en termes de création de matériel pédagogique.",
        "est_present": false
    },
    "autonomie": {
        "carnet_de_notes": "L'extrait ne reflète pas explicitement un sentiment d'autonomie ou de contrôle sur le contenu généré.",
        "est_present": false
    },
    "propriete_du_contenu": {
        "carnet_de_notes": "Il n'y a aucune mention de la propriété du contenu créé.",
        "est_present": false
    },
    "biais_culturels": {
        "carnet_de_notes": "Aucune mention de biais culturels dans l'extrait.",
        "est_present": false
    },
    "correction_des_biais": {
        "carnet_de_notes": "Aucune correction de biais n'est mentionnée.",
        "est_present": false
    },
    "engagement_des_etudiants": {
        "carnet_de_notes": "L'extrait ne fait pas mention de l'engagement des étudiants.",
        "est_present": false
    },
    "amelioration_des_pratiques_d_enseignement": {
        "carnet_de_notes": "Aucune amélioration des pratiques pédagogiques n'est mentionnée.",
        "est_present": false
    },
    "innovation": {
        "carnet_de_notes": "L'extrait ne parle pas de l'introduction de nouvelles idées ou méthodes pédagogiques.",
        "est_present": false
    },
    "nouvelles_methodes_d_enseignement": {
        "carnet_de_notes": "Aucune nouvelle méthode d'enseignement n'est mentionnée.",
        "est_present": false
    }
}
"""

# Exemple 2 - Productivité accrue
user_prompt_2 = 'Extrait : "Grâce à cet outil, j\'ai réussi à produire plus de matériel pédagogique que jamais auparavant. Non seulement j\'ai pu couvrir plus de sujets, mais j\'ai aussi eu le temps de peaufiner les détails, ce qui a vraiment amélioré la qualité de mon enseignement."'
assistant_response_2 = """
{
    "gain_de_temps": {
        "carnet_de_notes": "L'utilisateur suggère un gain de temps implicite en mentionnant qu'il a eu le temps de peaufiner les détails.",
        "est_present": true
    },
    "augmentation_productivite": {
        "carnet_de_notes": "L'utilisateur mentionne explicitement une augmentation de la productivité en termes de production de matériel pédagogique.",
        "est_present": true
    },
    "autonomie": {
        "carnet_de_notes": "L'extrait ne reflète pas un sentiment explicite d'autonomie.",
        "est_present": false
    },
    "propriete_du_contenu": {
        "carnet_de_notes": "Aucune mention de propriété du contenu.",
        "est_present": false
    },
    "biais_culturels": {
        "carnet_de_notes": "Aucun biais culturel n'est mentionné.",
        "est_present": false
    },
    "correction_des_biais": {
        "carnet_de_notes": "Aucune correction de biais n'est mentionnée.",
        "est_present": false
    },
    "engagement_des_etudiants": {
        "carnet_de_notes": "Aucune mention de l'engagement des étudiants.",
        "est_present": false
    },
    "amelioration_des_pratiques_d_enseignement": {
        "carnet_de_notes": "L'utilisateur mentionne une amélioration de la qualité de l'enseignement, mais pas explicitement une amélioration des pratiques pédagogiques.",
        "est_present": false
    },
    "innovation": {
        "carnet_de_notes": "Aucune innovation n'est mentionnée.",
        "est_present": false
    },
    "nouvelles_methodes_d_enseignement": {
        "carnet_de_notes": "Aucune nouvelle méthode d'enseignement n'est mentionnée.",
        "est_present": false
    }
}
"""

# Exemple 3 - Autonomie et propriété
user_prompt_3 = 'Extrait : "Avec cet outil, je me sens vraiment maître de ce que je produis. Même si je l\'utilise pour générer du contenu, je le personnalise tellement que je me considère comme le véritable auteur de tout ce que je présente à mes étudiants."'
assistant_response_3 = """
{
    "gain_de_temps": {
        "carnet_de_notes": "Aucune mention de gain de temps.",
        "est_present": false
    },
    "augmentation_productivite": {
        "carnet_de_notes": "Aucune mention d'augmentation de productivité.",
        "est_present": false
    },
    "autonomie": {
        "carnet_de_notes": "L'utilisateur exprime un sentiment explicite de contrôle et d'autonomie sur le contenu généré.",
        "est_present": true
    },
    "propriete_du_contenu": {
        "carnet_de_notes": "L'utilisateur mentionne explicitement qu'il se considère comme le véritable auteur du contenu, ce qui indique un sentiment de propriété.",
        "est_present": true
    },
    "biais_culturels": {
        "carnet_de_notes": "Aucun biais culturel n'est mentionné.",
        "est_present": false
    },
    "correction_des_biais": {
        "carnet_de_notes": "Aucune correction de biais n'est mentionnée.",
        "est_present": false
    },
    "engagement_des_etudiants": {
        "carnet_de_notes": "Aucune mention de l'engagement des étudiants.",
        "est_present": false
    },
    "amelioration_des_pratiques_d_enseignement": {
        "carnet_de_notes": "Aucune amélioration des pratiques pédagogiques n'est mentionnée.",
        "est_present": false
    },
    "innovation": {
        "carnet_de_notes": "Aucune innovation n'est mentionnée.",
        "est_present": false
    },
    "nouvelles_methodes_d_enseignement": {
        "carnet_de_notes": "Aucune nouvelle méthode d'enseignement n'est mentionnée.",
        "est_present": false
    }
}
"""

# Exemple 4 - Erreur simulée et correction
user_prompt_4 = 'Extrait : "Cet outil m\'a permis d\'introduire une nouvelle méthode pédagogique dans mes cours, ce qui est vraiment innovant."'
assistant_response_4_initial = """
{
    "gain_de_temps": {
        "carnet_de_notes": "Aucune mention de gain de temps.",
        "est_present": false
    },
    "augmentation_productivite": {
        "carnet_de_notes": "Aucune mention d'augmentation de productivité.",
        "est_present": false
    },
    "autonomie": {
        "carnet_de_notes": "Aucune mention d'autonomie.",
        "est_present": false
    },
    "propriete_du_contenu": {
        "carnet_de_notes": "Aucune mention de propriété du contenu.",
        "est_present": false
    },
    "biais_culturels": {
        "carnet_de_notes": "Aucun biais culturel n'est mentionné.",
        "est_present": false
    },
    "correction_des_biais": {
        "carnet_de_notes": "Aucune correction de biais n'est mentionnée.",
        "est_present": false
    },
    "engagement_des_etudiants": {
        "carnet_de_notes": "Aucune mention de l'engagement des étudiants.",
        "est_present": false
    },
    "amelioration_des_pratiques_d_enseignement": {
        "carnet_de_notes": "Aucune mention d'amélioration des pratiques pédagogiques.",
        "est_present": false
    },
    "innovation": {
        "carnet_de_notes": "L'utilisateur mentionne explicitement une innovation pédagogique introduite grâce à l'outil.",
        # "est_present": true -> Clé manquante pour simuler une erreur
    },
    "nouvelles_methodes_d_enseignement": {
        "carnet_de_notes": "L'utilisateur mentionne l'introduction d'une nouvelle méthode d'enseignement.",
        "est_present": true
    }
}
"""

# L'utilisateur reçoit une erreur de validation
validation_error = """Erreur rencontrée : 1 validation error for CodeResult innovation.est_present Field required [type=missing, input_value={'carnet_de_notes': 'L'utilisateur mentionne explicitement une innovation pédagogique introduite grâce à l'outil.'}, input_type=dict]"""

# Réponse corrigée par l'assistant
assistant_response_4_corrected = """
{
    "gain_de_temps": {
        "carnet_de_notes": "Aucune mention de gain de temps.",
        "est_present": false
    },
    "augmentation_productivite": {
        "carnet_de_notes": "Aucune mention d'augmentation de productivité.",
        "est_present": false
    },
    "autonomie": {
        "carnet_de_notes": "Aucune mention d'autonomie.",
        "est_present": false
    },
    "propriete_du_contenu": {
        "carnet_de_notes": "Aucune mention de propriété du contenu.",
        "est_present": false
    },
    "biais_culturels": {
        "carnet_de_notes": "Aucun biais culturel n'est mentionné.",
        "est_present": false
    },
    "correction_des_biais": {
        "carnet_de_notes": "Aucune correction de biais n'est mentionnée.",
        "est_present": false
    },
    "engagement_des_etudiants": {
        "carnet_de_notes": "Aucune mention de l'engagement des étudiants.",
        "est_present": false
    },
    "amelioration_des_pratiques_d_enseignement": {
        "carnet_de_notes": "Aucune mention d'amélioration des pratiques pédagogiques.",
        "est_present": false
    },
    "innovation": {
        "carnet_de_notes": "L'utilisateur mentionne explicitement une innovation pédagogique introduite grâce à l'outil.",
        "est_present": true  # Clé ajoutée pour corriger l'erreur
    },
    "nouvelles_methodes_d_enseignement": {
        "carnet_de_notes": "L'utilisateur mentionne l'introduction d'une nouvelle méthode d'enseignement.",
        "est_present": true
    }
}
"""

# Exemple 5 - Ambiguïté et biais culturels
user_prompt_5 = 'Extrait : "Je me demande parfois si cet outil comprend vraiment la diversité culturelle de ma classe. Il y a des moments où les réponses semblent un peu biaisées."'
assistant_response_5 = """
{
    "gain_de_temps": {
        "carnet_de_notes": "Aucune mention de gain de temps.",
        "est_present": false
    },
    "augmentation_productivite": {
        "carnet_de_notes": "Aucune mention d'augmentation de productivité.",
        "est_present": false
    },
    "autonomie": {
        "carnet_de_notes": "Aucune mention d'autonomie.",
        "est_present": false
    },
    "propriete_du_contenu": {
        "carnet_de_notes": "Aucune mention de propriété du contenu.",
        "est_present": false
    },
    "biais_culturels": {
        "carnet_de_notes": "L'utilisateur exprime une préoccupation concernant la compréhension de la diversité culturelle par l'outil, ce qui pourrait suggérer la présence de biais culturels.",
        "est_present": true
    },
    "correction_des_biais": {
        "carnet_de_notes": "L'extrait ne mentionne pas explicitement la correction des biais.",
        "est_present": false
    },
    "engagement_des_etudiants": {
        "carnet_de_notes": "Aucune mention de l'engagement des étudiants.",
        "est_present": false
    },
    "amelioration_des_pratiques_d_enseignement": {
        "carnet_de_notes": "Aucune mention d'amélioration des pratiques pédagogiques.",
        "est_present": false
    },
    "innovation": {
        "carnet_de_notes": "Aucune mention d'innovation.",
        "est_present": false
    },
    "nouvelles_methodes_d_enseignement": {
        "carnet_de_notes": "Aucune nouvelle méthode d'enseignement n'est mentionnée.",
        "est_present": false
    }
}
"""

# Exemple 6 - Complètement hors sujet
user_prompt_6 = 'Extrait : "L’autre jour, j’ai rencontré un ancien collègue de travail. Nous avons discuté de nos souvenirs passés au sein de l’entreprise, des projets sur lesquels nous avons travaillé ensemble, et des défis que nous avons relevés. C’était agréable de se remémorer ces moments."'
assistant_response_6 = """
{
    "gain_de_temps": {
        "carnet_de_notes": "L'extrait ne mentionne aucun gain de temps lié à la préparation des cours.",
        "est_present": false
    },
    "augmentation_productivite": {
        "carnet_de_notes": "Aucune augmentation de la productivité n'est évoquée dans cet extrait.",
        "est_present": false
    },
    "autonomie": {
        "carnet_de_notes": "L'extrait ne reflète aucun sentiment d'autonomie ou de contrôle sur le contenu pédagogique.",
        "est_present": false
    },
    "propriete_du_contenu": {
        "carnet_de_notes": "Aucune mention de la propriété du contenu n'est faite.",
        "est_present": false
    },
    "biais_culturels": {
        "carnet_de_notes": "Il n'y a aucune mention de biais culturels ou d'erreurs dans cet extrait.",
        "est_present": false
    },
    "correction_des_biais": {
        "carnet_de_notes": "Aucune correction de biais n'est mentionnée.",
        "est_present": false
    },
    "engagement_des_etudiants": {
        "carnet_de_notes": "L'engagement des étudiants n'est pas mentionné dans cet extrait.",
        "est_present": false
    },
    "amelioration_des_pratiques_d_enseignement": {
        "carnet_de_notes": "Aucune amélioration des pratiques pédagogiques n'est mentionnée.",
        "est_present": false
    },
    "innovation": {
        "carnet_de_notes": "Aucune innovation pédagogique n'est mentionnée.",
        "est_present": false
    },
    "nouvelles_methodes_d_enseignement": {
        "carnet_de_notes": "Aucune nouvelle méthode d'enseignement n'est mentionnée.",
        "est_present": false
    }
}
"""
