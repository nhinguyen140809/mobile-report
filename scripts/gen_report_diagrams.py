# -*- coding: utf-8 -*-
"""Sinh các .tex lặp lại của báo cáo: 12 bảng đặc tả use case, 6 activity diagram,
6 bảng mô tả/kích thích state-chart. Chạy: python3 scripts/gen_report_diagrams.py"""
import io, os, unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def w(path, text):
    text = unicodedata.normalize('NFC', text)
    text = text.replace('\u2212', '$- $').replace('\u2194', '$\\leftrightarrow$')
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with io.open(full, 'w', encoding='utf-8') as f:
        f.write(text)
    print('wrote', path, len(text.splitlines()), 'lines')

# ============================================================
# 1) USE CASE SPECS — 12 bảng theo mẫu sách
# ============================================================
SPEC_HEADER = r"""\subsubsection{Đặc tả chi tiết các use case mục tiêu}

Mỗi use case mục tiêu được đặc tả theo khuôn chín mục: tác nhân, mô tả, tiên/hậu điều kiện,
sự kiện kích hoạt, luồng chuẩn, luồng thay thế và ngoại lệ. Các bảng dưới đây là nguồn cho
ma trận truy vết (mục~\ref{sec:traceability}) và cho các sơ đồ activity, sequence ở các chương sau.
"""

