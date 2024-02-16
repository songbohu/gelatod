from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, AutoModelForCausalLM
import torch

device = "cuda" if torch.cuda.is_available() else "cpu"

class RGModel():
    def __init__(self):
        pass

    def predict(self, history):
        raise NotImplementedError()

class GelatoRGModel(RGModel):
    def __init__(self):
        super().__init__()
        self.model_path = "./output/rg_model/checkpoint-best"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(self.model_path).to(device)

    def history_to_string(self, history):
        assert isinstance(history, list)
        processed_history = " ".join(list(map(lambda x: x["speaker"] + ": " + x["utterance"], history)))
        return processed_history

    def predict(self, history):

        prefix = "response generation"

        context_text = self.history_to_string(history)

        inputs = prefix + " : " + context_text

        model_inputs = self.tokenizer([inputs], return_tensors="pt").to(device)

        generated_ids = self.model.generate(**model_inputs,  max_new_tokens=512)

        output = self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True, clean_up_tokenization_spaces=True)[0]

        return output

if __name__ == '__main__':
    rg_model = GelatoRGModel()

    history = [{
            "speaker": "customer",
            "utterance": "Hello! Could you please tell me if there is a vegan option available today?"
        },
        {
            "speaker": "assistant",
            "utterance": "Yes, we have several vegan options: Gianduja, Passion Fruit Sorbet, Dark Chocolate & Sea Salt, and Coconut, Raspberry Ripple."
        },
        {
            "speaker": "customer",
            "utterance": "I'd like a double scoop with Passion Fruit Sorbet and Dark Chocolate & Sea Salt, in a normal cone.",
            "state": {
                "flavours": [
                    "Passion Fruit Sorbet",
                    "Dark Chocolate & Sea Salt"
                ],
                "size": "Double Scoop",
                "container": "Normal Cone"
            }
        }]

    print(rg_model.predict(history))
