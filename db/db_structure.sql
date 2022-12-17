--
-- Файл сгенерирован с помощью SQLiteStudio v3.3.3 в вс дек. 11 17:45:41 2022
--
-- Использованная кодировка текста: UTF-8
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Таблица: Colors
DROP TABLE IF EXISTS Colors;

CREATE TABLE Colors (
    id_color   INTEGER PRIMARY KEY,
    color_name TEXT,
    hex_code   TEXT
);


-- Таблица: DBIndexes
DROP TABLE IF EXISTS DBIndexes;

CREATE TABLE DBIndexes (
    id_db_index INTEGER PRIMARY KEY,
    id_taxon    INTEGER REFERENCES Taxon (id_taxon),
    id_source   INTEGER REFERENCES DBSources (id_source),
    taxon_index TEXT
);

-- Таблица: DBSources
DROP TABLE IF EXISTS DBSources;

CREATE TABLE DBSources (
    id_source   INTEGER PRIMARY KEY,
    source_name TEXT,
    source_abbr TEXT,
    source_url  TEXT,
    index_link  TEXT
);

INSERT INTO DBSources (id_source, source_name, source_abbr, source_url, index_link) VALUES (1, 'iNaturalist', 'iNat', 'https://www.inaturalist.org/', 'https://www.inaturalist.org/taxa/49490');
INSERT INTO DBSources (id_source, source_name, source_abbr, source_url, index_link) VALUES (2, 'Encyclopædia Britannica Online', 'EBID', 'https://www.britannica.com/', 'https://www.britannica.com/science/');
INSERT INTO DBSources (id_source, source_name, source_abbr, source_url, index_link) VALUES (3, 'Swedish Taxonomic Database', 'Dyntaxa ID', 'https://www.dyntaxa.se/', 'https://www.dyntaxa.se/taxon/info/');
INSERT INTO DBSources (id_source, source_name, source_abbr, source_url, index_link) VALUES (4, 'Danmarks svampeatlas', 'DS ID', 'https://svampe.databasen.org/', 'https://svampe.databasen.org/taxon/');
INSERT INTO DBSources (id_source, source_name, source_abbr, source_url, index_link) VALUES (5, 'Catalogue of Life', 'CoL ID', 'https://www.catalogueoflife.org/', 'https://www.catalogueoflife.org/data/taxon/');
INSERT INTO DBSources (id_source, source_name, source_abbr, source_url, index_link) VALUES (6, 'Australian Lichen', 'AusLichen', 'https://lichen.biodiversity.org.au/', 'https://lichen.biodiversity.org.au/nsl/services/rest/name/lichen/');
INSERT INTO DBSources (id_source, source_name, source_abbr, source_url, index_link) VALUES (7, 'Australian Fungi', 'AusFungi', 'https://fungi.biodiversity.org.au/', 'https://fungi.biodiversity.org.au/nsl/services/rest/name/fungi/');
INSERT INTO DBSources (id_source, source_name, source_abbr, source_url, index_link) VALUES (8, 'Open Tree of Life ID', 'OTT ID', 'https://tree.opentreeoflife.org/', 'https://tree.opentreeoflife.org/taxonomy/browse?id=');
INSERT INTO DBSources (id_source, source_name, source_abbr, source_url, index_link) VALUES (9, 'Taxonomy database of the U.S. National Center for Biotechnology Information', 'NCBI', 'https://www.ncbi.nlm.nih.gov/', 'https://www.ncbi.nlm.nih.gov/taxonomy/');
INSERT INTO DBSources (id_source, source_name, source_abbr, source_url, index_link) VALUES (10, 'MycoBank Database', 'MycoBank', 'https://www.mycobank.org/', 'https://www.mycobank.org/page/Name%20details%20page/field/Mycobank%20%2523/');
INSERT INTO DBSources (id_source, source_name, source_abbr, source_url, index_link) VALUES (11, 'Index Fungorum', 'IF ID', 'http://www.indexfungorum.org/', 'http://www.indexfungorum.org/names/NamesRecord.asp?RecordID=');
INSERT INTO DBSources (id_source, source_name, source_abbr, source_url, index_link) VALUES (12, 'Global Biodiversity Information Facility', 'GBIF', 'https://www.gbif.org/', 'https://www.gbif.org/species/');
INSERT INTO DBSources (id_source, source_name, source_abbr, source_url, index_link) VALUES (13, 'Encyclopedia of Life', 'EoL', 'https://eol.org/', 'https://eol.org/pages/');