SPECS = [
dict(code='UC-01', name='Vào ứng dụng và chọn sở thích',
 actor='Người dùng',
 desc='Người dùng mở ứng dụng lần đầu, xem ba màn giới thiệu giá trị, chọn tối thiểu ba chủ đề quan tâm hoặc bỏ qua; Home sau đó đề xuất nội dung theo lựa chọn.',
 pre='Ứng dụng vừa được cài và chưa hoàn tất onboarding.',
 post='Sở thích được lưu vào DataStore; tab Home hiển thị đề xuất theo chủ đề đã chọn.',
 trig='Người dùng mở ứng dụng lần đầu tiên.',
 flow=['Ứng dụng kiểm tra trạng thái onboarding và hiển thị ba màn giới thiệu giá trị.',
       'Người dùng vuốt qua các màn giới thiệu.',
       'Hệ thống hiển thị lưới chủ đề của cả bốn phân hệ.',
       'Người dùng chọn tối thiểu ba chủ đề hoặc bấm bỏ qua.',
       'Hệ thống lưu lựa chọn và mở Home với đề xuất theo chủ đề.'],
 alt=['3a. Chọn chưa đủ ba chủ đề: nút “Bắt đầu” ở trạng thái khoá kèm nhắc cần chọn thêm.',
      '4a. Bấm bỏ qua: hệ thống dùng danh sách chủ đề mặc định.'],
 exc=['5a. Không ghi được tùy chọn: ứng dụng dùng đề xuất mặc định cho phiên hiện tại và ghi lại cảnh báo.']),
dict(code='UC-02', name='Xem video',
 actor='Người dùng',
 desc='Người dùng chọn một video trong feed, xem và điều khiển trình phát; khi rời màn hình, video chuyển thành cửa sổ nổi và tiếp tục phát.',
 pre='Ứng dụng đang mở feed Video; thiết bị có kết nối mạng.',
 post='Video phát đúng vị trí đã lưu; trạng thái phiên được giữ khi chuyển phân hệ.',
 trig='Người dùng chạm một thẻ video trong feed.',
 flow=['Hệ thống đọc vị trí xem đã lưu (checkpoint mỗi 3 giây) của video.',
       'Nếu nhạc đang phát, hệ thống hỏi hai lựa chọn kèm ô “Không hỏi lại” (X0).',
       'Trình phát mở stream tại vị trí đã lưu và phát trong tối đa 2 giây.',
       'Người dùng điều khiển dừng, tua, tốc độ, chất lượng, âm lượng, toàn màn hình.',
       'Khi rời màn hình, video chuyển thành cửa sổ nổi và tiếp tục phát (X1).',
       'Chạm “Mở rộng” đưa người dùng về trình phát đúng vị trí.'],
 alt=['4a. Đóng cửa sổ nổi: video dừng, vị trí được lưu và thêm vào Xem sau.',
      '4b. Tab đích là Home: video phát trong card của feed, không mở cửa sổ nổi.',
      '5a. Video kết thúc: hiện lời mời quiz cuối video (X3).'],
 exc=['3a. Lỗi mở stream: hiển thị “Không phát được video” kèm nút Thử lại, giữ nguyên vị trí.',
      '3b. Mất mạng giữa chừng: khung hình dừng, hệ thống tự thử lại trong 5--15 giây.']),
dict(code='UC-03', name='Nghe nhạc',
 actor='Người dùng',
 desc='Người dùng chọn bài từ thư viện, điều khiển phát đầy đủ; dock mini hiển thị trên mọi màn hình chính và hàng đợi được quản lý ngay trên trình phát.',
 pre='Ứng dụng đang mở feed Nhạc.',
 post='Bài hát đang phát hoặc đã dừng; hàng đợi được cập nhật.',
 trig='Người dùng chạm một bài hát trong feed hoặc danh sách phát.',
 flow=['Hệ thống nạp bài hát và hàng đợi tương ứng.',
       'Nếu video đang phát, hệ thống phân xử âm thanh theo quy tắc đã lưu hoặc hỏi (X0).',
       'Bộ phát âm thanh bắt đầu phát; dock mini hiện trên mọi tab trừ màn Now Playing.',
       'Người dùng điều khiển phát/dừng, chuyển bài, tua, tốc độ, thứ tự phát.',
       'Mở rộng dock để quản lý hàng đợi: thêm, xoá, kéo đổi thứ tự.'],
 alt=['2a. Chưa có quy tắc: popup hai lựa chọn như UC-02 và ghi nhớ nếu được tích.',
      '4a. Đóng dock: dừng phát, cho hoàn tác trong 4--10 giây.'],
 exc=['3a. Lỗi stream: hiển thị thông báo, giữ hàng đợi để thử lại.']),
dict(code='UC-04', name='Đọc tin',
 actor='Người dùng',
 desc='Người dùng đọc bài trong trình đọc sạch, chỉnh cỡ chữ, lưu bài để đọc sau; có thể nghe thay vì đọc (X4) hoặc làm quiz cuối bài (X5).',
 pre='Ứng dụng đang mở feed Tin tức.',
 post='Bài được đọc xong hoặc lưu lại; nhiệm vụ đọc được cập nhật.',
 trig='Người dùng chạm một bài trong feed.',
 flow=['Hệ thống mở trình đọc với tiêu đề, ảnh và nội dung.',
       'Người dùng đọc và có thể tăng/giảm cỡ chữ (A−/A+).',
       'Người dùng lưu bài hoặc bấm “Nghe tin” (X4).',
       'Khi đọc hết hoặc ở lại 20 giây, nhiệm vụ đọc được tính một lần.',
       'Hệ thống gợi ý “Kiểm tra nhanh” nếu bài có quiz (X5).'],
 alt=['3a. Bấm “Nghe tin”: nhạc tạm dừng nhường; audio phát có thanh tiến trình và nút dừng.',
      '5a. Bài không có quiz: không hiện lời mời.'],
 exc=['1a. Bài không tải được: hiển thị trạng thái lỗi kèm nút Thử lại.']),
dict(code='UC-05', name='Chơi minigame',
 actor='Người dùng',
 desc='Người dùng chọn một trong sáu minigame, chơi theo luật của game; kết thúc ván được cộng điểm và cập nhật nhiệm vụ, thử thách hằng ngày.',
 pre='Ứng dụng đang mở tab Trò chơi.',
 post='Điểm được cộng, kỷ lục và nhiệm vụ được cập nhật.',
 trig='Người dùng chọn một game trong hub.',
 flow=['Hệ thống kiểm tra trạng thái mở khoá của game.',
       'Game khởi tạo ván mới theo luật riêng.',
       'Người dùng chơi; game phát âm phản hồi và tự giảm khi có nhạc/video (F-GAME-13).',
       'Khi ván kết thúc, hệ thống tính điểm và cộng XP theo luật của game.',
       'Tiến độ nhiệm vụ “thắng một ván” và thử thách ngày được cập nhật.'],
 alt=['3a. Trong lúc chơi có video: game thường chia đôi màn hình (X7); hai game toàn màn yêu cầu đóng video.',
      '5a. Hoàn thành thử thách ngày: cộng 50+5×streak và tặng một treat cho pet (X6).'],
 exc=['2a. Game đang khoá: hiển thị điều kiện mở khoá thay vì vào ván.']),
dict(code='UC-06', name='Theo dõi tiến độ và thành tích',
 actor='Người dùng',
 desc='Người dùng xem tổng điểm, chuỗi ngày hoạt động, huy hiệu và tổng kết tháng của mình.',
 pre='Người dùng đã mở tab Tài khoản.',
 post='Không thay đổi dữ liệu; chỉ đọc và hiển thị.',
 trig='Người dùng mở màn Tài khoản hoặc màn tổng kết.',
 flow=['Hệ thống đọc tổng điểm từ sổ điểm và chuỗi ngày từ DataStore.',
       'Hiển thị huy hiệu đã mở và điều kiện của huy hiệu còn thiếu.',
       'Hiển thị tổng kết tháng: loại nội dung, kỷ lục, thành tựu nổi bật.'],
 alt=['3a. Chưa đủ dữ liệu tháng: tổng kết dùng số liệu tích lũy từ đầu.'],
 exc=[]),
dict(code='UC-07', name='Chăm sóc thú cưng',
 actor='Người dùng',
 desc='Người dùng cho thú cưng ăn bằng điểm hoặc treat; thú cưng tiến hoá theo mốc điểm tổng.',
 pre='Người dùng đã có thú cưng (nở sau ba nhiệm vụ đầu).',
 post='Thú cưng tăng tiến trình; điểm hoặc treat bị trừ.',
 trig='Người dùng chạm nút cho ăn trong hồ sơ.',
 flow=['Hệ thống kiểm tra giới hạn một lần cho ăn mỗi ngày.',
       'Người dùng chọn trả bằng 30 điểm hoặc một treat.',
       'Hệ thống trừ nguồn tương ứng và ghi nhận tiến trình.',
       'Nếu đủ mốc, thú cưng chuyển giai đoạn kế tiếp (500/2.000/5.000 điểm).'],
 alt=['1a. Đã cho ăn hôm nay: nút bị khoá kèm thông báo.'],
 exc=['3a. Không đủ điểm và không có treat: hiển thị gợi ý kiếm thêm điểm.']),
dict(code='UC-08', name='Đổi quà trong cửa hàng',
 actor='Người dùng',
 desc='Người dùng dùng điểm đổi vật phẩm: mở khoá game, phụ kiện thú cưng, khung avatar.',
 pre='Người dùng có số dư điểm lớn hơn hoặc bằng giá vật phẩm.',
 post='Điểm bị trừ; vật phẩm được đánh dấu sở hữu và áp dụng ngay.',
 trig='Người dùng chọn một vật phẩm trong cửa hàng.',
 flow=['Hệ thống hiển thị danh sách vật phẩm kèm giá điểm.',
       'Người dùng chọn mua một vật phẩm chưa sở hữu.',
       'Hệ thống kiểm tra số dư và trừ điểm.',
       'Vật phẩm được kích hoạt và đánh dấu “Đã có”.'],
 alt=['2a. Vật phẩm đã sở hữu: nút mua bị thay bằng nhãn “Đã có”.'],
 exc=['3a. Không đủ điểm: hiển thị số điểm còn thiếu.']),
dict(code='UC-09', name='Lưu nội dung để dùng sau',
 actor='Người dùng',
 desc='Người dùng lưu video vào Xem sau, lưu bài báo để đọc sau, đánh dấu nội dung đã tải và xem lại trong các danh sách riêng.',
 pre='Nội dung đang mở ở màn chi tiết hoặc trình đọc.',
 post='Nội dung xuất hiện trong danh sách tương ứng; bỏ lưu thì biến mất khỏi danh sách.',
 trig='Người dùng chạm biểu tượng lưu của một nội dung.',
 flow=['Hệ thống ghi nhận mã nội dung vào danh sách (Room hoặc DataStore).',
       'Biểu tượng lưu đổi trạng thái.',
       'Người dùng mở danh sách để xem lại các nội dung đã lưu.'],
 alt=['3a. Bỏ lưu: nội dung bị xoá khỏi danh sách, lịch sử xem vẫn giữ.'],
 exc=[]),
dict(code='UC-10', name='Tìm nội dung',
 actor='Người dùng',
 desc='Người dùng gõ từ khoá để tìm video, bài hát, bài báo và game trong phạm vi từng phần và xuyên nội dung từ Home.',
 pre='Người dùng đang ở màn danh sách (không ở trong trình phát hay trình đọc).',
 post='Danh sách được lọc theo từ khoá; chạm kết quả mở nội dung.',
 trig='Người dùng chạm ô tìm kiếm và nhập từ khoá.',
 flow=['Hệ thống hiển thị ô tìm kiếm của phần hiện tại.',
       'Người dùng nhập từ khoá; danh sách lọc ngay theo tiêu đề, tác giả hoặc chuyên mục.',
       'Kết quả được sắp theo mức khớp (kênh khớp hiện trước với video).',
       'Người dùng chạm kết quả để mở nội dung.'],
 alt=['2a. Không có kết quả: hiển thị “Không có nội dung phù hợp” kèm gợi ý liên quan.'],
 exc=[]),
dict(code='UC-11', name='Quản lý danh tính',
 actor='Người dùng',
 desc='Người dùng tạo tài khoản hoặc đăng nhập bằng OTP demo, tiếp tục với tư cách khách, chuyển tài khoản hoặc đăng xuất.',
 pre='Ứng dụng đang ở màn xác thực hoặc màn Cài đặt.',
 post='Phiên đăng nhập được tạo hoặc kết thúc; dữ liệu cục bộ được giữ nguyên khi đăng xuất.',
 trig='Người dùng chọn đăng nhập, dùng thử hoặc đăng xuất.',
 flow=['Hệ thống hiển thị màn xác thực với lựa chọn OTP, mật khẩu hoặc “Dùng thử”.',
       'Người dùng nhập số điện thoại hoặc email và yêu cầu mã.',
       'Hệ thống gửi mã OTP có hiệu lực 5 phút (I4).',
       'Người dùng nhập mã; hệ thống tạo phiên và mở Main.',
       'Khi đăng xuất, hệ thống kết thúc phiên và quay về màn xác thực.'],
 alt=['1a. Chọn “Dùng thử”: vào Main với cờ khách, mọi năng lực giữ nguyên.',
      '4a. Mã sai: báo lỗi và cho nhập lại, tối đa năm lần rồi phải gửi lại mã.'],
 exc=['3a. Dịch vụ gửi mã không khả dụng: thông báo và giữ màn hình chờ.']),
dict(code='X4', name='Nghe tin bằng TTS (biến thể của UC-04)',
 actor='Người dùng; «system» TTS engine',
 desc='Người dùng nghe một bài báo thay vì đọc: hệ thống chuyển bài thành audio và phát theo đoạn, nhạc đang phát tự nhường.',
 pre='Bài báo đã mở trong trình đọc; engine TTS sẵn sàng.',
 post='Audio kết thúc hoặc bị dừng; trạng thái nhạc trước đó được giữ nguyên.',
 trig='Người dùng chạm “Nghe tin” trên thanh công cụ trình đọc.',
 flow=['Hệ thống chuyển nội dung bài thành audio (có thanh tiến trình trong lúc chờ).',
       'Nhạc đang phát tự tạm dừng nhường luồng tiếng (C13).',
       'Audio phát theo đoạn; thanh tiến trình và nút dừng hiện trên trình đọc.',
       'Người dùng nghe hết hoặc bấm dừng.',
       'Nhạc phát lại từ chỗ dừng bằng một chạm trên dock.'],
 alt=['1a. Không có nhạc đang phát: bỏ qua bước 2.',
      '4a. Rời trình đọc khi đang nghe: thẻ TTS nổi giữ điều khiển phát/dừng.'],
 exc=['1a. Tổng hợp lỗi: thông báo kèm nút Thử lại; nhạc tiếp tục bình thường.',
      'Ghi chú hiện thực: bản demo phát audio mẫu thay vì đọc toàn văn; hợp đồng hành vi theo US-NEWS-04.']),
dict(code='UC-12', name='Ghi âm karaoke',
 actor='Người dùng',
 desc='Người dùng ghi giọng hát cùng bài đang phát, hoặc ghi màn hình video; bản ghi được lưu trong bộ nhớ riêng của ứng dụng.',
 pre='Có media đang phát; người dùng đã cấp quyền micro khi được hỏi.',
 post='Tệp ghi âm được lưu trong thư mục riêng của ứng dụng.',
 trig='Người dùng chạm nút micro trên trình phát.',
 flow=['Hệ thống hiển thị lựa chọn: hát cùng bài (chỉ micro) hoặc ghi màn hình kèm micro.',
       'Nếu chưa có quyền, hệ thống xin quyền micro đúng lúc này.',
       'Đếm ngược 3--2--1 và bắt đầu ghi.',
       'Người dùng dừng ghi; hệ thống lưu tệp và thông báo đường dẫn.'],
 alt=['2a. Người dùng từ chối quyền: quay lại trình phát, không ghi.'],
 exc=['4a. Lỗi ghi tệp: thông báo và giữ trình phát ở trạng thái ban đầu.']),
]

