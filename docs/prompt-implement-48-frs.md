# PROMPT — Implement toàn bộ 48 Functional Requirements của OneSpace

> **Repo app:** `/Users/giantkd/StudioProjects/mobile-app` — 23 module Kotlin, Compose, Hilt, Media3.
> **Repo report:** `/Users/giantkd/WINDOWS/BKU/HK261/Mobile/mobile-report` — để chụp ảnh + cập nhật audit.
> **Skill:** `@agency-senior-developer` + `@agency-agents-orchestrator` (pipeline nhiều phase).

---

## 0. ARCHITECTURE — ĐỌC TRƯỚC KHI CODE

**Pattern để thêm FR mới (9 file, theo đúng thứ tự):**

```
1. domain/<pkg>/model/X.kt              — data class thuần
2. domain/<pkg>/repository/XRepo.kt     — interface + Flow
3. domain/<pkg>/usecase/XUseCase.kt     — suspend operator fun invoke()
4. data/<pkg>/repository/MockXRepo.kt   — @Singleton, implement interface
5. feature/<pkg>/navigation/XRoute.kt   — sealed interface + @Serializable
6. feature/<pkg>/navigation/XNavGraph.kt — fun NavGraphBuilder.xGraph(callbacks)
7. feature/<pkg>/presentation/XViewModel.kt — @HiltViewModel + StateFlow
8. feature/<pkg>/presentation/XScreens.kt  — @Composable Screen
9. app/navigation/AppNavigation.kt       — wire graph vào NavHost
```

**Quy tắc BẮT BUỘC (VerifyArchitecture check):**
- Feature KHÔNG import feature khác
- Domain KHÔNG phụ thuộc Android/framework
- Feature không nhận NavController → dùng callback
- ViewModel scope theo parent graph qua `getGraphEntry()`
- Chạy `./gradlew verifyArchitecture` sau mỗi thay đổi

**Component sẵn có (dùng lại, không tạo mới):**
`FeaturePage`, `SectionTitle`, `ContentCard`, `Artwork`, `CatalogContent`, `SkeletonFeed`, `EmptyState`, `ErrorState`, `PlaybackFeedback`, `OneSpaceBrand`, `PrototypeNote`, `VideoSurface`, `FloatingVideo`, `MusicMiniPlayer`

**Media engine:** `MediaPlaybackCoordinator` (@Singleton) — 2 ExoPlayer dùng chung.
**Session:** `SessionCoordinator` (Activity-scoped ViewModel) — cross-tab state + C1 popup.
**Room:** `ContentDatabase` — hiện có `video_progress` + `watchlist` tables.
**DataStore:** 12 keys (topics, auth, settings, conflict_rule, simulate_offline...).

**Build & Test:**
```bash
cd /Users/giantkd/StudioProjects/mobile-app
./gradlew verifyArchitecture
./gradlew :app:assembleDebug
./gradlew :domain:test :core:session:testDebugUnitTest :data:auth:testDebugUnitTest
```

**Chụp ảnh verification:**
```bash
adb install -r app/build/outputs/apk/debug/app-debug.apk
adb shell am start -n com.example.onespace/.MainActivity
# điều hướng tới màn cần chụp (dùng uiautomator dump để tìm toạ độ)
adb exec-out screencap -p > /Users/giantkd/WINDOWS/BKU/HK261/Mobile/mobile-report/figures/app/<ten>-light.png
```

---

## 1. NỀN TẢNG GAMIFICATION (làm TRƯỚC TIÊN — mọi thứ khác phụ thuộc)

### 1a. Hệ điểm XP (F-COM-04) — NỀN TẢNG
**Domain:**
```kotlin
// domain/session/model/PointLedger.kt
data class PointEntry(val id: String, val source: String, val amount: Int, val timestamp: Long)
// domain/session/repository/PointRepository.kt
interface PointRepository {
    val totalPoints: Flow<Int>
    val recentEntries: Flow<List<PointEntry>>
    suspend fun add(source: String, amount: Int)
}
```
**Room:** thêm `point_entries` table vào `ContentDatabase` (bump version).
**Mock:** `data/games/repository/PointRepositoryImpl.kt` — Room-backed.
**Nguồn cộng điểm:** xem video +2, nghe nhạc +2, đọc tin +2, thắng game +10, nhiệm vụ +20.

