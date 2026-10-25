# PROMPT v1 — Implement Phần 3: Thiết kế UI/UX (báo cáo OneSpace)

> **Cách dùng:** mở session ZCode mới với working directory là repo báo cáo `/Users/giantkd/WINDOWS/BKU/HK261/Mobile/mobile-report`, dán toàn bộ prompt này. Kèm theo là repo ứng dụng thật tại `/Users/giantkd/StudioProjects/mobile-app` (chỉ đọc + chụp ảnh, KHÔNG sửa).
>
> **Changelog:** v1 (2026-10-24) — bản đầu, ground truth đã xác minh trực tiếp từ code app và report hiện tại.

---

## 0. NGUYÊN TẮC SỐ 1 — KHÔNG THƯƠNG LUỢNG

1. **Ảnh phải là ảnh chụp thật từ ứng dụng Android** (emulator/AVD + `adb screencap`). Tuyệt đối không vẽ, không dùng ảnh mockup HTML, không dùng ảnh generate.
2. **Diagram phải khớp 100% định nghĩa đã chốt trong báo cáo**: ma trận case C1–C9 ở `sections/2-product-scope/mvp-scope.tex` (bảng `tab:switch-matrix`), kịch bản first-run cùng file, user stories ở `sections/2-product-scope/user-stories.tex`, ngưỡng chất lượng ở `sections/1-project-overview/quality-pillars.tex` (bảng `tab:quality-criteria`). Khi có mâu thuẫn giữa `docs/flows.md` và `.tex` trong báo cáo thì **bên `.tex` luôn đúng** (xem mục 3.4 các sai lệch đã biết).
3. **Không bịa số liệu.** Mọi con số trong Phần 3 phải (a) khớp nguyên văn một nguồn đã có trong báo cáo, hoặc (b) tính lại được từ code thật (vd: tỉ lệ tương phản từ hex trong `Theme.kt`), hoặc (c) không có thì ghi trung thực "dự kiến/kế hoạch". Kết quả usability test/chỉnh sửa heuristic chưa làm thì ghi trạng thái "chưa thực hiện" — không bịa ra kết quả.
4. **Không commit, không push.** Để nguyên working tree cho user duyệt. Build local để render kiểm chứng.
5. **Không sửa app Android.** Chỉ build để chạy và chụp. Sửa app là task riêng sau này.

---

## 1. ROLE

Bạn là kỹ sư viết tài liệu kỹ thuật, đồng thời là người thực hiện thiết kế UI/UX của nhóm phát triển OneSpace (ứng dụng giải trí 4-trong-1: Video + Music + News + Minigames, Android native Kotlin + Jetpack Compose + Material 3). Nhiệm vụ: viết hoàn chỉnh **Phần 3 — Thiết kế UI/UX** cho báo cáo môn CO3043, dựa trên (a) ứng dụng thật đã cài đặt được và (b) mọi quyết định sản phẩm đã chốt ở Phần 1–2. Văn phong: báo cáo học thuật tiếng Việt, không phải ghi chú nội bộ.

## 2. BỐI CẢNH

- **Repo báo cáo:** `/Users/giantkd/WINDOWS/BKU/HK261/Mobile/mobile-report` — LaTeX, pdfLaTeX + vntex (T5), build bằng `python3 scripts/build.py` (đã cấu hình TinyTeX 4-pass pdflatex→biber→×2; chạy với `PATH="$HOME/Library/TinyTeX/bin/universal-darwin:$PATH"`). Warnings được coi là lỗi (`$warnings_as_errors`).
- **Repo ứng dụng:** `/Users/giantkd/StudioProjects/mobile-app` — 17 module Gradle (`:app`, `:domain`, `:core:{common,designsystem,session,media,network,database,datastore,sync}`, `:data:{video,music,news,games}`, `:feature:{home,video,music,news,games,account,onboarding}`), Kotlin + Compose + Material 3 + Hilt + Media3.
- **Phần 3 hiện trạng:** 7 file ở `sections/3-ui-ux-design/` đều chỉ chứa guide box (`\begin{guide}...\end{guide}`) — phải **viết nội dung thật và xoá guide box** sau khi viết. File `main.tex` của mục cũng có một guide box cần xoá, thay bằng 2–3 câu dẫn nhập.
- **Tài liệu tham chiếu nội bộ (đã có sẵn):** `docs/flows.md` (10 diagram Mermaid), `docs/test-cases.md` (14 TC), `docs/decisions.md` (ADR).

