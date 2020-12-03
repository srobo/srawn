SOURCES = $(wildcard *.md)
TARGETS = $(SOURCES:.md=.html)

.PHONY: all clean

all: $(SOURCES) $(TARGETS)

%.html: %.md
	pandoc $< -s -o $@

clean:
	rm -f $(TARGETS)
