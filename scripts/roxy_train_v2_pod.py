"""
ROXY v2 Fine-Tuning Script — designed to run ON the RunPod pod.
Upload this file to /workspace/train_v2.py, then run:
  nohup python3 /workspace/train_v2.py > /workspace/train_v2.log 2>&1 &
"""
import json, torch, shutil, os
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig, TrainingArguments
from peft import LoraConfig, PeftModel
from trl import SFTTrainer
from datasets import Dataset

NL = chr(10)  # newline character — avoids f-string escaping issues

print("=== ROXY v2 Training ===")
with open("/workspace/roxy-training-v2.jsonl") as f:
    raw = [json.loads(l) for l in f if l.strip()]
print(f"Examples: {len(raw)}")

tok = AutoTokenizer.from_pretrained("Qwen/Qwen3-8B", trust_remote_code=True)
if tok.pad_token is None:
    tok.pad_token = tok.eos_token

def fmt(ex):
    parts = []
    for m in ex.get("messages", []):
        r = m.get("role", "")
        c = m.get("content", "")
        if r == "system":
            parts.append("<|im_start|>system" + NL + str(c) + "<|im_end|>")
        elif r == "user":
            parts.append("<|im_start|>user" + NL + str(c) + "<|im_end|>")
        elif r == "assistant" and c:
            parts.append("<|im_start|>assistant" + NL + str(c) + "<|im_end|>")
        elif r == "assistant" and m.get("tool_calls"):
            tc = m["tool_calls"][0]["function"]
            a = json.loads(tc["arguments"]) if isinstance(tc["arguments"], str) else tc["arguments"]
            tc_json = json.dumps({"name": tc["name"], "arguments": a})
            parts.append("<|im_start|>assistant" + NL + "<tool_call>" + NL + tc_json + NL + "</tool_call><|im_end|>")
        elif r == "tool":
            parts.append("<|im_start|>tool" + NL + str(c) + "<|im_end|>")
    return {"text": NL.join(parts)}

ds = Dataset.from_list([fmt(e) for e in raw])
print(f"Dataset: {len(ds)}")

print("Loading 4-bit model...")
bnb = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True,
)
model = AutoModelForCausalLM.from_pretrained(
    "Qwen/Qwen3-8B",
    quantization_config=bnb,
    device_map="auto",
    trust_remote_code=True,
    dtype=torch.float16,
)

lora = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM",
)

args = TrainingArguments(
    output_dir="/workspace/roxy-lora-v2",
    num_train_epochs=3,
    per_device_train_batch_size=1,
    gradient_accumulation_steps=4,
    learning_rate=2e-4,
    fp16=True,
    logging_steps=10,
    save_strategy="no",
    warmup_steps=10,
    report_to="none",
)

trainer = SFTTrainer(
    model=model,
    processing_class=tok,
    train_dataset=ds,
    args=args,
    peft_config=lora,
)

print("Training...")
trainer.train()
trainer.save_model("/workspace/roxy-lora-v2")
tok.save_pretrained("/workspace/roxy-lora-v2")
print("Training complete!")

# Clean up GPU memory
del model, trainer
torch.cuda.empty_cache()

# Merge LoRA into base model
print("Merging LoRA into base model...")
model2 = AutoModelForCausalLM.from_pretrained(
    "Qwen/Qwen3-8B",
    torch_dtype=torch.float16,
    device_map="cpu",
    trust_remote_code=True,
)
model2 = PeftModel.from_pretrained(model2, "/workspace/roxy-lora-v2")
model2 = model2.merge_and_unload()

shutil.rmtree("/workspace/roxy-merged", ignore_errors=True)
model2.save_pretrained("/workspace/roxy-merged", safe_serialization=True)
tok.save_pretrained("/workspace/roxy-merged")
print("Merged!")

del model2

# Restart vLLM with the new model
print("Starting vLLM with ROXY v2...")
os.system(
    "nohup python3 -m vllm.entrypoints.openai.api_server "
    "--model /workspace/roxy-merged "
    "--served-model-name Qwen/Qwen3-8B "
    "--host 0.0.0.0 --port 8000 "
    "--max-model-len 8192 "
    "--enable-auto-tool-choice --tool-call-parser hermes "
    "--trust-remote-code --dtype auto "
    "--gpu-memory-utilization 0.9 "
    "> /workspace/vllm.log 2>&1 &"
)
print("=== ROXY v2 BAKED AND SERVING ===")
