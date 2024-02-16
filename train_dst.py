import pandas as pd
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, \
    DataCollatorForSeq2Seq, Seq2SeqTrainer, Seq2SeqTrainingArguments, EarlyStoppingCallback

import json
from transformers import set_seed
from datasets import Dataset, DatasetDict

def load_json_from_file(filename):
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
            return data
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def save_json_to_file(json_object, file_path):
    with open(file_path, 'w') as file:
        json.dump(json_object, file, indent=4, ensure_ascii=False)

def run_experiment():

    model_name = "google-t5/t5-base"
    set_seed(10086)

    tokenizer = AutoTokenizer.from_pretrained(
        model_name,
        max_length = 512
    )

    processed_data = load_json_from_file("dst_data.json")

    for data_key, data in processed_data.items():
        data = pd.DataFrame.from_dict(data)
        data = Dataset.from_pandas(data)
        processed_data[data_key] = data
    data_dic = DatasetDict(processed_data)

    print(data_dic)

    prefix = "dialogue state tracking"

    model = AutoModelForSeq2SeqLM.from_pretrained(model_name,
          max_length=512
    )

    def preprocess_function(examples):

        inputs = [prefix + " : " + example for example in examples["source"]]
        targets = [example for example in examples["target"]]
        model_inputs = tokenizer(inputs, text_target=targets, max_length=int(512))
        return model_inputs

    tokenized_dataset = data_dic.map(preprocess_function, batched=True)

    data_collator = DataCollatorForSeq2Seq(tokenizer=tokenizer, model=model)

    training_args = Seq2SeqTrainingArguments(
        output_dir="./output/dst_model",
        learning_rate=1e-3,
        per_device_train_batch_size=16,
        per_device_eval_batch_size=16,
        weight_decay=0.01,
        save_total_limit=int(1),
        predict_with_generate=True,
        max_steps=int(5000),
        save_steps=int(5000),
        save_strategy="steps",
        push_to_hub=True,
        fp16=False,
        generation_max_length=512
    )

    trainer = Seq2SeqTrainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_dataset["train"],
        eval_dataset=tokenized_dataset["val"],
        tokenizer=tokenizer,
        data_collator=data_collator,
        callbacks=[]
    )

    trainer.train()

    trainer.save_model("./output/dst_model/checkpoint-best")


def main():
    run_experiment()

if __name__ == '__main__':
    main()