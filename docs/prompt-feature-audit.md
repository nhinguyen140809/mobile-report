# PROMPT v1 — Tạo file HTML audit: 77 tính năng × mockup × khả thi

> **Cách dùng:** mở session ZCode mới với working directory là repo `/Users/giantkd/WINDOWS/BKU/HK261/Mobile/mobile-report`, dán toàn bộ prompt này. Kèm repo ứng dụng `/Users/giantkd/StudioProjects/mobile-app` (chỉ đọc + chụp ảnh, KHÔNG sửa).
>
> **Changelog:** v1 (2026-10-24) — bản đầu; ground truth ảnh chụp và màn hình app đã được xác minh trực tiếp trong phiên trước.

---

## 0. NGUYÊN TẮC SỐ 1 — KHÔNG THƯƠNG LUỢN

1. **Không được bịa trạng thái.** Mỗi tính năng phải được đối chiếu bằng (a) đọc/grep mã nguồn app thật và (b) ảnh chụp thật. Không đoán theo cảm tính, không suy từ tên tính năng.
2. **Mockup = ảnh chụp từ ứng dụng Android thật** (emulator, `adb screencap`). Tính năng nào có UI mà chưa có ảnh → chụp thêm theo quy trình mục 6. Tuyệt đối không vẽ mockup, không dùng ảnh HTML demo cũ.
3. **Không sửa gì ngoài file HTML** và ảnh chụp bổ sung: không đụng `.tex` của report, không sửa code app, không commit/push.
4. Kết luận "không làm được" phải kèm lý do kỹ thuật cụ thể (bản quyền, cần backend, ML thật, \ldots), không phải "thấy khó".

---

## 1. ROLE

Bạn là kỹ sư kiểm thử đối chiếu sản phẩm (feature auditor) của nhóm OneSpace. Nhiệm vụ: xây một **file HTML tự chứa** (`docs/feature-audit.html`) liệt kê toàn bộ 77 tính năng ứng viên của Phần 2 báo cáo, từng tính năng ghi rõ: đã có mockup trong app chưa (kèm ảnh), khả năng implement thế nào, và đề xuất hành động — để nhóm duyệt trước khi chốt phạm vi làm tiếp.

## 2. BỐI CẢNH — DỮ LIỆU GỐC (bắt buộc đọc trước khi làm)

| Nguồn | Đường dẫn | Lấy gì |
|---|---|---|
| Danh mục 77 tính năng | `sections/2-product-scope/feature-prioritization.tex` (bảng `tab:feature-pool`) | Mã (F-VID-01…F-COM-18), tên, Impact 1–5, Effort 1–5, nhóm (Quick Wins / Major Projects / Fill-ins / Thankless), ghi chú |
| Phạm vi đã chốt | `sections/2-product-scope/mvp-scope.tex` | Bảng MVP (`tab:mvp-scope-full`), danh sách mở rộng, danh sách ngoài phạm vi |
| App thật | `/Users/giantkd/StudioProjects/mobile-app` | Màn hình/composable, module, tính năng đã có |
| Ảnh chụp sẵn (27 ảnh) | `figures/app/*.png` | Ảnh thật đã chụp, mô tả ở mục 3.2 |

Phân bố 77 tính năng: F-VID 19, F-MUS 14, F-NEWS 11, F-GAME 15, F-COM 18.

## 3. GROUND TRUTH ĐÃ XÁC MINH (dùng trực tiếp; phần còn lại phải tự verify)

### 3.1. App thật — màn hình có (tên composable, module `feature/*`)

`SplashScreen`, `OnboardingScreen` (gồm `InfoStep`, `MultitaskStep`, `TopicsStep`), `LoginScreen`, `HomeScreen`, `VideoScreen`, `VideoDetailScreen` (có slot `videoSurface` cho cửa sổ nổi + nút "Thu nhỏ & khám phá"), `MusicScreen`, `NowPlayingScreen`, `NewsScreen`, `ArticleScreen`, `GamesScreen`, `GameScreen`, `AccountScreen`, `SettingsScreen`.
Điều hướng: 5 tab Home/Video/Music/News/Games (`Destinations.kt`), Home là mặc định. Component dùng chung (`core/designsystem`): `FeaturePage`, `SectionTitle`, `ContentCard`, `CatalogContent`, `SkeletonFeed`, `EmptyState`, `ErrorState`.

### 3.2. Bộ ảnh chụp sẵn trong `figures/app/` (đã verify bằng UI dump)

