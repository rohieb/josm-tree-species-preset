#!/usr/bin/env python3

import yaml
import sys


HEADER_TEMPLATE = """<?xml version="1.0"?>
<presets version="2.7.0" xmlns="http://josm.openstreetmap.de/tagging-preset-1.0">
<group name="Tree species" icon="natural_tree_24020.png">

<chunk id="common_keys">
    <text key="height" text="Height (meters)" />
    <text key="circumference" text="Circumference (meters)" />
    <text key="diameter" text="Diameter (millimeters)" />
    <text key="diameter_crown" text="Crown diameter (meters)" />
    <check key="protected" text="Protected" disable_off="true" />
    <combo key="denotation" text="Denotation" editable="false" values_sort="true">
        <list_entry value="agricultural" short_description="Agricultural" />
        <list_entry value="avenue" short_description="Avenue" />
        <list_entry value="landmark" short_description="Landmark" />
        <list_entry value="natural_monument" short_description="Natural monument" />
        <list_entry value="urban" short_description="Urban" />
    </combo>
</chunk>

<chunk id="dioecious">
    <combo key="sex" text="Sex" editable="false" values_sort="true">
        <list_entry value="female" />
        <list_entry value="male" />
    </combo>
</chunk>
"""

NAME_TEMPLATE = """
    <key key="{taxon}:{lang}" value="{name}" />"""

ITEM_TEMPLATE = """
<item name="{item_name}" icon="natural_tree_24020.png" type="node">
    <key key="natural" value="tree" />
    <key key="{taxon}" value="{name}" />{localised_names}
    <key key="leaf_cycle" value="{leaf_cycle}" />
    <key key="leaf_type" value="{leaf_type}" />{dioecious_template}
    <reference ref="common_keys" />
</item>
"""

DIOECIOUS_TEMPLATE = """
    <reference ref="dioecious" />"""

FOOTER_TEMPLATE = """</group>
</presets>"""

def escape(s):
    return s.replace('"', "&quot;")

def main():
    output = HEADER_TEMPLATE

    with open("species.yaml", "r") as f:
        species = yaml.load(f, Loader=yaml.SafeLoader)

        for name, attrs in species.items():
            dioecious_template = ""
            flags = set()
            leaf_cycle = ""
            leaf_type = ""
            localised_names = {}
            name_first = ""
            name_template = ""
            taxon = "species"
            taxon_name = name

            for item in attrs:
                if isinstance(item, str):
                    flags.add(item)
                elif isinstance(item, dict):
                    localised_names.update(item)
            
            if not " " in name:
                taxon = "genus"
                taxon_name = name + " sp."

            f = "dioecious"
            if f in flags:
                dioecious_template = DIOECIOUS_TEMPLATE
                flags.remove(f)

            for f in ["evergreen", "semi_evergreen", "semi_deciduous", "deciduous"]:
                if f in flags:
                    leaf_cycle = f
                    flags.remove(f)
                    break

            for f in ["needleleaved", "broadleaved", "leafless"]:
                if f in flags:
                    leaf_type = f
                    flags.remove(f)
                    break

            if len(flags) > 0:
                print("Warning: taxon '{name}' has unknown flags: {flags}".format(
                    name=name, flags=repr(flags)), file=sys.stderr)

            for lang, localised_name in localised_names.items():
                if not name_first:
                    name_first = localised_name
                name_template += NAME_TEMPLATE.format(taxon=taxon, lang=lang,
                    name=escape(localised_name))

            if not name_first:
                item_name = taxon_name
            else:
                item_name = "{} ({})".format(name_first, taxon_name)

            output += ITEM_TEMPLATE.format(
                    dioecious_template=dioecious_template,
                    item_name=escape(item_name),
                    leaf_cycle=leaf_cycle,
                    leaf_type=leaf_type,
                    localised_names=name_template,
                    name=escape(name),
                    name_template=name_template,
                    taxon=taxon,
                    taxon_name=escape(taxon_name),
                )

    print(output)
    print(FOOTER_TEMPLATE)

main()

# vim: set tw=100
