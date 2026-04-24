"""
OrientAI — Les 48 questions du questionnaire
Deux versions :
- QUESTIONS_ADULTE : vouvoiement, contexte professionnel (original)
- QUESTIONS_ELEVE  : tutoiement, contexte scolaire / lycée
"""

# ══════════════════════════════════════════════════════════════════════════════
# VERSION ADULTE (originale, inchangée)
# ══════════════════════════════════════════════════════════════════════════════
"""
OrientAI — Les 48 questions du questionnaire
ss: index soft skill (0-7)
mbti: dimension (EI/SN/TF/JP)
ml: lettre MBTI votée par les réponses hautes
sc: [A,B,C,D] score SS (2=fort, 1=moyen, 0=nul)
mp: [A,B,C,D] points MBTI
"""

QUESTIONS_ADULTE = [
    # ── COMMUNICATION (6 questions) ──────────────────────────────────────────
    {
        "n": 1, "ss": 0, "mbti": "JP", "ml": "J",
        "q": "En réunion, on vous demande soudainement de présenter vos idées devant des supérieurs sans préparation. Comment réagissez-vous ?",
        "opts": [
            "J'accepte spontanément et j'improvise avec aisance.",
            "Je prends quelques secondes pour structurer mes idées, puis je me lance.",
            "Je suggère de reporter à un moment où je pourrai mieux préparer.",
            "Je décline poliment car présenter sans préparation me stresse vraiment.",
        ],
        "sc": [2, 1, 0, 0], "mp": [2, 1, 0, 0],
    },
    {
        "n": 2, "ss": 0, "mbti": "EI", "ml": "E",
        "q": "Lorsque vous parlez, devez-vous souvent répéter ou reformuler vos phrases pour être bien compris ?",
        "opts": [
            "Non, je suis très clair, on me comprend du premier coup.",
            "Rarement, seulement dans des sujets complexes.",
            "Assez régulièrement, je dois souvent repréciser.",
            "Tout le temps, je dois souvent reprendre depuis le début.",
        ],
        "sc": [2, 1, 0, 0], "mp": [2, 1, 0, 0],
    },
    {
        "n": 3, "ss": 0, "mbti": "TF", "ml": "F",
        "q": "Quand on vous demande votre avis sur un sujet sensible qui pourrait blesser quelqu'un, vous avez tendance à :",
        "opts": [
            "Être direct et honnête, même si ça peut faire mal.",
            "Expliquer les faits objectivement, sans chercher à flatter.",
            "Mesurer vos mots pour ménager les susceptibilités.",
            "Bien choisir chaque mot pour que personne ne soit blessé.",
        ],
        "sc": [0, 0, 2, 1], "mp": [0, 0, 2, 1],
    },
    {
        "n": 4, "ss": 0, "mbti": "EI", "ml": "E",
        "q": "Vous trouvez un objet que vous vouliez depuis longtemps mais le prix est trop élevé. Que faites-vous ?",
        "opts": [
            "Vous négociez directement avec le vendeur pour trouver un accord gagnant-gagnant.",
            "Vous argumentez sur les défauts de l'objet pour justifier un prix plus bas.",
            "Vous cherchez ailleurs sans entrer dans une négociation.",
            "Vous attendez que le prix baisse ou d'avoir plus de budget.",
        ],
        "sc": [2, 1, 0, 0], "mp": [2, 1, 0, 0],
    },
    {
        "n": 5, "ss": 0, "mbti": "EI", "ml": "E",
        "q": "On vous demande de vous présenter devant une grande assemblée. Votre première réaction est :",
        "opts": [
            "Super, je suis pressé d'être sur scène !",
            "Ça ne me dérange pas, je vais le faire.",
            "Je n'aime pas trop ça, mais je vais quand même essayer.",
            "Ce n'est pas du tout mon truc, ça me stresse vraiment.",
        ],
        "sc": [2, 1, 0, 0], "mp": [2, 1, 0, 0],
    },
    {
        "n": 6, "ss": 0, "mbti": "EI", "ml": "E",
        "q": "Lorsque vous racontez une histoire ou le résumé d'un film à vos amis :",
        "opts": [
            "Les gens sont captivés et veulent en savoir plus.",
            "Vos interlocuteurs sont attentifs et suivent bien.",
            "Ils comprennent mais ont l'air de s'ennuyer un peu.",
            "Ils froncent les sourcils et semblent perdus.",
        ],
        "sc": [2, 1, 0, 0], "mp": [2, 1, 0, 0],
    },

    # ── ESPRIT CRITIQUE (6 questions) ────────────────────────────────────────
    {
        "n": 7, "ss": 1, "mbti": "SN", "ml": "S",
        "q": "Un nouveau logiciel révolutionnaire est mentionné entre collègues mais vous ne le connaissez pas. Que faites-vous ensuite ?",
        "opts": [
            "Je lis les articles et ouvrages les plus récents sur le sujet et vais aux conférences.",
            "Je pose des questions à mes collègues et envisage de m'informer davantage.",
            "Je n'y prête pas vraiment attention, si c'est important on me le dira.",
            "Je ne vois pas l'intérêt d'investir du temps là-dessus si ça ne m'apporte rien maintenant.",
        ],
        "sc": [2, 1, 0, 0], "mp": [2, 1, 0, 0],
    },
    {
        "n": 8, "ss": 1, "mbti": "SN", "ml": "S",
        "q": "Un ami partage une publication affirmant que les téléphones mobiles causent de graves problèmes de santé. Votre réaction ?",
        "opts": [
            "Je vérifie l'information en cherchant des sources fiables et des études scientifiques.",
            "Je lui demande où il a trouvé cette information avant de la croire.",
            "Je la partage sur mes réseaux sociaux pour alerter mes proches.",
            "J'arrête d'utiliser mon téléphone par précaution.",
        ],
        "sc": [2, 1, 0, 0], "mp": [2, 1, 0, 0],
    },
    {
        "n": 9, "ss": 1, "mbti": "JP", "ml": "P",
        "q": "Une nouvelle personne dans votre équipe affirme qu'une de vos méthodes de travail est obsolète. Votre réaction ?",
        "opts": [
            "Je l'envoie balader, elle devrait écouter avant de critiquer.",
            "Je ne change pas de méthode car elle a toujours fonctionné.",
            "Je me renseigne quand même sur les autres méthodes existantes.",
            "Par curiosité, je lui demande quelle méthode serait préférable selon elle.",
        ],
        "sc": [0, 0, 2, 1], "mp": [0, 0, 2, 1],
    },
    {
        "n": 10, "ss": 1, "mbti": "SN", "ml": "N",
        "q": "On vous demande de créer une histoire de toutes pièces. Que se passe-t-il ?",
        "opts": [
            "Je n'arrive pas à imaginer quoi que ce soit, je déteste cet exercice.",
            "J'ai besoin d'aide d'une personne plus imaginative que moi.",
            "J'arrive à imaginer une trame et quelques personnages assez vite.",
            "J'imagine immédiatement les lieux, l'époque, les personnages, leurs voix…",
        ],
        "sc": [0, 0, 2, 1], "mp": [0, 0, 2, 1],
    },
    {
        "n": 11, "ss": 1, "mbti": "SN", "ml": "S",
        "q": "Vous découvrez que votre destination de vacances est décrite comme dangereuse aux infos. Que faites-vous ?",
        "opts": [
            "Je me renseigne auprès de personnes qui y sont allées pour avoir un avis précis.",
            "Je contacte l'ambassade pour avoir des informations officielles.",
            "Je me fie au journal télévisé et change de destination.",
            "Je me fie à mon intuition pour décider.",
        ],
        "sc": [2, 1, 0, 0], "mp": [2, 1, 0, 0],
    },
    {
        "n": 12, "ss": 1, "mbti": "SN", "ml": "S",
        "q": "Vous devez monter un meuble complexe mais vous avez perdu la notice. Que faites-vous ?",
        "opts": [
            "Je contacte le constructeur pour qu'il me fournisse la notice.",
            "Je cherche des tutoriels vidéo sur internet.",
            "J'appelle un professionnel pour qu'il s'en charge.",
            "J'y vais à l'intuition et je m'adapte au fur et à mesure.",
        ],
        "sc": [2, 1, 0, 0], "mp": [2, 1, 0, 0],
    },

    # ── ÉTHIQUE (6 questions) ─────────────────────────────────────────────────
    {
        "n": 13, "ss": 2, "mbti": "TF", "ml": "T",
        "q": "Après avoir payé, vous réalisez que le caissier vous a rendu trop de monnaie. Comment réagissez-vous ?",
        "opts": [
            "Je signale immédiatement l'erreur et rends l'argent en trop.",
            "Je vérifie le montant et retourne à la caisse pour rectifier.",
            "Je garde l'argent, c'est une chance inattendue.",
            "Je garde l'argent, c'est le caissier qui a fait l'erreur.",
        ],
        "sc": [2, 1, 0, 0], "mp": [2, 1, 0, 0],
    },
    {
        "n": 14, "ss": 2, "mbti": "TF", "ml": "T",
        "q": "Vous devez finir un travail de groupe important demain. Votre meilleur ami vous appelle pour passer une dernière soirée avant de partir 6 mois. Que faites-vous ?",
        "opts": [
            "Vous terminez votre travail dans les délais, en gérant vos émotions.",
            "Vous faites une courte pause pour prendre des nouvelles, puis reprenez immédiatement.",
            "Vous lâchez tout pour rejoindre votre ami, l'amitié passe avant tout.",
            "Vous demandez aux autres membres de finir sans vous.",
        ],
        "sc": [2, 1, 0, 0], "mp": [2, 1, 0, 0],
    },
    {
        "n": 15, "ss": 2, "mbti": "TF", "ml": "T",
        "q": "Votre groupe de travail ne fonctionne pas du tout. Votre réaction ?",
        "opts": [
            "Vous restez et cherchez à remotiver le groupe pour améliorer la performance collective.",
            "Vous restez fidèle et compensez leur manque en travaillant davantage.",
            "Vous quittez le groupe pour en rejoindre un plus performant.",
            "Vous préférez travailler seul pour être sûr que le travail soit bien fait.",
        ],
        "sc": [2, 1, 0, 0], "mp": [2, 1, 0, 0],
    },
    {
        "n": 16, "ss": 2, "mbti": "TF", "ml": "F",
        "q": "En jouant au foot, vous brisez une fenêtre. Tous vos amis s'enfuient. Votre réaction ?",
        "opts": [
            "Vous vous enfuyez aussi, pas vu pas pris.",
            "Vous faites comme si vous ne jouiez pas et désignez les autres.",
            "Vous attendez pour vous dénoncer et assumer la sanction.",
            "Vous allez immédiatement frapper à la porte pour vous excuser et réparer.",
        ],
        "sc": [0, 0, 2, 1], "mp": [0, 0, 2, 1],
    },
    {
        "n": 17, "ss": 2, "mbti": "TF", "ml": "T",
        "q": "Vous pouvez acheter une voiture. Laquelle choisissez-vous ?",
        "opts": [
            "Un vélo ou trottinette électrique, le moins polluant possible.",
            "Une voiture 100% électrique pour réduire mon impact environnemental.",
            "Une voiture simple, fiable et durable qui correspond à mes besoins.",
            "Une grosse voiture à essence puissante, le plaisir de conduire d'abord.",
        ],
        "sc": [2, 1, 0, 0], "mp": [2, 1, 0, 0],
    },
    {
        "n": 18, "ss": 2, "mbti": "TF", "ml": "T",
        "q": "Pourriez-vous prendre en considération une opinion qui bafoue vos principes ou votre culture ?",
        "opts": [
            "Oui, c'est tout à fait possible.",
            "Oui, ça ne me dérange pas vraiment.",
            "Non, je préfère éviter.",
            "Non, c'est tout à fait impossible.",
        ],
        "sc": [2, 1, 0, 0], "mp": [2, 1, 0, 0],
    },

    # ── INTEL. ÉMOTIONNELLE (6 questions) ────────────────────────────────────
    {
        "n": 19, "ss": 3, "mbti": "TF", "ml": "T",
        "q": "Vous avez travaillé 3 mois sur un dossier complexe. Un inconnu le qualifie de déplorable. Votre réaction ?",
        "opts": [
            "Vous notez ses commentaires pour comprendre ce qui ne va pas.",
            "Ça vous énerve mais vous écoutez car aucun travail n'est parfait.",
            "Vous l'ignorez, cette personne vous veut du mal.",
            "Vous l'envoyez balader, il ne sait pas le travail que vous avez fourni.",
        ],
        "sc": [2, 1, 0, 0], "mp": [2, 1, 0, 0],
    },
    {
        "n": 20, "ss": 3, "mbti": "TF", "ml": "F",
        "q": "Si on vous demande de citer vos qualités et vos défauts, y arrivez-vous facilement ?",
        "opts": [
            "Non, je n'y arrive jamais.",
            "En général, j'ai besoin qu'on m'aide.",
            "Plutôt oui, j'y arrive.",
            "Oui, très facilement et précisément.",
        ],
        "sc": [0, 0, 2, 1], "mp": [0, 0, 2, 1],
    },
    {
        "n": 21, "ss": 3, "mbti": "EI", "ml": "E",
        "q": "Un acteur oublie son texte sur scène et c'est le silence gêné. Que ressentez-vous ?",
        "opts": [
            "Une forte gêne et l'envie de l'aider en applaudissant ou soufflant son texte.",
            "Vous vous sentez mal à l'aise, comme si vous étiez à sa place.",
            "Vous trouvez ça comique et ça vous fait sourire.",
            "Vous êtes déçu par sa prestation, c'est peu professionnel.",
        ],
        "sc": [2, 1, 0, 0], "mp": [2, 1, 0, 0],
    },
    {
        "n": 22, "ss": 3, "mbti": "EI", "ml": "E",
        "q": "On vous offre l'opportunité de diriger un projet important. Votre réaction ?",
        "opts": [
            "Vous êtes excité et confiant dans votre capacité à diriger.",
            "Vous ressentez une certaine pression mais êtes prêt à assumer.",
            "Vous êtes inquiet de ne pas être à la hauteur, vous hésitez.",
            "Vous envisagez de décliner par peur de l'échec.",
        ],
        "sc": [2, 1, 0, 0], "mp": [2, 1, 0, 0],
    },
    {
        "n": 23, "ss": 3, "mbti": "JP", "ml": "P",
        "q": "Une heure avant une présentation importante, votre ordinateur plante et vous perdez tout. Que faites-vous ?",
        "opts": [
            "Vous déprimez et perdez vos moyens, les larmes aux yeux.",
            "Vous cherchez à annuler la présentation.",
            "Vous respirez et tentez de reproduire la présentation de mémoire.",
            "Vous y allez au talent, ça passe ou ça casse.",
        ],
        "sc": [0, 0, 2, 1], "mp": [0, 0, 2, 1],
    },
    {
        "n": 24, "ss": 3, "mbti": "TF", "ml": "F",
        "q": "Vous apprenez que la femme d'un voisin peu proche vient d'être hospitalisée gravement. Vous êtes du genre à :",
        "opts": [
            "Ne rien ressentir car vous n'êtes pas proche de ce voisin.",
            "Ne pas vous mêler de ce qui ne vous regarde pas.",
            "Vouloir pleurer en voyant votre voisin triste et désespéré.",
            "Vouloir l'aider et le réconforter malgré le peu d'affinités.",
        ],
        "sc": [0, 0, 2, 1], "mp": [0, 0, 2, 1],
    },

    # ── INTEL. SOCIALE (6 questions) ─────────────────────────────────────────
    {
        "n": 25, "ss": 4, "mbti": "EI", "ml": "E",
        "q": "Vous êtes le seul à avoir bien noté les infos d'un examen important. Que faites-vous ?",
        "opts": [
            "Vous les partagez immédiatement avec tous sans distinction.",
            "Vous les partagez en priorité avec ceux qui ont des difficultés.",
            "Vous les partagez avec ceux qui pourraient vous apporter quelque chose en retour.",
            "Vous gardez l'information pour vous pour avoir un avantage.",
        ],
        "sc": [2, 1, 0, 0], "mp": [2, 1, 0, 0],
    },
    {
        "n": 26, "ss": 4, "mbti": "EI", "ml": "E",
        "q": "On vous impose un travail en groupe alors que vous préféreriez travailler seul. Votre réaction ?",
        "opts": [
            "Vous êtes heureux de travailler à plusieurs, c'est plus riche.",
            "Vous êtes pressé de connaître vos collaborateurs.",
            "Vous le faites mais uniquement parce que vous n'avez pas le choix.",
            "Cette idée vous fatigue déjà, vous détestez les travaux de groupe.",
        ],
        "sc": [2, 1, 0, 0], "mp": [2, 1, 0, 0],
    },
    {
        "n": 27, "ss": 4, "mbti": "EI", "ml": "E",
        "q": "En vacances à l'étranger, vous seriez plutôt :",
        "opts": [
            "Quelqu'un qui apprend la langue locale, essaie les coutumes et vêtements.",
            "Quelqu'un qui veut dormir chez l'habitant et visiter les lieux historiques.",
            "Quelqu'un qui préfère les restaurants internationaux à la cuisine locale.",
            "Quelqu'un qui reste à l'hôtel pour profiter du calme et de la piscine.",
        ],
        "sc": [2, 1, 0, 0], "mp": [2, 1, 0, 0],
    },
    {
        "n": 28, "ss": 4, "mbti": "EI", "ml": "E",
        "q": "Avez-vous une facilité à collaborer avec des personnes avec qui vous n'avez aucune affinité ?",
        "opts": [
            "Oui, je m'adapte à n'importe quel profil efficacement.",
            "Oui, tant qu'on se respecte mutuellement.",
            "Pas vraiment, il me faut un minimum de points communs.",
            "Non, j'ai besoin d'apprécier les personnes pour être efficace.",
        ],
        "sc": [2, 1, 0, 0], "mp": [2, 1, 0, 0],
    },
    {
        "n": 29, "ss": 4, "mbti": "EI", "ml": "E",
        "q": "Aimez-vous nouer des liens avec les gens et entretenir les relations sur le long terme ?",
        "opts": [
            "Oui carrément, j'adore ça et je le fais très bien.",
            "Plutôt oui, mais je ne suis pas encore expert.",
            "Non pas du tout, je préfère avoir un petit cercle proche.",
            "Non, je préfère être seul.",
        ],
        "sc": [2, 1, 0, 0], "mp": [2, 1, 0, 0],
    },
    {
        "n": 30, "ss": 4, "mbti": "EI", "ml": "E",
        "q": "En soirée ou anniversaire, vous êtes du genre à :",
        "opts": [
            "Aller parler à tout le monde car vous voulez savoir qui est qui.",
            "Lancer des conversations même si vous n'y êtes pas obligé.",
            "Chercher un moyen de vous échapper pour éviter de parler.",
            "Faire tout pour ne pas y aller.",
        ],
        "sc": [2, 1, 0, 0], "mp": [2, 1, 0, 0],
    },

    # ── MGMT DE PROJET (6 questions) ─────────────────────────────────────────
    {
        "n": 31, "ss": 5, "mbti": "JP", "ml": "J",
        "q": "On vous confie un projet sans instructions détaillées. Comment procédez-vous ?",
        "opts": [
            "Je me fixe mes propres objectifs, j'organise mon travail de façon autonome.",
            "Je recherche des tutoriels et articles pour trouver la meilleure approche.",
            "Je préfère me faire accompagner par un expert pour être sûr du résultat.",
            "Je demande de l'aide à des amis ou collègues qui s'y connaissent mieux.",
        ],
        "sc": [2, 1, 0, 0], "mp": [2, 1, 0, 0],
    },
    {
        "n": 32, "ss": 5, "mbti": "TF", "ml": "T",
        "q": "Vous voulez apprendre une nouvelle langue cette année. Comment planifiez-vous ce projet ?",
        "opts": [
            "Je planifie X heures par semaine et fixe des jalons (bases en 3 mois, etc.).",
            "Je m'inscris à un cours en ligne avec des objectifs clairs et un rythme régulier.",
            "J'achète des livres et applis, sans plan précis sur quand les utiliser.",
            "J'apprendrai quand j'aurai du temps libre, sans objectif ni calendrier.",
        ],
        "sc": [2, 1, 0, 0], "mp": [2, 1, 0, 0],
    },
    {
        "n": 33, "ss": 5, "mbti": "TF", "ml": "T",
        "q": "Lors de la mise en place d'un projet, que faut-il prendre en compte en premier lieu ?",
        "opts": [
            "Les événements qui pourraient annuler le projet.",
            "Avoir un plan de secours pour chaque imprévu.",
            "Que la qualité soit au rendez-vous.",
            "L'avis des participants, car l'essentiel c'est qu'ils soient satisfaits.",
        ],
        "sc": [2, 1, 0, 0], "mp": [2, 1, 0, 0],
    },
    {
        "n": 34, "ss": 5, "mbti": "TF", "ml": "T",
        "q": "Il reste 3 mois à vivre à une personne que vous aimez. Un médecin propose une opération risquée : réussite = 10 ans de vie, échec = mort. Que faites-vous ?",
        "opts": [
            "Je lis toutes les études disponibles, évalue les risques et prends une décision éclairée.",
            "Je décide de tenter l'opération car face à l'urgence, il faut agir.",
            "Je réunis les proches pour décider collectivement.",
            "Je ne parviens pas à prendre de décision, l'enjeu est trop lourd.",
        ],
        "sc": [2, 1, 0, 0], "mp": [2, 1, 0, 0],
    },
    {
        "n": 35, "ss": 5, "mbti": "JP", "ml": "J",
        "q": "Dans un travail de groupe, ce que vous préférez faire, c'est :",
        "opts": [
            "Établir des outils pour contrôler l'avancée du travail.",
            "Vérifier au fur et à mesure que les tâches ont bien été réalisées.",
            "Terminer vite, puis corriger la qualité globalement.",
            "Faire d'abord les tâches qui vous plaisent le plus.",
        ],
        "sc": [2, 1, 0, 0], "mp": [2, 1, 0, 0],
    },
    {
        "n": 36, "ss": 5, "mbti": "JP", "ml": "P",
        "q": "En plein jeu de société, toutes les règles changent d'un coup. Comment réagissez-vous ?",
        "opts": [
            "J'arrête de jouer, on ne change pas les règles en cours de partie.",
            "Je suis perturbé et énervé, je ne sais pas quoi faire.",
            "Je lis les nouvelles règles et essaie de gagner quand même.",
            "Je continue à jouer, ça pourra être amusant.",
        ],
        "sc": [0, 0, 2, 1], "mp": [0, 0, 2, 1],
    },

    # ── MGMT D'ÉQUIPE (6 questions) ───────────────────────────────────────────
    {
        "n": 37, "ss": 6, "mbti": "TF", "ml": "T",
        "q": "Comment pensez-vous que les richesses du monde devraient être réparties ?",
        "opts": [
            "Les pays riches devraient aider les pays pauvres.",
            "Tout le monde devrait avoir assez pour vivre correctement.",
            "La répartition actuelle reflète la compétence individuelle, pas besoin de changer.",
            "La redistribution n'est pas nécessaire, chacun mérite ce qu'il a gagné.",
        ],
        "sc": [2, 1, 0, 0], "mp": [2, 1, 0, 0],
    },
    {
        "n": 38, "ss": 6, "mbti": "TF", "ml": "T",
        "q": "Deux personnes que vous connaissez sont en conflit. Vous avez tendance à :",
        "opts": [
            "Chercher l'origine du conflit, comprendre les deux points de vue et proposer une solution.",
            "Mettre en place une médiation pour que les deux parties s'expriment calmement.",
            "Préférer ne pas intervenir par peur des répercussions.",
            "Ne pas vous impliquer, de peur d'aggraver la situation.",
        ],
        "sc": [2, 1, 0, 0], "mp": [2, 1, 0, 0],
    },
    {
        "n": 39, "ss": 6, "mbti": "EI", "ml": "E",
        "q": "En soirée, vous remarquez qu'un invité est seul dans son coin. Que faites-vous ?",
        "opts": [
            "Vous allez le chercher pour l'intégrer à votre groupe de discussion.",
            "Vous allez lui parler pour qu'il se sente moins seul.",
            "Vous le laissez tranquille, il se fera des amis par lui-même.",
            "Vous faites comme si vous ne l'aviez pas vu.",
        ],
        "sc": [2, 1, 0, 0], "mp": [2, 1, 0, 0],
    },
    {
        "n": 40, "ss": 6, "mbti": "JP", "ml": "P",
        "q": "Face à un travail qui nécessite une compétence que vous n'avez pas, allez-vous tenter de le réaliser quand même ?",
        "opts": [
            "Non, le travail sera mal réalisé.",
            "Non, sauf si un expert peut m'aider.",
            "Oui, je vais m'autoformer grâce à internet.",
            "Oui, je m'adapterai au fur et à mesure.",
        ],
        "sc": [0, 0, 2, 1], "mp": [0, 0, 2, 1],
    },
    {
        "n": 41, "ss": 6, "mbti": "EI", "ml": "E",
        "q": "Un membre de votre équipe a du mal à réaliser ses tâches. Que faites-vous ?",
        "opts": [
            "Je cherche à comprendre ses difficultés, puis je l'accompagne avec une formation adaptée.",
            "Je prends le temps de comprendre et lui prodigue des conseils ciblés.",
            "Je le laisse trouver les solutions par lui-même, c'est en cherchant qu'on apprend.",
            "Je prends en charge ses tâches moi-même pour éviter de perdre du temps.",
        ],
        "sc": [2, 1, 0, 0], "mp": [2, 1, 0, 0],
    },
    {
        "n": 42, "ss": 6, "mbti": "JP", "ml": "J",
        "q": "Dans un groupe de travail, vous êtes plutôt celui :",
        "opts": [
            "Qu'on laisse prendre la direction pour montrer la voie.",
            "Dont les idées sont écoutées et mises en oeuvre.",
            "Qui suit le plan rigoureusement pour que tout se passe bien.",
            "Qui écoute les autres sans s'imposer.",
        ],
        "sc": [2, 1, 0, 0], "mp": [2, 1, 0, 0],
    },

    # ── ORGANISATION (6 questions) ────────────────────────────────────────────
    {
        "n": 43, "ss": 7, "mbti": "JP", "ml": "J",
        "q": "Vous entendez parler d'un sujet intéressant non couvert par votre formation. Que faites-vous ?",
        "opts": [
            "Je recherche des cours en ligne, vidéos, articles pour m'autoformer.",
            "J'emprunte des livres et cherche des tutoriels pour approfondir.",
            "Je trouve ça intéressant mais ne vois pas l'intérêt d'en apprendre plus.",
            "C'est le rôle des enseignants d'enseigner, pas besoin d'explorer seul.",
        ],
        "sc": [2, 1, 0, 0], "mp": [2, 1, 0, 0],
    },
    {
        "n": 44, "ss": 7, "mbti": "JP", "ml": "J",
        "q": "Vous devez accomplir une tâche longue et répétitive. Comment maintenez-vous votre concentration ?",
        "opts": [
            "Je me fixe des petits objectifs et prends de courtes pauses régulières.",
            "J'alterne avec d'autres activités plus stimulantes pour rester alerte.",
            "Je me laisse souvent distraire, notamment par mon téléphone.",
            "J'ai tendance à procrastiner car je trouve ça trop ennuyeux.",
        ],
        "sc": [2, 1, 0, 0], "mp": [2, 1, 0, 0],
    },
    {
        "n": 45, "ss": 7, "mbti": "JP", "ml": "J",
        "q": "Vous devez rendre un travail dans plusieurs mois. Vous préférez :",
        "opts": [
            "Vous organiser pour travailler à un rythme régulier chaque jour.",
            "Identifier les tâches simples et les finir vite pour consacrer plus de temps aux autres.",
            "Travailler en fonction de votre motivation du moment.",
            "Attendre le dernier moment car c'est là que vous êtes le plus performant.",
        ],
        "sc": [2, 1, 0, 0], "mp": [2, 1, 0, 0],
    },
    {
        "n": 46, "ss": 7, "mbti": "JP", "ml": "J",
        "q": "Pour passer les meilleures vacances possibles, il vaut mieux :",
        "opts": [
            "Planifier chaque étape avec dates, lieux et budgets.",
            "Calculer les délais de chaque activité pour les enchaîner au bon moment.",
            "Surtout se reposer et se prélasser sans trop planifier.",
            "Improviser sur place car le spontané est plus amusant.",
        ],
        "sc": [2, 1, 0, 0], "mp": [2, 1, 0, 0],
    },
    {
        "n": 47, "ss": 7, "mbti": "SN", "ml": "S",
        "q": "Comment planifiez-vous vos actions avant un projet ou événement important ?",
        "opts": [
            "Je visualise clairement toutes les étapes dans ma tête.",
            "J'utilise des cartes mentales ou listes pour organiser mes pensées.",
            "Je me sens souvent dépassé et ne sais pas par où commencer.",
            "J'attends que les choses se présentent et je réagis au fur et à mesure.",
        ],
        "sc": [2, 1, 0, 0], "mp": [2, 1, 0, 0],
    },
    {
        "n": 48, "ss": 7, "mbti": "JP", "ml": "J",
        "q": "Vous avez rendez-vous avec quelqu'un de spécial. Vous êtes plutôt du genre à :",
        "opts": [
            "Arriver en avance pour ne pas le faire attendre.",
            "Arriver pile à l'heure.",
            "Arriver 5 minutes en retard pour ne pas paraître impatient.",
            "Arriver en retard car vous mettez beaucoup de temps à vous préparer.",
        ],
        "sc": [2, 1, 0, 0], "mp": [2, 1, 0, 0],
    },
]