| File | Nội dung |
|---|---|
| onboarding-info/multitask/topics-light | 3 bước onboarding (giới thiệu, đa nhiệm, chọn ≥3 chủ đề) |
| login-light, guest-sheet-light | Đăng nhập (email + OTP demo + Google + dùng thử); bottom sheet xác nhận guest mode |
| home-light / home-dark / home-pip-light | Home (``Tiếp tục'' + ``Đề xuất hôm nay'': 1 video + 1 bài hát + 1 bài tin); bản có cửa sổ nổi video |
| video-feed-light, video-player-light | Feed video theo danh mục; trình phát (tiến trình, tua, nút thu nhỏ, ``Liên quan'') |
| video-offline-light | Trạng thái mất mạng + nút ``Thử lại'' |
| news-feed-light, news-pip-light, news-empty-light | Feed tin (chip ``Mới nhất''/``Đã lưu''); bản có cửa sổ nổi; trạng thái rỗng ``Chưa lưu bài nào'' + CTA |
| article-light, article-dark, article-music-dock-light | Trình đọc bài (chuyên mục, ``Lưu bài viết''); bản có dock nhạc đang phát |
| music-light, now-playing-light/dark | Thư viện nhạc (``Đã tải'', ``Dành cho bạn''); trình phát đầy đủ (Bài trước/Tạm dừng/Tiếp theo) |
| games-light, game-2048-light/dark | Hub game (2048 + Tic-Tac-Toe kèm ``Điểm cao''); màn chơi 2048 |
| account-light | Chế độ Khách: Điểm, Chuỗi ngày, Thú cưng (Trứng), Tùy chỉnh, ``Đăng nhập để giữ tiến độ'' |
| settings-light | Giao diện Sáng/Tối/Hệ thống, Ngôn ngữ, Tiết kiệm dữ liệu (720p), Nhắc nhiệm vụ, Mô phỏng mất mạng |
| c1-audio-conflict-light | **Popup xung đột C1 thật**: ``Tắt tiếng video, phát nhạc / Dừng video, phát nhạc / Chỉ giữ video'' + Bỏ qua |

### 3.3. Đã xác minh CÓ trong app

Trình phát video + PIP cửa sổ nổi (Mở rộng/Tạm dừng/Đóng); dock mini player xuyên suốt (kể cả trong trình đọc bài và trên tab Games); popup xung đột C1 với luật nhớ theo cặp (`SessionPolicy.resolveMusicStart`, enum `MUTE_VIDEO/PAUSE_VIDEO/KEEP_VIDEO`); lưu bài + danh sách đã lưu; trạng thái offline/empty/error có CTA; chế độ khách + sheet xác nhận; cài đặt theme/ngôn ngữ/data saver; thống kê Điểm/Chuỗi ngày/Thú cưng (hiển thị); 2048 + Tic-Tac-Toe; ``Tiếp tục'' (video xem dở, `ViewingSessionRepository`); khôi phục phiên (`SessionCoordinator`, TC05/TC09/TC10); engine media dùng chung ExoPlayer (`MediaPlaybackCoordinator`).

### 3.4. Đã xác minh CHƯA có trong app

TTS nghe tin (F-NEWS-05), quiz từ bài báo / quiz tin tức (F-NEWS-10, F-GAME-03), tìm kiếm (mọi dạng), phát nhạc nền ngoài app (không có foreground service~--~F-MUS-03), haptic, karaoke (F-GAME-04), wrapped (F-COM-10), notification thật. Danh sách này là khởi đầu~--~các tính năng còn lại tự verify theo mục 4.

## 4. QUY TRÌNH AUDIT TỪNG TÍNH NĂNG (làm đủ 77 cái, không bỏ sót)

Với MỖI dòng trong bảng `tab:feature-pool`:

1. **Grep app repo** theo từ khoá liên quan (tên màn hình, chữ hiển thị tiếng Việt trong code, tên module \ldots). Ví dụ F-NEWS-03 → grep ``Lưu bài viết'', ``bookmark''; F-VID-10 → grep ``trích'', ``extract'', ``mp3''.
2. **Đối chiếu ảnh**: tính năng có UI thì ảnh nào trong mục 3.2 minh hoạ được? Nếu không có ảnh nào minh hoạ được nhưng UI tồn tại → đưa vào hàng chờ chụp ảnh (mục 6).
3. **Phân loại** theo cây quyết định ở mục 5, ghi bằng chứng: file code (đường dẫn + dòng), tên composable, và/hoặc tên file ảnh.
4. **So với quyết định đã chốt** trong mvp-scope: tính năng trong bảng MVP? trong danh sách mở rộng? trong ngoài phạm vi? hay không nằm trong cả ba (orphan)? Đề xuất của audit không được mâu thuẫn với quyết định đã chốt; nếu bạn thấy nên khác đi → đánh dấu ``⚠ lệch report'' kèm lý do, để người duyệt quyết.

