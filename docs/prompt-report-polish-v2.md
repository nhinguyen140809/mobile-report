# PROMPT v2 — Sửa report THẬT SỰ: từng đoạn văn + từng trang PDF

> **Cách dùng:** session ZCode mới, wd = repo `mobile-report`. Tag `@agency-senior-developer`.
> **Lần trước fail vì:** chỉ regex thay từ, không ĐỌC hiểu ngữ cảnh. Lần này PHẢI đọc từng đoạn, hiểu ý, viết lại.

---

## NGUYÊN TẮC #1: ĐỌC — HIỂU — VIẾT LẠI, KHÔNG CHỈ TÌM-THAY

Không dùng `grep` + `replace`. Phải MỞ file, ĐỌC từng đoạn văn, HỎI: "Một sinh viên/người Việt bình thường có viết câu này không?" Nếu không → viết lại.

### Ví dụ cụ thể trong report hiện tại:

**SAI (hiện tại) — không ai viết vậy:**
| Câu trong report | Tại sao sai |
|---|---|
| "Câu chuyện phiên đầu tiên (first-run)" | "Câu chuyện" + "phiên" trống không. AI-ism. Nên là: "Luồng lần đầu mở app" |
| "Ranh giới thiết kế để không chặn tương lai" | Cú tao. Nên là: "Thiết kế để mở rộng được sau này" |
| "Đây là phần định nghĩa trực tiếp lời hứa liền mạch" | "Lời hứa liền mạch" là gì? Nên bỏ hẳn câu này |
| "MVP không chỉ được định nghĩa bởi tính năng mà bởi 5 phút đầu tiên" | "Định nghĩa bởi" + "5 phút" — nonsense. Nên bỏ |
| "Trải nghiệm xuyên phân hệ liền mạch" | 3 từ ghép undefined. Nên: "Chuyển giữa các tab không bị gián đoạn" |
| "điểm yếu của việc dùng nhiều ứng dụng riêng lẻ" | OK nhưng wordy. Nên: "nhược điểm khi phải cài nhiều app" |
| "không bao giờ lệch nhau~--~điểm yếu của quy trình thiết kế riêng trên Figma" | Câu 40+ từ. Tách. |
| "Phản hồi trước khi có dữ liệu" | Không rõ. Nên: "Hiển thị skeleton khi đang tải" |
| "Đường dẫn sâu, không lặp lại tab" | Jargon. Nên: "Bấm vào nội dung là mở thẳng, không phải chuyển tab rồi tìm" |
| "Nếu thẻ chỉ chuyển tab, người dùng phải tìm lại nội dung vừa thấy" | OK, giữ |
| "song song hoá nhẹ nhất cũng không tồn tại" | "Song song hoá nhẹ nhất"?? Nên: "không thể nghe nhạc khi đọc tin" |
| "đúng trải nghiệm gián đoạn mà sản phẩm muốn khắc phục" | OK |
| "Chỉ định đoạt" | Không phải từ tiếng Việt. Nên: "Quyết định" |
| "Bộ điều phối" | Hơi nặng. "Xử lý" hoặc "Quản lý" |

### Quy tắc viết:
1. **Câu tối đa 25 từ.** Dài hơn → tách.
2. **Chủ ngữ rõ ràng.** "Điều này", "nó" → gọi tên đúng.
3. **Không dịch từ tiếng Anh.** Giữ nguyên: "case", "dock", "PIP", "streak", "popup", "mockup", "user story". KHÔNG viết "cửa sổ nổi" khi ý là "PIP".
4. **Không thêm từ cho "văn".** "vốn", "phải chăng", "tự nhiên", "một cách" — bỏ hết.
5. **Không "play on words".** "đỡ nhau", "gãy theo", "bám vào" — dùng từ trực tiếp.

---

## NGUYÊN TẮC #2: DUYỆT TỪNG TRANG PDF, KHÔNG CHỈ CHECK MARGIN

### Cách làm:
```python
import pymupdf
doc = pymupdf.open('main.pdf')
for i in range(len(doc)):
    page = doc[i]
    pix = page.get_pixmap(dpi=200)  # DPI CAO để thấy chi tiết
    pix.save(f'/tmp/check/page_{i+1:03d}.png')
    # ĐỌC text trên trang này
    text = page.get_text()
    # CHECK: từ nào bị cắt? caption có tách khỏi hình không?
    # CHECK: bảng có cột chữ chèn lên nhau không?
```

