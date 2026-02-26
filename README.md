# 🚑 PYGAME <br> (Paramedics! Yield to Guardians Against Medical Emergencies!)

**PyGame 미니 프로젝트: 환자 이송 게임 만들기**

[![Python Version](https://img.shields.io/badge/python-3.13.5-blue.svg)](https://python.org)
[![PyGame](https://img.shields.io/badge/pygame-project-yellow.svg)](https://www.pygame.org/)

**팀명**: PYGAME (아시아경제 메디컬 4기 세미1 3팀)  
**팀원**: 팀장(AA) 이충환, AA 이승원, TA 이다혜  

Python과 PyGame을 활용하여 제작한 교육용 구급차 시뮬레이션 게임 **'PYGAME (Paramedics! Yield to Guardians Against Medical Emergencies!)'** 의 프로젝트 저장소입니다.

---

## 1. 💡 기획 및 시나리오

* **기획 의도**: 응급 상황 발생 시 **골든타임** 내에 빠른 처치가 생명을 좌우하는 중요성을 인식시키고, 긴급차량에 대한 우선 통행 비협조 문제(경찰차 논란 사례 등)를 해결하기 위해 기획되었습니다.
* **게임 목적**: **골든타임**이라는 제한된 시간 내에 도로 위의 장애물을 피해 환자를 제시간에 무사히 병원으로 이송하는 것입니다.
* **사전 조사**: 응급 환자의 구분은 KTAS(한국형 응급환자 분류도구) 분류 기준을 따랐으며, 2024년 통계에서 전국 구급차의 절반 이상이 환자에게 제시간에 도착하지 못하는 현실적인 문제점을 게임 배경에 반영했습니다.

---

## 2. 🎮 게임 소개 및 기능

* **게임명**: PYGAME (Paramedics! Yield to Guardians Against Medical Emergencies!)
* **장르**: 교육용 아케이드 게임
* **개발 환경**: Python 3.13.5 / VS Code
* **화면 구성 (인터페이스)**
  * 스테이지 및 현재 중증 질환 / KTAS 등급 표시
  * 획득 시 클리어되는 **병원 아이콘**
  * 충돌 시 감소하는 **체력 개수** 표시
  * 남은 시간을 보여주는 **타이머** 및 **필살기(사이렌)** 보유 상태
  * 방해 요소 요소인 **장애물** (차량, 표지판 등)과 플레이어가 조작하는 **구급차**
* **조작키**
  * `←`, `→` : 구급차 좌우 이동
  * `Space` : 사이렌 작동 (필살기 - 화면 내의 모든 장애물이 즉시 제거됨)

### 🚨 스테이지별 정보
| 스테이지 | 질환 및 분류 | 제한 시간 |
| :---: | :--- | :---: |
| **Stage 1** | 뇌졸중 (**KTAS: 긴급**) | 30초 |
| **Stage 2** | 중증 외상 (**KTAS: 긴급**) | 25초 |
| **Stage 3** | 심정지 (**KTAS: 소생**) | 10초 |

* **필살기(사이렌) 조건**: 장애물을 5회 연속 회피할 경우 사이렌(필살기) 1회가 충전됩니다.

---

## 3. 🔄 플로우차트 (Flowchart)

1. **Game Start 클릭**
2. ➡️ **질환별 골든타임 퀴즈** (정답을 맞혀야 게임 환경에 진입 가능)
3. ➡️ **본 게임 진행** (좌우 방향키를 활용해 주행)
4. ➡️ **장애물 조우**
   * **충돌 시**: 체력 감소 (체력이 0이 되면 `Game Over`)
   * **회피 시**: 5회 무사 회피 시 필살기(사이렌) 아이템 생성
5. ➡️ **병원 도착** (스테이지 3까지 모두 돌파하면 `Game Clear`)

---

## 4. 🛠️ 기술 스택 및 주요 구현 요소

* **언어 및 라이브러리**: Python 3.13.5, PyGame
* **객체 지향 모델링 (OOP)**: `pygame.sprite.Sprite`를 상속받아 구급차(`PlayerVehicle`), 방해 차량(`Vehicle`), 목적지(`Hospital`) 등의 엔티티를 모듈화하고 스프라이트 그룹으로 묶어 렌더링 파이프라인을 최적화했습니다.
* **이벤트 구동 아키텍처 (Event-Driven)**: `pygame.event.get()`을 통해 마우스 클릭(UI 상호작용 및 퀴즈)과 키워드 입력(방향키 이동, 스페이스바 스킬)을 실시간으로 감지하고 분기 상태(초기 화면, 퀴즈 단계, 인게임 레이싱) 간 전환 루프를 처리합니다.
* **정밀한 렉트(Rect) 충돌 판정**: `pygame.sprite.spritecollide()` 로직을 활용하여 무작위 좌표에서 떨어지는 장애물과 구급차 오브젝트 간의 충돌 영역 교집합을 정확히 계산해 체력 하트 시스템에 반영했습니다.
* **타이머 및 동적 난이도 스케일링**: `pygame.time.get_ticks()` 및 `time.time()`을 조합하여 스테이지별 골든타임을 추적합니다. 프레임 경과 시간에 비례하여 스크롤 스피드를 점진적으로 높이는 알고리즘을 도입해 긴박한 난이도 설계를 구현했습니다.
* **동적 렌더링 및 시각 효과**: 초당 120프레임(`pygame.time.Clock`)의 부드러운 화면을 제공합니다. 특히 **남은 시간이 줄어들수록 타이머의 색상이 '초록색 ➡️ 노란색 ➡️ 빨간색' 순으로 변하도록** 디자인하여, 플레이어가 긴박한 상황을 직관적으로 느낄 수 있게 했습니다. 또한 `pygame.mixer` 모듈을 활용한 효과음과 해상도에 맞춘 그래픽 요소들을 적용해 몰입감을 높였습니다.

---

## 5. 🌟 게임 활용 및 기대 효과

* **교육적 효과 극대화**: 중증 질환별 골든타임을 플레이어가 직접 체감할 수 있게 교육하고, '시간이 줄어드는 압박감'을 통해 통과함으로써 생명의 소중함과 응급구조대의 막중한 책임감을 깊이 각인시킵니다.
* **시민의식 개선**: 긴급차량의 우선 통행 협조에 대한 필요성을 환기시키고 불법 주정차의 심각성을 간접적으로 겪도록 하여 성숙한 시민 의식을 조성하는 효과를 기대할 수 있습니다.

---

## 6. 🔗 링크 및 자료

* 📥 **게임 플레이 파일**: [Google Drive 링크](https://drive.google.com/file/d/12j-dLCgtlBUXx03O5vuu3zFv3X1QPadX/view?usp=drive_link)
* 📄 **프로젝트 기획안**: [Google Drive 링크](https://docs.google.com/document/d/1XK_EBGhVR2V4WVNj4h9NOL62Y6-eCB7JAbf3kJJEEbk/edit?usp=drive_link)
* 📊 **발표 자료**:
  * [PPT 보기 (Google Slides)](https://docs.google.com/presentation/d/1RKz149_N48ay9aDfaBS34H3UiVk8aZ8GbrV_SuZA6zk/edit?usp=drive_link)
  * [PDF 다운로드 (Google Drive)](https://drive.google.com/file/d/1TbUBW9PvNKOi44PRwGicIKUmCwa6w_65/view?usp=drive_link)
* 🎬 **시연 영상**: [Google Drive 링크](https://drive.google.com/file/d/1dglFAZK7H0RgfRZSPC2nccm7OPdZavpF/view?usp=drive_link)