### 1b. Nhiệm vụ hằng ngày (F-COM-05)
**Domain:**
```kotlin
data class DailyMission(
    val id: String,
    val title: String,        // "Nghe 1 bài", "Đọc 1 tin", "Thắng 1 ván"
    val targetType: MissionType, // LISTEN, READ, PLAY
    val target: Int,           // 1
    val progress: Int = 0,
    val completed: Boolean = false,
    val date: LocalDate
)
```
**Room:** `daily_missions` table, tự reset theo ngày.
**UI:** Banner trên Home (3 nhiệm vụ + progress bar + tổng điểm).

### 1c. Streak (F-COM-06)
**Domain:** `StreakCalculator` — dùng app đủ 1 nhiệm vụ → +1; bỏ lỡ → reset 0.
**DataStore:** `streak_count`, `last_active_date`.
**UI:** Tap vào streak → màn calendar tuần (T2-CN, ô xanh = hoàn thành, 🔥 = streak).

### 1d. Pet (F-COM-07)
**Domain:**
```kotlin
data class Pet(
    val stage: PetStage,    // EGG, BABY, TEEN, ADULT
    val pointsEarned: Int
)
```
Trứng nở sau 3 nhiệm vụ hoàn thành. Tiến hoá theo mốc điểm (0/500/2000/5000).
**UI:** Trong Account — ảnh pet + progress evolution + nút cho ăn (-30 điểm).

### 1e. Cửa hàng (F-COM-15)
**UI:** Danh sách quà + giá điểm + nút Mua (trừ số dư).
Items: mở game mới (300-800), đồ pet (50-200), khung avatar (200-800).
**Kèm:** F-COM-09 (khung avatar theo mốc) + F-COM-08 (huy hiệu).

---

## 2. TRỤ USP — TTS + QUIZ (song song với gamification)

### 2a. TTS Nghe tin (F-NEWS-05) — TRỤ W3
**Cách làm:** Android `TextToSpeech` với locale `vi-VN`.
```kotlin
// domain/news/usecase/ListenArticle.kt
class ListenArticle(private val tts: TtsEngine) {
    suspend operator fun invoke(article: Article): Result<AudioSegment>
}
```
**UI:** Nút "Nghe bài này" trong ArticleScreen → progress → phát qua dock.
**Fallback:** nếu TTS vi-VN không có → hiển thị thông báo + hiện bản chữ.

### 2b. Quiz từ bài báo (F-NEWS-10) — TRỤ W4
**Mock data:** Thêm `questions: List<QuizQuestion>` vào Article model.
```kotlin
data class QuizQuestion(
    val question: String,
    val options: List<String>,
    val correctIndex: Int
)
```
**UI:** Nút "Kiểm tra nhanh" cuối bài → màn quiz (3 câu, chọn đáp án, cộng điểm).
**Dùng chung cho:** F-GAME-03 (quiz tin tức) + F-VID-18 (quiz video).

### 2c. Game đoán bài hát (F-GAME-02)
**Cách làm:** Random bài từ kho nhạc → phát 5 giây → hiện 4 tên bài (1 đúng + 3 sai).
**UI:** Màn chơi với timer + 4 buttons đáp án.

---

## 3. VIDEO MODULE (sau khi có nền)

