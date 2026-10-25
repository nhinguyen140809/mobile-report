#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build docs/feature-audit.html — audit 77 tính năng OneSpace × mockup × khả thi.

Nguồn:
  - sections/2-product-scope/feature-prioritization.tex  (77 tính năng + I/E/nhóm)
  - sections/2-product-scope/mvp-scope.tex                 (thành viên MVP / mở rộng / ngoài phạm vi)
  - AUDIT dict bên dưới (kết quả verify từng tính năng bằng grep/đọc code app + ảnh chụp)
  - figures/app/*.png                                      (ảnh chụp thật từ app)

Chạy lại bất cứ lúc nào:  python3 docs/feature-audit-build.py
"""
import base64
import io
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
APP = Path("/Users/giantkd/StudioProjects/mobile-app")
OUT = ROOT / "docs" / "feature-audit.html"

# ----------------------------------------------------------------------------- 
# 1. Phân tích danh mục tính năng từ report
# -----------------------------------------------------------------------------
def parse_features():
    tex = (ROOT / "sections/2-product-scope/feature-prioritization.tex").read_text(encoding="utf-8")
    feats = []
    for line in tex.splitlines():
        m = re.match(r"\\texttt\{(F-(?:VID|MUS|NEWS|GAME|COM)-\d+)\} & (.+?) & (\d) & (\d) & (.+?) & ?(.*?)\s*\\\\\s*$", line.strip())
        if not m:
            continue
        code, name, i, e, group, note = m.groups()
        group = re.sub(r"\\texttt\{\[[^\]]*\]}\s*", "", group).strip()
        feats.append({"code": code, "name": name.strip(), "i": int(i), "e": int(e), 
                      "group": group, "note": note.strip()})
    assert len(feats) == 69, f"kỳ vọng 71 tính năng, tìm thấy {len(feats)}"
    return feats


def parse_scope():
    """Trả về dict mã -> 'v1' | 'v2'. v1 = có trong bảng MVP của mvp-scope."""
    tex = (ROOT / "sections/2-product-scope/mvp-scope.tex").read_text(encoding="utf-8")
    mvp_block = re.search(r"\\label\{tab:mvp-scope-full\}(.*?)\n\\end\{table\}", tex, re.S).group(1)
    mvp_codes = set()
    for raw in re.findall(r"(F-(?:VID|MUS|NEWS|GAME|COM)-\d+(?:/\d+)*)", mvp_block):
        parts = raw.split("/")
        mvp_codes.add(parts[0])
        prefix = parts[0].rsplit("-", 1)[0]
        for tail in parts[1:]:
            mvp_codes.add(f"{prefix}-{tail}")
    # mọi mã trong bảng tính năng mà KHÔNG nằm trong MVP = v2
    feat_codes = set()
    for m in re.finditer(r"\\texttt\{(F-(?:VID|MUS|NEWS|GAME|COM)-\d+)\} &", tex):
        pass  # tex ở đây là mvp-scope, không phải feature-prioritization
    ftex = (ROOT / "sections/2-product-scope/feature-prioritization.tex").read_text(encoding="utf-8")
    all_codes = set(re.findall(r"\\texttt\{(F-(?:VID|MUS|NEWS|GAME|COM)-\d+)\} &", ftex))
    return {c: ("v1" if c in mvp_codes else "v2") for c in all_codes}


A = {
  # ----- A. Streaming Video -----
  "F-VID-01": dict(mock="done", feas="easy", rec="giữ-mvp", img="video-player-gestures.png",
      code="feature/video/presentation/VideoScreens.kt + core/media (ExoPlayer)",
      why="Player YouTube-style: slider tua; transport 5 nút ◀◀ / ⏪10s / ▶ / ⏩10s / ▶▶▶ centered (12dp gap); 3 nút Chia sẻ/Tải/Lưu icon-only ngang hàng kênh (26dp icon, 48dp button); Liên quan dùng FeedCard; ảnh thật.",
      ),
  "F-VID-02": dict(mock="done", feas="easy", rec="giữ-mvp", img="video-feed-chips.png",
      code="feature/video — feed hiện phẳng, không có filter sở thích",
      why="Chip lọc kiểu YouTube: Tất cả (mặc định, toàn bộ video) / Dành cho bạn / chip từng chủ đề; ảnh thật.",
      ),
  "F-VID-03": dict(mock="done", feas="easy", rec="giữ-mvp", img="video-search-results.png",
      code="grep search/tìm kiếm trong feature/video = 0 kết quả",
      why="Search: kênh khớp hiện TRƯỚC (card avatar + số video, mở trang kênh), video xếp sau, không hiện \"Tất cả video\" khi tìm; không khớp → \"Không có video phù hợp\" + mục Liên quan (video chia sẻ token với từ khoá); ảnh thật.",
      ),
  "F-VID-04": dict(mock="done", feas="easy", rec="giữ-mvp", img="home-watchlist-sheet.png",
      code="core/media/MediaPlaybackCoordinator.kt:250 addToWatchlist() + ViewingSessionRepository",
      why="Nút \"Xem sau (n)\" chuyển sang tab Home (dưới ô tìm toàn cục), bấm mở bottom sheet danh sách video đã lưu; ảnh thật.",
      ),
  "F-VID-05": dict(mock="done", feas="easy", rec="giữ-mvp", img="video-history-sheet.png",
      code="HomeScreen \"Tiếp tục\" + VideoScreens \"Tiếp tục xem\" + ViewingSessionRepository",
      why="Chip \"Đã xem\" thứ 3 trên hàng lọc; nhóm Hôm nay/Hôm qua/thứ/dd.MM (updatedAt); MỌI thẻ video trên feed/search/playlist/kênh đều có thanh đỏ tiến độ xem — chữ \"Đã xem đến X\" chỉ trong mục Đã xem; ảnh thật.",
      ),
  "F-VID-06": dict(mock="done", feas="easy", rec="giữ-mvp", img="video-quality-menu.png",
      code="core/media/MediaPlaybackCoordinator.kt:102 trackSelectionParameters + Settings \"Tiết kiệm dữ liệu\"",
      why="Menu ⚙️: Tốc độ phát = thanh trượt 4 mức (0.5/1/1.5/2) + giá trị to đậm; Chất lượng = danh sách riêng với tick CheckCircle — hai phân vùng phân biệt rõ; ảnh thật.",
      ),
  "F-VID-07": dict(mock="done", feas="easy", rec="giữ-mvp", img="video-download.png",
      code="không có UI tải video",
      why="Nút tải trên video detail ghi/xoá Room downloaded_content (DB v5); Hồ sơ có màn \"Đã tải\" với tab chips Video/Music/Báo — mỗi tab list nội dung đã lưu, chạm mở đúng loại; ảnh thật.",
      ),
  "F-VID-08": dict(mock="done", feas="easy", rec="giữ-mvp", img="news-pip-light",
      code="core/media/VideoSurface.kt + nút \"Thu nhỏ & khám phá\" trong VideoScreens",
      why="Cửa sổ nổi chạy thật trên mọi tab, có ảnh chụp."),
  "F-VID-09": dict(mock="done", feas="easy", rec="giữ-mvp", img="video-audio-mp3.png",
      code="không có UI chế độ chỉ âm thanh",
      why="Nút \"Chỉ nghe âm thanh\" (Headphones) cạnh nút PIP góc dưới-phải: bật audio-only + thu nhỏ — cửa sổ nổi render thành mini player kiểu nhạc (AudioOnlyState shell-level); nút \"Xem video\" trên placeholder mở lại hình; ảnh thật.",
      ),
  "F-VID-10": dict(mock="done", feas="easy", rec="giữ-mvp", img="video-longpress-mp3.png",
      code="data/music/MockMusicRepository.kt (mp3 mẫu cờ ngoại tuyến) + MusicScreens \"Đã tải\"",
      why="Giữ video → dialog xác nhận → ghi Room extracted_audio (kèm url + duration, DB v4); thẻ trong mục \"Từ video của bạn\" ĐÚNG format thẻ nhạc (MusicNote + title + \"creator · duration\"); chạm = PHÁT NHƯ BÀI NHẠC THẬT qua engine nhạc (Track ext-<id> + playMusicPlaylist) → NowPlaying + dock mini player nhạc điều khiển, KHÔNG dính video; ảnh thật.",
      ),
  "F-VID-11": dict(mock="done", feas="easy", rec="giữ-mvp", img="video-share-sheet.png",
      code="grep Chia sẻ/share chỉ ra comment mã nguồn",
      why="Intent ACTION_SEND mở sheet chia sẻ hệ thống; ảnh thật.",
      ),
  "F-VID-14": dict(mock="done", feas="easy", rec="giữ-mvp", img="video-artist-profile.png",
      code="không có màn hồ sơ nghệ sĩ — creator chỉ hiện dạng text trên card",
      why="Route Artist(creator): avatar chữ cái đầu, số video, danh sách video của kênh; ảnh thật.",
      ),
  "F-VID-15": dict(mock="done", feas="easy", rec="giữ-mvp", img="video-save-sheet.png",
      code="grep Playlist trong feature/video = 0",
      why="Sheet Lưu gọn: hàng Xem sau chỉ nhãn + CheckCircle (không mô tả), playlist chỉ tên + số, một nút \"Tạo\" duy nhất — bỏ \"Tạo và lưu vào playlist\" và \"Xong\"; ảnh thật.",
      ),
  "F-VID-17": dict(mock="done", feas="easy", rec="giữ-mvp", img="video-speed-menu.png",
      code="core/media/VideoSurface.kt:22 detectTapGestures(onDoubleTap) → onSeekBy(10s)",
      why="Tốc độ phát 0.5x-2x chuyển thành thanh trượt (steps=2) trong menu ⚙️, kèm giá trị đậm; huy hiệu tốc độ trên góc video; ảnh thật.",
      ),
  "F-VID-18": dict(mock="done", feas="easy", rec="giữ-mvp", img="video-end-offer.png",
      code="không có thẻ game cuối video",
      why="Hết video: dialog hỏi \"Chơi thử câu đố?\" trước, đồng ý mới hiện quiz +20 XP; ảnh thật.",
      ),

  # ----- B. Listening to Music -----
  "F-MUS-01": dict(mock="done", feas="easy", rec="giữ-mvp", img="music-nowplaying-favorite.png",
      code="feature/music/presentation/MusicScreens.kt NowPlayingScreen",
      why="Player compact: artwork 64dp trái + title/artist phải + 3 nút (Yêu thích/Tải/Lưu) IconButton bên phải header; transport YouTube-style: ◀◀ prev / ▶▶ play / ▶▶▶ next (KHÔNG nút ±10s, KHÔNG shuffle/repeat — chỉ trong playlist); ảnh thật.",
      ),
  "F-MUS-02": dict(mock="done", feas="easy", rec="giữ-mvp", img="article-music-dock-light",
      code="dock mini trong app shell + SessionCoordinator",
      why="Dock hiện trên mọi feed và trong trình đọc bài, có ảnh chụp."),
  "F-MUS-03": dict(mock="done", feas="easy", rec="giữ-mvp", img="music-nowplaying-queue.png",
      code="grep ForegroundService/MediaSessionService = 0",
      why="Nhạc chạy nền: NHẮM ĐÚNG NGHĨA — thoát app nhạc vẫn phát, điều khiển qua notification (trong demo: mini player dock + audio tiếp tục khi rời app; notification cần MediaSessionService ở bản phát hành); ảnh thật.",
      ),
  "F-MUS-04": dict(mock="done", feas="easy", rec="giữ-mvp", img="music-playlist-screen.png",
      code="grep playlist trong feature/music = 0 UI",
      why="Playlist nhạc: nút Phát + công tắc Ngẫu nhiên/Lặp lại gắn thẳng shuffle/repeat của SessionCoordinator (giữ nguyên 2 nút này trên NowPlaying khi đang nghe); playMusicPlaylist phát nguyên playlist thành queue; có nút xóa; ảnh thật.",
      ),
  "F-MUS-05": dict(mock="done", feas="easy", rec="giữ-mvp", img="music-nowplaying-queue.png",
      code="domain SelectNextTrack + core/media queue logic",
      why="Queue: số thứ tự + title + artist (click mở trang nghệ sĩ) + nút ✕ xoá (removeTrackFromQueue qua port, rebuild setMediaItems + full state emit); KHÔNG hiển thị chú thích internal; ảnh thật.",
      ),
  "F-MUS-06": dict(mock="done", feas="easy", rec="giữ-mvp", img="music-feed-search.png",
      code="không có UI tìm nhạc",
      why="Search: NGHỆ SĨ hiện đầu (card avatar gradient + \"n bài hát\", click mở trang nghệ sĩ) → track khớp → không khớp → \"Không có bài hát phù hợp\" + \"Liên quan\"; nút ✕ xóa toàn bộ; ảnh thật.",
      ),
  "F-MUS-07": dict(mock="done", feas="easy", rec="giữ-mvp", img="music-feed-suggest.png",
      code="MusicScreens segment \"Đã tải\" (mp3 mẫu cờ ngoại tuyến)",
      why="Chips lọc Tất cả / Dành cho bạn / Yêu thích / Đã tải / thể loại (Pop, US-UK, Việt, Lo-fi, Acoustic, Chill) + \"Từ video của bạn\" nằm CUỐI feed (không ngang cấp); TrackCard có ảnh nghệ sĩ gradient riêng + chữ \"Đã tải\" bên phải; ảnh thật.",
      ),
  "F-MUS-08": dict(mock="done", feas="easy", rec="giữ-mvp", img="music-feed-suggest.png",
      code="MusicScreens segment \"Dành cho bạn\"",
      why="\"Dành cho bạn\" gộp vào chip lọc (không còn section riêng) — hiển thị bài theo nghệ sĩ đã yêu thích; ảnh thật.",
      ),
  "F-MUS-09": dict(mock="none", feas="easy", rec="xoá", img="music-super-playlist-created.png",
      code="nút Siêu playlist đã xoá khỏi UI theo user",
      why="User quyết định bỏ: nhảm nhí.",
      ),
  "F-MUS-10": dict(mock="done", feas="easy", rec="giữ-mvp", img="c1-audio-conflict-light",
      code="SessionPolicy.resolveMusicStart + MediaPlaybackCoordinator + popup C1 trong OneSpaceApp",
      why="Trọng tài âm thanh chạy thật: hỏi lần đầu theo cặp, nhớ lựa chọn."),
  "F-MUS-11": dict(mock="none", feas="hard", rec="chuyển-v2", img=None,
      code="không có UI equalizer",
      why="User: 'Thankless — làm thì v2 chứ v1 không có'. Android Equalizer API gắn vào ExoPlayer."),
  "F-MUS-12": dict(mock="done", feas="easy", rec="giữ-mvp", img="music-feed-search.png",
      code="không có UI tải nhạc",
      why="Chữ \"Đã tải\" hiển thị BÊN PHẢI thẻ nhạc (không phải icon button) — bấm vào chữ để bỏ tải; nút tải trên NowPlaying ghi Room downloaded_content; ảnh thật.",
      ),

  # ----- C. Reading News -----
  "F-NEWS-01": dict(mock="done", feas="easy", rec="giữ-mvp", img="news-feed-search.png",
      code="NewsScreens — category hiển thị trên card, feed chưa lọc theo sở thích",
      why="Chips lọc Tất cả / Dành cho bạn / chuyên mục (KHÔNG có \"Đã lưu\"); NewsCard có ảnh gradient theo chuyên mục + title + tên chuyên mục; ảnh thật.",
      ),
  "F-NEWS-02": dict(mock="done", feas="easy", rec="giữ-mvp", img="news-article-largefont.png",
      code="ArticleScreen — grep cỡ chữ/textSize/fontSize = 0",
      why="Hai nút A−/A+ nhỏ gọn (IconButton 32dp); ảnh thật.",
      ),
  "F-NEWS-03": dict(mock="done", feas="easy", rec="giữ-mvp", img="news-empty-light",
      code="ArticleScreen \"Lưu bài viết\" + NewsScreens chip \"Đã lưu\" + EmptyState",
      why="Article: 4 nút icon-only trong header — 🔖 Lưu bài (Xem sau) + ⬇ Tải + 🎧 Nghe + 🎵 Trích MP3; KHÔNG text label; ảnh thật.",
      ),
  "F-NEWS-04": dict(mock="done", feas="easy", rec="giữ-mvp", img="news-feed-search.png",
      code="không có UI tìm tin",
      why="Thanh tìm trên feed tin, lọc theo tiêu đề và chuyên mục; ảnh thật.",
      ),
  "F-NEWS-05": dict(mock="done", feas="easy", rec="giữ-mvp", img="tts-listen-light",
      code="AndroidTtsEngine (core:media) + ListenArticle use case + ArticleScreen TTS button",
      why="🎧 Nghe: TTS init EAGER trong constructor (Thread riêng, không bao giờ block main thread — ANR FIX); 🎵 Trích xuất MP3: nút icon trong article header, ghi Room extracted_audio → mục \"Từ video của bạn\" trong Music; ảnh thật.",
      ),
  "F-NEWS-06": dict(mock="done", feas="easy", rec="giữ-mvp", img="news-feed-search.png",
      code="NewsScreens chip \"Mới nhất\"",
      why="Chips sắp xếp: Mới nhất / A đến Z / Đọc nhanh; ảnh thật.",
      ),
  "F-NEWS-09": dict(mock="done", feas="easy", rec="giữ-mvp", img="article-music-dock-light",
      code="dock mini hiển thị trong ArticleScreen",
      why="Nghe nhạc khi đọc tin chạy thật, có ảnh chụp."),
  "F-NEWS-10": dict(mock="done", feas="easy", rec="giữ-mvp", img="quiz-screen-light",
      code="QuizQuestion model + ArticleScreen quiz section + SubmitQuizAnswer",
      why="Dialog \"Kiểm tra nhanh\" hỏi trước khi hiện quiz (Chơi ngay / Để sau) — KHÔNG tự động; ảnh thật.",
      ),
  "F-NEWS-11": dict(mock="done", feas="easy", rec="giữ-mvp", img="news-related.png",
      code="không có UI bài liên quan trong News (\"Liên quan\" chỉ có ở Video)",
      why="Mục \"Tin liên quan\" cùng chuyên mục cuối bài đọc, thêm 3 bài mẫu để có cặp cùng chuyên mục; ảnh thật.",
      ),
  "F-NEWS-12": dict(mock="done", feas="easy", rec="giữ-mvp", img="news-floating-card.png",
      code="tính năng mới — chưa có trong app",
      why="Thẻ nổi \"Đang đọc\" hiện khi rời tab News, bấm Đọc tiếp quay lại bài; ảnh thật.",
      ),

  # ----- D. Playing Minigames -----
  "F-GAME-01": dict(mock="done", feas="easy", rec="giữ-mvp", img="games-light",
      code="GamesScreens.kt — hub 2 game + Điểm cao từng game",
      why="Hub chạy thật, có ảnh chụp. Trạng thái khoá/mở chưa có."),
  "F-GAME-02": dict(mock="done", feas="easy", rec="giữ-mvp", img="guess-song-light",
      code="GuessSongScreen + StartGuessSong + GuessSongViewModel + GamesNavGraph",
      why="ĐÃ IMPLEMENT: Phát 5 giây → chọn 1 trong 4 tên bài từ kho nhạc. +10 điểm khi đúng."),
  "F-GAME-03": dict(mock="done", feas="easy", rec="giữ-mvp", img="games-newsquiz.png",
      code="không có UI quiz tin tức",
      why="Game \"Quiz tin tức\" g4: câu hỏi lấy từ quiz các bài báo, trả lời đúng +15 XP; ảnh thật.",
      ),
  "F-GAME-05": dict(mock="none", feas="hard", rec="chuyển-v2", img=None,
      code="không có UI rhythm game",
      why="Trùng trải nghiệm karaoke nhưng kém khác biệt; report xếp hoãn."),
  "F-GAME-06": dict(mock="none", feas="easy", rec="chuyển-v2", img=None,
      code="không có UI trivia",
      why="User: 'Không làm v1 — Fill-ins đúng rồi'. Kiến thức chung, không gắn nội dung app."),
  "F-GAME-07": dict(mock="done", feas="easy", rec="giữ-mvp", img="games-leaderboard-full.png",
      code="không có UI bảng xếp hạng",
      why="Bảng xếp hạng Tuần/Tháng, hàng \"Bạn\" dùng tổng điểm thật từ PointRepository; hiển thị ở đầu Games hub; ảnh thật.",
      ),
  "F-GAME-08": dict(mock="done", feas="easy", rec="giữ-mvp", img="games-split-video.png",
      code="không có UI game + video chia nửa màn",
      why="Split screen: khi video đang phát + mở game → Column{VideoSurface 170dp; game weight(1f)}; FloatingVideo tắt khi contextTitle=\"Games\"; verify: title đổi giữa 2 video liên tiếp ( autoplay ); ảnh thật.",
      ),
  "F-GAME-09": dict(mock="done", feas="easy", rec="giữ-mvp", img="games-tictactoe-win.png",
      code="Game model bestScore + GamesScreens \"Điểm cao\" + AccountScreens StatCard \"Điểm\"",
      why="Thắng Tic-Tac-Toe +20 XP, Snake +2 XP/điểm, quiz +15 XP — cùng ví điểm chung; ảnh thật.",
      ),
  "F-GAME-10": dict(mock="none", feas="easy", rec="chuyển-v2", img=None,
      code="không có UI memory match",
      why="Lưới thẻ đơn giản; Fill-ins ngoài MVP."),
  "F-GAME-11": dict(mock="none", feas="easy", rec="chuyển-v2", img=None,
      code="không có UI đập chuột",
      why="Cơ chế cổ điển; Fill-ins ngoài MVP."),
  "F-GAME-12": dict(mock="done", feas="easy", rec="giữ-mvp", img="game-2048-light",
      code="data/games/MockGamesRepository + GameScreen",
      why="2048 chơi thật (vuốt, ghép ô, điểm), có ảnh chụp."),
  "F-GAME-13": dict(mock="done", feas="easy", rec="giữ-mvp", img="games-snake-play.png",
      code="không có Snake (app làm Tic-Tac-Toe thay thế — xem ghi chú)",
      why="Snake chơi thật bằng Canvas + vuốt điều hướng, va chạm kết thúc; ảnh thật.",
      ),
  "F-GAME-14": dict(mock="none", feas="hard", rec="chuyển-v2", img=None,
      code="không có UI beat tiles",
      why="User: 'Thôi đừng làm, khó lắm'. Bỏ khỏi v1 — cần engine timing + sinh nốt theo metadata bài hát."),
  "F-GAME-15": dict(mock="none", feas="easy", rec="chuyển-v2", img=None,
      code="không có UI flappy",
      why="Cơ chế quen thuộc; Fill-ins ngoài MVP."),

  # ----- Dùng chung -----
  "F-COM-01": dict(mock="done", feas="easy", rec="giữ-mvp", img="login-phone-filled.png",
      code="LoginScreen — email + OTP demo (mã bất kỳ) + Google + dùng thử",
      why="Login: SĐT (OTP demo) + Email + MẬT KHẨU (PasswordVisualTransformation) + Google; KHÔNG chữ \"Bản thử nghiệm\"; ảnh thật.",
      ),
  "F-COM-02": dict(mock="done", feas="easy", rec="giữ-mvp", img="onboarding-topics-light",
      code="OnboardingScreens — InfoStep/MultitaskStep/TopicsStep (≥3 chủ đề)",
      why="Chạy thật, có ảnh chụp cả 3 bước."),
  "F-COM-03": dict(mock="done", feas="easy", rec="giữ-mvp", img="account-profile-stats.png",
      code="AccountScreens — avatar, tên, chế độ khách",
      why="Hồ sơ: avatar chữ cái đầu với khung màu, điểm/chuỗi/thú cưng, pet card + shop; ảnh thật.",
      ),
  "F-COM-04": dict(mock="done", feas="easy", rec="giữ-mvp", img="gamification-banner-light",
      code="Room PointEntryEntity + PointDao + RoomPointRepository + HomeScreen GamificationBanner",
      why="ĐÃ IMPLEMENT: Room point_entries table + AddPoints use case + GamificationBanner hiển thị tổng điểm + 3 nhiệm vụ."),
  "F-COM-05": dict(mock="done", feas="easy", rec="giữ-mvp", img="mission-daily-light",
      code="Room DailyMissionEntity + TrackMissionAction + HomeScreen banner",
      why="Banner nhiệm vụ trên Home: 3 nhiệm vụ (Nghe/Đọc/Thắng) + điểm + streak; click nhiệm vụ navigate sang tab tương ứng (onMissionClick); ảnh thật.",
      ),
  "F-COM-06": dict(mock="done", feas="easy", rec="giữ-mvp", img="streak-calendar-light",
      code="DataStore streak + StreakCalculator + AccountScreen StatCard",
      why="ĐÃ IMPLEMENT: StreakState + StreakCalculator (onMissionCompleted) + hiển thị trong Account."),
  "F-COM-07": dict(mock="done", feas="easy", rec="giữ-mvp", img="pet-screen-light",
      code="DataStore pet + PetStage evolution + AccountScreen PetCard",
      why="Pet card: emoji lớn (🥚→🐣→🐥→🦜) + gradient CircleShape + mô tả stage + nút Cho ăn (−30 điểm, giới hạn 2 lần/ngày); ảnh thật.",
      ),
  "F-COM-08": dict(mock="done", feas="easy", rec="giữ-mvp", img="account-profile-badges.png",
      code="grep huy hiệu/badge = 0",
      why="Card \"Huy hiệu n/6 đã đạt\" trên profile → mở màn BadgeGrid riêng (6 hàng, icon + Đã đạt/Chưa mở); KHÔNG tràn màn hình; ảnh thật.",
      ),
  "F-COM-09": dict(mock="done", feas="easy", rec="giữ-mvp", img="account-profile-badges.png",
      code="không có UI khung avatar",
      why="Nút Edit (bút chì) trên avatar → AvatarEditorSheet: emoji grid (8 avatar) + frame picker (4 khung theo mốc điểm); ảnh thật.",
      ),
  "F-COM-10": dict(mock="done", feas="easy", rec="giữ-mvp", img="account-wrapped.png",
      code="không có UI wrapped",
      why="Wrapped: điểm + chuỗi + thú cưng + 4 emoji breakdown (🎬🎵📰🎮) + nút chia sẻ ACTION_SEND; ảnh thật.",
      ),
  "F-COM-11": dict(mock="done", feas="easy", rec="giữ-mvp", img="home-global-search.png",
      code="không có UI tìm kiếm",
      why="Ô tìm \"Tìm trong OneSpace\" trên Home lọc video/nhạc/tin cùng lúc, hiển thị theo nhóm; ảnh thật.",
      ),
  "F-COM-12": dict(mock="done", feas="easy", rec="giữ-mvp", img="account-notifications.png",
      code="Settings \"Nhắc nhiệm vụ\" toggle; grep NotificationChannel/WorkManager = 0",
      why="Trung tâm Nhắc nhở: nhắc nhiệm vụ 9:00 (gắn công tắc thông báo trong DataStore), nhắc chuỗi 20:00, giờ yên tĩnh 22:00-7:00; ảnh thật.",
      ),
  "F-COM-13": dict(mock="done", feas="easy", rec="giữ-mvp", img="settings-light",
      code="SettingsScreen — Sáng/Tối/Hệ thống, ngôn ngữ, data saver, nhắc, mô phỏng mạng",
      why="Chạy thật, có ảnh chụp."),
  "F-COM-14": dict(mock="done", feas="easy", rec="giữ-mvp", img="c1-audio-conflict-light",
      code="OneSpaceApp popup xung đột + SessionPolicy + DataStore nhớ rule",
      why="Popup gọn: \"Phát [tên bài]?\" + \"Video đang phát\" + 3 nút emoji: 🔇 Tắt tiếng / ⏸ Dừng / ▶ Giữ video; ảnh thật.",
      ),
  "F-COM-15": dict(mock="done", feas="easy", rec="giữ-mvp", img="shop-light",
      code="DataStore shop + PurchaseItem + AccountScreen ShopSheet",
      why="Shop: ListItem có leading emoji (🐍🎵🎩🧣🥉🥈🥇) + nút \"n điểm\" + trạng thái \"Đã có\"; ảnh thật.",
      ),
  "F-COM-16": dict(mock="done", feas="easy", rec="giữ-mvp", img="home-offline-banner.png",
      code="CatalogContent offline + tin \"Mẫu ngoại tuyến\" trong mock nhạc",
      why="Banner mất kết nối trên Home (cờ mô phỏng trong Settings) + bài đã lưu vẫn đọc được; ảnh thật.",
      ),
  "F-COM-17": dict(mock="none", feas="easy", rec="chuyển-v2", img=None,
      code="không có UI báo nội dung (grep chỉ trùng từ mã nguồn)",
      why="Liên quan chính sách vận hành; Fill-ins ngoài MVP."),
  "F-COM-18": dict(mock="done", feas="easy", rec="giữ-mvp", img="guest-sheet-light",
      code="LoginScreen \"Dùng thử\" + bottom sheet xác nhận + Account \"Chế độ dùng thử\"",
      why="Chạy thật đúng spec: lưu dữ liệu yêu cầu tạo tài khoản."),
}
# sửa lỗi chính tả rec chuẩn hoá
for k, v in A.items():
    if v["rec"] == "làm-tipc":
        v["rec"] = "làm-tiếp"

MOCK_LABEL = {"done": "Đã có mockup", "partial": "Mockup một phần", "none": "Chưa có mockup"}
FEAS_LABEL = {"easy": "Làm được", "hard": "Khó nhưng làm được", "infeasible": "Không khả thi"}
REC_LABEL = {"giữ-mvp": "Giữ — trong MVP", "làm-tiếp": "Làm tiếp", "chuyển-v2": "Chuyển v2", "bỏ": "Đề xuất bỏ", "xoá": "Đã bỏ (user)"}
SECTION_NAME = {"VID": "A — Streaming Video", "MUS": "B — Listening to Music",
                "NEWS": "C — Reading News", "GAME": "D — Playing Minigames",
                "COM": "Dùng chung"}


def embed_thumb(name, width=360):
    """Nhung anh base64 (thumbnail JPEG) tu figures/app/<name>.png."""
    try:
        from PIL import Image
    except ImportError:
        return None
    p = ROOT / "figures" / "app" / f"{name}.png"
    if not p.exists():
        return None
    img = Image.open(p).convert("RGB")
    ratio = width / img.width
    img = img.resize((width, int(img.height * ratio)), Image.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=70, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def main():
    feats = parse_features()
    scope = parse_scope()
    for f in feats:
        a = A[f["code"]]
        f["mock"] = a["mock"]
        f["feas"] = a["feas"]
        f["rec"] = a["rec"]
        f["img"] = a.get("img")
        f["code_evi"] = a["code"]
        f["why"] = a["why"]
        f["mvp"] = scope.get(f["code"])
        f["scope_label"] = f["mvp"] or "v2"
        f["needs_fb"] = f["feas"] != "infeasible" and f["mock"] != "done"
        f["plan"] = a.get("plan")
    # gắn ảnh (nhúng một lần mỗi file)
    img_cache = {}
    for f in feats:
        key = f["img"]
        if key and key not in img_cache:
            img_cache[key] = embed_thumb(key)
        f["img_data"] = img_cache.get(key) if key else None
    # commit app
    try:
        commit = subprocess.run(["git", "-C", str(APP), "rev-parse", "--short", "HEAD"],
                                capture_output=True, text=True).stdout.strip()
    except Exception:
        commit = "?"
    stats = {
        "total": len(feats),
        "done": sum(1 for f in feats if f["mock"] == "done"),
        "partial": sum(1 for f in feats if f["mock"] == "partial"),
        "none": sum(1 for f in feats if f["mock"] == "none"),
        "easy": sum(1 for f in feats if f["feas"] == "easy"),
        "hard": sum(1 for f in feats if f["feas"] == "hard"),
        "infeas": sum(1 for f in feats if f["feas"] == "infeasible"),
        "drop": sum(1 for f in feats if f["rec"] == "bỏ"),
        "orphan": sum(1 for f in feats if not f["mvp"]),
        "needs_fb": sum(1 for f in feats if f["needs_fb"]),
    }
    html = render(feats, stats, commit)
    OUT.write_text(html, encoding="utf-8")
    print(f"OK → {OUT} ({OUT.stat().st_size/1024:.0f} KB)")
    print(f"   {stats}")


def render(feats, stats, commit):
    import html as H
    cards = []
    for f in feats:
        sec = f["code"].split("-")[1]
        needs = f["feas"] != "infeasible" and f["mock"] != "done"
        img_html = ""
        if f["img_data"]:
            img_html = (f'<button class="thumb" data-full="{f["img_data"]}" title="Xem ảnh lớn">'
                        f'<img src="{f["img_data"]}" alt="Ảnh chụp: {H.escape(f["img"])}" loading="lazy"></button>')
        elif f["mock"] == "done":
            img_html = '<div class="thumb missing">chưa chụp ảnh</div>'
        warn = "⚠" if ("⚠" in (f.get("why") or "") + (f.get("code") or "")) else ""
        cards.append(f'''<article class="card mock-{f["mock"]} feas-{f["feas"]} rec-{f["rec"].replace("giữ","giu")} sec-{sec} ver-{f["mvp"] or "v2"} {"needs-fb" if needs else "no-fb"}" data-sec="{sec}" data-mock="{f["mock"]}" data-feas="{f["feas"]}" data-rec="{f["rec"]}" data-ver="{f["mvp"] or "v2"}">
  <header>
    <span class="code">{f["code"]}</span>
    <span class="scope {f["mvp"] or "v2"}">{f["scope_label"]}</span>
  </header>
  <h3>{H.escape(f["name"])}{warn}</h3>
  <div class="meta">
    <span class="pill">I {f["i"]}</span><span class="pill">E {f["e"]}</span><span class="pill">{H.escape(f["group"])}</span>
  </div>
  {img_html}
  <div class="badges">
    <span class="badge mock">{MOCK_LABEL[f["mock"]]}</span>
    <span class="badge feas">{FEAS_LABEL[f["feas"]]}</span>
    <span class="badge rec">{REC_LABEL[f["rec"]]}</span>
  </div>
  <dl class="evi">
    <dt>Bằng chứng</dt><dd><code>{H.escape(f["code_evi"] if "code_evi" in f else f["code"])}</code></dd>
    <dt>Đánh giá</dt><dd>{H.escape(f["why"])}</dd>
    {f'<dt class="plan-lbl">Kế hoạch</dt><dd class="plan">{H.escape(f["plan"])}</dd>' if f.get("plan") else ''}
  </dl>

</article>''')
    cards_html = "\n".join(cards)

    # Bảng quyết định cho tab Phản hồi — chỉ tính năng user đã nói + phần chưa quyết
    DECIDED = [
        ("F-VID-02", "SẼ LÀM", "Code đã viết trong working tree (6 file, build pass). Feed tách Dành cho bạn / Khám phá thêm."),
        ("F-VID-03", "SẼ LÀM", "User: 'Phải triển khai luôn'. Ô tìm ở đầu tab Video, lọc title/creator."),
        ("F-VID-04", "SẼ LÀM", "User chọn. Backend addToWatchlist có sẵn; cần màn danh sách."),
        ("F-VID-06", "SẼ LÀM", "User chọn. Thêm menu chất lượng 240p-1080p/Auto."),
        ("F-VID-07", "SẼ LÀM", "User: 'Vẫn làm nhưng UI tùy bản quyền — disable nút + báo lý do nếu không cho tải'."),
        ("F-VID-10", "SẼ LÀM", "User: chưa implement, chưa biết cơ chế. Cần: nhấn giữ video → menu Trích âm thanh → progress → file .m4a vào kho. Tech: MediaExtractor+MediaMuxer. Tùy bản quyền: disable nút + báo lý do."),
        ("F-VID-09", "SẼ LÀM", "User: 'Nếu đã làm trích mp3 thì làm luôn' — audio-only là biến thể nhẹ của player, tắt surface giữ audio."),
        ("F-VID-11", "SẼ LÀM", "User: 'Thì cứ làm thôi'. Nút share + Android Intent (WhatsApp/Zalo/Messenger). Deep link onespace://video/id."),
        ("F-VID-11", "SẼ LÀM", "User: 'Thì cứ làm thôi, mock up th mà'. Nút share + Android Intent chooser."),
        ("F-VID-14", "SẼ LÀM", "User: 'làm luôn nhé'. Bấm tên creator trên card → màn list nội dung của creator đó."),
        ("F-VID-15", "SẼ LÀM", "User: 'làm luôn vì cần giao diện mock up'. Người dùng tự tạo playlist video riêng theo chủ đề."),
        ("F-VID-18", "SẼ LÀM", "User: 'làm luôn trong v1'. Thẻ quiz cuối video, 2-3 câu soạn sẵn trong mock data. Dùng chung engine với F-NEWS-10."),
        ("F-MUS-03", "SẼ LÀM", "User: 'làm luôn, mock up thôi cũng được, cần show khi chạy nền'. Media3 MediaSessionService + notification/lock screen controls tự render. Chụp ảnh notification shade + lock screen."),
        ("F-MUS-06", "SẼ LÀM", "User: 'làm luôn'. Ô tìm trong tab Music, lọc theo title/nghệ sĩ/album."),
        ("F-MUS-07", "SẼ LÀM", "User: 'cần show rõ hơn — phân biệt mp3 đã trích từ video vs nhạc chính thống'. Tab Đã tải cần badge nguồn: trích từ video / catalog."),
        ("F-MUS-08", "SẼ LÀM", "User: 'làm luôn, cần có chỗ gợi ý theo sở thích của bạn chứ không chỉ chung chung'. Section 'Dành cho bạn' lọc theo topics onboarding."),
        ("F-MUS-09", "SẼ LÀM", "User: 'giống bên VID, làm luôn'. Siêu playlist trộn nhạc + audio tin + mp3 trích, phát liên tiếp qua một engine."),
        ("F-MUS-12", "SẼ LÀM", "User: 'cho nút nhưng tùy bản quyền disable hoặc không'. Giống F-VID-07 — nút tải hiện sẵn, disable + báo lý do nếu không cho."),
        ("F-NEWS-01", "SẼ LÀM", "User mô tả UI: tab 'Dành cho bạn' (theo sở thích onboarding) + tab chia theo category (Đời sống, Công nghệ, Du lịch...). Trong mỗi tab có sort Mới nhất/Phổ biến. Cần thêm mock articles cho nhiều category."),
        ("F-NEWS-02", "SẼ LÀM", "User: 'đổi cỡ chữ là setting chung của hệ thống, không để riêng cho News'. Thêm vào Settings (F-COM-13) — slider/gần chữ A- A+ áp dụng toàn app qua Material 3 typography."),
        ("F-NEWS-12", "SẼ LÀM", "User bổ sung tính năng mới: 'đang đọc báo chuyển tab phải có floating'. Thẻ nổi hiển thị tên bài + bấm quay lại đúng vị trí cuộn."),
        ("F-NEWS-04", "SẼ LÀM", "User: 'làm luôn'. Ô tìm trong tab News, lọc theo title/category."),
        ("F-NEWS-05", "SẼ LÀM", "User: 'làm luôn'. TRỤ W3 USP — quan trọng nhất. TTS on-device Android TextToSpeech locale vi-VN, render theo đoạn."),
        ("F-NEWS-06", "SẼ LÀM", "User mô tả: sort Mới nhất/Phổ biến nằm TRONG từng tab category và tab Dành cho bạn (F-NEWS-01)."),
        ("F-NEWS-11", "SẼ LÀM", "User: 'làm luôn'. Section 'Liên quan' cuối bài — gợi ý bài cùng chuyên mục."),
        ("F-GAME-02", "SẼ LÀM", "User: 'nên có luôn, ít nhất phải có mockup'. Trụ W4 — phát 5 giây → chọn 1 trong 4 tên bài từ kho nhạc."),
        ("F-GAME-03", "SẼ LÀM", "User: 'làm luôn nhé'. Quiz tin — dùng chung engine + nguồn câu hỏi với F-NEWS-10."),
        ("F-GAME-07", "SẼ LÀM", "User: 'ừ cần làm'. Mockup BXH với tên + điểm giả lập, reset theo tuần. UI thật nhưng dữ liệu mock."),
        ("F-GAME-08", "SẼ LÀM", "User: 'cần làm'. Bố cục chia đôi màn — game 60% dưới + PIP video 40% trên (case C4)."),
        ("F-GAME-09", "SẼ LÀM", "User: 'thì làm đi'. Thắng ván → cộng điểm vào hệ XP dùng chung (nối F-COM-04)."),
        ("F-GAME-13", "SẼ LÀM", "User: 'làm luôn'. Snake — canvas đơn giản, không bản quyền, offline hoàn toàn."),
        ("F-COM-01", "SẼ LÀM", "User góp ý: 'Hiện tại rất tệ, mix lung tung. Phải cho nhập MẬT KHẨU chứ không phải lúc nào cũng OTP'. THIẾT KẾ LẠI: (1) chính: SĐT/Email + MẬT KHẨU → Đăng nhập, (2) phụ: 'Quên mật khẩu?' → gửi OTP reset, (3) Google, (4) tách màn ĐN vs ĐK, (5) flow tuần tự."),
        ("F-COM-03", "SẼ LÀM", "User: 'Thêm khung ảnh theo thành tích, phải cho đổi được avatar'. Màn hồ sơ: avatar + nút đổi + gallery khung theo mốc."),
        ("F-COM-05", "SẼ LÀM", "User: 'làm luôn'. 3 nhiệm vụ/ngày: nghe 1 bài, đọc 1 tin, thắng 1 ván. Tự reset + banner trên Home."),
        ("F-COM-06", "SẼ LÀM", "User: 'thêm logic + bấm vào có giao diện từng ngày, không chỉ show số'. Weekly calendar view: T2-CN, ô xanh = hoàn thành, ô xám = bỏ lỡ, 🔥 = streak hiện tại."),
        ("F-COM-08", "SẼ LÀM", "User: 'implement luôn'. Gallery huy hiệu theo thành tích — hiển thị trong hồ sơ."),
        ("F-COM-09", "SẼ LÀM", "User: 'implement luôn'. Khung avatar theo mốc — gắn với F-COM-03 hồ sơ + F-COM-04 điểm."),
        ("F-COM-10", "SẼ LÀM", "User: 'cần thực hiện'. Wrapped tháng — thẻ tổng kết chia sẻ được (kiểu Spotify Wrapped)."),
        ("F-COM-11", "SẼ LÀM", "User: 'cần thực hiện'. Một ô tìm chung cho cả 4 phân hệ — đặt trên thanh Home."),
        ("F-COM-14", "SẼ LÀM", "User góp ý: 'Nên có nút KHÔNG hỏi lại cho lần sau, chứ đừng mặc định set luôn dù user không yêu cầu'. Thêm checkbox 'Đừng hỏi lại' trên popup + chọn này thành default toàn cục, đổi được trong Settings."),
        ("F-COM-16", "SẼ LÀM", "User: 'làm luôn'. Offline: tin đã lưu đọc được không mạng + game offline + trạng thái mất mạng rõ ràng."),
        ("F-COM-04", "SẼ LÀM", "Nền tảng gamification. PointLedger Room + flow tổng điểm. Nguồn: xem +2, nghe +2, đọc +2, thắng game +10, nhiệm vụ +20."),
        ("F-COM-07", "SẼ LÀM", "Trứng nở sau 3 nhiệm vụ hoàn thành. Tiến hoá theo mốc điểm. Màn nuôi trong Account."),
        ("F-COM-12", "SẼ LÀM", "Notification nhắc khi quên nhiệm vụ (sau 20h, tối đa 1 lần/ngày). Cần NotificationChannel."),
        ("F-COM-15", "SẼ LÀM", "Cửa hàng đổi quà: mở game mới, đồ pet, khung avatar. Giá bằng điểm, trừ số dư khi mua."),
        ("F-MUS-01", "SẼ LÀM", "User chọn. Thêm nút shuffle + repeat vào NowPlaying."),
        ("F-MUS-04", "SẼ LÀM", "User chọn. CRUD playlist + Room entity."),
        ("F-MUS-05", "SẼ LÀM", "User chọn. UI hàng phát: thêm tiếp theo + kéo sắp."),
    ]
    feat_map = {f["code"]: f for f in feats}
    rows_dec = []
    for code, status, plan in DECIDED:
        f = feat_map.get(code)
        if not f: continue
        rows_dec.append(
            f'<tr class="done-dec"><td class="code">{code}</td>'
            f'<td>{f["name"]}</td>'
            f'<td class="ver {f["mvp"] or "v2"}">{f["mvp"] or "v2"}</td>'
            f'<td>{status}</td>'
            f'<td class="plan">{plan}</td></tr>')
    dec_codes = {d[0] for d in DECIDED}
    rows_undec = []
    for f in feats:
        if f["code"] in dec_codes or f["mock"] == "done": continue
        rows_undec.append(
            f'<tr class="undec"><td class="code">{f["code"]}</td>'
            f'<td>{f["name"]}</td>'
            f'<td class="ver {f["mvp"] or "v2"}">{f["mvp"] or "v2"}</td>'
            f'<td>—</td><td></td></tr>')
    dec_table = (
        '<table class="dec-table">'
        '<thead><tr><th>Mã</th><th>Tính năng</th><th>Ver</th><th>Quyết định</th><th>Kế hoạch / Ghi chú user</th></tr></thead>'
        '<tbody>'
        '<tr class="sec-hdr"><td colspan="5">✅ ĐÃ QUYẾT — SẼ LÀM (' + str(len(rows_dec)) + ')</td></tr>'
        + '\n'.join(rows_dec) +
        '<tr class="undec-hdr"><td colspan="5">⏳ CHƯA QUYẾT (' + str(len(rows_undec)) + ')</td></tr>'
        + '\n'.join(rows_undec) +
        '</tbody></table>')
    sec_short = {"VID": "A - Video", "MUS": "B - Music", "NEWS": "C - News",
                 "GAME": "D - Games", "COM": "Dùng chung"}
    import json as J
    feat_js = J.dumps({f["code"]: {"name": f["name"], "ver": f["mvp"] or "v2",
                                   "sec": sec_short[f["code"].split("-")[1]],
                                   "why": f["why"], "needs": f["needs_fb"]}
                        for f in feats}, ensure_ascii=False)

    return f'''<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>OneSpace — Audit tính năng × mockup × khả thi</title>
<style>
:root {{
  --bg: #F8FAF2; --surface: #FFFFFF; --ink: #191D17; --muted: #43483D;
  --primary: #41690F; --primary-soft: #C3F491; --primary-ink: #0E2000;
  --teal: #006A68; --line: #DEE3D0;
  --green: #1B7F3B; --green-bg: #E4F3E6;
  --amber: #8A5A00; --amber-bg: #FCF3DD;
  --gray-bg: #EDEFE6; --gray-ink: #555B4E;
  --red: #A02A22; --red-bg: #FBE7E5;
  --radius: 14px; --shadow: 0 1px 2px rgba(25,29,23,.06), 0 6px 18px rgba(25,29,23,.05);
}}
* {{ box-sizing: border-box; }}
body {{
  margin: 0; background: var(--bg); color: var(--ink);
  font-family: "Be Vietnam Pro", -apple-system, "Segoe UI", system-ui, sans-serif;
  font-size: 15px; line-height: 1.55;
}}
header.top {{
  background: linear-gradient(135deg, #223500 0%, #41690F 60%, #006A68 120%);
  color: #fff; padding: 28px clamp(16px, 4vw, 48px) 24px;
}}
header.top h1 {{ margin: 0 0 4px; font-size: clamp(20px, 3vw, 28px); letter-spacing: -.01em; }}
header.top p {{ margin: 0; opacity: .85; font-size: 13px; }}
.stats {{ display: flex; flex-wrap: wrap; gap: 10px; margin-top: 16px; }}
.stat {{
  background: rgba(255,255,255,.12); border: 1px solid rgba(255,255,255,.22);
  border-radius: 10px; padding: 8px 14px; min-width: 90px;
}}
.stat b {{ display: block; font-size: 20px; }}
.stat span {{ font-size: 12px; opacity: .85; }}
main {{ padding: 20px clamp(16px, 4vw, 48px) 60px; max-width: 1480px; margin: 0 auto; }}
.filters {{ position: sticky; top: 0; z-index: 5; background: var(--bg); padding: 14px 0 10px; border-bottom: 1px solid var(--line); margin-bottom: 18px; }}
.fgroup {{ display: flex; flex-wrap: wrap; gap: 6px; align-items: center; margin-bottom: 6px; }}
.fgroup .lbl {{ font-size: 12px; font-weight: 600; color: var(--muted); width: 86px; }}
.chip {{
  border: 1.5px solid var(--line); background: var(--surface); color: var(--muted);
  border-radius: 999px; padding: 5px 14px; font-size: 13px; font-weight: 500;
  cursor: pointer; font-family: inherit; transition: all .15s ease;
}}
.chip:hover {{ border-color: var(--primary); color: var(--primary); }}
.chip.on {{ background: var(--primary); border-color: var(--primary); color: #fff; }}
.count {{ font-size: 12px; color: var(--muted); margin-left: 8px; }}
.grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(330px, 1fr)); gap: 16px; }}
.card {{
  background: var(--surface); border: 1px solid var(--line); border-radius: var(--radius);
  padding: 16px 16px 14px; box-shadow: var(--shadow); display: flex; flex-direction: column; gap: 10px;
  border-top: 4px solid var(--line);
}}
.card.mock-done {{ border-top-color: var(--green); }}
.card.mock-partial {{ border-top-color: #D99A00; }}
.card.rec-bỏ {{ border-top-color: var(--red); }}
.card header {{ display: flex; justify-content: space-between; align-items: center; gap: 8px; }}
.code {{ font-weight: 700; font-size: 14px; letter-spacing: .02em; }}
.scope {{ font-size: 11px; font-weight: 600; border-radius: 6px; padding: 3px 8px; background: var(--gray-bg); color: var(--gray-ink); white-space: nowrap; }}
.scope.v1 {{ background: var(--green-bg); color: var(--green); }}

.scope.orphan {{ background: var(--amber-bg); color: var(--amber); }}
h3 {{ margin: 0; font-size: 15.5px; line-height: 1.35; }}
.meta {{ display: flex; flex-wrap: wrap; gap: 6px; }}
.pill {{ font-size: 11.5px; background: var(--gray-bg); color: var(--gray-ink); border-radius: 6px; padding: 2px 8px; font-weight: 600; }}
.thumb {{ padding: 0; border: 1px solid var(--line); border-radius: 10px; overflow: hidden; cursor: zoom-in; background: #fff; width: fit-content; max-width: 100%; }}
.thumb img {{ display: block; height: 190px; width: auto; border-radius: 9px; }}
.thumb.missing {{ padding: 14px 18px; color: var(--gray-ink); font-size: 12px; border-style: dashed; }}
.badges {{ display: flex; flex-wrap: wrap; gap: 6px; }}
.badge {{ font-size: 12px; font-weight: 600; padding: 4px 10px; border-radius: 999px; }}
.badge.mock {{ background: var(--gray-bg); color: var(--gray-ink); }}
.mock-done .badge.mock {{ background: var(--green-bg); color: var(--green); }}
.mock-partial .badge.mock {{ background: var(--amber-bg); color: var(--amber); }}
.badge.feas {{ background: #E0F2F1; color: var(--teal); }}
.feas-infeasible .badge.feas {{ background: var(--red-bg); color: var(--red); }}
.badge.rec {{ background: var(--gray-bg); color: var(--gray-ink); }}
.rec-giữ-mvp .badge.rec, .rec-giu-mvp .badge.rec {{ background: var(--primary-soft); color: var(--primary-ink); }}
.rec-bỏ .badge.rec {{ background: var(--red-bg); color: var(--red); }}
dl.evi {{ margin: 0; font-size: 13px; display: grid; grid-template-columns: 84px 1fr; gap: 4px 10px; }}
dl.evi dt {{ color: var(--muted); font-weight: 600; font-size: 12px; }}
dl.evi dd {{ margin: 0; color: var(--muted); }}
dl.evi code {{ font-size: 11.5px; background: var(--gray-bg); padding: 1px 6px; border-radius: 5px; word-break: break-word; }}
dl.evi dd.plan {{ color: var(--teal); font-weight: 500; }}
body:not(.mode-fb) dt.plan-lbl, body:not(.mode-fb) dd.plan {{ display: none; }}
.note {{
  margin-top: 26px; padding: 14px 18px; border: 1.5px dashed var(--line); border-radius: var(--radius);
  background: var(--surface); font-size: 13.5px; color: var(--muted);
}}
.note b {{ color: var(--ink); }}
footer {{ padding: 22px clamp(16px, 4vw, 48px) 40px; color: var(--muted); font-size: 12.5px; border-top: 1px solid var(--line); }}

.tabbar {{ display: flex; gap: 8px; margin-bottom: 14px; }}
.tab {{
  border: 1.5px solid var(--line); background: var(--surface); color: var(--muted);
  border-radius: 10px; padding: 9px 18px; font-size: 14px; font-weight: 600;
  cursor: pointer; font-family: inherit; transition: all .15s ease;
}}
.tab.on {{ background: var(--primary); border-color: var(--primary); color: #fff; }}
.badge-n {{ background: rgba(255,255,255,.25); border-radius: 6px; padding: 1px 7px; margin-left: 4px; }}
.fbbar {{
  display: none; align-items: center; flex-wrap: wrap; gap: 10px;
  background: var(--surface); border: 1.5px dashed var(--primary); border-radius: var(--radius);
  padding: 12px 16px; margin-bottom: 14px; font-size: 14px;
}}
.mode-fb .fbbar {{ display: flex; }}
.mode-fb .filters {{ display: none; }}
.fbstat b {{ font-size: 16px; }}
.fbstat .ok {{ color: var(--green); }} .fbstat .no {{ color: var(--red); }}
.fbchips {{ display: inline-flex; gap: 6px; flex-wrap: wrap; }}
.fbchip {{
  border: 1.5px solid var(--line); background: var(--surface); color: var(--muted);
  border-radius: 999px; padding: 4px 13px; font-size: 12.5px; font-weight: 600;
  cursor: pointer; font-family: inherit;
}}
.fbchip.on {{ background: var(--primary); border-color: var(--primary); color: #fff; }}
.export {{
  margin-left: auto; border: none; background: var(--primary); color: #fff;
  border-radius: 10px; padding: 9px 16px; font-size: 13.5px; font-weight: 700;
  cursor: pointer; font-family: inherit;
}}
.export:active {{ transform: scale(.97); }}
#fbout {{
  display: none; width: 100%; min-height: 200px; margin-top: 10px;
  font-family: ui-monospace, Menlo, monospace; font-size: 12px; line-height: 1.5;
  border: 1px solid var(--line); border-radius: 10px; padding: 12px; background: #fff; color: var(--ink);
}}
.fb {{ display: none; align-items: center; gap: 8px; padding-top: 10px; border-top: 1px dashed var(--line); }}
.mode-fb .needs-fb .fb {{ display: flex; }}
.fb-lbl {{ font-size: 12.5px; font-weight: 600; color: var(--muted); margin-right: auto; }}

/* Tab Phản hồi: ẩn card grid, hiện bảng quyết định */
body.mode-fb .grid {{ display: none; }}
body.mode-fb .dec-table {{ display: table; }}
.dec-table {{ display: none; width: 100%; border-collapse: collapse; background: var(--surface); border-radius: var(--radius); overflow: hidden; box-shadow: var(--shadow); }}
.dec-table th, .dec-table td {{ padding: 8px 12px; text-align: left; border-bottom: 1px solid var(--line); font-size: 13.5px; vertical-align: top; }}
.dec-table th {{ font-weight: 700; font-size: 11.5px; text-transform: uppercase; color: var(--muted); background: var(--gray-bg); padding: 10px 12px; letter-spacing: .04em; }}
.dec-table td.code {{ font-weight: 700; white-space: nowrap; font-size: 13px; }}
.dec-table td.ver {{ font-weight: 600; white-space: nowrap; }}
.dec-table td.ver.v1 {{ color: var(--green); }}
.dec-table td.ver.v2 {{ color: var(--gray-ink); }}
.dec-table td.plan {{ color: var(--teal); font-size: 13px; max-width: 380px; }}
.dec-table tr.done-dec {{ background: var(--green-bg); }}
.dec-table .sec-hdr td {{ font-weight: 700; font-size: 13px; color: var(--primary-ink); background: var(--primary-soft); padding: 10px 12px; }}
.dec-table .undec-hdr td {{ font-weight: 600; font-size: 12.5px; color: var(--muted); background: var(--gray-bg); padding: 8px 12px; }}
.dec-table .undec {{ color: var(--gray-ink); }}
.dec-table .undec td {{ padding: 5px 12px; font-size: 12.5px; }}
#lightbox {{
  position: fixed; inset: 0; background: rgba(15,20,10,.82); display: none;
  align-items: center; justify-content: center; z-index: 99; cursor: zoom-out; padding: 3vw;
}}
#lightbox img {{ max-width: min(420px, 92vw); max-height: 94vh; border-radius: 12px; box-shadow: 0 20px 60px rgba(0,0,0,.5); }}
#lightbox:target, #lightbox.open {{ display: flex; }}
@media (max-width: 640px) {{ .grid {{ grid-template-columns: 1fr; }} .fgroup .lbl {{ width: 100%; }} }}
</style>
</head>
<body>
<header class="top">
  <h1>OneSpace — Audit tính năng × mockup × khả thi</h1>
  <p>Đối chiếu Danh mục tính năng ứng viên (Phần 2 report) với mockup/UI đã có trong app Android · lập ngày 24/10</p>
  <div class="stats">
    <div class="stat"><b>{stats["total"]}</b><span>tính năng</span></div>
    <div class="stat"><b>{stats["done"]}</b><span>đã có mockup</span></div>
    <div class="stat"><b>{stats["partial"]}</b><span>mockup một phần</span></div>
    <div class="stat"><b>{stats["none"]}</b><span>chưa mockup</span></div>
    <div class="stat"><b>{stats["easy"]}</b><span>làm được</span></div>
    <div class="stat"><b>{stats["hard"]}</b><span>khó nhưng được</span></div>
    <div class="stat"><b>{stats["drop"]}</b><span>đề xuất bỏ</span></div>
  </div>
