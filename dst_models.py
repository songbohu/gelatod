from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, AutoModelForCausalLM
import torch

device = "cuda" if torch.cuda.is_available() else "cpu"

class DSTModel():
    def __init__(self):
        pass

    def predict(self, history):
        raise NotImplementedError()

class GelatoDSTModel(DSTModel):
    def __init__(self):
        super().__init__()
        self.model_path = "./output/dst_model/checkpoint-best"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(self.model_path).to(device)

    def history_to_string(self, history):
        assert isinstance(history, list)
        processed_history = " ".join(list(map(lambda x: x["speaker"] + ": " + x["utterance"], history)))
        return processed_history

    def state_to_string(self, state):
        state_st = "flavours: " + ", ".join(state["flavours"]) + "# size: " + state["size"] + "# container: " + state[
            "container"]
        return state_st

    def string_to_state(self, state_string):

        pairs = state_string.split("# ")
        state = {}
        for pair in pairs:
            key, value = pair.split(": ", 1)
            if key == "flavours":
                value = value.split(", ")
            state[key] = value
        return state

    def predict(self, history):

        prefix = "dialogue state tracking"

        context_text = self.history_to_string(history)

        inputs = prefix + " : " + context_text

        model_inputs = self.tokenizer([inputs], return_tensors="pt").to(device)

        generated_ids = self.model.generate(**model_inputs,  max_new_tokens=512)

        output = self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True, clean_up_tokenization_spaces=True)[0]


        try:
            state = self.string_to_state(output)
        except:
            state = {"flavours": [], "size": "", "container": ""}
        return state

if __name__ == '__main__':
    dst_model = GelatoDSTModel()

    history = [{
            "speaker": "customer",
            "utterance": "Hello! I am looking for an icecream?"
        },
        {
            "speaker": "assistant",
            "utterance": "Yes, we have several options."
        },
        {
            "speaker": "customer",
            "utterance": "Can I have a double scoop with coconut and ube and Dark Chocolate & Sea Salt, in a normal cone.",
            "state": {
                "flavours": [
                    "Passion Fruit Sorbet",
                    "Dark Chocolate & Sea Salt"
                ],
                "size": "Double Scoop",
                "container": "Normal Cone"
            }
        }]


    print(dst_model.predict(history))
