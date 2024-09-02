all: xml zip

xml: tree-species.xml
%.xml: %.yaml transform.py
	./transform.py > $@ || rm -f $@

zip: tree-species.zip
%.zip: %.xml natural_tree_24020.png
	zip $@ $^

clean:
	rm tree-species.zip tree-species.xml