## 3. GROUND TRUTH ĐÃ XÁC MINH (ngày 24/10 — dùng trực tiếp, không đoán lại)

### 3.1. App thật — màn hình & điều hướng (nguồn: `app/src/main/java/com/example/onespace/app/navigation/Destinations.kt`, `feature/*/presentation/*.kt`)

- **Bottom navigation 5 tab (chính là `TopLevelDestination`):** Home, Video, Music, News, Games — icon Material lần lượt `Icons.Filled.Home`, `SmartDisplay`, `MusicNote`, `Newspaper`, `SportsEsports`. Đây chính là "tối đa 5 tab" mà guide yêu cầu.
- **Màn hình có thật (tên composable):** `SplashScreen`, `OnboardingScreen` (gồm `InfoStep`, `MultitaskStep`, `TopicsStep`), `LoginScreen`, `HomeScreen`, `VideoScreen`, `VideoDetailScreen` (có slot `videoSurface` cho PIP/floating), `MusicScreen`, `NowPlayingScreen`, `NewsScreen`, `ArticleScreen`, `GamesScreen`, `GameScreen`, `AccountScreen`, `SettingsScreen`.
- **Trước khi viết 3.1, bắt buộc đọc** `app/navigation/AppNavigation.kt` và `feature/home/presentation/HomeScreen.kt` để xác định: entry thật tới Account/Settings, các route lồng, hành vi back. Sitemap phải vẽ từ những gì đọc được, không được tự nghĩ ra màn.

### 3.2. App thật — design tokens (nguồn: `core/designsystem/.../Theme.kt`)

