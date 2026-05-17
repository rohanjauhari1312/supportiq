"""
Eval harness for SupportIQ.

Metrics:
  - Precision@k: fraction of retrieved sources that match expected_source_ids
  - Recall@k: fraction of expected sources found in top-k results
  - Keyword hit rate: fraction of expected_keywords present in the answer
  - Mean latency (ms)

Usage:
  python -m eval.run_eval [--top-k 5] [--output results.json]
"""
import argparse, json, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from pipeline.generate import query as rag_query


def precision_at_k(retrieved_ids: list[str], expected_ids: list[str]) -> float:
    if not retrieved_ids:
        return 0.0
    hits = sum(1 for r in retrieved_ids if any(e in r for e in expected_ids))
    return hits / len(retrieved_ids)


def recall_at_k(retrieved_ids: list[str], expected_ids: list[str]) -> float:
    if not expected_ids:
        return 1.0
    hits = sum(1 for e in expected_ids if any(e in r for r in retrieved_ids))
    return hits / len(expected_ids)


def keyword_hit_rate(answer: str, keywords: list[str]) -> float:
    if not keywords:
        return 1.0
    answer_lower = answer.lower()
    return sum(1 for kw in keywords if kw.lower() in answer_lower) / len(keywords)


def run_eval(top_k: int = 5, output_path: str | None = None):
    test_path = Path(__file__).parent / "test_set.json"
    with open(test_path) as f:
        test_cases = json.load(f)

    results = []
    total_precision, total_recall, total_khr, total_latency = 0.0, 0.0, 0.0, 0.0

    for case in test_cases:
        result = rag_query(case["query"], top_k=top_k)
        retrieved_source_ids = [s.get("source_id", "") for s in result.get("sources", [])]

        p = precision_at_k(retrieved_source_ids, case.get("expected_source_ids", []))
        r = recall_at_k(retrieved_source_ids, case.get("expected_source_ids", []))
        khr = keyword_hit_rate(result["answer"], case.get("expected_keywords", []))
        lat = result["latency_ms"]

        total_precision += p
        total_recall += r
        total_khr += khr
        total_latency += lat

        results.append({
            "id": case["id"],
            "query": case["query"],
            "precision_at_k": round(p, 3),
            "recall_at_k": round(r, 3),
            "keyword_hit_rate": round(khr, 3),
            "latency_ms": lat,
            "answer_preview": result["answer"][:200],
        })

        print(f"[{case['id']}] P@{top_k}={p:.2f} R@{top_k}={r:.2f} KHR={khr:.2f} {lat}ms")

    n = len(test_cases)
    summary = {
        "total_cases": n,
        "top_k": top_k,
        "mean_precision_at_k": round(total_precision / n, 3),
        "mean_recall_at_k": round(total_recall / n, 3),
        "mean_keyword_hit_rate": round(total_khr / n, 3),
        "mean_latency_ms": round(total_latency / n),
    }

    print("\n--- Summary ---")
    for k, v in summary.items():
        print(f"  {k}: {v}")

    output = {"summary": summary, "results": results}
    if output_path:
        with open(output_path, "w") as f:
            json.dump(output, f, indent=2)
        print(f"\nResults written to {output_path}")

    return output


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--output", type=str, default=None)
    args = parser.parse_args()
    run_eval(top_k=args.top_k, output_path=args.output)
