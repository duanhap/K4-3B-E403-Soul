"""
knowledge_base.py — Module quản lý Knowledge Base độc lập với bot.py

Tách riêng để:
  1. Dễ mở rộng KB mà không đụng logic bot
  2. Test KB độc lập (python knowledge_base.py)
  3. CP3: golden set có thể import module này để test trực tiếp
"""

import json
from pathlib import Path
from typing import Optional

# ─────────────────────────────────────────────
# Đường dẫn file KB — luôn relative với file này
# ─────────────────────────────────────────────
KB_FILE_PATH = Path(__file__).parent / "knowledge.json"

# ─────────────────────────────────────────────
# CRUD cơ bản
# ─────────────────────────────────────────────

def load() -> list[dict]:
    """Tải toàn bộ KB từ file JSON. Trả về [] nếu file lỗi."""
    if not KB_FILE_PATH.exists():
        print(f"⚠️  KB file không tồn tại: {KB_FILE_PATH}")
        return []
    try:
        with open(KB_FILE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError) as e:
        print(f"⚠️  Lỗi đọc KB: {e}")
        return []


def save(kb_data: list[dict]) -> bool:
    """Ghi KB vào file JSON. Trả về True nếu thành công."""
    try:
        with open(KB_FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(kb_data, f, ensure_ascii=False, indent=2)
        return True
    except OSError as e:
        print(f"❌  Lỗi ghi KB: {e}")
        return False


def add_item(title: str, content: str, category: str = "Cập nhật mới", link: str = "") -> dict:
    """
    Thêm 1 mục mới vào KB và lưu file.
    Trả về item vừa thêm.
    """
    kb = load()
    new_id = f"KB_{len(kb) + 1:03d}"
    item = {
        "id": new_id,
        "category": category,
        "title": title,
        "content": content,
        "link": link,
    }
    kb.append(item)
    save(kb)
    return item


def remove_item(item_id: str) -> bool:
    """Xóa mục theo id. Trả về True nếu tìm thấy và xóa được."""
    kb = load()
    original_len = len(kb)
    kb = [item for item in kb if item.get("id") != item_id]
    if len(kb) == original_len:
        return False  # Không tìm thấy id
    return save(kb)


def get_by_id(item_id: str) -> Optional[dict]:
    """Lấy 1 mục theo id."""
    for item in load():
        if item.get("id") == item_id:
            return item
    return None


# ─────────────────────────────────────────────
# Tìm kiếm / format cho prompt
# ─────────────────────────────────────────────

def search(query: str, top_k: int = 5) -> list[dict]:
    """
    Tìm kiếm đơn giản theo keyword trong title, content, category.
    Trả về tối đa top_k kết quả khớp nhất (theo số từ khớp).
    """
    kb = load()
    query_lower = query.lower()
    query_words = set(query_lower.split())

    scored: list[tuple[int, dict]] = []
    for item in kb:
        text = " ".join([
            item.get("title", ""),
            item.get("content", ""),
            item.get("category", ""),
        ]).lower()
        score = sum(1 for w in query_words if w in text)
        if score > 0:
            scored.append((score, item))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [item for _, item in scored[:top_k]]


def format_for_prompt(kb_items: Optional[list[dict]] = None) -> str:
    """
    Chuyển KB (hoặc toàn bộ nếu không truyền) thành chuỗi context cho LLM.
    Link KHÔNG đưa vào prompt — tránh LLM copy đường dẫn nội bộ vào reply.
    Format: - [title]: content
    """
    items = kb_items if kb_items is not None else load()
    if not items:
        return "(Chưa có dữ liệu chính thức trong KB)"
    lines = []
    for item in items:
        lines.append(f"- [{item.get('title', '')}]: {item.get('content', '')}")
    return "\n".join(lines)


def stats() -> dict:
    """Trả về thống kê nhanh về KB (dùng để debug/log)."""
    kb = load()
    categories: dict[str, int] = {}
    for item in kb:
        cat = item.get("category", "Không rõ")
        categories[cat] = categories.get(cat, 0) + 1
    return {
        "total": len(kb),
        "categories": categories,
        "file": str(KB_FILE_PATH),
    }


# ─────────────────────────────────────────────
# Chạy trực tiếp để kiểm tra KB
# ─────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 60)
    print("KIỂM TRA KNOWLEDGE BASE")
    print("=" * 60)

    s = stats()
    print(f"\n📊 Tổng số mục: {s['total']}")
    print(f"📁 File: {s['file']}")
    print("\n📂 Phân loại theo category:")
    for cat, count in sorted(s["categories"].items()):
        print(f"   {cat}: {count} mục")

    print("\n" + "-" * 60)
    print("🔍 Test search('hạn nộp lab'):")
    results = search("hạn nộp lab")
    for r in results:
        print(f"   [{r['id']}] {r['title']}")

    print("\n🔍 Test search('git push lỗi'):")
    results = search("git push lỗi")
    for r in results:
        print(f"   [{r['id']}] {r['title']}")

    print("\n🔍 Test search('điểm danh workshop'):")
    results = search("điểm danh workshop")
    for r in results:
        print(f"   [{r['id']}] {r['title']}")

    print("\n✅ KB module hoạt động bình thường.")