### Cụ thể cần check:
1. **Bảng:** cột chữ có chồng lên cột kế bên không? Text có tràn ra ngoài ô không?
2. **Diagram TikZ:** node có chồng node không? Arrow có xuyên qua chữ không? Label có đọc được không?
3. **Ảnh:** có bị méo không? Có quá nhỏ không? Caption có tách rời hình không?
4. **Toàn trang:** có chỗ nào chữ đè lên hình, hình đè lên chữ không?
5. **Trang trắng:** có trang nào trống không lý do không?

### Cách check bảng:
```python
# Tìm các từ có x0 < x0_cột_trước + width_cột_trước
# = từ này bắt đầu TRƯỚC khi cột trước kết thúc = chồng chữ
words = page.get_text('words')
# Group by y-coordinate (cùng dòng)
# Check overlap: word_A.x1 > word_B.x0 khi cùng y
```

### Cách check diagram:
```python
# Render trang ở DPI cao, tìm vùng có đường vẽ (TikZ)
# Check: có vùng chữ (dark pixels) chồng lên vùng đường vẽ khác không?
```

---

## DANH SÁCH FILE CẦN DUYỆT (thứ tự ưu tiên)

### Nhóm 1 — Văn phong tệ nhất (làm trước):
1. `mvp-scope.tex` — nhiều đoạn AI-ism nhất ("Câu chuyện phiên đầu tiên", "Ranh giới thiết kế", "kinh tế điểm")
2. `user-personas.tex` — 73 textbf, 25 em-dash, nhiều câu dài
3. `feature-prioritization.tex` — "Nền tảng kỹ thuật" paragraph + bảng dài
4. `usp-winning-zone.tex` — "Winning Zone" giải thích vòng vo

### Nhóm 2 — Hình/bảng xấu nhất:
5. `information-architecture.tex` — sitemap TikZ, bảng bottom-nav
6. `user-flows.tex` — 3 diagram TikZ (first-run, C1, C3) + bảng truy vết
7. `accessibility.tex` — bảng tương phản + ví dụ màu + touch target
8. `design-system.tex` — bảng token có swatch

### Nhóm 3 — Còn lại:
9. `problem-statement.tex`
10. `market-research.tex`
11. `quality-pillars.tex`
12. `user-stories.tex`
13. `wireframes-prototypes.tex` (mockup section)
14. `micro-interactions.tex`
15. `heuristic-evaluation.tex`
16. `mobile-constraints.tex`
17. `platform-selection.tex`
18. `layered-architecture.tex`
19. `lifecycle-state.tex`

---

## NGUYÊN TẮC #3: MOCKUP PHẢI LÀ ẢNH THẬT, KHÔNG PHẢI BẢNG CHỮ

### Vấn đề hiện tại:
Mục 3.3 hiện có một BẢNG 48 dòng ghi text "Có/Placeholder" — không phải mockup. Người đọc muốn THẤY HÌNH của từng màn hình ứng dụng, không đọc bảng chữ.

### Cách sửa mục 3.3 (Mockup):

**XOÁ bảng mapping text** (tab:mockup-mapping). Thay bằng:

**Cách 1 (nếu màn hình đã có trong app):** chèn ảnh screenshot trực tiếp:
```latex
\begin{figure}[H]
\centering
\includegraphics[width=0.28\textwidth]{figures/app/home-light.png}
\caption{F-VID-01: Trình phát video}
\end{figure}
```

**Cách 2 (nếu màn CHƯA có):** chụp thêm từ emulator. Dùng adb:
```bash
adb shell am start -n com.example.onespace/.MainActivity
# điều hướng tới màn cần chụp
adb exec-out screencap -p > figures/app/<tên-màn>-light.png
```

**Cách 3 (nếu KHÔNG THỂ chụp — chưa code):** tạo placeholder VISUAL:
```latex
\begin{figure}[H]
\centering
\fbox{\parbox[c][6cm][c]{0.3\textwidth}{\centering\large F-VID-03\\Tìm kiếm video\\(chưa có mockup)}}
\caption{F-VID-03: Tìm kiếm video — placeholder}
\end{figure}
```

