package main

import (
	"fmt"
	"log"
	"os"

	"github.com/deiu/rdf2go"
	"github.com/wallix/triplestore"
)

func main() {
	/*tris := []Triple{
		SubjPredRes("me", "rel", "you"),
		SubjPredRes("me", "rdf:type", "person"),
		SubjPredRes("you", "rel", "other"),
		SubjPredRes("you", "rdf:type", "child"),
		SubjPredRes("other", "any", "john"),
	}

	f, err := os.Create("./triples.nt")
	g, err := os.Open("./triples.nt")
	defer f.Close()
	defer g.Close()

	enc := NewLenientNTEncoder(f)
	for _, t := range tris {
		err = enc.Encode(t)
	}*/

	g, err := os.Open("./smart_tv.n3")
	dec := triplestore.NewLenientNTDecoder(g)
	triples, err := dec.Decode()

	if err != nil {
		log.Fatal(err)
	}

	src := triplestore.NewSource()
	for _, t := range triples {
		src.Add(t)
	}

	snap := src.Snapshot()

	trist := snap.WithSubject("ex:samsungtv")
	for _, tri := range trist {
		fmt.Printf("%+v\n", tri)
	}

	if err != nil {
		print("error")
	}

	r, err := os.Open("./smart_tv.n3")
	if err != nil {
		print("error")
	}
	// Set a base URI
	baseUri := "www.example.org"

	// Create a new graph
	t := rdf2go.NewGraph(baseUri)

	// r is of type io.Reader
	err = t.Parse(r, "text/turtle")
	if err != nil {
		log.Fatal(err)
	}
	log.Println(t.Len())
	// Look up one triple matching the given subject
	triples2 := t.All(nil, nil, rdf2go.NewResource("http://elite.polito.it/ontologies/dogont.owl#DoorActuator")) //
	log.Println(len(triples))

	for _, triple := range triples2 {
		log.Println(triple.String())
		print("j")
	}

	f, err := os.Create("./smart_tv_created.n3")

	triple := rdf2go.NewTriple(rdf2go.NewResource("http://example.org/ex#lgtv"), rdf2go.NewResource("http://www.w3.org/1999/02/22-rdf-syntax-ns#type"), rdf2go.NewResource("http://gsi.dit.upm.es/ontologies/ewe-connected-home-smarttv/ns/#SmartTv"))
	t.Add(triple)

	t.Serialize(f, "text/turtle")
}
