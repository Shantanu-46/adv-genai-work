"""measure.py: same 5 bank questions on every profile -> results.csv (S10 + S11 reference)."""
import csv
import time

from providers import PROVIDERS, connect

QUESTIONS = [
    "What is the difference between a savings account and a fixed deposit?",
    "What is the monthly EMI on a loan of Rs 10 lakh at 9% annual interest for 20 years?",
    "Explain KYC in two sentences to a first-time bank customer.",
    "I shared my OTP with a caller who said he was from the bank. What should I do right now?",
    "Translate into Hindi: 'Your fixed deposit matures next week.'",
]
SYSTEM = {"role": "system",
          "content": "You are a concise retail-bank assistant."}
rows = [["profile", "question", "seconds", "tokens_per_s", "prompt_tokens", "completion_tokens", "answer"]]
for name in PROVIDERS:
    client, model = connect(name)
    for q in QUESTIONS:
        msgs = [SYSTEM, {"role": "user", "content": q}]
        try:
            t0 = time.perf_counter()
            r = client.chat.completions.create(model=model, messages=msgs)
            secs = time.perf_counter() - t0
        except Exception as e:  # a failed profile is a finding, not a crash
            rows.append([name, q, "", "", "", "", f"ERROR: {type(e).__name__}: {str(e)[:120]}"])
            continue
        u = r.usage
        tps = u.completion_tokens / secs
        rows.append([name, q, round(secs, 2), round(tps),
                     u.prompt_tokens, u.completion_tokens,
                     r.choices[0].message.content])
        print(f"{name:11} {secs:6.2f}s {tps:6.0f} tok/s  {q[:40]}")
        time.sleep(2)              # kind to free tiers
with open("results.csv", "w", newline="", encoding="utf-8") as f:
    csv.writer(f).writerows(rows)
print("wrote results.csv")