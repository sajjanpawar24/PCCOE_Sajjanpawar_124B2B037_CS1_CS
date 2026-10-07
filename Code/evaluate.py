"""Step 3: run all test questions and measure quality.
Run:  python Code/evaluate.py              (full: retrieval + LLM answers)
      python Code/evaluate.py --no-llm     (retrieval + extractive answers only, fast)
Outputs go to Evaluation_Results/.
"""
import argparse
import csv
import json

import config
import rag


def norm(s):
    return "".join(s.lower().split())


def answer_correct(text, must_include):
    t = norm(text)
    return all(any(norm(alt) in t for alt in group) for group in must_include)


def main(use_llm):
    questions = json.loads(config.QUESTIONS_PATH.read_text(encoding="utf-8"))
    rows, samples = [], []

    for q in questions:
        res = rag.answer(q["question"], use_llm=use_llm)
        refused = "not found" in res["answer"].lower()
        if q["answerable"]:
            retr = bool(set(q["pages"]) & set(res["retrieved_pages"]))
            correct = (not refused) and answer_correct(res["answer"], q["must_include"])
            cite = bool(set(q["pages"]) & set(res["cited"]))
        else:
            retr, correct, cite = None, refused, None   # correct = refused properly

        rows.append({
            "id": q["id"], "answerable": q["answerable"], "question": q["question"],
            "expected_pages": q["pages"], "retrieved_pages": res["retrieved_pages"],
            "cited_pages": res["cited"], "top_distance": res["top_distance"], "mode": res["mode"],
            "retrieval_hit": retr, "answer_correct": correct, "citation_correct": cite,
            "answer": res["answer"].replace("\n", " "),
        })
        samples.append(f"### Q{q['id']}. {q['question']}\n"
                       f"- Expected: {q['expected_answer']} (pages {q['pages']})\n"
                       f"- System answer: {res['answer']}\n"
                       f"- Cited pages: {res['cited']} | Retrieved pages: {res['retrieved_pages']} | "
                       f"Top distance: {res['top_distance']} | Mode: {res['mode']}\n"
                       f"- Correct: {correct}\n")
        print(f"Q{q['id']:>2} correct={correct} retrieval={retr} citation={cite} dist={res['top_distance']}")

    ans = [r for r in rows if r["answerable"]]
    unans = [r for r in rows if not r["answerable"]]
    pct = lambda n, d: round(100 * n / d, 1) if d else None
    summary = {
        "mode": rows[0]["mode"] if rows else None,
        "total_questions": len(rows),
        "answerable_questions": len(ans),
        "retrieval_hit_rate_pct": pct(sum(r["retrieval_hit"] for r in ans), len(ans)),
        "answer_accuracy_pct": pct(sum(r["answer_correct"] for r in ans), len(ans)),
        "citation_accuracy_pct": pct(sum(r["citation_correct"] for r in ans), len(ans)),
        "unanswerable_questions": len(unans),
        "correct_refusal_pct": pct(sum(r["answer_correct"] for r in unans), len(unans)),
    }

    config.RESULTS_DIR.mkdir(exist_ok=True)
    with open(config.RESULTS_DIR / "results.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    (config.RESULTS_DIR / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    (config.RESULTS_DIR / "sample_outputs.md").write_text(
        "# Sample outputs with citations\n\n" + "\n".join(samples), encoding="utf-8")
    print("\nSUMMARY:\n" + json.dumps(summary, indent=2))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-llm", action="store_true")
    main(use_llm=not ap.parse_args().no_llm)