SS_SECTION_NAMES = [
    "Communication",
    "Esprit critique",
    "Éthique",
    "Intelligence émotionnelle",
    "Intelligence sociale",
    "Management de projet",
    "Management d'équipe",
    "Organisation",
]


# ══════════════════════════════════════════════════════════════════════════════
# VERSION ÉLÈVE (tutoiement, contexte scolaire / lycée)
# Mêmes scores ss/mp/sc — seules les formulations changent
# ══════════════════════════════════════════════════════════════════════════════

QUESTIONS_ELEVE = [
    # ── COMMUNICATION (6 questions) ──────────────────────────────────────────
    {
        "n": 1, "ss": 0, "mbti": "JP", "ml": "J",
        "q": "En cours, ton prof te demande soudainement de présenter tes idées devant la classe sans préparation. Comment tu réagis ?",
        "opts": [
            "J'accepte spontanément et j'improvise avec aisance.",
            "Je prends quelques secondes pour structurer mes idées, puis je me lance.",
            "Je suggère de le faire plus tard pour mieux préparer.",
            "Je décline poliment car parler sans préparer me stresse vraiment.",
        ],
        "sc": [2, 1, 0, 0], "mp": [2, 1, 0, 0],
    },
    {
        "n": 2, "ss": 0, "mbti": "EI", "ml": "E",
        "q": "Quand tu parles, est-ce que tu dois souvent répéter ou reformuler pour être bien compris ?",
        "opts": [
            "Non, je suis très clair, on me comprend du premier coup.",
            "Rarement, seulement sur des sujets complexes.",
            "Assez souvent, je dois repréciser régulièrement.",
            "Tout le temps, je dois souvent reprendre depuis le début.",
        ],
        "sc": [2, 1, 0, 0], "mp": [2, 1, 0, 0],
    },
    {
        "n": 3, "ss": 0, "mbti": "TF", "ml": "F",
        "q": "Quand un ami te demande ton avis sur quelque chose de sensible qui pourrait le blesser, tu as tendance à :",
        "opts": [
            "Être direct et honnête, même si ça peut faire mal.",
            "Expliquer les faits objectivement, sans chercher à flatter.",
            "Choisir tes mots pour ménager les susceptibilités.",
            "Bien tourner chaque phrase pour que personne ne soit blessé.",
        ],
        "sc": [0, 0, 2, 1], "mp": [0, 0, 2, 1],
    },
    {
        "n": 4, "ss": 0, "mbti": "EI", "ml": "E",
        "q": "Tu trouves un objet que tu voulais depuis longtemps mais le prix est trop élevé. Que fais-tu ?",
        "opts": [
            "Tu négocies directement avec le vendeur pour trouver un accord.",
            "Tu argumentes sur les défauts de l'objet pour justifier un prix plus bas.",
            "Tu cherches ailleurs sans entrer dans une négociation.",
            "Tu attends que le prix baisse ou d'avoir plus d'argent.",
        ],
        "sc": [2, 1, 0, 0], "mp": [2, 1, 0, 0],
    },
    {
        "n": 5, "ss": 0, "mbti": "EI", "ml": "E",
        "q": "On te demande de te présenter devant toute l'école lors d'un événement. Ta première réaction c'est :",
        "opts": [
            "Super, j'ai hâte d'être sur scène !",
            "Ça ne me dérange pas, je vais le faire.",
            "Je n'aime pas trop ça, mais je vais quand même essayer.",
            "Ce n'est pas du tout mon truc, ça me stresse vraiment.",
        ],
        "sc": [2, 1, 0, 0], "mp": [2, 1, 0, 0],
    },
    {
        "n": 6, "ss": 0, "mbti": "EI", "ml": "E",
        "q": "Quand tu racontes une histoire ou le résumé d'un film à tes amis :",
        "opts": [
            "Ils sont captivés et veulent en savoir plus.",
            "Ils écoutent attentivement et suivent bien.",
            "Ils comprennent mais ont l'air de s'ennuyer un peu.",
            "Ils froncent les sourcils et semblent perdus.",
        ],
        "sc": [2, 1, 0, 0], "mp": [2, 1, 0, 0],
    },

    # ── ESPRIT CRITIQUE (6 questions) ────────────────────────────────────────
    {
        "n": 7, "ss": 1, "mbti": "SN", "ml": "S",
        "q": "Tes amis parlent d'une nouvelle appli ou tendance que tu ne connais pas. Que fais-tu ensuite ?",
        "opts": [
            "Je lis des articles, je regarde des vidéos et je creuse le sujet à fond.",
            "Je pose des questions à mes amis et j'envisage de m'informer davantage.",
            "Je n'y prête pas vraiment attention, si c'est important j'en entendrai parler.",
            "Je ne vois pas l'intérêt de m'y intéresser si ça ne me sert à rien maintenant.",
        ],
        "sc": [2, 1, 0, 0], "mp": [2, 1, 0, 0],
    },
    {
        "n": 8, "ss": 1, "mbti": "SN", "ml": "S",
        "q": "Un ami partage un post affirmant que les téléphones causent de graves maladies. Ta réaction ?",
        "opts": [
            "Je vérifie l'info en cherchant des sources fiables et des études scientifiques.",
            "Je lui demande où il a trouvé ça avant de le croire.",
            "Je le partage sur mes réseaux pour alerter mes proches.",
            "J'arrête d'utiliser mon téléphone par précaution.",
        ],
        "sc": [2, 1, 0, 0], "mp": [2, 1, 0, 0],
    },
    {
        "n": 9, "ss": 1, "mbti": "JP", "ml": "P",
        "q": "Un nouveau camarade dit que ta façon de travailler est dépassée. Ta réaction ?",
        "opts": [
            "Je l'envoie balader, il devrait observer avant de critiquer.",
            "Je ne change rien, ma méthode a toujours fonctionné.",
            "Je me renseigne quand même sur d'autres façons de faire.",
            "Par curiosité, je lui demande quelle méthode serait meilleure selon lui.",
        ],
        "sc": [0, 0, 2, 1], "mp": [0, 0, 2, 1],
    },
    {
        "n": 10, "ss": 1, "mbti": "SN", "ml": "N",
        "q": "On te demande d'inventer une histoire de toutes pièces. Que se passe-t-il ?",
        "opts": [
            "Je n'arrive pas à imaginer quoi que ce soit, je déteste cet exercice.",
            "J'ai besoin d'aide d'une personne plus imaginative que moi.",
            "J'arrive à imaginer une trame et quelques personnages assez vite.",
            "J'imagine immédiatement les lieux, l'époque, les personnages, leurs voix…",
        ],
        "sc": [0, 0, 2, 1], "mp": [0, 0, 2, 1],
    },
    {
        "n": 11, "ss": 1, "mbti": "SN", "ml": "S",
        "q": "Tu apprends que ta destination de vacances est décrite comme dangereuse aux infos. Que fais-tu ?",
        "opts": [
            "Je me renseigne auprès de personnes qui y sont allées pour avoir un avis précis.",
            "Je contacte un organisme officiel pour avoir des informations fiables.",
            "Je me fie aux infos et change de destination.",
            "Je me fie à mon intuition pour décider.",
        ],
        "sc": [2, 1, 0, 0], "mp": [2, 1, 0, 0],
    },
    {
        "n": 12, "ss": 1, "mbti": "SN", "ml": "S",
        "q": "Tu dois monter un meuble complexe mais tu as perdu la notice. Que fais-tu ?",
        "opts": [
            "Je contacte le fabricant pour qu'il me fournisse la notice.",
            "Je cherche des tutoriels vidéo sur internet.",
            "J'appelle quelqu'un de compétent pour qu'il s'en charge.",
            "J'y vais à l'intuition et je m'adapte au fur et à mesure.",
        ],
        "sc": [2, 1, 0, 0], "mp": [2, 1, 0, 0],
    },

    # ── ÉTHIQUE (6 questions) ─────────────────────────────────────────────────
    {
        "n": 13, "ss": 2, "mbti": "TF", "ml": "T",
        "q": "Après avoir payé, tu réalises que le caissier t'a rendu trop de monnaie. Comment tu réagis ?",
        "opts": [
            "Je signale immédiatement l'erreur et je rends l'argent en trop.",
            "Je vérifie le montant et retourne à la caisse pour rectifier.",
            "Je garde l'argent, c'est une chance inattendue.",
            "Je garde l'argent, c'est le caissier qui a fait l'erreur.",
        ],
        "sc": [2, 1, 0, 0], "mp": [2, 1, 0, 0],
    },
    {
        "n": 14, "ss": 2, "mbti": "TF", "ml": "T",
        "q": "Tu dois finir un devoir de groupe important pour demain. Ton meilleur ami t'appelle pour passer une dernière soirée avant de partir 6 mois. Que fais-tu ?",
        "opts": [
            "Tu termines ton travail dans les délais, en gérant tes émotions.",
            "Tu fais une courte pause pour lui parler, puis tu reprends immédiatement.",
            "Tu lâches tout pour rejoindre ton ami, l'amitié passe avant tout.",
            "Tu demandes aux autres membres du groupe de finir sans toi.",
        ],
        "sc": [2, 1, 0, 0], "mp": [2, 1, 0, 0],
    },
    {
        "n": 15, "ss": 2, "mbti": "TF", "ml": "T",
        "q": "Ton groupe de travail ne fonctionne pas du tout. Ta réaction ?",
        "opts": [
            "Tu restes et cherches à remotiver le groupe pour améliorer la situation.",
            "Tu restes fidèle et tu compenses leur manque en travaillant davantage.",
            "Tu quittes le groupe pour en rejoindre un plus efficace.",
            "Tu préfères travailler seul pour être sûr que le travail soit bien fait.",
        ],
        "sc": [2, 1, 0, 0], "mp": [2, 1, 0, 0],
    },
    {
        "n": 16, "ss": 2, "mbti": "TF", "ml": "F",
        "q": "En jouant au foot, tu brises une fenêtre. Tous tes amis s'enfuient. Ta réaction ?",
        "opts": [
            "Tu t'enfuis aussi, pas vu pas pris.",
            "Tu fais comme si tu ne jouais pas et tu désignes les autres.",
            "Tu attends pour te dénoncer et assumer la sanction.",
            "Tu vas immédiatement frapper à la porte pour t'excuser et proposer de réparer.",
        ],
        "sc": [0, 0, 2, 1], "mp": [0, 0, 2, 1],
    },
    {
        "n": 17, "ss": 2, "mbti": "TF", "ml": "T",
        "q": "Plus tard, quand tu pourras acheter un véhicule, lequel choisiras-tu ?",
        "opts": [
            "Un vélo ou une trottinette électrique, le moins polluant possible.",
            "Une voiture 100% électrique pour réduire mon impact environnemental.",
            "Une voiture simple, fiable et durable qui correspond à mes besoins.",
            "Une grosse voiture puissante, le plaisir de conduire d'abord.",
        ],
        "sc": [2, 1, 0, 0], "mp": [2, 1, 0, 0],
    },
    {
        "n": 18, "ss": 2, "mbti": "TF", "ml": "T",
        "q": "Est-ce que tu pourrais prendre en considération une opinion qui va à l'encontre de tes principes ou de ta culture ?",
        "opts": [
            "Oui, c'est tout à fait possible.",
            "Oui, ça ne me dérange pas vraiment.",
            "Non, je préfère éviter.",
            "Non, c'est tout à fait impossible.",
        ],
        "sc": [2, 1, 0, 0], "mp": [2, 1, 0, 0],
    },

    # ── INTEL. ÉMOTIONNELLE (6 questions) ────────────────────────────────────
    {
        "n": 19, "ss": 3, "mbti": "TF", "ml": "T",
        "q": "Tu as travaillé 3 semaines sur un exposé. Un camarade le qualifie de nul devant tout le monde. Ta réaction ?",
        "opts": [
            "Tu notes ses remarques pour comprendre ce qui ne va pas.",
            "Ça t'énerve mais tu écoutes car aucun travail n'est parfait.",
            "Tu l'ignores, cette personne te veut du mal.",
            "Tu l'envoies balader, il ne sait pas le travail que tu as fourni.",
        ],
        "sc": [2, 1, 0, 0], "mp": [2, 1, 0, 0],
    },
    {
        "n": 20, "ss": 3, "mbti": "TF", "ml": "F",
        "q": "Si on te demande de citer tes qualités et tes défauts, tu y arrives facilement ?",
        "opts": [
            "Non, je n'y arrive jamais.",
            "En général, j'ai besoin qu'on m'aide.",
            "Plutôt oui, j'y arrive.",
            "Oui, très facilement et précisément.",
        ],
        "sc": [0, 0, 2, 1], "mp": [0, 0, 2, 1],
    },
    {
        "n": 21, "ss": 3, "mbti": "EI", "ml": "E",
        "q": "Un camarade oublie son texte lors d'un exposé et c'est le silence gêné. Que ressens-tu ?",
        "opts": [
            "Une forte gêne et l'envie de l'aider en applaudissant ou en lui soufflant son texte.",
            "Tu te sens mal à l'aise, comme si tu étais à sa place.",
            "Tu trouves ça comique et ça te fait sourire.",
            "Tu es déçu par sa prestation, il aurait dû mieux préparer.",
        ],
        "sc": [2, 1, 0, 0], "mp": [2, 1, 0, 0],
    },
    {
        "n": 22, "ss": 3, "mbti": "EI", "ml": "E",
        "q": "On te propose d'être délégué de classe ou responsable d'un projet important. Ta réaction ?",
        "opts": [
            "Tu es enthousiaste et confiant dans ta capacité à assumer ce rôle.",
            "Tu ressens une certaine pression mais tu es prêt à te lancer.",
            "Tu es inquiet de ne pas être à la hauteur, tu hésites.",
            "Tu envisages de décliner par peur de l'échec.",
        ],
        "sc": [2, 1, 0, 0], "mp": [2, 1, 0, 0],
    },
    {
        "n": 23, "ss": 3, "mbti": "JP", "ml": "P",
        "q": "Une heure avant un exposé important, ton ordinateur plante et tu perds tout. Que fais-tu ?",
        "opts": [
            "Tu déprimes et tu perds tes moyens, les larmes aux yeux.",
            "Tu cherches à annuler ou reporter l'exposé.",
            "Tu respires et tu essaies de reproduire le travail de mémoire.",
            "Tu y vas au talent, ça passe ou ça casse.",
        ],
        "sc": [0, 0, 2, 1], "mp": [0, 0, 2, 1],
    },
    {
        "n": 24, "ss": 3, "mbti": "TF", "ml": "F",
        "q": "Tu apprends qu'un voisin que tu connais à peine traverse une période très difficile. Tu es plutôt du genre à :",
        "opts": [
            "Ne rien ressentir car tu n'es pas proche de cette personne.",
            "Ne pas te mêler de ce qui ne te regarde pas.",
            "Vouloir pleurer en le voyant triste et désespéré.",
            "Vouloir l'aider et le réconforter malgré le peu d'affinités.",
        ],
        "sc": [0, 0, 2, 1], "mp": [0, 0, 2, 1],
    },

    # ── INTEL. SOCIALE (6 questions) ─────────────────────────────────────────
    {
        "n": 25, "ss": 4, "mbti": "EI", "ml": "E",
        "q": "Tu es le seul à avoir bien noté les informations pour un contrôle important. Que fais-tu ?",
        "opts": [
            "Tu les partages immédiatement avec tout le monde sans distinction.",
            "Tu les partages en priorité avec ceux qui ont des difficultés.",
            "Tu les partages avec ceux qui pourraient t'apporter quelque chose en retour.",
            "Tu gardes l'information pour toi pour avoir un avantage.",
        ],
        "sc": [2, 1, 0, 0], "mp": [2, 1, 0, 0],
    },
    {
        "n": 26, "ss": 4, "mbti": "EI", "ml": "E",
        "q": "On t'impose un travail en groupe alors que tu préférerais travailler seul. Ta réaction ?",
        "opts": [
            "Tu es content de travailler à plusieurs, c'est plus riche.",
            "Tu es pressé de connaître tes camarades.",
            "Tu le fais mais uniquement parce que tu n'as pas le choix.",
            "Cette idée te fatigue déjà, tu détestes les travaux de groupe.",
        ],
        "sc": [2, 1, 0, 0], "mp": [2, 1, 0, 0],
    },
    {
        "n": 27, "ss": 4, "mbti": "EI", "ml": "E",
        "q": "En voyage à l'étranger, tu serais plutôt :",
        "opts": [
            "Quelqu'un qui apprend la langue locale, essaie les coutumes et vêtements.",
            "Quelqu'un qui veut dormir chez l'habitant et visiter les lieux historiques.",
            "Quelqu'un qui préfère les restaurants internationaux à la cuisine locale.",
            "Quelqu'un qui reste à l'hôtel pour profiter du calme et de la piscine.",
        ],
        "sc": [2, 1, 0, 0], "mp": [2, 1, 0, 0],
    },
    {
        "n": 28, "ss": 4, "mbti": "EI", "ml": "E",
        "q": "Est-ce que tu arrives facilement à travailler avec des gens avec qui tu n'as aucune affinité ?",
        "opts": [
            "Oui, je m'adapte à n'importe quel profil efficacement.",
            "Oui, tant qu'on se respecte mutuellement.",
            "Pas vraiment, il me faut un minimum de points communs.",
            "Non, j'ai besoin d'apprécier les gens pour être efficace.",
        ],
        "sc": [2, 1, 0, 0], "mp": [2, 1, 0, 0],
    },
    {
        "n": 29, "ss": 4, "mbti": "EI", "ml": "E",
        "q": "Est-ce que tu aimes nouer des liens avec les gens et entretenir les amitiés sur le long terme ?",
        "opts": [
            "Oui carrément, j'adore ça et je le fais très bien.",
            "Plutôt oui, mais je ne suis pas encore très doué.",
            "Pas vraiment, je préfère avoir un petit cercle proche.",
            "Non, je préfère être seul.",
        ],
        "sc": [2, 1, 0, 0], "mp": [2, 1, 0, 0],
    },
    {
        "n": 30, "ss": 4, "mbti": "EI", "ml": "E",
        "q": "En soirée ou en fête entre amis, tu es plutôt du genre à :",
        "opts": [
            "Aller parler à tout le monde car tu veux savoir qui est qui.",
            "Lancer des conversations même si tu n'y es pas obligé.",
            "Chercher un moyen de t'éclipser pour éviter de parler.",
            "Faire tout pour ne pas y aller.",
        ],
        "sc": [2, 1, 0, 0], "mp": [2, 1, 0, 0],
    },

    # ── MGMT DE PROJET (6 questions) ─────────────────────────────────────────
    {
        "n": 31, "ss": 5, "mbti": "JP", "ml": "J",
        "q": "On te confie un projet scolaire sans instructions détaillées. Comment tu procèdes ?",
        "opts": [
            "Je me fixe mes propres objectifs et j'organise mon travail de façon autonome.",
            "Je cherche des tutoriels et des exemples pour trouver la meilleure approche.",
            "Je préfère me faire accompagner par mon prof pour être sûr du résultat.",
            "Je demande de l'aide à des camarades qui s'y connaissent mieux.",
        ],
        "sc": [2, 1, 0, 0], "mp": [2, 1, 0, 0],
    },
    {
        "n": 32, "ss": 5, "mbti": "TF", "ml": "T",
        "q": "Tu veux apprendre une nouvelle langue pendant les vacances. Comment tu planifies ça ?",
        "opts": [
            "Je planifie X heures par semaine et je fixe des objectifs clairs.",
            "Je m'inscris à une appli ou un cours en ligne avec un rythme régulier.",
            "J'achète des livres et applis, sans plan précis sur quand les utiliser.",
            "J'apprendrai quand j'aurai du temps libre, sans objectif ni calendrier.",
        ],
        "sc": [2, 1, 0, 0], "mp": [2, 1, 0, 0],
    },
    {
        "n": 33, "ss": 5, "mbti": "TF", "ml": "T",
        "q": "Quand tu organises un projet ou un événement avec des amis, qu'est-ce que tu prends en compte en premier ?",
        "opts": [
            "Les choses qui pourraient faire rater le projet.",
            "Avoir un plan B pour chaque imprévu.",
            "Que tout soit de bonne qualité.",
            "L'avis de tout le monde, car l'essentiel c'est que tout le monde soit content.",
        ],
        "sc": [2, 1, 0, 0], "mp": [2, 1, 0, 0],
    },
    {
        "n": 34, "ss": 5, "mbti": "TF", "ml": "T",
        "q": "Il reste 3 mois à vivre à quelqu'un que tu aimes. Un médecin propose une opération risquée : réussite = 10 ans de vie, échec = mort immédiate. Que fais-tu ?",
        "opts": [
            "Je lis toutes les études disponibles, j'évalue les risques et je prends une décision éclairée.",
            "Je décide de tenter l'opération car face à l'urgence, il faut agir.",
            "Je réunis la famille pour décider collectivement.",
            "Je n'arrive pas à prendre de décision, l'enjeu est trop lourd.",
        ],
        "sc": [2, 1, 0, 0], "mp": [2, 1, 0, 0],
    },
    {
        "n": 35, "ss": 5, "mbti": "JP", "ml": "J",
        "q": "Dans un travail de groupe, ce que tu préfères faire, c'est :",
        "opts": [
            "Créer des outils pour suivre l'avancée du travail.",
            "Vérifier au fur et à mesure que les tâches ont bien été réalisées.",
            "Finir vite, puis corriger la qualité globalement.",
            "Faire d'abord les tâches qui te plaisent le plus.",
        ],
        "sc": [2, 1, 0, 0], "mp": [2, 1, 0, 0],
    },
    {
        "n": 36, "ss": 5, "mbti": "JP", "ml": "P",
        "q": "En plein jeu de société, toutes les règles changent d'un coup. Comment tu réagis ?",
        "opts": [
            "J'arrête de jouer, on ne change pas les règles en cours de partie.",
            "Je suis perturbé et énervé, je ne sais pas quoi faire.",
            "Je lis les nouvelles règles et j'essaie de gagner quand même.",
            "Je continue à jouer, ça peut être amusant.",
        ],
        "sc": [0, 0, 2, 1], "mp": [0, 0, 2, 1],
    },

    # ── MGMT D'ÉQUIPE (6 questions) ───────────────────────────────────────────
    {
        "n": 37, "ss": 6, "mbti": "TF", "ml": "T",
        "q": "Selon toi, comment les richesses du monde devraient-elles être réparties ?",
        "opts": [
            "Les pays riches devraient aider les pays pauvres.",
            "Tout le monde devrait avoir assez pour vivre correctement.",
            "La répartition actuelle reflète le mérite individuel, pas besoin de changer.",
            "La redistribution n'est pas nécessaire, chacun mérite ce qu'il a gagné.",
        ],
        "sc": [2, 1, 0, 0], "mp": [2, 1, 0, 0],
    },
    {
        "n": 38, "ss": 6, "mbti": "TF", "ml": "T",
        "q": "Deux amis que tu connais sont en conflit. Tu as tendance à :",
        "opts": [
            "Chercher l'origine du conflit, comprendre les deux points de vue et proposer une solution.",
            "Organiser une discussion pour que les deux s'expriment calmement.",
            "Préférer ne pas intervenir par peur des répercussions.",
            "Ne pas t'impliquer, de peur d'aggraver la situation.",
        ],
        "sc": [2, 1, 0, 0], "mp": [2, 1, 0, 0],
    },
    {
        "n": 39, "ss": 6, "mbti": "EI", "ml": "E",
        "q": "En cours ou en soirée, tu remarques qu'un camarade est seul dans son coin. Que fais-tu ?",
        "opts": [
            "Tu vas le chercher pour l'intégrer à votre groupe.",
            "Tu vas lui parler pour qu'il se sente moins seul.",
            "Tu le laisses tranquille, il se fera des amis par lui-même.",
            "Tu fais comme si tu ne l'avais pas vu.",
        ],
        "sc": [2, 1, 0, 0], "mp": [2, 1, 0, 0],
    },
    {
        "n": 40, "ss": 6, "mbti": "JP", "ml": "P",
        "q": "Face à un devoir qui nécessite une compétence que tu n'as pas encore, vas-tu quand même tenter de le faire ?",
        "opts": [
            "Non, le travail sera mal réalisé.",
            "Non, sauf si quelqu'un de compétent peut m'aider.",
            "Oui, je vais m'autoformer grâce à internet.",
            "Oui, je m'adapterai au fur et à mesure.",
        ],
        "sc": [0, 0, 2, 1], "mp": [0, 0, 2, 1],
    },
    {
        "n": 41, "ss": 6, "mbti": "EI", "ml": "E",
        "q": "Un camarade de groupe a du mal à réaliser sa partie du travail. Que fais-tu ?",
        "opts": [
            "Je cherche à comprendre ses difficultés, puis je l'accompagne avec des conseils adaptés.",
            "Je prends le temps de comprendre et lui donne des conseils ciblés.",
            "Je le laisse trouver les solutions par lui-même, c'est en cherchant qu'on apprend.",
            "Je prends en charge sa partie moi-même pour éviter de perdre du temps.",
        ],
        "sc": [2, 1, 0, 0], "mp": [2, 1, 0, 0],
    },
    {
        "n": 42, "ss": 6, "mbti": "JP", "ml": "J",
        "q": "Dans un groupe de travail, tu es plutôt celui :",
        "opts": [
            "Qu'on laisse prendre les décisions pour montrer la voie.",
            "Dont les idées sont écoutées et mises en pratique.",
            "Qui suit le plan rigoureusement pour que tout se passe bien.",
            "Qui écoute les autres sans s'imposer.",
        ],
        "sc": [2, 1, 0, 0], "mp": [2, 1, 0, 0],
    },

    # ── ORGANISATION (6 questions) ────────────────────────────────────────────
    {
        "n": 43, "ss": 7, "mbti": "JP", "ml": "J",
        "q": "Tu entends parler d'un sujet intéressant qui n'est pas au programme. Que fais-tu ?",
        "opts": [
            "Je recherche des vidéos, articles et cours en ligne pour me former.",
            "J'emprunte des livres et cherche des tutoriels pour approfondir.",
            "Je trouve ça intéressant mais je ne vois pas l'intérêt d'en apprendre plus.",
            "C'est le rôle des profs d'enseigner, pas besoin d'explorer seul.",
        ],
        "sc": [2, 1, 0, 0], "mp": [2, 1, 0, 0],
    },
    {
        "n": 44, "ss": 7, "mbti": "JP", "ml": "J",
        "q": "Tu dois faire un devoir long et répétitif. Comment tu maintiens ta concentration ?",
        "opts": [
            "Je me fixe des petits objectifs et prends de courtes pauses régulières.",
            "J'alterne avec d'autres activités plus stimulantes pour rester alerte.",
            "Je me laisse souvent distraire, notamment par mon téléphone.",
            "J'ai tendance à procrastiner car je trouve ça trop ennuyeux.",
        ],
        "sc": [2, 1, 0, 0], "mp": [2, 1, 0, 0],
    },
    {
        "n": 45, "ss": 7, "mbti": "JP", "ml": "J",
        "q": "Tu dois rendre un grand projet dans plusieurs semaines. Tu préfères :",
        "opts": [
            "T'organiser pour travailler à un rythme régulier chaque jour.",
            "Identifier les tâches simples et les finir vite pour consacrer plus de temps aux autres.",
            "Travailler selon ta motivation du moment.",
            "Attendre le dernier moment car c'est là que tu es le plus efficace.",
        ],
        "sc": [2, 1, 0, 0], "mp": [2, 1, 0, 0],
    },
    {
        "n": 46, "ss": 7, "mbti": "JP", "ml": "J",
        "q": "Pour passer les meilleures vacances possibles, il vaut mieux :",
        "opts": [
            "Planifier chaque étape avec dates, lieux et budgets.",
            "Calculer les délais de chaque activité pour les enchaîner au bon moment.",
            "Surtout se reposer et se prélasser sans trop planifier.",
            "Improviser sur place car le spontané est plus amusant.",
        ],
        "sc": [2, 1, 0, 0], "mp": [2, 1, 0, 0],
    },
    {
        "n": 47, "ss": 7, "mbti": "SN", "ml": "S",
        "q": "Comment tu t'organises avant un contrôle ou un événement important ?",
        "opts": [
            "Je visualise clairement toutes les étapes dans ma tête.",
            "J'utilise des listes ou des cartes mentales pour organiser mes révisions.",
            "Je me sens souvent dépassé et je ne sais pas par où commencer.",
            "J'attends que ça vienne et je réagis au fur et à mesure.",
        ],
        "sc": [2, 1, 0, 0], "mp": [2, 1, 0, 0],
    },
    {
        "n": 48, "ss": 7, "mbti": "JP", "ml": "J",
        "q": "Tu as rendez-vous avec quelqu'un d'important pour toi. Tu es plutôt du genre à :",
        "opts": [
            "Arriver en avance pour ne pas le faire attendre.",
            "Arriver pile à l'heure.",
            "Arriver 5 minutes en retard pour ne pas paraître impatient.",
            "Arriver en retard car tu mets beaucoup de temps à te préparer.",
        ],
        "sc": [2, 1, 0, 0], "mp": [2, 1, 0, 0],
    },
]


# ══════════════════════════════════════════════════════════════════════════════
# ALIAS PAR DÉFAUT (compatibilité avec les imports existants)
# ══════════════════════════════════════════════════════════════════════════════
QUESTIONS = QUESTIONS_ADULTE
