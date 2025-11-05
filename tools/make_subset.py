import json
import os
import random
import re
from typing import Dict, Any, List


def load_json_or_jsonl(path: str) -> List[Dict[str, Any]]:
    if path.endswith('.jsonl'):
        data = []
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    data.append(json.loads(line))
        return data
    with open(path, 'r', encoding='utf-8') as f:
        obj = json.load(f)
        if isinstance(obj, list):
            return obj
        raise ValueError('JSON must be an array of objects')


def save_jsonl(path: str, rows: List[Dict[str, Any]]):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + '\n')


COLLOQUIAL = [
    (r"anticipatory bail", "bail before arrest"),
    (r"juvenile", "minor"),
    (r"statute", "law"),
    (r"provision", "rule"),
    (r"Section\s+19", "reporting rule"),
]


def add_misspellings(text: str, rate: float = 0.03) -> str:
    out = []
    for ch in text:
        if ch.isalpha() and random.random() < rate:
            if ch.lower() == 'o':
                out.append('0')
            elif ch.lower() == 'i':
                out.append('l')
            else:
                out.append(ch.upper() if ch.islower() else ch.lower())
        else:
            out.append(ch)
    return ''.join(out)


def random_insert_delete_swap(text: str, ops: int = 1) -> str:
    if not text:
        return text
    s = list(text)
    for _ in range(ops):
        if not s:
            break
        r = random.random()
        idx = random.randrange(0, len(s))
        if r < 0.33:  # delete
            s.pop(idx)
        elif r < 0.66:  # insert nearby char
            ch = s[idx]
            s.insert(idx, ch)
        else:  # swap
            j = min(len(s) - 1, idx + 1)
            s[idx], s[j] = s[j], s[idx]
    return ''.join(s)


def to_colloquial(text: str) -> str:
    out = text
    for pat, rep in COLLOQUIAL:
        out = re.sub(pat, rep, out, flags=re.IGNORECASE)
    return out


SMS_SLANG = [
    (r"you", "u"),
    (r"are", "r"),
    (r"please", "pls"),
    (r"with", "wid"),
    (r"because", "bcoz"),
]


INDIAN_ENGLISH = [
    (r"police station", "thana"),
    (r"complaint", "FIR"),
    (r"hospital", "govt hospital"),
    (r"lawyer", "advocate"),
]


def apply_list_replacements(text: str, pairs: list, prob: float) -> str:
    out = text
    for pat, rep in pairs:
        if random.random() < prob:
            out = re.sub(pat, rep, out, flags=re.IGNORECASE)
    return out


def fuzz_numbers(text: str, pct: float = 0.1) -> str:
    def repl(m):
        n = m.group(0)
        try:
            val = int(n)
            delta = max(1, int(abs(val) * pct))
            return str(val + random.choice([-delta, delta]))
        except ValueError:
            return n
    return re.sub(r"\b\d{1,3}\b", repl, text)


def random_casing(text: str, prob: float = 0.05) -> str:
    out = []
    for ch in text:
        if ch.isalpha() and random.random() < prob:
            out.append(ch.upper() if ch.islower() else ch.lower())
        else:
            out.append(ch)
    return ''.join(out)


def drop_articles(text: str, prob: float = 0.2) -> str:
    return re.sub(r"\b(the|a|an)\b", lambda m: '' if random.random() < prob else m.group(0), text, flags=re.IGNORECASE)


EXTRANEOUS_PREFIX = [
    "My cousin told me something different last week, but… ",
    "Not sure if this matters, but the school also called us. ",
    "We are very scared and new to this process. ",
]


USER_PROFILES = {
    "layperson": {
        "colloq_prob": 0.7, "sms_prob": 0.4, "indian_prob": 0.4,
        "misspell_rate": 0.03, "ops": 1, "extraneous_prob": 0.5,
        "ambiguity_prob": 0.5, "num_fuzz": 0.1, "case_prob": 0.05,
        "drop_article_prob": 0.2
    },
    "frontline": {
        "colloq_prob": 0.5, "sms_prob": 0.2, "indian_prob": 0.5,
        "misspell_rate": 0.02, "ops": 1, "extraneous_prob": 0.3,
        "ambiguity_prob": 0.4, "num_fuzz": 0.05, "case_prob": 0.03,
        "drop_article_prob": 0.1
    },
    "paralegal": {
        "colloq_prob": 0.3, "sms_prob": 0.1, "indian_prob": 0.3,
        "misspell_rate": 0.01, "ops": 0, "extraneous_prob": 0.2,
        "ambiguity_prob": 0.3, "num_fuzz": 0.02, "case_prob": 0.01,
        "drop_article_prob": 0.05
    }
}


