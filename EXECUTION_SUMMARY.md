# VERA Project - Execution Summary

## 📋 How the Project Reads researchpaper.txt

The **researchpaper.txt** file contains the complete research paper that describes the VERA framework. The project itself doesn't directly read this file programmatically - it's the **documentation and reference** for understanding:

1. **The methodology** behind each stage
2. **The theoretical framework** (RAG, ARR, CDA, CoV, VERA)
3. **The evaluation metrics** and results
4. **The dataset construction** process
5. **The implementation details** and hyperparameters

**Key Points from researchpaper.txt:**
- VERA is a multi-stage legal reasoning pipeline
- Designed for Child Sexual Abuse (CSA) legal support in India
- Uses CALSD dataset (10,000 MCQ legal QA pairs)
- Achieves 93.8% accuracy and 0.7984 NLI score
- Combines RAG + ARR + CDA + CoV stages

---

## 🏃 How to Run the Complete Research Project

### **Prerequisites Setup**

1. **Install Python Packages:**
   ```bash
   pip install transformers datasets scikit-learn pandas numpy 
   pip install sentence-transformers pyyaml openpyxl langchain 
   pip install faiss-cpu huggingface-hub accelerate bitsandbytes
   ```

2. **HuggingFace Authentication:**
   ```python
   from huggingface_hub import login
   login('YOUR_HF_TOKEN')  # Get token from https://huggingface.co/settings/tokens
   ```

3. **Ollama Setup (for CoV stage):**
   ```bash
   # Install from https://ollama.ai/
   ollama pull llama3.1:8b
   ```

4. **Create config.yaml:**
   ```yaml
   arr_prompt: "ARR_prompting.txt"
   actual_data: "test_data.json"
   rag_retrieved_context: "rag_retrieved_questions.jsonl"
   save_file_main_model: "qwen7b"
   ```

### **Step-by-Step Execution (In Order)**

#### **STEP 1: RAG (Retrieval-Augmented Generation)**
**File:** `rag.ipynb`

**What it does:**
- Loads `child_laws.txt` (legal corpus)
- Creates document chunks (500 chars, 50 overlap)
- Builds FAISS vector index
- Retrieves relevant legal context for each question
- Saves to `rag_retrieved_questions.jsonl`

**How to run:**
```python
# Open rag.ipynb
# Run all cells sequentially
# Output: rag_retrieved_questions.jsonl
```

**Expected Output:** JSONL file with retrieved context for each question

---

#### **STEP 2: ARR (Analyze, Reason, Respond)**
**File:** `ARR_model_qwen.ipynb`

**What it does:**
- Loads Qwen2.5-7B-Instruct model
- Uses ARR prompting template
- Generates initial answer and reasoning for each question
- Matches answers to options using semantic similarity
- Saves to `result_qwen7b_main_architecture.jsonl`

**How to run:**
```python
# Open ARR_model_qwen.ipynb
# Run all cells sequentially
# Ensure config.yaml exists
# Output: result_qwen7b_main_architecture.jsonl
```

**Expected Output:** JSONL with:
- Question
- Predicted Answer
- main_model_reasoning

---

#### **STEP 3: Critique**
**File:** `critique.ipynb`

**What it does:**
- Loads Llama-3.1-8B-Instruct
- Critiques the initial ARR answer
- Identifies logical gaps and errors
- Saves to `Critique.jsonl`

**How to run:**
```python
# Open critique.ipynb
# Run all cells sequentially
# Output: Critique.jsonl
```

**Expected Output:** JSONL with critique for each question

---

#### **STEP 4: Defense**
**File:** `Defense.ipynb`

**What it does:**
- Loads Qwen2.5-7B-Instruct
- Defends the original answer against critique
- Rebuts critique points using legal context
- Saves to `Defense.jsonl`

**How to run:**
```python
# Open Defense.ipynb
# Run all cells sequentially
# Output: Defense.jsonl
```

**Expected Output:** JSONL with defense for each question

---

#### **STEP 5: Judge (Adjudication)**
**File:** `judgements.py`

**What it does:**
- Loads Llama-3.2-3B-Instruct or Llama-3.1-8B-Instruct
- Evaluates critique vs defense debate
- Declares winner (Challenger or Defender)
- Provides final answer and reasoning
- Saves to `judge1.jsonl` or `judge2.jsonl`

**How to run:**
```bash
python judgements.py
# Or run in Jupyter notebook
```

**Expected Output:** JSONL with:
- Winner (Challenger/Defender)
- Correct Answer
- Judgement
- final_reasoning

---

#### **STEP 6: Chain of Verification (CoV)**
**File:** `COV.ipynb`

**What it does:**
- Uses Ollama with llama3.1:8b model
- Independently verifies the judge's answer
- Evaluates each option (A/B/C/D) against legal context
- Corrects answer if needed
- Saves to `cov.jsonl`

**How to run:**
```python
# Open COV.ipynb
# Ensure Ollama is running: ollama serve
# Run all cells sequentially
# Output: cov.jsonl
```

**Expected Output:** JSONL with verified answer and reasoning

