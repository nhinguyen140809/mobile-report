# OneSpace — Test cases cho kiểm chứng kiến trúc

Trích từ bảng TC01–TC14 mục 4.4 trong report; dùng để team test trên máy thật/emulator.

| ID | Tình huống | Kết quả mong đợi | Cách test |
|----|-----------|-----------------|-----------|
| TC01 | Video → Tin | Video thu nhỏ thành PIP, tiếp tục phát | Chuyển tab trong app |
| TC02 | Video → Nhạc | Video pause, Nhạc bắt đầu | Chuyển tab + chạm 1 bài |
| TC03 | Nhạc → Home → khoá màn | Nhạc tiếp tục, lock screen hiện nút điều khiển | Bấm Home rồi khoá |
| TC04 | Nhạc → Games (game mute) | Nhạc vẫn phát | Vào game đã mute SFX |
| TC05 | Game → Tin → Game | Khôi phục đúng board + score | Chuyển tab rồi quay lại; check Room |
| TC06 | Mất mạng khi đọc Tin | Hiển thị bài đã cache | Tắt Wi-Fi/Data, mở app |
| TC07 | Mất mạng khi stream Video | Phát buffer còn lại, rồi hiện retry | Tắt mạng giữa lúc xem |
| TC08 | Có mạng trở lại | Cho phép retry/resume | Bật lại mạng |
| TC09 | Activity recreate (xoay màn) | Trạng thái giữ (rememberSaveable + ViewModel) | Xoay ngang → dọc |
| TC10 | OS kill app process | Khôi phục phiên từ Room/DataStore | Force stop từ Settings → mở lại |
| TC11 | Cuộc gọi khi nghe Nhạc | Pause → sau cuộc gọi resume | Gọi từ máy khác |
| TC12 | Rút tai nghe | Nhạc pause, không phát loa | Ngắt jack hoặc Bluetooth |
| TC13 | Thiết bị RAM 3 GB | Không crash/OOM trong demo | Chạy trên emulator hoặc máy thật 3 GB |
| TC14 | Bật Battery Saver | Giảm tác vụ nền | Vào Settings > Battery → test |

## Công cụ đo hiệu năng/pin

- **Android Studio Profiler**: đo CPU, memory, network per phân hệ
- **Memory Profiler**: heap dump khi nền 3 app (video PIP + nhạc + game)
- **Perfetto (trace)**: timeline chi tiết spacing frame

So sánh kịch bản đo:
1. Chỉ mở 1 phân hệ (baseline)
2. PIP video + đọc tin
3. Nhạc + game
4. Cả 3 luồng chạy (nếu hỗ trợ)

Ghi kết quả vào đây sau khi test:
```
[Device model]: [RAM], [Android version]
TC01: [pass/fail] — ghi chú nếu fail
TC02: [pass/fail]
...
TC13: [pass/fail] — FPS khi PIP = __, RAM dùng = __ MB
TC14: [pass/fail]
```
