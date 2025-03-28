import torch
import re
import time
from transformers import AutoTokenizer, AutoModelForCausalLM
from datasets import load_dataset
from peft import PeftModel

def extract_answer(text: str) -> float | None:
    """
    Return the first valid numeric answer after '####'.
    Handles integers or decimals, ignores malformed extras.
    """
    match = re.search(r"####\s*(-?\d+(?:\.\d+)?)", text)
    if not match:
        return None
    try:
        return float(match.group(1))
    except ValueError:
        return None

def evaluate_gsm8k_finetuned():
    base_model_id = "meta-llama/Meta-Llama-3.1-8B-Instruct"
    adapter_id = "Bill11235813/lora-grpo-output"
    
    print(f"Loading tokenizer from '{base_model_id}'...")
    tokenizer = AutoTokenizer.from_pretrained(base_model_id)
    tokenizer.padding_side = "left"
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    print(f"Loading base model '{base_model_id}'...")
    base_model = AutoModelForCausalLM.from_pretrained(
        base_model_id, 
        torch_dtype=torch.float16, 
        device_map="auto"
    )
    
    print(f"Loading LoRA adapter from '{adapter_id}'...")
    model = PeftModel.from_pretrained(base_model, adapter_id)
    device = next(model.parameters()).device
    print(f"Model with adapter loaded on {device}\n")

    print("Loading GSM8K test split...")
    dataset = load_dataset("gsm8k", "main", split="test")
    print(f"Total examples: {len(dataset)}\n")

    batch_size = 512  # Same as original script
    correct = total = 0
    start_time = time.time()

    for i in range(0, len(dataset), batch_size):
        batch = [dataset[j] for j in range(i, min(i + batch_size, len(dataset)))]
        prompts = [
            f"""Solve this math problem. Provide your reasoning between <think> and </think>, 
            and put your final answer between <answer> and </answer>. Also inside the <answer> tag, include your numeric answer after '####'.

            For example, if the question is:
            'If Alice has 3 apples and buys 2 more, how many apples does she have?'

            Your answer should be:
            <think>Alice starts with 3 apples, then adds 2, giving 3 + 2 = 5 apples.</think> <answer> Alice has 5 apples #### 5 </answer>

            Question: {ex['question']}
            """
            for ex in batch
        ]

        inputs = tokenizer(prompts, return_tensors="pt", padding=True, truncation=True).to(device)
        print(f"Processing batch {i+1}-{i+len(batch)} | Prompt example:\n{prompts[0]}\n")

        with torch.no_grad():
            outputs = model.generate(**inputs, max_new_tokens=256, temperature=0.1, pad_token_id=tokenizer.eos_token_id)

        responses = tokenizer.batch_decode(outputs[:, inputs.input_ids.shape[1]:], skip_special_tokens=True)
        for idx, (resp, ex) in enumerate(zip(responses, batch)):
            ref_str = ex["answer"].split("####")[-1].strip().replace(",", "")
            ref = float(ref_str)
            pred = extract_answer(resp)

            print(f"Example {i+idx+1}:")
            print("Model response:\n" + resp.strip())
            print(f"Extracted answer: {pred} | Reference answer: {ref}")

            if pred is not None and abs(pred - ref) < 1e-5:
                print("Result: ✓ CORRECT\n")
                correct += 1
            else:
                print("Result: ✗ INCORRECT\n")
            total += 1

        print(f"Current accuracy after {total} examples: {correct}/{total} = {100*correct/total:.2f}%\n{'-'*80}\n")

    elapsed = time.time() - start_time
    accuracy = correct/total if total else 0
    print(f"FINAL RESULTS — {total} examples")
    print(f"Correct: {correct} | Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
    print(f"Total elapsed time: {elapsed:.2f}s")

    return {"total": total, "correct": correct, "accuracy": accuracy, "time": elapsed}

if __name__ == "__main__":
    results = evaluate_gsm8k_finetuned()
    with open("gsm8k_finetuned_eval_verbose.txt", "w") as out:
        out.write(str(results))
    print("Saved detailed results to gsm8k_finetuned_eval_verbose.txt")