JOSM Preset for mapping tree species
====================================

How to use
----------

In JOSM, open Preferences (F12), then go to tab "Tagging Presets".
Add new preset (+ button on the right) with the URL
<https://github.com/rohieb/josm-tree-species-preset/raw/main/tree-species.zip>
(which directly uses the file in this repo).

Now you can select a node, press F3 to search for a taxon, and the preset will
set the keys `species`, `species:<lang>`, and `species:wikidata` (if the chosen
taxon is a species), or `genus`, `genus:<lang>`, and `genus:wikidata` (if the
taxon describes a genus only), as well as `natural=tree`, `leaf_cycle`, and
`leaf_type`.

How to add new species
----------------------

* Add new species to `species.yaml`.
  * If the main key is a single word (like *"Prunus"*), a `genus` template will
    be created.
  * If the main key is multiple words (like *"Gleditsia triacanthos"* or
    *"Quercus robur 'Fastigiata'"*), a `species` template will be created.
* Run `make`, which should (re-)create `species.xml` and `species.zip`.
* Add your local `species.xml` file as a preset in JOSM

TODO
----

* Generate different language versions
* Pull all language names from Wikidata
