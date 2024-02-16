import json
from PIL import Image, ImageDraw
import difflib


def load_json_from_file(filename):
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print(f"The file {filename} was not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error decoding JSON from the file {filename}.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def save_json_to_file(json_object, file_path):
    with open(file_path, 'w') as file:
        json.dump(json_object, file, indent=4, ensure_ascii=False)

def history_to_string(history):
    assert isinstance(history, list)
    processed_history =  " ".join(list(map(lambda x : x["speaker"] + ": " + x["utterance"], history)))
    return processed_history


def state_to_string(state):
    state_st = "flavours: " + ", ".join(state["flavours"]) + "# size: " + state["size"] + "# container: " + state[
        "container"]

    return state_st


def string_to_state(state_string):
    pairs = state_string.split("# ")

    state = {}

    for pair in pairs:
        key, value = pair.split(": ", 1)

        if key == "flavours":
            value = value.split(", ")

        state[key] = value

    return state


if __name__ == '__main__':
    data = load_json_from_file('dialogue_data.json')

    dst_data_dic = {}
    dst_dataset = []
    for dial in data[:-2]:
        history = []
        for utt in dial:
            history.append(utt)
            if utt["speaker"] == "customer":
                state = utt["state"]
                data_entry = {}
                data_entry["source"] = history_to_string(history)
                data_entry["target"] =  state_to_string(state)
                dst_dataset.append(data_entry)

    dst_data_dic["train"] = dst_dataset
    dst_dataset = []
    for dial in data[-2:-1]:
        history = []
        for utt in dial:
            history.append(utt)
            if utt["speaker"] == "customer":
                state = utt["state"]
                data_entry = {}
                data_entry["source"] = history_to_string(history)
                data_entry["target"] = state_to_string(state)
                dst_dataset.append(data_entry)

    dst_data_dic["val"] = dst_dataset
    dst_dataset = []
    for dial in data[-1:]:
        history = []
        for utt in dial:
            history.append(utt)
            if utt["speaker"] == "customer":
                state = utt["state"]
                data_entry = {}
                data_entry["source"] = history_to_string(history)
                data_entry["target"] = state_to_string(state)
                dst_dataset.append(data_entry)

    dst_data_dic["test"] = dst_dataset

    save_json_to_file(dst_data_dic, "dst_data.json")

    rg_data_dic = {}

    rg_dataset = []
    for dial in data[:-2]:
        history = []
        for utt in dial:
            if utt["speaker"] == "assistant":
                data_entry = {}
                data_entry["source"] = history_to_string(history)
                data_entry["target"] = utt["utterance"]
                rg_dataset.append(data_entry)
            history.append(utt)

    rg_data_dic["train"] = rg_dataset

    rg_dataset = []
    for dial in data[-2:-1]:
        history = []
        for utt in dial:
            if utt["speaker"] == "assistant":
                data_entry = {}
                data_entry["source"] = history_to_string(history)
                data_entry["target"] = utt["utterance"]
                rg_dataset.append(data_entry)
            history.append(utt)

    rg_data_dic["val"] = rg_dataset

    rg_dataset = []
    for dial in data[-1:]:
        history = []
        for utt in dial:
            if utt["speaker"] == "assistant":
                data_entry = {}
                data_entry["source"] = history_to_string(history)
                data_entry["target"] = utt["utterance"]
                rg_dataset.append(data_entry)
            history.append(utt)

    rg_data_dic["test"] = rg_dataset

    save_json_to_file(rg_data_dic, "rg_data.json")
