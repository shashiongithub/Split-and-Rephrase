# Split and Rephrase

This repository releases the split-and-rephrase benchmark and scripts to replicate experiments from [Our EMNLP 2017 paper](http://aclweb.org/anthology/D/D17/D17-1065.pdf). 

If you use any of these, please cite our paper:

**Split and Rephrase, Shashi Narayan, Claire Gardent, Shay B. Cohen and Anastasia Shimorina, In the 2017 Conference on Empirical Methods on Natural Language Processing (EMNLP), Copenhagen, Denmark [bib](http://aclweb.org/anthology/D/D17/D17-1065.bib)**

> We propose a new sentence simplification task where the aim is to split a complex sentence into a meaning preserving sequence of shorter sentences.  Like sentence simplification, Split-and-Rephrase has the potential of benefiting both natural language processing and societal applications. Because shorter sentences are generally better processed by NLP systems, it could be used as a preprocessing step which facilitates and improves the performance of parsers, semantic role labelers and machine translation systems. It should also be of use for people with reading disabilities because it allows the conversion of longer sentences into shorter ones. This paper makes two contributions towards this new task. First, we create and make available a benchmark consisting of 1,066,115 tuples mapping a single complex sentence to a sequence of sentences expressing the same meaning. Second, we propose five models (from vanilla seq-2-seq to semantically-motivated models) to understand the difficulty of the proposed task.

## The Split and Rephrase Benchmark

*

Format

*

## Split and Rephrase Models

### Baseline Models

```
python prepare-baseline-data.py
```

This parses "final-complexsimple-meanpreserve-intreeorder-full.txt"
and "Split-train-dev-test.DONT-CHANGE.json" files and prepares data
for three baseline models: baseline-seq2seq, baseline-seq2seq-multisrc
and baseline-symbolic.

* baseline-seq2seq (SEQ2SEQ)

* baseline-seq2seq-multisrc (MULTISEQ2SEQ) 

* baseline-symbolic (HYBRIDSIMPL)


### Prepare Train, Validation and Test Evaluation Directory

prepare-evaluation-directories.py

This parses 
final-complexsimple-meanpreserve-intreeorder-full.txt
and build evaluation directories for train, test and validation using 
Split-train-dev-test.DONT-CHANGE.json.

Follows: https://github.com/moses-smt/mosesdecoder/blob/master/scripts/generic/multi-bleu.perl
usage: multi-bleu.pl [-lc] reference < hypothesis\n";
Reads the references from reference or reference0, reference1, ...\n";

If more than one reference sentence, it generates multiple reference files in 
data/evaluation-directories/
.

Train:
Max reference: 76283
Min reference: 1
Avreage: 199.8

[(76283, '3938'), (76283, '280'), (62294, '3879'), (57012, '1515'), (52738, '1630'), (33887, '3789'), (33887, '2711'), (31448, '408'), (24993, '349'), (18719, '2911')]

Validation: 
Max reference: 33068
Min reference: 1
Avreage: 176.8

[(33068, '4748'), (12776, '5146'), (8406, '4396'), (7637, '1502'), (6417, '3582'), (4634, '2379'), (1313, '4355'), (905, '1556'), (701, '2215'), (585, '5137')]

Test: 
Max reference: 28068
Min reference: 1
Avreage: 146.8

[(28068, '1203'), (6483, '3765'), (5262, '2561'), (4141, '1043'), (2924, '1870'), (2476, '4417'), (1749, '2820'), (1556, '3088'), (1550, '3629'), (1339, '3624')]














