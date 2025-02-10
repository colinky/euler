import tkinter as tk
import datetime
import time

def create_popup(target_time):
    popup = tk.Tk()
    popup.title("남은 시간")

    # 창 크기 설정 (가로 200픽셀, 세로 120픽셀)
    popup.geometry("200x120")

    # 창 크기 조정 비활성화
    popup.resizable(False, False)

    # 팝업을 항상 화면 가장 앞에 표시
    popup.attributes("-topmost", True)

    # 화면의 우측 하단에 창 위치 설정
    screen_width = popup.winfo_screenwidth()  # 화면의 가로 길이
    screen_height = popup.winfo_screenheight()  # 화면의 세로 길이
    window_width = 200  # 창의 가로 길이
    window_height = 120  # 창의 세로 길이
    x_position = screen_width - window_width  # 우측 하단 X 좌표
    y_position = screen_height - window_height  # 우측 하단 Y 좌표
    popup.geometry(f"+{x_position}+{y_position}")  # 창 위치 설정

    # 현재 시간 레이블 (폰트 크기 164, 가운데 정렬)
    current_time_label = tk.Label(
        popup, text="", font=("Helvetica", 16), fg="black"
    )
    current_time_label.pack(expand=True)  # 세로로 가운데 정렬

    # 남은 시간 레이블 (폰트 크기 20, 가운데 정렬)
    remaining_time_label = tk.Label(
        popup, text="", font=("Helvetica", 20), fg="red"
    )
    remaining_time_label.pack(expand=True)  # 세로로 가운데 정렬

    # 깜빡이는 효과를 위한 상태 변수
    blink_state = False

    def update_time(target_time):
        nonlocal blink_state
        now = datetime.datetime.now()
        target = datetime.datetime.combine(now.date(), datetime.time.fromisoformat(target_time))
        time_before = target - datetime.timedelta(minutes=10)
        time_left = (target - now).total_seconds()

        if now >= time_before and now < target:
            minutes = int(time_left // 60)
            seconds = int(time_left % 60)

            # 현재 시간 HH:MM 형식으로 표시
            current_time_str = now.strftime("%H:%M")
            current_time_label.config(text=f"현재 시간: {current_time_str}")

            # 남은 시간 표시
            remaining_time_str = f"{minutes:02d}:{seconds:02d}"
            remaining_time_label.config(text=f"남은 시간: {remaining_time_str}")

            # 종료 2분 전부터 깜빡이는 효과 적용
            if time_left <= 120:  # 2분 = 120초
                if blink_state:
                    current_time_label.config(fg="black")
                    remaining_time_label.config(fg="red")
                else:
                    current_time_label.config(fg="white")
                    remaining_time_label.config(fg="white")
                blink_state = not blink_state  # 상태 전환

            popup.after(500, update_time, target_time)  # 0.5초마다 업데이트 (target_time 전달)
        elif now >= target:
            remaining_time_label.config(text="시간 종료!")
            popup.after(2000, popup.destroy)  # 2초 후 창 닫기
        else:
            popup.after(1000, update_time, target_time)  # 1초마다 업데이트 (target_time 전달)

    # 초기 호출 시 target_time 전달
    update_time(target_time)
    popup.mainloop()

def validate_time(time_str):
    try:
        datetime.datetime.strptime(time_str, "%H:%M")
        return True
    except ValueError:
        return False

# 24시간 형식으로 목표 시간 입력 받기
target_time_input = input("24시간 형식으로 목표 시간을 입력하세요 (HH:MM): ")

if validate_time(target_time_input):
    now = datetime.datetime.now()
    target = datetime.datetime.combine(now.date(), datetime.time.fromisoformat(target_time_input))
    time_before = target - datetime.timedelta(minutes=10)

    # 현재 시간이 목표 시간 10분 전보다 이전인 경우 대기
    if now < time_before:
        time_to_wait = (time_before - now).total_seconds()
        print(f"팝업은 {time_to_wait // 60}분 후에 나타납니다.")
        time.sleep(time_to_wait)  # 대기

    # 팝업 창 생성
    create_popup(target_time_input)
else:
    print("잘못된 시간 형식입니다. 프로그램을 종료합니다.")