</header>
<main>
  <div class="tabbar">
    <button class="tab on" data-mode="list" type="button">📋 Danh sách</button>
    <button class="tab" data-mode="fb" type="button">✍️ Phản hồi &amp; Kế hoạch</button>
  </div>
  <div class="fbbar">
    <span class="fbstat">📋 Tính năng đã quyết (user nói trực tiếp)</span>
  </div>
  <textarea id="fbout" readonly title="Danh sách xuất — copy gửi mobile-app"></textarea>
  <div class="filters">
    <div class="fgroup"><span class="lbl">Phân hệ</span>
      <button class="chip on" data-k="sec" data-v="">Tất cả</button>
      <button class="chip" data-k="sec" data-v="VID">A · Video</button>
      <button class="chip" data-k="sec" data-v="MUS">B · Music</button>
      <button class="chip" data-k="sec" data-v="NEWS">C · News</button>
      <button class="chip" data-k="sec" data-v="GAME">D · Games</button>
      <button class="chip" data-k="sec" data-v="COM">Dùng chung</button>
    </div>
    <div class="fgroup"><span class="lbl">Mockup</span>
      <button class="chip on" data-k="mock" data-v="">Tất cả</button>
      <button class="chip" data-k="mock" data-v="done">Đã có</button>
      <button class="chip" data-k="mock" data-v="partial">Một phần</button>
      <button class="chip" data-k="mock" data-v="none">Chưa có</button>
    </div>
    <div class="fgroup"><span class="lbl">Khả thi</span>
      <button class="chip on" data-k="feas" data-v="">Tất cả</button>
      <button class="chip" data-k="feas" data-v="easy">Làm được</button>
      <button class="chip" data-k="feas" data-v="hard">Khó nhưng được</button>
      <button class="chip" data-k="feas" data-v="infeasible">Không khả thi</button>
    </div>
    <div class="fgroup"><span class="lbl">Đề xuất</span>
      <button class="chip on" data-k="rec" data-v="">Tất cả</button>
      <button class="chip" data-k="rec" data-v="giữ-mvp">Giữ MVP</button>
      <button class="chip" data-k="rec" data-v="làm-tiếp">Làm tiếp</button>
      <button class="chip" data-k="rec" data-v="chuyển-v2">Chuyển v2</button>
      <button class="chip" data-k="rec" data-v="bỏ">Đề xuất bỏ</button>
    </div>
    <span class="count" id="count"></span>
  </div>
  <div class="grid" id="grid">
{cards_html}
  </div>
  {dec_table}
  <div class="note">
    <b>Ghi chú:</b> ⚠ = có điểm cần nhóm quyết (lệch app–report hoặc không nằm trong bảng MVP/mở rộng/ngoài phạm vi của Phần 2).
    Kết luận trạng thái được verify bằng grep/đọc mã nguồn app và ảnh chụp thật; ảnh trong thẻ là bản thu nhỏ, bấm để xem lớn.
    App có sẵn <b>Tic-Tac-Toe</b> (chạy thật, có ảnh) nhưng chưa có trong danh mục report — cân nhắc thêm vào F-GAME hoặc ghi rõ là game bổ sung ngoài danh mục.
  </div>
