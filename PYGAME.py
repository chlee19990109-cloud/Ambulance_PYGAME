import pygame
from pygame.locals import *
import random
import time

# Pygame 초기화
pygame.init()

# ----------------------------------------------------------------------
# 1. 게임 설정
# ----------------------------------------------------------------------

# 윈도우 생성
width = 500
height = 500
screen_size = (width, height)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("PYGAME")

# 색상 정의
gray = (100, 100, 100)
green = (76, 208, 56)
red = (200, 0, 0)
white = (255, 255, 255)
yellow = (255, 232, 0) # 노란색 추가
black = (0, 0, 0)

# 도로 및 마커 크기
road_width = 300
marker_width = 10
marker_height = 50

# 차선 좌표
left_lane = 150
center_lane = 250
right_lane = 350
lanes = [left_lane, center_lane, right_lane]

# 도로 및 가장자리 마커 위치
road = (100, 0, road_width, height)
left_edge_marker = (95, 0, marker_width, height)
right_edge_marker = (405, 0, marker_width, height)

# 차선 마커 애니메이션을 위한 변수
lane_marker_move_y = 0

# 플레이어 시작 위치
player_x = 250
player_y = 400

# 프레임 설정
clock = pygame.time.Clock()
fps = 120

# 게임 상태 변수
gameover = False
game_success = False
initial_start = True # 시작 화면 표시 여부
speed = 2
speed_increase_count = 0 # 속도 증가 횟수 (10초 감소 시마다 1씩 증가)
collision_count = 0 # 충돌 횟수 (하트)

# 필살기 (사이렌) 관련 변수
special_skill_count = 0 # 현재 보유한 필살기 횟수
vehicles_dodged_since_last_charge = 0 # 충전까지 남은 회피 횟수

# 타이머 관련 변수
start_ticks = pygame.time.get_ticks()
max_time = 30
remaining_time = max_time

# 스테이지 관련 변수
stage = 1
stage_time_limits = {1: 30, 2: 25, 3: 10}
stage_finished = False
hospital_spawn_time = {1: 13, 2: 8, 3: 5} # 남은 시간 기준 병원 생성 시점

# 퀴즈 관련 변수
stage_quizzes = {
 1: {
  "question": "1단계 퀴즈: 뇌졸중의 골든타임은?",
  "options": ["1. 200(분)", "2. 180(분)", "3. 160(분)"],
  "answer": 2,
 }, # 정답: 2. 180(분)
 2: {
  "question": "2단계 퀴즈: 중증외상의 골든타임은?",
  "options": ["1. 60(분)", "2. 45(분)", "3. 30(분)"],
  "answer": 1,
 }, # 정답: 1. 60(분)
 3: {
  "question": "3단계 퀴즈: 심정지의 골든타임은?",
  "options": ["1. 6(분)", "2. 5(분)", "3. 4(분)"],
  "answer": 3,
 }, # 정답: 3. 4(분)
}
quiz_active = False # 퀴즈 화면 활성화 여부
current_quiz_data = stage_quizzes[stage]
current_question = current_quiz_data["question"]
current_options = current_quiz_data["options"]
current_answer = current_quiz_data["answer"]

feedback_text = ""
feedback_start_time = 0

# 퀴즈 버튼 테두리 관련 변수
selected_option_index = -1 # -1: 선택 안됨, 0부터 시작
highlight_end_time = 0.0

# 폰트 설정 (한글 폰트 로드 시도, 실패 시 기본 폰트 사용)
try:
 hangeul_font = pygame.font.Font("C:/Windows/Fonts/malgun.ttf", 20)
 quiz_font = hangeul_font
 game_font_big = pygame.font.Font("C:/Windows/Fonts/malgun.ttf", 28)
 game_font_small = pygame.font.Font("C:/Windows/Fonts/malgun.ttf", 16)

except FileNotFoundError:
 print("시스템 폰트(malgun.ttf)를 찾을 수 없습니다. 기본 폰트로 대체합니다.")
 quiz_font = pygame.font.Font(pygame.font.get_default_font(), 20)
 game_font_big = pygame.font.Font(pygame.font.get_default_font(), 28)
 game_font_small = pygame.font.Font(pygame.font.get_default_font(), 16)


