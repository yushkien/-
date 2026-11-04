# =============================================================
#  options.rpy  —  Ren'Py 프로젝트 기본 설정
# =============================================================

define config.name = _("관계 중심 미연시 (가제)")
define config.version = "0.0.1"

define gui.show_name = True

## 창 제목
define config.window_title = u"관계 중심 미연시 (프로토타입)"

## 한국어 표시용 폰트 설정
## ※ Ren'Py 기본 폰트(DejaVuSans)는 한글을 그리지 못합니다.
##    아래 경로에 한글 폰트(.ttf/.otf)를 넣고 주석을 해제하세요.
##    예: game/fonts/NotoSansKR-Regular.ttf (Noto Sans KR 등)
# define gui.text_font = "fonts/NotoSansKR-Regular.ttf"
# define gui.name_text_font = "fonts/NotoSansKR-Regular.ttf"
# define gui.interface_text_font = "fonts/NotoSansKR-Regular.ttf"

## 자동 전진/스킵 등 기본값
define config.has_autosave = True
define config.save_directory = "relationship_vn_proto"

## 창 크기 (기본 1280x720)
# define config.screen_width = 1280
# define config.screen_height = 720

init python:
    ## 빌드 설정 (배포 시 사용)
    build.name = "relationship_vn_proto"