---

#### **STEP 7: Final Aggregation (VERA)**
**Combines all stages:**
- ARR reasoning (`main_model_reasoning`)
- Judge reasoning (`final_reasoning`)
- CoV verification (`verified_reasoning`)

**Final Output:** Comprehensive answer with verified legal reasoning

---

## 🔍 Complete Understanding of the Research Project

### **Problem Statement**
- Need for trustworthy AI-assisted legal support for Child Sexual Abuse cases in India
- Existing systems lack explainability and statutory grounding
- High-stakes domain requires accuracy and interpretability

### **Solution: VERA Framework**

**Multi-Stage Architecture:**

1. **RAG Stage**: Retrieves relevant legal context from Indian child protection laws
   - Uses FAISS vector similarity search
   - Grounds reasoning in statutory provisions

2. **ARR Stage**: Structured reasoning (Analyze → Reason → Respond)
   - Generates interpretable legal reasoning
   - Reduces hallucinations through structured prompting

3. **CDA Stage**: Critique-Debate-Adjudicate
   - **Critique**: Identifies flaws (adversarial perspective)
   - **Defense**: Defends original answer
   - **Judge**: Adjudicates and provides final answer

4. **CoV Stage**: Chain of Verification
   - Independently verifies answer correctness
   - Evaluates each option against legal context
   - Corrects if needed

5. **VERA Stage**: Final aggregation
   - Combines verified facts with interpretive reasoning
   - Ensures legal faithfulness and coherence

### **Dataset: CALSD**
- **10,000 MCQ-style legal QA pairs**
- Derived from 6,000 Indian court judgments
- Grounded in:
  - POCSO Act (Protection of Children from Sexual Offences)
  - IPC (Indian Penal Code)
  - JJ Act (Juvenile Justice Act)

### **Key Results**
- **93.8% QA Accuracy**
- **0.7984 NLI Score** (21% improvement over baselines)
- **Enhanced interpretability** through multi-stage reasoning
- **Legal faithfulness** through statutory grounding

### **Models Used**
- **Qwen2.5-7B-Instruct**: ARR and Defense
- **Llama-3.1-8B-Instruct**: Critique
- **Llama-3.2-3B-Instruct**: Judge
- **Sentence Transformers**: Semantic matching
- **Ollama llama3.1:8b**: CoV verification

### **Evaluation Metrics**
1. **Classification Accuracy**: Percentage of correct answers
2. **NLI Entailment Score**: Logical consistency of reasoning
3. **Citation Density**: Frequency of legal statute references
4. **Expert Evaluation**: Human legal expert assessment

### **Key Contributions**
1. First framework for CSA legal QA in Indian context
2. CALSD dataset: 10,000 verified legal QA pairs
3. Multi-stage reasoning pipeline ensuring accuracy and interpretability
4. Practical validation through expert evaluation

---

## 📊 Data Flow Diagram

```
Input: Legal Question + Options (A, B, C, D)
    ↓
[RAG] → Retrieved Legal Context
    ↓
[ARR] → Initial Answer + Reasoning
    ↓
[Critique] → Critique of Answer
    ↓
[Defense] → Defense of Answer
    ↓
[Judge] → Winner + Final Answer + Reasoning
    ↓
[CoV] → Verified Answer + Corrected Reasoning
    ↓
[VERA] → Final Aggregated Answer
    ↓
Output: Correct Answer + Detailed Legal Reasoning
```

---

## ⚠️ Important Notes

1. **Sequential Execution**: Must run stages in order
2. **Checkpointing**: Each stage saves results incrementally
3. **File Formats**: 
   - Some stages expect `.jsonl` (one JSON per line)
   - `test_data.json` may need conversion to `.jsonl`
4. **Memory Requirements**: GPU recommended for large models
5. **Model Downloads**: First run downloads models (10-20GB)

---

## 🐛 Common Issues & Solutions

1. **HuggingFace Authentication Error**
   - Solution: `huggingface-cli login` or use token in code

2. **FAISS Import Error**
   - Solution: `pip install faiss-cpu` (or `faiss-gpu` for GPU)

3. **Ollama Connection Error**
   - Solution: Ensure `ollama serve` is running

4. **Memory Error**
   - Solution: Use 8-bit quantization, reduce batch size

5. **File Not Found Error**
   - Solution: Check file paths in config.yaml

---

## 📚 Additional Resources

- **Complete Research Paper**: `researchpaper.txt`
- **Detailed Guide**: `PROJECT_GUIDE.md`
- **Quick Start**: `README.md`

---

## ✅ Summary

The VERA project is a **complete end-to-end legal reasoning system** that:
1. Retrieves relevant legal context (RAG)
2. Generates structured reasoning (ARR)
3. Refines through adversarial debate (CDA)
4. Verifies correctness (CoV)
5. Aggregates final answer (VERA)

**To run:** Execute notebooks/scripts in sequential order (RAG → ARR → Critique → Defense → Judge → CoV)

**Expected results:** 93.8% accuracy with highly interpretable legal reasoning grounded in Indian child protection statutes.