def spec_table(s):
    rows = []
    rows.append(r'\begin{longtable}{>{\RaggedRight\arraybackslash}p{0.16\linewidth}>{\RaggedRight\arraybackslash}p{0.76\linewidth}}')
    rows.append(r'\caption{Đặc tả use case %s --- %s}' % (s['code'], s['name']))
    rows.append(r'\label{tab:spec-%s}\\' % s['code'].lower())
    rows.append(r'\toprule')
    rows.append(r'\textbf{Mục} & \textbf{Nội dung} \\')
    rows.append(r'\midrule')
    rows.append(r'\endfirsthead')
    rows.append(r'\toprule')
    rows.append(r'\textbf{Mục} & \textbf{Nội dung} \\')
    rows.append(r'\midrule')
    rows.append(r'\endhead')
    rows.append(r'\bottomrule')
    rows.append(r'\endfoot')
    rows.append(r'Use case & %s \\' % s['name'])
    rows.append(r'Tác nhân & %s \\' % s['actor'])
    rows.append(r'Mô tả & %s \\' % s['desc'])
    rows.append(r'Tiên điều kiện & %s \\' % s['pre'])
    rows.append(r'Hậu điều kiện & %s \\' % s['post'])
    rows.append(r'Kích hoạt & %s \\' % s['trig'])
    flow = ' '.join('%d. %s' % (i+1, x) for i, x in enumerate(s['flow']))
    rows.append(r'Luồng chuẩn & %s \\' % flow)
    alt = ' '.join(s['alt']) if s['alt'] else 'Không có.'
    rows.append(r'Luồng thay thế & %s \\' % alt)
    exc = ' '.join(s['exc']) if s['exc'] else 'Không có.'
    rows.append(r'Ngoại lệ & %s \\' % exc)
    rows.append(r'\end{longtable}')
    return '\n'.join(rows)

