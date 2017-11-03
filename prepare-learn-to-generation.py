import random
import json
import re
import os

def process_sentdata_baseline(data, datasplit, 
                              f_sym_train_complex, f_sym_train_compsem, f_sym_train_simple, f_sym_train_simpsem, 
                              f_sym_validation_complex, f_sym_validation_compsem, f_sym_validation_simple, f_sym_validation_simpsem,
                              f_sym_test_complex, f_sym_test_compsem, f_sym_test_simple, f_sym_test_simpsem):

    data = data.strip().split("\n\n")
    
    complexsentdata = data[0].strip().split("\n")
    complexid = int(complexsentdata[0].split("-")[1].strip())
    complexsent = complexsentdata[1].strip()
    # print complexsentdata

    mr_dict = {}
    # Collect all complex mrs
    for item in data[1:]:
        if re.match('COMPLEX-'+str(complexid)+':MR-[0-9]*\n', item):
            # print item
            mrdata = item.strip().split("\n")
            mrid = mrdata[0]
            mr = mrdata[1]
            mr_dict[mrid] = [mr, {}]
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
            
            for catdata in catlist:
                temp = catdata.strip().split("\n")
                
                mrsinfo = "category="+temp[0].strip()
                ssent = " ".join(temp[1:])
                # print mrsinfo
                # print ssent
                
                if mrsinfo not in mr_dict[mrid][1]:
                    mr_dict[mrid][1][mrsinfo] = [ssent]
                else:
                    if ssent not in mr_dict[mrid][1][mrsinfo]:
                        mr_dict[mrid][1][mrsinfo].append(ssent)


                # if len(temp[1:]) > 1 and "SPTYPE-NONE" not in item:
                #     exit(0)

    # print mr_dict

    complexid = int(complexsentdata[0].split("-")[1].strip())
    complexsent = complexsentdata[1].strip()

    if complexid in datasplit["TEST"]:
        # Test example
        for mrid in mr_dict:
            mrcinfo = mr_dict[mrid][0]
            for mrsinfo in mr_dict[mrid][1]:
                for ssent in mr_dict[mrid][1][mrsinfo]:
                    f_sym_test_complex.write(complexsent+"\n")
                    f_sym_test_compsem.write(mrcinfo+"\n")
                    f_sym_test_simple.write(ssent+"\n")
                    f_sym_test_simpsem.write(mrsinfo+"\n")

    elif complexid in datasplit["VALIDATION"]:
        # Validation 
        for mrid in mr_dict:
            mrcinfo = mr_dict[mrid][0]
            for mrsinfo in mr_dict[mrid][1]:
                for ssent in mr_dict[mrid][1][mrsinfo]:
                    f_sym_validation_complex.write(complexsent+"\n")
                    f_sym_validation_compsem.write(mrcinfo+"\n")
                    f_sym_validation_simple.write(ssent+"\n")
                    f_sym_validation_simpsem.write(mrsinfo+"\n")
    else:
        # Train
         for mrid in mr_dict:
            mrcinfo = mr_dict[mrid][0]
            for mrsinfo in mr_dict[mrid][1]:
                for ssent in mr_dict[mrid][1][mrsinfo]:
                    f_sym_train_complex.write(complexsent+"\n")
                    f_sym_train_compsem.write(mrcinfo+"\n")
                    f_sym_train_simple.write(ssent+"\n")
                    f_sym_train_simpsem.write(mrsinfo+"\n")


if __name__ == "__main__":

    with open('benchmark/Split-train-dev-test.DONT-CHANGE.json') as data_file:
        datasplit = json.load(data_file)
        
    print len(datasplit["TEST"]), len(datasplit["VALIDATION"]), len(datasplit["TRAIN"])
    
    # Prepare generation module datasets   
    f_sym_train_complex = open("mymodel/generation-module/train.complex", "w")
    f_sym_train_compsem = open("mymodel/generation-module/train.complex-semantics", "w")
    f_sym_train_simple = open("mymodel/generation-module/train.simple", "w")    
    f_sym_train_simpsem = open("mymodel/generation-module/train.simple-semantics", "w")
    
    f_sym_validation_complex = open("mymodel/generation-module/validation.complex", "w")
    f_sym_validation_compsem = open("mymodel/generation-module/validation.complex-semantics", "w")
    f_sym_validation_simple = open("mymodel/generation-module/validation.simple", "w")    
    f_sym_validation_simpsem = open("mymodel/generation-module/validation.simple-semantics", "w")
    
    f_sym_test_complex = open("mymodel/generation-module/test.complex", "w")
    f_sym_test_compsem = open("mymodel/generation-module/test.complex-semantics", "w")
    f_sym_test_simple = open("mymodel/generation-module/test.simple", "w")    
    f_sym_test_simpsem = open("mymodel/generation-module/test.simple-semantics", "w")

    with open("benchmark/final-complexsimple-meanpreserve-intreeorder-full.txt") as f:
        
        sentdata = []

        for line in f:
            if len(sentdata) == 0:
                print line
                sentdata.append(line)
            else:
                if re.match('COMPLEX-[0-9]*\n', line):
                    process_sentdata_baseline("".join(sentdata), datasplit, 
                                              f_sym_train_complex, f_sym_train_compsem, f_sym_train_simple, f_sym_train_simpsem, 
                                              f_sym_validation_complex, f_sym_validation_compsem, f_sym_validation_simple, f_sym_validation_simpsem,
                                              f_sym_test_complex, f_sym_test_compsem, f_sym_test_simple, f_sym_test_simpsem)
                    
                    # exit(0)
                    
                    print line
                    sentdata = [line]
                else:
                    sentdata.append(line)
            
        # Process last sentdata
        process_sentdata_baseline("".join(sentdata), datasplit, 
                                  f_sym_train_complex, f_sym_train_compsem, f_sym_train_simple, f_sym_train_simpsem, 
                                  f_sym_validation_complex, f_sym_validation_compsem, f_sym_validation_simple, f_sym_validation_simpsem,
                                  f_sym_test_complex, f_sym_test_compsem, f_sym_test_simple, f_sym_test_simpsem)
    f_sym_train_complex.close()
    f_sym_train_compsem.close()
    f_sym_train_simple.close() 
    f_sym_train_simpsem.close()
    
    f_sym_validation_complex.close()
    f_sym_validation_compsem.close()
    f_sym_validation_simple.close() 
    f_sym_validation_simpsem.close() 
    
    f_sym_test_complex.close()
    f_sym_test_compsem.close()
    f_sym_test_simple.close()
    f_sym_test_simpsem.close()
   
