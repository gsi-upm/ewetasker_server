NAME:=ewetasker
IMAGENAME:=registry.cluster.gsi.dit.upm.es/ewe/ewetasker_server
DOCKERFILEPATH:=./ewetasker

include .makefiles/base.mk
include .makefiles/k8s.mk
