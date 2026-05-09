# app/rag/generator.py

import re
import torch
import logging
from transformers import AutoTokenizer, AutoModelForCausalLM
from huggingface_hub import logging as hf_logging

logging.basicConfig(level=logging.INFO)
hf_logging.set_verbosity_info()

MODEL_NAME = "Qwen/Qwen2.5-3B-Instruct"

print("[GEN] Loading Qwen generator...")

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME,
    trust_remote_code=True
)

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    device_map="auto",
    torch_dtype=torch.float16,
    trust_remote_code=True
)

print("[GEN] Generator loaded.")




def clean_context(text: str) -> str:
    text = text.replace("<|im_start|>", "")
    text = text.replace("<|im_end|>", "")
    text = text.replace("User:", "")
    text = text.replace("Assistant:", "")
    text = text.replace("Human:", "")
    text = text.replace("###", "")

    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"!\[.*?\]\(.*?\)", " ", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)

    text = "\n".join(
        line for line in text.splitlines()
        if not re.match(r"^\s*\|.*\|\s*$", line)
    )

    text = re.sub(r"\s+", " ", text)

    return text.strip()




def build_context_from_retrieved(
    retrieved_list,
    chunks_map,
    top_k=5,
    max_chars=None
):
    ctx_parts = []

    for r in retrieved_list[:top_k]:
        cid = r.get("chunk_id")
        text = chunks_map.get(cid)
        if text:
            ctx_parts.append(f"--- CHUNK {cid} ---\n{text}\n")

    context = "\n".join(ctx_parts).strip()

    if max_chars and len(context) > max_chars:
        half = max_chars // 2
        context = context[:half] + "\n...\n" + context[-half:]

    return clean_context(context)




def generate_rag_answer_local(
    query: str,
    context: str,
    max_new_tokens: int = 150,
    temperature: float = 0.0
) -> str:

    query = (
        query.replace("<|im_start|>", "")
             .replace("<|im_end|>", "")
             .replace("###", "")
             .replace("User:", "")
             .replace("Assistant:", "")
             .replace("Human:", "")
    )

    prompt = (
        "<|im_start|>system\n"
        "You are an assistant that answers ONLY using the provided context.\n"
        "Write a short, factual answer.\n"
        "Do NOT continue the conversation.\n"
        "Do NOT ask questions.\n"
        "Do NOT add examples.\n"
        "Do NOT add disclaimers.\n"
        "Stop immediately after the answer.\n"
        "<|im_end|>\n"
        "<|im_start|>user\n"
        f"Context:\n{context}\n\n"
        f"Question:\n{query}\n"
        "<|im_end|>\n"
        "<|im_start|>assistant\n"
    )

    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

    out = model.generate(
        **inputs,
        max_new_tokens=max_new_tokens,
        do_sample=False,
        temperature=temperature,
        eos_token_id=tokenizer.convert_tokens_to_ids("<|im_end|>"),
        pad_token_id=tokenizer.eos_token_id,
    )

    text = tokenizer.decode(out[0], skip_special_tokens=False)

    answer = text.split("<|im_start|>assistant")[-1]
    answer = answer.split("<|im_end|>")[0].strip()

    return answer
