# =============================================================
#  script.rpy  —  최소 프로토타입 메인 흐름
#
#  목적: 질투 시스템이 "실제로 도는" 것을 확인하는 수직 슬라이스.
#  흐름: 슬롯마다 [히로인과 데이트 / 공평하게] 선택
#        → 호감·질투·긴장 변동 → 연합/견제 판정 → 상태 표시
#        → 지정한 슬롯 수가 끝나면 엔딩 평가
#
#  아트 없음(플레이스홀더). 로직 검증용.
# =============================================================

define TOTAL_SLOTS = 8        # 프로토타입 길이 (실제 게임은 훨씬 김)
define SLOTS_PER_DAY = 3      # 하루 = 3슬롯 (방과후/야자/저녁)

default turn_index = 1        # 1 .. TOTAL_SLOTS (전체 슬롯 카운터)

label start:

    scene black
    "── 관계 중심 미연시 · 로직 프로토타입 ──"
    "고3의 1년. 크리스마스 고백까지, 당신의 선택이 그녀들의 관계를 바꾼다."
    "(이 프로토타입은 질투·연합·견제 시스템이 도는지 확인하는 용도입니다.)"

    jump main_loop

label main_loop:

    # 전체 슬롯을 다 쓰면 엔딩
    if turn_index > TOTAL_SLOTS:
        jump ending

    # 절반 지나면 수능 후로 전환 (phase 데모)
    if turn_index == (TOTAL_SLOTS // 2) + 1 and phase == "pre_exam":
        $ phase = "post_exam"
        "── 수능이 끝났다. 이제 시간이 많아졌다. (phase: 수능후) ──"

    $ phase_label = u"수능전" if phase == "pre_exam" else u"수능후"
    "[[Day [day] / Slot [slot] / [phase_label]]  ([turn_index]/[TOTAL_SLOTS])"

    menu:
        "누구와 시간을 보낼까?"

        "[heroines['A'].name] 와(과) 데이트":
            $ result = do_action_date("A")
        "[heroines['B'].name] 와(과) 데이트":
            $ result = do_action_date("B")
        "[heroines['C'].name] 와(과) 데이트":
            $ result = do_action_date("C")
        "[heroines['D'].name] 와(과) 데이트":
            $ result = do_action_date("D")
        "모두에게 공평하게 (하렘 수용도↑)":
            $ result = do_action_fair()

    # 행동 결과 로그 출력
    python:
        for line in result:
            renpy.say(None, line)

    # 슬롯 종료: 상태 + 연합/견제 판정
    call relationship_report from _call_rel_report

    # 시간 진행
    python:
        end_of_slot_decay()
        store.turn_index += 1
        store.slot += 1
        if store.slot > SLOTS_PER_DAY:
            store.slot = 1
            store.day += 1

    jump main_loop


# ---- 슬롯 종료 리포트: 상태 + 연합/견제 판정 ----
label relationship_report:

    python:
        status = u"현재 상태 ─\n"
        for hid in ["A", "B", "C", "D"]:
            h = heroines[hid]
            status += u"  {}: 호감 {} / 질투 {}\n".format(
                h.name, int(h.affection), int(h.jealousy))
        status += u"  하렘 수용도: {}".format(int(store.harem_acceptance))
    "[status]"

    python:
        snipes = check_snipe()
        alliance = check_alliance()

    if snipes:
        python:
            a, b = snipes[0]
            msg = u"{na} 와(과) {nb}, 웃고 있지만 눈이 웃지 않는다… (견제 발생)".format(
                na=heroines[a].name, nb=heroines[b].name)
        "[msg]"

    if alliance:
        python:
            leader, members = alliance
            mnames = u" · ".join(heroines[m].name for m in members)
            amsg = u"{ms} 이(가) {ld} 의 독주를 막으려 손을 잡았다… (연합 발생)".format(
                ms=mnames, ld=heroines[leader].name)
        "[amsg]"

    return


# ---- 엔딩 ----
label ending:

    "── 12월 25일, 크리스마스. 그리고 2월, 졸업식. ──"

    python:
        tag, text = evaluate_ending()
    "[text]"

    "── 프로토타입 종료 (엔딩 태그: [tag]) ──"

    return