out = [SPEC_HEADER]
for s in SPECS:
    out.append('')
    out.append(r'\begingroup\small\renewcommand{\arraystretch}{1.15}\setlength{\tabcolsep}{3pt}')
    out.append(spec_table(s))
    out.append(r'\endgroup')
w('sections/2-product-scope/use-case-specs.tex', '\n'.join(out) + '\n')

# ============================================================
# 2) ACTIVITY DIAGRAMS — 6 hình, layout thẳng đứng cố định
# ============================================================
def activity_figure(act):
    L = []
    L.append(r'\begin{figure}[H]')
    L.append(r'\centering')
    L.append(r'\begin{tikzpicture}[font=\footnotesize]')
    y = 0.0
    names = []
    def node_name(i): return 'n%d' % i
    idx = [0]
    def newname():
        idx[0] += 1
        return node_name(idx[0])
    # start
    sn = newname()
    L.append(r'\node[umlstart] (%s) at (0,0) {};' % sn)
    last = sn
    cursor = 0.0
    def place_action(x, cy, text, width=6.2):
        nn = newname()
        L.append(r'\node[actnode, text width=%scm] (%s) at (%s,%s) {%s};' % (width, nn, x, cy, text))
        return nn
    def edge(a, b, label=None, above=True):
        if label:
            L.append(r'\draw[umlline] (%s) -- node[%s, font=\scriptsize, fill=white, inner sep=1pt]{%s} (%s);' % (a, 'above' if above else 'below', label, b))
        else:
            L.append(r'\draw[umlline] (%s) -- (%s);' % (a, b))
    for item in act['items']:
        if item[0] == 'a':
            cy = cursor - 1.05
            nn = place_action(0, cy, item[1])
            edge(last + '.south', nn + '.north')
            last, cursor = nn, cy
        elif item[0] == 'd':
            _, q, gl, lchain, gr, rchain = item
            cy = cursor - 1.55
            qn = newname()
            L.append(r'\node[decnode, text width=3.0cm] (%s) at (0,%s) {%s};' % (qn, cy, q))
            edge(last + '.south', qn + '.north')
            # branches
            depth = max(len(lchain), len(rchain), 1)
            left_end = None
            right_end = None
            for k, txt in enumerate(lchain):
                cyk = cy - 1.05 * k
                nn = place_action(-4.95, cyk, txt, width=5.0)
                if k == 0:
                    edge(qn + '.west', nn + '.east', gl)
                else:
                    edge(prev + '.south', nn + '.north')
                prev = nn
                left_end = nn
            for k, txt in enumerate(rchain):
                cyk = cy - 1.05 * k
                nn = place_action(4.95, cyk, txt, width=5.0)
                if k == 0:
                    edge(qn + '.east', nn + '.west', gr)
                else:
                    edge(prev + '.south', nn + '.north')
                prev = nn
                right_end = nn
            my = cy - 1.08 * depth - 1.15
            mn = newname()
            L.append(r'\node[mergenode] (%s) at (0,%s) {};' % (mn, my))
            if left_end:
                L.append(r'\draw[umlline] (%s.south) |- (%s.west);' % (left_end, mn))
            else:
                L.append(r'\draw[umlline] (%s.west) -- ++(-0.6,0) |- (%s.west);' % (qn, mn))
            if right_end:
                L.append(r'\draw[umlline] (%s.south) |- (%s.east);' % (right_end, mn))
            else:
                L.append(r'\draw[umlline] (%s.east) -- ++(0.6,0) |- (%s.east);' % (qn, mn))
            last, cursor = mn, my
    cy = cursor - 1.1
    en = newname()
    L.append(r'\node[umlend] (%s) at (0,%s) {};' % (en, cy))
    edge(last + '.south', en + '.north')
    L.append(r'\end{tikzpicture}')
    L.append(r'\caption{%s}' % act['caption'])
    L.append(r'\label{%s}' % act['label'])
    L.append(r'\end{figure}')
    return '\n'.join(L)

