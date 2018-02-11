# Split and Rephrase

This repository releases the split-and-rephrase benchmark and scripts to replicate experiments from [Our EMNLP 2017 paper](http://aclweb.org/anthology/D/D17/D17-1064.pdf). 

If you use any of these, please cite our paper:

**Split and Rephrase, Shashi Narayan, Claire Gardent, Shay B. Cohen and Anastasia Shimorina, In the 2017 Conference on Empirical Methods on Natural Language Processing (EMNLP), Copenhagen, Denmark [(bib)](http://aclweb.org/anthology/D/D17/D17-1064.bib)**

> We propose a new sentence simplification task where the aim is to split a complex sentence into a meaning preserving sequence of shorter sentences.  Like sentence simplification, Split-and-Rephrase has the potential of benefiting both natural language processing and societal applications. Because shorter sentences are generally better processed by NLP systems, it could be used as a preprocessing step which facilitates and improves the performance of parsers, semantic role labelers and machine translation systems. It should also be of use for people with reading disabilities because it allows the conversion of longer sentences into shorter ones. This paper makes two contributions towards this new task. First, we create and make available a benchmark consisting of 1,066,115 tuples mapping a single complex sentence to a sequence of sentences expressing the same meaning. Second, we propose five models (from vanilla seq-2-seq to semantically-motivated models) to understand the difficulty of the proposed task.

If you have any issue using this repository, please contact me at shashi.narayan@ed.ac.uk.

## The Split and Rephrase Benchmark ("benchmark")

**We are working on an improved version of this dataset, stay tuned!**

It consists of three files:

* final-complexsimple-meanpreserve-intreeorder-full.txt: Complex and Simple Sentences with their semantic identifiers.

* benchmark_verified_simplifcation: RDF triples related to each semantic identifier.

* Split-train-dev-test.DONT-CHANGE.json: Train, Development and Test Splits.

and two additional directories:

* "complex-sents" directory: Train, Development and Test complex sentences used as input during testing.

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

## Semantically motivated Split and Rephrase Models (SPLIT-MULTISEQ2SEQ and SPLIT-SEQ2SEQ)

### Learn to partition

```
python prepare-learn-to-partition.py
```

It generates a directory called "mymodel/partition-module." Please
have a look at our paper to use this data to learn a probabilistic
model to learn to partition.

### Learn to Generate

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
 
