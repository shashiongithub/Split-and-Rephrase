
if __name__ == "__main__":

    # Read Dict
    semid_sent_dict = {}
    semids = open(
        "benchmark/modtripleset-linealization/modtriple.mrid").readlines()
    semid_sents = open(
        "benchmark/modtripleset-linealization/modtriple.linearization.tokenized").readlines()
    for semid, sent in zip(semids, semid_sents):
        semid_sent_dict[semid.strip()] = sent.strip()
    print len(semid_sent_dict)

    filetolinearize = "validation.semantics"
    foutput = open(filetolinearize + ".linearized", "w")

    for item in open(filetolinearize).readlines():
        if item.strip() not in semid_sent_dict:
            print "Some problem"
            print item
            exit(0)
        else:
            foutput.write(semid_sent_dict[item.strip()] + "\n")

    foutput.close()
