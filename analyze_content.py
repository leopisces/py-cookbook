"""Analyze py-cookbook content structure for website data extraction."""
import ast
import os
import json

base = os.path.dirname(os.path.abspath(__file__))
chapters = sorted([d for d in os.listdir(base) if d[:2].isdigit() and os.path.isdir(os.path.join(base, d))])
results = []

for ch in chapters:
    chpath = os.path.join(base, ch)
    files = sorted([f for f in os.listdir(chpath) if f.endswith(".py")])
    for f in files:
        fpath = os.path.join(chpath, f)
        try:
            src = open(fpath, encoding="utf-8").read()
            tree = ast.parse(src)
            doc = ast.get_docstring(tree) or ""
            first_line = doc.split("\n")[0].strip() if doc else ""
            # Check if has main() function
            has_main = any(node.name == "main" for node in ast.walk(tree) if isinstance(node, ast.FunctionDef))
            # Get 学习目标 lines
            goals = []
            in_goals = False
            for line in doc.split("\n"):
                stripped = line.strip()
                if "学习目标" in stripped or "学习目标" in stripped:
                    in_goals = True
                    continue
                if in_goals and stripped.startswith("-"):
                    goals.append(stripped[2:].strip())
                elif in_goals and not stripped.startswith("-") and stripped and not stripped.startswith("="):
                    if not any(kw in stripped for kw in ["=", "---", "参考", "Python"]):
                        goals.append(stripped)
            results.append({
                "chapter": ch,
                "file": f,
                "title": first_line,
                "goals_count": len(goals),
                "has_main": has_main,
                "goals": goals[:3],  # first 3 goals only for preview
            })
        except Exception as e:
            results.append({"chapter": ch, "file": f, "title": f"ERROR: {e}", "goals_count": 0, "has_main": False, "goals": []})

print(json.dumps(results[:10], indent=2, ensure_ascii=False))
print(f"\nTotal: {len(results)} files analyzed")

# Summary stats
chapters_with_files = {}
for r in results:
    ch = r["chapter"]
    if ch not in chapters_with_files:
        chapters_with_files[ch] = 0
    chapters_with_files[ch] += 1

print("\nChapter summary:")
for ch, count in sorted(chapters_with_files.items()):
    titles = [r["title"] for r in results if r["chapter"] == ch]
    print(f"  {ch}: {count} files, titles: {titles[:2]}...")