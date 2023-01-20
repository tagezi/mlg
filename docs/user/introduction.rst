.. introduction:

Introduction
------------

About MLI
~~~~~~~~~

General idea
""""""""""""

Many nature lovers want to know what they observe in nature. Institutes are
developing various applications based on artificial intelligence and neural
networks to help them. But, at least this applies to fungi and lichens,
technology is too far from giving a quality result. In addition, they do not
suggest how the naturalist can improve the result of the identification, if it
possible.

For the reasons above, those who really want to know have to go back to the
pre-computer era, take books and try to guess by the keys.

This application is intended to facilitate the "manual" identification of
lichens. It should store all the keys, and unlike paper books, the naturalist
no longer has to start with an awkward key. It can be start the identification
with any key that is in the database. In addition, the application should help
to see those signs that were missed for an accurate identification.
For example, to look the reverse side of the lobe in Peltigera, in order to
distinguish between forms close to different species.

Taxon Tree
""""""""""

Currently, the taxon tree uses the taxonomy adopted in the GBIF project. The
`GBIF <https://www.gbif.org/>`_ taxon tree is collected automatically from
several sources and is not of high quality. For example, it does not always
have scientific names, but only canonical ones, there are taxa that are
synonymous with themselves, and etc. However, to date, GBIF is the only
platform that has a deployed API and does not severely restrict access to it.
So, downloading a tree only takes about a week.

`iNaturalist <https://www.inaturalist.org/>`_ which, in my opinion, has a
better taxon tree, albeit often without forms and subspecies, would require
from two weeks to a month, as it has a limit of 10,000 API calls per day.

Currently, the database contains 60 965 taxonomic units. Of these, 38.8
thousand are synonyms, 22 thousand are real names. Below is a table that
summarizes the taxonomic tree.

+-------------+--------+
| rank        | Count  |
+=============+========+
| kingdom     | 1      |
+-------------+--------+
| division    | 2      |
+-------------+--------+
| class       | 7      |
+-------------+--------+
| order       | 28     |
+-------------+--------+
| family      | 126    |
+-------------+--------+
| genus       | 1199   |
+-------------+--------+
| species     | 19817  |
+-------------+--------+
| subspecies  | 258    |
+-------------+--------+
| synonym     | 28810  |
+-------------+--------+

Install and run
~~~~~~~~~~~~~~~

.. note::
   First of all, you should remember that this application is written in
   Python 3. And Python versions from 3.6 to 3.10 are supported.
   So, it is necessary to `install its interpreter <https://www.python.org/>`_
   for work. After installing python you need to
   `install pip <https://pip.pypa.io/en/stable/installation/>`_.

You can download code from only github now. Download zip archive from github
or use `git applications <https://git-scm.com/>`_ to sync with storage.
The latter method will allow you to have the latest version of the application
and database possible.

If you downloaded zip-file, unzip it to a folder of your choice.
Below there are the commands if you decide to use git.

.. code-block:: bash

   git clone https://github.com/tagezi/mli.git

In the future, to update the program, you will need to run the command in the
application directory `mli`:

.. code-block:: bash

    git pull -r

Go to `mli` directory:

.. code-block:: bash

   $ cd mli

Install requirements:

.. code-block:: bash

   $ pip install -r requirements.txt

Now you are ready to run the application:

.. code-block:: bash

   $ python3 -m mli

Licenses
~~~~~~~~

The application is licensed under the `GNU General Public License version 3
<https://www.gnu.org/licenses/gpl-3.0-standalone.html>`_ (GNU GPLv3). All
non-software parts including documentation, information stored in databases,
photographs, drawings, screenshots are distributed under the `Creative Commons
Attribution-ShareAlike 4.0 International
<https://creativecommons.org/licenses/by-sa/4.0/deed.en>`_ (CC BY-SA 4.0)
license.

In simple terms, you have the right to use, modify and distribute the
application and the information in it, if you indicate the source of the
information in any reasonable way and do not change the licenses.

Contributors
~~~~~~~~~~~~

This list may not be complete, as some authors may not contribute directly to
github, but send information and patches to other authors. Also, it may happen
that some authors forget to include themselves in the contributor list. So,
this is the minimum list of contributors. To get a complete list, you need to
do a full revision of authorship.

**The list of contributors:**

.. include:: ../../contributors.txt
