
# Run with python 3
# Assumes that first one is the root

import json
import os
import xml.etree.ElementTree as ET
import itertools
import re

def indent(elem, level=0):
  i = "\n" + level*"  "
  if len(elem):
    if not elem.text or not elem.text.strip():
      elem.text = i + "  "
    if not elem.tail or not elem.tail.strip():
      elem.tail = i
    for elem in elem:
      indent(elem, level+1)
    if not elem.tail or not elem.tail.strip():
      elem.tail = i
  else:
    if level and (not elem.tail or not elem.tail.strip()):
      elem.tail = i

def extract_entry_data(entry): #, text_corenlp_dict):
    entry_data = []
    entry_data.append(entry.attrib)
    
    originaltripleset = []
    for item in entry.iter('originaltripleset'):
        originaltripleset.append(item)
    entry_data.append(originaltripleset)

    modifiedtripleset = []
    for item in entry.iter('modifiedtripleset'):
        modifiedtripleset.append(item)
    entry_data.append(modifiedtripleset)
    
    # lex_data = {}
    # for item in entry.iter('lex'):
    #     if item.text.strip() not in text_corenlp_dict:
    #         print("lex item not in corenlp dict.")
    #         exit(0)
    #     # this removes duplicates if any
    #     lex_data[item.text.strip()] = text_corenlp_dict[item.text.strip()][:]
    # entry_data.append(lex_data)    
    

    return entry_data

def build_forest( nodelist ):
    forest = [] 
    nodes = {}  

    id = 'id'
    children = 'children'

    for node_id, parent_id in nodelist:
        # print("shashi: ", node_id, parent_id)
        
        #create current node if necessary
        if not node_id in nodes:
            node = { id : node_id }
            nodes[node_id] = node
        else:
            node = nodes[node_id]

        if node_id == parent_id:
            #add node to forrest
            forest.append( node )
        else:
            #create parent node if necessary
            if not parent_id in nodes:
                parent = { id : parent_id }
                nodes[parent_id] = parent
            else:
                parent = nodes[parent_id]
            #create children if necessary
            if not children in parent:
                parent[children] = []
            #add node to children of parent
            parent[children].append( node )

        # print("shashi F: ",forest)
        # print("shashi N: ",nodes)

    return forest  
  
def traverse_depthfirst(finaltree):
    if len(finaltree) == 1:
        return finaltree["id"], ""

    strdepthfirst = ""
    for child in finaltree["children"]:
        child_id, child_shape = traverse_depthfirst(child)

        strdepthfirst += (finaltree["id"]+"|"+child_id+" ")
        if len(child_shape) != 0:
            strdepthfirst += child_shape
    
    return finaltree["id"], strdepthfirst

def get_strdepthfirst(modifiedtripleset):
    # Identify parent node
    parents = {}
    nonparents = {}
    child_parent_list = [] # list of (child, parent)
    
    for mtriple in modifiedtripleset.iter('mtriple'):
        mtriple_text = (mtriple.text).split(" | ")
        # print(mtriple_text)
        
        parent = ""
        child = ""
        if mtriple_text[0] != mtriple_text[2]:
            parent = mtriple_text[0]
            child = mtriple_text[2]
        else:
            parent = mtriple_text[0]
            child = mtriple_text[2]+"-DUPLICATE"

        child_parent_list.append((child, parent))

        if parent not in nonparents:
            parents[parent] = 1
        nonparents[child] = 1
        if child in parents:
            del parents[child]
    
    if len(parents) != 1:
        # More than one parent: Not a tree
        return None
    else:    
        # APPEND PARENT INFO
        for item in list(parents.keys()):
            child_parent_list.append((item, item))
        # print(child_parent_list)

        forest = build_forest( child_parent_list )
        if len(forest) != 1:
            return None
            
        finaltree = forest[0]
        print(finaltree)
        _, strdepthfirst = traverse_depthfirst(finaltree)
        return strdepthfirst

