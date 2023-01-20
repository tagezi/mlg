# Manual Lichen identification

[![Documentation Status](https://readthedocs.org/projects/manual-lichen-identification/badge/?version=latest)](https://manual-lichen-identification.readthedocs.io/en/latest/?badge=latest)

## Table of contents

- [About Manual Lichen identification](#about-manual-lichen-identification)
- [Install and run](#install-and-run)
- [License](#license)

## About Manual Lichen identification

Many nature lovers want to know what they observe in nature. Institutes are
developing various applications based on artificial intelligence and neural
networks to help them. But, at least this applies to fungi and lichens,
technology is too far from giving a quality result. In addition, they do not
suggest how the naturalist can improve the result of the identification.

For the reasons above, those who really want to know have to go back to the
pre-computer era, take books and try to guess by the keys.

This application is intended to facilitate the "manual" identification of
lichens. It should store all the keys, and unlike paper books, the naturalist
no longer has to start with an awkward key. It can be start the recognition
with any key that is in the database. In addition, the application should help
to see those signs that were missed for an accurate identification. 
For example, to look the reverse side of the lobe in Peltigera, in order to 
distinguish between forms close to different species.

Now you can enter information into the taxon tree:
Scientific name, canonical name, authors, year and synonyms.

![common view app](https://github.com/tagezi/mli/blob/master/files/images/common_view_01.png?raw=true)

All names of lichens are given in Latin.
Parts of lichens and other information, if possible, are given in English.

The interface can be translated into the standard way for GNU projects.

## Install and run

**_NOTE:_**
   First of all, you should remember that this program is written in
   Python 3.10. So, it is necessary to 
   [install its interpreter](https://www.python.org/) for work.
   After installing python
   [install pip](https://pip.pypa.io/en/stable/installation/).

You can download code from only github now. Download zip archive from github
or use [git applications](https://git-scm.com/) to sync with storage.

If you downloaded zip-file, unzip it to a folder of your choice.
Below are the commands if you decide to use git.

```commandline
git clone https://github.com/tagezi/mil.git
```

Go to `mil` directory:

```commandline
cd mil
```

Install requirements:

```commandline
pip install -r requirements.txt
```

Now you are ready to run the script:

```commandline
python3 -m mil
```

## License

All information including documentation, photographs, drawings, screenshots,
information in the database and other background information is distributed
under license [Creative Commons Attribution-ShareAlike 4.0 
International](https://creativecommons.org/licenses/by-sa/4.0/deed.en) 
(CC BY-SA 4.0).

All code and database structure is distributed under licenseAll code and
database structure is distributed under license [GNU General Public License
version 3](https://www.gnu.org/licenses/gpl-3.0-standalone.html) (GNU GPLv3).
