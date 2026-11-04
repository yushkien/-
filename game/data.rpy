# =============================================================
#  data.rpy
#  히로인 4명 + 초기 관계값 + 글로벌 상태 정의
#  (설계 문서 1, 3, 2-4 장)
#
#  ※ 이름/세부 설정은 임시(플레이스홀더). 추후 확정 예정.
# =============================================================

# ---- 글로벌 상태 (설계 2-4) ----
default day = 1
default slot = 1
default phase = "pre_exam"        # "pre_exam"(수능전) / "post_exam"(수능후)
default harem_acceptance = 0      # 히든 스택 0~100
default turn_log = []             # 최근 슬롯 결과 메시지

# ---- 히로인 4명 (설계 3) ----
# dere 유형별 성격 파라미터로 "같은 로직, 다른 체감" 구현 (설계 2-3)
default heroines = {
    "A": Heroine("A", u"하루(가명)", u"츤데레",
                 affection=10,
                 affection_gain=0.9, jealousy_gain=1.4,   # 질투 빠름
                 jealousy_threshold=55, tension_decay=4,
                 sabotage_power=1.1, hides_feelings=0.7),

    "B": Heroine("B", u"메이(가명)", u"메가데레/소꿉친구",
                 affection=45,                              # 시작 호감 높음(친구벽)
                 affection_gain=1.3, jealousy_gain=0.8,
                 jealousy_threshold=65, tension_decay=8,   # 뒤끝 없음
                 sabotage_power=0.8, hides_feelings=0.2),

    "C": Heroine("C", u"유키(가명)", u"소프트 얀데레",
                 affection=15,
                 affection_gain=1.0, jealousy_gain=1.0,
                 jealousy_threshold=50, tension_decay=3,   # 임계 넘으면 폭발
                 sabotage_power=1.6, hides_feelings=0.5),

    "D": Heroine("D", u"소라(가명)", u"소심한 쿨데레",
                 affection=8,
                 affection_gain=0.8, jealousy_gain=0.9,
                 jealousy_threshold=70, tension_decay=2,   # 안으로 쌓음
                 sabotage_power=1.0, hides_feelings=0.9),
}

# ---- 초기 히로인 간 관계 (설계 2-2: 쌍 6개 / 방향성) ----
# 사전 설정: 원래 친한 쌍 / 서먹한 쌍을 미리 배치
#   bond: -100~100 (대칭),  t: 0~100 (방향성 긴장, 초기 0)
default rels = {
    # A-B: 원래 친한 사이 (높은 bond) → 나중에 질투로 '웃으며 견제' 후보
    ("A", "B"): {"bond": 55, "t": 0}, ("B", "A"): {"bond": 55, "t": 0},
    # A-C: 서먹 (낮은 bond)
    ("A", "C"): {"bond": -10, "t": 0}, ("C", "A"): {"bond": -10, "t": 0},
    # A-D: 중립
    ("A", "D"): {"bond": 5, "t": 0},  ("D", "A"): {"bond": 5, "t": 0},
    # B-C: 중립
    ("B", "C"): {"bond": 10, "t": 0}, ("C", "B"): {"bond": 10, "t": 0},
    # B-D: 약간 친함
    ("B", "D"): {"bond": 30, "t": 0}, ("D", "B"): {"bond": 30, "t": 0},
    # C-D: 서먹 (낮은 bond) → 공동의 적 앞에서 '연합' 후보
    ("C", "D"): {"bond": -5, "t": 0}, ("D", "C"): {"bond": -5, "t": 0},
}