-- Таблица: Images
DROP TABLE IF EXISTS Images;

CREATE TABLE Images (
    id_images INTEGER PRIMARY KEY,
    id_taxon  INTEGER REFERENCES Taxon,
    images    BLOB
);


-- Таблица: Lang
DROP TABLE IF EXISTS Lang;

CREATE TABLE Lang (
    id_lang       INTEGER   PRIMARY KEY,
    lang          TEXT (20) NOT NULL,
    iso_639_1     TEXT,
    iso_639_2     TEXT,
    iso_639_3     TEXT,
    iso_639_5     TEXT,
    gost_7_75_lat TEXT,
    gost_7_75_rus TEXT,
    d_code        TEXT
);


-- Таблица: LangVariant
DROP TABLE IF EXISTS LangVariant;

CREATE TABLE LangVariant (
    id_lang_variant INTEGER PRIMARY KEY,
    id_lang         INTEGER REFERENCES Lang (id_lang),
    lang            TEXT
);


-- Таблица: LifeForm
DROP TABLE IF EXISTS LifeForm;

CREATE TABLE LifeForm (
    id_life_form       INTEGER PRIMARY KEY,
    life_form_name     TEXT,
    life_form_lat_name TEXT
);

INSERT INTO LifeForm (id_life_form, life_form_name, life_form_lat_name) VALUES (1, 'накипные', NULL);
INSERT INTO LifeForm (id_life_form, life_form_name, life_form_lat_name) VALUES (2, 'листоватые', NULL);
INSERT INTO LifeForm (id_life_form, life_form_name, life_form_lat_name) VALUES (3, 'кустичные', NULL);
INSERT INTO LifeForm (id_life_form, life_form_name, life_form_lat_name) VALUES (4, 'слизистые', NULL);

-- Таблица: LifeFormTaxon
DROP TABLE IF EXISTS LifeFormTaxon;

CREATE TABLE LifeFormTaxon (
    id_life_form_taxon INTEGER PRIMARY KEY,
    id_taxon                   REFERENCES Taxon,
    id_life_form       INTEGER REFERENCES LifeForm (id_life_form) 
);


-- Таблица: LocalName
DROP TABLE IF EXISTS LocalName;

CREATE TABLE LocalName (
    id_local_name INTEGER PRIMARY KEY,
    id_taxon      INTEGER REFERENCES Taxon (id_taxon),
    id_lang       INTEGER REFERENCES Lang (id_lang),
    local_name    TEXT
);


-- Таблица: Metering
DROP TABLE IF EXISTS Metering;

CREATE TABLE Metering (
    id_metering   INTEGER PRIMARY KEY,
    metering_name TEXT
);


-- Таблица: PartProperties
DROP TABLE IF EXISTS PartProperties;

CREATE TABLE PartProperties (
    id_properties         PRIMARY KEY,
    id_taxon      INTEGER REFERENCES Taxon (id_taxon),
    id_part       INTEGER REFERENCES Parts (id_part),
    properte      TEXT
);


-- Таблица: Parts
DROP TABLE IF EXISTS Parts;

CREATE TABLE Parts (
    id_part       INTEGER PRIMARY KEY,
    part_lat_name TEXT,
    part_name
);

