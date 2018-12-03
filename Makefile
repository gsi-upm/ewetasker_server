NAME:=ewetasker
IMAGENAMEAPI:=registry.cluster.gsi.dit.upm.es/ewe/ewetasker_server/api
IMAGENAMECROSSBAR:=registry.cluster.gsi.dit.upm.es/ewe/ewetasker_server/crossbar
DOCKERFILEPATHAPI:=./ewetasker
DOCKERFILEPATHCROSSBAR:=./ewe-crossbar

include .makefiles/base.mk
include .makefiles/k8s.mk
