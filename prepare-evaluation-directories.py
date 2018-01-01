import random
import json
import re
import os


def process_sentdata(data, datasplit):

    data = data.strip().split("\n\n")

    complexsentdata = data[0].strip().split("\n")
    complexid = int(complexsentdata[0].split("-")[1].strip())
    print complexid

    simpsents = {}
    for item in data[1:]:
        if re.match('COMPLEX-' + str(complexid) + ':MR-[0-9]*:SIMPLE-[0-9]*\n', item):
            # print item
            sents = (" ".join(item.strip().split("\n")[1:])).lower()
            # print sents
            if sents not in simpsents:
                simpsents[sents] = 1
    print len(simpsents)

    directory = ""
    if complexid in datasplit["TEST"]:
        # Test example
        directory = "evaluation-directories/test/" + str(complexid)
    #     directory = "evaluation-directories/test-lowercased/"+str(complexid)
    else:
        return

    # elif complexid in datasplit["VALIDATION"]:
    #     # Validation
    #     directory = "evaluation-directories/validation/"+str(complexid)
    # else:
    #     # Train
    #     directory = "evaluation-directories/training/"+str(complexid)

    # Build directory
    os.system("mkdir -p " + directory)
    count = 0
    for sents in simpsents:
        fopen = open(directory + "/reference" + str(count), "w")
        fopen.write(sents + "\n")
        fopen.close()
        count += 1

if __name__ == "__main__":

    with open('benchmark/Split-train-dev-test.DONT-CHANGE.json') as data_file:
        datasplit = json.load(data_file)

    print len(datasplit["TEST"]), len(datasplit["VALIDATION"]), len(datasplit["TRAIN"])

    # Parse Simplification-Full Pairs
    with open("benchmark/final-complexsimple-meanpreserve-intreeorder-full.txt") as f:

        sentdata = []

        for line in f:
            if len(sentdata) == 0:
                sentdata.append(line)
            else:
                if re.match('COMPLEX-[0-9]*\n', line):
                    process_sentdata("".join(sentdata), datasplit)

                    print line
                    sentdata = [line]
                else:
                    sentdata.append(line)

        # Process last sentdata
        process_sentdata("".join(sentdata), datasplit)
