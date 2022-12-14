.. about:

About MLI
==================================

General idea
------------

Many nature lovers want to know what they observe in nature. Institutes are
developing various applications based on artificial intelligence and neural
networks to help them. But, at least this applies to fungi and lichens,
technology is too far from giving a quality result. In addition, they do not
suggest how the naturalist can improve the result of the determination.

For the reasons above, those who really want to know have to go back to the
pre-computer era, take books and try to guess by the keys.

This application is intended to facilitate the "manual" identification of
lichens. It should store all the keys, and unlike paper books, the naturalist
no longer has to start with an awkward key. It can be start the definition
with any key that is in the database. In addition, the application should help
to see those signs that were missed for an accurate definition. For example, to
look the reverse side of the lobe in Peltigera, in order to distinguish between
forms close to different species.

Taxon Tree
__________

Currently, the taxon tree uses the taxonomy adopted in the GBIF project. The
GBIF taxon tree is collected automatically from several sources and is not of
high quality. For example, it does not always have scientific names, but only
canonical ones, there are taxa that are synonymous with themselves, and so on.
However, to date, GBIF is the only platform that has a deployed API and does
not severely restrict access to it. So, downloading a tree only takes about
a week.

iNaturalist which, in my opinion, has a better taxon tree, albeit often without
forms and subspecies, would require two weeks to a month, as it has a limit of
10,000 API calls per day.

Currently, the database contains 48.5 thousand taxonomic units. Of these, 28.8
thousand are synonyms, 18.6 thousand are real names and 1.7 thousand have an
incorrect interpretation of reality.

+----+------------+--------+
| №  | rank       | Count  |
+====+============+========+
| 1  | superregio | 1      |
+----+------------+--------+
| 2  | regio	  | 1      |
+----+------------+--------+
| 3  | regnum     | 1      |
+----+------------+--------+
| 4  | subregnum  | 5      |
+----+------------+--------+
| 5  | divisio    | 4      |
+----+------------+--------+
| 6  | subdivisio | 1      |
+----+------------+--------+
| 7  | classis    | 1      |
+----+------------+--------+
| 8  | subclassis | 4      |
+----+------------+--------+
| 9  | ordo       | 21     |
+----+------------+--------+
| 10 | subordo    | 4      |
+----+------------+--------+
| 11 | familia    | 83     |
+----+------------+--------+
| 12 | subfamilia | 10     |
+----+------------+--------+
| 13 | genus      | 1025   |
+----+------------+--------+
| 14 | species    | 16679  |
+----+------------+--------+
| 15 | subspecies | 240    |
+----+------------+--------+
| 16 | varietas   | 441    |
+----+------------+--------+
| 17 | forma      | 100    |
+----+------------+--------+
| 18 | synonym    | 28810  |
+----+------------+--------+