def get_tree(modifiedtripleset):
    # Identify parent node
    parents = {}
    nonparents = {}
    child_parent_list = [] # list of (child, parent)
    
    for mtriple in modifiedtripleset.iter('mtriple'):
        mtriple_text = (mtriple.text).split(" | ")
        # print(mtriple_text)
        
        parent = ""
        child = ""
        if mtriple_text[0] != mtriple_text[2]:
            parent = mtriple_text[0]
            child = mtriple_text[2]
        else:
            parent = mtriple_text[0]
            child = mtriple_text[2]+"-DUPLICATE"

        child_parent_list.append((child, parent))

        if parent not in nonparents:
            parents[parent] = 1
        nonparents[child] = 1
        if child in parents:
            del parents[child]
    
    if len(parents) != 1:
        # More than one parent: Not a tree
        return None
    else:    
        # APPEND PARENT INFO
        for item in list(parents.keys()):
            child_parent_list.append((item, item))
        # print(child_parent_list)

        forest = build_forest( child_parent_list )
        if len(forest) != 1:
            return None
            
        finaltree = forest[0]
        return finaltree
      
def get_shape_nodedict(finaltree, prefix, nodedict):
  nodename =  prefix
  nodeval = finaltree["id"]
  nodedict[nodeval] = nodename
  treeshape = [nodename]
  if "children" in finaltree:
    for childid in range(len(finaltree["children"])):
      childshape, nodedict = get_shape_nodedict(finaltree["children"][childid], nodename+str(childid+1), nodedict)
      treeshape.append(childshape)

  return treeshape, nodedict

def map_tree_to_shape(finaltree, nodedict):
  treeshape = [nodedict[finaltree["id"]]]
  if "children" in finaltree:
    for childid in range(len(finaltree["children"])):
      childshape = map_tree_to_shape(finaltree["children"][childid], nodedict)
      treeshape.append(childshape)
  return treeshape
      
