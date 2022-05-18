# references:
# How to train
# 1. https://huggingface.co/blog/how-to-train
# 2. https://www.thepythoncode.com/article/pretraining-bert-huggingface-transformers-in-python

# POC on colab (Meine)
# 3. https://colab.research.google.com/drive/14XbE_81JlfSiIBkxebevPHqUBETzate4#scrollTo=K4N8ZRsRg-ic

# Choosing right parameter
# 4. https://quick-adviser.com/how-many-epochs-are-enough/#How_many_epochs_do_you_need_to_train_a_Bert
# 5. https://medium.com/analytics-vidhya/choosing-the-right-parameters-for-pre-training-bert-using-tpu-4584a598ca50


from transformers import BertForMaskedLM, DistilBertForMaskedLM
from transformers import DataCollatorForLanguageModeling
from transformers import Trainer, TrainingArguments
from get_tokenizer import *
import config
from os.path import join
from dataset import *
from util_log import log


def run():
    log.info("Creating transformers test dataset object ...")

    log.info("Initializing {} model ...".format(config.MODEL_NAME))
    if 'distil' in config.MODEL_NAME:
        model = DistilBertForMaskedLM.from_pretrained(config.MODEL_NAME, local_files_only=True)
    else:
        model = BertForMaskedLM.from_pretrained(config.MODEL_NAME, local_files_only=True)

    log.info("Initializing DataCollatorForLanguageModeling mlm_prob={} ...".format(config.MLM_PROP))
    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer, mlm=True, mlm_probability=config.MLM_PROP
    )

    lm_datasets = get_torch_datasets()

    log.info("Initializing TrainingArguments  ...")
    log.info("Batch_Size = {}".format(config.per_device_train_batch_size))
    log.info("epochs = {}".format(config.num_train_epochs))

    training_args = TrainingArguments(
        output_dir=config.LOCAL_DIR,
        overwrite_output_dir=True,
        evaluation_strategy="steps",
        # evaluation_strategy = "epoch",
        log_level="error",
        report_to="none",

        num_train_epochs=config.num_train_epochs,
        per_device_train_batch_size=config.per_device_train_batch_size,
        gradient_accumulation_steps=config.gradient_accumulation_steps,
        gradient_checkpointing=True,
        fp16=True,

        do_train=True,
        do_eval=True,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        data_collator=data_collator,
        train_dataset=lm_datasets["train"],
        eval_dataset=lm_datasets["validation"],  # evaluation dataset

    )
    log.info("Training Args:")
    log.info(training_args)

    log.info("Training ...")
    # train from scratch
    if config.train_from_sratch:
        trainer.train()
    else:
        trainer.train(join(config.LOCAL_DIR, config.CHECKPOINT_NAME))  # resume training from a checkpoint

    log.info("Saving model offline at ".format(config.LOCAL_DIR))
    trainer.save_model(config.LOCAL_DIR)


if __name__ == '__main__':
    # Testing for this file only, for the entire senario, check main.py
    run()