# 🔹 배경 이미지 로드
image_path = "resources/"
try:
 s_d_background = pygame.image.load(image_path + "s_d.png")
 s_d_background = pygame.transform.scale(s_d_background, screen_size)
 startbar_img_orig = pygame.image.load(image_path + "startbar.png")
 startbar_width = int(width * 0.7)
 startbar_height = 150
 startbar_img = pygame.transform.scale(
  startbar_img_orig, (startbar_width, startbar_height)
 )

 start_background = pygame.image.load(image_path + "start.png")
 start_background = pygame.transform.scale(start_background, (width, height))
 mid_background = pygame.image.load(image_path + "mid.png")
 mid_background = pygame.transform.scale(mid_background, (width, height))

 finish_line = pygame.image.load(image_path + "finish_line.png")
 finish_line = pygame.transform.scale(finish_line, (width, height))

except pygame.error as e:
 print(f"이미지 로드 오류: {e}. 'images' 폴더에 파일이 있는지 확인하세요.")
 s_d_background = pygame.Surface(screen_size)
 s_d_background.fill(black)
 startbar_img = pygame.Surface((100, 30))
 startbar_img.fill(white)
 start_background = pygame.Surface(screen_size)
 start_background.fill(black)
 mid_background = pygame.Surface(screen_size)
 mid_background.fill(black)
 finish_line = pygame.Surface((width, height))
 finish_line.fill(green)

# 오디오 초기화 및 로드
pygame.mixer.init()
try:
 siren_sound = pygame.mixer.Sound(image_path + "siren.mp3")
except pygame.error as e:
 print(
  f"사이렌 오디오 로드 오류: {e}. 'siren.mp3' 파일이 코드 폴더에 있는지 확인하세요."
 )
 siren_sound = pygame.mixer.Sound(pygame.Surface((1, 1))) # 더미 사운드

siren_playing = False
siren_start_time = 0


# 시간 바 이미지 로드
try:
 red_bar_img = pygame.image.load(image_path + "redbar.png")
 yellow_bar_img = pygame.image.load(image_path + "yellowbar.png")
 green_bar_img = pygame.image.load(image_path + "greenbar.png")
except pygame.error as e:
 print(f"시계바 이미지 로드 오류: {e}. 'images' 폴더에 파일이 있는지 확인하세요.")
 red_bar_img = pygame.Surface((150, 40))
 red_bar_img.fill(red)
 yellow_bar_img = pygame.Surface((150, 40))
 yellow_bar_img.fill(yellow)
 green_bar_img = pygame.Surface((150, 40))
 green_bar_img.fill(green)


# 하트 이미지 로드
try:
 heart_img_orig = pygame.image.load(image_path + "h.png")
 heart_size = 40
 heart_img = pygame.transform.scale(heart_img_orig, (heart_size, heart_size))
except pygame.error as e:
 print(f"하트 이미지 로드 오류: {e}. 'images' 폴더에 파일이 있는지 확인하세요.")
 heart_img = pygame.Surface((heart_size, heart_size))
 heart_img.fill(red)


# 하트 표시 함수
def draw_hearts(screen, collision_count):
 max_hearts = 2
 hearts_to_draw = max_hearts - collision_count

 start_x = width - (heart_size * max_hearts) - 30
 start_y = 20

 for i in range(max(0, hearts_to_draw)):
  screen.blit(heart_img, (start_x + i * (heart_size + 5), start_y))

 heart_rect_width = max_hearts * heart_size + (max_hearts - 1) * 5
 return pygame.Rect(start_x, start_y, heart_rect_width, heart_size)


# mid 표시 플래그 및 텍스트 지속시간
mid_shown_for_stage = {1: False, 2: False, 3: False}
show_mid_text = False
mid_text_start_time = 0
current_background = start_background

# ----------------------------------------------------------------------
# 2. 스프라이트 클래스 정의
# ----------------------------------------------------------------------


