# =============================================================
#  logic.rpy
#  관계/질투 시스템의 핵심 로직 (설계 문서 2~5장 구현)
#
#  - 모든 상태는 default 로 선언 → Ren'Py 세이브/로드에 자동 포함
#  - 데이터: Python 클래스(Heroine) + 관계 쌍 딕셔너리(rels)
#  - 로직: init python 블록의 순수 함수
# =============================================================

init -1 python:

    def clamp(v, lo=0, hi=100):
        """값을 [lo, hi] 범위로 제한."""
        return max(lo, min(hi, v))

    class Heroine(object):
        """히로인 1명의 상태 (플레이어 기준 수치 + 성격 파라미터)."""
        def __init__(self, hid, name, dere,
                     affection=0, jealousy=0,
                     affection_gain=1.0, jealousy_gain=1.0,
                     jealousy_threshold=60, tension_decay=5,
                     sabotage_power=1.0, hides_feelings=0.0):
            self.id = hid
            self.name = name
            self.dere = dere                      # 데레 유형(표시용)
            self.affection = affection            # 0~100 플레이어 호감
            self.jealousy = jealousy              # 0~100 질투 게이지
            # --- 성격 파라미터 (설계 2-3) ---
            self.affection_gain = affection_gain
            self.jealousy_gain = jealousy_gain
            self.jealousy_threshold = jealousy_threshold
            self.tension_decay = tension_decay
            self.sabotage_power = sabotage_power
            self.hides_feelings = hides_feelings
            self.flags = {}

    # ---- 관계 쌍(방향성) 모델 (설계 2-2) ----
    # rels[(a, b)] = {"bond": 대칭값, "t": a->b 긴장}
    # bond 는 대칭이라 (a,b)/(b,a) 양쪽에 같은 값을 넣어 조회를 단순화.

    def rel_key(a, b):
        return (a, b)

    def get_bond(a, b):
        return rels[(a, b)]["bond"]

    def set_bond(a, b, v):
        v = clamp(v, -100, 100)
        rels[(a, b)]["bond"] = v
        rels[(b, a)]["bond"] = v   # 대칭 유지

    def add_bond(a, b, d):
        set_bond(a, b, get_bond(a, b) + d)

    def get_tension(a, b):
        """a 가 b 에게 느끼는 긴장(방향성, 비대칭)."""
        return rels[(a, b)]["t"]

    def add_tension(a, b, d):
        rels[(a, b)]["t"] = clamp(rels[(a, b)]["t"] + d)

    # -------------------------------------------------------------
    #  핵심 루프 (설계 4장)
    # -------------------------------------------------------------

    def do_action_date(target_id):
        """플레이어가 target 히로인과 데이트/호감 행동을 한 슬롯.
           → 호감 상승 + 다른 히로인 질투 상승 + 긴장 전이."""
        phase_mul = 1.3 if store.phase == "pre_exam" else 1.0  # 수능전 가속(설계 S)
        tgt = heroines[target_id]

        # (2) 호감 반영
        gained = 8 * tgt.affection_gain
        tgt.affection = clamp(tgt.affection + gained)

        log = []
        log.append("%s 와(과) 시간을 보냈다. (호감 +%d)" % (tgt.name, int(gained)))

        # (3) 질투: 타인 히로인들이 질투를 느낌
        for hid, h in heroines.items():
            if hid == target_id:
                continue
            # 이미 호감이 있을수록 더 질투함
            jealous = (3 + h.affection * 0.08) * h.jealousy_gain * phase_mul
            h.jealousy = clamp(h.jealousy + jealous)
            # (4) 긴장 전이: 질투하는 h -> 편애받은 target 방향으로 tension↑
            #     긴장은 자연감소보다 빠르게 쌓여야 임계(60)에 도달 가능 → 1.6배
            add_tension(hid, target_id, int(jealous * 1.6))

        return log

    def do_action_fair():
        """모두에게 공평하게 — 질투 완화 + 하렘 수용도 상승 (설계 6장).
           하렘 루트가 성립하려면 완화량이 데이트발 질투를 상쇄할 만큼 커야 함."""
        store.harem_acceptance = clamp(store.harem_acceptance + 6)
        for h in heroines.values():
            h.jealousy = clamp(h.jealousy - 12)   # 완화 강화(4→12)
            h.affection = clamp(h.affection + 2)  # 모두에게 소폭 호감(하렘 루트 보상)
        # 수용도가 높을수록 긴장이 유대로 더 강하게 전환됨
        for (a, b), r in rels.items():
            if store.harem_acceptance >= 40:
                drop = heroines[a].tension_decay + 6
                r["t"] = clamp(r["t"] - drop)
                add_bond(a, b, 1)   # 긴장이 유대로 전환(설계 6장)
        return ["모두에게 공평하게 대했다. (질투 완화 / 하렘 수용도 +6)"]

    # -------------------------------------------------------------
    #  연합 / 견제 판정 (설계 4-5) — 작성하지 않고 상태로 계산
    # -------------------------------------------------------------

    def find_leader():
        """독주자: affection 1등이고 2등과 격차 > 25 인 히로인 id. 없으면 None."""
        ranked = sorted(heroines.values(), key=lambda h: h.affection, reverse=True)
        if len(ranked) < 2:
            return None
        if ranked[0].affection - ranked[1].affection > 25 and ranked[0].affection > 40:
            return ranked[0].id
        return None

    def check_alliance():
        """독주자를 겨냥한 긴장이 높은(>=60) 히로인 2명 이상 → 연합 목록 반환."""
        leader = find_leader()
        if leader is None:
            return None
        members = [hid for hid in heroines
                   if hid != leader and get_tension(hid, leader) >= 60]
        if len(members) >= 2:
            return (leader, members)
        return None

    def check_snipe():
        """'웃으며 견제': bond 높은데(>=40) 한쪽 tension 높은(>=60) 쌍 목록."""
        out = []
        seen = set()
        for (a, b) in rels:
            if (b, a) in seen:
                continue
            seen.add((a, b))
            if get_bond(a, b) >= 40 and (get_tension(a, b) >= 60 or get_tension(b, a) >= 60):
                out.append((a, b))
        return out

    def end_of_slot_decay():
        """슬롯 종료 시 자연 감소.
           - 긴장: 아주 완만하게만 감소(편애가 지속되면 임계까지 쌓이도록).
           - 질투: 편애를 안 받으면 서서히 식음(성격별 decay 절반).
           tension 감소를 1~2로 낮춘 것이 '연합/견제가 실제로 발생'하는 핵심."""
        for (a, b), r in rels.items():
            r["t"] = clamp(r["t"] - 2)
        for h in heroines.values():
            h.jealousy = clamp(h.jealousy - max(1, h.tension_decay // 3))

    # -------------------------------------------------------------
    #  엔딩 평가 (설계 7장) — 최종 상태로 계산
    # -------------------------------------------------------------

    def evaluate_ending():
        all_aff = [h.affection for h in heroines.values()]
        all_ten = [r["t"] for r in rels.values()]

        # [하렘] 수용도 높고 + 모두 호감 충분 + 모든 긴장 낮음
        if (store.harem_acceptance >= 70
                and min(all_aff) >= 60
                and (max(all_ten) if all_ten else 0) <= 30):
            return ("harem", "하렘 엔딩 — 모두가 당신을 받아들였다.")

        top = max(heroines.values(), key=lambda h: h.affection)

        # [배드/파국] 질투 폭주
        jmax = max(heroines.values(), key=lambda h: h.jealousy)
        if jmax.jealousy >= 85 and jmax.id != top.id:
            return ("bad", "배드 엔딩 — %s 의 질투가 모든 걸 무너뜨렸다." % jmax.name)

        # [개별 굿] 최고 호감 히로인
        if top.affection >= 60:
            return ("good_%s" % top.id, "%s 엔딩 — 두 사람은 이어졌다." % top.name)

        # [노멀] 아무도 임계 못 넘음
        return ("normal", "노멀 엔딩 — 혼자서 졸업식을 맞이했다.")