| FR | Việc cần làm | File chính |
|---|---|---|
| F-VID-02 | Feed "Dành cho bạn" theo topic | ✅ ĐÃ CODE (verify trên emulator) |
| F-VID-03 | Ô search ở đầu tab Video | `VideoScreens.kt` + filter theo title/creator |
| F-VID-04 | Màn Watchlist | `WatchlistScreen.kt` + Room watchlist query |
| F-VID-06 | Menu chọn chất lượng 240p-1080p | `VideoDetailScreen` + trackSelectionParameters |
| F-VID-07 | Nút tải video (disable theo copyright flag) | `DownloadVideoUseCase` + copyright check |
| F-VID-09 | Audio-only mode | Toggle ẩn VideoSurface, giữ audio |
| F-VID-10 | Nhấn giữ → Trích mp3 | `MediaExtractor` + `MediaMuxer` → file .m4a |
| F-VID-11 | Share link | `Intent.createChooser` với deep link |
| F-VID-14 | Màn hồ sơ nghệ sĩ | Filter feed theo creator |
| F-VID-15 | Playlist video | `Playlist.kt` model + Room + CRUD screen |
| F-VID-18 | Thẻ quiz cuối video | `QuizQuestion` trong Video model + ContentCard cuối detail |

---

## 4. MUSIC MODULE

| FR | Việc cần làm | File chính |
|---|---|---|
| F-MUS-01 | Thêm nút shuffle + repeat | `NowPlayingScreen` + engine player |
| F-MUS-03 | Nhạc nền notification/lock screen | `MediaSessionService` + FOREGROUND_SERVICE |
| F-MUS-04 | CRUD Playlist | `Playlist.kt` + Room + màn danh sách |
| F-MUS-05 | UI Queue: thêm tiếp theo + kéo sắp | `QueueScreen.kt` + drag-drop |
| F-MUS-06 | Search nhạc | `MusicScreen` + filter title/artist |
| F-MUS-07 | Kho cá nhân + badge nguồn | `MusicScreen` "Đã tải" + badge "trích từ video" |
| F-MUS-08 | Gợi ý theo sở thích | Filter theo selected_topics |
| F-MUS-09 | Siêu playlist trộn | Mixed queue (Track + Article audio) |
| F-MUS-12 | Tải nhạc offline (copyright flag) | Similar F-VID-07 |

---

## 5. NEWS MODULE

| FR | Việc cần làm | File chính |
|---|---|---|
| F-NEWS-01 | Feed "Dành cho bạn" theo topic | `NewsScreen` + filter theo selected_topics |
| F-NEWS-02 | Đổi cỡ chữ (setting toàn app) | Settings screen + M3 typography override |
| F-NEWS-04 | Search bài báo | `NewsScreen` + filter title/category |
| F-NEWS-06 | Sắp xếp Mới nhất/Phổ biến | Chip sort trong feed |
| F-NEWS-11 | Gợi ý bài liên quan | Section "Liên quan" cuối bài (cùng category) |
| F-NEWS-12 | Thẻ nổi khi rời tab | Floating card với scroll position |

---

## 6. GAMES MODULE

| FR | Việc cần làm | File chính |
|---|---|---|
| F-GAME-02 | Đoán bài hát (5 giây → 4 đáp án) | `GuessSongScreen.kt` |
| F-GAME-03 | Quiz tin tức | Tái dùng quiz engine từ F-NEWS-10 |
| F-GAME-07 | Bảng xếp hạng tuần | Mock data + `LeaderboardScreen.kt` |
| F-GAME-08 | Game + video hai nửa màn | Split layout trong `GameScreen` |
| F-GAME-09 | Điểm thưởng khi thắng → XP | Gọi `pointRepository.add("game_win", 10)` |
| F-GAME-13 | Snake | `SnakeGameScreen.kt` — Canvas đơn giản |

---

## 7. DÙNG CHUNG MODULE

| FR | Việc cần làm | File chính |
|---|---|---|
| F-COM-01 | Redesign login: SĐT/email + mật khẩu chính, OTP phụ | `AuthScreens.kt` rewrite |
| F-COM-03 | Hồ sơ + đổi avatar + khung | `AccountScreen` + photo picker |
| F-COM-10 | Wrapped tháng | Mock data + share card |
| F-COM-11 | Search xuyên nội dung | Global search bar trên Home |
| F-COM-12 | Notification nhắc nhiệm vụ | `NotificationChannel` + WorkManager |
| F-COM-14 | C1 popup + checkbox "Đừng hỏi lại" | `OneSpaceApp.kt` C1 dialog |
| F-COM-16 | Offline mode | Cache tin đã lưu + game offline |

