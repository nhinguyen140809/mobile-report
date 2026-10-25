# PROMPT: Verify citations trong market-research (mục 1.2) và quality-pillars (mục 1.5)

> Copy prompt này vào Claude/AI. Đi kèm các file .tex cần verify + refs.bib.

---

## ROLE

Bạn là **fact-checker** cho báo cáo học tập. Nhiệm vụ: verify 15 citation keys được sử dụng trong `sections/1-project-overview/market-research.tex` và `sections/1-project-overview/quality-pillars.tex`. Với MỖI citation, xác minh rằng nguồn (URL) thực sự chứa thông tin mà file .tex trích dẫn.

---

## QUY TRÌNH

Bước 1: Đọc `refs.bib` để lấy URL cho từng citation key.
Bước 2: Với mỗi key, truy cập URL bằng WebFetch.
Bước 3: So sánh nội dung nguồn với claim trong .tex.
Bước 4: Phân loại kết quả.

---

## DANH SÁCH CẦN VERIFY

### Section 1.2.2 — Đối thủ trực tiếp (7 sources)

| Key | URL trong refs.bib | Claim cần verify | Câu hỏi verify |
|-----|---|---|---|
| `sggp-mocha2019` | sggp.org.vn/... | "từ cuối năm 2018, Viettel nâng cấp Mocha theo hướng ứng dụng giải trí, phục vụ nghe nhạc, xem phim, đọc tin tức, chơi game" + "tổng hợp từ 100 đầu báo" | Bài SGGP có nói Mocha nâng cấp cuối 2018? Có nhắc "100 đầu báo"? |
| `mocha-googleplay` | play.google.com/... | "Mocha là siêu ứng dụng: gọi điện, nhắn tin, chơi game có thưởng, xem video, phim, livestream, nghe nhạc từ Keeng" | Google Play có liệt kê các tính năng này? |
| `mocha-appstore` | apps.apple.com/... | "thuê bao Viettel được miễn phí data: học sinh/sinh viên không giới hạn, các thuê bao khác 5GB/tháng" | App Store có nói về data miễn phí? |
| `youtube-playables` | (?) | "YouTube Playables đã có mặt tại Việt Nam" | Trang có xác nhận Playables available ở VN? |
| `youtube-premium` | (?) | "phát trong nền / tải về chỉ dành cho YouTube Premium" | Trang có nói các tính năng này yêu cầu Premium? |
| `tiktok-minigames` | (?) | "TikTok có Mini Games và Việt Nam nằm trong danh sách thị trường có tính năng này" | Trang có nói Mini Games + VN? |
| `tiktok-music-shutdown` | (?) | "TikTok đóng cửa TikTok Music từ ngày 28/11/2024" | Bài có nói ngày đóng cửa? |

### Section 1.2.3 — Đối thủ gián tiếp (4 sources)

| Key | Claim cần verify |
|-----|---|
| `zingmp3-appstore` | "chất lượng âm thanh cao, hiển thị lời bài hát dạng karaoke" |
| `spotify-free2025` | "từ tháng 9/2025, tài khoản Spotify miễn phí chọn và phát bài hát bất kỳ" |
| `baomai-appstore` | ✅ **ĐÃ VERIFIED** — Báo Mới "hơn 150+ báo điện tử" (App Store xác nhận) — **KHÔNG cần verify lại** |
| `momo-shopxu` | "người dùng MoMo nhận Xu khi thanh toán hoặc cho Heo Đất ăn, dùng Xu đổi ưu đãi/trang phục" |

### Quality-pillars (5 sources)

| Key | Claim cần verify |
|-----|---|
| `android-vitals` | "ngưỡng Google Play: crash 1.09%, ANR 0.47%" |
| `android-app-size` | "kích thước tải về càng lớn → tỉ lệ gỡ càng tăng" |
| `adjust2026vn` | KHÔNG thể verify (Adjust rate-limit). **Chỉ giữ nếu số liệu có trong bài Tuổi Trẻ thay thế** |
| `nd147-2024` | "Nghị định 147/2024/NĐ-CP về điểm thưởng ảo, không quy đổi tiền" |
| `luat-bvdlcn-2025` | "Luật bảo vệ dữ liệu cá nhân 2025 — đồng ý cá nhân hóa" |

---

## QUY TẮC QUYẾT ĐỊNH

Với mỗi source, trả về kết quả theo format:

```
✅ VERIFIED — [key]: Nguồn có chứa claim. [Trích dẫn 1 câu từ nguồn]
❌ NOT FOUND — [key]: Nguồn KHÔNG đề cập claim này. [Nội dung nguồn thực sự nói gì]
�cíCANNOT ACCESS — [key]: URL không truy cập được (404, rate limit...). Đề xuất: thử URL khác / tìm secondary source
```

**Quy tắc xử lý kết quả:**

1. **✅ VERIFIED** → giữ nguyên citation, không thay đổi gì
2. **❌ NOT FOUND** → tìm source thay thế:
   a. Tìm secondary source (báo chí VN, tech blog) đề cập đúng thông tin
   b. Nếu tìm được → thay cite key + thêm entry refs.bib mới
   c. Nếu KHÔNG tìm được → **BỎ câu/số liệu** và viết lại câu chung chung (không nêu số cụ thể)
3. **⚠️ CANNOT ACCESS** → cố gắng secondary source. Nếu vẫn không được → đánh dấu cần verify bằng tay

---

## OUTPUT FORMAT

Trả về một bảng tóm tắt:

| # | Key | Kết quả | Hành động |
|---|---|---|---|
| 1 | sggp-mocha2019 | ✅/❌/⚠️ | Giữ/Thay/Bỏ |
| ... | ... | ... | ... |
| 15 | luat-bvdlcn-2025 | ✅/❌/⚠️ | ... | 

Sau đó liệt kê những thay đổi cần thực hiện trong .tex và refs.bib.

---

## CONSTRAINTS

1. **KHÔNG bịa đặt** — nếu verify không được, ghi rõ "không xác minh được"
2. Chỉ dùng URLs trong `refs.bib` hoặc secondary sources tìm được qua WebFetch
3. Ghi rõ URL truy cập + ngày truy cập
4. Nếu source chỉ verify được MỘT PHẦN claim, ghi rõ phần nào verify được, phần nào không
5. Không modify file .tex — chỉ REPORT; người đọc quyết định thay đổi
