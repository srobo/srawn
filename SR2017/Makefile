SOURCES = $(wildcard *.md)
TARGETS = $(SOURCES:.md=.html)

.PHONY: all clean

all: $(SOURCES) $(TARGETS)

%.html: %.md styles.css
	pandoc $< -s -o $@ -c styles.css

clean:
	rm -f $(TARGETS)
