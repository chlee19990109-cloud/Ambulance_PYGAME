# PyGame 미니 프로젝트: 환자 이송 게임 만들기

팀명: PYGAME (아시아경제 메디컬 4기 세미1 3팀)

팀원: AA 및 팀장 이충환, AA 이승원, TA 이다혜

PyGame을 활용하여 제작한 'PYGAME (Paramedics! Yield to Guardians Against Medical Emergencies!)'이라는 교육용 게임에 대한 코드 및 발표 자료입니다.


**1. 기획 및 시나리오**
  * **기획 의도:** 응급 상황 발생 시 '골든타임' 내에 빠른 처치가 생명을 좌우하는 중요성을 인식시키고, 긴급차량에 대한 우선 통행 비협조 문제(경찰차 논란 사례 언급)를 해결하기 위해 기획되었습니다.
  * **게임 목적:** 골든타임 내에 장애물을 피해 환자를 제시간에 이송하는 것입니다.
  * **사전 조사:** 응급 환자의 구분은 KTAS 분류 기준에 따르며, 2024년 통계에서 전국 자료 중 절반 이상이 제시간에 도착하지 못하는 문제점이 확인되었습니다.


**2. 게임 소개 및 기능**
  * **게임 속성:**
      * **게임명:** PYGAME (Paramedics\! Yield to Guardians Against Medical Emergencies\!)
      * **장르:** 교육용 게임
      * **개발 환경:** Python 3.13.5 / VS Code
  * **화면 구성 (인터페이스):** 스테이지 표시, 중증 질환/KTAS 등급 표시, 병원 아이콘 (획득 시 클리어), 체력 개수 (충돌 시 감소), 필살기/타이머, 장애물 (차량, 표지판), 구급차로 구성됩니다.
  * **조작키:** Move: ←→, Space: 사이렌 (모든 장애물 제거).
  * **스테이지별 정보:**
      * Stage 1: 뇌졸증 (KTAS: 긴급), 제한 시간 30초.
      * Stage 2: 중증 외상 (KTAS: 긴급), 제한 시간 25초.
      * Stage 3: 심정지 (KTAS: 소생), 제한 시간 10초.
  * **필살기 조건:** 장애물 5회 회피 시 필살기(사이렌) 1회 충전.


**3. 플로우차트**
  * 'game start' 클릭 → 질환별 골든타임 퀴즈 (정답 시 게임 진행) → 게임 진행 (방향키: 좌우 이동) → 물체 충돌 (체력 감소, 체력\<1이면 게임 오버) 또는 물체 회피 5회 (필살기 생성) → 병원 도착 (스테이지 3이면 게임 클리어).


**4. 게임 활용 및 기대 효과**
  * 중증 질환별 골든타임을 교육하고, '시간이 줄어드는 압박'을 통해 생명의 소중함과 응급구조대의 책임감을 각인시키는 교육적 효과가 기대됩니다.
  * 긴급차량의 우선 통행 협조 인식 강화 및 불법 주정차의 심각성을 간접적으로 체감하여 시민의식을 개선하는 효과를 기대합니다.





게임 파일: https://drive.google.com/file/d/12j-dLCgtlBUXx03O5vuu3zFv3X1QPadX/view?usp=drive_link

프로젝트 기획안: https://drive.google.com/file/d/1vRSwhpQz-n4YmiBMbc3uSGyo8Jp6yIgi/view?usp=drive_link

발표 자료:

ppt - https://docs.google.com/presentation/d/1RKz149_N48ay9aDfaBS34H3UiVk8aZ8GbrV_SuZA6zk/edit?usp=drive_link

pdf - https://drive.google.com/file/d/1TbUBW9PvNKOi44PRwGicIKUmCwa6w_65/view?usp=drive_link