def process_sentdata_baseline(data, datasplit, mrid_modifiedtripleset_dict,
                              f_sym_train_complex, f_sym_train_compsem, f_sym_train_compshape, f_sym_train_split, f_sym_train_nodedict, f_sym_train_compid, 
                              f_sym_validation_complex, f_sym_validation_compsem, f_sym_validation_compshape, f_sym_validation_split, f_sym_validation_nodedict, f_sym_validation_compid, 
                              f_sym_test_complex, f_sym_test_compsem, f_sym_test_compshape, f_sym_test_split, f_sym_test_nodedict, f_sym_test_compid):

    data = data.strip().split("\n\n")
    
    complexsentdata = data[0].strip().split("\n")
    complexid = int(complexsentdata[0].split("-")[1].strip())
    complexsent = complexsentdata[1].strip()
    # print(complexsentdata)

    mr_dict = {}
    # Collect all complex mrs
    for item in data[1:]:
        if re.match('COMPLEX-'+str(complexid)+':MR-[0-9]*\n', item):
            # print item
            mrdata = item.strip().split("\n")
            mrid = mrdata[0]
            mr = mrdata[1]
            
            mr_tree = get_tree(mrid_modifiedtripleset_dict[mr])
            # print(mr_tree)
            mr_tree_shape, mr_tree_nodedict = get_shape_nodedict(mr_tree, "N1", {})
            # print(mr_tree_shape, mr_tree_nodedict)
            # mr_tree, mr_treemapping = get_strdepthfirst
            # print(mr_tree, mr_treemapping)

            mr_dict[mrid] = [mr, mr_tree_shape, mr_tree_nodedict, []]
            
    # print mr_dict
    
    # Collect all simple data for corresponding mrs
    for item in data[1:]:
        if re.match('COMPLEX-'+str(complexid)+':MR-[0-9]*:SIMPLE-[0-9]*:SPTYPE-', item):
            # print item
            # print 

            mrid = ":".join(item.strip().split("\n")[0].split(":")[:2])
            # print mrid
            
            catlist = item.strip().split("category=")[1:]
            # print catlist
            
            mrsinfo_list = []

            for catdata in catlist:
                temp = catdata.strip().split("\n")
                
                mrsinfo = "category="+temp[0].strip()
                # ssent = " ".join(temp[1:])
                # print mrsinfo
                # print ssent
                
                mrsinfo_tree = get_tree(mrid_modifiedtripleset_dict[mrsinfo])
                # print(mrsinfo_tree)

                mrsinfo_tree_shape = map_tree_to_shape(mrsinfo_tree, mr_dict[mrid][2])
                # print(mrsinfo_tree_shape)
              
                mrsinfo_list.append(str(mrsinfo_tree_shape))
              
            # print("\n\n")
            mrsinfo_str = " || ".join(mrsinfo_list)
            if mrsinfo_str not in mr_dict[mrid][3]:
              mr_dict[mrid][3].append(mrsinfo_str)
                
    # print(mr_dict)
    
    if complexid in datasplit["TEST"]:
        # Test example
        for mrid in mr_dict:
          mrcinfo = mr_dict[mrid][0]
          mrcshape = mr_dict[mrid][1]
          mrcnodedict = mr_dict[mrid][2]
          for mrsshapes in mr_dict[mrid][3]:
            f_sym_test_complex.write(complexsent+"\n")
            f_sym_test_compsem.write(mrcinfo+"\n")
            f_sym_test_compshape.write(str(mrcshape)+"\n")
            f_sym_test_split.write(mrsshapes+"\n")
            f_sym_test_nodedict.write(str(mrcnodedict)+"\n")
            f_sym_test_compid.write(str(complexid)+"\n")

    elif complexid in datasplit["VALIDATION"]:
      # Validation 
      for mrid in mr_dict:
        mrcinfo = mr_dict[mrid][0]
        mrcshape = mr_dict[mrid][1]
        mrcnodedict = mr_dict[mrid][2]
        for mrsshapes in mr_dict[mrid][3]:
          f_sym_validation_complex.write(complexsent+"\n")
          f_sym_validation_compsem.write(mrcinfo+"\n")
          f_sym_validation_compshape.write(str(mrcshape)+"\n")
          f_sym_validation_split.write(mrsshapes+"\n")
          f_sym_validation_nodedict.write(str(mrcnodedict)+"\n")
          f_sym_validation_compid.write(str(complexid)+"\n")

    else:
      # Train
      for mrid in mr_dict:
        mrcinfo = mr_dict[mrid][0]
        mrcshape = mr_dict[mrid][1]
        mrcnodedict = mr_dict[mrid][2]
        for mrsshapes in mr_dict[mrid][3]:
          f_sym_train_complex.write(complexsent+"\n")
          f_sym_train_compsem.write(mrcinfo+"\n")
          f_sym_train_compshape.write(str(mrcshape)+"\n")
          f_sym_train_split.write(mrsshapes+"\n")
          f_sym_train_nodedict.write(str(mrcnodedict)+"\n")
          f_sym_train_compid.write(str(complexid)+"\n")

