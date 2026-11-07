#!/usr/bin/env python3
"""Sinh lại các slide Mock Up trong presentation/content/2-scope.tex.

Mỗi F-code có thể có nhiều ảnh chụp (figures/app/<mã>-01.png, -02.png, ...):
- 0 ảnh   -> giữ placeholder (qua \\mockbody)
- 1-3 ảnh -> một slide, ảnh xếp cạnh nhau (qua \\mockbody)
- >=4 ảnh -> CHIA thành nhiều slide, mỗi slide tối đa 3 ảnh

Dữ liệu gốc (mã, module, tên, nhóm ưu tiên) cache trong scripts/mockups.json
lần chạy đầu; chạy lại sau khi thêm ảnh mới: python3 scripts/gen_mockups.py
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCOPE = ROOT / "presentation" / "content" / "3-uiux.tex"
CACHE = ROOT / "scripts" / "mockups.json"
FIG_ROOT = ROOT / "figures" / "app"            # report đọc trực tiếp
FIG_PRES = ROOT / "presentation" / "figures" / "app"  # presentation đọc trước
BEGIN = "% ===== MOCKUP SECTION (sinh bởi scripts/gen_mockups.py — chạy lại sau khi thêm ảnh) ====="
END = "% ===== END MOCKUP ====="

FRAME_RE = re.compile(
    r"\\begin\{frame\}\{Mock Up: ([^}]*)\}\s*\n"
    r"\\mockbody\{(F-[A-Z]{3,4}-\d{2})\}\{([^}]*)\}\{([^}]*)\}\s*\n"
    r"\\end\{frame\}"
)

def img_path(code: str, k: int) -> str | None:
    """Đường dẫn ảnh -0k cho pdflatex chạy trong presentation/ (ưu tiên thư mục riêng)."""
    name = f"{code}-{k:02d}.png"
    if (FIG_PRES / name).exists():
        return f"figures/app/{name}"
    if (FIG_ROOT / name).exists():
        return f"../figures/app/{name}"
    return None

def count_images(code: str) -> int:
    n = 0
    while img_path(code, n + 1):
        n += 1
    return n

def images_block(paths: list[str]) -> str:
    sizes = {1: "[height=6.1cm]", 2: "[width=2.75cm]", 3: "[width=2.32cm]"}
    gaps = {2: r"\hspace{0.25cm}", 3: r"\hspace{0.2cm}"}
    parts = []
    for i, p in enumerate(paths):
        if i:
            parts.append(gaps[len(paths)])
        parts.append(r"\includegraphics" + sizes[len(paths)] + "{" + p + "}")
    return "".join(parts) + "\n"

def frame(module: str, code: str, title: str, desc: str, paths: list[str] | None, part=None) -> str:
    label = module if part is None else f"{module} ({part[0]}/{part[1]})"
    if paths is None:  # chưa có ảnh: placeholder qua macro cũ
        body = f"\\mockbody{{{code}}}{{{title}}}{{{desc}}}"
    else:
        body = (
            "\\begin{columns}[T]\n"
            "\\begin{column}{0.46\\textwidth}\n"
            f"{{\\small\\bfseries\\color{{BKTemplate}} {code}: {title}}}\\\\[2.5mm]\n"
            f"{desc}\n"
            "\\end{column}\n"
            "\\begin{column}{0.50\\textwidth}\n"
            "\\centering\n"
            + images_block(paths) +
            "\\end{column}\n"
            "\\end{columns}"
        )
    return f"\\begin{{frame}}{{Mock Up: {label}}}\n{body}\n\\end{{frame}}\n"

def main() -> None:
    src = SCOPE.read_text(encoding="utf-8")

    # 1) Lấy dữ liệu gốc: từ cache, gộp thêm mockbody mới xuất hiện trong file
    entries: dict[str, dict] = {}
    if CACHE.exists():
        entries = {e["code"]: e for e in json.loads(CACHE.read_text(encoding="utf-8"))}
    for module, code, title, desc in FRAME_RE.findall(src):
        entries[code] = {"code": code, "module": module, "title": title, "desc": desc}
    if not entries:
        sys.exit("Không tìm thấy mockbody nào để làm dữ liệu gốc.")
    # Chặn an toàn: số F-code phải khớp các bảng tính năng trong 2-scope.tex
    table_codes = set(re.findall(r"\\texttt\{(F-[A-Z]{3,4}-\d{2})\}", src))
    missing = table_codes - set(entries)
    if missing and len(entries) < 70:
        sys.exit(f"DỪNG: bảng feature có {len(table_codes)} mã nhưng chỉ parse được {len(entries)} "
                 f"(thiếu {sorted(missing)}) — không ghi đè để tránh mất slide.")
    CACHE.write_text(json.dumps(list(entries.values()), ensure_ascii=False, indent=1), encoding="utf-8")

    # 2) Sinh các frame theo số ảnh hiện có — đúng thứ tự phân hệ
    MODULE_ORDER = {
        "Phân hệ Video": 0,
        "Phân hệ Nhạc": 1,
        "Phân hệ Tin tức": 2,
        "Phân hệ Trò chơi": 3,
        "Dùng chung": 4,
    }
    def order_key(e):
        return (MODULE_ORDER.get(e["module"], 99), e["code"])
    out = [BEGIN, "\n"]
    split = 0
    for code in sorted(entries, key=lambda c: order_key(entries[c])):
        e = entries[code]
        n = count_images(code)
        if n <= 3:
            paths = [p for p in (img_path(code, k) for k in range(1, n + 1)) if p] or None
            out.append(frame(e["module"], code, e["title"], e["desc"], paths))
        else:
            # 4 ảnh trở lên: chia mỗi slide 2 tấm
            chunks = [list(range(i, min(i + 1, n) + 1)) for i in range(1, n + 1, 2)]
            total = len(chunks)
            for idx, chunk in enumerate(chunks, 1):
                paths = [img_path(code, k) for k in chunk]
                out.append(frame(e["module"], code, e["title"], e["desc"], paths, part=(idx, total)))
                split += 1
    out.append(END + "\n")

    # 3) Thay thế (hoặc chèn sau marker) trong 2-scope.tex
    generated = "\n".join(out)
    if BEGIN in src and END in src:
        pre, rest = src.split(BEGIN, 1)
        _, post = rest.split(END, 1)
        src = pre + generated + post
    else:
        sys.exit("Chưa có khối MOCKUP SECTION trong 2-scope.tex — chạy bootstrap trước.")
    SCOPE.write_text(src, encoding="utf-8")
    print(f"Đã sinh {len(entries)} F-code → {len(entries) + split} slide ({split} slide chia thêm).")

if __name__ == "__main__":
    main()