INSERT INTO Parts (id_part, part_lat_name, part_name) VALUES (1, 'apothecium', 'апотеций');
INSERT INTO Parts (id_part, part_lat_name, part_name) VALUES (2, 'perithecium', 'перитеций');
INSERT INTO Parts (id_part, part_lat_name, part_name) VALUES (3, 'isidium', 'изидии');
INSERT INTO Parts (id_part, part_lat_name, part_name) VALUES (4, 'soredium', 'соредии');
INSERT INTO Parts (id_part, part_lat_name, part_name) VALUES (5, 'cyfella', 'цифелла');
INSERT INTO Parts (id_part, part_lat_name, part_name) VALUES (6, 'cyfelodium', 'цифелодия');
INSERT INTO Parts (id_part, part_lat_name, part_name) VALUES (7, 'pseudocyfelodium', 'псевдоцифелодия');
INSERT INTO Parts (id_part, part_lat_name, part_name) VALUES (8, 'lobuli', 'лобулы');
INSERT INTO Parts (id_part, part_lat_name, part_name) VALUES (9, 'lamella', 'пластинка');
INSERT INTO Parts (id_part, part_lat_name, part_name) VALUES (10, 'rhezinae', 'резины');
INSERT INTO Parts (id_part, part_lat_name, part_name) VALUES (11, 'rhezoida', 'резойды');
INSERT INTO Parts (id_part, part_lat_name, part_name) VALUES (12, 'gomfus', 'гомф');
INSERT INTO Parts (id_part, part_lat_name, part_name) VALUES (13, 'squamulae', 'чешуйки');
INSERT INTO Parts (id_part, part_lat_name, part_name) VALUES (14, 'ramus', 'ветвь');
INSERT INTO Parts (id_part, part_lat_name, part_name) VALUES (15, 'paraphyses', 'парафизы');
INSERT INTO Parts (id_part, part_lat_name, part_name) VALUES (16, 'asci', 'сумки');
INSERT INTO Parts (id_part, part_lat_name, part_name) VALUES (17, 'sporae', 'споры');
INSERT INTO Parts (id_part, part_lat_name, part_name) VALUES (18, 'pycnoconidia', 'пикноконидии');
INSERT INTO Parts (id_part, part_lat_name, part_name) VALUES (19, 'pycnidia', 'пикнидии');
INSERT INTO Parts (id_part, part_lat_name, part_name) VALUES (20, 'podetia', 'подеции');
INSERT INTO Parts (id_part, part_lat_name, part_name) VALUES (21, 'photobiont', 'фотобионт');
INSERT INTO Parts (id_part, part_lat_name, part_name) VALUES (22, 'thallus', 'слоевище');
INSERT INTO Parts (id_part, part_lat_name, part_name) VALUES (23, 'medulla', 'сердцевина');


-- Таблица: PartsColor
DROP TABLE IF EXISTS PartsColor;

CREATE TABLE PartsColor (
    id_part_color INTEGER PRIMARY KEY,
    id_taxon      INTEGER REFERENCES Taxon,
    id_part       INTEGER REFERENCES LichenParts (id_part),
    id_color      INTEGER REFERENCES Colors (id_color) 
);


-- Таблица: PartsSize
DROP TABLE IF EXISTS PartsSize;

CREATE TABLE PartsSize (
    id_lichen_part_size         PRIMARY KEY,
    id_taxon            INTEGER REFERENCES Taxon,
    id_part             INTEGER REFERENCES LichenParts (id_part),
    id_metering         INTEGER REFERENCES Metering (id_metering),
    size                DOUBLE
);


-- Таблица: Places
DROP TABLE IF EXISTS Places;

CREATE TABLE Places (
    id_region  INTEGER PRIMARY KEY,
    place_name
);


-- Таблица: PlacesOfLive
DROP TABLE IF EXISTS PlacesOfLive;

CREATE TABLE PlacesOfLive (
    id_place_of_live INTEGER PRIMARY KEY,
    id_taxon         INTEGER REFERENCES Taxon,
    id_region        INTEGER REFERENCES Places (id_region) 
);


-- Таблица: Substrate
DROP TABLE IF EXISTS Substrate;

CREATE TABLE Substrate (
    id_substrate   INTEGER PRIMARY KEY,
    substrate_name TEXT
);

