# OneSpace — Mermaid flows để review

Dán các sơ đồ dưới đây vào các công cụ render Mermaid (VS Code Mermaid Preview, GitHub, [mermaid.live](https://mermaid.live)).

---

## 1. Execution Flow — từ launch đến Home

```mermaid
flowchart TD
    A[Launch app] --> B[Initialize Hilt DI]
    B --> C[Load preferences + saved session\nfrom DataStore/Room]
    C --> D{Có phiên đăng nhập?}
    D -- Có --> E[Home Screen]
    D -- Không --> F[Guest Mode\nhoặc màn Đăng nhập]
    F --> E
    E --> G{Người dùng chọn phân hệ}
    G --> H[Video]
    G --> I[Music]
    G --> J[News]
    G --> K[Games]
    H & I & J & K --> L[SessionCoordinator\nlưu / khôi phục trạng thái]
```

---

## 2. SessionCoordinator — chuyển tab Video → News (case C3)

```mermaid
flowchart TD
    A[Người dùng chạm tab News\nđang trong tab Video] --> B[SessionCoordinator]
    B --> C[VideoPlayerController:\nchuyển sang chế độ Floating]
    C --> D[Navigation Compose:\nđiều hướng sang News]
    D --> E[Video vẫn phát\ntrong cửa sổ PIP góc màn]
    E --> F[News screen hiển thị\nnhạc vẫn có thể đang phát]
    F --> G{Người dùng chạm PIP?}
    G -- Có --> H[Quay lại tab Video\nfull screen, đúng vị trí]
    G -- Vuốt ngang PIP --> I[Dừng video\nlưu vào Watchlist theo vị trí]
```

---

## 3. Audio Focus Conflict — Video + Music (case C1)

```mermaid
flowchart TD
    A[Video đang phát] --> B[Người dùng mở bài nhạc]
    B --> C{Lần đầu cho cặp\nVideo + Nhạc?}
    C -- Có --> D[Popup 3 lựa chọn]
    D --> E1[🔇 Tắt tiếng video\nphát nhạc]
    D --> E2[⏹ Dừng video\nphát nhạc]
    D --> E3[🎵 Giữ nguyên\nkhông phát nhạc]
    C -- Không --> F{Quy tắc đã nhớ?}
    F -- mute --> G[Tự tắt tiếng video\nphát nhạc, không hỏi]
    F -- stopv --> H[Tự dừng video\nphát nhạc, không hỏi]
    F -- keep --> I[Không phát nhạc\nvideo tiếp tục, không hỏi]
    E1 --> J[Lựa chọn lưu vào DataStore]
    E2 --> J
    E3 --> J
```

---

## 4. Background Audio Playback — Music khi khoá màn

```mermaid
flowchart TD
    A[Người dùng phát nhạc] --> B[MediaSessionService nhận AudioAttributes]
    B --> C[musicservice打响 MediaSession\nnotification hiện]
    C --> D{Người dùng hành động?}
    D -- Khoá màn hình --> E[Nhạc tiếp tục\nLock screen hiện nút play/pause/next]
    D -- Bấm Home --> F[Nhạc tiếp tục\nNotification điều khiển được]
    D -- Cuộc gọi đến --> G[AudioManager phát AudioFocus LOSS\n→ Nhạc pause]
    G --> H[Sau cuộc gọi\nNhạc tự resume]
    D -- Rút tai nghe --> I[AudioDeviceCallback\n→ Nhạc pause, không phát loa]
    D -- Mở video có tiếng --> J[AudioFocus LOSS_TRANSIENT\n→ Nhạc pause, video phát]
    D -- Mở game đã mute SFX --> K[Nhạc tiếp tục\ngame chỉ phát SFX không]
```

---

## 5. Kiến trúc 3 lớp

```mermaid
flowchart LR
    subgraph Presentation
        UI[Compose Screens\n+ Floating UI\n+ Mini Player]
        VM[Feature ViewModels\nStateFlow + State]
        UI --> VM
    end
    subgraph Domain
        UC1[PlayMediaUseCase]
        UC2[SwitchContentUseCase]
        UC3[ResolveAudioConflict]
        UC4[SaveGameUseCase]
        UC5[RestoreSessionUseCase]
        UC6[SyncNewsUseCase]
        RI[Repository Interfaces]
        UC1 & UC2 & UC3 & UC4 & UC5 & UC6 --> RI
    end
    subgraph Data
        REPO[Repository Impls]
        LOCAL[Room\nDataStore\nMedia Cache\nGame State]
        REMOTE[Video API\nMusic API\nNews API\nAuth API]
        REPO --> LOCAL
        REPO --> REMOTE
    end
    VM -->|use cases| UC1
    RI -->|implements| REPO
```

## 6. Module structure

```mermaid
flowchart TD
    APP[app/\nMainActivity\nAppNavigation\nOneSpaceApplication]
    subgraph core/
        C1[common/]
        C2[model/]
        C3[database/]
        C4[network/]
        C5[datastore/]
        C6[media/]
        C7[designsystem/]
        C8[session/]
    end
    subgraph feature/
        F0[home/]
        F1[video/]
        F2[music/]
        F3[news/]
        F4[games/]
        F5[account/]
    end
    subgraph domain/
        D1[repository/\ninterfaces]
        D2[usecase/]
        D3[model/]
    end
    APP --> F0 & F1 & F2 & F3 & F4 & F5
    F1 & F2 & F3 & F4 --> D2 --> D1
    D1 --> C3 & C4 & C5 & C6
    F0 & F1 & F2 & F3 & F4 & F5 --> C7
```

---

## 7. Ma trận chuyển tab — hành vi tổng quan

```mermaid
flowchart LR
    V[Video] -- "PIP" --> N[News]
    V -- "pause vid, play music" --> M[Music]
    V -- "PIP + game mute" --> G[Games]
    M -- "dock + đọc" --> N
    M -- "pause music khi vid có tiếng" --> V
    M -- "dock + game mute" --> G
    G -- "pause + save" --> N
    G -- "pause + save" --> V
    N -- "lưu vị trí đọc" --> G

    style V fill:#fb5e7c,color:#fff
    style M fill:#8b5cf6,color:#fff
    style N fill:#22d3ee,color:#000
    style G fill:#34d399,color:#000
```

---

## 8. Activity Lifecycle vs MediaSessionService

```mermaid
stateDiagram-v2
    [*] --> Created
    Created --> Started
    Started --> Resumed
    Resumed --> Paused : App loses focus
    Paused --> Resumed : Return quickly
    Paused --> Stopped : No longer visible
    Stopped --> Resumed : Return
    Stopped --> ProcessRemoved : System reclaims memory
    Stopped --> Destroyed : Activity finishes
    ProcessRemoved --> Created : Relaunch
    Destroyed --> [*]

    note right of ProcessRemoved
        MediaSessionService vẫn chạy
        (vòng đời riêng)
    end note
```

---

## 9. Game Session Save/Resume

```mermaid
flowchart TD
    A[Người dùng chơi 2048] --> B{Chuyển tab?}
    B -- Có --> C[GameSessionManager:\npause game loop]
    C --> D[Lưu board + score + level\nvào Room]
    D --> E[Người dùng quay lại]
    E --> F{Có saved state?}
    F -- Có --> G[Đọc từ Room\nResume từ vị trí cũ]
    F -- Không --> H[New game]
    B -- OS kill process --> I[Room đã lưu trước đó]
    I --> J[Mở lại app → RestoreSession\nkhôi phục đúng board + score]
```

---

## 10. First-run (phiên đầu tiên)

```mermaid
flowchart TD
    A[Mở app ≤3 giây] --> B[Onboarding:\nchọn tối thiểu 3 sở thích\ntrong chip cả 4 phân hệ\n≤30 giây]
    B --> C[Home:\ndanh sách Thử ngay hôm nay\n1 video + 1 bài hát + 1 tin]
    C --> D[Chạm 1 bài hát\n→ dock mini player xuất hiện\nlần đầu kèm hint]
    D --> E[Banner nhiệm vụ ngày đầu:\nNghe 1 bài · Đọc 1 tin · Thắng 1 ván\n+20 mỗi việc]
    E --> F[Mở bài tin đầu tiên\n→ gợi ý nhỏ\n``đọc và nghe nhạc cùng lúc'']
    F --> G[Hoàn thành 3 nhiệm vụ]
    G --> H[Trứng thú cưng nở\+50 bonus\nstreak = 1]
    H --> I[Kết phiên:\nnhắc mai quay lại giữ mốc 7 ngày]
```