ACTIVITIES = [
 dict(label='fig:act-login', caption='Activity diagram UC-11 --- đăng nhập bằng OTP',
      items=[('a', 'Mở màn hình Đăng nhập'),
             ('a', 'Nhập số điện thoại hoặc email; yêu cầu gửi mã'),
             ('a', 'Hệ thống gửi mã OTP (hiệu lực 5 phút)'),
             ('d', 'Mã đúng và còn hạn?', 'Có', ['Tạo phiên; mở Main'], 'Không', ['Báo lỗi; tăng số lần sai']),
             ('a', 'Phiên đăng nhập hoàn tất; dữ liệu cục bộ giữ nguyên') ]),
 dict(label='fig:act-first-run', caption='Activity diagram UC-01 --- phiên đầu tiên',
      items=[('a', 'Mở ứng dụng (chưa hoàn tất onboarding)'),
             ('a', 'Ba màn giới thiệu giá trị'),
             ('d', 'Bỏ qua chọn chủ đề?', 'Có', ['Vào Home với đề xuất mặc định'], 'Không', ['Chọn tối thiểu 3 chủ đề']),
             ('a', 'Lưu sở thích; Home đề xuất theo chủ đề'),
             ('a', 'Hiện dock demo và nhiệm vụ ngày đầu')]),
 dict(label='fig:act-video', caption='Activity diagram UC-02 --- xem video và chuyển phân hệ',
      items=[('a', 'Chạm thẻ video trong feed'),
             ('d', 'Nhạc đang phát?', 'Có', ['Popup C2: tắt tiếng video hoặc dừng nhạc'], 'Không', []),
             ('a', 'Mở stream tại vị trí đã lưu (checkpoint 3 giây)'),
             ('a', 'Phát video trong tối đa 2 giây'),
             ('d', 'Rời màn hình player?', 'Có', ['Cửa sổ nổi hiện; dùng chung engine'], 'Không', ['Điều khiển trong player']),
             ('d', 'Mở rộng hay đóng cửa sổ?', 'Mở rộng', ['Về player đúng vị trí'], 'Đóng', ['Dừng; lưu vị trí; thêm Xem sau'])]),
 dict(label='fig:act-conflict', caption='Activity diagram UC-03/X0 --- nghe nhạc và phân xử âm thanh',
      items=[('a', 'Chọn bài hát trong feed'),
             ('d', 'Video đang phát?', 'Có', ['Popup C1: tắt tiếng video hoặc dừng video'], 'Không', ['Không cần phân xử']),
             ('a', 'Phát nhạc; dock mini hiện trên mọi tab'),
             ('d', 'Đóng dock?', 'Có', ['Dừng phát; hoàn tác trong 4--10 giây'], 'Không', ['Tiếp tục hàng đợi'])]),
 dict(label='fig:act-news', caption='Activity diagram UC-04 --- đọc tin và nghe tin',
      items=[('a', 'Chọn bài trong feed Tin tức'),
             ('a', 'Đọc trong trình đọc; chỉnh cỡ chữ A−/A+'),
             ('d', 'Bấm “Nghe tin”?', 'Có', ['Nhạc tạm dừng; audio phát có tiến trình'], 'Không', ['Đọc tiếp; có thể lưu bài']),
             ('a', 'Kết thúc bài; nhiệm vụ đọc được tính một lần')]),
 dict(label='fig:act-game', caption='Activity diagram UC-05 --- chơi minigame và nhận điểm',
      items=[('a', 'Mở tab Trò chơi'),
             ('a', 'Chọn game; hệ thống kiểm tra mở khoá'),
             ('a', 'Chơi ván theo luật của game'),
             ('d', 'Ván kết thúc?', 'Có', ['Tính điểm; cộng XP; cập nhật nhiệm vụ'], 'Không', ['Tiếp tục chơi']),
             ('d', 'Hoàn thành thử thách ngày?', 'Có', ['+50+5×streak; tặng treat cho pet'], 'Không', [])]),
]

