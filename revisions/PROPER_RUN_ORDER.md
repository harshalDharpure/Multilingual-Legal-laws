# ✅ Proper Run Order - Complete Evaluation Pipeline

## 📋 Prerequisites

1. **Install dependencies**:
   ```bash
   pip install transformers datasets scikit-learn pandas numpy sentence-transformers pyyaml openpyxl accelerate
   ```

2. **HuggingFace Login** (if needed):
   - Add your HF token in notebooks where `login()` is called

3. **Verify `config.yaml` exists**:
   ```yaml
   arr_prompt: "QA_CHild_legal/ARR_prompting.txt"
   actual_data: "QA_CHild_legal/test_data.json"
   rag_retrieved_context: "QA_CHild_legal/rag_retrieved_questions.jsonl"
   save_file_main_model: "qwen7b"
   ```

---

## 🔄 Execution Order

### **Step 0: Prepare User-Style Subsets** (Already Done ✅)

You've already generated:
- `QA_CHild_legal/calsd_real_test_layperson.json`
- `QA_CHild_legal/calsd_real_test_frontline.json`
- `QA_CHild_legal/calsd_real_test_paralegal.json`

**Note**: These are in JSON format. If any notebook expects JSONL, convert using:
```bash
python QA_CHild_legal/utils.py QA_CHild_legal/calsd_real_test_layperson.json QA_CHild_legal/calsd_real_test_layperson.jsonl
```

---

### **Step 1: Build RAG Contexts (Canonical)**

**File**: `QA_CHild_legal/rag.ipynb`

**Actions**:
1. Open `rag.ipynb`
2. Run all cells
3. Verify output: `QA_CHild_legal/rag_retrieved_questions.jsonl`

**Expected Output**:
- JSONL file with `Question` and `retrieved_context` fields
- One line per question from `test_data.json`

---

### **Step 2: ARR on Canonical Data (with Routing Logs)**

**File**: `QA_CHild_legal/ARR_model_qwen.ipynb`

**Before Running**:
1. Ensure `config.yaml` has:
   ```yaml
   actual_data: "QA_CHild_legal/test_data.json"
   rag_retrieved_context: "QA_CHild_legal/rag_retrieved_questions.jsonl"
   ```

2. **Fix the notebook** (if not already done):
   - Ensure `get_best_option()` handles None values (already fixed ✅)
   - Ensure `model_output()` has error handling (already fixed ✅)

**Actions**:
1. Open `ARR_model_qwen.ipynb`
2. Run all cells
3. Check output directory: `result_log/qwen7b/result_qwen7b_main_architecture.jsonl`

**Expected Output Fields**:
- `Question`
- `Correct Answer`
- `Predicted`
- `main_model_reasoning`
- `arr_similarity_margin` (new)
- `retrieved_context_len` (new)
- `route` (new: 'simple' or 'full')

---

### **Step 3: ARR on User-Style Subsets**

**For each subset** (layperson, frontline, paralegal):

#### 3a. Layperson Subset
1. **Update `config.yaml`**:
   ```yaml
   actual_data: "QA_CHild_legal/calsd_real_test_layperson.json"
   ```

2. **Run `ARR_model_qwen.ipynb`** (all cells)

3. **Rename output** (to avoid overwriting):
   ```bash
   mv result_log/qwen7b/result_qwen7b_main_architecture.jsonl \
      result_log/qwen7b/result_qwen7b_layperson.jsonl
   ```

#### 3b. Frontline Subset
1. **Update `config.yaml`**:
   ```yaml
   actual_data: "QA_CHild_legal/calsd_real_test_frontline.json"
   ```

2. **Run `ARR_model_qwen.ipynb`** (all cells)

3. **Rename output**:
   ```bash
   mv result_log/qwen7b/result_qwen7b_main_architecture.jsonl \
      result_log/qwen7b/result_qwen7b_frontline.jsonl
   ```

#### 3c. Paralegal Subset
1. **Update `config.yaml`**:
   ```yaml
   actual_data: "QA_CHild_legal/calsd_real_test_paralegal.json"
   ```

2. **Run `ARR_model_qwen.ipynb`** (all cells)

