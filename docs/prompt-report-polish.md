# PROMPT v1 — Đại tu 3 lớp: Ngôn ngữ + Hình thức + Mockup Coverage

> **Cách dùng:** session ZCode mới, working dir = repo report (`mobile-report`). Repo app tại `~/StudioProjects/mobile-app` (chỉ đọc).
> **Skill đề xuất:** `@agency-senior-developer` (chính) + `@agency-code-reviewer` (QC cuối). KHÔNG dùng orchestrator — 3 việc này tuần tự, không cần pipeline.

---

## 0. NGUYÊN TẮC

1. **Làm theo thứ tự 1 → 2 → 3.** Mỗi phần xong phải build PDF kiểm chứng trước khi sang phần sau.
2. **Không bịa nội dung.** Mọi chỉnh sửa phải giữ nguyên ý nghĩa kỹ thuật, chỉ đổi cách diễn đạt.
3. **Không commit/push.** Build local, để working tree cho user duyệt.

---

## 1. ĐƠN GIẢN HOÁ NGÔN NGŨ TOÀN BÀI

### Mục tiêu
Đọc từng file `.tex` trong `sections/` (tất cả Phần 1-4) và sửa:

**1a. Bỏ sến súa / AI-isms:**
- ~~"ra đời để"~~ → "nhằm" hoặc "để"
- ~~"cốt lõi"~~ → "chính" (nếu lặp quá nhiều lần)
- ~~"nền tảng"~~ lặp 5 lần trong 1 đoạn → dùng từ khác
- ~~"kéo theo"~~ → "gây ra" hoặc "khiến"
- ~~"không chỉ... mà còn"~~ → tách 2 câu
- ~~"chính là"~~ → bỏ (thừa)
- ~~"đáng chú ý" / "đáng kể"~~ → "quan trọng"
- Mọi câu quá 40 từ → tách ngắn
- Mọi đoạn quá 6 câu → tách đoạn

**1b. Chuẩn hoá in đậm / in nghiêng:**
- **In đậm**: CHỈ dùng cho tiêu đề bảng, mã tính năng, và kết luận quan trọng (tối đa 1-2 lần/đoạn)
- **In nghiêng**: CHỈ dùng cho thuật tiếng Anh lần đầu xuất hiện + nhấn nhẹ 1 từ. KHÔNG nghiêng cả cụm.
- **~--~** (em-dash): tối đa 1 lần/đoạn. Nếu nhiều hơn → tách câu hoặc đổi thành dấu chấm.
- **\textit{...}** bao cả câu dài → bỏ, chỉ giữ text thường
- **Số đếm**: "ba thành viên" → "3 thành viên" (chuẩn technical writing)

**1c. Chuẩn hoá mũi tên và toán tử:**
- `$\rightarrow$` → dùng "→" trong text mode (hoặc "sang" nếu ngắn)
- `$\cap$` → "giao" hoặc "vừa...vừa..."
- `$\geq$` → "≥" (không cần math mode cho 1 ký tự đơn)
- `$\times$` → "×"
- Nếu công thức đơn giản (1 ký tự) → dùng Unicode thay math mode

**1d. Ví dụ Before → After:**
```
TRƯỚC:
"Quy trình thiết kế của nhóm đi thẳng từ sơ đồ luồng sang bản dựng
trong Jetpack Compose: mỗi màn hình được phác bố cục dạng wireframe
khối, sau đó được cài đặt trực tiếp bằng component và token Material 3"

SAU:
"Nhóm thiết kế trực tiếp bằng Jetpack Compose với component
Material 3, không qua công cụ trung gian."
```

### Cách làm
Duyệt từng file `.tex`:
1. Đọc toàn bộ
2. Áp dụng các quy tắc 1a-1c
3. Lưu, build PDF, check lỗi
4. Chuyển file tiếp

### Files cần sửa
```
sections/1-project-overview/problem-statement.tex
sections/1-project-overview/market-research.tex
sections/1-project-overview/user-personas.tex
sections/1-project-overview/usp-winning-zone.tex
sections/1-project-overview/quality-pillars.tex
sections/2-product-scope/feature-prioritization.tex
sections/2-product-scope/mvp-scope.tex
sections/2-product-scope/user-stories.tex
sections/3-ui-ux-design/information-architecture.tex
sections/3-ui-ux-design/user-flows.tex
sections/3-ui-ux-design/wireframes-prototypes.tex
sections/3-ui-ux-design/design-system.tex
sections/3-ui-ux-design/accessibility.tex
sections/3-ui-ux-design/micro-interactions.tex
sections/3-ui-ux-design/heuristic-evaluation.tex
sections/4-technical-architecture/mobile-constraints.tex
sections/4-technical-architecture/platform-selection.tex
sections/4-technical-architecture/layered-architecture.tex
sections/4-technical-architecture/lifecycle-state.tex
```