INSERT INTO Substrate (id_substrate, substrate_name) VALUES (1, 'кора живых деревьев');
INSERT INTO Substrate (id_substrate, substrate_name) VALUES (2, 'кора хвойных деревьев');
INSERT INTO Substrate (id_substrate, substrate_name) VALUES (3, 'кора лиственных деревьев');
INSERT INTO Substrate (id_substrate, substrate_name) VALUES (4, 'валежник');
INSERT INTO Substrate (id_substrate, substrate_name) VALUES (5, 'обработаная древисина');
INSERT INTO Substrate (id_substrate, substrate_name) VALUES (6, 'пни');
INSERT INTO Substrate (id_substrate, substrate_name) VALUES (7, 'с неопавше корой');
INSERT INTO Substrate (id_substrate, substrate_name) VALUES (8, 'с опавшей корой');
INSERT INTO Substrate (id_substrate, substrate_name) VALUES (9, 'обгорелые');
INSERT INTO Substrate (id_substrate, substrate_name) VALUES (10, 'гниющие');
INSERT INTO Substrate (id_substrate, substrate_name) VALUES (11, 'почва');
INSERT INTO Substrate (id_substrate, substrate_name) VALUES (12, 'песчаная почва');
INSERT INTO Substrate (id_substrate, substrate_name) VALUES (13, 'гумусная почва');
INSERT INTO Substrate (id_substrate, substrate_name) VALUES (14, 'порфянистая почва');
INSERT INTO Substrate (id_substrate, substrate_name) VALUES (15, 'почва на камнях');
INSERT INTO Substrate (id_substrate, substrate_name) VALUES (16, 'древесина');
INSERT INTO Substrate (id_substrate, substrate_name) VALUES (17, 'камни');
INSERT INTO Substrate (id_substrate, substrate_name) VALUES (18, 'силикатная порода камней');
INSERT INTO Substrate (id_substrate, substrate_name) VALUES (19, 'извесняк');
INSERT INTO Substrate (id_substrate, substrate_name) VALUES (20, 'освещённые камни');
INSERT INTO Substrate (id_substrate, substrate_name) VALUES (21, 'затенённые камни');
INSERT INTO Substrate (id_substrate, substrate_name) VALUES (22, 'вертикальные поверхности камней');
INSERT INTO Substrate (id_substrate, substrate_name) VALUES (23, 'горизонтальные поверхности камней');
INSERT INTO Substrate (id_substrate, substrate_name) VALUES (24, 'в тени');
INSERT INTO Substrate (id_substrate, substrate_name) VALUES (25, 'на свету');
INSERT INTO Substrate (id_substrate, substrate_name) VALUES (26, 'на замшелом камне');
INSERT INTO Substrate (id_substrate, substrate_name) VALUES (27, 'на водной границе');
INSERT INTO Substrate (id_substrate, substrate_name) VALUES (28, 'заливаемый водами');

-- Таблица: SubstrateOfTaxon
DROP TABLE IF EXISTS SubstrateOfTaxon;

CREATE TABLE SubstrateOfTaxon (
    id_substrate_of_taxon INTEGER PRIMARY KEY,
    id_substrate          INTEGER REFERENCES Substrate (id_substrate),
    id_taxon              INTEGER REFERENCES Taxon (id_taxon) 
);


-- Таблица: Taxon
DROP TABLE IF EXISTS Taxon;

CREATE TABLE Taxon (
    id_taxon       INTEGER PRIMARY KEY,
    id_level       INTEGER REFERENCES TaxonLevel (id_level),
    id_main_taxon  INTEGER REFERENCES Taxon (id_taxon),
    taxon_lat_name TEXT,
    author         TEXT,
    year           INTEGER,
    id_status      INTEGER REFERENCES TaxonStatus (id_status) 
);

INSERT INTO Taxon (id_taxon, id_level, id_main_taxon, taxon_lat_name, author, year, id_status) VALUES (1, 1, NULL, 'Biota', '', NULL, 1);
INSERT INTO Taxon (id_taxon, id_level, id_main_taxon, taxon_lat_name, author, year, id_status) VALUES (2, 3, 1, 'Fungi', 'R.T.Moore', 1980, 1);


-- Таблица: TaxonLevel
DROP TABLE IF EXISTS TaxonLevel;

CREATE TABLE TaxonLevel (
    id_level       INTEGER PRIMARY KEY,
    principal      BOOLEAN,
    level_lat_name TEXT,
    level_name     TEXT,
    level_en_name  TEXT
);

