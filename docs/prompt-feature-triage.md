# PROMPT v1 — Phân loại 3 lớp cho bảng tính năng: XOÁ / v2 / v1

> **Cách dùng:** mở session ZCode mới với working directory là repo `/Users/giantkd/WINDOWS/BKU/HK261/Mobile/mobile-report`, dán toàn bộ prompt này.
>
> **Changelog:** v1 (2026-10-24) — bản đầu; kết quả audit verify ngày 24/10 được nhúng sẵn làm ground truth (file `docs/feature-audit.html` có đầy đủ bằng chứng từng tính năng).

---

## 0. NGUYÊN TẮC SỐ 1 — KHÔNG THƯƠNG LUỢN

1. **Mỗi tính năng trong bảng 77 ứng viên phải rơi vào đúng một trong ba lớp, không ngoại lệ, không lưỡng lự:**
   - **XOÁ** — thật sự quá vô lý/không triển khai thực tế được trong phạm vi môn học → xoá khỏi report và **dọn mọi dấu vết ở mọi nơi** (danh sách xoá và bản đồ dọn ở mục 3). **Xoá không cần hỏi lại user.**
   - **v1** — nằm trong bảng MVP hiện tại (`tab:mvp-scope-full`) → được nêu đích danh trong MVP.
   - **v2** — khả thi nhưng chưa có trong MVP → ghi rõ ``version 2, version 1 hiện tại chưa có''.
2. Sau khi phân loại, **không còn tính năng nào "không rõ số phận"** (hết trạng thái orphan — 25 tính năng hiện không nằm trong bất kỳ danh sách nào của report đều phải được gán v1/v2).
3. **Đếm lại mọi con số:** xoá 6 tính năng thì bảng còn 71; mọi chỗ ghi "77" trong report phải cập nhật theo.
4. Xoá phải **sạch**: grep mã tính năng bị xoá (vd `F-GAME-04`) trên toàn bộ `sections/` phải trả về 0 kết quả.
5. Không commit/push; build kiểm chứng trước khi báo xong.

## 1. ROLE

Bạn là biên tập viên phạm vi sản phẩm của nhóm OneSpace. Nhiệm vụ: dọn bảng tính năng của báo cáo CO3043 thành ba lớp rạch ròi — xoá cái không làm được, gắn nhãn v2 cái khả thi nhưng để sau, giữ nguyên cái trong MVP — và bảo đảm toàn bộ report nhất quán sau khi dọn.

## 2. GROUND TRUTH ĐÃ XÁC MINH (ngày 24/10, nguồn: audit `docs/feature-audit.html`)

### 2.1. Danh sách XOÁ (6 tính năng, đã verify là không khả thi kèm lý do kỹ thuật)

| Mã | Tính năng | Lý do xoá |
|---|---|---|
| F-VID-13 | Bình luận video | Cần backend + kiểm duyệt nội dung — ngoài phạm vi môn học |
| F-VID-19 | Tự động sinh quiz AI từ video | Cần transcript + ML sinh câu hỏi; rủi ro câu hỏi sai |
| F-MUS-13 | Đồng bộ vị trí phát đa thiết bị | Cần backend đồng bộ thật |
| F-MUS-14 | Lời bài hát (lyrics) | Bản quyền phức tạp nhất danh mục |
| F-GAME-04 | Karaoke chấm điểm giọng hát | Pitch detection dễ làm sai trải nghiệm nhất |
| F-NEWS-08 | Tóm tắt AI một đoạn | Cần AI tóm tắt thật; với catalog tự dựng giá trị thấp |

Đây là đúng 6 tính năng bị audit đánh giá `infeasible`. **Không xoá thêm cái nào khác** — các tính năng còn lại (kể cả Equalizer F-MUS-11, Rhythm F-GAME-05, Tải offline F-VID-07/F-MUS-12) đều khả thi ở mức "khó nhưng làm được" → giữ và gán **v2**.

### 2.2. Phân bố scope hiện tại (đối chiếu `tab:mvp-scope-full` + 2 danh sách của mục 2.5)

- MVP: 38 tính năng → lớp **v1**.
- Mở rộng sau MVP: 6 (F-MUS-03, F-MUS-09, F-GAME-07, F-GAME-08, F-COM-10, F-COM-11) → lớp **v2**.
- Ngoài phạm vi v1: 8 — sau khi bỏ 4 cái đã xoá (F-MUS-14, F-VID-13, F-GAME-04, F-MUS-13), còn 4 (F-VID-07, F-MUS-12, F-MUS-11, F-GAME-05) → lớp **v2**.
- Orphan (không nằm trong bất kỳ danh sách nào): 25 → tất cả gán **v2** (Fill-ins khả thi, làm khi dư thời gian / giai đoạn sau).

### 2.3. Vấn đề Quick Wins (quan trọng — phải tổng hợp và nêu cho user)

Theo logic ma trận Impact $\times$ Effort, **mọi Quick Wins phải nằm trong v1** (làm trước khi đụng Major Projects). Hiện có **5 Quick Wins KHÔNG nằm trong bảng MVP**:

