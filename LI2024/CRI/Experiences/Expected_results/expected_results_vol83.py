expected = {
    1: [],
    35: ["Rhizina inflata", "Rhizina inflata"],
    36: [],
    60: ["Macrorhinus elephantinus", "Canis jubatus",
         "Bradypus tridactylus"],
    64: [],
    # beaucoup de questions sur ce que je dois mettre pour celui-ci
    80: ["Homarus americanus", "Pinnotheres pisum",
         "Birgus latro", "Nephrops norvegicus",
         "Limnoria ‘ lignorium",
         "Limnoria ef des Chelura", "Leander serra",
         "Crangon vulgar is", "Pandalus borealis"],
    81: ["Cancer pagurus", "Carcinus moœnas",
         "Portunus puber", "Callinectes sapidus",
         "Eupagurus Bernhardus", "Balanus psittacus",
         "Pollicipes cornucopiæ", "Pinnotheres pisum",
         "Asellus aquaticus", "Limnoria lignorium",
         "Chelura terebrans"],
    83: [],
    92: ["Catarrhactes chrysolophus", "Pygoscelis antarctica",
         "P, Adeliæ", "Catarrhactes chrysolophus",
         "Aptenodytes Forsteri", "P.papua",
         "Catarrhacteschrysolophus", "Pygoscelis antarctica",
         "P ygoscelis papua", "Pygoscelis Adeliæ"],
    95: [],
    101: ["Chr ysanthemum leucanthemum", "Pulicaria vulqaris",
          "Pyrethrum carneum", "P. roseum", "Pyrethrum roseum"],
    102: [],
    # abréviation grandement non standard
    103: ["Phyteuma Villarsi", "Phyt. Charmelii", ],
    105: [],
    106: ["Culex fatigans", "Stegomya fasciata",
          ],
    109: [],
    116: ["Desoria glacialis", "Polytrichum formosum",
          "Polytrichum for mosum", "Pellia epiphylla",
          "Polytrichum formosum", "Polytrichum formosum"],
    118: [],
    120: ["Palinurus regius", "Temnodon sallator",
          "Dentiex macro phthalmus", "Dentex maroccanus",
          "Temnodon Sallaior", "Beryx decadactylus",
          "Berg decadactylus"],
    122: [],
    124: ["Pices berg", "Picea esvention",
          "Betula nana", "Coronella austriaca",
          "Cypripedium calceolus", "Ophrys muscifera",
          "Eryngium maritimum"],
    127: [],
    136: ["Carex stricta", "Carex stricta",
          "Phragmites comcelle", "Typha angustifolia",
          "Juncus obtusiflorus", "Scirpus lacustris",
          "Carex stricta", "Carex riparia",
          # il manque des fins de noms souvent quand ils sont coupés
          "Scirpus lacustris", "Scirpus lacus",
          "Scirpus lacustris", "Carex .stricta"],
    139: [],
    164: ["Grampus griseus", "Grampus griseus"],
    166: [],
    169: ["Mirabilis Jalappa", "Mirabilis jalappa"],
    172: [],
    176: ["Amanita phalloides",  # , mappa, verna qui viennent après
          "Russula emetica", "Amanita phalloides",
          "Lepiota procera", "Balliota campestris",
          "Amanita muscaria",  # , pantherina
          "Boletus edulis"],
    177: [],
    183: ["Lomentaria articulata",
          "Padina Pavotia",
          "Corallina officinalis",
          "Rhodymenia palmata",
          "Delesseria sanguinea",
          "Laminaria Cloustoni",
          "Callophyllis laciniata",
          "Fucus vesiculosus",
          "Calliblepharis ciliata",
          "Calliblepharis laciniata",
          "Plocamium coccineum",
          "Chondrus crispus",
          "Heterosiphonia coccinea",
          "Ulva Lactuca"],
    186: [],
    192: ["Littorina littoralis"],
    194: [],
    211: ["ficus carica"],
    212: [],
    218: ["Vipera berus", "Vipera aspis",
          "Naja hiperdians", "Lachesis lanceolatus",
          "Vipera aspis", "Crotalus terrificus"],
    222: [],
    227: ["Ornithodorus Savignyi", "Ornithodorus moubaia",
          "Solanum Luberosum"],
    228: [],
    230: ["Raphidium nivale", "Protococcus nivalis",
          "Sphærella ‘mivalis", "Sphærella: lacustris",
          "rococcus vulgäris", "Pteromonas nivalis",
          "Ancylonema Nordenskioldii"],
    232: [],
    252: ["Balænoptera Sibbaldii", "B. musculus",
          "B. borealis"],
    257: [],
    262: ["Chæropsis : libe- ‘” “riensis", "Hippopotamus amphibius",
          "Hippopotamus amphibius major", "Hippopotamus melitensis",
          "H. minutus", "H. madagascariensis"],
    264: [],
    # ombreux noms de genre seuls
    278: ["Hydra fusca", "Branchipus stagnalis",
          "Apus productus", "Daphnia similis",
          "Gammarus négiectus", "Nepa cinerea"],
    281: [],
    302: ["Eumenes coarctatus", "Eumenes coarclatus",
          "Euinenes unguiculus", "Odynevus spinipes",
          "Celonites abbreviatus", "Odyner us spinipes",
          "Belenogaster junceuset", "Polistes gallicus",
          "Vespa - germanica", "Leipomeles lamellaria",
          "Prolopolybia emoTtualis", "Polybia dimidiaia",
          "Polybia rejecta", "Ceramius lusitanicus",
          "Odynerus spinipes", "Chelonites abbreviätus",
          "Polistes gallicus", "Vespa germanica",
          "Vespa media", "Protopolybia emortualis",
          "Protopolybia emortualis", "Leipomeles lamellaria",
          "Polybia rejecta", "Cassicus persicus",
          "Polybia rejecta"],  # collé à gauche à un 'de'
    306: [],
    310: ["Rotalina orbicularis", "Pupa similis",
          "Pupa similis"],
    311: ["bacillus butylicus", "bacillus orthobutylicus"],
    314: [],
    341: ["Botr ylis bassiana", "Sporotrichum globuliferum"],
    342: [],
    346: ["Shistocerca peregrina", "Shis{ocerca americana",
          "Shistocerca americana", "Micrococcus Acridiorum",
          "Coccobacillus Acridiorum", "Coccobacillus Acridiorum",
          "Atta Sexdens"],
    348: [],
    351: ["Ginkgo biloba", "Ginkgo biloba"],
    353: [],
    369: ["Arvicola agrestis", "Mus sylvaticus",
          "B. Typhi murium"],
    372: [],
    # la fin du nom d'espèce est en haut de la page suivante et donc coupé
    # par le titre et le "Droits reservés au Cnam et à ses partenaires"
    397: ["Drosera rotundifolia", "Drosera rotundifolia",
          "Drosera rotundifolia", "Dionaca müscipula",
          "Drosera rotundifolia", "Drosera rotundifolia",
          "Pinguicula caudata", "Drosera rotundifolia",
          "Dionaea muscipula", "Drosera ratun",
          "Dionaea muscipula", "Apocynum androsoemifolium"],
    400: [],
    # fyphus levissimus qui est un nom de maladie,
    # en particulier une forme de Typhus
    405: [],
    # le nom de genre a été abimé et coupé par l'OCR
    # Heros qui est visiblement Australauheros
    406: ["Plerophy Ju scalare", "Seatophagus arqUs",
          "Heros | facetus", "Mesonaula insignis",
          "Herniramphus fluvia", "Danio rerio",
          "Rasbora heteromorpha", "Moïlienesia latipinna",
          "Paratilapia multicolor"],
    408: [],
    422: ["Libellula depressa"],
    424: [],
    # pas réussi à déterminer quel est le nom de genre
    # mais mention certaine d'un binôme avec le cristata qui est un nom d'espèce
    # encore utilisé
    451: ["Zirphaea {Pholas] cristata", "Saxicava rugosa"],
    452: [],
    466: ["Chinoeletes opilio", "Lithodes kamschatica"],
    470: [],
    471: ["Atriplex halimus", "Atriplex nummularia",
          "Artemisia maritima", "Casuarina equisetifolia",
          "Ephedra alata", "Hippophæ rhamnoïdes",
          "Juniperus macrocarpa", "Melaleuca eriæœfolia",
          "Phytolacca dioïca", "Phœnix tenuis",
          "Phœnix dactylifera", "Rhus viminalis",
          "Salsola fruticosa", "Tamarix articulata",
          "Tamarix gallica", "Vitex agnus castus",
          "Acacia-nilatica", "Acacia cyclopis",
          "Acacia cyanophylla", "Albizzia lophauta",
          "Prosopis dulcis", "Casuarina quadrivalvis",
          "Cupressus lambertiana", "Eucalyptus robusta",
          "Evonymus japonica", "Ficus carica",
          "Pittosporum tobira", "Phillyrea media",
          "Parkinsonia aculeata", "Punica granatum", "Statice arborea"],
    472: [],
    478: ["tradescantia virginica", "geum urbanum", "deutzia scabra"],
    479: ["uassia amara"],
    480: [],
    486: ["Cimex lectularius", "Acanthia lectularia"],
    # passage en italien du XVe siecle
    487: [],
    488: ["Cereus pitahaya"],
    489: [],
    507: ["Gigantosaurus africanus", "G. robustus"],
    508: [],
    # S transformé en $ par l'OCR
    # deux articles entremêlés
    510: ["galega officinalis", "Mistichthys luzonensis",
          "Balænoptera sibbaldi", "Microsorex minnemana",
          "Blarina parva", "Calypte kelenæ", "Diomedea exulans",
          "Sphærodactylus sputator", "$. notatus",
          "Varanus saltator", "aspergilluss fumigatus",
          "Arthroleptis sechellensis", "Hyla Pickeringi",
          "Megalobatrachus japonicus", "Acanthophacelus bifurcus",
          "Arapaima gigas", "Carcharodon Rondeletii",
          "Oospora pulmonalis", "Rhizomucor parasiticus",
          "Mucor corymbifer"],
    512: [],
    # les boites aux lettres vont probablement nous ramener
    # pleins de faux positifs avec beaucoup de noms de gens
    519: ["Eriocampa limacina"],
    521: [],
    530: ["Cichorium intrbus"],
    531: [],
    534: ["ficus carica"],
    535: ["Eucalyptus globulus", "quassia amara", "quassia amara"],
    537: [],
    538: ["Xantophyllum lanceatum"],
    540: [],
    543: ["Zeusèra æsculi", "Cossus ligniperda"],
    544: [],
    550: ["yucca filamentosa", "statice limonium",
          "helianthus multiflorus", "bocconia microcarpa",
          "anemone japonica"],
    # nom de genre mentionné une seule fois et ce tout seul avant d'être abregé
    551: ["Ceroxylon audicola", "Copernicia cerifera",
          "M. Cerifera", "M. Carolinensis", "M. Pensylvanica",
          "M. Cordifolia", "M. Quercifolia", "M. Serrata",
          "Rhus succedanea", "Rhus vermicifera",
          "Stillingia Sebifera"],
    552: [],
    554: ["Gonioma Kamassi"],
    555: [],
    558: [],
    568: ["quassia amara"],
    569: ["Homo heidelbergensis"],
    570: [],
    582: ["polygonum cuspidatum"],
    583: [],
    610: ["Polysiphonia Brodiaei", "P. nigrescens",
          "Rhodomela suübfusca", "Batrachospermum Gallaer",
          "Demanea fluviatilis", "Ceramium rubrum"],
    611: [],
    622: ["veronica speciosa", "helianthus rigidus", "helianthus orgyalis"],
    623: [],
    632: ["Luillaja Saponaria", "Zuillaja Saponaria",
          "Sapindus Saponaria officinalis", "castilloa elastica"],
    634: [],
    648: ["Helix pomatia"],
    649: [],
    651: ["Falco tinnunculus", "Aceipiter nisus",
          "Astur.palumbarius", "Buteo vulgaris"],
    652: [],
    # bulletin météo sans rien
    654: [],
    655: [],
    656: ["Quillaja sapo", "Schisotrypanum Cruzi"],
    657: [],
    658: ["Paromæcium aurelia", "Colpomenia sinuosa"],
    660: [],
}