3. **Rename output**:
   ```bash
   mv result_log/qwen7b/result_qwen7b_main_architecture.jsonl \
      result_log/qwen7b/result_qwen7b_paralegal.jsonl
   ```

**After all subsets**:
- Restore `config.yaml` to canonical:
  ```yaml
  actual_data: "QA_CHild_legal/test_data.json"
  ```

---

### **Step 4: Critique Stage** (Canonical First)

**File**: `QA_CHild_legal/critique.ipynb`

**⚠️ FIXES NEEDED** (before running):

1. **Remove/Comment Cell 0** (judge filtering - not needed for critique)

2. **Fix Cell 4** (RAG context loading):
   ```python
   # OLD (wrong):
   contexts_file="rag.xlsx"
   context_df = pd.read_excel(contexts_file)
   
   # NEW (correct):
   contexts_file = config['rag_retrieved_context']
   context_dict = {}
   with open(contexts_file, 'r', encoding='utf-8') as cf:
       for line in cf:
           entry = json.loads(line)
           question = entry.get('Question')
           retrieved_context = entry.get('retrieved_context')
           if question and retrieved_context:
               context_dict[question] = retrieved_context
   ```

3. **Fix Cell 5** (ARR results loading):
   ```python
   # OLD (wrong):
   contexts_file1="result_qwen7b_main_architecture05032025.jsonl"
   
   # NEW (correct):
   model_name = config['save_file_main_model']
   contexts_file1 = f"result_log/{model_name}/result_{model_name}_main_architecture.jsonl"
   context_dict1 = {}
   with open(contexts_file1, 'r', encoding='utf-8') as cf:
       for line in cf:
           entry = json.loads(line)
           question = entry.get('Question')
           retrieved_context = entry.get('main_model_reasoning')
           if question and retrieved_context:
               context_dict1[question] = retrieved_context
   ```

4. **Fix Cell 6** (Data loading - handle JSON/JSONL):
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

**Actions**:
1. Apply fixes above
2. Ensure `config.yaml` points to canonical data:
   ```yaml
   actual_data: "QA_CHild_legal/test_data.json"
   ```
3. Run all cells in `critique.ipynb`
4. Verify output: `QA_CHild_legal/Critique.jsonl`

**Expected Output**:
- JSONL with `Question` and `Critique` fields

---

### **Step 5: Defense Stage**

**File**: `QA_CHild_legal/Defense.ipynb`

**Before Running**:
- Ensure `Critique.jsonl` exists (from Step 4)
- Ensure `config.yaml` points to canonical data

**Actions**:
1. Open `Defense.ipynb`
2. Check that it loads:
   - Test data from `config['actual_data']`
   - ARR results (for main_model_reasoning)
   - Critique from `Critique.jsonl`
   - RAG contexts from `config['rag_retrieved_context']`
3. Run all cells
4. Verify output: `QA_CHild_legal/Defense.jsonl`

**Expected Output**:
- JSONL with `Question` and `Defense` fields

---

### **Step 6: Judge Stage**

**File**: `QA_CHild_legal/judgements.py`

**Before Running**:
- Ensure `Defense.jsonl` exists
- Ensure `Critique.jsonl` exists
- Ensure ARR results exist

**Actions**:
1. **Update `judgements.py`** (if needed):
   - Check file paths match your setup
   - Verify it reads from:
     - ARR results: `result_log/qwen7b/result_qwen7b_main_architecture.jsonl`
     - Critique: `Critique.jsonl`
     - Defense: `Defense.jsonl`
     - Test data: `config['actual_data']`

2. **Run**:
   ```bash
   cd QA_CHild_legal
   python judgements.py
   ```

3. Verify output: `judge2.jsonl` (or `judge1.jsonl` as configured)

**Expected Output**:
- JSONL with `Question`, `Winner`, `Correct Answer`, `Judgement`, `final_reasoning`

---

### **Step 7: CoV with Fallacy Checks**

**File**: `QA_CHild_legal/COV.ipynb`

**Before Running**:
- Ensure `judge2.jsonl` (or `judge1.jsonl`) exists
- Verify CoV notebook has fallacy checks (already updated ✅)

