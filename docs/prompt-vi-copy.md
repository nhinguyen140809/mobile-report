# PROMPT: Chuẩn hoá 100% ngôn ngữ UI của OneSpace (tiếng Việt là ngôn ngữ chính)

> Copy file này vào AI kèm repo `mobile-app` khi cần đồng bộ hoá copy.
> Áp dụng SAU các prompt trước (đã có 5 tab, onboarding, states, mini player).

---

## ROLE

Bạn là **senior Android content designer + Compose developer** phụ trách copy/UI string. Nhiệm vụ: **đồng bộ hoá toàn bộ text hiển thị trên app OneSpace về tiếng Việt**, xóa hết trạng thái trộn Anh–Việt hiện có. **KHÔNG đổi logic, navigation, data model, hay luồng nghiệp vụ** — chỉ đổi chuỗi hiển thị và các anchor test liên quan.

---

## CONTEXT — vì sao app đang trộn ngôn ngữ

1. Catalog demo (tên video, bài hát, bài báo, nhãn nút cũ) sinh từ giai đoạn scaffold bằng tiếng Anh.
2. Các đợt redesign về sau bị ràng buộc "UI copy preserved" nên giữ nguyên phần Anh.
3. Đợt bổ sung full-UX (onboarding, settings, empty/error states) viết theo rule "tiêng Việt" → hai lớp copy khác nhau tồn tại song song.
4. Một số thuật ngữ bị lai trong cùng một màn: nhãn "Data saver" giữa các dòng tiếng Việt, tiêu đề stats "Streak"/"Pet", toast "Đã lưu vào Watchlist", "Best · 2048".

---

## CHÍNH SÁCH NGÔN NGỮ (bắt buộc)

1. **Tiếng Việt là ngôn ngữ giao diện mặc định** cho: nhãn nút, tab phụ đề, menu, dialog, snackbar, toast, contentDescription (TalkBack), empty/error/loading copy, metadata ("phút đọc", "Điểm cao").
2. **Catalog demo (tên bài, tên video, tiêu đề bài báo, artist, studio, mô tả) cũng dịch sang tiếng Việt** — người dùng cuối của OneSpace là người Việt; bài mẫu tiếng Anh làm demo mất tự nhiên.
3. **Giữ nguyên tiếng Anh — whitelist (không dịch):**
   - Tên 5 tab: `Home | Video | Music | News | Games` (đã chốt ở brief IA, chuẩn common-app).
   - Thuật ngữ chuyên môn đã phổ biến: `OTP`, `mp3`, `TTS`, `PIP`, `Data saver → *xin lưu ý: DỊCH thành "Tiết kiệm dữ liệu"*`, `demo` (chữ để chỉ bản demo), `Lo-fi`, `Chill`.
   - Tên riêng: `oneSpace`, `OneSpace Studio`, `2048`, `Tic-Tac-Toe`.
   - Số/thời lượng: `1:00`, `5:40`, `6:12`, `0:24` — không đụng.
   - Tên route/id (`video/watch/{id}`, `v1`, `m1`) và khóa DataStore — **tuyệt đối không đổi**.
4. **Viết hoa & câu cú:** nhãn nút dạng vô-thời ("Lưu bài viết", không "Hãy lưu"), tiêu đề section viết thường; câu hoàn chỉnh có dấu chấm лише khi là câu mô tả.
5. **contentDescription của icon-only buttons phải tiếng Việt** và mang hành động ("Tạm dừng", không "Nút tạm dừng").

---

## BẢNG ÁP DỤNG — copy mapping từng màn

### 1. Catalog demo (data mocks)

| Hiện tại | Thay bằng |
|---|---|
| Video "A little closer to nature" | "Gần với thiên nhiên thêm chút" |
| Video "Saigon, after hours" | "Sài Gòn, sau giờ tan" |
| Video "The art of slowing down" | "Nghệ thuật chậm lại" |
| Video "Steady frames, quiet streets" | "Khung hình êm, phố vắng" |
| Creator "OneSpace Studio" | giữ nguyên (whitelist) |
| Creator "City Stories" | "Chuyện phố" |
| Creator "Slow Living" | "Sống chậm" |
| Track "Morning light" | "Nắng sớm" |
| Track "Somewhere quiet" | "Nơi nào yên tĩnh" |
| Track "Late night thoughts" | "Suy nghĩ đêm muộn" |
| Track "Slow stories" | "Chuyện kể chậm rãi" |
| Artist "Lo-fi Collective" | "Nhóm Lo-fi" |
| Artist "Sunday Radio" | "Đài Chủ nhật" |
| Artist "Chill Station" | "Trạm Chill" |
| Article "A greener city starts with small ideas" | "Thành phố xanh bắt đầu từ ý nhỏ" |
| Article "Technology that makes room for life" | "Công nghệ nhường chỗ cho cuộc sống" |
| Article "Your next weekend escape" | "Chạy trốn cuối tuần kế tiếp" |
| Category "Lifestyle / Technology / Travel" | "Đời sống / Công nghệ / Du lịch" (khớp chip onboarding) |
| "4 min read" | "4 phút đọc" |
| Body các bài báo | viết lại mẫu tiếng Việt 2–3 câu, giữ ý hiện tại |
| Game desc "A little focus. A bigger number." | "Tập trung chút, số lớn hơn." |
| Game desc "A classic break for two." | "Trò cổ điển cho hai người." |
| "Offline sample" (chip nhạc) | "Mẫu ngoại tuyến" |

### 2. Nhãn nút / trạng thái UI