acts = [r'\subsection{Sơ đồ hoạt động cho các luồng chính}', r'\label{sec:activity-diagrams}', '',
        r'Mỗi use case mục tiêu được mô tả lại bằng một sơ đồ hoạt động (activity diagram) theo ký pháp UML: nút bắt đầu đặc, nút kết thúc hai vòng, hành động bo tròn, quyết định hình thoi với nhãn nhánh, các nhánh hội tụ về nút gộp trước khi tiếp tục. Sáu luồng dưới đây phủ các nhóm chức năng chính; các luồng còn lại có cùng khuôn và được đặc tả ở mục~\ref{sec:uc-specs}.', '']
for a in ACTIVITIES:
    acts.append(activity_figure(a))
    acts.append('')
w('sections/3-ui-ux-design/activity-diagrams.tex', '\n'.join(acts) + '\n')

# ============================================================
# 3) STATE TABLES — mô tả trạng thái + bảng kích thích
# ============================================================
def twotables(spec):
    L = []
    L.append(r'\begingroup\small\renewcommand{\arraystretch}{1.12}\setlength{\tabcolsep}{3pt}')
    L.append(r'\begin{longtable}{>{\RaggedRight\arraybackslash}p{0.09\linewidth}>{\RaggedRight\arraybackslash}p{0.20\linewidth}>{\RaggedRight\arraybackslash}p{0.63\linewidth}}')
    L.append(r'\caption{%s}' % spec['state_caption'])
    L.append(r'\label{tab:%s}\\' % spec['state_label'])
    L.append(r'\toprule')
    L.append(r'\textbf{Mã} & \textbf{Trạng thái} & \textbf{Mô tả và hành vi} \\')
    L.append(r'\midrule')
    L.append(r'\endfirsthead')
    L.append(r'\toprule')
    L.append(r'\textbf{Mã} & \textbf{Trạng thái} & \textbf{Mô tả và hành vi} \\')
    L.append(r'\midrule')
    L.append(r'\endhead')
    L.append(r'\bottomrule')
    L.append(r'\endfoot')
    for code, name, desc in spec['states']:
        L.append(r'%s & %s & %s \\' % (code, name, desc))
    L.append(r'\end{longtable}')
    L.append('')
    L.append(r'\begin{longtable}{>{\RaggedRight\arraybackslash}p{0.24\linewidth}>{\RaggedRight\arraybackslash}p{0.16\linewidth}>{\RaggedRight\arraybackslash}p{0.17\linewidth}>{\RaggedRight\arraybackslash}p{0.35\linewidth}}')
    L.append(r'\caption{%s}' % spec['stim_caption'])
    L.append(r'\label{tab:%s}\\' % spec['stim_label'])
    L.append(r'\toprule')
    L.append(r'\textbf{Kích thích} & \textbf{Nguồn} & \textbf{Chuyển trạng thái} & \textbf{Hành động} \\')
    L.append(r'\midrule')
    L.append(r'\endfirsthead')
    L.append(r'\toprule')
    L.append(r'\textbf{Kích thích} & \textbf{Nguồn} & \textbf{Chuyển trạng thái} & \textbf{Hành động} \\')
    L.append(r'\midrule')
    L.append(r'\endhead')
    L.append(r'\bottomrule')
    L.append(r'\endfoot')
    for stim, src, trans, action in spec['stimuli']:
        L.append(r'%s & %s & %s & %s \\' % (stim, src, trans, action))
    L.append(r'\end{longtable}')
    L.append(r'\endgroup')
    return '\n'.join(L)