| Mã | Tính năng | Nhóm | Hiện trạng |
|---|---|---|---|
| F-VID-03 | Tìm kiếm video | Quick Wins | ngoài MVP, chưa có trong app |
| F-VID-18 | Thẻ game cuối video | Quick Wins [W4] | ngoài MVP (US-VID-07 đã hạ Could) |
| F-MUS-06 | Tìm kiếm nhạc | Quick Wins | ngoài MVP, chưa có trong app |
| F-NEWS-06 | Sắp xếp mới nhất/phổ biến | Quick Wins | ngoài MVP; app đã có chip ``Mới nhất'' |
| F-COM-12 | Nhắc nhiệm vụ/streak | Quick Wins | ngoài MVP; app có toggle trong Settings |

Xử lý: **giữ 5 cái này ở v2** trong lần dọn này (không tự ý phình MVP), nhưng trong báo cáo cuối phải có mục riêng nêu vấn đề này kèm hai phương án cho user chọn: (a) kéo vào v1 vì "Quick Wins phải làm hết", hoặc (b) hạ nhóm của chúng (đổi ghi chú nhóm trong bảng, vì search từng phân hệ sẽ gộp vào F-COM-11 v2; F-NEWS-06/F-COM-12 giá trị thấp hơn các QW còn lại). Không tự quyết.

## 3. BẢN ĐỒ DỌN DẤU VẾT KHI XOÁ (6 mã ở mục 2.1)

Grep từng mã bị xoá trên `sections/` để tìm mọi nơi, nhưng tối thiểu các chỗ sau (đã khảo sát sẵn):

1. `sections/2-product-scope/feature-prioritization.tex`:
   - 6 dòng trong bảng `tab:feature-pool`;
   - danh sách tổng hợp cuối bảng: bỏ F-VID-13, F-VID-19 khỏi hàng Thankless; bỏ F-MUS-13, F-MUS-14 khỏi hàng Thankless; bỏ F-GAME-04 khỏi hàng Major Projects; bỏ F-NEWS-08 khỏi hàng Major (cân nhắc);
   - dòng chữ ``Trong 77 ứng viên'' → đổi thành số mới (71);
   - ghi chú của F-VID-19 nhắc ``cùng nhóm rủi ro với karaoke F-GAME-04'' → cả hai bị xoá nên câu đó biến mất luôn;
   - ghi chú của F-GAME-05 ``Trùng trải nghiệm với karaoke nhưng kém khác biệt'' → **viết lại lý do** không dựa vào karaoke nữa (vd ``trùng trải nghiệm theo nhịp nhạc nhưng kém khác biệt'') vì karaoke đã bị xoá.
2. `sections/2-product-scope/mvp-scope.tex` — danh sách ``Ngoài phạm vi ở giai đoạn đầu'': bỏ 4 mục bị xoá (F-MUS-14, F-VID-13 kèm ``feed theo dõi'', F-GAME-04, F-MUS-13); giữ và chuyển 4 mục còn lại (F-VID-07, F-MUS-12, F-MUS-11, F-GAME-05) sang trình bày v2.
3. `sections/2-product-scope/user-stories.tex`: **US-GAME-06 (karaoke, F-GAME-04)** — xoá nguyên dòng story (đây là story duy nhất của 6 mã bị xoá); kiểm tra lại đoạn mở đầu và bảng `tab:usp-trace` không tham chiếu tới nó.
4. Phần 3 (`sections/3-ui-ux-design/`): grep 6 mã — dự kiến không tham chiếu trực tiếp, nhưng phải kiểm chứng; nếu có thì viết lại câu.
5. `docs/feature-audit-build.py`: bỏ 6 entry trong dict AUDIT, đổi `assert len(feats) == 77` thành số mới, rồi **chạy lại để tái sinh `docs/feature-audit.html`** (cập nhật cả bản copy trong thư mục visualizations nếu có).

## 4. CÁCH GHI v1/v2 TRONG REPORT

1. **Bảng tính năng** (`tab:feature-pool`): thêm cột **``Phiên bản''** (hẹp ~1cm) sau cột ``Nhóm đề xuất'', mỗi dòng ghi `v1` hoặc `v2` (không in đậm). Điều chỉnh bớt độ rộng cột ``Ghi chú'' để bảng vẫn vừa \textwidth (tránh overfull).
2. **Mục 2.5 (mvp-scope):**
   - Bảng MVP giữ nguyên (đây chính là v1);
   - Đổi tiêu đề ``Mục tiêu mở rộng cho giai đoạn sau MVP'' thành cơ cấu rõ hơn: đây là **danh sách v2** — gộp 6 mục mở rộng hiện có + các tính năng còn lại gán v2, nhóm lại theo phân hệ cho gọn (không cần liệt kê đủ 33 dòng, liệt kê theo cụm mã: ``các tính năng Fill-ins còn lại (F-VID-03, 09, 11, \ldots)'');
   - Danh sách ``Ngoài phạm vi'' sau khi bỏ 4 mục xoá: chuyển thành ``chậm lại ở v2 vì bản quyền/công sức'' (không còn khái niệm ``loại hẳn'' — cái bị loại hẳn đã bị xoá khỏi report).