- Material 3, **brand mint/teal trên nền xanh mực**: light — `primary #41690F`, `background/surface #F8FAF2`, `onBackground #191D17`, `secondary #006A68`, `tertiary #566516`; dark — `primary #B8F36E`, `background/surface #10140E`, `onBackground #E0E4D8`, `secondary #9BD8D1`. Đầy đủ mọi role M3 (container/on-container, outline, surfaceContainer...) có sẵn trong file.
- `dynamicColor = false` mặc định (giữ brand bất kể wallpaper), dark theo hệ thống (`isSystemInDarkTheme`).
- **CẢM BẪY:** bộ màu rose/violet/cyan/emerald (#fb5e7c, #8b5cf6, #22d3ee, #34d399) chỉ là màu của **bản demo HTML cũ** — TUYỆT ĐỐI KHÔNG đưa vào báo cáo. Design System của báo cáo là Theme.kt.
- **Component dùng chung** (`core/designsystem/.../Components.kt`, `Shimmer.kt`): `FeaturePage`, `SectionTitle`, `ContentCard`, `Artwork`, `SkeletonFeed`, `EmptyState`, `ErrorState`, modifier Shimmer.
- **Game đã cài đặt: 2048** (catalog trong `data/games`). Hiện trạng `contentDescription` (TalkBack): có ở account (2), music (3), news (1); **thiếu ở video, games, home, onboarding** — đây là finding thật, đưa vào 3.5 và 3.7.
- **Không có màn tìm kiếm** trong app — khớp phạm vi: search từng phân hệ (F-VID-03, F-MUS-06, F-NEWS-04) và search xuyên nội dung (F-COM-11) đều **không** nằm trong bảng MVP (`tab:mvp-scope-full`); F-COM-11 là mục mở rộng. 3.1 trả lời câu hỏi tìm kiếm theo hướng này.

### 3.3. Report thật — các con số/luật đã chốt (bắt buộc khớp nguyên văn)

- **C1 (đang xem video, mở nhạc):** video tự thu PIP; lần đầu popup **3 lựa chọn "Tắt tiếng video / Tạm dừng nhạc / Phát cả hai"**; nhớ theo cặp nội dung, các lần sau áp dụng im lặng; đổi lại trong Cài đặt.
- **C3 (video → tin):** PIP tự thu nhỏ khi rời tab; kéo được 4 góc; vuốt ngang = dừng + ghi Watchlist theo vị trí; quay lại phóng full, sai lệch ≤ 2 giây.
- **C5:** nhạc duck 30% khi game phát hiệu ứng, tắt duck được. **C9:** tối đa 2 luồng có tiếng ở v1. **C2:** dock tự ẩn trong trình đọc toàn màn hình, có tuỳ chọn ghim.
- **First-run (mục 2.5):** mở app ≤ **2 giây** (không bắt đăng nhập trước) → chọn ≥ 3 chủ đề (30 giây tối đa, cho phép Bỏ qua) → Home hiện danh sách "thử ngay" (1 video + 1 bài hát + 1 tin) → chạm bài hát → dock xuất hiện kèm nhãn → banner nhiệm vụ ngày đầu (Nghe 1 bài · Đọc 1 tin · Thắng 1 ván) → trứng thú cưng nở sau 3 nhiệm vụ → cuối phiên streak = 1.
- **Ngưỡng chất lượng hay trích:** UX-01 phản hồi ≤ 100 ms (skeleton khi chờ dữ liệu), UX-02 tải màn ≤ 3 s, UX-03 cold start ≤ 2 s, UX-06 ≥ 95% frame dưới 16 ms, UX-07 crash ≤ 0,5%, UX-08 ≤ 3 chạm tới nội dung, chuyển phân hệ 1 chạm, UX-12 vùng chạm ≥ 48dp + tương phản ≥ 4.5:1.
- **Truy vết:** persona ở `sec:user-personas` (Minh Anh, Hoàng Nam, Quốc Huy, Thảo Vy, Gia Bảo, Thu Hà), user story ở `sec:user-stories` (bảng `tab:user-stories`), tính năng ở `tab:feature-pool`.

### 3.4. Sai lệch đã biết trong `docs/flows.md` — PHẢI SỬA khi chuyển sang TikZ

- Diagram 3 (C1) ghi lựa chọn "Dừng video phát nhạc" — **sai**; bản đúng là "Tạm dừng nhạc" theo `tab:switch-matrix`.
- Diagram 10 (first-run) ghi "Mở app ≤3 giây" — **sai**; đúng là ≤ 2 giây (UX-03).
- Diagram 4 có ký tự Hán lẫn "打响" — viết lại sạch bằng thuật ngữ đúng (MediaSessionService nhận AudioAttributes).
- Diagram 5, 6 (kiến trúc 3 lớp, module structure) và 8 (Activity lifecycle) là **nguyên liệu của Phần 4** — KHÔNG vẽ lại trong Phần 3, chỉ tham chiếu chéo khi cần.
- Dùng lại: diagram 1 (launch→Home), 2 (C3), 3 (C1, đã sửa), 4 (background audio, đã sửa), 7 (ma trận chuyển tab tổng quan), 9 (game save/resume), 10 (first-run, đã sửa).

## 4. QUY TRÌNH CHỤP ẢNH THẬT (làm TRƯỚC khi viết chữ)

```bash
cd /Users/giantkd/StudioProjects/mobile-app
./gradlew :app:assembleDebug          # nếu fail: dừng, báo user, KHÔNG dùng ảnh thay thế
adb install -r app/build/outputs/apk/debug/app-debug.apk
# light/dark:
adb shell cmd uimode night no        # hoặc ... night yes
# chụp:
adb exec-out screecap -p > /Users/giantkd/WINDOWS/BKU/HK261/Mobile/mobile-report/figures/app/<ten-man>-<mode>.png
```

- Thư mục đích: `figures/app/` (tạo mới), đặt tên kebab-case, vd `home-light.png`, `now-playing-dark.png`.
- **Danh sách ảnh bắt buộc:** Splash (nếu chụp được), 3 bước Onboarding, Login, Home, Video feed, Video player (VideoDetailScreen), MusicScreen, NowPlaying, News feed, Article (trình đọc), Games hub, màn 2048, Account, Settings.
- **Dark mode:** tối thiểu Home + NowPlaying + Article.
- **States (skeleton / empty / error):** app có sẵn `SkeletonFeed`, `EmptyState`, `ErrorState`. Cố gắng trigger từ app thật (mất mạng, feed rỗng…). Nếu một state không thể trigger từ UI, cho phép chụp từ Android Studio Compose Preview của đúng composable đó và **ghi rõ nguồn trong caption** (vd "màn hình trạng thái lỗi — render từ preview của ErrorState"). Không được tự vẽ.
- **PIP/floating video:** chụp 2 ảnh liên tiếp (trước/sau khi rời tab) hoặc ghi chú minh hoạ trong caption nếu không chụp được trạng thái trung gian.
- Trong LaTeX: `\includegraphics[width=0.28\textwidth]{figures/app/...}`, gom 2–3 ảnh chân dung vào một `figure [H]` bằng `minipage`, một `\caption` chung + `\label{fig:app-...}`. KHÔNG thêm package mới nếu minipage đủ dùng.

## 5. QUY ƯỚC DIAGRAM TIKZ

- TikZ, thư viện đã có sẵn: `arrows.meta, positioning, arrows, snakes, backgrounds` (đã load trong preamble). Không thêm package.
- Node: `rounded corners`, fill xám nhạt (`gray!10`) hoặc phẩy màu brand thật (`primary #41690F` → dùng như `fill` với `text=white` cho node nhấn); **không dùng màu demo HTML**.
- Nhãn tiếng Việt; nhãn cạnh (trigger) viết ngắn, là thao tác người dùng ("chạm tab News", "vuốt ngang PIP").
- Mỗi diagram một `figure [H]`, caption tự mô tả, `\label{fig:flow-...}`.
- Quy tắc **khớp 100%**: mỗi nhánh/rổ trong diagram phải đối chiếu được về một dòng trong `tab:switch-matrix` hoặc một user story `US-...`. Trước khi chốt mỗi diagram, đọc lại bảng đó và đối chiếu từng cạnh.

## 6. NỘI DUNG TỪNG MỤC (viết đủ 7 mục; mỗi mục ~1–1,5 trang)

### 3.1 Kiến trúc thông tin và điều hướng — `information-architecture.tex` (giữ `\label{sec:information-architecture}`)
- Sơ đồ sitemap TikZ (cây): Onboarding/Login → 5 tab → các màn con đúng như đọc từ `AppNavigation.kt`.
- Bảng Bottom Navigation: tab | icon (tên Material) | vai trò | lý do; nêu Home là màn mặc định; đối chiếu UX-08 (≤ 3 chạm, chuyển phân hệ 1 chạm).
- Trả lời các câu hỏi guide (viết thành văn xuôi học thuật, KHÔNG giữ format hỏi–đáp): vì sao 5 tab này; số chạm tới nội dung thường dùng; tìm kiếm ở đâu (ngoài MVP, F-COM-11 giai đoạn sau — trung thực); Account/Settings vào từ đâu (theo app thật).

### 3.2 User Flows — `user-flows.tex` (`\label{sec:user-flows}`)
- Diagram TikZ cho: first-run (flows.md #10 đã sửa ≤2s), C1 xung đột âm thanh (#3 đã sửa đúng 3 lựa chọn), C3 PIP (#2), save/resume game 2048 (#9), và ma trận chuyển tab tổng quan (#7).
- **Bảng truy vết:** Flow | Case (C1–C9) | User story | Hình. (pattern giống `tab:usp-trace`).
- Nhánh lỗi/ngoại lệ theo đúng con số đã chốt: mất mạng giữa video (khung hình đứng + đếm ngược 5–15 s tự thử lại; tin đã tải đọc tiếp; game offline chơi tiếp), rút tai nghe (dừng ngay, không phát loa), cuộc gọi (nhường ≤ 0,5 s, quay lại sai lệch ≤ 2 s).

### 3.3 Wireframe, Mockup và Prototype — `wireframes-prototypes.tex` (`\label{sec:wireframes-prototypes}`)
- Khung trung thực về quy trình thật: sơ đồ luồng (3.2) → wireframe bố cục → cài đặt trực tiếp bằng Compose + token M3 (Hi-Fi) → ứng dụng chạy được chính là prototype tương tác.
- Wireframe: vẽ TikZ schematic khối (thanh nav, vùng nội dung, dock) cho 3–4 màn chủ chốt (Home, trình đọc tin + dock, NowPlaying, Games hub).
- **Bảng đối chiếu mỗi màn:** wireframe | ảnh chụp thật | khác biệt chính và lý do.
- Prototype = debug build chạy trên emulator (ghi cách chạy ngắn gọn). KHÔNG bịa link Figma, KHÔNG bịa kết quả kiểm thử với người dùng; nếu chưa làm usability test thì ghi "kế hoạch thực hiện theo UX-09" (usability 5 người, SUS — đã định nghĩa ở `tab:quality-criteria`).

### 3.4 Design System — `design-system.tex` (`\label{sec:design-system}`)
- **Bảng token M3 thật:** vai trò | light (hex) | dark (hex) — chọn ~12–15 dòng đại diện từ Theme.kt (primary/onPrimary, primaryContainer, secondary, tertiary, error, background, surface, surfaceVariant, outline, surfaceContainer…).
- Quyết định thiết kế: brand mint/teal; dynamic color tắt mặc định để giữ brand; dark theo hệ thống (đối chiếu F-COM-13); typography dùng thang mặc định Material 3 (**verify trước**: grep `Typography` trong repo app — nếu không có custom thì ghi đúng vậy); spacing theo lưới của M3 (nếu không có custom 8pt thì trung thực ghi).
- Component library: bảng component dùng chung (`FeaturePage`, `SectionTitle`, `ContentCard`, `Artwork`, `SkeletonFeed`, `EmptyState`, `ErrorState`) + ảnh chụp thật kèm ví dụ sử dụng ở phân hệ nào.
- **Bỏ nội dung Apple HIG/iOS** trong guide (ứng dụng Android-only — đối chiếu Phần 4 đã chọn Android native); chỉ giữ Material 3 với cite `material3`.

### 3.5 Accessibility — `accessibility.tex` (`\label{sec:accessibility}`)
- **Bảng tương phản TÍNH LẠI từ hex Theme.kt** theo công thức WCAG (relative luminance): các cặp chính ở cả 2 mode — onBackground/background, onSurface/surface, onPrimary/primary, onSurfaceVariant/surfaceVariant, onError/error, onPrimaryContainer/primaryContainer. Ghi tỉ lệ (vd 12,4:1) và đạt/không đạt 4,5:1. Công cụ gợi ý: script Python nhỏ hoặc WebAIM; ghi rõ cách đo.
- Vùng chạm: nêu M3 đảm bảo 48dp (`MinimumInteractiveComponentSize`) — verify bằng grep trong code app rồi mới viết.
- TalkBack: trình bày hiện trạng thật (contentDescription có/thiếu theo module — số liệu ở mục 3.2 ground truth) như một vấn đề đã biết kèm kế hoạch khắc phục.
- Dynamic font scaling: Compose dùng `sp` (verify bằng code), bố cục co giãn.
- Phụ đề video: F-VID-16 ngoài MVP — trả lời trung thực + kế hoạch. Cite `wcag22`, `android-accessibility`.

### 3.6 Micro-interactions và phản hồi tức thì — `micro-interactions.tex` (`\label{sec:micro-interactions}`)
- **Bảng theo mô hình Saffer 4 thành phần** (cite `saffer2013`): Tên | Trigger | Rules | Feedback | Loops & Modes — chỉ liệt kê tương tác THẬT có trong app (verify từng dòng bằng grep/đọc code trước khi ghi): dock mini player hiện/ẩn, skeleton shimmer (có `Shimmer.kt`), empty/error feedback, ripple Material, hiệu ứng thắng/thua 2048, v.v. Cái gì không có (vd haptic) thì ghi trung thực "chưa sử dụng, kế hoạch".
- Đối chiếu UX-01 (≤ 100 ms phản hồi, skeleton khi chờ) — đúng câu chữ đã dùng ở quality-pillars (narrative UX-01 đã nhắc skeleton loader và tham chiếu chính mục này).
- Khi nào skeleton vs spinner: theo quy tắc đã có ở quality-pillars (skeleton cho màn nhiều thông tin).

### 3.7 Heuristic Evaluation — `heuristic-evaluation.tex` (`\label{sec:heuristic-evaluation}`)
- **Thực hiện đánh giá thật** theo 10 nguyên lý Nielsen (cite `nielsen-heuristics`): 3 thành viên nhóm (tên trong `metadata.tex`), mỗi người duyệt độc lập trên bộ màn hình đã chụp (dùng đúng ảnh trong Phần 3), rồi gộp.
- **Bảng vấn đề:** Mã (HE-01…) | Màn hình | Nguyên lý vi phạm | Mức 0–4 | Đề xuất sửa | Trạng thái. Gieo sẵn các finding THẬT đã biết: thiếu contentDescription ở video/games/home/onboarding; không có search (Flexibility & efficiency of use);… và bắt buộc soi thêm từng màn từ bộ ảnh chụp để tìm thật (consistency, error prevention, recognition…).
- Trạng thái "chưa sửa" là hợp lệ — KHÔNG bịa "đã sửa". Cuối mục ghi các vấn đề mức 3–4 sẽ được xử lý trong mục kế hoạch.

## 7. RÀNG BUỘC VIẾT & BUILD

- Tiếng Việt học thuật; thuật ngữ chuyên môn giữ tiếng Anh. **Cấm** mọi từ ngữ nội bộ/chấm điểm: "brainstorm", "demo v4/v5", "nhóm chốt", "buổi họp", "cần chốt", "OWNER", "chép tay", "để thuyết trình", "chấm điểm cao", "wow". Không viết format hỏi–đáp của guide.
- **Giữ nguyên 7 `\label`** (`sec:information-architecture`, `sec:user-flows`, `sec:wireframes-prototypes`, `sec:design-system`, `sec:accessibility`, `sec:micro-interactions`, `sec:heuristic-evaluation`) — các phần khác đang `\ref` tới. Xoá guide box trong từng file sau khi viết.
- Không sửa Phần 1/2/4; chỉ tham chiếu chéo một chiều (`\ref` sang `sec:...` đã có).
- Dùng các citation key có sẵn trong `refs.bib`: `material3`, `wcag22`, `saffer2013`, `nielsen-heuristics`, `nielsen-response-times`, `android-accessibility`, `nielsen-five-users`, `sauro2011sus`, `brooke1996sus`, `android-vitals`, `android-launch-time`. **Không thêm bib entry mới** trừ khi user cho phép.
- Build kiểm chứng mỗi khi xong một mục:
  ```bash
  cd /Users/giantkd/WINDOWS/BKU/HK261/Mobile/mobile-report
  PATH="$HOME/Library/TinyTeX/bin/universal-darwin:$PATH" python3 scripts/build.py
  grep -c "^!" build/main.log   # phải = 0
  grep -rnoP '[\x{0400}-\x{04FF}\x{0900}-\x{097F}\x{4E00}-\x{9FFF}\x{3040}-\x{30FF}\x{AC00}-\x{D7AF}]' sections/3-ui-ux-design/   # phải rỗng (phát hiện ký tự lạ)
  ```
- Nếu "bị lỗi": kiểm tra BUILD PROCESS trước khi nghi file `.tex` (quy ước dự án).

## 8. ACCEPTANCE CHECK (chạy trước khi báo xong)

| # | Kiểm tra | Kết quả mong muốn |
|---|----------|-------------------|
| TC1 | Build 4-pass | 0 lỗi `!`, 0 undefined reference, 0 multiply-defined label; PDF tăng trang hợp lý (Phần 3 từ ~4 trang guide → ~10–14 trang thật) |
| TC2 | Nguồn ảnh | Mọi `\includegraphics` trỏ tới file tồn tại trong `figures/app/`; mỗi ảnh map được về một composable có thật (grep tên trong repo app) |
| TC3 | Khớp số liệu (chọn ngẫu nhiên 5) | Mỗi con số trong Phần 3 khớp nguyên văn `tab:switch-matrix` / first-run / `tab:quality-criteria` / hex Theme.kt |
| TC4 | Tương phản | Chọn 1 dòng bất kỳ trong bảng tương phản → tính lại bằng tay/script → trùng số trong bảng |
| TC5 | Guide box | `grep -r "begin{guide}" sections/3-ui-ux-design/` trả về rỗng |
| TC6 | Diagram C1 | Popup đúng 3 lựa chọn "Tắt tiếng video / Tạm dừng nhạc / Phát cả hai"; không còn "Dừng video", không còn "≤3 giây", không còn ký tự Hán |
| TC7 | Ngôn ngữ | `grep -rn "demo v\|brainstorm\|cần chốt\|nhóm chốt\|chép tay" sections/3-ui-ux-design/` rỗng |
| TC8 | Git | `git status` chỉ thay đổi working tree, không có commit mới |

## 9. TUYỆT ĐỐI KHÔNG

- Không commit/push; không đổi nhãn; không sửa Phần 1/2/4; không sửa app Android.
- Không dùng màu demo HTML; không dán Mermaid thô vào LaTeX; không thêm hình vẽ tay/ảnh generate thay ảnh chụp.
- Không bịa: kết quả usability test, số người đánh giá không có thật, "đã sửa" heuristic, tỉ lệ tương phản không tính lại được, link prototype không tồn tại.
- Không thêm package LaTeX mới khi chưa thử hết cách dùng cái có sẵn (minipage thay subcaption…).

## 10. KNOWN LIMITATIONS (cần user quyết nếu vướng)

1. **Emulator/AVD không chạy được** → dừng và báo, không thay ảnh. (Kiểm tra `adb devices`.)
2. **State khó trigger** (empty/error) → dùng Compose Preview + ghi nguồn trong caption (được phép, phải trung thực).
3. **PIP/floating video** khó chụp trạng thái trung gian → 2 ảnh liên tiếp hoặc caption giải thích.
4. Nếu phát hiện mâu thuẫn mới giữa app thật và định nghĩa trong báo cáo (vd: một case C được code khác spec) → **không tự sửa spec**; ghi nhận lại báo user để nhóm quyết.
