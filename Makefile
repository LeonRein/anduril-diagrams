# Andúril 2 diagrams — build & check
#   make          -> regenerate all SVGs and PNGs in diagrams/
#   make check    -> geometric layout check (fails on new findings)

VARIANTS := e12 generic
OUT      := diagrams
SVGS     := $(foreach v,$(VARIANTS),$(OUT)/anduril2-$(v)-advanced-ui.svg $(OUT)/anduril2-$(v)-simple-ui.svg)
PNGS     := $(SVGS:.svg=.png)
SRC      := src/common.py

.PHONY: all svg png check clean
all: png

svg: $(SVGS)
png: $(PNGS)

$(OUT)/anduril2-%-advanced-ui.svg: src/advanced.py $(SRC)
	python3 src/advanced.py $@ $*

$(OUT)/anduril2-%-simple-ui.svg: src/simple.py $(SRC)
	python3 src/simple.py $@ $*

# advanced diagrams at 2x (4000 px wide), simple diagrams at 1.5x (3072 px wide)
$(OUT)/%-advanced-ui.png: $(OUT)/%-advanced-ui.svg tools/render.js
	node tools/render.js $< $@ 2

$(OUT)/%-simple-ui.png: $(OUT)/%-simple-ui.svg tools/render.js
	node tools/render.js $< $@ 1.5

check: $(SVGS)
	node tools/check.js $(SVGS)

clean:
	rm -f $(SVGS) $(PNGS)
