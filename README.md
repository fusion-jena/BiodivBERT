# BiodivBERT
Biodiversity domain language model. It is fine-tuned on 2 downstream tasks for Named Entity Recognition (NER) and Relation Extraction (RE) using various state-of-the-art datasets.
![STA Tasks!](images/biodivbert.png)

**Quick Download**
  * [BiodivBERT on Huggingface hub](https://huggingface.co/NoYo25/BiodivBERT) [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.6554141.svg)](https://doi.org/10.5281/zenodo.6554141)
  * Pre-proccessed Datasets for Fine-tuning [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.6554208.svg)](https://doi.org/10.5281/zenodo.6554208)
  * Pre-training corpora

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

### How to Use BiodivBERT

1. Masked Language Model
````buildoutcfg
from transformers import AutoTokenizer, AutoModelForMaskedLM

tokenizer = AutoTokenizer.from_pretrained("NoYo25/BiodivBERT")

model = AutoModelForMaskedLM.from_pretrained("NoYo25/BiodivBERT")
````

2. Token Classification - Named Entity Recognition
````buildoutcfg
from transformers import AutoTokenizer, AutoModelForTokenClassification

tokenizer = AutoTokenizer.from_pretrained("NoYo25/BiodivBERT")

model = AutoModelForTokenClassification.from_pretrained("NoYo25/BiodivBERT")
````

3. Sequence Classification - Relation Extraction
````buildoutcfg
from transformers import AutoTokenizer, AutoModelForSequenceClassification

tokenizer = AutoTokenizer.from_pretrained("NoYo25/BiodivBERT")

model = AutoModelForSequenceClassification.from_pretrained("NoYo25/BiodivBERT")
````

## Citation
