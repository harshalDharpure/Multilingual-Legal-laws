from transformers import  AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig, TrainingArguments, DataCollatorForLanguageModeling
from sklearn.model_selection import train_test_split
from datasets import DatasetDict, Dataset
import pandas as pd
import numpy as np
import warnings
import logging
import random
import torch
import json
import yaml
import os
import json
import torch
from transformers import pipeline
from sklearn.metrics import accuracy_score
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

warnings.filterwarnings("ignore")

with open('/DATA/harsh_2311ai14/QA_architecture1/config.yaml', 'r') as file:
    config = yaml.safe_load(file)
def seed_everything(seed: int):
    random.seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = True

seed_everything(42)


contexts_file1="/DATA/harsh_2311ai14/QA_architecture1/result_qwen7b_main_architecture05032025.jsonl"
context_dict1 = {}
with open(contexts_file1, 'r', encoding='utf-8') as cf:
    for line in cf:
        entry = json.loads(line)
        question = entry.get('Question')
        retrieved_context = entry.get('main_model_reasoning')
        if question and retrieved_context:
            context_dict1[question] = retrieved_context

contexts_file2="/DATA/harsh_2311ai14/QA_architecture1/Critique.jsonl"
context_dict2 = {}
with open(contexts_file2, 'r', encoding='utf-8') as cf:
    for line in cf:
        entry = json.loads(line)
        question = entry.get('Question')
        retrieved_context = entry.get('Critique')
        if question and retrieved_context:
            context_dict2[question] = retrieved_context

contexts_file="/DATA/harsh_2311ai14/QA_architecture1/Defense.jsonl"
context_dict = {}
with open(contexts_file, 'r', encoding='utf-8') as cf:
    for line in cf:
        entry = json.loads(line)
        question = entry.get('Question')
        retrieved_context = entry.get('Defense')
        if question and retrieved_context:
            context_dict[question] = retrieved_context

data_file = config['actual_data']
data_list = []
with open(data_file, 'r', encoding='utf-8') as df:
    for line in df:
        data_list.append(json.loads(line))

def get_data_point_with_context_list(data_entry):
    record = data_entry
    question = record.get('Question')
    reasoning = context_dict1.get(question, None)
    critique = context_dict2.get(question, None)
    defense = context_dict.get(question, None)

    record_with_context = record.copy()
    record_with_context['main_model_reasoning'] = reasoning
    record_with_context['Critique'] = critique
    record_with_context['Defense'] = defense
    return record_with_context

judge_system_prompt = '''
You are a neutral legal expert who evaluates debates between a Challenger and a Defender.
Judge who made the stronger case. Clearly state the winner ('Challenger' or 'Defender') and explain your reasoning.
Provide the correct answer and sound reasoning for the case.
Your job is to:
1️⃣ **Assess both arguments** based on legal correctness, logical strength, and clarity.
2️⃣ **Declare the winner** by deciding who presented the stronger case: 'Challenger' or 'Defender'.
3️⃣ **Provide the correct legal answer** to the question (even if both parties made mistakes).
4️⃣ **Explain your final reasoning** concisely and precisely.Your job is to:
Your response must be in strict JSON format as shown below:
```json

{
    "Question": "<Insert the question here>",
    "A": "<Insert Option A text>",
    "B": "<Insert Option B text>",
    "C": "<Insert Option C text>",
    "D": "<Insert Option D text>",
    "Winner": "<Challenger or Defender>",
    "Correct Answer": "<Write the full correct answer, not just the option letter>",
    "Judgement": "<Provide detailed reasoning explaining why the winner’s argument was stronger and why the correct answer is correct>",
    "final_reasoning" : <Provide overall final reasoning behind the answer. Write full reasoning behind the answer Don't mention which option it is directly You can mention content of option>
}

 Output should be in strictly in json format
'''


def generate_judge_content(data_entry):
    question = data_entry.get('Question', '')
    A = data_entry.get('A', '')
    B = data_entry.get('B', '')
    C = data_entry.get('C', '')
    D = data_entry.get('D', '')
    answer = data_entry.get('Correct Answer', '')
    reasoning = data_entry.get('main_model_reasoning', '')
    critique = data_entry.get('Critique', '')
    defense= data_entry.get('Defense', '')

    judge_content = f'''
            Question:
            {question}

            Options:
            A: {A}
            B: {B}
            C: {C}
            D: {D}


            Initial Answer:
            {answer}

            Initial Reasoning:
            {reasoning}

            Challenger’s Critique:
            {critique}

            Defender's defense:
            {defense}

Do not mention which option you are choosing. Provide only the content of the option. 
                '''

    return judge_content

def extract_nested_braces(s):
    # s = s.replace('"','')
    s += "}"
    stack = []
    start = -1
    result = []
    # print(s)
    for i, char in enumerate(s):
        if char == '{':
            if not stack:
                start = i
            stack.append(char)
        elif char == '}':
            if stack:
                stack.pop()
                if not stack:
                    result.append(s[start:i+1])
    return result[0] if result else None

def string_to_dict(json_string):
    try:
        # Parse the JSON string into a dictionary
        return json.loads(json_string)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON string: {e}")


from huggingface_hub import login
login('')


model_id = "meta-llama/Llama-3.2-3B-Instruct"
pipe = pipeline(
    "text-generation",
    model=model_id,
    torch_dtype=torch.bfloat16,
    device_map="auto",
)


def judge_model( data_entry):
    judge_content = generate_judge_content(data_entry)
    messages = [
            {"role": "system", "content": judge_system_prompt},
            {"role": "user", "content": judge_content}
        ]
    outputs = pipe(
        messages,
        max_new_tokens=1500,
    )
    json_output=outputs[0]["generated_text"][-1]['content']
    # print(json_output)
    result = string_to_dict(extract_nested_braces(json_output))
    # print(result)
    return result


result_log_path = 'judge2.jsonl'  # ✅ Path to save the results

# 🔄 Load existing results if available
if os.path.isfile(result_log_path):
    with open(result_log_path, 'r', encoding='utf-8') as file:
        output_log = [json.loads(line) for line in file]
else:
    output_log = []

# 🛑 Create a set of already processed questions to avoid duplicates
processed_questions = set(entry["Question"] for entry in output_log)

# Start processing
i = 0
for datapoint in data_list:
    question = datapoint.get('Question')
    if question in processed_questions:
        i += 1
        continue  # Skip already processed

    try:
        # 🗂️ Get data + context
        compact_data = get_data_point_with_context_list(datapoint)

        # 🤖 Run the judge model
        judge_result = judge_model(compact_data)
        temp_data=judge_result.copy()
        temp_data.pop("Question")
        temp_data["Question"]=datapoint["Question"]

        # ✅ Add to log
        output_log.append(judge_result)

        # 💾 Save incrementally to JSONL file
        with open(result_log_path, 'a', encoding='utf-8') as file:
            file.write(json.dumps(judge_result, ensure_ascii=False) + '\n')

        print(f"✅ Data point {i} processed and saved.")
        i += 1

    except Exception as e:
        print(f"⚠️ Error processing question: {question}")
        print(f"Exception: {e}")

print("🎉 Processing complete. All results saved to:", result_log_path)