def make_user_question(canonical_q: str, profile: str = "layperson", intensity: float = 1.0) -> (str, Dict[str, Any]):
    cfg = USER_PROFILES.get(profile, USER_PROFILES["layperson"]).copy()
    # scale intensities
    for k in ["colloq_prob","sms_prob","indian_prob","misspell_rate","extraneous_prob","ambiguity_prob","num_fuzz","case_prob","drop_article_prob"]:
        cfg[k] = max(0.0, min(1.0, cfg[k] * intensity))
    cfg["ops"] = max(0, int(cfg["ops"] * intensity))

    noise = {
        "misspellings": 0,
        "colloquialisms": 0,
        "sms_slang": 0,
        "indianism": 0,
        "extraneous": False,
        "ambiguity": False,
        "num_fuzz": False,
        "ops_noise": 0,
        "case_rand": False,
        "drop_articles": False
    }
    q = canonical_q

    if random.random() < cfg["colloq_prob"]:
        q2 = to_colloquial(q)
        if q2 != q:
            noise["colloquialisms"] += 1
            q = q2

    if random.random() < cfg["sms_prob"]:
        q2 = apply_list_replacements(q, SMS_SLANG, prob=0.7)
        if q2 != q:
            noise["sms_slang"] += 1
            q = q2

    if random.random() < cfg["indian_prob"]:
        q2 = apply_list_replacements(q, INDIAN_ENGLISH, prob=0.7)
        if q2 != q:
            noise["indianism"] += 1
            q = q2

    if random.random() < 0.8:  # light character noise frequently present
        ops = cfg["ops"]
        if ops > 0:
            q2 = random_insert_delete_swap(q, ops=ops)
            if q2 != q:
                noise["ops_noise"] += ops
                q = q2

    if random.random() < 0.9:
        q2 = add_misspellings(q, rate=cfg["misspell_rate"])
        if q2 != q:
            noise["misspellings"] += 1
            q = q2

    if random.random() < cfg["extraneous_prob"]:
        q = random.choice(EXTRANEOUS_PREFIX) + q
        noise["extraneous"] = True

    if random.random() < cfg["ambiguity_prob"]:
        q = re.sub(r"POCSO|IPC|JJ\s*Act|Section\s*\d+", "the law", q, flags=re.IGNORECASE)
        noise["ambiguity"] = True

    if random.random() < 0.5:
        q2 = fuzz_numbers(q, pct=cfg["num_fuzz"])
        if q2 != q:
            noise["num_fuzz"] = True
            q = q2

    if random.random() < 0.5:
        q2 = random_casing(q, prob=cfg["case_prob"])
        if q2 != q:
            noise["case_rand"] = True
            q = q2

    if random.random() < 0.4:
        q2 = drop_articles(q, prob=cfg["drop_article_prob"])
        if q2 != q:
            noise["drop_articles"] = True
            q = q2

    return q, noise


def build_subset(rows: List[Dict[str, Any]], n: int, seed: int = 42, profile: str = "layperson", intensity: float = 1.0) -> List[Dict[str, Any]]:
    random.seed(seed)
    sample = rows if len(rows) <= n else random.sample(rows, n)
    out = []
    for i, r in enumerate(sample):
        q_user, noise = make_user_question(r.get('Question') or r.get('question') or '', profile=profile, intensity=intensity)
        rec = {
            "id": f"real-{i}",
            "passage": r.get('Passage') or r.get('passage') or "",
            "question_canonical": r.get('Question') or r.get('question') or "",
            "options": {
                "A": r.get('A') or r.get('a') or "",
                "B": r.get('B') or r.get('b') or "",
                "C": r.get('C') or r.get('c') or "",
                "D": r.get('D') or r.get('d') or "",
            },
            "correct_answer_text": r.get('Correct Answer') or r.get('correct_answer') or "",
            "rationale_statutory": r.get('Reasoning') or r.get('reasoning') or "",
            "question_user": q_user,
            "noise": noise,
            "robustness_tags": []
        }
        # heuristic robustness tag
        if len(rec["question_user"]) > 220:
            rec["robustness_tags"].append("long_context")
        out.append(rec)
    return out


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('--input', required=True, help='Path to train_data.jsonl or test_data.json')
    p.add_argument('--output', required=True, help='Path to output .jsonl')
    p.add_argument('--n', type=int, default=500, help='number of items')
    p.add_argument('--seed', type=int, default=42)
    p.add_argument('--profile', choices=list(USER_PROFILES.keys()), default='layperson', help='user noise profile')
    p.add_argument('--intensity', type=float, default=1.0, help='noise intensity multiplier (0.5..2.0)')
    args = p.parse_args()

    rows = load_json_or_jsonl(args.input)
    subset = build_subset(rows, n=args.n, seed=args.seed, profile=args.profile, intensity=args.intensity)
    save_jsonl(args.output, subset)
    print(f"Wrote {len(subset)} items to {args.output}")


