# PROMPT — Tự động verify PDF + fix + lặp tới sạch

> **Mục tiêu:** Duyệt toàn bộ PDF, tìm MỌI lỗi hình thức, fix, rebuild, verify lại. Lặp tới khi 0 lỗi.

---

## BƯỚC 1: RENDER TOÀN BỘ TRANG THÀNH PNG

```python
import pymupdf, os
doc = pymupdf.open('main.pdf')
os.makedirs('/tmp/verify', exist_ok=True)
for i in range(len(doc)):
    doc[i].get_pixmap(dpi=200).save(f'/tmp/verify/p{i+1:03d}.png')
```

## BƯỚC 2: PHÂN TÍCH TỪNG TRANG BẮT LỖI

### Loại lỗi cần tìm:

**A. Chữ tràn lề phải:**
```python
# Mọi từ có x1 > 540pt (lề phải = 595.28 - 56.7 = 538.6pt)
overflow = [w for w in words if w[2] > 540]
```

**B. Chữ chồng chữ (trong bảng):**
```python
# Group từ theo y (cùng dòng), sort theo x
# Nếu từ trước có x1 > từ sau có x0 + 2 → chồng
for j in range(len(ws) - 1):
    if ws[j][2] > ws[j+1][0] + 2:
        OVERLAP
```

**C. Chữ trong ô bảng tràn ra ngoài ô:**
```python
# Kiểm tra từ có x0 < left_margin hoặc x1 > right_margin của bảng
# Cần biết vị trí cột từ \begin{tabularx} spec
```

**D. Bảng dồn cột (cột quá hẹp, chữ bị ép):**
```python
# Tìm vùng có mật độ từ cao bất thường trên cùng 1 dòng
# Hoặc: nhiều từ rất ngắn (<5 chars) liên tiếp trên cùng y
```

**E. Diagram TikZ node chồng node:**
```python
# Tìm vùng có đường vẽ (drawing) + chữ chồng lên nhau
# Render DPI cao, check vùng có cả vector graphics và text
```

**F. Ảnh méo / quá nhỏ / caption tách rời:**
```python
# Check kích thước ảnh: width < 3cm = quá nhỏ
# Check caption có ở trang khác với ảnh không
```

**G. Trang trắng không lý do:**
```python
# Trang có < 10 từ và không có ảnh
```

### Script phân tích:

```python
import pymupdf
from collections import defaultdict

doc = pymupdf.open('main.pdf')
all_issues = []

for i in range(len(doc)):
    page = doc[i]
    words = page.get_text('words')
    text = page.get_text()
    images = page.get_images()

    # A: Tràn lề
    for w in words:
        if w[2] > 540:
            all_issues.append({
                'page': i+1, 'type': 'TRÀN_LỀ',
                'word': w[4], 'x': w[0], 'x1': w[2], 'y': w[1]
            })

    # B: Chồng chữ
    by_y = defaultdict(list)
    for w in words:
        y_key = round(w[1] / 3) * 3  # group theo 3pt
        by_y[y_key].append(w)
    for y, ws in by_y.items():
        ws.sort(key=lambda w: w[0])
        for j in range(len(ws) - 1):
            if ws[j][2] > ws[j+1][0] + 1:
                all_issues.append({
                    'page': i+1, 'type': 'CHỒNG_CHỮ',
                    'word1': ws[j][4], 'word2': ws[j+1][4],
                    'y': y, 'x1': ws[j][2], 'x2': ws[j+1][0]
                })

    # G: Trang trắng
    if len(words) < 10 and not images and i > 5:
        all_issues.append({
            'page': i+1, 'type': 'TRANG_TRỐNG',
            'word_count': len(words)
        })

    # D: Bảng dồn cột (nhiều từ ngắn liên tiếp cùng y)
    for y, ws in by_y.items():
        if len(ws) > 15:  # quá nhiều từ trên 1 dòng
            short_words = [w for w in ws if len(w[4]) <= 3]
            if len(short_words) > len(ws) * 0.5:
                all_issues.append({
                    'page': i+1, 'type': 'BẢNG_DỒN',
                    'y': y, 'word_count': len(ws),
                    'sample': ' '.join(w[4] for w in ws[:10])
                })

# In báo cáo
print(f"Tổng số lỗi: {len(all_issues)}")
for iss in all_issues:
    if iss['type'] == 'TRÀN_LỀ':
        print(f"  T{iss['page']} TRÀN: '{iss['word'][:30]}' x={iss['x1']:.0f}")
    elif iss['type'] == 'CHỒNG_CHỮ':
        print(f"  T{iss['page']} CHỒNG: '{iss['word1'][:15]}' + '{iss['word2'][:15]}'")
    elif iss['type'] == 'TRANG_TRỐNG':
        print(f"  T{iss['page']} TRỐNG: {iss['word_count']} từ")
    elif iss['type'] == 'BẢNG_DỒN':
        print(f"  T{iss['page']} DỒN: {iss['sample']}")
```

## BƯỚC 3: FIX TỪNG LỖI

Cho mỗi lỗi tìm thấy:
1. Xác định file `.tex` nguồn (từ build/main.log)
2. Sửa file (nới cột, ngắt dòng, đổi kích thước)
3. Rebuild PDF
4. Re-run Bước 2 → verify lỗi đã fix
5. Nếu chưa fix → sửa cách khác → repeat

### Quy tắc fix:
- **Tràn lề:** nới cột bảng / thêm `\allowbreak` / giảm font
- **Chồng chữ:** nới cột / thêm column separator / đổi p{} width
- **Bảng dồn:** tăng cột width hoặc giảm nội dung
- **Trang trắng:** check float placement

## BƯỚC 4: LẶP

```
while (issues > 0):
    fix(issues)
    rebuild()
    issues = analyze()
    print(f"Còn {len(issues)} lỗi")
```

MAX_ITERATIONS = 10. Nếu sau 10 lần vẫn còn lỗi → báo user các lỗi không fix được + lý do.

## BƯỚC 5: MOCKUP THEO FR

Sau khi PDF sạch hình thức, tái cấu trúc mục 3.3:

1. Lấy danh sách 48 FR từ DECIDED list trong `docs/feature-audit-build.py`
2. Với mỗi FR:
   - Tìm ảnh screenshot tương ứng trong `figures/app/`
   - Nếu có → `\includegraphics` + caption "F-XXX-NN: Tên tính năng"
   - Nếu chưa → placeholder box: `\fbox{\parbox...}`
3. Sắp xếp theo phân hệ (Video → Music → News → Games → Dùng chung)
4. Mỗi ảnh 0.28\textwidth, 3 ảnh/hàng
5. Rebuild + verify

## BƯỚC 6: FINAL CHECK

```python
# Kiểm tra tất cả:
# 1. 0 lỗi hình thức (tràn, chồng, dồn, trống)
# 2. PDF build 0 lỗi, 0 undefined
# 3. Mockup section có ảnh theo từng FR
# 4. Overfull log: mọi cái >5pt đã được fix
# 5. Git: chưa commit
```

## TUYỆT ĐỐI KHÔNG

- Không nói "đã fix" mà không verify lại
- Không chỉ fix 1-2 lỗi rồi báo xong
- Không skip bước verify
- Không commit/push
