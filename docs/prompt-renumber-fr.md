# PROMPT — Dồn số thứ tự F-... liền mạch + audit mockup theo FR

> **Cách dùng:** session ZCode mới, wd = repo `mobile-report`. Tag `@agency-senior-developer`.
> **Lỗi phải tránh:** thay thế chuỗi nhiều lượt gây đè số (F-VID-14→12 rồi 12→10). Chỉ dùng MỘT lượt duy nhất bằng regex callback.

---

## BỐI CẢNH

Báo cáo liệt kê FR theo mã `F-<PHÂN HỆ>-<SỐ>`. Vì đã bỏ dần một số FR, dãy số bị thưa:
mỗi phân hệ phải là dãy liền `01..N` không gap. Số FR cũ vẫn nằm khắp 9 file .tex
(bảng ưu tiên, user story, MVP scope, caption mockup, heuristic, IA, personas) —
và KHÔNG được sửa code app hay docs/ (audit HTML, decisions.md) vì đó là tài liệu làm việc.

## BẢNG ÁNH XẠ (duy nhất, áp một lượt cho MỌI file trong `sections/`)

| Phân hệ | Giữ nguyên | Đổi thành |
|---|---|---|
| F-VID | 01–11 | 14→12, 15→13, 17→14, 18→15 |
| F-MUS | 01–12 (liền mạch) | không đổi |
| F-NEWS | 01–06 | 09→07, 10→08, 11→09, 12→10 |
| F-GAME | 01–03 | 05→04, 06→05, 07→06, 08→07, 09→08, 10→09, 11→10, 12→11, 13→12, 14→13, 15→14 |
| F-COM | 01–18 (liền mạch) | không đổi |

Cả ba nhóm trên sau khi dồn: F-VID 01–15, F-MUS 01–12, F-NEWS 01–10, F-GAME 01–14, F-COM 01–18.

## CÁCH THAY (bắt buộc)

1. Duyệt `sections/**/*.tex` bằng MỘT lượt `re.sub` với hàm callback tra bảng trên.
   Không được thay theo kiểu chuỗi-đến-chuỗi nhiều lần.
2. Sau khi thay, chạy lại kiểm kê: mỗi prefix phải cho dãy `01..N` liền, không sót số cũ
   (so `grep -rhoE 'F-(VID|MUS|NEWS|GAME|COM)-[0-9]+' sections/ | sort -u`).
3. Tổng số LẦN nhắc FR trước/sau phải bằng nhau (chỉ đổi mã, không thêm mất chỗ nào).

## AUDIT MOCKUP (đi qua TỪNG FR một)

Với danh sách FR thuộc MVP (trong `sections/2-product-scope/mvp-scope.tex`), từng FR một:

1. FR có được nhắc trong caption nào ở `sections/3-ui-ux-design/wireframes-prototypes.tex` không?
2. Caption đó có mô tả đúng hành vi của FR (so với dòng tương ứng trong bảng
   `feature-prioritization.tex`) không? Sai lệch → sửa caption, không bịa hành vi.
3. FR trong MVP mà KHÔNG có mockup → phải bổ sung: chụp màn hình thật từ app
   (emulator đang chạy bản build mới nhất), thêm block `\begin{figure}[H]` cùng vị trí
   phân hệ tương ứng, caption nêu FR mới. KHÔNG dùng ảnh cũ sai nội dung.
4. Mỗi ảnh trong `figures/app/` phải được ít nhất một caption dùng đến; ảnh mồ côi → xoá.

## CỔNG CHẤT LƯỢNG TRƯỚC KHI XONG

- `python3 scripts/build.py` build sạch, không "File not found" trong `build/main.log`
  (trừ 2 dòng info ieee.dbx / biblatex-dm.cfg vốn có sẵn).
- Kiểm kê lại: 5 prefix đều `01..N` liền mạch, không lẻ số.
- Extract text PDF (`pymupdf`) phải chứa mã FR mới ở các caption chính; dò khoảng trắng
  dính do kerning bằng cách strip whitespace trước khi so.
- Pixel-margin gate 117+ trang: chỉ cho phép 2 flag đã biết (trang bìa full-bleed,
  khung lstlisting ~1mm) — không thêm flag mới.
- KHÔNG commit. User duyệt rồi mới commit.

## VÍ DỤ KIỂM TRA BIÊN

- "Rắn săn mồi (F-GAME-13)" → phải thành "F-GAME-12" sau khi dồn, và caption Rắn vẫn nói về Snake.
- "F-VID-17 tốc độ phát" → thành "F-VID-14" — tra bảng ưu tiên dòng Tốc độ phát vẫn là đúng video đó.
- Không được để xuất hiện cả "F-NEWS-09" và "F-NEWS-07" trỏ cùng một tính năng
  sau khi đổi (kiểm tra bằng grep từng cặp cũ→mới).
