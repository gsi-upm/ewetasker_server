from data.sparql.channels import *
from data.sparql.actions import *
from data.sparql.parameters import *
from data.sparql.events import *
from rdflib import Graph
import json

# get base channels
def get_base_channels():

    channels = {"@context": { "@vocab" : "http://www.gsi.dit.upm.es/ontologies/ewe#"}, "channels" : []}
    channels_result = get_all_base_channels()

    index = 0
    for uri, label, comment, logo in channels_result:

        channels["channels"].append({"@id" : uri, "rdfs:label" : label.n3(), "rdfs:comment" : comment.n3(), "foaf:logo" : logo.n3(), "events" : [], "actions" : [], "parameters" : []})

        actions_result = get_channel_actions(uri)  
        action_index = 0

        for action_uri, action_label, action_comment in actions_result:

            channels["channels"][index]["actions"].append({"@id" : action_uri, "rdfs:label" : action_label.n3(), "rdfs:comment" : action_comment.n3(), "input_parameters" : [], "output_parameters" : []})

            # get input parameters
            input_params_result = get_input_parameters(action_uri, uri)
            for input_param_uri, input_param_label, input_param_comment in input_params_result:
                channels["channels"][index]["actions"][action_index]["input_parameters"].append({"@id" : input_param_uri, "rdfs:label" : input_param_label.n3(), "rdfs:comment" : input_param_comment.n3()})

            # get output parameters
            output_params_result = get_output_parameters(action_uri, uri)
            for output_param_uri, output_param_label, output_param_comment in output_params_result:
                channels["channels"][index]["actions"][action_index]["output_parameters"].append({"@id" : output_param_uri, "rdfs:label" : output_param_label.n3(), "rdfs:comment" : output_param_comment.n3()})

            action_index+=1

        # get events
        events_result = get_channel_events(uri)
        event_index = 0

        for event_uri, event_label, event_comment in events_result:
            channels["channels"][index]["events"].append({"@id" : event_uri, "rdfs:label" : event_label.n3(), "rdfs:comment" : event_comment.n3(), "input_parameters" : [], "output_parameters" : []})
            
            # get input parameters
            input_params_result = get_input_parameters(action_uri, uri)

            for input_param_uri, input_param_label, input_param_comment in input_params_result:
                channels["channels"][index]["events"][event_index]["input_parameters"].append({"@id" : input_param_uri, "rdfs:label" : input_param_label.n3(), "rdfs:comment" : input_param_comment.n3()})

            # get output parameters
            output_params_result = get_output_parameters(action_uri, uri)

            for output_param_uri, output_param_label, output_param_comment in output_params_result:
                channels["channels"][index]["events"][event_index]["output_parameters"].append({"@id" : output_param_uri, "rdfs:label" : output_param_label.n3(), "rdfs:comment" : output_param_comment.n3()})

            event_index+=1

        # get channel parameters
        parameters_result = get_channel_parameters(uri)
        for param_uri, param_label, param_comment in parameters_result:
            channels["channels"][index]["parameters"].append({"@id" : param_uri, "rdfs:label" : param_label.n3(), "rdfs:comment" : param_comment.n3()})

        index+=1
    

    return json.dumps(channels).replace('\\"', "")

# get  channels
def get_custom_channels():

    channels = {"@context": { "@vocab" : "http://www.gsi.dit.upm.es/ontologies/ewe#"}, "channels" : []}
    channels_result = get_all_custom_channels()

    index = 0
    for uri, label, comment, baseChannel, logo in channels_result:

        channels["channels"].append({"@id" : uri, "rdfs:label" : label.n3(), "rdfs:comment" : comment.n3(), "foaf:logo" : logo.n3(), "rdfs:type" : baseChannel, "parameters" : []})

        parameters_result = get_custom_channel_parameters(uri)
        for param_uri, param_label, param_value in parameters_result:
            channels["channels"][index]["parameters"].append({"@id" : param_uri, "rdfs:label" : param_label.n3(), "rdf:value" : param_value.n3()})

        index+=1
    
    
    return json.dumps(channels).replace('\\"', "")

def import_new_channel(channel_json):
    channel_label = channel_json["rdfs:label"]
    channel_comment = channel_json["rdfs:comment"]
    channel_type = channel_json["rdf:type"]
    channel_base = channel_json["@context"]["@base"]
    channel_parameters = channel_json["parameters"]

    return create_channel(channel_base, channel_label.replace(" ", "").lower(), channel_type, channel_label, channel_comment, channel_parameters)