### Tổ chức mục 3.3 mới:

```
3.3 Mockup
├── Mở đầu: 1-2 câu giới thiệu (không dài dòng)
├── Nhóm màn hình theo phân hệ:
│   ├── A · Video: 4-5 ảnh (player, feed, PIP, search, watchlist)
│   ├── B · Music: 3-4 ảnh (player, dock, playlist, search)
│   ├── C · News: 3-4 ảnh (feed, reader, TTS, quiz)
│   ├── D · Games: 3-4 ảnh (hub, 2048, Snake, quiz)
│   └── Dùng chung: 4-5 ảnh (login, account, settings, pet, shop)
├── Mỗi ảnh: caption ghi rõ mã tính năng + tên màn
└── Tổng kết cuối: đếm "X/Y màn đã có mockup"
```

### Ảnh chụp cần bổ sung (nếu chưa có trong figures/app/):
Kiểm tra 48 tính năng decided → màn nào chưa có ảnh → chụp thêm từ emulator:
- Tìm kiếm video (F-VID-03) → mở tab Video + gõ vào search bar
- Watchlist (F-VID-04) → màn danh sách xem sau
- Audio-only (F-VID-09) → player với nút audio-only
- Chia sẻ (F-VID-11) → menu share
- Hồ sơ nghệ sĩ (F-VID-14) → màn nghệ sĩ
- Playlist video (F-VID-15) → màn playlist
- v.v.

Nếu emulator KHÔNG chạy được → dùng placeholder box (Cách 3), KHÔNG bỏ trống.

---

## QUY TRÌNH CHO TỪNG FILE

### Bước 1: ĐỌC toàn bộ file `.tex`
- Mở file, đọc từ đầu đến cuối
- Ghi chú mọi câu/đoạn có vấn đề (văn phong, logic, ngữ pháp)

### Bước 2: VIẾT LẠI từng đoạn có vấn đề
- Không chỉ thay 1-2 từ — viết lại CẢ CÂU nếu cần
- Đảm bảo: câu ≤25 từ, chủ ngữ rõ, không AI-ism
- GIỮ NGUYÊN: số liệu, mã tính năng, tên thuật ngữ kỹ thuật đúng

### Bước 3: BUILD PDF sau mỗi file
- `python3 scripts/build.py`
- Check 0 lỗi

### Bước 4: RENDER + CHECK trang tương ứng
- Render trang PDF nơi file này xuất hiện
- Check: bảng đẹp chưa? diagram đọc được chưa? chữ không chồng?
- Nếu có vấn đề → fix → build lại → check lại

### Bước 5: Chuyển file tiếp

---

## ACCEPTANCE CHECK (chạy CUỐI CÙNG, trước khi báo user)

```python
# 1. Ngôn ngữ
grep -rn "Câu chuyện\|Ranh giới thiết kế\|đỡ nhau\|Chỉ định đoạt\|song song hoá\|xuyên phân hệ\|điều phối\|Bộ điều phối\|lời hứa" sections/*.tex
# → PHẢI = 0 kết quả

# 2. Overfull
grep -c "Overfull" build/main.log
# → MỌI overfull >1pt phải đã được fix

# 3. Trang có chữ chồng (pixel check)
# Render 100 trang, check overlap: mọi cặp từ cùng dòng có x-coordinate giao nhau

# 4. PDF build
# → 0 lỗi, 0 undefined

# 5. Mockup section KHÔNG có bảng text
grep -c "mockup-mapping" sections/3-ui-ux-design/wireframes-prototypes.tex
# → PHẢI = 0 (đã xoá bảng text, thay bằng ảnh)

# 6. Mockup section CÓ ảnh thật
grep -c "includegraphics" sections/3-ui-ux-design/wireframes-prototypes.tex
# → PHẢI > 10 (nhiều ảnh screenshot)

# 7. Đọc LẠI 5 đoạn ngẫu nhiên trong PDF
# → Mỗi đoạn phải đọc tự nhiên như người viết
```

---

## TUYỆT ĐỐI KHÔNG

- Không chỉ regex thay từ mà không đọc ngữ cảnh
- Không build PDF mà không render check
- Không nói "đã fix" mà không verify từng trang
- Không commit/push
- Không thêm feature mới — chỉ sửa ngôn ngữ + hình thức
