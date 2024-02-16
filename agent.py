import torch

import gelatoAPI
from dst_models import GelatoDSTModel
from rg_models import GelatoRGModel

device = "cuda" if torch.cuda.is_available() else "cpu"

class Agent():
    def __init__(self):
        self.reset()

    def reset(self):
        pass

    def chat(self, utterance):
        raise NotImplementedError()

class GelatoAgent(Agent):
    def __init__(self):
        super().__init__()
        self.reset()
        # These models are stateless.
        self.dst_model = GelatoDSTModel()
        self.rg_model = GelatoRGModel()
        self.conversation_history = []

    def reset(self):
        self.conversation_history = []

    def chat(self, utterance):

        self.conversation_history.append({"speaker" : "customer", "utterance": utterance})
        state = self.dst_model.predict(self.conversation_history)
        response = self.rg_model.predict(self.conversation_history)
        self.conversation_history.append({"speaker" : "assistant", "utterance": response})
        return response, state

    def start_a_chat(self):
        print("The system is ready. Please say `bye` or `exit` to end the conversation.")
        while (True):
            string = str(input())
            if string.lower() in ["exit", "bye"]:
                break
            reply, state = self.chat(string)
            print(reply)
            if state["flavours"] and "size" in state and "container" in state:
                print(state)
                gelatoAPI.get_gelato(state)

            print()



if __name__ == '__main__':
    agent = GelatoAgent()
    agent.start_a_chat()