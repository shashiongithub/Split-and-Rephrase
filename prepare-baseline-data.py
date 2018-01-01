import random
import json
import re
import os


def process_sentdata_baseline(data, datasplit,
                              f_src_s2s_train, f_src_s2s_val, f_src_s2s_test,
                              f_trg_s2s_train, f_trg_s2s_val, f_trg_s2s_test,
                              f_sym_train, f_sym_train_complex, f_sym_train_simple,
                              f_sym_val, f_sym_val_complex, f_sym_val_simple,
                              f_sym_test, f_sym_test_complex, f_sym_test_simple,
                              f_src_s2smsrc_train, f_src_s2smsrc_val, f_src_s2smsrc_test,
                              f_srcsem_s2smsrc_train, f_srcsem_s2smsrc_val, f_srcsem_s2smsrc_test,
                              f_trg_s2smsrc_train, f_trg_s2smsrc_val, f_trg_s2smsrc_test):

    data = data.strip().split("\n\n")

    complexsentdata = data[0].strip().split("\n")
    complexid = int(complexsentdata[0].split("-")[1].strip())
    complexsent = complexsentdata[1].strip()

    mr_dict = {}
    # Collect all complex mrs
    for item in data[1:]:
        if re.match('COMPLEX-' + str(complexid) + ':MR-[0-9]*\n', item):
            # print item
            mrdata = item.strip().split("\n")
            mrid = mrdata[0]
            mr = mrdata[1]
            mr_dict[mrid] = [mr, {}]
    # print mr_dict

    simpsents = {}
    for item in data[1:]:
        if re.match('COMPLEX-' + str(complexid) + ':MR-[0-9]*:SIMPLE-[0-9]*\n', item):
            # print item

            mrid = ":".join(item.strip().split("\n")[0].split(":")[:2])
            # print mrid

            sents = ("\n".join(item.strip().split("\n")[1:])).strip()
            # print sents

            if sents not in simpsents:
                simpsents[sents] = 1

            if sents not in mr_dict[mrid][1]:
                mr_dict[mrid][1][sents] = 1

    print complexid, len(simpsents), len(mr_dict)

    # simpsents = {}
    # for item in data[1:]:
    #     if re.match('COMPLEX-'+str(complexid)+':MR-[0-9]*:SIMPLE-[0-9]*\n', item):
    #         # print item
    #         sents = ("\n".join(item.strip().split("\n")[1:])).strip()
    #         # print sents
    #         if sents not in simpsents:
    #             simpsents[sents] = 1
    # print complexid, len(simpsents)

    if complexid in datasplit["TEST"]:
        # Test example
        for sents in simpsents:
            f_src_s2s_test.write(complexsent + "\n")
            f_trg_s2s_test.write(sents.replace("\n", " ") + "\n")

            f_sym_test.write(complexsent + "\n" + sents + "\n\n")
            f_sym_test_complex.write(complexsent + "\n")
            f_sym_test_simple.write(sents + "\n")
        for mrid in mr_dict:
            mrcinfo = mr_dict[mrid][0]
            for sents in mr_dict[mrid][1]:
                f_src_s2smsrc_test.write(complexsent + "\n")
                f_srcsem_s2smsrc_test.write(mrcinfo + "\n")
                f_trg_s2smsrc_test.write(sents.replace("\n", " ") + "\n")

    elif complexid in datasplit["VALIDATION"]:
        # Validation
        for sents in simpsents:
            f_src_s2s_val.write(complexsent + "\n")
            f_trg_s2s_val.write(sents.replace("\n", " ") + "\n")

            f_sym_val.write(complexsent + "\n" + sents + "\n\n")
            f_sym_val_complex.write(complexsent + "\n")
            f_sym_val_simple.write(sents + "\n")
        for mrid in mr_dict:
            mrcinfo = mr_dict[mrid][0]
            for sents in mr_dict[mrid][1]:
                f_src_s2smsrc_val.write(complexsent + "\n")
                f_srcsem_s2smsrc_val.write(mrcinfo + "\n")
                f_trg_s2smsrc_val.write(sents.replace("\n", " ") + "\n")
    else:
        # Train
        for sents in simpsents:
            f_src_s2s_train.write(complexsent + "\n")
            f_trg_s2s_train.write(sents.replace("\n", " ") + "\n")

            f_sym_train.write(complexsent + "\n" + sents + "\n\n")
            f_sym_train_complex.write(complexsent + "\n")
            f_sym_train_simple.write(sents + "\n")
        for mrid in mr_dict:
            mrcinfo = mr_dict[mrid][0]
            for sents in mr_dict[mrid][1]:
                f_src_s2smsrc_train.write(complexsent + "\n")
                f_srcsem_s2smsrc_train.write(mrcinfo + "\n")
                f_trg_s2smsrc_train.write(sents.replace("\n", " ") + "\n")