## 5. CÂY QUYẾT ĐỊNH PHÂN LOẠI

**Trạng thái mockup** (một giá trị):
- `done` — **Đã có mockup**: UI đầy đủ cho tính năng này tồn tại trong app, kèm ảnh chụp (dùng ảnh có hoặc chụp thêm).
- `partial` — **Mockup một phần**: nền tảng UI có (vd feed, dock) nhưng chi tiết riêng của tính năng chưa có (vd chỉ có feed chưa có filter). Ghi rõ phần nào có, phần nào thiếu.
- `none` — **Chưa có mockup**: không tìm thấy UI liên quan.

**Khả thi** (một giá trị):
- `easy` — **Làm được**: dựng được bằng stack sẵn có (Compose + Material 3 + Media3 + Room + DataStore), Effort ≤ 3.
- `hard` — **Khó nhưng làm được**: Effort 4–5 hoặc cần thêm engine/API ngoài (TTS on-device, foreground service, pitch detection…), có đường đi kỹ thuật rõ.
- `infeasible` — **Không khả thi trong phạm vi môn học**: vướng bản quyền (F-MUS-14 lời bài hát), cần ML thật (F-VID-19), cần backend đồng bộ/kiểm duyệt (F-MUS-13, F-VID-13), karaoke chấm điểm (F-GAME-4) — nhóm này thường trùng nhóm Thankless đã ghi trong report.

**Đề xuất** (một giá trị):
- `giữ-mvp` — đã trong bảng MVP, có/không mockup đều làm tiếp.
- `làm-tiếp` — chưa mockup nhưng `easy`/`hard` + nằm trong MVP hoặc mở rộng.
- `chuyển-v2` — khả thi nhưng ngoài MVP (khớp danh sách mở rộng).
- `bỏ` — `infeasible` (đối chiếu nhóm Thankless của report; nếu report chưa phân loại thì đề xuất kèm ⚠).

Quy tắc ràng buộc: `none` + `infeasible` → chỉ được đề xuất `bỏ`; tính năng trong bảng MVP không bao giờ được đề xuất `bỏ`.

## 6. CHỤP ẢNH BỔ SUNG (cho tính năng có UI nhưng chưa có ảnh)

```bash
export PATH="$HOME/Library/Android/sdk/platform-tools:$PATH"
cd /Users/giantkd/StudioProjects/mobile-app && ./gradlew :app:assembleDebug
adb install -r app/build/outputs/apk/debug/app-debug.apk   # emulator-5554 thường đang chạy; adb devices để kiểm
adb shell am start -n com.example.onespace/.MainActivity
adb exec-out screencap -p > /Users/giantkd/WINDOWS/BKU/HK261/Mobile/mobile-report/figures/app/<ten>-light.png
```

- Đặt tên kebab-case trùng phong cách hiện có (`now-playing-light.png`).
- Điều hướng bằng `adb shell input tap X Y`: bottom nav — Home x≈100, Video x≈321, Music x≈540, News x≈760, Games x≈980, y≈2298; Tài khoản = (1006, 226) trên Home; đọc UI hiện trạng bằng `adb shell uiautomator dump /sdcard/ui.xml && adb pull /sdcard/ui.xml /tmp/ui.xml` rồi grep text/bounds để lấy toạ độ bấm (đừng bấm mù).
- Màn cần chụp thêm (dự kiến): watchlist/lịch sử video, kho nhạc cá nhân ``Đã tải'', Tic-Tac-Toe đang chơi, hồ sơ có khung avatar (nếu có), màn nhiệm vụ/streak (nếu có)… — đúng những gì audit phát hiện là có UI mà thiếu ảnh.
- Nếu emulator không chạy nổi: dừng, dùng ảnh có sẵn, đánh dấu ``chưa chụp được'' trung thực — không thay bằng ảnh vẽ.

## 7. SPEC FILE HTML — `docs/feature-audit.html`

**Tự chứa hoàn toàn (một file duy nhất):** nhúng ảnh dạng base64, thu nhỏ về chiều rộng ~360px, nén JPEG quality ~70 (Python + Pillow) để file tổng dưới ~4MB. Mở bằng trình duyệt là chạy, không cần server.