---

## 8. THỨ TỰ IMPLEMENT (PHỤ THUỘC)

```
Phase 1: NỀN TẢNG (bắt buộc đầu tiên)
  1a. XP system → Room + PointRepository
  1b. Daily missions → Room + reset logic
  1c. Streak → DataStore + calculator
  1d. Pet → Room + evolution logic
  1e. Shop → UI + point spending
  (F-COM-04, 05, 06, 07, 15, 08, 09)

Phase 2: USP FEATURES (song song)
  2a. TTS nghe tin (F-NEWS-05)
  2b. Quiz engine (F-NEWS-10, F-GAME-03, F-VID-18)
  2c. Đoán bài hát (F-GAME-02)

Phase 3: VIDEO (sau nền)
  F-VID-03 search, F-VID-04 watchlist, F-VID-06 quality,
  F-VID-07 download, F-VID-09 audio-only, F-VID-10 extract,
  F-VID-11 share, F-VID-14 artist, F-VID-15 playlist

Phase 4: MUSIC
  F-MUS-01 shuffle/repeat, F-MUS-03 background, F-MUS-04 playlist,
  F-MUS-05 queue, F-MUS-06 search, F-MUS-07 library, F-MUS-08 suggest,
  F-MUS-09 super playlist

Phase 5: NEWS
  F-NEWS-01 feed, F-NEWS-02 font size, F-NEWS-04 search,
  F-NEWS-06 sort, F-NEWS-11 related, F-NEWS-12 floating

Phase 6: GAMES
  F-GAME-07 leaderboard, F-GAME-08 split, F-GAME-09 points,
  F-GAME-13 Snake

Phase 7: DÙNG CHUNG
  F-COM-01 login redesign, F-COM-03 profile, F-COM-10 wrapped,
  F-COM-11 global search, F-COM-12 notifications, F-COM-14 popup,
  F-COM-16 offline
```

---

## 9. MỖI FR HOÀN THÀNH PHẢI:

1. **Code** theo đúng pattern (9 file template trên)
2. **Build pass:** `./gradlew verifyArchitecture :app:assembleDebug` — 0 lỗi
3. **Unit test pass** (nếu có logic đáng test)
4. **Chạy trên emulator** → điều hướng tới màn mới
5. **Chụp ảnh** → `figures/app/<ten-man>-light.png`
6. **Cập nhật mockup trong REPORT** — thay placeholder bằng ảnh thật:
   - Mở `sections/3-ui-ux-design/wireframes-prototypes.tex`
   - Tìm `\framebox` placeholder cho FR này
   - Thay bằng `\includegraphics[width=0.22\textwidth]{figures/app/<ten-man>-light.png}`
   - Cập nhật caption (bỏ "(chưa có ảnh)")
7. **Cập nhật audit HTML** — sửa `docs/feature-audit-build.py`:
   - Entry AUDIT cho FR này: `mock="none"` → `mock="done"`, `img=None` → `img="<ten-man>-light"`
   - Chạy `python3 docs/feature-audit-build.py` để rebuild HTML
8. **Build report PDF** → 0 lỗi → verify mockup section có ảnh mới
9. **Commit** với message `feat(<module>): <FR code> <tên tính năng>`

### Quy trình chụp ảnh mockup (chi tiết):

