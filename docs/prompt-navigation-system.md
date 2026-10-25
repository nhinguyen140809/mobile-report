# Prompt: Thiết kế lại hệ thống Back/Điều hướng của OneSpace

> Dùng với 2 skill (load trước khi làm): **agency-ux-architect** (thiết kế hợp đồng điều hướng) và **agency-mobile-app-builder** (thực hiện trên Kotlin/Jetpack Compose).
> Repo app: `/Users/giantkd/StudioProjects/mobile-app` · Repo report: `/Users/giantkd/WINDOWS/BKU/HK261/Mobile/mobile-report`

## Vai trò

Bạn là kỹ sư Android điều phối cả thiết kế UX và cài đặt. Nhiệm vụ duy nhất: đưa hệ thống back của OneSpace về **một quy tắc dự đoán được**, cài thật, verify trên emulator.

## Bối cảnh — triệu chứng lỗi

1. Màn detail có nút ← + tiêu đề nhưng "chả ai biết bấm xong đi đâu".
2. Back nhiều lần bị "bay qua home qua video tùm lum" — không có hệ thống.
3. Nguyên nhân trong code (đã truy vết):
   - Mọi điểm mở nội dung (`openVideo`, `openMusicPlayer`, `openArticle`, `openGame`…) gọi `navController.navigate()` thẳng → detail của phân hệ A nằm trên stack của tab B.
   - `navigateToSection` dùng `saveState/restoreState` → đống màn trộn được lưu lại; bấm tab sau này đáp xuống màn cũ của phân hệ khác.
   - Nút ← chỉ `popBackStack()` theo lịch sử, không theo phân cấp; không có gợi ý đích đến.

## Hợp đồng thiết kế bắt buộc (không tự đổi)

**QUY TẮC DUY NHẤT: back luôn hạ một cấp — detail → feed của phân hệ đó → Home → thoát app.**

1. Mỗi màn detail thuộc về tab chủ nhân của nó (Video/Music/News/Games). Mở nội dung từ ngữ cảnh khác tab (tìm kiếm Home, sheet Xem sau, mini player, thẻ nổi "Đang đọc", hub Playlist ở Hồ sơ) → điều hướng về **tab chủ nhân** với stack sạch `[feed, detail]`, KHÔNG dùng restoreState ở bước này.
2. Trong cùng tab, chuỗi khám phá (feed → detail → artist/playlist…) vẫn đẩy dồn lên như cũ — back đi ngược từng bước, linear.
3. Bấm bottom tab: giữ hành vi chuẩn `saveState/restoreState` (quay lại chỗ cũ trong tab) — nhưng vì stack tab giờ chỉ chứa màn của chính nó, không còn màn "lạ" xuất hiện.
4. Các màn Hồ sơ (Profile/Settings/Wrapped/Nhắc nhở/hub Playlist) thuộc ngữ cảnh Home — back về Home/Hồ sơ như trước.
5. Home root: back hệ thống thoát app (chuẩn Android).

## Phạm vi công việc

1. **Kiểm kê** mọi điểm `navigate` chéo ngữ cảnh trong `OneSpaceAppState` + `AppNavigation` (openVideo, openVideoInPlaylist, openVideoArtist, openVideoPlaylist, openMusicPlayer, openMusicPlaylist, openArticle, openGame, openProfile…). Liệt kê ra bảng trước khi sửa.
2. **Cài đặt**: thêm helper `openInTab(tab, route)` trong `OneSpaceAppState` — `navigate(tab.route) { popUpTo<HomeRoute.Feed> { saveState = true }; launchSingleTop }` rồi `navigate(route) { launchSingleTop }`; chuyển các hàm mở nội dung chéo tab qua helper này. Không đổi `navigateToSection` (bottom tab) và `navigateBack`.
3. **Xây**: `./gradlew :app:assembleDebug verifyArchitecture` phải pass.
4. **Verify trên emulator** bằng bảng test dưới đây — mỗi dòng phải đạt, dùng dump UI để xác nhận màn hiện tại.
5. **Report**: chỉ đụng nếu có chỗ mô tả hành vi back mâu thuẫn với hợp đồng mới; không thêm figure mới. Rebuild PDF + pixel-margin gate.

## Bộ test bắt buộc (đạt hết mới xong)

| # | Luồng thao tác | Kỳ vọng sau khi bấm back |
|---|---|---|
| 1 | Home tìm "chill" → mở video | Back 1: feed Video (không phải Home). Back 2: Home (ô tìm còn nguyên). Back 3: thoát được app |
| 2 | Home mở sheet Xem sau → mở video | Back: feed Video → Home |
| 3 | Mini player nhạc (Home) → mở rộng | Back: feed Music → Home |
| 4 | Thẻ nổi "Đang đọc" → Đọc tiếp | Back: feed News → Home |
| 5 | Hồ sơ → Playlist của tôi → playlist video → mở video | Back: playlist detail → feed Video → Home |
| 6 | Tab Video: feed → video → trang kênh | Back: video → feed Video → Home |
| 7 | Home tìm → mở video → qua tab News → bấm tab Home | Đáp trên Home.Feed, KHÔNG đáp trên video detail cũ |
| 8 | Mọi màn: bấm ← trên top bar | Đúng một cấp theo quy tắc, không nhảy Tab |

## Ràng buộc

- Tiếng Việt trong app đơn giản, trực tiếp; không thêm chữ mới ngoài cần thiết.
- KHÔNG commit — để user duyệt.
- Không tự mở rộng phạm vi (đừng đụng đến behavior chưa được yêu cầu).
- Nếu một dòng test fail: sửa đến khi pass, không bỏ qua dòng nào.

## Đầu ra

- Code thay đổi trong app repo (working tree, chưa commit).
- Bảng kết quả 8/8 test pass.
- Report PDF build sạch (0 lỗi, không tràn lề).