**Actions**:
1. Open `COV.ipynb`
2. Check that `judge_file` variable points to correct judge output
3. Run all cells
4. Verify output: `QA_CHild_legal/cov.jsonl`

**Expected Output Fields**:
- `Verification.option_verdicts` (A/B/C/D: Supported/Not Supported)
- `Verification.fallacy_report` (misapplication, missing_elements, procedural_errors)
- `Verification.chosen_option_verdict` (Fully Verified/Partially Verified/Not Verified)
- `Verification.verification_reasoning`
- `Correct Answer`
- `final_reasoning`

---

### **Step 8: Simple-Case Bypass Analysis**

**Script**: Create analysis script or use notebook

**Actions**:
1. Load ARR outputs from Step 2:
   - `result_log/qwen7b/result_qwen7b_main_architecture.jsonl`

2. Aggregate by `route` field:
   ```python
   import json
   
   simple_count = 0
   full_count = 0
   
   with open('result_log/qwen7b/result_qwen7b_main_architecture.jsonl', 'r') as f:
       for line in f:
           entry = json.loads(line)
           route = entry.get('route', 'full')
           if route == 'simple':
               simple_count += 1
           else:
               full_count += 1
   
   total = simple_count + full_count
   simple_pct = (simple_count / total) * 100 if total > 0 else 0
   
   print(f"Simple cases: {simple_count} ({simple_pct:.1f}%)")
   print(f"Full pipeline: {full_count} ({100-simple_pct:.1f}%)")
   ```

3. Compute accuracy/NLI deltas (compare simple vs full routes)

4. Estimate token/time savings

---

### **Step 9: Robustness/OOD Evaluation** (Optional)

**Actions**:
1. Download external dataset (CaseHOLD/LegalBench/LLeQA)
2. Run ARR + CoV zero-shot
3. Collect Accuracy/NLI metrics
4. Analyze error patterns

---

### **Step 10: Human-Centered Evaluation** (Optional)

**File**: `QA_CHild_legal/revisions/HUMAN_EVAL_PROTOCOL.md`

**Actions**:
1. Sample 200 items (100 canonical, 100 user-style)
2. Get stakeholder ratings per protocol
3. Compute mean±SD per metric
4. Calculate Cohen's κ for inter-annotator agreement

---

### **Step 11: Assemble Results**

**Actions**:
1. Create summary tables:
   - Canonical vs user-style (3 subsets) Accuracy/NLI
   - CoV fallacy counts/corrections
   - Gating savings (compute vs accuracy)
   - OOD results (if done)
   - Stakeholder metrics (if done)

2. Update manuscript using:
   - `revisions/ABSTRACT_AND_METHOD_EDITS.md`
   - `revisions/RESPONSE_TO_REVIEWERS.md`

3. Build DOCX package per:
   - `revisions/REVISION_PACKAGE_CHECKLIST.md`

---

## 📝 Quick Reference: File Dependencies

```
test_data.json (canonical)
    ↓
rag.ipynb → rag_retrieved_questions.jsonl
    ↓
ARR_model_qwen.ipynb → result_qwen7b_main_architecture.jsonl
    ↓
critique.ipynb → Critique.jsonl
    ↓
Defense.ipynb → Defense.jsonl
    ↓
judgements.py → judge2.jsonl
    ↓
COV.ipynb → cov.jsonl
```

**User-style subsets** (parallel path):
```
calsd_real_test_*.json → ARR → result_qwen7b_*.jsonl
(Optional: Continue through Critique/Defense/Judge/CoV)
```

---

## ⚠️ Common Issues & Fixes

1. **JSON vs JSONL**: Always check file format. Use `utils.py` to convert if needed.

2. **File paths**: Use `config.yaml` for paths. Avoid hardcoded paths.

3. **Missing files**: Ensure previous step completed successfully before proceeding.

4. **Memory issues**: Process in batches if dataset is large.

5. **Model loading**: Ensure HF token is set if models are private.

---

## ✅ Verification Checklist

After each step, verify:
- [ ] Output file exists
- [ ] Output has expected fields
- [ ] No errors in logs
- [ ] File format matches expectations (JSON vs JSONL)
- [ ] Config.yaml is correct for next step