```bash
export PATH="$HOME/Library/Android/sdk/platform-tools:$PATH"
# Build + install
cd /Users/giantkd/StudioProjects/mobile-app
./gradlew :app:assembleDebug
adb install -r app/build/outputs/apk/debug/app-debug.apk
# Mở app
adb shell am start -n com.example.onespace/.MainActivity
sleep 3
# Điều hướng tới màn cần chụp (dùng toạ độ bottom nav)
# Home: tap 100 2298 | Video: tap 321 2298 | Music: tap 540 2298
# News: tap 760 2298 | Games: tap 980 2298
# Tài khoản: tap 1006 226 (chỉ hiện trên Home)
# Chụp
adb exec-out screencap -p > /Users/giantkd/WINDOWS/BKU/HK261/Mobile/mobile-report/figures/app/<ten-man>-light.png
# Dark mode (nếu cần)
adb shell cmd uimode night yes
adb exec-out screencap -p > .../<ten-man>-dark.png
adb shell cmd uimode night no
```

### Đặt tên ảnh (kebab-case, nhất quán):
- `xp-banner-light.png` — banner XP trên Home
- `mission-daily-light.png` — màn nhiệm vụ hằng ngày
- `streak-calendar-light.png` — calendar streak
- `pet-screen-light.png` — màn thú cưng
- `shop-light.png` — cửa hàng đổi quà
- `tts-listen-light.png` — TTS nghe tin
- `quiz-screen-light.png` — màn quiz
- `guess-song-light.png` — đoán bài hát
- `video-search-light.png` — search video
- `watchlist-light.png` — danh sách xem sau
- `snake-game-light.png` — Snake
- `leaderboard-light.png` — bảng xếp hạng
- `login-redesign-light.png` — login mới
- v.v.

### Sau khi chụp, cập nhật report mockup:
```bash
cd /Users/giantkd/WINDOWS/BKU/HK261/Mobile/mobile-report
# Thay placeholder bằng ảnh thật
# (tìm \framebox trong wireframes-prototypes.tex, thay bằng \includegraphics)
# Build PDF
PATH="$HOME/Library/TinyTeX/bin/universal-darwin:$PATH" python3 scripts/build.py
# Verify
python3 -c "
import re
log = open('build/main.log', encoding='utf-8', errors='replace').read()
print('Lỗi:', len(re.findall(r'^!', log, re.M)))
s = open('sections/3-ui-ux-design/wireframes-prototypes.tex').read()
print('Ảnh mockup:', s.count('includegraphics'))
print('Còn placeholder:', s.count('framebox'))
"
```

---

## 10. TUYỆT ĐỐI KHÔNG

- KHÔNG skip bước verify (build + emulator + screenshot)
- KHÔNG tạo mock data giả mạo kết quả (nếu chưa làm → placeholder)
- KHÔNG vi phạm architecture rules (feature import feature, domain import Android)
- KHÔNG quên `verifyArchitecture` sau mỗi thay đổi cấu trúc
- KHÔNG commit khi build fail

## 11. SUCCESS CRITERIA

Sau khi hoàn thành toàn bộ:
```bash
./gradlew verifyArchitecture           # Pass
./gradlew :app:assembleDebug           # Success
./gradlew :domain:test                 # All pass
adb install -r app/build/outputs/apk/debug/app-debug.apk  # Install OK
# Mở app → mọi màn hoạt động → 48 screenshot trong figures/app/
# Report PDF build → 0 lỗi
# Mockup section: 0 placeholder còn lại (mọi \framebox đã thay bằng \includegraphics)
# Audit HTML: 48/48 FR có mock status = "done" + ảnh screenshot
```

### Verify cuối cùng mockup coverage:
```bash
cd /Users/giantkd/WINDOWS/BKU/HK261/Mobile/mobile-report
# Đếm ảnh trong mockup section
grep -c "includegraphics" sections/3-ui-ux-design/wireframes-prototypes.tex
# → Phải = 48 (mỗi FR một ảnh)

# Đếm placeholder còn lại
grep -c "framebox" sections/3-ui-ux-design/wireframes-prototypes.tex
# → Phải = 0

# Kiểm tra audit HTML
python3 -c "
html = open('docs/feature-audit.html', encoding='utf-8').read()
print('Decided:', html.count('class=\"done-dec\"'))
print('Mockup done:', html.count('Đã có mockup'))
# → Cả hai phải = 48
"
```