---

## 2. SỬA HÌNH ẢNH / BẢNG / DIAGRAM

### Mục tiêu
Mọi hình + bảng phải đọc được rõ ràng, không chồng chữ, không tràn lề.

### Cách kiểm tra
Build PDF → render từng trang có hình/bảng → kiểm tra pixel:

```python
import pymupdf
doc = pymupdf.open('main.pdf')
# render trang có hình/bảng
for i in range(len(doc)):
    page = doc[i]
    has_img = len(page.get_images()) > 0
    has_table = 'Bảng' in page.get_text() or 'bảng' in page.get_text()
    if has_img or has_table:
        pix = page.get_pixmap(dpi=150)
        pix.save(f'/tmp/page_{i+1}.png')
```

### Quy tắc sửa

**Bảng (longtable / tabularx):**
- Tổng độ rộng cột `p{}` + `2×tabcolsep×số_cột` ≤ `\textwidth` (17cm)
- Nếu cột chữ hẹp → giảm `\small` xuống `\footnotesize`
- Cột "Ghi chú" quá dài → đặt `>{\raggedright\arraybackslash}p{Xcm}` + thêm `\\` ngắt dòng thủ công
- Nếu bảng quá nhiều cột (>6) → gộp cột hoặc tách bảng

**Diagram TikZ:**
- Node chồng node → tăng `node distance`
- Chữ tràn node → thêm `text width=` cho node
- Arrow chồng chữ → thêm `above`/`below` cho label
- Nếu diagram quá phức tạp → đơn giản hoá (bớt node, gộp nhánh)
- `\resizebox{\textwidth}{!}{...}` cho diagram rộng

**Ảnh chụp (screenshots):**
- Nếu 5+ ảnh trên 1 hàng → giảm `width` xuống `0.14\textwidth` hoặc tách 2 hàng
- Caption quá dài → rút gọn, chi tiết đưa vào body text
- Ảnh cách nhau ít nhất `4pt` (thêm `\hspace{2pt}` nếu cần)

**Overfull / Underfull:**
```bash
grep -n "Overfull" build/main.log | grep -v "0\.\d" # chỉ >1pt
```
Mọi overfull >1pt phải được xử lý.

---

## 3. MAPPING MOCKUP + MINH HOẠ MÀU

### 3a. Bảng mapping tính năng ↔ mockup

Thêm vào **mục 3.3 (Mockup)** một bảng lớn: **mỗi dòng = 1 tính năng decided, cột:**

| Mã | Tính năng | Mockup hiện có | Trạng thái |
|---|---|---|---|
| F-VID-01 | Xem video | `video-player-light.png` | ✅ Có |
| F-VID-02 | Feed theo sở thích | (code viết, chưa verify) | ⏳ |
| F-VID-03 | Tìm kiếm video | — | 📷 Placeholder |
| ... | ... | ... | ... |

- **Danh sách 48 tính năng decided**: lấy từ `docs/feature-audit-build.py` → `DECIDED` list
- **Ảnh có sẵn**: `figures/app/` (28 file)
- **Placeholder**: dùng `\fbox{\parbox{0.28\textwidth}{\centering\vspace{2cm}Chưa chụp\vspace{2cm}}}` — KHÔNG dùng ảnh giả
- Sắp xếp theo phân hệ (A-Video, B-Music, C-News, D-Games, Dùng chung)
- Cuối bảng: đếm tổng (X có mockup / Y placeholder / Z đã có sẵn)

### 3b. Minh hoạ màu cho bảng token (3.4 Design System)

Thêm **cột swatch màu** vào bảng `tab:design-tokens`:

