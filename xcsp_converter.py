import os
import xml.etree.cElementTree as ET

from xml.etree import ElementTree
from xml.dom import minidom

def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")


## Parse .txt files

domains_data = []

# Open dom.txt
with open("dom.txt","r") as dom:
    #Store each line in a line
    lines = [line.rstrip('\n') for line in dom]
    #Process each line
    for line in lines:
        domains_data.append(line.split())

variables_data = []

with open("var.txt", "r") as var:
    lines = [line.rstrip('\n') for line in var]
    for line in lines:
        variables_data.append(line.split())

constraints_data = []

with open("ctr.txt", "r") as ctr:
    lines = [line.rstrip('\n') for line in ctr]
    for line in lines:
        constraints_data.append(line.split())

## Build the xcsp file

instance = ET.Element('instance', {'xmlns:xsi':"http://www.w3.org/2001/XMLSchema-instance",
                                   'xsi:noNamespaceSchemaLocation':"src/frodo2/algorithms/XCSPschema.xsd"
                                   })

# Generate agents section
agents = ET.SubElement(instance, "agents", {"nbAgents":str(len(variables_data))})

for a in variables_data:
    ET.SubElement(agents,"agent",{"name":"F{}".format(a[0])})

# Generate domains section
domains = ET.SubElement(instance, "domains", {"nbDomains":str(len(domains_data))})

for d in domains_data:
    nb = d.pop(0)
    ET.SubElement(domains, "domain", {"name":"domain{}".format(nb),
        "nbValues":str(len(d))})\
        .text = " ".join(d)

variables = ET.SubElement(instance, "variables", {"nbVariables":str(len(variables_data))})

for v in variables_data:
    ET.SubElement(variables, "variable", {"name":"x{}".format(v[0]),
        "domain":"domain{}".format(v[1]),
        "agent":"F{}".format(v[0])})

predicates_data = [
        {
                "name":"SUP",
                "parameters": "int X1 int X2 int K",
                "function": "gt(abs(sub(X1, X2)), K)"
        },
        {
                "name":"EQ",
                "parameters": "int X1 int X2 int K",
                "function": "eq(abs(sub(X1, X2)), K)"
        }
]

predicates = ET.SubElement(instance, "predicates", {"nbPredicates":str(len(predicates_data))})
for p in predicates_data:
        p_tmp = ET.SubElement(predicates, "predicate", {"name":p["name"]})
        param_tmp = ET.SubElement(p_tmp, "parameters").text = p["parameters"]
        exp_tmp = ET.SubElement(p_tmp, "expression")
        funct_tmp = ET.SubElement(exp_tmp, "functional").text = p["function"]

constraints = ET.SubElement(instance, "constraints", {"nbConstraints":str(len(constraints_data))})

for c in constraints_data:
        ctr_tmp = ET.SubElement(constraints, "constraint",{
                "name":"x{}_x{}".format(c[0],c[1]),
                "scope":"x{} x{}".format(c[0],c[1]),
                "arity":"2",
                "reference":"{}".format("EQ" if c[3] == "=" else "SUP")
        })
        param_tmp = ET.SubElement(ctr_tmp,"parameter").text = "x{} x{} {}".format(c[0], c[1], c[4])


print(prettify(instance))