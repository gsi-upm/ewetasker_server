# EWE Tasker Server

This repository contains EWE Tasker Server module, written in Golang.

## API CALLS

| Route | Method | Description |
|---|---|---|
| /channels  | GET  | Get a list of base channels available at the platform  |
| /channels/user/{userID}  | GET  |  Get a list of channels available for the specified user |
| /channels/place/{placeID}  | GET  | Get a list of channels available at the platform associated to a certain place |
| /channels/new  | POST  | Create a new channel |
| /rules  | GET  | Get a list of rules available at the platform  |
| /rules/user/{userID}  | GET  | Get a list of rules available at the platform for the specified user |
| /rules/new | POST  | Create a new rule |
| /rules/place/{placeID}  | GET  | Get a list of rules available at the platform associated to a certain place |
| /event/evaluate  | POST  | Evaluate an event |

## Get Channels

```
[
   {
      "@id":"http://gsi.dit.upm.es/ontologies/ewe-connected-home-smarttv/ns/SmartTv",
      "rdfs:label":"\"Connected door-lock\"@en",
      "rdfs:comment":"\"This channel represents a simplified smarttv with simple capabilities\"",
      "events":[

      ],
      "actions":[
         {
            "@id":"http://gsi.dit.upm.es/ontologies/ewe-connected-home-smarttv/ns/SwitchOn",
            "rdfs:label":"\"Switch on\"@en",
            "rdfs:comment":"\"This action will switch on the TV.\"@en",
            "input_parameters":[
               {
                  "@id":"http://gsi.dit.upm.es/ontologies/ewe-connected-home-smarttv/ns/LocalIP",
                  "rdfs:label":"\"Local IP\"@en",
                  "rdfs:comment":"\"This parameter represents the local IP of the TV.\"@en"
               },
               {
                  "@id":"http://gsi.dit.upm.es/ontologies/ewe-connected-home-smarttv/ns/PublicIP",
                  "rdfs:label":"\"Public IP\"@en",
                  "rdfs:comment":"\"This parameter represents the public IP of the TV.\"@en"
               }
            ],
            "output_parameters":[

            ]
         },
         {
            "@id":"http://gsi.dit.upm.es/ontologies/ewe-connected-home-smarttv/ns/SwitchOff",
            "rdfs:label":"\"Switch off\"@en",
            "rdfs:comment":"\"This action will switch off the TV.\"@en",
            "input_parameters":[
               {
                  "@id":"http://gsi.dit.upm.es/ontologies/ewe-connected-home-smarttv/ns/LocalIP",
                  "rdfs:label":"\"Local IP\"@en",
                  "rdfs:comment":"\"This parameter represents the local IP of the TV.\"@en"
               },
               {
                  "@id":"http://gsi.dit.upm.es/ontologies/ewe-connected-home-smarttv/ns/PublicIP",
                  "rdfs:label":"\"Public IP\"@en",
                  "rdfs:comment":"\"This parameter represents the public IP of the TV.\"@en"
               }
            ],
            "output_parameters":[

            ]
         },
         {
            "@id":"http://gsi.dit.upm.es/ontologies/ewe-connected-home-smarttv/ns/DisplayImage",
            "rdfs:label":"\"Display image\"@en",
            "rdfs:comment":"\"This action will display an image on the screen.\"@en",
            "input_parameters":[
               {
                  "@id":"http://gsi.dit.upm.es/ontologies/ewe-connected-home-smarttv/ns/LocalIP",
                  "rdfs:label":"\"Local IP\"@en",
                  "rdfs:comment":"\"This parameter represents the local IP of the TV.\"@en"
               },
               {
                  "@id":"http://gsi.dit.upm.es/ontologies/ewe-connected-home-smarttv/ns/PublicIP",
                  "rdfs:label":"\"Public IP\"@en",
                  "rdfs:comment":"\"This parameter represents the public IP of the TV.\"@en"
               }
            ],
            "output_parameters":[

            ]
         }
      ],
      "parameters":[
         {
            "@id":"http://gsi.dit.upm.es/ontologies/ewe-connected-home-smarttv/ns/LocalIP",
            "rdfs:label":"\"Local IP\"@en",
            "rdfs:comment":"\"This parameter represents the local IP of the TV.\"@en"
         },
         {
            "@id":"http://gsi.dit.upm.es/ontologies/ewe-connected-home-smarttv/ns/PublicIP",
            "rdfs:label":"\"Public IP\"@en",
            "rdfs:comment":"\"This parameter represents the public IP of the TV.\"@en"
         }
      ]
   }
]
```