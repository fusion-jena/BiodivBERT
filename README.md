# BiodivBERT
BERT for Biodiversity domain including 2 downstream tasks: Named Entity Recognition (NER) and Relation Extraction (RE)
* [BiodivBERT on Huggingface hub]()
* [BiodivBERT Pre-trained Weights]()

## Pre-training 
* Code is published under this repo \pre-training 
* Data:
  1. Download [Abstracts Corpus]()
  2. Download [Full Text Corpus]()

## Fine-tuning 
* We have fine-tuned BiodivBERT on two down stream tasks: Named Entity Recognition & Relation Extration using the state-of-the-art datasets from biodiversity domain.
* The preprocessed version of [NER + RE datasets]() are avaiable under Zenodo as well.

### Named Entity Recognition
* Datasets:
  * COPIOUS
  * QEMP 
  * BiodivNER
  * Species-800
  * LINNAEUS
* Code:
  * We have fine-tuned BiodivBERT for /NER on a single TPU provided by ColabPro for few hours per dataset.
### Relation Extraction 
* Datasets:
  *  GAD
  *  EU-ADR
  *  BioRelEx
  *  BiodivRE
*  Same as in NER, We have fine-tuned BiodivBERT for /RE on a single TPU provided by ColabPro for few hours per dataset.

## Citation