3. Đoạn văn nối sau bảng `tab:feature-pool` (nơi giải thích nhóm I×E): bổ sung 2--3 câu giải thích cột Phiên bản: ``v1 là phạm vi MVP đã chốt ở mục 2.5; v2 là mọi tính năng khả thi còn lại, làm sau khi MVP hoàn tất và ổn định'' — khớp chữ với mvp-scope.

## 5. QUY TRÌNH (thứ tự bắt buộc)

1. Grep 6 mã bị xoá trên toàn bộ `sections/` → lập danh sách mọi vị trí xuất hiện (đối chiếu với mục 3, bổ sung chỗ thiếu).
2. Xoá 6 tính năng + dọn từng vị trí theo mục 3.
3. Thêm cột Phiên bản vào bảng tính năng, gán v1/v2 theo ground truth mục 2.2.
4. Cập nhật mvp-scope theo mục 4.2.
5. Cập nhật `docs/feature-audit-build.py` (assert mới, bỏ 6 entry AUDIT) → chạy lại sinh file HTML mới, copy đè bản visualizations.
6. Build PDF: `PATH="$HOME/Library/TinyTeX/bin/universal-darwin:$PATH" python3 scripts/build.py` — 0 lỗi, 0 undefined ref.
7. Chạy acceptance check (mục 7) rồi báo cáo.

## 6. RÀNG BUỘC VIẾT

- Giữ nguyên văn phong học thuật tiếng Việt sẵn có; không thêm ngôn ngữ nội bộ.
- Các con số đổi phải khớp ở **mọi** chỗ (71 ở bảng, ở câu chữ ``Trong 71 ứng viên'', ở audit script).
- Không đụng Phần 1, 3, 4 trừ chỗ grep phát hiện tham chiếu tới mã bị xoá.

## 7. ACCEPTANCE CHECK (chạy trước khi báo xong)

| # | Kiểm tra | Mong muốn |
|---|---|---|
| TC1 | `grep -rn "F-VID-13\|F-VID-19\|F-MUS-13\|F-MUS-14\|F-GAME-04\|F-NEWS-08" sections/` | **0 kết quả** |
| TC2 | `grep -rn "US-GAME-06" sections/` | 0 kết quả |
| TC3 | Số dòng bảng `tab:feature-pool` | đúng 71, mỗi dòng có v1 hoặc v2 ở cột Phiên bản |
| TC4 | `grep -rn "77" sections/2-product-scope/feature-prioritization.tex` | không còn "77 ứng viên" (đổi 71) |
| TC5 | Mỗi tính năng v1 (38) đều có trong bảng `tab:mvp-scope-full`; mỗi tính năng v2 đều KHÔNG có trong bảng đó | khớp 1--1 |
| TC6 | Bảng tính năng không bị tràn lề (overfull >5pt ở khối bảng) | sạch |
| TC7 | Build PDF | 0 lỗi `!`, 0 undefined reference, số trang ổn định (chênh lệch nhỏ) |
| TC8 | `docs/feature-audit.html` tái sinh | mở được, đủ 71 thẻ, không còn 6 mã bị xoá |
| TC9 | Git | chỉ file sửa trong working tree, không commit |

## 8. BÁO CÁO CUỐI (bắt buộc có đủ)

1. Danh sách 6 mã đã xoá + mỗi mã đã dọn ở những file nào.
2. Thống kê: 71 tính năng = X v1 + Y v2.
3. **Mục "Vấn đề Quick Wins"**: bảng 5 Quick Wins chưa vào v1 + 2 phương án xử lý, chờ user quyết (mục 2.3).
4. Kết quả build + acceptance check.

## 9. TUYỆT ĐỐI KHÔNG

- Không xoá thêm tính năng ngoài 6 mã đã verify (kể cả khi "thấy khó" — khó $\neq$ vô lý).
- Không đổi điểm I/E, không đổi nhóm của tính năng nào chưa bị yêu cầu (trừ câu ghi chú F-GAME-05 phải viết lại vì karaoke bị xoá).
- Không tự quyết việc kéo Quick Wins vào v1 — chỉ tổng hợp và nêu vấn đề.
- Không commit/push; không sửa app Android.

## 10. KNOWN LIMITATIONS

1. Nếu grep phát hiện 6 mã bị xoá xuất hiện ở file khác ngoài bản đồ mục 3 (vd Phần 3/4): xoá/viết lại chỗ đó và ghi nhận vào báo cáo.
2. Danh sách v2 trong mvp-scope được gộp theo cụm cho gọn; nếu user muốn liệt kê đủ 33 dòng từng tính năng thì sẽ chỉnh ở vòng sau.