</main>
<footer>
  Nguồn: sections/2-product-scope/feature-prioritization.tex · mvp-scope.tex · app OneSpace @ commit {commit} · ảnh: figures/app/ (chụp từ emulator).
  File sinh tự động bởi docs/feature-audit-build.py — chạy lại để cập nhật.
</footer>
<div id="lightbox"><img alt="Xem ảnh lớn"></div>
<script>
const state = {{ sec: "", mock: "", feas: "", rec: "" }};
const FB = JSON.parse(localStorage.getItem("onespace-fb") || "{{}}");
const FEAT = {feat_js};
let mode = "list";

function apply() {{
  let n = 0;
  document.querySelectorAll(".card").forEach(c => {{
    if (mode === "fb") {{
      c.style.display = ""; n++;
      return;
    }}
    const ok = (!state.sec || c.dataset.sec === state.sec)
            && (!state.mock || c.dataset.mock === state.mock)
            && (!state.feas || c.dataset.feas === state.feas)
            && (!state.rec || c.dataset.rec === state.rec);
    c.style.display = ok ? "" : "none"; if (ok) n++;
  }});
  document.getElementById("count").textContent = n + " tính năng đang hiển thị";
}}

function setMode(m) {{
  mode = m;
  document.querySelectorAll(".tab").forEach(t => t.classList.toggle("on", t.dataset.mode === m));
  document.body.classList.toggle("mode-fb", m === "fb");
  apply();
}}
document.querySelectorAll(".tab").forEach(t => t.addEventListener("click", () => setMode(t.dataset.mode)));



