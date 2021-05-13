all: xml zip

xml: species.xml
species.xml: species.yaml transform.py
	./transform.py > $@ || rm -f $@

zip: species.zip
species.zip: species.xml natural_tree_24020.png
	zip $@ $^

clean:
	rm species.zip species.xml