| Hiện tại | Thay bằng |
|---|---|
| "Play" / "Pause" (nút video, transport) | "Phát" / "Tạm dừng" |
| "Float & explore" | "Thu nhỏ & khám phá" |
| "Latest" | "Mới nhất" |
| "Saved (n)" | "Đã lưu (n)" |
| "Save story" | "Lưu bài viết" |
| "Saved ✓" | "Đã lưu ✓" |
| "For you" | "Dành cho bạn" |
| "Downloaded" | "Đã tải" |
| "Pause preview" / "Resume preview" | "Tạm dừng bản demo" / "Chơi bản demo" |
| "Best · 2048" | "Điểm cao · 2048" |
| "Track unavailable" / "Video unavailable" / "Article unavailable" / "Game unavailable" | "Chưa có bài này" / "Chưa có video này" / "Chưa có bài viết này" / "Chưa có game này" |
| Snackbar "Đã lưu vào Watchlist" | "Đã lưu vào Xem sau" |
| "Floating · Demo playing" / "Floating · Paused" | "Đang phát · cửa sổ nổi" / "Tạm dừng · cửa sổ nổi" |
| Label stats "Streak" / "Pet" | "Chuỗi ngày" / "Thú cưng" |
| Settings "Data saver" | "Tiết kiệm dữ liệu" |
| "Watch later/Watchlist" còn sót trong code copy | "Xem sau" |
| "Tiếp tục xem" / "Tiếp tục" / "Đề xuất hôm nay" | giữ nguyên (đã chuẩn) |

### 3. contentDescription (TalkBack)

| Hiện tại | Thay bằng |
|---|---|
| "Back" | "Quay lại" |
| "Play" / "Pause" / "Next" / "Previous" | "Phát" / "Tạm dừng" / "Tiếp theo" / "Bài trước" |
| "Close" | "Đóng" |
| "Expand" | "Mở rộng" |
| "Tài khoản" | giữ nguyên |

### 4. KHÔNG đụng (đã tiếng Việt chuẩn)

Onboarding toàn bộ, empty states, error/offline states, undo snackbar, dialog xung đột C1, Settings còn lại, Home, chips sở thích.

---

## CẬP NHẬT TEST BẮT BUỘC (cùng một commit)

`NavigationSmokeTest` đang assert theo chuỗi — đổi **đồng bộ** theo bảng sau nếu không suite sẽ đỏ:

| Anchor cũ | Anchor mới |
|---|---|
| text "A little closer to nature" (onFirst + await) | "Gần với thiên nhiên thêm chút" |
| text "Float & explore" (2 chỗ) | "Thu nhỏ & khám phá" |
| text "Latest" | "Mới nhất" |
| text "Floating · Demo playing" | "Đang phát · cửa sổ nổi" |
| text "A greener city starts with small ideas" (2 chỗ) | "Thành phố xanh bắt đầu từ ý nhỏ" |
| text "Save story" | "Lưu bài viết" |
| text "Saved ✓" | "Đã lưu ✓" |
| text "Saved (1)" | "Đã lưu (1)" |
| text "Morning light" (2 chỗ) | "Nắng sớm" |
| text "Lo-fi Collective" | "Nhóm Lo-fi" |
| cd "Pause" | "Tạm dừng" |
| cd "Expand" | "Mở rộng" |
| cd "Back" | "Quay lại" |
| cd "Close" (trong @Before resetMedia) | "Đóng" |
| Tab labels "Video"/"Music"/"News"/"Home" trong tapTab | GIỮ NGUYÊN (whitelist) |
| Onboarding texts (Tiếp tục, chips, Bắt đầu, Dùng thử…) | GIỮ NGUYÊN |

Lưu ý mapping test chạy đã được verify: giữ nguyên cấu trúc `awaitText`/`tapTab` đã có, chỉ thay chuỗi.

---

## CONSTRAINTS

1. Chỉ đổi **chuỗi hiển thị + anchor test**. Không sửa: StateFlow logic, SessionPolicy, engine, navigation route, mã phân hệ, Hilt wiring, theme.
2. Không thêm dependency mới, không thêm component mới.
3. Mọi chuỗi viết trực tiếp theo codebase hiện tại (chưa có strings.xml) — giữ pattern inline, ghi chú TODO i18n choPhase sau.
4. Thứ tự thực hiện: (a) data mocks → (b) screens/nút → (c) contentDescription → (d) shell/snackbar → (e) tests → (f) build + full suite.
5. Hạn chế mọi xung đột: nếu một chuỗi nằm trong cả UI lẫn test, đổi CÙNG commit.

---

## ACCEPTANCE / EVALUATION

Sau khi xong, kiểm tra từng câu:

| Kiểm | Cách xác nhận |
|---|---|
| Không còn tiếng Anh ngoài whitelist | Lướt 9 màn (Home/4 tab/Onboarding/Login/Settings/Account) — chỉ thấy tab labels, tên riêng, thuật ngữ whitelist là Anh |
| Metadata thuần Việt | "4 phút đọc", "Điểm cao", "phút xem đến…" |
| TalkBack đọc tiếng Việt | Bật TalkBack trên 1 icon-only: đọc "Phát/Tạm dừng/Quay lại" |
| Test xanh | `:app:connectedDebugAndroidTest` 4/4, chạy 2 lần liên tiếp; unit 15/15 |
| Grep audit | `grep -rE "Pause|Save story|Latest|Float & explore|Watchlist|Data saver|Streak|Pet\"" --include="*.kt" app/src/*/main feature data core` → 0 kết quả (trừ whitelist) |
| Định danh giữ nguyên | build thành công + app mở vào đúng tab lưu lastIndex (TC10 restore vẫn đạt) |

Chấm bằng 4 lens bài học: Component (nhãn = hành động), Flow (copy dẫn bước kế tiếp), Access (TalkBack Việt), State (feedback bằng tiếng Việt).
