import json
import os

from openai import OpenAI

client = OpenAI(
    api_key="YOU_OPENAI_KEY"
)

def read_json_string(text):
    start = text.find('```json') + len('```json\n')
    end = text.rfind('```')

    json_str = text[start:end].strip()

    try:
        json_data = json.loads(json_str)
        return json_data
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return None


def save_json_to_file(json_object, filename):
    if os.path.exists(filename) and os.path.getsize(filename) > 0:

        with open(filename, 'r') as file:
            try:
                existing_data = json.load(file)

                if not isinstance(existing_data, list):
                    print("Existing data in the file is not a list. Cannot append.")
                    return
            except json.JSONDecodeError as e:
                print(f"Error reading existing JSON data: {e}")
                return
    else:

        existing_data = []

    existing_data.append(json_object)

    with open(filename, 'w') as file:
        json.dump(existing_data, file, indent=4, ensure_ascii=False)


def get_prediction(instructions, user_inp):
    try_counter = 0

    while try_counter < 50:
        try:
            try_counter += 1
            response = client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": instructions},
                    {"role": "user", "content": user_inp},
                ],
            )
            prediction = response.choices[0].message.content

            return prediction

        except Exception as e:
            print("Fail " + str(try_counter) + " times.")
            print(e)
    raise Exception("Failed to get results from OpenAI.")


if __name__ == '__main__':

    file_path = 'prompt.txt'

    try:
        with open(file_path, 'r') as file:
            content = file.read()
    except FileNotFoundError:
        print(f"The file {file_path} was not found.")

    instruction = "You are a helpful assistant. You are helping researchers to build a dataset for training a task-oriented dialogue system for a local gelato shop."
    user_inp = content


    success = 0
    fail = 0
    for i in range(50):
        prediction = get_prediction(instruction, user_inp)
        result = read_json_string(prediction)
        if result:
            success += 1
            print("success")
            print(success)
            save_json_to_file(result, "./dialogue_data.json")
        else:
            fail += 1
            print("fail")
            print(fail)

    print(success)