```latex
% Cột mới: ô màu
\newcommand{\swatch}[1]{\textcolor[HTML]{#1}{\rule{1.2cm}{0.5cm}}}

% Bảng:
\begin{tabularx}{\textwidth}{...p{1.8cm} p{2.8cm} p{2.8cm} p{2.8cm} X}
\toprule
\textbf{Vai trò} & \textbf{Light} & \textbf{Dark} & \textbf{Swatch L/D} & \textbf{Dùng cho} \\
\midrule
primary & \swatch{41690F} \newline 41690F & \swatch{B8F36E} \newline B8F36E & ... & Nút chính \\
...
```

Hoặc đơn giản hơn: thêm 1 cột với `\textcolor{white}{\rule{1cm}{0.4cm}}` nền màu:
```latex
\newcommand{\colorsw}[2]{\colorbox[HTML]{#1}{\textcolor[HTML]{#2}{\rule{0pt}{0.35cm}\hspace{0.9cm}}}}
% \colorsw{41690F}{FFFFFF} → ô màu nền xanh chữ trắng
```

### 3c. Minh hoạ tương phản (3.5 Accessibility)

Thêm **ví dụ trực quan** cạnh bảng tương phản:

```latex
% Ví dụ: 2 dòng chữ trên nền thật
\colorbox[HTML]{F8FAF2}{\textcolor[HTML]{191D17}{\rule{0pt}{0.5cm}Nền sáng, chữ tối — 16,2:1 \checkmark}} \\[4pt]
\colorbox[HTML]{10140E}{\textcolor[HTML]{E0E4D8}{\rule{0pt}{0.5cm}Nền tối, chữ sáng — 14,4:1 \checkmark}} \\[4pt]
\colorbox[HTML]{41690F}{\textcolor[HTML]{FFFFFF}{\rule{0pt}{0.5cm}Nút chính, chữ trắng — 6,5:1 \checkmark}}
```

Thêm **minh hoạ vùng chạm 48dp**:
```latex
\begin{tikzpicture}[scale=0.8]
    \draw[dashed] (0,0) rectangle (4.8,4.8); % vùng chạm 48dp (toạ độ scaled)
    \fill[gray!30] (1.4,1.4) rectangle (3.4,3.4); % icon 20dp
    \node at (2.4,5.4) {\small Vùng chạm 48dp};
    \node at (2.4,-0.6) {\small Icon 20dp};
\end{tikzpicture}
```

---

## 4. THỨ TỰ THỰC HIỆN

1. **Phần 1** (ngôn ngữ): duyệt 19 file `.tex` → build → check → tiếp
2. **Phần 2** (hình thức): render PDF → fix từng trang có vấn đề → build lại → check
3. **Phần 3** (mapping + màu): thêm bảng + swatch → build → check

Sau mỗi phần: build PDF + verify 0 lỗi + gửi user xem trước khi sang phần sau.

---

## 5. ACCEPTANCE CHECK

| # | Kiểm tra | Mong muốn |
|---|---|---|
| TC1 | grep "ra đời để\|cơ chế nền\|trọng tài\|đỡ nhau\|bám vào\|tái hiện đúng" sections/ | 0 kết quả |
| TC2 | Đếm `\textit{` mỗi file | ≤ 3 lần/file |
| TC3 | Đếm `\textbf{` mỗi file | ≤ 8 lần/file (trừ header bảng) |
| TC4 | Đếm `~--~` mỗi file | ≤ 3 lần/file |
| TC5 | Overfull >1pt trong build/main.log | 0 |
| TC6 | PDF build | 0 lỗi `!` |
| TC7 | Bảng mapping mockup có đủ 48 dòng | đúng 48 |
| TC8 | Bảng token có cột swatch màu | có |
| TC9 | Bảng tương phản có ví dụ trực quan | có |
| TC10 | Git | chỉ working tree, không commit |

---

## 6. TUYỆT ĐỐI KHÔNG

- Không bịa ảnh mockup mới (nếu chưa có → placeholder text)
- Không đổi nội dung kỹ thuật (số liệu, mã tính năng, cấu trúc bảng)
- Không thêm package LaTeX mới trừ khi bắt buộc (thử hết cách dùng package có sẵn)
- Không commit/push

## 7. KNOWN LIMITATIONS

1. Một số diagram TikZ có thể cần thiết kế lại hoàn toàn (không chỉ chỉnh khoảng cách)
2. Bảng mapping 48 dòng sẽ dài 2-3 trang — chấp nhận được vì là bảng tham chiếu
3. Swatch màu dùng `\colorbox` — nếu màu quá nhạt thì chữ khó đọc, cân nhắc thêm viền `\fbox`
