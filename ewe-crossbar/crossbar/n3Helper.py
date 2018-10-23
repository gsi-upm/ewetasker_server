import objectpath
import json,requests,time
import pprint
import re


class N3Helper():
    
    def getEvent(self, params):
        prefix = "@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>. @prefix ewe: <http://gsi.dit.upm.es/ontologies/ewe/ns/>. @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>. @prefix string: <http://www.w3.org/2000/10/swap/string#>. @prefix math: <http://www.w3.org/2000/10/swap/math#>. "
        ewe_uri="http://gsi.dit.upm.es/ontologies/ewe/ns/"

        event = prefix+" ewe:"+params['event']+" rdf:type <"+ewe_uri+params['event']+">;"
        event += " rdf:type ewe:Event; rdfs:domain <"+ewe_uri+params['channel']+">;"
        if not params['params']:
            event += "."
        else:
            event += "."
            for parameter in params['params']:
                event +=" ewe:"+params['event']+" ewe:hasParameter ewe:"+parameter+"."
                event += " ewe:"+parameter+" rdf:type <"+ewe_uri+parameter+">; rdf:value "
                if type(params['params'][parameter]) is int:
                    event +=""+str(params['params'][parameter]) +"."
                else:
                    event += "\""+params['params'][parameter] +"\"."
        event += "  { ?A ?B ?C } => { ?A ?B ?C }. " 
        
        return event



