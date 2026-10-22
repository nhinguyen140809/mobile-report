# PROMPT: Bổ sung đầy đủ UI/UX screens cho OneSpace demo

> Copy file này vào Claude/ChatGPT/AI khi cần bổ sung screens. Đi kèm file `mvp-demo.html` hiện tại.

---

## ROLE

Bạn là **senior Android UI/UX developer** implement Jetpack Compose + Material 3. Bạn đang mở rộng một bản HTML demo (OneSpace) đã có 5 tab Home/Video/Music/News/Games với dock mini-player. Nhiệm vụ của bạn là **bổ sung các screens và states còn thiếu** theo checklist UI/UX bên dưới — KHÔNG đụng vào logic gameplay/streaming đã có.

---

## EXISTING DESIGN SYSTEM (giữ nguyên)

```css
/* Module colors */
--cA: #fb5e7c  /* Video - rose */
--cB: #8b5cf6  /* Music - violet */
--cC: #22d3ee  /* News - cyan */
--cD: #34d399  /* Games - emerald */
--cX: #fbbf24  /* Points - gold */

/* Glass surfaces */
background: rgba(16,20,32,.72);
backdrop-filter: blur(18px);
border: 1px solid rgba(255,255,255,.13);
border-radius: 20px;

/* Font */
font-family: "Be Vietnam Pro", sans-serif;

/* Buttons: pill, gradient primary, glass secondary */

/* Layout: phone frame 396px, bottom nav 5 tabs */
```

---

## CHECKLIST SCREENS & STATES CẦN BỔ SUNG

### A. ONBOARDING FLOW (chưa có)

**Rule từ bài giảng:** *Value, Permission, Continuity. First-run experience explains the benefit, asks only contextual permissions, and creates a safe next action.*

| Màn | Nội dung | Component |
|-----|----------|-----------|
| Splash | Logo OneSpace gradient, tagline "4 trong 1 · liền mạch", fade-out → Onboarding | Container: full-screen gradient |
| Onboarding 1/3 | "Tất cả trong một app" — 4 icon phân hệ nhỏ, text 1 câu | Information card |
| Onboarding 2/3 | "Đa nhiệm liền mạch" — mockup dock + PIP mini | Illustration (CSS art) |
| Onboarding 3/3 | "Chọn sở thích" — chip chọn chủ đề của 4 phân hệ, skip được | Input: multi-select chips |
| Login | Google Sign-In + email/OTP | Input: form 2 fields + button |
| Guest mode | "Dùng thử không cần tài khoản" | Navigation: bottom-sheet |

### B. PROFILE & SETTINGS (chưa có)

| Màn | Nội dung |
|-----|----------|
| Profile sheet | Avatar + khung, tên, streak count, pet, đóng góp điểm |
| Settings sheet | Dark/light mode switch, ngôn ngữ (Vietnamese/English), Data Saver, notification preferences |
| Logout confirm | Bottom-sheet "Bạn có muốn đăng xuất?" + Cancel/OK |

### C. EMPTY STATES (chưa có — bắt buộc mỗi phân hệ)

**Rule:** *Empty result offer no next step = fail. Luôn cho CTA.*

| Phân hệ | Empty content | CTA |
|----------|---------------|-----|
| Video feed | Icon 🎬 + "Chưa có video nào" +原因是 | Button: "Chọn chủ đề khác" |
| Music library | Icon 🎵 + "Kho nhạc trống" | Button: "Bật nhạc ngẫu nhiên" |
| News feed | Icon 📰 + "Chưa có tin tức" | Button: "Chọn chuyên mục" |
| Games hub | Icon 🎮 + "Chưa mở khoá game nào" | Button: "Chơi thử Snake" |
| Watch later | "Chưa lưu video nào" | Button: "Khám phá video" |
| Queue/dock | "Hàng phát trống" | Hint: "Chạm đĩa để mở trình phát" |

### D. ERROR STATES (chưa có — quan trọng nhất)

**Rule:** *Offline error + Partial error + Server error. Không hiện "Error -1". Luôn cho retry + hướng dẫn.*