if __name__ == "__main__":

    # Baseline directories
    os.system("mkdir -p baseline-seq2seq")
    os.system("mkdir -p baseline-seq2seq-multisrc")
    os.system("mkdir -p baseline-symbolic")

    with open('benchmark/Split-train-dev-test.DONT-CHANGE.json') as data_file:
        datasplit = json.load(data_file)

    print len(datasplit["TEST"]), len(datasplit["VALIDATION"]), len(datasplit["TRAIN"])

    # Parse Simplification-Full Pairs and prepare baseline system
    f_src_s2s_train = open("baseline-seq2seq/train.complex", "w")
    f_src_s2s_val = open("baseline-seq2seq/validation.complex", "w")
    f_src_s2s_test = open("baseline-seq2seq/test.complex", "w")
    f_trg_s2s_train = open("baseline-seq2seq/train.simple", "w")
    f_trg_s2s_val = open("baseline-seq2seq/validation.simple", "w")
    f_trg_s2s_test = open("baseline-seq2seq/test.simple", "w")

    f_src_s2smsrc_train = open("baseline-seq2seq-multisrc/train.complex", "w")
    f_src_s2smsrc_val = open(
        "baseline-seq2seq-multisrc/validation.complex", "w")
    f_src_s2smsrc_test = open("baseline-seq2seq-multisrc/test.complex", "w")
    f_srcsem_s2smsrc_train = open(
        "baseline-seq2seq-multisrc/train.complex-semantics", "w")
    f_srcsem_s2smsrc_val = open(
        "baseline-seq2seq-multisrc/validation.complex-semantics", "w")
    f_srcsem_s2smsrc_test = open(
        "baseline-seq2seq-multisrc/test.complex-semantics", "w")
    f_trg_s2smsrc_train = open("baseline-seq2seq-multisrc/train.simple", "w")
    f_trg_s2smsrc_val = open(
        "baseline-seq2seq-multisrc/validation.simple", "w")
    f_trg_s2smsrc_test = open("baseline-seq2seq-multisrc/test.simple", "w")

    f_sym_train = open("baseline-symbolic/train.both", "w")
    f_sym_train_complex = open("baseline-symbolic/train.complex", "w")
    f_sym_train_simple = open("baseline-symbolic/train.simple", "w")
    f_sym_val = open("baseline-symbolic/validation.both", "w")
    f_sym_val_complex = open("baseline-symbolic/validation.complex", "w")
    f_sym_val_simple = open("baseline-symbolic/validation.simple", "w")
    f_sym_test = open("baseline-symbolic/test.both", "w")
    f_sym_test_complex = open("baseline-symbolic/test.complex", "w")
    f_sym_test_simple = open("baseline-symbolic/test.simple", "w")

    with open("benchmark/final-complexsimple-meanpreserve-intreeorder-full.txt") as f:

        sentdata = []

        for line in f:
            if len(sentdata) == 0:
                print line
                sentdata.append(line)
            else:
                if re.match('COMPLEX-[0-9]*\n', line):
                    process_sentdata_baseline("".join(sentdata), datasplit,
                                              f_src_s2s_train, f_src_s2s_val, f_src_s2s_test,
                                              f_trg_s2s_train, f_trg_s2s_val, f_trg_s2s_test,
                                              f_sym_train, f_sym_train_complex, f_sym_train_simple,
                                              f_sym_val, f_sym_val_complex, f_sym_val_simple,
                                              f_sym_test, f_sym_test_complex, f_sym_test_simple,
                                              f_src_s2smsrc_train, f_src_s2smsrc_val, f_src_s2smsrc_test,
                                              f_srcsem_s2smsrc_train, f_srcsem_s2smsrc_val, f_srcsem_s2smsrc_test,
                                              f_trg_s2smsrc_train, f_trg_s2smsrc_val, f_trg_s2smsrc_test)

                    print line
                    sentdata = [line]
                else:
                    sentdata.append(line)

        # Process last sentdata
        process_sentdata_baseline("".join(sentdata), datasplit,
                                  f_src_s2s_train, f_src_s2s_val, f_src_s2s_test,
                                  f_trg_s2s_train, f_trg_s2s_val, f_trg_s2s_test,
                                  f_sym_train, f_sym_train_complex, f_sym_train_simple,
                                  f_sym_val, f_sym_val_complex, f_sym_val_simple,
                                  f_sym_test, f_sym_test_complex, f_sym_test_simple,
                                  f_src_s2smsrc_train, f_src_s2smsrc_val, f_src_s2smsrc_test,
                                  f_srcsem_s2smsrc_train, f_srcsem_s2smsrc_val, f_srcsem_s2smsrc_test,
                                  f_trg_s2smsrc_train, f_trg_s2smsrc_val, f_trg_s2smsrc_test)

    f_src_s2s_train.close()
    f_src_s2s_val.close()
    f_src_s2s_test.close()
    f_trg_s2s_train.close()
    f_trg_s2s_val.close()
    f_trg_s2s_test.close()

    f_src_s2smsrc_train.close()
    f_src_s2smsrc_val.close()
    f_src_s2smsrc_test.close()
    f_srcsem_s2smsrc_train.close()
    f_srcsem_s2smsrc_val.close()
    f_srcsem_s2smsrc_test.close()
    f_trg_s2smsrc_train.close()
    f_trg_s2smsrc_val.close()
    f_trg_s2smsrc_test.close()

    f_sym_train.close()
    f_sym_train_complex.close()
    f_sym_train_simple.close()
    f_sym_val.close()
    f_sym_val_complex.close()
    f_sym_val_simple.close()
    f_sym_test.close()
    f_sym_test_complex.close()
    f_sym_test_simple.close()
