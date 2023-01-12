SELECT taxonID, parentNameUsageID, acceptedNameUsageID, originalNameUsageID,
    scientificName, canonicalName, scientificNameAuthorship, taxonRank, namePublishedIn, taxonomicStatus, taxonRemarks,
    kingdom, phylum, class, "order", family, genus
FROM Taxon
WHERE taxonRank<>'unranked' AND
    (class='Lecanoromycetes' OR class='Arthoniomycetes' OR class='Lichinomycetes' OR 'order'='Pyrenulales' OR 'order'='Verrucariales' OR
    family='Abrothallaceae' OR family='Aphanopsidaceae' OR family='Arthopyreniaceae' OR family='Coniocybaceae' OR family='Naetrocymbaceae' OR
    family='Sphinctrinaceae' OR family='Strigulaceae' OR family='Thelocarpaceae' OR genus='Dictyonema' OR genus='Lichenomphalia' OR genus='Multiclavula' OR
    canonicalName='Ascomycota' OR canonicalName='Basidiomycota' OR canonicalName='Arthoniomycetes' OR canonicalName='Lecanoromycetes' OR
    canonicalName='Coniocybomycetes' OR canonicalName='Eurotiomycetes'  OR canonicalName='Dothideomycetes' OR canonicalName='Agaricomycetes' OR
    canonicalName='Lichinomycetes' OR canonicalName='Arthoniales' OR canonicalName='Fungi' OR canonicalName='Schaereriales' OR
    canonicalName='Umbilicariales' OR canonicalName='Lecanorales' OR canonicalName='Hymeneliales' OR canonicalName='Caliciales' OR
    canonicalName='Coniocybales' OR canonicalName='Arctomiales' OR canonicalName='Pertusariales' OR canonicalName='Graphidales' OR
    canonicalName='Peltigerales' OR canonicalName='Acarosporales' OR canonicalName='Mycocaliciales' OR canonicalName='Lecideales' OR
    canonicalName='Thelocarpales' OR canonicalName='Strigulales' OR canonicalName='Cantharellales' OR canonicalName='Rhizocarpales' OR
    canonicalName='Pleosporales' OR canonicalName='Atheliales' OR canonicalName='Teloschistales' OR canonicalName='Agaricales' OR
    canonicalName='Abrothallales' OR canonicalName='Lichenostigmatales' OR canonicalName='Ostropales' OR canonicalName='Turquoiseomycetales' OR
    canonicalName='Lichinales' OR canonicalName='Baeomycetales' OR canonicalName='Megalariaceae' OR canonicalName='Haematommataceae' OR
    canonicalName='Gypsoplacaceae' OR canonicalName='Chrysothricaceae' OR canonicalName='Rhizoplacopsidaceae' OR canonicalName='Opegraphaceae' OR
    canonicalName='Schaereriaceae' OR canonicalName='Umbilicariaceae' OR canonicalName='Ophioparmaceae' OR canonicalName='Lobariaceae' OR
    canonicalName='Lopadiaceae' OR canonicalName='Parmeliaceae' OR canonicalName='Lecanoraceae' OR canonicalName='Psilolechiaceae' OR
    canonicalName='Crocyniaceae' OR canonicalName='Hymeneliaceae' OR canonicalName='Stereocaulaceae' OR canonicalName='Psoraceae' OR
    canonicalName='Sphaerophoraceae' OR canonicalName='Pilocarpaceae' OR canonicalName='Microcaliciaceae' OR canonicalName='Ropalosporaceae' OR
    canonicalName='Physciaceae' OR canonicalName='Caliciaceae' OR canonicalName='Coniocybaceae' OR canonicalName='Phaneromycetaceae' OR
    canonicalName='Spirographaceae' OR canonicalName='Squamarinaceae' OR canonicalName='Lecanactidaceae' OR canonicalName='Siphulaceae' OR
    canonicalName='Xylographaceae' OR canonicalName='Cladoniaceae' OR canonicalName='Biatorellaceae' OR canonicalName='Strangosporaceae' OR
    canonicalName='Leprocaulaceae' OR canonicalName='Sarrameanaceae' OR canonicalName='Ramboldiaceae' OR canonicalName='Arctomiaceae' OR
    canonicalName='Tephromelataceae' OR canonicalName='Helocarpaceae' OR canonicalName='Ochrolechiaceae' OR canonicalName='Pertusariaceae' OR
    canonicalName='Coccotremataceae' OR canonicalName='Fissurinaceae' OR canonicalName='Porinaceae' OR canonicalName='Coccocarpiaceae' OR
    canonicalName='Vahliellaceae' OR canonicalName='Acarosporaceae' OR canonicalName='Letrouitiaceae' OR canonicalName='Sphinctrinaceae' OR
    canonicalName='Catillariaceae' OR canonicalName='Baeomycetaceae' OR canonicalName='Brigantieaceae' OR canonicalName='Lecideaceae' OR
    canonicalName='Thelocarpaceae' OR canonicalName='Arthopyreniaceae' OR canonicalName='Gloeoheppiaceae' OR canonicalName='Strigulaceae' OR
    canonicalName='Roccellaceae' OR canonicalName='Arthoniaceae' OR canonicalName='Chrysotrichaceae' OR canonicalName='Chiodectonaceae' OR
    canonicalName='Solorinellaceae' OR canonicalName='Nephromataceae' OR canonicalName='Heterodeaceae' OR canonicalName='Phlyctidaceae' OR
    canonicalName='Byssolomataceae' OR canonicalName='Porpidiaceae' OR canonicalName='Myeloconidiaceae' OR canonicalName='Cantharellaceae' OR
    canonicalName='Agyriaceae' OR canonicalName='Aphanopsidaceae' OR canonicalName='Miltideaceae' OR canonicalName='Pachyascaceae' OR
    canonicalName='Graphidaceae' OR canonicalName='Megasporaceae' OR canonicalName='Gomphillaceae' OR canonicalName='Odontotremataceae' OR
    canonicalName='Collemataceae' OR canonicalName='Koerberiaceae' OR canonicalName='Rhizocarpaceae' OR canonicalName='Thelenellaceae' OR
    canonicalName='Naetrocymbaceae' OR canonicalName='Lecanographaceae' OR canonicalName='Heppiaceae' OR canonicalName='Sagiolechiaceae' OR
    canonicalName='Fuscideaceae' OR canonicalName='Malmideaceae' OR canonicalName='Elixiaceae' OR canonicalName='Ramalinaceae' OR
    canonicalName='Roccellographaceae' OR canonicalName='Atheliaceae' OR canonicalName='Peltulaceae' OR canonicalName='Brigantiaeaceae' OR
    canonicalName='Peltigeraceae' OR canonicalName='Massalongiaceae' OR canonicalName='Thrombiaceae' OR canonicalName='Carbonicolaceae' OR
    canonicalName='Megalosporaceae' OR canonicalName='Teloschistaceae' OR canonicalName='Hygrophoraceae' OR canonicalName='Cameroniaceae' OR
    canonicalName='Candelariella' OR canonicalName='Abrothallaceae' OR canonicalName='Mycoblastaceae' OR canonicalName='Ectolechiaceae' OR
    canonicalName='Loxosporaceae' OR canonicalName='Thelotremataceae' OR canonicalName='Icmadophilaceae' OR canonicalName='Dactylosporaceae' OR
    canonicalName='Phaeococcomycetaceae' OR canonicalName='Stictidaceae' OR canonicalName='Protothelenellaceae' OR canonicalName='Coenogoniaceae' OR
    canonicalName='Pannariaceae' OR canonicalName='Gyalectaceae' OR canonicalName='Andreiomycetaceae' OR canonicalName='Bruceomycetaceae' OR
    canonicalName='Turquoiseomycetaceae' OR canonicalName='Scoliciosporaceae' OR canonicalName='Lichinaceae' OR canonicalName='Sporastatiaceae' OR
    canonicalName='Placynthiaceae' OR canonicalName='Arthrorhaphidaceae' OR canonicalName='Trapeliaceae' OR canonicalName='Redonographaceae' OR
    canonicalName='Dictyonema' OR canonicalName='Lichenomphalia' OR canonicalName='Multiclavula')
ORDER BY genus ASC, family ASC, "order" ASC, class ASC,  phylum ASC;