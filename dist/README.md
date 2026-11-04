# 실행 파일 (프로토타입 빌드)

관계·질투 시스템 최소 프로토타입의 실행 가능한 빌드입니다.
디자인 요소는 플레이스홀더(표준 Ren'Py GUI + 본고딕 폰트)이며, 로직 검증용입니다.

## 플랫폼별 실행 방법

| 파일 | 플랫폼 | 실행 |
|------|--------|------|
| `relationship_vn_proto-0.0.1-win.zip` | Windows | 압축 해제 후 `relationship_vn_proto.exe` 실행 |
| `relationship_vn_proto-0.0.1-mac.zip` | macOS | 압축 해제 후 `.app` 실행 |
| `relationship_vn_proto-0.0.1-linux.tar.bz2` | Linux | 압축 해제 후 `relationship_vn_proto.sh` 실행 |

> Ren'Py 8.1.3 으로 빌드. (통합 PC 빌드와 마켓 빌드는 용량 관계로 제외했습니다.)

## 플레이 방법

1. 게임 실행 → 시작
2. 슬롯마다 "누구와 시간을 보낼까?" 선택
   - 특정 히로인 편애 → 그 히로인 호감↑ + 다른 히로인 질투↑
   - "모두에게 공평하게" → 질투 완화 + 하렘 수용도↑
3. 매 슬롯 종료 시 현재 상태(호감/질투/수용도)와
   견제·연합 발생 여부가 표시됨
4. 전체 슬롯(8회) 종료 시 상태에 따라 엔딩 결정
   (하렘 / 개별 굿 / 배드 / 노멀)

## 재현 빌드

소스에서 직접 빌드하려면 Ren'Py 8.x SDK 설치 후:
```
renpy.sh <SDK>/launcher distribute <이 저장소 루트>
```