| State | Nội dung | CTA |
|-------|----------|-----|
| Offline (feed) | ⚠️ "Không có kết nối" + "Hiển thị nội dung đã tải" | Button: "Thử lại" + link: "Xem tin đã lưu" |
| Offline mid-stream | Video khung hình đứng + countdown 5-15s | Button: "Hủy" hoặc auto-retry |
| Partial error | "Không tải được hình ảnh" + text vẫn đọc được | Icon inline, không chặn |
| Server 500 | 🖥 "Lỗi hệ thống, thử lại sau" | Button: "Thử lại" |
| Permission denied | "Cần quyền thông báo để nhắc nhiệm vụ" | Button: "Mở Cài đặt" |

### E. LOADING STATES (chưa có)

**Rule từ bài giảng:** *Skeleton dùng khi giao diện có nhiều thông tin. Spinner dùng khi giao diện nhẹ.*

| Phân hệ | Loading type | Hiển thị |
|----------|--------------|---------|
| Video feed | Skeleton | 3-4 rectangle shimmer cards + avatar circles |
| Music library | Skeleton | 3 row shimmer với circle + lines |
| News feed | Skeleton | 2 card shimmer + text line shimmer |
| Quiz/TTS | Spinner | Small spinner trong button "Đang chuẩn bị..." |
| Trích mp3 | Progress | Progress bar với % + cancel |
| Sign in | Button state | Text đổi thành "Đang đăng nhập..." + disabled |

### F. MICRO-INTERACTIONS CẦN THÊM

| Feature | Rule áp dụng |
|---------|-------------|
| Undo toast | Sau khi xoá playlist/đổi quà: snackbar "Đã xoá. Hoàn tac?" + [Undo] |
| Back button | Khi trong bottom-sheet: chạm ngoài = đóng (không mất data) |
| Permission request | Không hỏi ngay lúc mở app; hỏi lúc user làm action liên quan |
| Touch target | Mọi button ≥ 48×48dp (Google) / ≥ 44×44pt (Apple) |
| Contrast | Text trên background: ratio ≥ 4.5:1 (WCAG AA) |
| Typography hierarchy | Display / Headline / Body / Caption — roles rõ ràng |

---

## CONSTRAINTS (bắt buộc)

1. **State management**: Screens mới dùng cùng system `class="screen"` + `id="scr-xxx"` như bản hiện tại; thêm vào `go()` function.
2. **Tự động tạo error/empty states**: Mỗi list có 3 chế độ: `data-state="loading" | "loaded" | "error" | "empty" | "offline"`.
3. **Skeleton**: Dùng CSS animation `@keyframes shimmer` với gradient background, KHÔNG dùng ảnh.
4. **ControllerCSS**: Compose dùng Material 3; demo HTML dùng glass card style hiện có.
5. **Accessibility**: Mỗi button thêm `aria-label` nếu chỉ có icon; touch target 48px.
6. **Undo pattern**: Snackbar/Toast hiện [Undo] button, tự biến mất sau 4 giây.
7. **Ngôn ngữ**: Toàn bộ text tiếng Việt; thuật ngữ giữ tiếng Anh.

---

## OUTPUT FORMAT

Trả về **một patch** (diff hoặc file mới) gộp vào file `mvp-demo.html` existed, gồm:
1. CSS mới cho onboarding, skeleton, error states
2. HTML mới cho các screens mới
3. JS function mới cho state switching

---

## EVALUATION CHECK

Sau khi implement, mỗi screen phải trả lời 4 câu (từ khung đánh giá bài giảng):

| Lens | Câu hỏi |
|------|---------|
| **Component** | Button có matched với action không? |
| **Flow** | Next step có giảm uncertainty không? |
| **Access** | State có đọc được, nghe được, phóng to được, chạm được? |
| **State** | Progress và recovery có hiển thị? |

---

## TEST CASES

```
TC01: Mở demo lần đầu → Splash → Onboarding 1/2/3 → chọn sở thích → Home
TC02: Guest mode → mọi phân hệ hoạt động → lưu playlist → hiện prompt tạo tài khoản
TC03: Tắt Wi-Fi → mở Video → hiện offline状態 + retry
TC04: Feed rỗng → hiện empty state + CTA "Chọn chủ đề"
TC05: Xoá bài hát khỏi playlist → snackbar [Undo] → chạm Undo → bài hát restored
TC06: Button "Trích mp3" loading → progress bar 0-100% → hoàn tất → toast success
TC07: SignUp → email không hợp lệ → inline error message + button vẫn enabled
TC08: Logout → confirm sheet → OK → quay về Login
TC09: Đозна button ≥ 48px bằng Inspect Element
TC10: Contrast text/nền ≥ 4.5:1 (dùng WebAIM Contrast Checker)
```