**Giao diện tiếng Việt, chuẩn như một công cụ nội bộ xịn** (theo đúng quality bar của nhóm: font tiếng Việt chuẩn — dùng ``Be Vietnam Pro'' hoặc system stack + `lang="vi"`; icon-first; không màu mè rẻ tiền). Bố cục:

1. **Header:** tên ``OneSpace — Audit tính năng × mockup × khả thi'', ngày lập, số liệu tổng: `77 tính năng | X đã có mockup | Y làm được | Z đề xuất bỏ`.
2. **Dải lọc (filter chip, click được):** theo phân hệ (Tất cả / A-Video / B-Music / C-News / D-Games / Dùng chung), theo trạng thái mockup (done/partial/none), theo khả thi (easy/hard/infeasible), theo đề xuất. Lọc bằng JS thuần, không framework.
3. **Bảng chính** (mỗi tính năng một thẻ hoặc một hàng, responsive):
   - Mã + tên tính năng (nguyên văn từ report)
   - Impact / Effort / nhóm I×E
   - Trạng thái MVP (badge: MVP / Mở rộng / Ngoài phạm vi / ⚠ không nằm trong report)
   - **Trạng thái mockup** (badge màu: xanh=done, vàng=partial, xám=none) + **ảnh thumbnail** (khi có; click mở lightbox đơn giản xem ảnh lớn) + tên màn hình/composable làm bằng chứng
   - **Khả thi** (badge: dễ/khó/không khả thi) + lý do một dòng
   - **Đề xuất** (badge) + ghi chú
   - Bằng chứng code: đường dẫn file (đường dẫn + số dòng nếu được)
4. **Footer:** chú thích nguồn (feature-prioritization.tex, mvp-scope.tex, app repo @ commit hiện tại — lấy `git -C /Users/giantkd/StudioProjects/mobile-app rev-parse --short HEAD`).

**Dữ liệu nhúng trong một biến JS** (`const FEATURES = [...]`), sinh ra bằng Python từ việc audit (viết script Python build file HTML để tái tạo được sau này — lưu script cạnh file HTML: `docs/feature-audit-build.py`).

## 8. RÀNG BUỘC VIẾT & KIỂM CHỨNG

- Toàn bộ text tiếng Việt; thuật ngữ kỹ thuật giữ tiếng Anh. Đây là công cụ nội bộ duyệt phạm vi~--~viết thoáng, thẳng, không văn phong học thuật.
- **Acceptance check (chạy trước khi báo xong):**

| # | Kiểm tra | Mong muốn |
|---|---|---|
| TC1 | Số tính năng trong HTML | đúng 77, khớp từng dòng `tab:feature-pool` |
| TC2 | Chọn ngẫu nhiên 5 tính năng `done` | mỗi cái có ảnh base64 hiển thị được (mở HTML kiểm tra không có ảnh vỡ) |
| TC3 | Chọn ngẫu nhiên 5 tính năng ghi trạng thái | đối chiếu lại grep/code app → kết luận giống nhau |
| TC4 | Tính năng MVP đề xuất `bỏ` | phải bằng 0 |
| TC5 | Mọi tính năng `infeasible` | có lý do kỹ thuật cụ thể, không phải cảm tính |
| TC6 | File HTML | mở trực tiếp bằng browser không lỗi console, tổng dung lượng < 4MB |
| TC7 | Git | `git status` chỉ thêm file HTML mới + ảnh mới trong `figures/app/` (+ script build), không có commit |

## 9. TUYỆT ĐỐI KHÔNG

- Không sửa `.tex`, không sửa code app, không commit/push.
- Không bịa trạng thái/ảnh; không dùng ảnh demo HTML cũ; không chèn ảnh placeholder khi không có ảnh thật.
- Không đổi quyết định đã chốt trong report (MVP/mở rộng/ngoài phạm vi)~--~chỉ đánh dấu ⚠ khi thấy lệch.
- Không dùng framework build (React/Vue…): HTML + CSS + JS thuần một file.

## 10. KNOWN LIMITATIONS

1. **Emulator không chạy được** → chỉ dùng 27 ảnh có sẵn, tính năng thiếu ảnh ghi ``có UI, chưa chụp được''~--~báo user, không bịa.
2. **Trạng thái `partial` mang tính phán đoán của auditor** — ghi rõ phần có/thiếu để người duyệt tự cân nhắc lại.
3. Điểm Effort/Impact lấy nguyên từ report; nếu auditor thấy sai thì ghi ⚠ ở ghi chú, không tự sửa số trong HTML.
