# main.py

import os
from playwright.sync_api import sync_playwright
from ai_reviewer import review_text
from transformers import pipeline
from transformers import AutoTokenizer
from chroma_handler import add_version, query_content, get_next_version_num
from human_loop import review_and_edit_loop

# Paths
screenshot_path = "screenshots/chapter1_page.png"
rewrite_path = "versions/chapter1_v1.txt"
final_base = "versions/chapter1_final"

# Step 1: Scrape content + Take Screenshot
def scrape_content(url):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url)
        page.wait_for_selector(".mw-parser-output")
        
        # Save screenshot instead of text file
        os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
        page.screenshot(path=screenshot_path, full_page=True)
        print(f"[📸] Screenshot saved to {screenshot_path}")
        
        text = page.inner_text(".mw-parser-output")
        browser.close()
        return text

# Step 2: Rewrite using a HuggingFace model
def rewrite_with_ai(text, chunk_size=450):
    print("🤖 Loading AI model...")
    summarizer = pipeline("text2text-generation", model="google/flan-t5-base")
    tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-base")

    print("🧩 Splitting input into chunks...")
    tokens = tokenizer.encode(text, return_tensors="pt")[0]
    chunks = [tokens[i:i + chunk_size] for i in range(0, len(tokens), chunk_size)]

    rewritten_chunks = []

    for idx, chunk in enumerate(chunks):
        chunk_text = tokenizer.decode(chunk, skip_special_tokens=True)
        prompt = "Rewrite this clearly:\n" + chunk_text
        print(f"✍️ Rewriting chunk {idx + 1}/{len(chunks)}...")
        rewritten = summarizer(prompt, max_new_tokens=512, truncation=True)[0]['generated_text']
        rewritten_chunks.append(rewritten)

    return "\n\n".join(rewritten_chunks)

# Step 3: Save helper
def save_text(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[💾] Saved to {path}")

# MAIN FLOW
if __name__ == "__main__":
    url = "https://en.wikisource.org/wiki/The_Gates_of_Morning/Book_1/Chapter_1"
    print(f"\n🌐 Scraping content from: {url}")
    raw_text = scrape_content(url)

    print("\n--- Raw Chapter Preview (first 1000 chars) ---\n")
    print(raw_text[:1000], "\n")

    print("✍️ Rewriting with AI...")
    rewritten = rewrite_with_ai(raw_text)
    save_text(rewrite_path, rewritten)

    print("\n🤖 AI Rewritten Output (preview) ---\n")
    print(rewritten[:1000], "...")

    print("\n🧐 AI Reviewer Feedback:")
    print("-" * 80)
    print(review_text(rewritten))
    print("-" * 80)

    # Step 4: Human-in-the-loop full review + edit loop
    review_and_edit_loop(rewrite_path)

    

    # Step 5: Optional query for retrieval
    print("\n🔍 Searching ChromaDB for related versions...")
    result = query_content("AI rewritten chapter")
    for i, doc in enumerate(result['documents'][0]):
        print(f"\n📄 Result {i + 1} Preview:\n{doc[:300]} ...")
