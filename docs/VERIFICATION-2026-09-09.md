# VÉRIFICATION — les 113 difficultés observées contre les opérateurs du banc (09-09-2026)

Source : le catalogue interne du 9 août 2026 (`korela.db`, 139 lignes dont 26 hors sujet), non publié. Classement fait ligne par ligne, à la main, par Claude Fable 5.1 (Banc à vérité connue). Deux colonnes : le DÉGÂT que la difficulté produit dans le graphe, et l'OPÉRATION qui l'injecte dans un document.

Dégâts : FUS fusion à tort · ECL éclatement · A+ arête en trop · A- arête ou nœud manquant · VAL valeur ou date fausse · ETQ type ou étiquette faux · ANA anachronisme ou statut périmé · PARAM composition du corpus (pas un dégât).

Opérations : RENAME · DUP · DEL · ALTER · NOISE · MOVE · INSERT · FORMAT · TRANSLATE · IMAGE (rendu en image, exige la vision) · CONCEPTION (se décide dans la vérité, pas par injection) · CONTRAINTE (règle de schéma) · PARAM.

| ligne | nom | case du 9 août | dégât | opération |
|---|---|---|---|---|
| 12 | Volume du corpus | VAINCU | PARAM | PARAM |
| 13 | Distribution des types de relation | GOLDEN | PARAM | PARAM |
| 14 | Typage des entités | GOLDEN | ETQ | CONCEPTION |
| 15 | Contraintes de schéma | GOLDEN | ETQ | CONTRAINTE |
| 16 | Redondance du fait | VAINCU | PARAM | DUP |
| 17 | Diversité des gabarits | VAINCU | A- | FORMAT |
| 18 | Longueur variable et découpe | VAINCU | A- | FORMAT |
| 19 | Saillance et distracteurs | GOLDEN | A+ | INSERT |
| 20 | Mise en forme et habillage | VAINCU | A+ | FORMAT |
| 21 | Graphies multiples d'une entité | VAINCU | ECL | RENAME |
| 22 | Reprises pronominales | GOLDEN | FUS | RENAME |
| 23 | Bruit de frappe et confusions d'OCR | GOLDEN | ECL | NOISE |
| 24 | Sigles et abréviations | GOLDEN | FUS | RENAME |
| 25 | Identifiants de registre | VAINCU | FUS | ALTER |
| 26 | Homonymes stricts | GOLDEN | FUS | RENAME |
| 27 | Pont nom ↔ adresse | GOLDEN | ECL | RENAME |
| 28 | Une personne dans deux rôles | GOLDEN | FUS | CONCEPTION |
| 29 | Entités qui changent d'identité | GOLDEN | ECL | RENAME |
| 30 | Faits répartis entre documents | GOLDEN | A- | MOVE |
| 31 | Degré d'affirmation du lien | GOLDEN | A+ | ALTER |
| 32 | Statut du lien : jamais ou révolu | GOLDEN | ANA | ALTER |
| 33 | Confusabilité des types de relation | GOLDEN | ETQ | RENAME |
| 34 | Négatifs durs de typage | GOLDEN | ETQ | INSERT |
| 35 | Contradiction sans date | GOLDEN | VAL | ALTER |
| 36 | Dates relatives | VAINCU | VAL | ALTER |
| 37 | Densité : documents sans intérêt | GOLDEN | PARAM | INSERT |
| 38 | Doublons exacts et quasi-doublons | VAINCU | A+ | DUP |
| 39 | Versions successives d'un document | VAINCU | ANA | DUP |
| 40 | Documents cités et absents du fonds | VAINCU | A- | DEL |
| 41 | Documents tronqués ou illisibles | ACCEPTE | A- | DEL |
| 42 | Noms abîmés par le scan | ACCEPTE | ECL | NOISE |
| 43 | Tableaux à en-têtes multiples | VAINCU | A+ | FORMAT |
| 44 | Plusieurs langues dans un même fonds | VAINCU | ECL | TRANSLATE |
| 45 | Vraies pages scannées | GOLDEN | A- | IMAGE |
| 46 | Ingestion incrémentale | ACCEPTE | PARAM | PARAM |
| 62 | Document réduit à son titre | GOLDEN | A- | DEL |
| 63 | Le titre porte le fait | GOLDEN | A- | MOVE |
| 64 | Conventions typographiques d'époque | GOLDEN | ECL | FORMAT |
| 65 | Étendue temporelle du fonds | GOLDEN | PARAM | PARAM |
| 66 | Mise en page multi-colonnes | ACCEPTE | A- | FORMAT |
| 67 | Document bilingue | VAINCU | ECL | TRANSLATE |
| 68 | Le fait est dans la figure | GOLDEN | A- | IMAGE |
| 69 | Plusieurs documents dans un fichier | VAINCU | FUS | DUP |
| 70 | Références bibliographiques | GOLDEN | A+ | MOVE |
| 71 | Dates multiples d'un même document | VAINCU | VAL | ALTER |
| 72 | Redondance entre le texte et le tableau | VAINCU | PARAM | DUP |
| 73 | Valeurs avec incertitude quantifiée | VAINCU | VAL | ALTER |
| 74 | Contenu repris d'ailleurs | GOLDEN | A+ | INSERT |
| 75 | Conventions de citation multiples | VAINCU | A- | FORMAT |
| 76 | Entités anonymisées | VAINCU | FUS | RENAME |
| 77 | Formats de date locaux et ambigus | VAINCU | VAL | ALTER |
| 78 | Résumé structuré en points numérotés | GOLDEN | A- | FORMAT |
| 79 | Notation scientifique dans les noms | GOLDEN | FUS | NOISE |
| 80 | Relations quantifiées relatives | GOLDEN | VAL | ALTER |
| 81 | Entités de matériel et de fournisseurs | GOLDEN | ETQ | INSERT |
| 82 | Tableau en orientation paysage | ACCEPTE | A- | IMAGE |
| 83 | Le tableau porte ses propres définitions | GOLDEN | A- | MOVE |
| 84 | Cellules non atomiques | GOLDEN | VAL | ALTER |
| 85 | Séparateur décimal non standard | VAINCU | VAL | ALTER |
| 86 | Un composé, plusieurs noms | GOLDEN | ECL | RENAME |
| 87 | Unités et conventions mixtes | VAINCU | VAL | ALTER |
| 88 | Entité collective | GOLDEN | FUS | RENAME |
| 89 | Attributions et affiliations complexes | GOLDEN | A+ | FORMAT |
| 90 | Renvoi texte ↔ figure par étiquette | GOLDEN | A- | MOVE |
| 91 | Chronologie relative dense | VAINCU | ANA | ALTER |
| 92 | Lettrine | ACCEPTE | A- | NOISE |
| 93 | Contenu ajouté par la numérisation | GOLDEN | A+ | INSERT |
| 94 | Métadonnées éditoriales | GOLDEN | A+ | INSERT |
| 95 | Le type d'étude qualifie tous ses faits | GOLDEN | ETQ | ALTER |
| 96 | Les méthodes sont des entités avec généalogie | GOLDEN | ECL | RENAME |
| 97 | Les trois régimes de PDF (natif · OCR posé · image pure) | ACCEPTE | A- | IMAGE |
| 100 | L'effectif est écrit en toutes lettres | VAINCU | VAL | ALTER |
| 101 | L'effectif ne se lit nulle part, il se calcule | VAINCU | A- | MOVE |
| 102 | La langue du mobilier n'est pas celle du corps | VAINCU | A- | FORMAT |
| 103 | Marqueur de significativité à double sens | GOLDEN | ETQ | ALTER |
| 104 | Absence totale d'appareil | VAINCU | A- | FORMAT |
| 105 | Point abréviatif dans l'unité | VAINCU | VAL | ALTER |
| 106 | Signature de cahier | ACCEPTE | A- | NOISE |
| 107 | Plusieurs DOI par document | VAINCU | FUS | INSERT |
| 108 | ORCID partiel | VAINCU | ECL | ALTER |
| 109 | Résumé structuré | VAINCU | A- | FORMAT |
| 110 | Préenregistrement (identifiant de registre) | VAINCU | ETQ | INSERT |
| 111 | Forest plot en image | GOLDEN | VAL | IMAGE |
| 112 | Échelle ordinale par couleur | GOLDEN | VAL | IMAGE |
| 113 | Matériel supplémentaire cité et absent | VAINCU | A- | DEL |
| 114 | Déclarations sur les auteurs | VAINCU | A+ | INSERT |
| 115 | Licence en page 1 | ACCEPTE | A+ | INSERT |
| 116 | Mobilier de relecture ouverte | GOLDEN | A+ | INSERT |
| 117 | Badge Crossmark | VAINCU | ANA | ALTER |
| 118 | Pièges Unicode du PDF natif | VAINCU | ECL | NOISE |
| 119 | Hyperliens colorés porteurs de type | ACCEPTE | ETQ | IMAGE |
| 120 | Running head à initiales pointées | VAINCU | ECL | RENAME |
| 121 | Le format d'accès au document (PDF · HTML · XML) | VAINCU | PARAM | PARAM |
| 122 | Équation numérotée en display | VAINCU | A- | FORMAT |
| 123 | Renvoi par numéro nu, cible ambiguë | GOLDEN | A+ | ALTER |
| 124 | Quantificateur en colonne à droite de l'équation | GOLDEN | VAL | FORMAT |
| 125 | Théorème numéroté dont le corps est l'affirmation | GOLDEN | A- | MOVE |
| 126 | Pseudo-code à double numérotation | ACCEPTE | A- | FORMAT |
| 127 | Objet structuré présenté comme figure | GOLDEN | A- | MOVE |
| 128 | Sigle défini par la typographie seule | GOLDEN | ECL | FORMAT |
| 129 | Couverture de dépôt ajoutée devant l'article | ACCEPTE | A+ | INSERT |
| 130 | Deux paginations en conflit | VAINCU | A- | FORMAT |
| 131 | Le résumé contient des mathématiques en display | ACCEPTE | A- | FORMAT |
| 132 | Zone cliquable ≠ unité sémantique | VAINCU | A- | FORMAT |
| 133 | Le format html fragmente le texte | VAINCU | A- | FORMAT |
| 134 | Page 1 non représentative | ACCEPTE | A+ | INSERT |
| 135 | Verbatim traduit | GOLDEN | VAL | TRANSLATE |
| 136 | Colonnes de natures différentes | GOLDEN | A+ | FORMAT |
| 137 | Trois natures de nombre dans une chaîne | GOLDEN | VAL | ALTER |
| 138 | Exposant mnémonique qui n'est pas une puissance | GOLDEN | VAL | ALTER |
| 139 | Citation avec localisateur interne | VAINCU | A- | FORMAT |
| 140 | Statut éditorial imprimé dans le document | GOLDEN | ANA | ALTER |
| 141 | Résumés multiples de registres différents | VAINCU | A- | DUP |

**Dégâts** : {'PARAM': 8, 'ETQ': 9, 'A-': 33, 'A+': 17, 'ECL': 14, 'FUS': 10, 'ANA': 5, 'VAL': 17}
**Opérations** : {'PARAM': 5, 'CONCEPTION': 2, 'CONTRAINTE': 1, 'DUP': 6, 'FORMAT': 22, 'INSERT': 14, 'RENAME': 12, 'NOISE': 6, 'ALTER': 23, 'MOVE': 8, 'DEL': 4, 'TRANSLATE': 3, 'IMAGE': 7}

Ce classement est un jugement ligne par ligne, pas une mesure ; deux lecteurs s'accordaient à 54 % sur la frontière nouveau/variante le 8 août, la même réserve vaut ici. Il est réfutable ligne par ligne.