STATES = [
 dict(prefix='video', fig='fig:state-video',
      state_caption='Mô tả trạng thái của video khi hiển thị', state_label='state-video',
      state_tbl_caption='',
      states=[('S0', 'Không hoạt động', 'Không có video được mở; engine ở trạng thái rỗi.'),
              ('S1', 'Trong trình phát', 'Video phát toàn màn hình tại màn chi tiết; điều khiển đầy đủ.'),
              ('S2', 'Cửa sổ nổi', 'Video thu nhỏ ở góc khi người dùng rời màn hình; vẫn phát, dùng chung engine.'),
              ('S3', 'Chia đôi màn hình', 'Video chiếm dải trên, nội dung phân hệ chiếm phần dưới (X7).'),
              ('S4', 'Tạm dừng', 'Giữ nguyên vị trí; có thể phát tiếp bất cứ lúc nào.'),
              ('S5', 'Kết thúc', 'Video dừng hẳn; vị trí được lưu; tuỳ ngữ cảnh thì thêm vào Xem sau.')],
      stimuli=[('Chạm thẻ video', 'Người dùng', 'S0 → S1', 'Đọc checkpoint và mở stream tại vị trí đã lưu.'),
               ('Rời màn hình player', 'Điều hướng', 'S1 → S2', 'Hiện cửa sổ nổi, tiếp tục phát.'),
               ('Mở rộng', 'Người dùng (cửa sổ nổi)', 'S2 → S1', 'Về trình phát, giữ vị trí.'),
               ('Chọn chia đôi', 'Người dùng', 'S2 → S3', 'Dồn video lên dải trên 34\\%.'),
               ('Thu nhỏ', 'Người dùng', 'S3 → S2', 'Trả video về cửa sổ nổi.'),
               ('Tạm dừng / phát tiếp', 'Người dùng', 'S1,S2 ↔ S4', 'Dừng hoặc tiếp tục phát.'),
               ('Đóng cửa sổ nổi', 'Người dùng', 'S2 → S5', 'Dừng, lưu vị trí, thêm Xem sau.'),
               ('Video kết thúc', 'Player', 'S1,S2 → S5', 'Hiện lời mời quiz nếu có (X3).'),
               ('Lỗi stream', 'Player', 'S1 → S4', 'Thông báo và chờ thử lại 5--15 giây.')]),
 dict(prefix='music', fig='fig:state-music',
      state_caption='Mô tả trạng thái của bộ phát nhạc', state_label='state-music',
      states=[('M0', 'Rỗi', 'Chưa có bài nào được nạp.'),
              ('M1', 'Đã nạp, chờ phát', 'Trạng thái sau khởi động lạnh: bài cuối được nạp ở 0:00, chưa phát.'),
              ('M2', 'Đang phát', 'Nhạc phát; dock hiện trên mọi tab trừ Now Playing.'),
              ('M3', 'Tạm dừng', 'Giữ vị trí; xảy ra khi người dùng dừng hoặc khi TTS bắt đầu.'),
              ('M4', 'Kết thúc', 'Hàng đợi hết; chờ người dùng chọn bài mới.'),
              ('M5', 'Lỗi', 'Không mở được stream; hàng đợi được giữ để thử lại.')],
      stimuli=[('Chọn bài', 'Người dùng', 'M0,M1 → M2', 'Nạp hàng đợi, phát; phân xử âm thanh nếu video đang phát (X0).'),
               ('Khởi động lạnh', 'Hệ thống', '→ M1', 'Nạp bài cuối ở 0:00, không tự phát.'),
               ('Tạm dừng', 'Người dùng', 'M2 → M3', 'Dừng phát, giữ vị trí.'),
               ('Bắt đầu TTS', 'Người dùng (nghe tin)', 'M2 → M3', 'Nhường luồng tiếng cho TTS.'),
               ('Phát tiếp trên dock', 'Người dùng', 'M3 → M2', 'Tiếp tục từ chỗ dừng.'),
               ('Hết bài trong hàng đợi', 'Player', 'M2 → M2', 'Tự chuyển bài kế tiếp.'),
               ('Hết hàng đợi', 'Player', 'M2 → M4', 'Dừng; chờ chọn bài mới.'),
               ('Lỗi stream', 'Player', 'M2 → M5', 'Thông báo lỗi, giữ hàng đợi.')]),
 dict(prefix='rule', fig='fig:state-rule',
      state_caption='Mô tả trạng thái của quy tắc xung đột âm thanh', state_label='state-rule',
      states=[('R0', 'Chưa có quy tắc', 'Mỗi lần xung đột đều hỏi người dùng (trạng thái mặc định).'),
              ('R1', 'Ghi nhớ tắt tiếng video', 'Video tiếp tục hiển thị nhưng âm lượng bằng không khi xung đột.'),
              ('R2', 'Ghi nhớ dừng video', 'Video dừng và lưu vị trí khi xung đột.'),
              ('R3', 'Ưu tiên video', 'Không phát nhạc khi video đang phát; chỉ đặt được từ Cài đặt.')],
      stimuli=[('Chọn kèm tích “Không hỏi lại”', 'Người dùng (popup C1)', 'R0 → R1,R2', 'Ghi quy tắc vào DataStore.'),
               ('Chọn không tích', 'Người dùng (popup C1)', 'R0 → R0', 'Chỉ áp dụng cho lần đó.'),
               ('Đổi trong Cài đặt', 'Người dùng', 'R0..R3 → R1,R2,R3', 'Cập nhật quy tắc đang lưu.'),
               ('Chọn “Luôn hỏi”', 'Người dùng (Cài đặt)', 'R1,R2,R3 → R0', 'Xoá quy tắc đã lưu.')]),
]

st = [r'\subsection{Mô hình trạng thái}', r'\label{sec:state-charts}', '',
      r'Ba đối tượng có vòng đời phức tạp nhất của OneSpace được mô hình hoá bằng máy trạng thái: cách video hiển thị khi người dùng đổi phân hệ, vòng đời bộ phát nhạc, và quy tắc phân xử âm thanh được ghi nhớ. Với mỗi sơ đồ, bảng mô tả trạng thái và bảng kích thích đi kèm xác định rõ sự kiện, nguồn phát và hành động.', '']
# figures are handcrafted, inserted via placeholders read from files
st.append(r'\input{sections/4-technical-architecture/state-figures}')
st.append('')
for s in STATES:
    st.append(twotables(dict(state_caption=s['state_caption'], state_label=s['state_label'],
                             stim_caption='Kích thích chuyển trạng thái — ' + s['state_caption'].split('của')[-1].strip(),
                             stim_label=s['state_label'] + '-stim',
                             states=s['states'], stimuli=s['stimuli'])))
    st.append('')
w('sections/4-technical-architecture/state-tables.tex', '\n'.join(st) + '\n')
print('DONE')
