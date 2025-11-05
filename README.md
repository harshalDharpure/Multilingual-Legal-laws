<<<<<<< HEAD
# Multilingual-Legal-laws
Multilingual-Legal-laws
=======
# VERA: QA Child Legal Bot

## Quick Overview

This project implements **VERA** (Verified and Reasoned Answer), a multi-stage legal reasoning framework for answering sensitive child protection legal questions in India. The system achieves **93.8% accuracy** and **0.7984 NLI score** on the Child Abuse Legal Support Dataset (CALSD).

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install transformers datasets scikit-learn pandas numpy 
pip install sentence-transformers pyyaml openpyxl langchain faiss-cpu
pip install huggingface-hub accelerate bitsandbytes
```

### 2. Setup HuggingFace

```python
from huggingface_hub import login
login('YOUR_HUGGINGFACE_TOKEN')
```

### 3. Setup Ollama (for CoV stage)

```bash
# Install Ollama from https://ollama.ai/
ollama pull llama3.1:8b
```

### 4. Run Pipeline (Sequential Order)

1. **RAG Stage** (`rag.ipynb`): Build vector store and retrieve legal context
2. **ARR Stage** (`ARR_model_qwen.ipynb`): Generate initial answer with reasoning
3. **Critique Stage** (`critique.ipynb`): Generate critique of initial answer
4. **Defense Stage** (`Defense.ipynb`): Generate defense against critique
5. **Judge Stage** (`judgements.py`): Adjudicate between critique and defense
6. **CoV Stage** (`COV.ipynb`): Verify and correct final answer

## 📖 Complete Documentation

See **[PROJECT_GUIDE.md](PROJECT_GUIDE.md)** for:
- Complete research paper understanding
- Detailed architecture explanation
- Step-by-step execution guide
- Troubleshooting tips

## 📊 Pipeline Flow

```
Question → RAG → ARR → Critique → Defense → Judge → CoV → Final Answer
```

## 📁 Key Files

- `researchpaper.txt`: Complete research paper
- `PROJECT_GUIDE.md`: Comprehensive project documentation
- `child_laws.txt`: Legal corpus (Indian child protection laws)
- `test_data.json`: Test dataset (2,000 samples)
- `train_data.jsonl`: Training dataset (8,000 samples)

## 🎯 Key Features

- **Multi-stage reasoning** for high accuracy
- **Legal grounding** in Indian statutes (POCSO, IPC, JJ Act)
- **Interpretable outputs** with detailed reasoning
- **Verified answers** through chain-of-verification
- **Adversarial refinement** via critique-debate

## 📈 Results

- **QA Accuracy**: 93.8%
- **NLI Score**: 0.7984
- **Improvement**: 19-21% over baseline models

## ⚠️ Requirements

- Python 3.8+
- GPU recommended (16GB+ VRAM)
- 16GB+ RAM
- HuggingFace account and token
- Ollama installed (for CoV stage)

## 📝 Citation

If you use this work, please cite the research paper in `researchpaper.txt`.

---

For detailed information, see **[PROJECT_GUIDE.md](PROJECT_GUIDE.md)**

>>>>>>> 4b59b72 (latest-update)
