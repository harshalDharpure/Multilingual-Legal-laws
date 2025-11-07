# Critique Notebook Analysis & File Explanations

## 📋 File Explanations

### 1. **`data.json` / `data.jsonl`**
- **What it is**: This refers to your test dataset (`test_data.json` in JSON format, or `data.jsonl` if converted to JSONL)
- **Purpose**: Contains the canonical test questions with Passage, Question, A/B/C/D options, Correct Answer, and Reasoning
- **Location**: Should be `QA_CHild_legal/test_data.json` (as specified in `config.yaml`)
- **Usage**: 
  - Loaded in `critique.ipynb` via `config['actual_data']`
  - Used to get questions for critique generation

### 2. **`judge1.jsonl` / `judge2.jsonl`**
- **What it is**: Output file from the **Judge stage** (`judgements.py`)
- **Purpose**: Contains the judge's decision after evaluating Critique vs Defense
- **Structure**: Contains:
  - `Question`: The question text
  - `Winner`: "Challenger" or "Defender"
  - `Correct Answer`: Full text of correct option
  - `Judgement`: Reasoning for the decision
  - `final_reasoning`: Overall final reasoning
- **When created**: After running Step 6 (Judge stage) - **NOT needed for Critique stage**
- **Note**: The first cell in `critique.ipynb` filters `judge1.jsonl`, but this is **optional** and should be removed or moved to a separate cleanup script

---

## ⚠️ Issues Found in `critique.ipynb`

### Issue 1: Cell 0 - Unnecessary Judge Filtering
**Problem**: 
- References `data.jsonl` (should use `config['actual_data']` which is `test_data.json`)
- Filters `judge1.jsonl` which is an **output** file, not needed for critique stage
- This cell should be **removed** or moved to a post-processing script

**Fix**: Remove this cell or comment it out. The critique stage doesn't need judge outputs.

### Issue 2: Cell 4 - Hardcoded Excel File
**Problem**:
```python
contexts_file="rag.xlsx"  # ❌ Hardcoded, may not exist
context_df = pd.read_excel(contexts_file)
```

**Should be**:
```python
contexts_file = config['rag_retrieved_context']  # ✅ Use config
# Load from JSONL, not Excel
with open(contexts_file, 'r', encoding='utf-8') as cf:
    for line in cf:
        entry = json.loads(line)
        question = entry.get('Question')
        retrieved_context = entry.get('retrieved_context')
        if question and retrieved_context:
            context_dict[question] = retrieved_context
```

### Issue 3: Cell 5 - Hardcoded ARR Result File
**Problem**:
```python
contexts_file1="result_qwen7b_main_architecture05032025.jsonl"  # ❌ Hardcoded path
```

**Should be**:
```python
# Use config to get the ARR result file path
model_name = config['save_file_main_model']
result_log_path = f"result_log/{model_name}/result_{model_name}_main_architecture.jsonl"
# Or read from config if you add it
```

### Issue 4: Data Loading - JSON vs JSONL
**Problem**: Cell 6 assumes JSONL format:
```python
with open(data_file, 'r', encoding='utf-8') as df:
    for line in df:
        data_list.append(json.loads(line))  # ❌ Assumes JSONL
```

**But `config.yaml` points to**:
```yaml
actual_data: "QA_CHild_legal/test_data.json"  # JSON format, not JSONL
```

**Fix**: Handle both JSON and JSONL:
```python
data_file = config['actual_data']
data_list = []

if data_file.endswith('.jsonl'):
    with open(data_file, 'r', encoding='utf-8') as df:
        for line in df:
            if line.strip():
                data_list.append(json.loads(line))
else:  # JSON format
    with open(data_file, 'r', encoding='utf-8') as df:
        data_list = json.load(df)
```

---

## ✅ Corrected Critique Notebook Structure

The critique notebook should:

1. **Load config.yaml** ✅ (Cell 3 - already correct)
2. **Load RAG contexts** from `config['rag_retrieved_context']` (JSONL format)
3. **Load ARR results** from the result log directory (based on `config['save_file_main_model']`)
4. **Load test data** from `config['actual_data']` (handle both JSON and JSONL)
5. **Generate critiques** using Llama-3.1-8B-Instruct
6. **Save to `Critique.jsonl`**

---

## 🔧 Recommended Fixes

### Fix 1: Remove/Update Cell 0
Either:
- **Option A**: Delete Cell 0 entirely (it's not needed for critique)
- **Option B**: Move it to a separate cleanup script `tools/filter_judge_output.py`

### Fix 2: Update Cell 4 (RAG Context Loading)
Replace Excel loading with JSONL loading from config.

### Fix 3: Update Cell 5 (ARR Results Loading)
Use config-based path instead of hardcoded file.

### Fix 4: Update Cell 6 (Data Loading)
Handle both JSON and JSONL formats.

---

## 📝 Summary

| File | Purpose | When Used | Format |
|------|---------|-----------|--------|
| `test_data.json` | Test dataset (canonical questions) | All stages | JSON array |
| `data.jsonl` | Same as above, JSONL format | If converted | JSONL (one JSON per line) |
| `judge1.jsonl` | Judge stage output | After Step 6 | JSONL |
| `judge2.jsonl` | Alternative judge output | After Step 6 | JSONL |
| `rag_retrieved_questions.jsonl` | RAG contexts | ARR, Critique, Defense | JSONL |
| `result_<model>_main_architecture.jsonl` | ARR stage output | Critique, Defense, Judge | JSONL |

**Key Point**: The critique notebook should **NOT** depend on judge outputs. It only needs:
- Test data (from config)
- RAG contexts (from config)
- ARR results (from result log)

