import os
import tempfile
import subprocess
import platform
from ai_reviewer import review_text
from rl_search import semantic_search, display_results
from chroma_handler import add_version
import chromadb

# ─── Utility Functions ─────────────────────────────────────────────────────────

def load_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def save_text(file_path, content):
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def save_version(base_name, version, content):
    os.makedirs("versions", exist_ok=True)
    version_path = f"versions/{base_name}_v{version}.txt"
    save_text(version_path, content)
    print(f"\n💾 Saved version {version} to: {version_path}")

def open_text_editor(initial_text):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode='w', encoding='utf-8') as tf:
        tf.write(initial_text)
        tf.flush()
        temp_path = tf.name

    system = platform.system()
    if system == "Windows":
        editor_cmd = ["notepad.exe", temp_path]
    else:
        editor = os.environ.get('EDITOR', 'nano')
        editor_cmd = [editor, temp_path]

    subprocess.call(editor_cmd)

    with open(temp_path, 'r', encoding='utf-8') as f:
        edited_text = f.read()

    os.remove(temp_path)
    return edited_text

def get_next_version_num(doc_id="chapter1"):
    client = chromadb.Client()
    collection = client.get_or_create_collection("content_versions")
    results = collection.get(where={"doc_id": doc_id})
    versions = [int(m['version']) for m in results['metadatas'] if m.get('version')]
    return max(versions, default=0) + 1

# ─── Main Review and Edit Loop ─────────────────────────────────────────────────

def review_and_edit_loop(file_path):
    base_name = "chapter1"
    text = load_text(file_path)
    saved = False

    while True:
        print("\n👀 Review complete! What would you like to do next?")
        print("1. ✅ Accept AI output as final")
        print("2. 📝 Edit manually before saving")
        print("3. ❌ Reject and skip saving")
        print("4. 🔍 Search past versions")
        print("5. 🚪 Exit")

        choice = input("\nEnter your choice (1/2/3/4/5): ").strip()

        if choice == "1":
            version_num = get_next_version_num(doc_id=base_name)
            final_path = f"versions/{base_name}_final_v{version_num}.txt"
            save_text(final_path, text)

            add_version(
                doc_text=text,
                doc_id=base_name,
                version_num=version_num,
                author="Human+AI",
                tags="final"
            )
            saved = True
            print(f"✅ Final version saved to: {final_path}")
            print(f"✅ Final version saved to ChromaDB as version {version_num}")

            cont = input("\n🔁 Do you want to continue reviewing or searching? (y/n): ").strip().lower()
            if cont != "y":
                print("👋 Exiting review loop.")
                break

        elif choice == "2":
            text = open_text_editor(text)
            print("💾 Saved edited version.")
            print("\n🧐 AI Reviewer Feedback:")
            print("-" * 80)
            print(review_text(text))
            print("-" * 80)

        elif choice == "3":
            print("❌ Rejected. No file saved.")
            break

        elif choice == "4":
            if not saved:
                print("⚠️ You must save the final version first using option 1 before searching.")
                continue
            query = input("🔍 Enter your search query:\n> ").strip()
            result = semantic_search(query)
            display_results(result)

        elif choice == "5":
            print("👋 Exiting review loop.")
            break

        else:
            print("⚠️ Invalid choice. Please enter 1, 2, 3, 4, or 5.")

# ─── CLI Entry ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    rewritten_file = input("Enter the path to the rewritten version (e.g., versions/chapter1_v1.txt):\n> ").strip()
    if os.path.exists(rewritten_file):
        review_and_edit_loop(rewritten_file)
    else:
        print("❌ File not found.")