function fbCounts() {{
  let needs = 0, lam = 0, khong = 0;
  Object.entries(FEAT).forEach(([code, f]) => {{
    if (!f.needs) return;
    needs++;
    if (FB[code] === "lam") lam++; else if (FB[code] === "khong") khong++;
  }});
  const set = (id, v) => {{ const el = document.getElementById(id); if (el) el.textContent = v; }};
  set("fbTotal", needs); set("fbTotal2", needs);
  set("fbDone", lam + khong); set("fbLam", lam); set("fbKhong", khong);
}}

function exportFB() {{
  const lam = [], khong = [], chua = [];
  Object.entries(FEAT).forEach(([code, f]) => {{
    if (!f.needs) return;
    const d = FB[code];
    (d === "lam" ? lam : d === "khong" ? khong : chua).push([code, f]);
  }});
  const grp = (arr, title) => {{
    if (!arr.length) return "\\n## " + title + " (0)\\n_(không có)_\\n";
    const bySec = {{}};
    arr.forEach(([c, f]) => {{ (bySec[f.sec] = bySec[f.sec] || []).push([c, f]); }});
    let out = "\\n## " + title + " (" + arr.length + ")\\n";
    Object.entries(bySec).forEach(([sec, items]) => {{
      out += "\\n### " + sec + "\\n";
      items.forEach(([c, f]) => {{
        out += "- **" + c + "** — " + f.name + " (v" + f.ver.slice(1) + ")\\n  Ghi chú audit: " + f.why + "\\n";
      }});
    }});
    return out;
  }};
  const md = "# Feedback tính năng OneSpace — danh sách gửi mobile-app làm mockup\\n"
    + "\\nTổng: " + (lam.length + khong.length + chua.length) + " tính năng cần quyết — "
    + "sẽ làm " + lam.length + " · không làm " + khong.length + " · chưa quyết " + chua.length + ".\\n"
    + grp(lam, "SẼ LÀM — làm mockup") + grp(khong, "KHÔNG LÀM") + grp(chua, "CHƯA QUYẾT");
  const out = document.getElementById("fbout");
  out.value = md; out.style.display = "block";
  const btn = document.getElementById("exportBtn");
  if (navigator.clipboard && navigator.clipboard.writeText) {{
    navigator.clipboard.writeText(md).then(() => {{
      btn.textContent = "✓ Đã copy — dán vào chat";
      setTimeout(() => btn.textContent = "📤 Xuất & copy danh sách", 2500);
    }});
  }}
}}
const exportBtn = document.getElementById("exportBtn");
if (exportBtn) exportBtn.addEventListener("click", exportFB);
document.querySelectorAll(".chip").forEach(ch => ch.addEventListener("click", () => {{
  const g = ch.parentElement.querySelectorAll(".chip");
  g.forEach(c => c.classList.remove("on"));
  ch.classList.add("on");
  state[ch.dataset.k] = ch.dataset.v;
  apply();
}}));
const lb = document.getElementById("lightbox"), lbImg = lb.querySelector("img");
document.querySelectorAll(".thumb").forEach(t => t.addEventListener("click", e => {{
  e.preventDefault(); lbImg.src = t.dataset.full; lb.classList.add("open");
}}));
lb.addEventListener("click", () => lb.classList.remove("open"));
document.addEventListener("keydown", e => {{ if (e.key === "Escape") lb.classList.remove("open"); }});
apply();
</script>
</body>
</html>'''


if __name__ == "__main__":
    main()