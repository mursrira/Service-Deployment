all: fxs
.PHONY: all

# Include standard NCS examples build definitions and rules
include $(NCS_DIR)/src/ncs/build/include.ncs.mk

SRC = yang/l3vpn.yang
SRC +=  yang/vrf-config.yang
SUBMODULES = $(shell ls yang/*.yang | grep -v $(SRC))
DIRS = ../load-dir java/src/$(JDIR)/$(NS)
FXS = $(SRC:yang/%.yang=../load-dir/%.fxs)
YANGPATH +=  ../../cisco-iosxr/src/ncsc-out/modules/yang
YANGPATH += $(NCS_DIR)/src/ncs/yang/:./yang/
NCSCPATH   = $(YANGPATH:%=--yangpath %)
YANGERPATH = $(YANGPATH:%=--path %)

fxs: $(DIRS) $(FXS)

$(DIRS):
	mkdir -p $@

../load-dir/%.fxs: yang/%.yang
	$(NCSC)  `ls $*-ann.yang  > /dev/null 2>&1 && echo "-a $*-ann.yang"` \
             $(NCSCPATH) -c -o $@ $<

clean:
	rm -rf $(DIRS)
.PHONY: clean
