from rag_core import retrieve_and_answer
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from tabulate import tabulate


test_cases = [
    {"question": " কল্যানীর বাবার নাম কী ছিল?", "expected_answer": "শম্ভুনাথ বাবু"},
    {"question": "অপরিচিতা গল্পে কল্যানীর বিয়ে না হওয়ার কারন কী ছিল?", "expected_answer": "আত্মমর্যাদা"},
    # {"question": "বিয়ের সময় কল্যাণীর প্রকৃত বয়স কত ছিল?", "expected_answer": "১৫ বছর"},
    # Add more as needed
]

embedder = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

def evaluate():
    results = []
    for case in test_cases:
        answer, context = retrieve_and_answer(case["question"])
        emb_expected = embedder.encode([case["expected_answer"]])
        emb_answer = embedder.encode([answer])
        sim = cosine_similarity(emb_expected, emb_answer)[0][0]
        grounded = case["expected_answer"] in context
        results.append([
            case["question"][:30] + "...",  # Truncate for display
            case["expected_answer"],
            answer[:30] + "...",            # Truncate for display
            f"{sim:.2f}",
            "Yes" if grounded else "No"
        ])
    headers = ["Question", "Expected", "Answer", "Similarity", "Grounded"]
    print(tabulate(results, headers=headers, tablefmt="grid"))

    # Summary metrics
    avg_sim = sum(float(row[3]) for row in results) / len(results)
    grounded_count = sum(1 for row in results if row[4] == "Yes")
    print(f"\nAverage Similarity: {avg_sim:.2f}")
    print(f"Grounded Answers: {grounded_count}/{len(results)}")

if __name__ == "__main__":
    evaluate()