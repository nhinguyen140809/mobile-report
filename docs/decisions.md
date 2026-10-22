# OneSpace — Quyết định kỹ thuật đã chốt (tóm tắt ADR cho team)

Trích từ bảng ADR mục 4.4 trong report; đặt file này ở `docs/` để mọi thành viên tra nhanh mà không cần mở PDF.

| ADR | Quyết định | File báo cáo |
|-----|-----------|--------------|
| ADR-01 | Android Native, Kotlin + Jetpack Compose | 4.2 |
| ADR-02 | Android 8.0+ (API 26+), mục tiêu RAM tối thiểu 3 GB | 4.1 |
| ADR-03 | MVVM + 3-layer architecture + UDF | 4.3 |
| ADR-04 | Feature-based modularization (app/core/feature/domain) | 4.3 |
| ADR-05 | AndroidX Media3 (ExoPlayer) cho audio/video | 4.2 |
| ADR-06 | MediaSessionService cho Music background | 4.4 |
| ADR-07 | Một nguồn audio có tiếng tại một thời điểm; game được mute SFX | 4.4 |
| ADR-08 | In-app Floating Player cho Video → News/Games | 4.4 |
| ADR-09 | Room cho persisted session/game state; DataStore cho preferences | 4.3 |
| ADR-10 | News cache và offline-first minigame | 4.1 |
| ADR-11 | SessionCoordinator xử lý chuyển đổi phân hệ | 4.3 |
| ADR-12 | Video và game pause khi app vào background; Music tiếp tục | 4.4 |

## Phân công đề xuất

| Module | Thành viên | Ghi chú |
|--------|-----------|---------|
| core/media + dock | Duy | SessionCoordinator, PlaybackCoordinator, AudioFocusController |
| feature/video + PIP | Yến Nhi | VideoPlayerController, watch-later, trích mp3, feed |
| feature/music + TTS nghe tin | Hồng Ái | MusicPlaybackService, playlist/queue, kho cá nhân, F-NEWS-05 |
| feature/news + quiz | Duy | NewsReader, cache, quiz từ bài báo, F-NEWS-10 |
| feature/games | Hồng Ái | GameSessionManager, F-GAME-01/02/03/12/13/14, SaveResume |
| core:database + network | Yến Nhi | Room schema, Retrofit interfaces, DataStore |
| designsystem + home | Duy | Component library, Home Screen, onboarding |
| Testing | Cả nhóm | 14 test case TC01–TC14 (bảng 4.4) |

## Stack liên hệ nhanh

```
Language:     Kotlin
UI:           Jetpack Compose + Material 3
Navigation:   Navigation Compose
State:        ViewModel + StateFlow
DI:           Hilt
Network:      Retrofit + OkHttp
DB:           Room
Preferences:  DataStore
Media:        AndroidX Media3 (ExoPlayer + MediaSessionService)
Image:        Coil
Background:  WorkManager
Testing:      JUnit + Compose UI Test
```
