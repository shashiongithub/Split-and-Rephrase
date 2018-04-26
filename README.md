# Split and Rephrase

This repository contains the split-and-rephrase benchmark and scripts from our [EMNLP 2017 paper](http://aclweb.org/anthology/D/D17/D17-1064.pdf). 

If you use our datasets, please cite the following paper:

**Split and Rephrase, Shashi Narayan, Claire Gardent, Shay B. Cohen and Anastasia Shimorina, In the 2017 Conference on Empirical Methods on Natural Language Processing (EMNLP), Copenhagen, Denmark [(bib)](http://aclweb.org/anthology/D/D17/D17-1064.bib)**

If you have any issue using this repository, please contact me at shashi.narayan@ed.ac.uk.

## The Split and Rephrase Benchmark

### Version 1.0 ("benchmark-v1.0")

We have extracted this dataset from the complete version of the [WebNLG data](http://webnlg.loria.fr/pages/challenge.html). It consists of following files:

* final-complexsimple-meanpreserve-intreeorder-full.txt: Complex and Simple Sentences with their semantic identifiers.

* webnlg-corpus-release: RDF triples related to each semantic identifier.

* Split-train-dev-test.benchmark-v1.0.json: Train, Development and Test Splits.

#### Improvements over Version 0.1

##### The WebNLG Categories

* **benchmark-v0.1:** It was extracted from an incomplete version of the [WebNLG](http://webnlg.loria.fr/pages/challenge.html) corpus with 8 DBPedia categories (Airport, Astronaut, Building, Food, Monument, SportsTeam, University, WrittenWork).

* **benchmark-v1.0:** It is extracted from the final version of the [WebNLG](http://webnlg.loria.fr/pages/challenge.html) corpus with 15 DBPedia categories (Airport, Building, Food, SportsTeam, Artist, CelestialBody, MeanOfTransportation, University, Astronaut,  City, Monument, WrittenWork, Athlete, ComicsCharacter, Politician).

##### Number of Meaning Preserving (Complex-Simple) Pairs

| Version | # distinct complex sentences | # complex-simple pairs with partitions | # complex-simple pairs without partitions |
| --- | --- | --- | --- |
| **benchmark-v0.1** | 5546 | 1098221 | 1945 |
| **benchmark-v1.0** | 18830 | 1445159 | 6951 |


##### Splitting Method

* **benchmark-v0.1:** In this version, we followed standard practice in the Simplification literature. We ensured that complex sentences in validation and test sets are not seen during training by splitting the 5,546 distinct complex sentences into three subsets: Training set (4,438, 80%),
Validation set (554, 10%) and Test set (554, 10%). This way of splitting does not guarantee that the RDF triples seen in the validation and test sets won't occur in the training set. As a result, it leads to a large n-gram overlaps between the training, validation and test sets. 

* **benchmark-v1.0:** In this version, we ensured that if an RDF triple t: (e1, r, e2) is seen in the validation or test set, it does not occur in the training set. However, e1 or r or e2 may have occurred in the training set with some other RDF triples. This automatically guarantees that the complex sentences in the validation and test sets are not seen in the training set. 

##### Final Numbers of Distinct Complex Sentences 

| Version | Training | Validation | Test |
| --- | --- | --- | --- |
| **benchmark-v0.1** | 4438 |  554 |  554 |
| **benchmark-v1.0** | 16946 |  954 | 930 |


##### Overlap Statistics w.r.t. RDF Triples, Entities and Properties

| Version | **benchmark-v0.1**  | **benchmark-v1.0** |
| --- | --- | --- |
| RDFs (Train vs Test) | 672 (1025 vs 676) | **0** (3162 vs 352)|
| RDFs (Train vs Valid)| 671 (1025 vs 675) | **0** (3162 vs 356) |
| RDFs (Test vs Valid) | 501 (676 vs 675) | 338 (352 vs 356)|
| Entities (Train vs Test) | 642 (908 vs 644) | 56 (2665 vs 357)|
| Entities (Train vs Valid)| 634 (908 vs 636) | 56 (2665 vs 360) |
| Entities (Test vs Valid) | 505 (644 vs 636) | 345 (357 vs 360)|
| Properties (Train vs Test) | 139 (168 vs 140) | 122 (346 vs 138)|
| Properties (Train vs Valid)| 132 (168 vs 133) | 119 (346 vs 137) |
| Properties (Test vs Valid) | 120 (140 vs 133) | 134 (138 vs 137)|


##### Overlap Statistics w.r.t. Simple Sentences

| Version | **benchmark-v0.1**  | **benchmark-v1.0** |
| --- | --- | --- |
| Total Simple Sentences | 9552 | 31159 |
| Train | 8840 | 28150 | 
| Validation | 3765 | 2464 | 
| Test | 4015 | 2466 | 
| Train vs Test |  3606 | 3 |
| Train vs Val |  3425  | 2 |
| Test vs Val |  2210 | 1918 | 
| Train vs Test vs Val |  2173 | 2 |




<!---
1. we may have the same complex sentence occurring with many simplification
2. perhaps these complex sentences describe a few entities which leads the model to learn to describe the entity rather than simplifying the sentence

so another possibility would be 
1. to restrict the nb of pairs (in the tg corpus) containing the same complex sentence
2. to restrict the nb of complex sentences describing the same entity
--->


### Version 0.1 ("benchmark-v0.1", deprecated)

This is the version of the dataset reported in our EMNLP paper. It was extracted from an incomplete version (then available) of the [WebNLG data](http://webnlg.loria.fr/pages/challenge.html).

In this version, we had followed a standard practice in Simplification
literature and split our dataset into the training, validation and test
subsets such that complex sentences in validation and test sets were
not seen during training. 

Recently (Feb 18), Jan Botha and Jason Baldridge (Google), informed us that this way of splitting led to a large n-gram overlap between training, development and test sets. We found that this overlap appeared due to the shared RDF triples in our dataset. As a result, we have decided to deprecate the split used in the paper. Instead, we encourage others to use an improved version (benchmark-v1.0) of this dataset. 

In case you would like to work with this version, we suggest you to use the split of [Aharoni and Goldberg](https://github.com/roeeaharoni/sprp-acl2018).


benchmark-v0.1 consists of following files:

* final-complexsimple-meanpreserve-intreeorder-full.txt: Complex and Simple Sentences with their semantic identifiers.

* benchmark_verified_simplifcation: RDF triples related to each semantic identifier.

* Split-train-dev-test.DONT-CHANGE.json: Train, Development and Test Splits. (**Removed**)

and two additional directories:

* "complex-sents" directory: Train, Development and Test complex sentences used as input during testing. (**Removed**)

* "modtripleset-linealization" directory: Semantic identifier associated with their linearized RDF representation. 

## Split and Rephrase Models

Our models use codes from [Multiple Source NMT Toolkit,
Zoph_RNN](https://github.com/isi-nlp/Zoph_RNN) and our [Hybrid
Sentence Simplification
System](https://github.com/shashiongithub/Sentence-Simplification-ACL14). To
replicate all the models discussed in the paper, please make sure that
you have these codes available.

### Baseline Models

```
python prepare-baseline-data.py
```

This parses "final-complexsimple-meanpreserve-intreeorder-full.txt"
and "Split-train-dev-test.DONT-CHANGE.json" files and prepares data
for three baseline models: baseline-seq2seq, baseline-seq2seq-multisrc
and baseline-symbolic.

* baseline-seq2seq (SEQ2SEQ, C ==> S1, S2, S3): Training and decoding with ZOPH_RNN.

```
./ZOPH_RNN -t baseline-seq2seq/train.complex baseline-seq2seq/train.simple model.nn -N 3 -H 500 -m 64 -d 0.8 -l 0.5 --attention-model true --feed-input true -a baseline-seq2seq/validation.complex baseline-seq2seq/validation.simple -A 0.5 --tmp-dir-location baseline-seq2seq/fullvocab/ --logfile baseline-seq2seq/fullvocab/logfile.txt -B best.nn -M 1 1 1 1

./ZOPH_RNN -k 1 baseline-seq2seq/fullvocab/best.nn  baseline-seq2seq/fullvocab/test.1best.txt --decode-main-data-files benchmark/complex-sents/test.complex
```

* baseline-seq2seq-multisrc (MULTISEQ2SEQ, C T_C ==> S1, S2, S3) 

```
./ZOPH_RNN -n 30 -t baseline-seq2seq-multisrc/train.complex baseline-seq2seq-multisrc/train.simple baseline-seq2seq-multisrc/fullvocab/model.nn -N 3 -H 500 -m 64 -d 0.8 -l 0.5 --multi-source baseline-seq2seq-multisrc/train.complex-semantics.linearized baseline-seq2seq-multisrc/fullvocab/src.nn --attention-model 1 --feed-input 1 --multi-attention 1 -a baseline-seq2seq-multisrc/validation.complex baseline-seq2seq-multisrc/validation.simple baseline-seq2seq-multisrc/validation.complex-semantics.linearized -A 0.5 --tmp-dir-location baseline-seq2seq-multisrc/fullvocab/ --logfile baseline-seq2seq-multisrc/fullvocab/logfile.txt -B baseline-seq2seq-multisrc/fullvocab/best.nn -M 1 1 1 1

./ZOPH_RNN -k 1 baseline-seq2seq-multisrc/fullvocab/best.nn baseline-seq2seq-multisrc/fullvocab/test.1best.txt --decode-main-data-files benchmark/complex-sents/test.complex --decode-multi-source-data-files complex-sents/test.semantics.linearized --decode-multi-source-vocab-mappings baseline-seq2seq-multisrc/fullvocab/src.nn
```

Please use "extract-modtriple-linearized-tokenized-forafile.py" to generate ".linearized" file.

* baseline-symbolic (HYBRIDSIMPL, C ==> S1, S2, S3 using Boxer and SMT)

Please follow instructions from our [Hybrid Sentence Simplification
System](https://github.com/shashiongithub/Sentence-Simplification-ACL14). Please
contact me at shashi.narayan@ed.ac.uk if you have any issue.

### Semantically motivated Split and Rephrase Models (SPLIT-MULTISEQ2SEQ and SPLIT-SEQ2SEQ)

#### Learn to partition

```
python prepare-learn-to-partition.py
```

It generates a directory called "mymodel/partition-module." Please
have a look at our paper to use this data to learn a probabilistic
model to learn to partition.

#### Learn to Generate

```
python prepare-learn-to-generation.py
```

It generates a directory called "mymodel/generation-module." Please
use ZOPH_RNN codes (as in baseline models) to implement MULTISEQ2SEQ
or SEQ2SEQ followed by the SPLIT step. 


### Evaluation Scripts: Prepare Reference Directory and Evaluation

```
python prepare-evaluation-directories.py
```

This parses final-complexsimple-meanpreserve-intreeorder-full.txt and
build evaluation directories for train, test and validation using
Split-train-dev-test.DONT-CHANGE.json.

Follows: https://github.com/moses-smt/mosesdecoder/blob/master/scripts/generic/multi-bleu.perl
usage: multi-bleu.pl [-lc] reference < hypothesis\n";
Reads the references from reference or reference0, reference1, ...\n";

If more than one reference sentence, it generates multiple reference
files in "evaluation-directories."

Finally use multi-bleu.perl to estimate BLEU scores.
 