if __name__ == "__main__":

  print("Step A: Read all WebNLG entries and build mrid and mr representation dict")
  topdir = "benchmark/benchmark_verified_simplifcation"
  mrid_modifiedtripleset_dict = {}
  for item in range(1,8):
    finaldir = topdir+"/"+str(item)+"triples"
    for filename in os.listdir(finaldir):
      print(finaldir + "/" + filename)
      tree = ET.parse(finaldir + "/" + filename)
      root = tree.getroot()            
      for entry in root.iter('entry'):
        entry_data = extract_entry_data(entry) # , text_corenlp_dict)

        mrid = "category="+entry_data[0]["category"]+" eid="+entry_data[0]["eid"]+" size="+entry_data[0]["size"]
        modifiedtripleset = entry_data[2][0]
        
        mrid_modifiedtripleset_dict[mrid] = modifiedtripleset
  print(len(mrid_modifiedtripleset_dict))
  
  print("\nStep B: Read training, dev and test splits")
  with open('benchmark/Split-train-dev-test.DONT-CHANGE.json') as data_file:            
    datasplit = json.load(data_file)
  print(len(datasplit["TEST"]), len(datasplit["VALIDATION"]), len(datasplit["TRAIN"]))

  print("\nStep C: Start reading final simplification dataset")
  
  f_sym_train_complex = open("mymodel/partition-module/train.complex", "w")
  f_sym_train_compsem = open("mymodel/partition-module/train.complex-semantics", "w")
  f_sym_train_compshape = open("mymodel/partition-module/train.complex-shape", "w")    
  f_sym_train_split = open("mymodel/partition-module/train.split", "w")
  f_sym_train_nodedict = open("mymodel/partition-module/train.nodedict", "w")
  f_sym_train_compid = open("mymodel/partition-module/train.complex-id", "w")

  f_sym_validation_complex = open("mymodel/partition-module/validation.complex", "w")
  f_sym_validation_compsem = open("mymodel/partition-module/validation.complex-semantics", "w")
  f_sym_validation_compshape = open("mymodel/partition-module/validation.complex-shape", "w")    
  f_sym_validation_split = open("mymodel/partition-module/validation.split", "w")
  f_sym_validation_nodedict = open("mymodel/partition-module/validation.nodedict", "w")
  f_sym_validation_compid = open("mymodel/partition-module/validation.complex-id", "w")

  f_sym_test_complex = open("mymodel/partition-module/test.complex", "w")
  f_sym_test_compsem = open("mymodel/partition-module/test.complex-semantics", "w")
  f_sym_test_compshape = open("mymodel/partition-module/test.complex-shape", "w")    
  f_sym_test_split = open("mymodel/partition-module/test.split", "w")
  f_sym_test_nodedict  = open("mymodel/partition-module/test.nodedict", "w")
  f_sym_test_compid = open("mymodel/partition-module/test.complex-id", "w")

  with open("benchmark/final-complexsimple-meanpreserve-intreeorder-full.txt") as f:
    sentdata = []
    for line in f:
      if len(sentdata) == 0:
        print(line)
        sentdata.append(line)
      else:
        if re.match('COMPLEX-[0-9]*\n', line):
          process_sentdata_baseline("".join(sentdata), datasplit, mrid_modifiedtripleset_dict,
                                    f_sym_train_complex, f_sym_train_compsem, f_sym_train_compshape, f_sym_train_split, f_sym_train_nodedict, f_sym_train_compid, 
                                    f_sym_validation_complex, f_sym_validation_compsem, f_sym_validation_compshape, f_sym_validation_split, f_sym_validation_nodedict, f_sym_validation_compid,
                                    f_sym_test_complex, f_sym_test_compsem, f_sym_test_compshape, f_sym_test_split, f_sym_test_nodedict, f_sym_test_compid)
          
          # exit(0)
          
          print(line)
          sentdata = [line]
        else:
          sentdata.append(line)
            
    # Process last sentdata
    process_sentdata_baseline("".join(sentdata), datasplit, mrid_modifiedtripleset_dict,
                              f_sym_train_complex, f_sym_train_compsem, f_sym_train_compshape, f_sym_train_split, f_sym_train_nodedict, f_sym_train_compid, 
                              f_sym_validation_complex, f_sym_validation_compsem, f_sym_validation_compshape, f_sym_validation_split, f_sym_validation_nodedict, f_sym_validation_compid,
                              f_sym_test_complex, f_sym_test_compsem, f_sym_test_compshape, f_sym_test_split, f_sym_test_nodedict, f_sym_test_compid)
    
  f_sym_train_complex.close()
  f_sym_train_compsem.close()
  f_sym_train_compshape.close() 
  f_sym_train_split.close()
  f_sym_train_nodedict.close()
  f_sym_train_compid.close()

  f_sym_validation_complex.close()
  f_sym_validation_compsem.close()
  f_sym_validation_compshape.close() 
  f_sym_validation_split.close() 
  f_sym_validation_nodedict.close()
  f_sym_validation_compid.close()

  f_sym_test_complex.close()
  f_sym_test_compsem.close()
  f_sym_test_compshape.close()
  f_sym_test_split.close()
  f_sym_test_nodedict.close()
  f_sym_test_compid.close()
  
  
  
  
  
  
