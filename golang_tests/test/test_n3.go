package main

import (
	"log"
	"os"

	"github.com/deiu/rdf2go"
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
	/*
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
	*/
	loadFromFuseki()
	loadFromFile()
}

func loadFromFuseki() {

	// Create a new graph
	g := rdf2go.NewGraph("http://localhost:3030/test/data")
	//g.Add(rdf2go.NewTriple(rdf2go.NewResource("a"), rdf2go.NewResource("b"), rdf2go.NewResource("c")))
	// Look up one triple matching the given subject
	triples2 := g.All(nil, nil, nil) //
	log.Println(len(triples2))
	log.Println(g.Len())

	for _, triple := range triples2 {
		log.Println(triple.String())
		print("h")
	}
}

func loadFromFile() {
	// Set a base URI
	baseUri := "www.example.org"

	// Create a new graph
	t := rdf2go.NewGraph(baseUri)
	r, err := os.Open("./smart_tv.n3")

	// r is of type io.Reader
	err = t.Parse(r, "text/turtle")
	if err != nil {
		log.Fatal(err)
	}
	log.Println(t.Len())
	// Look up one triple matching the given subject
	triples2 := t.All(nil, rdf2go.NewResource("http://www.w3.org/2000/01/rdf-schema#subClassOf"), rdf2go.NewResource("http://gsi.dit.upm.es/ontologies/ewe/ns/Channel")) //
	log.Println(len(triples2))
	g := rdf2go.NewGraph(baseUri)

	for _, triple := range triples2 {
		log.Println(triple.String())
		print("j")
		g.Add(triple)

	}
	f, err := os.Create("./a.json-ld")

	t.Serialize(f, "application/ld+json")
}