# 일반 차량 클래스
class Vehicle(pygame.sprite.Sprite):
 def __init__(self, image, x, y):
  pygame.sprite.Sprite.__init__(self)
  image_scale = 45 / image.get_rect().width
  new_width = int(image.get_rect().width * image_scale)
  new_height = int(image.get_rect().height * image_scale)
  self.image = pygame.transform.scale(image, (new_width, new_height))
  self.rect = self.image.get_rect()
  self.rect.center = [x, y]


# 플레이어 차량 (구급차) 클래스
class PlayerVehicle(Vehicle):
 def __init__(self, x, y):
  self.image_default = pygame.image.load(image_path + "a.png")
  self.image_siren = pygame.image.load(image_path + "a1.png")
  super().__init__(self.image_default, x, y)
  self.siren_mode = False
  self.siren_start = 0

 # 사이렌 모드 활성화 (필살기)
 def activate_siren(self):
  self.siren_mode = True
  self.siren_start = time.time()
  self.image = pygame.transform.scale(self.image_siren, self.image.get_size())

 # 업데이트: 사이렌 모드 시간 확인
 def update(self):
  if self.siren_mode and (
  time.time() - self.siren_start >= 3
  ): # 3초 후 사이렌 비활성화
   self.siren_mode = False
   self.image = pygame.transform.scale(
    self.image_default, self.image.get_size()
   )


player_group = pygame.sprite.Group()
vehicle_group = pygame.sprite.Group()
player = PlayerVehicle(player_x, player_y)
player_group.add(player)

# 장애물 차량 이미지 로드
image_filenames = [
 "car4.png",
 "car6.png",
 "car7.png",
 "car9.png",
 "car13.png",
 "taxi.png",
 "conn.png",
]
vehicle_images = []
for image_filename in image_filenames:
 image = pygame.image.load(image_path + image_filename)
 vehicle_images.append(image)

# 충돌, 병원 이미지 로드
try:
 crash = pygame.image.load(image_path + "crash.png")
 hospital_image = pygame.image.load(image_path + "hospital.png")
except pygame.error as e:
 print(f"충돌/병원 이미지 로드 오류: {e}")
 crash = pygame.Surface((50, 50))
 crash.fill(red)
 hospital_image = pygame.Surface((50, 50))
 hospital_image.fill(white)

crash_rect = crash.get_rect()


# 병원 (목표 지점) 클래스
class Hospital(pygame.sprite.Sprite):
 def __init__(self, x, y):
  pygame.sprite.Sprite.__init__(self)
  image = hospital_image
  image_scale = 45 / image.get_rect().width
  new_width = int(image.get_rect().width * image_scale)
  new_height = int(image.get_rect().height * image_scale)
  self.image = pygame.transform.scale(image, (new_width, new_height))
  self.rect = self.image.get_rect()
  self.rect.center = [x, y]

 # 업데이트: 속도에 따라 아래로 이동
 def update(self):
  self.rect.y += speed


hospital_group = pygame.sprite.Group()
hospital_spawned = False

obstacles_spawned_for_stage = {1: False, 2: False, 3: False}
random_vehicle_spawned = False # 무작위 차량 생성 플래그

# ----------------------------------------------------------------------
# 3. 렌더링 및 상태 관리 함수
# ----------------------------------------------------------------------