INSERT INTO TaxonLevel (id_level, principal, level_lat_name, level_name, level_en_name) VALUES (1, 1, 'superregio', 'наддомен', 'superregio');
INSERT INTO TaxonLevel (id_level, principal, level_lat_name, level_name, level_en_name) VALUES (2, 1, 'regio', 'домен', 'domain');
INSERT INTO TaxonLevel (id_level, principal, level_lat_name, level_name, level_en_name) VALUES (3, 1, 'regnum', 'царство', 'kingdom');
INSERT INTO TaxonLevel (id_level, principal, level_lat_name, level_name, level_en_name) VALUES (4, 0, 'subregnum', 'подцарство', 'subkingdom');
INSERT INTO TaxonLevel (id_level, principal, level_lat_name, level_name, level_en_name) VALUES (5, 1, 'divisio', 'тип', 'division');
INSERT INTO TaxonLevel (id_level, principal, level_lat_name, level_name, level_en_name) VALUES (6, 0, 'subdivisio', 'подтип', 'subdivision');
INSERT INTO TaxonLevel (id_level, principal, level_lat_name, level_name, level_en_name) VALUES (7, 1, 'classis', 'класс', 'class');
INSERT INTO TaxonLevel (id_level, principal, level_lat_name, level_name, level_en_name) VALUES (8, 0, 'subclassis', 'подкласс', 'subclass');
INSERT INTO TaxonLevel (id_level, principal, level_lat_name, level_name, level_en_name) VALUES (9, 1, 'ordo', 'порядок', 'order');
INSERT INTO TaxonLevel (id_level, principal, level_lat_name, level_name, level_en_name) VALUES (10, 0, 'subordo', 'подпорядок', 'suborder');
INSERT INTO TaxonLevel (id_level, principal, level_lat_name, level_name, level_en_name) VALUES (11, 1, 'familia', 'семейство', 'family');
INSERT INTO TaxonLevel (id_level, principal, level_lat_name, level_name, level_en_name) VALUES (12, 0, 'subfamilia', 'подсемейство', 'subfamily');
INSERT INTO TaxonLevel (id_level, principal, level_lat_name, level_name, level_en_name) VALUES (13, 0, 'tribus', 'триба', 'tribe');
INSERT INTO TaxonLevel (id_level, principal, level_lat_name, level_name, level_en_name) VALUES (14, 0, 'subtribus', 'подтриба', 'subtribe');
INSERT INTO TaxonLevel (id_level, principal, level_lat_name, level_name, level_en_name) VALUES (15, 1, 'genus', 'род', 'genus');
INSERT INTO TaxonLevel (id_level, principal, level_lat_name, level_name, level_en_name) VALUES (16, 0, 'subgenus', 'подрод', 'subgenus');
INSERT INTO TaxonLevel (id_level, principal, level_lat_name, level_name, level_en_name) VALUES (17, 0, 'sectio', 'секция', 'section');
INSERT INTO TaxonLevel (id_level, principal, level_lat_name, level_name, level_en_name) VALUES (18, 0, 'subsectio', 'подсекция', 'subsection');
INSERT INTO TaxonLevel (id_level, principal, level_lat_name, level_name, level_en_name) VALUES (19, 0, 'series', 'ряд', 'series');
INSERT INTO TaxonLevel (id_level, principal, level_lat_name, level_name, level_en_name) VALUES (20, 0, 'subseries', 'подряд', 'subseries');
INSERT INTO TaxonLevel (id_level, principal, level_lat_name, level_name, level_en_name) VALUES (21, 1, 'species', 'вид', 'species');
INSERT INTO TaxonLevel (id_level, principal, level_lat_name, level_name, level_en_name) VALUES (22, 0, 'subspecies', 'подвид', 'subspecies');
INSERT INTO TaxonLevel (id_level, principal, level_lat_name, level_name, level_en_name) VALUES (23, 0, 'varietas', 'разновидность', 'variety');
INSERT INTO TaxonLevel (id_level, principal, level_lat_name, level_name, level_en_name) VALUES (24, 0, 'subvarietas', 'подразновидность', 'subvariety');
INSERT INTO TaxonLevel (id_level, principal, level_lat_name, level_name, level_en_name) VALUES (25, 1, 'forma', 'форма', 'form');
INSERT INTO TaxonLevel (id_level, principal, level_lat_name, level_name, level_en_name) VALUES (26, 0, 'subforma', 'субформа', 'subform');


-- Таблица: TaxonStatus
DROP TABLE IF EXISTS TaxonStatus;

CREATE TABLE TaxonStatus (
    id_status   INTEGER PRIMARY KEY,
    status_name TEXT
);

INSERT INTO TaxonStatus (id_status, status_name) VALUES (1, 'ACCEPTED');
INSERT INTO TaxonStatus (id_status, status_name) VALUES (2, 'SYNONYM');
INSERT INTO TaxonStatus (id_status, status_name) VALUES (3, 'DOUBTFUL');


-- Таблица: UpdateTaxonGBIF
DROP TABLE IF EXISTS UpdateTaxonGBIF;

CREATE TABLE UpdateTaxonGBIF (
    id          INTEGER  PRIMARY KEY,
    update_date DATETIME,
    id_taxon_sp INTEGER,
    id_taxon_sn INTEGER
);


COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
