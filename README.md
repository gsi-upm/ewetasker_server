# EWE Tasker Server

This repository contains EWE Tasker Server module, written in Python.

## INSTALLATION

### REQUIREMENTS
In order to install Ewetasker server, it is needed to have installed docker-compose. Follow this [link](https://docs.docker.com/compose/install/) if you need more information about it.

### STEP BY STEP

First of all, clone the git project locally and access to Ewetasker server directory.

```
$ git clone https://lab.cluster.gsi.dit.upm.es/ewe/ewetasker_server.git ewetasker_server
```

Once made it, access to ewetasker_server directory.

```
$ cd ewetasker_server
```

Ewetasker communicates with the web application using jwt tokens, so it is needed to encode the data with a .pem file. If you have your own .key and .csr files, you only need to create a .pem file; otherwise, you need to install openssl and follow the next steps:

```
$ cd ewetasker
$ mkdir certs
$ cd certs
$ openssl genrsa -out ewetasker.pem 2048
```

Then you must modify the config.ini file, to change the path to the .pem file with the name you have choosen.

```
[CERTS]

BASE_PATH = certs/ewetasker.pem
```

Once made it, go back to /ewetasker_server and launch docker-compose.

```
$ docker-compose up --build
```

When build process finishes, access to Fuseki service in localhost:3030 to upload the .n3 files. Fuseki credentials are "admin" and "ewefuseki".

Click on "manage datasets" and then "add new dataset". You must name the dataset as "ewetasker", and choose "persistent" option.

![fuseki_1](./img/fuseki_1.png)

Then, click on "upload data" and select .n3 files contained in "vocabularies" folder. To finish click on "upload all".

![fuseki_2](./img/fuseki_2.png)

At this point, you can test your installation by making a GET Request to localhost:5050.

```
curl -i -H "Accept: application/json" -H "Content-Type: application/json" -X GET http://localhost:5050/channels/base
```

The response must be like this:

```
{"@context": {"@vocab": "http://www.gsi.dit.upm.es/ontologies/ewe#"}, "channels": [{"@id": "http://gsi.dit.upm.es/ontologies/ewe/ns/CMS", "rdfs:label": "Content Management System", "rdfs:comment": "This channel represents a Content Management System.", "foaf:logo": "fa fa-newspaper-o", "events": [], "actions": [{"@id": "http://gsi.dit.upm.es/ontologies/ewe/ns/ShowContent", "rdfs:label": "Show content generated", "rdfs:comment": "This action will show the content page created.", "input_parameters": [], "output_parameters": [{"@id": "http://gsi.dit.upm.es/ontologies/ewe/ns/ContentID", "rdfs:label": "Content ID", "rdfs:comment": "This parameter represents the content ID.", "rdf:datatype": "http://www.w3.org/2001/XMLSchema#string"}]}], "parameters": []}, ...
```

In order to interact with Ewetasker server in a simple way, you can install Ewetasker web application in this [link](https://lab.cluster.gsi.dit.upm.es/ewe/ewetasker_webclient).

## API CALLS

| Route | Method | Description |
|---|---|---|
| /channels/base  | GET  | Get a list of base channels available at the platform  |
| /channels/category/{categoryUri}  | GET  | Get a list by category (Services or Devices) of channels available at the platform  |
| /channels/custom  | GET  | Get a list of custom channels available at the platform  |
| /channels/custom/category/{categoryUri}  | GET  | Get a list by category (Services or Devices) of custom channels available at the platform  |
| /channels/import  | POST  | Import a new custom channel from a json |
| /channels/custom/delete/{customChannelUri}  | DELETE  | Delete a custom channel |
| /rules/new | POST  | Create a new rule from a json|
| /rules/user/{userUri}  | GET  | Get a list of rules available at the platform for the specified user |
| /rules/delete/{ruleUri}  | DELETE  | Delete a custom channel |
| /users/new | POST  | Create a new user|
| /users/login | POST  | Login at platform|
| /users/delete  | DELETE  | Delete a user |
| /evaluate  | POST  | Evaluate an event |

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

# License
   Copyright 2018 Sergio Muñoz López and Carlos A. Iglesias Fernández.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.