# 퀴즈 화면 렌더링 함수
def draw_quiz_screen(screen, background, question, options, feedback, selected_index, highlight_time):
 screen.blit(background, (0, 0))
 option_rects = []

 # 질문 텍스트
 text_surface = game_font_big.render(question, True, black)
 screen.blit(
  text_surface, (width // 2 - text_surface.get_width() // 2, height // 2 - 100)
 )

 # 옵션 버튼 렌더링
 button_width = 150
 button_height = 40
 start_y = height // 2
 padding = 10

 current_time = time.time()

 for i, option in enumerate(options):
  button_x = width // 2 - button_width // 2
  button_y = start_y + i * (button_height + padding)
  button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

  pygame.draw.rect(screen, gray, button_rect, 0, 5)

  # 선택된 버튼이고, 강조 시간이 지나지 않았다면 노란색 테두리
  if i == selected_index and current_time < highlight_time:
   pygame.draw.rect(screen, yellow, button_rect, 4, 5) # 노란색 테두리 (두껍게)
  else:
   pygame.draw.rect(screen, black, button_rect, 2, 5) # 기본 검은색 테두리

  option_surface = quiz_font.render(option, True, white)
  option_rect = option_surface.get_rect(center=button_rect.center)
  screen.blit(option_surface, option_rect)

  option_rects.append(button_rect)

 # 피드백 텍스트 (정답/오답)
 feedback_surface = quiz_font.render(
  feedback, True, red if "오답" in feedback else yellow
 )
 screen.blit(
  feedback_surface,
  (width // 2 - feedback_surface.get_width() // 2, height // 2 + 180),
 )

 return option_rects


# 시계바 렌더링 함수 (타이머 시각화)
def draw_time_bar(screen, remaining_time, total_time, stage):
 bar_width = 330
 bar_height = 40
 bar_x = 70
 bar_y = 440

 # 남은 시간에 따라 바의 색상 변경
 if stage == 1:
  if remaining_time > 15:
   bar_image = red_bar_img
  elif remaining_time > 7:
   bar_image = yellow_bar_img
  else:
   bar_image = green_bar_img
 elif stage == 2:
  if remaining_time > 10:
   bar_image = red_bar_img
  elif remaining_time > 5:
   bar_image = yellow_bar_img
  else:
   bar_image = green_bar_img
 elif stage == 3:
  if remaining_time > 5:
   bar_image = red_bar_img
  elif remaining_time > 2:
   bar_image = yellow_bar_img
  else:
   bar_image = green_bar_img
 else:
  bar_image = red_bar_img

 bar_image_scaled = pygame.transform.scale(bar_image, (bar_width, bar_height))
 screen.blit(bar_image_scaled, (bar_x, bar_y))


# 게임 상태 초기화 및 다음 스테이지 준비 함수
def reset_game_state(new_stage):
 global gameover, game_success, stage, speed, hospital_spawned, start_ticks, obstacles_spawned_for_stage, mid_shown_for_stage, show_mid_text, current_background, quiz_active, current_question, current_options, current_answer, feedback_text, stage_finished, collision_count
 global special_skill_count, vehicles_dodged_since_last_charge
 global random_vehicle_spawned
 global initial_start
 global speed_increase_count
 global selected_option_index, highlight_end_time # 추가

 # 스테이지 설정 및 초기화
 stage = new_stage
 gameover = False
 game_success = False
 stage_finished = False
 speed = 2
 vehicle_group.empty()
 hospital_group.empty()
 hospital_spawned = False
 speed_increase_count = 0 # 속도 증가 카운트 초기화

 # 퀴즈 재설정
 quiz_active = True
 current_quiz_data = stage_quizzes[stage]
 current_question = current_quiz_data["question"]
 current_options = current_quiz_data["options"]
 current_answer = current_quiz_data["answer"]

 feedback_text = ""
 current_background = start_background

 # 플레이어 스프라이트 다시 생성
 global player
 player = PlayerVehicle(player_x, player_y)
 player_group.empty()
 player_group.add(player)

 obstacles_spawned_for_stage = {1: False, 2: False, 3: False}
 mid_shown_for_stage = {1: False, 2: False, 3: False}
 show_mid_text = False
 collision_count = 0

 # 필살기 재설정
 special_skill_count = 0
 vehicles_dodged_since_last_charge = 0
 random_vehicle_spawned = False
 # 타이머 리셋
 start_ticks = pygame.time.get_ticks()

 # 퀴즈 버튼 하이라이트 리셋
 selected_option_index = -1
 highlight_end_time = 0.0


# ----------------------------------------------------------------------
# 4. 메인 게임 루프
# ----------------------------------------------------------------------

running = True
option_rects = []
startbar_rect = startbar_img.get_rect(center=(width // 2, height // 2.5))

while running:
 clock.tick(fps)

 # 이벤트 처리
 for event in pygame.event.get():
  if event.type == QUIT:
   running = False

  # 초기 시작 화면 상태 처리
  if initial_start:
   if event.type == MOUSEBUTTONDOWN:
    pos = pygame.mouse.get_pos()
    if startbar_rect.collidepoint(pos):
     initial_start = False
     quiz_active = True
     current_quiz_data = stage_quizzes[stage]
     current_question = current_quiz_data["question"]
     current_options = current_quiz_data["options"]
     current_answer = current_quiz_data["answer"]

  # 퀴즈 활성화 상태 처리 (객관식)
  # 퀴즈 정답 후 피드백이 표시되는 중에는 마우스 클릭 처리를 막지 않습니다.
  elif quiz_active or (feedback_text and time.time() - feedback_start_time < 1.5):
   if event.type == MOUSEBUTTONDOWN:
    pos = pygame.mouse.get_pos()

    # 이미 피드백 표시 중이면 새로운 클릭 처리는 무시
    if feedback_text and time.time() - feedback_start_time < 1.5:
     continue

    for i, rect in enumerate(option_rects):
     if rect.collidepoint(pos):
      # 버튼 클릭 시 노란색 하이라이트 시작
      selected_option_index = i
      highlight_end_time = time.time() + 0.15 # 0.15초 동안 노란색 테두리 유지

      selected_answer = i + 1

      if selected_answer == current_answer:
       # 정답 시 퀴즈 종료 및 게임 시작 준비
       quiz_active = False # 플래그만 변경
       start_ticks = pygame.time.get_ticks()
       feedback_text = "정답! 게임을 시작합니다."
       feedback_start_time = time.time()
      else:
       # 오답 시 피드백
       feedback_text = "오답입니다. 다시 시도하세요."
       feedback_start_time = time.time()
      break

  # 게임 중인 상태 처리 (키 입력) - 퀴즈가 비활성화되고 게임 오버/성공이 아닐 때
  # ⭐ 게임 시작 후 키 입력을 여기서 처리합니다.
  elif not quiz_active and not gameover and not game_success:
   if event.type == KEYDOWN:
    if player in player_group:
     if event.key == K_LEFT and player.rect.center[0] > left_lane:
      player.rect.x -= 100
     elif event.key == K_RIGHT and player.rect.center[0] < right_lane:
      player.rect.x += 100
     elif event.key == K_SPACE and not player.siren_mode:
      if special_skill_count > 0:
       player.activate_siren()
       siren_sound.play()
       siren_playing = True
       siren_start_time = time.time()
       for v in list(vehicle_group):
        v.kill()
       special_skill_count -= 1

 # 초기 시작 화면 렌더링
 if initial_start:
  screen.blit(s_d_background, (0, 0))
  screen.blit(startbar_img, startbar_rect)
  pygame.display.update()
  continue

 # 퀴즈 화면 렌더링 (quiz_active가 True이거나, 피드백 표시 중일 때)
 # 정답을 맞혀 quiz_active가 False가 되었더라도 피드백 표시 시간 동안은 퀴즈 화면을 유지합니다.
 if quiz_active or (
  feedback_text and time.time() - feedback_start_time < 1.5
 ):
  # 퀴즈 화면 렌더링 시 하이라이트 관련 변수 전달
  option_rects = draw_quiz_screen(
   screen, start_background, current_question, current_options, feedback_text, selected_option_index, highlight_end_time
  )

  # 피드백 표시 시간이 끝나면 피드백 텍스트와 하이라이트 해제
  if feedback_text and (time.time() - feedback_start_time >= 1.5):
   feedback_text = ""
   selected_option_index = -1
   # 피드백 종료 후, 루프를 종료하지 않고 아래의 게임 로직으로 넘어갑니다.

  # 하이라이트 시간(0.15초)이 지났으면 하이라이트 해제 (오답의 경우)
  if time.time() > highlight_end_time:
   selected_option_index = -1
   
  pygame.display.update()
  
  # 피드백이 아직 표시 중이거나(feedback_text != "") 퀴즈가 활성화 상태(quiz_active == True)일 때만 continue를 실행합니다.
  if quiz_active or (feedback_text != ""):
   continue 

 # ----------------------------------------------------------------------
 # 게임 로직
 # ----------------------------------------------------------------------
 # ⭐ 퀴즈 화면이 아닌, 실제 게임 로직을 실행하는 메인 블록입니다.

 # 사이렌 3초 지속 후 종료
 if siren_playing and time.time() - siren_start_time >= 3:
  siren_sound.stop()
  siren_playing = False

 # 타이머 계산
 elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
 remaining_time = stage_time_limits[stage] - elapsed_time

 # 남은 시간이 10초 감소할 때마다 속도 증가 로직
 time_decreased = stage_time_limits[stage] - remaining_time
 increase_check = int(time_decreased // 10) # 10초 감소한 횟수

 if increase_check > speed_increase_count and increase_check > 0:
  speed += 1
  speed_increase_count = increase_check # 속도 증가 횟수를 업데이트합니다.


 # 무작위 차량 일괄 생성 (게임 중반)
 time_for_random_spawn = stage_time_limits[stage] - 13

 if (
  remaining_time <= time_for_random_spawn
  and not random_vehicle_spawned
  and not game_success
 ):

  target_spawn_count = random.randint(3, 7)
  current_spawn_count = 0
  max_attempts = 50

  while current_spawn_count < target_spawn_count and max_attempts > 0:

   lane_choice = random.choice(lanes)
   image_choice = random.choice(vehicle_images)
   y_offset = -random.randint(50, 400)

   new_v = Vehicle(image_choice, lane_choice, y_offset)
   colliding_vehicles = pygame.sprite.spritecollide(
    new_v, vehicle_group, False
   )

   if not colliding_vehicles:
    vehicle_group.add(new_v)
    current_spawn_count += 1
   else:
    new_v.kill()

   max_attempts -= 1

  random_vehicle_spawned = True

 # 배경 변경 (환자 거절 상황)
 time_elapsed_for_mid = stage_time_limits[stage] - 7
 if (
  remaining_time <= time_elapsed_for_mid
  and not mid_shown_for_stage[stage]
  and not game_success
  and random.random() < 0.001
 ):
  show_mid_text = True
  mid_text_start_time = time.time()
  mid_shown_for_stage[stage] = True
  current_background = mid_background # mid_background로 배경 영구 설정

 # 화면 그리기 시작
 screen.fill(black)

 # 배경 그리기 로직 (mid_background 유지 및 깜빡임 수정)

 # 1. 최종 성공 또는 중간 성공 시
 if game_success:
  screen.blit(finish_line, (0, 0))
 # 2. 게임 오버 시 (start_background 고정)
 elif gameover:
  screen.blit(start_background, (0, 0))
 # 3. 일반 게임 진행 중
 else:
  # 현재 배경 이미지 (start 또는 mid) 그리기
  screen.blit(current_background, (0, 0))

  # 도로 마커 그리기 (start 또는 mid 배경 위에 도로를 덮어 그립니다)
  if (
   current_background == mid_background
   or current_background == start_background
  ):
   pygame.draw.rect(screen, gray, road)
   pygame.draw.rect(screen, yellow, left_edge_marker)
   pygame.draw.rect(screen, yellow, right_edge_marker)
   # 차선 애니메이션
   lane_marker_move_y += speed * 2
   if lane_marker_move_y >= marker_height * 2:
    lane_marker_move_y = 0
   for y in range(marker_height * -2, height, marker_height * 2):
    pygame.draw.rect(
     screen,
     white,
     (
      left_lane + 45,
      y + lane_marker_move_y,
      marker_width,
      marker_height,
     ),
    )
    pygame.draw.rect(
     screen,
     white,
     (
      center_lane + 45,
      y + lane_marker_move_y,
      marker_width,
      marker_height,
     ),
    )

  if show_mid_text: # 배경 변경 시 메시지 표시 (2초 후 메시지만 사라짐)
   if time.time() - mid_text_start_time <= 2:
    mid_text = quiz_font.render(
     "환자가 거절당했습니다. 목적지가 변경됐습니다.", True, red
    )
    mid_rect = mid_text.get_rect(center=(width / 2, height / 2))
    screen.blit(mid_text, mid_rect)
   else:
    show_mid_text = False # 배경은 mid_background로 유지됩니다.

 # 플레이어 및 차량 그룹 업데이트/그리기
 # ⭐ 플레이어 업데이트 (움직임 처리)
 player.update()
 player_group.draw(screen)

 # 차량 자동 생성 로직
 if len(vehicle_group) < 2 and not game_success:
  add_vehicle = True
  for vehicle in vehicle_group:
   if vehicle.rect.top < vehicle.rect.height * 1.5:
    add_vehicle = False
  if add_vehicle:
   lane = random.choice(lanes)
   image = random.choice(vehicle_images)
   vehicle = Vehicle(image, lane, height / -2)
   vehicle_group.add(vehicle)

 # 차량 이동 및 화면 밖 제거
 for vehicle in vehicle_group:
  vehicle.rect.y += speed
  if vehicle.rect.top >= height:

   # 필살기 충전 로직
   if not gameover and not game_success:
    vehicles_dodged_since_last_charge += 1
    if vehicles_dodged_since_last_charge >= 5:
     special_skill_count += 1
     vehicles_dodged_since_last_charge = 0

   vehicle.kill()

 vehicle_group.draw(screen)
 hospital_group.draw(screen)

 # 병원 생성 로직
 required_time = hospital_spawn_time[stage]

 if (
  not hospital_spawned
  and remaining_time <= required_time
  and not game_success
 ):

  found_safe_lane = False
  max_spawn_attempts = 10
  hospital = None

  for _ in range(max_spawn_attempts):
   hospital_lane = random.choice(lanes)
   hospital_y = -100

   temp_hospital = Hospital(hospital_lane, hospital_y)
   colliding_with_vehicles = pygame.sprite.spritecollide(
    temp_hospital, vehicle_group, False
   )

   if not colliding_with_vehicles:
    hospital = temp_hospital
    found_safe_lane = True
    break
   else:
    temp_hospital.kill()

  if found_safe_lane and hospital:
   hospital_group.add(hospital)
   hospital_spawned = True
  else:
   hospital_spawned = False

 # 병원 이동 및 화면 밖 제거
 if not game_success:
  hospital_group.update()
  for h in hospital_group:
   if h.rect.top >= height:
    h.kill()
    hospital_spawned = False

 # 타임 오버
 if remaining_time <= 0 and not game_success:
  remaining_time = 0
  gameover = True

 # HUD 표시
 if not (game_success and stage == 3):

  skill_text = game_font_small.render(
   f"필살기: {special_skill_count}회", True, yellow
  )
  screen.blit(skill_text, (70, 400))

  time_text = game_font_small.render(
   f"Time: {int(remaining_time)}", True, white
  )
  screen.blit(time_text, (70, 420))

  draw_time_bar(screen, remaining_time, stage_time_limits[stage], stage)

  if stage == 1:
   stage_info = "Stage 1_뇌졸중(긴급)"
  elif stage == 2:
   stage_info = "Stage 2_중증외상(긴급)"
  elif stage == 3:
   stage_info = "Stage 3_심정지(소생)"

  stage_text = game_font_big.render(stage_info, True, white)
  screen.blit(stage_text, (20, 20))

  if not gameover:
   draw_hearts(screen, collision_count)

 # 충돌 감지 및 처리
 if not game_success and pygame.sprite.spritecollide(
  player, vehicle_group, True
 ):
  if player in player_group:
   crash_rect.center = [player.rect.center[0], player.rect.top]

   collision_count += 1

   screen.blit(crash, crash_rect)
   pygame.display.update()
   pygame.time.delay(500)

   if collision_count >= 2:
    gameover = True

 # 병원 도착 (스테이지 성공) 감지 및 처리
 if not game_success and pygame.sprite.spritecollide(
  player, hospital_group, True
 ):
  game_success = True
  stage_finished = True

  if stage == 3:
   vehicle_group.empty()
   random_vehicle_spawned = True
   player.kill()

 # 성공/오버 메시지
 # 1. 최종 성공 또는 중간 성공 시 (finish_line 배경 위에 메시지)
 if game_success:
  
  # Stage 3 성공 시 (Stage 1부터 다시 할지 물어봄)
  if stage == 3:
   success_msg = "최종 성공! Stage 1부터 다시 시작하시겠습니까?"
   restart_message = "다시 시도 (Y) / 게임 종료 (N)"
  # Stage 1 또는 2 성공 시 (다음 단계로 넘어갈지 물어봄)
  elif stage < 3:
   success_msg = f"Stage {stage} Success!"
   restart_message = "다음 단계로 넘어가시겠습니까? (Y / N)"


  success_text = game_font_big.render(success_msg, True, black)
  success_rect = success_text.get_rect(center=(width / 2, 100))
  screen.blit(success_text, success_rect)
  
  restart_text = game_font_small.render(restart_message, True, black)
  restart_rect = restart_text.get_rect(center=(width / 2, 130))
  screen.blit(restart_text, restart_rect)


 # 3. 게임 오버 메시지
 elif gameover:
  gameover_text = game_font_big.render("Game Over!", True, red)
  gameover_rect = gameover_text.get_rect(center=(width / 2, 100))
  screen.blit(gameover_text, gameover_rect)

  restart_message = f"Stage {stage}부터 다시 시도하겠습니까? (Y / N)"

  restart_text = game_font_small.render(restart_message, True, white)
  restart_rect = restart_text.get_rect(center=(width / 2, 130))
  screen.blit(restart_text, restart_rect)

 pygame.display.update()

 # 게임 오버/성공 후 대기 루프 (배경 재그리기 및 깜빡임 방지)
 # Stage 3 성공 시에도 진입하도록 조건을 변경했습니다.
 while gameover or (game_success and stage <= 3):
  clock.tick(fps)

  # 대기 루프 내에서 배경 이미지와 메시지를 다시 그려서 깜빡임 방지
  if game_success:
   screen.blit(finish_line, (0, 0))
   
   if stage == 3:
    success_msg = "최종 성공! Stage 1부터 다시 시작하시겠습니까?"
    restart_message = "다시 시도 (Y) / 게임 종료 (N)"
   else: # Stage 1, 2 성공
    success_msg = f"Stage {stage} Success!"
    restart_message = "다음 단계로 넘어가시겠습니까? (Y / N)"

   success_text = game_font_big.render(success_msg, True, black)
   success_rect = success_text.get_rect(center=(width / 2, 100))
   screen.blit(success_text, success_rect)
   restart_text = game_font_small.render(
    restart_message, True, black
   )
   restart_rect = restart_text.get_rect(center=(width / 2, 130))
   screen.blit(restart_text, restart_rect)
   
  elif gameover:
   screen.blit(start_background, (0, 0))
   gameover_text = game_font_big.render("Game Over!", True, red)
   gameover_rect = gameover_text.get_rect(center=(width / 2, 100))
   screen.blit(gameover_text, gameover_rect)
   restart_message = f"Stage {stage}부터 다시 시도하겠습니까? (Y / N)"
   restart_text = game_font_small.render(restart_message, True, white)
   restart_rect = restart_text.get_rect(center=(width / 2, 130))
   screen.blit(restart_text, restart_rect)

  pygame.display.update()

  for event in pygame.event.get():
   if event.type == QUIT:
    running = False
    gameover = False
    game_success = False
   if event.type == KEYDOWN:
    if event.key == K_y:
     if game_success and stage < 3: # Stage 1, 2 성공 시 다음 단계로
      reset_game_state(stage + 1)
     elif game_success and stage == 3: # Stage 3 성공 시 Stage 1로 재시작
      reset_game_state(1)
     elif gameover: # 게임 오버 시 현재 Stage부터 다시 시작
      reset_game_state(stage)
    
    elif event.key == K_n:
     running = False # 게임 종료
     gameover = False
     game_success = False
   
   if not running or quiz_active:
    break

pygame.quit()