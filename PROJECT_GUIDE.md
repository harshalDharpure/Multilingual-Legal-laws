# VERA: QA Child Legal Bot - Complete Project Guide

## 📋 Table of Contents
1. [Research Paper Overview](#research-paper-overview)
2. [Project Architecture](#project-architecture)
3. [Understanding the VERA Framework](#understanding-the-vera-framework)
4. [How to Run the Complete Project](#how-to-run-the-complete-project)
5. [Project Structure](#project-structure)
6. [Key Components](#key-components)

---

## 📄 Research Paper Overview

### Title
**VERA: A Structured and Verified Reasoning Pipeline for Sensitive Legal Question Answering**

### Key Contributions
The research paper presents VERA, a multi-stage legal reasoning framework designed for **Child Sexual Abuse (CSA) legal support** in India. The system addresses the critical need for trustworthy AI-assisted legal question answering in high-stakes, sensitive legal domains.

### Main Achievements
- **93.8% QA accuracy** on the Child Abuse Legal Support Dataset (CALSD)
- **NLI consistency score of 0.7984** (21% improvement over baselines)
- Dataset of **10,000 MCQ-style legal QA instances** derived from Indian CSA case law
- Multi-stage reasoning pipeline ensuring legal faithfulness and interpretability

### Dataset: CALSD (Child Abuse Legal Support Dataset)
- 10,000 multiple-choice question-answer pairs
- Derived from 6,000 Indian court judgments
- Grounded in Indian statutory provisions:
  - POCSO Act (Protection of Children from Sexual Offences)
  - IPC (Indian Penal Code)
  - JJ Act (Juvenile Justice Act)

---

## 🏗️ Project Architecture

### Multi-Stage Pipeline Flow

```
User Query (Legal Question)
    ↓
[RAG] Retrieval-Augmented Generation
    ↓ (Retrieved Legal Context)
[ARR] Analyze, Reason, Respond Prompting
    ↓ (Initial Answer + Reasoning)
[CDA] Critique-Debate-Adjudicate Framework
    ├── Critique Model (Challenger)
    ├── Defense Model (Defender)
    └── Judge Model (Adjudicator)
    ↓ (Final Answer + Judge Reasoning)
[CoV] Chain of Verification
    ↓ (Verified Answer + Corrected Reasoning)
[VERA] Verified ARR-enhanced Response Aggregation
    ↓
Final Answer with Legal Reasoning
```

---

## 🔍 Understanding the VERA Framework

### Stage 1: RAG (Retrieval-Augmented Generation)
**Purpose**: Retrieve relevant legal context from a corpus of Indian child protection laws

**Implementation** (`rag.ipynb`):
- Uses FAISS vector store for similarity search
- Embedding model: `intfloat/e5-base-v2` or similar
- Chunk size: 500 characters with 50 character overlap
- Retrieves top-K (typically 5) most relevant legal document chunks

**Key Files**:
- `rag.ipynb`: RAG implementation
- `child_laws.txt`: Legal corpus containing Indian child protection laws

### Stage 2: ARR (Analyze, Reason, Respond) Prompting
**Purpose**: Generate structured legal reasoning using retrieved context

**Three-Step Process**:
1. **Analyze**: Understand the question and retrieved legal context
2. **Reason**: Compare each option against the context
3. **Respond**: Select the correct option with detailed reasoning

**Implementation** (`ARR_model_qwen.ipynb`):
- Model: `Qwen2.5-7B-Instruct` or `Qwen2.5-1.5B-Instruct`
- Uses structured prompting from `ARR_prompting.txt`
- Outputs JSON format with Answer and Reasoning

**Key Files**:
- `ARR_model_qwen.ipynb`: ARR implementation
- `ARR_prompting.txt`: ARR prompt template

### Stage 3: CDA (Critique-Debate-Adjudicate)
**Purpose**: Refine answers through adversarial reasoning

#### 3.1 Critique Model (`critique.ipynb`)
- **Role**: Challenger - identifies flaws in initial reasoning
- **Model**: `Llama-3.1-8B-Instruct`
- **Task**: Critically assess reasoning, identify logical gaps, misinterpretations

#### 3.2 Defense Model (`Defense.ipynb`)
- **Role**: Defender - defends the original answer
- **Model**: `Qwen2.5-7B-Instruct`
- **Task**: Rebut critiques, reinforce correct answer using legal context

#### 3.3 Judge Model (`judgements.py`)
- **Role**: Neutral adjudicator
- **Model**: `Llama-3.2-3B-Instruct` or `Llama-3.1-8B-Instruct`
- **Task**: 
  - Declare winner (Challenger or Defender)
  - Provide final correct answer
  - Generate final reasoning and judgement

**Output Format**:
```json
{
    "Winner": "Challenger/Defender",
    "Correct Answer": "Full text of correct option",
    "Judgement": "Reasoning for winner",
    "final_reasoning": "Overall final reasoning"
}
```

### Stage 4: CoV (Chain of Verification)
**Purpose**: Independently verify and correct the final answer

**Implementation** (`COV.ipynb`):
- Model: `Llama-3.1-8B-Instruct` (via Ollama)
- **Verification Steps**:
  1. Analyze retrieved legal context
  2. Evaluate each option (A/B/C/D) as Supported/Not Supported
  3. Verify the model's chosen option
  4. Correct if needed and provide final reasoning

**Output**: Verified answer with correction if needed

### Stage 5: VERA (Verified ARR-enhanced Response Aggregation)
**Purpose**: Synthesize final response combining verified facts and interpretive reasoning

**Merging Strategy**:
- Combines `Rˆverified` (from CoV) and `Rˆfinal` (from Judge)
- Prioritizes factual claims from verification
- Retains interpretive richness from debate

---

## 🚀 How to Run the Complete Project

### Prerequisites

1. **Python Environment**:
   ```bash
   pip install transformers datasets scikit-learn pandas numpy 
   pip install sentence-transformers pyyaml openpyxl langchain
   pip install faiss-cpu  # or faiss-gpu for GPU support
   pip install huggingface-hub accelerate bitsandbytes
   ```

2. **HuggingFace Authentication**:
   - Get your HuggingFace token from https://huggingface.co/settings/tokens
   - Login: `huggingface-cli login` or use `login()` in code

3. **Ollama (for CoV stage)**:
   - Install Ollama: https://ollama.ai/
   - Pull model: `ollama pull llama3.1:8b`

4. **Hardware Requirements**:
   - GPU recommended (NVIDIA GPU with CUDA support)
   - Minimum 16GB RAM
   - Sufficient disk space for models (10-20GB)

### Step-by-Step Execution

#### Step 1: Prepare Data and Legal Corpus

1. **Legal Corpus** (`child_laws.txt`):
   - Should contain Indian child protection laws
   - Already provided in the project

2. **Dataset Files**:
   - `train_data.jsonl`: Training data (8,000 samples)
   - `test_data.json`: Test data (2,000 samples)
   - Each entry format:
     ```json
     {
         "Passage": "...",
         "Question": "...",
         "A": "...",
         "B": "...",
         "C": "...",
         "D": "...",
         "Correct Answer": "...",
         "Reasoning": "..."
     }
     ```

#### Step 2: Build RAG Vector Store (`rag.ipynb`)

```python
# Run cells in rag.ipynb
# This will:
# 1. Load legal corpus (child_laws.txt)
# 2. Create document chunks
# 3. Build FAISS index
# 4. Generate retrieved_context for each question
# 5. Save to rag_retrieved_questions.jsonl
```

**Output**: `rag_retrieved_questions.jsonl` with retrieved context for each question

#### Step 3: ARR Reasoning (`ARR_model_qwen.ipynb`)

```python
# Run cells in ARR_model_qwen.ipynb
# This will:
# 1. Load model: Qwen2.5-7B-Instruct
# 2. Load ARR prompt template
# 3. Process each question with retrieved context
# 4. Generate initial answer and reasoning
# 5. Save to result_qwen7b_main_architecture.jsonl
```

**Output**: `result_qwen7b_main_architecture.jsonl` with:
- Question
- Predicted Answer
- main_model_reasoning

#### Step 4: Critique Stage (`critique.ipynb`)

```python
# Run cells in critique.ipynb
# This will:
# 1. Load Llama-3.1-8B-Instruct
# 2. For each question, generate critique of initial answer
# 3. Save to Critique.jsonl
```

**Output**: `Critique.jsonl` with critique for each question

#### Step 5: Defense Stage (`Defense.ipynb`)

```python
# Run cells in Defense.ipynb
# This will:
# 1. Load Qwen2.5-7B-Instruct
# 2. For each question, generate defense against critique
# 3. Save to Defense.jsonl
```

**Output**: `Defense.jsonl` with defense for each question

#### Step 6: Judge Stage (`judgements.py`)

```python
# Run judgements.py
# This will:
# 1. Load Llama-3.2-3B-Instruct
# 2. For each question, judge between critique and defense
# 3. Declare winner and final answer
# 4. Save to judge1.jsonl or judge2.jsonl
```

**Output**: `judge1.jsonl` with:
- Winner (Challenger/Defender)
- Correct Answer
- Judgement
- final_reasoning

#### Step 7: Chain of Verification (`COV.ipynb`)

```python
# Run cells in COV.ipynb
# This will:
# 1. Use Ollama with llama3.1:8b
# 2. For each question, verify the judge's answer
# 3. Correct if needed
# 4. Save to cov.jsonl
```

**Output**: `cov.jsonl` with verified answer and reasoning

#### Step 8: Final Aggregation (VERA)

Combine outputs from:
- ARR reasoning (`main_model_reasoning`)
- Judge reasoning (`final_reasoning`)
- CoV verification (`verified_reasoning`)

Create final ensemble answer.

### Configuration File

Create `config.yaml`:
```yaml
arr_prompt: "ARR_prompting.txt"
actual_data: "test_data.json"  # or train_data.jsonl
rag_retrieved_context: "rag_retrieved_questions.jsonl"
save_file_main_model: "qwen7b"
```

---

## 📁 Project Structure

```
QA_CHild_legal/
│
├── researchpaper.txt              # Complete research paper
├── child_laws.txt                 # Legal corpus (Indian child protection laws)
├── ARR_prompting.txt              # ARR prompt template
│
├── Data Files:
├── train_data.jsonl               # Training dataset (8,000 samples)
├── test_data.json                 # Test dataset (2,000 samples)
│
├── Notebooks (Execution Order):
├── rag.ipynb                      # Step 1: RAG implementation
├── ARR_model_qwen.ipynb          # Step 2: ARR reasoning
├── critique.ipynb                 # Step 3: Critique stage
├── Defense.ipynb                  # Step 4: Defense stage
├── COV.ipynb                      # Step 5: Chain of Verification
│
├── Python Scripts:
├── judgements.py                  # Step 6: Judge/adjudication
│
└── Output Files (Generated):
    ├── rag_retrieved_questions.jsonl
    ├── result_qwen7b_main_architecture.jsonl
    ├── Critique.jsonl
    ├── Defense.jsonl
    ├── judge1.jsonl
    └── cov.jsonl
```

---

## 🔑 Key Components

### Models Used

1. **Qwen2.5-7B-Instruct**: ARR and Defense stages
   - Long-context, instruction-tuned
   - Good for structured reasoning

2. **Llama-3.1-8B-Instruct**: Critique stage
   - Fine-tuned for critique tasks
   - Identifies flaws effectively

3. **Llama-3.2-3B-Instruct**: Judge stage
   - Balanced reasoning capability
   - Efficient for adjudication

4. **Sentence Transformers**: Semantic matching
   - `paraphrase-mpnet-base-v2`: For option matching
   - `intfloat/e5-base-v2`: For RAG embeddings

### Evaluation Metrics

1. **Classification Accuracy**:
   - Percentage of correctly predicted answers
   - Uses semantic similarity for option matching

2. **NLI Entailment Score**:
   - Measures logical consistency of reasoning
   - Uses `facebook/bart-large-mnli` model
   - Score: 0.7984 (highest achieved)

### Key Features

1. **Statutory Fidelity**: All reasoning grounded in Indian legal statutes
2. **Interpretability**: Each stage provides explainable reasoning
3. **Verification**: Multi-level verification ensures correctness
4. **Adversarial Robustness**: Critique-debate improves answer quality

---

## 📊 Expected Results

Based on the research paper:
- **QA Accuracy**: 93.8%
- **NLI Score**: 0.7984
- **Improvement over baselines**: 19-21% in NLI scores

---

## ⚠️ Important Notes

1. **Sequential Execution**: Run stages in order (RAG → ARR → Critique → Defense → Judge → CoV)
2. **Checkpointing**: Each stage saves results incrementally to avoid re-processing
3. **Memory Management**: Use quantization (8-bit) for large models if needed
4. **API Keys**: Ensure HuggingFace token is set for model downloads
5. **Ollama Setup**: Required for CoV stage - ensure Ollama is running

---

## 🔬 Research Contributions

1. **First framework** for CSA legal QA in Indian context
2. **CALSD dataset**: 10,000 verified legal QA pairs
3. **Multi-stage reasoning**: Combines RAG, ARR, CDA, CoV
4. **Verified outputs**: Ensures legal faithfulness and interpretability
5. **Practical deployment**: Validated by legal experts

---

## 📚 References

The complete research paper is available in `researchpaper.txt` with:
- Detailed methodology
- Ablation studies
- Qualitative case studies
- Expert evaluation results
- Complete bibliography

---

## 🆘 Troubleshooting

1. **Model Loading Issues**: 
   - Check HuggingFace authentication
   - Ensure sufficient disk space
   - Use `device_map="auto"` for GPU allocation

2. **FAISS Issues**:
   - Install `faiss-cpu` or `faiss-gpu` based on your system
   - Check CUDA compatibility for GPU version

3. **Ollama Connection**:
   - Ensure Ollama is running: `ollama serve`
   - Verify model is pulled: `ollama list`

4. **Memory Errors**:
   - Reduce batch size
   - Use 8-bit quantization
   - Process in smaller chunks

---

## 📝 Summary

VERA is a comprehensive multi-stage legal reasoning framework designed for sensitive child protection legal questions in India. The system combines:
- **Retrieval** (RAG) for legal grounding
- **Structured reasoning** (ARR) for interpretability
- **Adversarial refinement** (CDA) for robustness
- **Verification** (CoV) for correctness
- **Aggregation** (VERA) for final output

The complete pipeline ensures legal faithfulness, interpretability, and high accuracy - critical for deployment in real-world legal support scenarios.

