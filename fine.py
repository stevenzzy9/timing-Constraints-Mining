from pm4py.objects.log.importer.xes import factory as xes_importer
from pm4py.algo.discovery.alpha import factory as alpha_miner
from pm4py.visualization.petrinet import factory as pn_vis_factory
from pm4py.algo.conformance.alignments import factory as alignments
from pm4py.algo.discovery.inductive import factory as induct_miner
from pm4py.algo.discovery.heuristics import factory as heurs_miner
import datetime
import time
from collections import defaultdict
from pm4py.algo.discovery.simple.model.log import factory as simple_algorithm

# log = xes_importer.apply("testData.xes")
log = xes_importer.apply("data.xes")

# //discover petri net by alpha algorithm
# net, initial_marking, final_marking = simple_algorithm.apply(log, classic_output=True, parameters={"max_no_variants": 20})
# gviz = pn_vis_factory.apply(net, initial_marking, final_marking)
# pn_vis_factory.view(gviz)

# //discover petri net by induct miner
# net, im, fm= induct_miner.apply(log)
# gviz = pn_vis_factory.apply(net, im, fm)
# pn_vis_factory.view(gviz)

# //discover petri net by alpha
# net, im, fm = alpha_miner.apply(log)
# gviz = pn_vis_factory.apply(net, im, fm)
# pn_vis_factory.view(gviz)

# // read xes file
# first_trace_concept_name = log[0].attributes["concept:name"]
# first_event_first_trace_concept_name = log[0][0]["time:timestamp"].strftime("%m,%d,%H,%M")
#
# print("first_trace_concept_name is" + first_trace_concept_name + " " + "first_event_first_trace_concept_name " + first_event_first_trace_concept_name)
#

# import dependence table
dependence = {}
timeConstrain = {}
error=[]
with open('dependence.txt','r') as f:
    for line in f:
        dependence[line.split(":")[0]] = line.split(":")[1].split('\n')[0].split(",")
        timeConstrain[line.split(":")[0]] =[1000,0]

for key in dependence:
    print(dependence[key])
    print(timeConstrain[key])
for case_index, case in enumerate(log):
    if case_index > 2:
        break
    else:
        print("\n case index: %d  case id: %s" % (case_index, case.attributes["concept:name"]))
        for event_index, event in enumerate(case):
            print("event index: %d  event activity: %s  event timestamp stamp: %s" % (event_index, event["concept:name"],event["time:timestamp"].strftime("%m,%d")))
            if event_index >= 1:
                delta = event["time:timestamp"]-log[case_index][event_index-1]["time:timestamp"]
                print(delta.days)

for case_index, case in enumerate(log):
        print("\n case index: %d  case id: %s" % (case_index, case.attributes["concept:name"]))
        for event_index, event in enumerate(case):
            if event_index >= 1:
                if event["concept:name"] not in dependence.keys():
                    break
                for i in range(event_index-1,-1,-1):
                    # print(i)
                    # print(log[case_index][i]["concept:name"])
                    # print(dependence[event["concept:name"]])
                    if log[case_index][i]["concept:name"] in dependence[event["concept:name"]]:
                        delta = event["time:timestamp"] - log[case_index][i]["time:timestamp"]
                        # if delta.days > 300:
                        #     print("current name:"  + event["concept:name"] + " current time:" + event["time:timestamp"].strftime("%y,%m,%d") + " per event" + log[case_index][i]["time:timestamp"].strftime("%y,%m,%d") )
                        if delta.days < timeConstrain[event["concept:name"]][0]:
                            timeConstrain[event["concept:name"]][0] = delta.days
                        if delta.days > timeConstrain[event["concept:name"]][1]:
                            timeConstrain[event["concept:name"]][1] = delta.days
                        break


for key in dependence:
    # print(dependence[key])
    print(key + " : " + str(timeConstrain[key]))
