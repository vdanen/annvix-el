# Makefile for aide
# $Id: Makefile 23 2009-03-23 00:56:11Z vdanen $

NAME := aide
SPECFILE = $(firstword $(wildcard *.spec))
DIST = EL5

define find-makefile-common
for d in common ../common ../../common ; do if [ -f $$d/Makefile.common ] ; then if [ -f $$d/CVS/Root -a -w $$/Makefile.common ] ; then cd $$d ; cvs -Q update ; fi ; echo "$$d/Makefile.common" ;      
break ; fi ; done
endef

MAKEFILE_COMMON := $(shell $(find-makefile-common))

include $(MAKEFILE_COMMON)

