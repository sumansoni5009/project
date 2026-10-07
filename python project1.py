
import tkinter as tk
import random

# ---------- GAME SETTINGS ----------

COLORS = {
    "RED": "#ff3333",
    "LIGHT BLUE": "#55bbff",
    "GREEN": "#28c76f",
    "BLACK": "#111111",
    "YELLOW": "#ffd633",
    "PURPLE": "#a855f7"
}

COLOR_NAMES = list(COLORS.keys())

ROWS = 8
COLUMNS = 4
BLOCK_WIDTH = 90
BLOCK_HEIGHT = 70
CANVAS_WIDTH = 380
CANVAS_HEIGHT = 570

score = 0
selected_speed = 1
target_color = ""
game_running = False
blocks = []
game_loop_id = None

# ---------- MAIN WINDOW ----------

root = tk.Tk()
root.title("Colour Rush")
root.geometry("420x700")
root.resizable(False, False)
root.configure(bg="#f5f5f5")


# ---------- START SCREEN ----------

start_frame = tk.Frame(root, bg="#f5f5f5")
start_frame.pack(fill="both", expand=True)

tk.Label(
    start_frame,
    text="COLOUR RUSH",
    font=("Arial", 28, "bold"),
    bg="#f5f5f5",
    fg="#222222"
).pack(pady=(100, 15))

tk.Label(
    start_frame,
    text="Tap the correct colour!",
    font=("Arial", 14),
    bg="#f5f5f5",
    fg="#555555"
).pack(pady=10)

tk.Label(
    start_frame,
    text="Choose Your Speed",
    font=("Arial", 16, "bold"),
    bg="#f5f5f5"
).pack(pady=(30, 10))

speed_choice = tk.StringVar(value="1x")

speed_menu = tk.OptionMenu(
    start_frame,
    speed_choice,
    "1x", "2x", "3x", "4x", "5x"
)
speed_menu.config(
    font=("Arial", 14),
    width=8,
    bg="white"
)
speed_menu.pack(pady=5)

tk.Button(
    start_frame,
    text="START",
    font=("Arial", 18, "bold"),
    width=10,
    height=2,
    bg="#222222",
    fg="white",
    command=lambda: start_game()
).pack(pady=30)


# ---------- GAME SCREEN ----------

game_frame = tk.Frame(root, bg="#f5f5f5")

top_frame = tk.Frame(game_frame, bg="#f5f5f5")
top_frame.pack(fill="x", pady=8)

score_label = tk.Label(
    top_frame,
    text="Score: 0",
    font=("Arial", 14, "bold"),
    bg="#f5f5f5"
)
score_label.pack(side="left", padx=15)

speed_label = tk.Label(
    top_frame,
    text="Speed: 1x",
    font=("Arial", 14, "bold"),
    bg="#f5f5f5"
)
speed_label.pack(side="right", padx=15)

target_label = tk.Label(
    game_frame,
    text="RED",
    font=("Arial", 23, "bold"),
    bg="#f5f5f5"
)
target_label.pack(pady=4)

tk.Label(
    game_frame,
    text="Click the matching colour",
    font=("Arial", 11),
    bg="#f5f5f5",
    fg="#555555"
).pack(pady=3)

canvas = tk.Canvas(
    game_frame,
    width=CANVAS_WIDTH,
    height=CANVAS_HEIGHT,
    bg="white",
    highlightthickness=2,
    highlightbackground="#cccccc"
)
canvas.pack(pady=4)


# ---------- GAME FUNCTIONS ----------

def choose_target():
    global target_color

    target_color = random.choice(COLOR_NAMES)

    target_label.config(
        text=target_color,
        fg=COLORS[target_color]
    )


def create_blocks():
    global blocks

    canvas.delete("all")
    blocks = []

    for row in range(ROWS):
        for col in range(COLUMNS):

            color_name = random.choice(COLOR_NAMES)

            x1 = col * BLOCK_WIDTH + 5
            y1 = row * BLOCK_HEIGHT + 5
            x2 = x1 + BLOCK_WIDTH - 10
            y2 = y1 + BLOCK_HEIGHT - 10

            rectangle = canvas.create_rectangle(
                x1, y1, x2, y2,
                fill=COLORS[color_name],
                outline="white",
                width=3
            )

            blocks.append({
                "id": rectangle,
                "color": color_name,
                "column": col
            })

            canvas.tag_bind(
                rectangle,
                "<Button-1>",
                lambda event, block_id=rectangle:
                    block_clicked(block_id)
            )


def block_clicked(block_id):
    global score

    if not game_running:
        return

    selected_color = None

    for block in blocks:
        if block["id"] == block_id:
            selected_color = block["color"]
            break

    if selected_color is None:
        return

    if selected_color == target_color:
        score += 1
        score_label.config(text=f"Score: {score}")

        choose_target()
    else:
        game_over()


def move_blocks():
    global game_loop_id

    if not game_running:
        return

    # Selected speed increases movement.
    # Every 10 points adds one more speed level.
    current_speed = selected_speed + score // 10

    for block in blocks:
        canvas.move(
            block["id"],
            0,
            current_speed
        )

    # Recycle blocks that pass the bottom.
    # Each block returns to the top of its own column.
    for block in blocks:
        coords = canvas.coords(block["id"])

        if coords and coords[1] >= CANVAS_HEIGHT:
            column = block["column"]

            # Find the highest block in this column.
            column_blocks = [
                other for other in blocks
                if other["column"] == column
                and other["id"] != block["id"]
            ]

            highest_y = min(
                canvas.coords(other["id"])[1]
                for other in column_blocks
            )

            new_y1 = highest_y - BLOCK_HEIGHT
            new_y2 = new_y1 + BLOCK_HEIGHT - 10

            canvas.coords(
                block["id"],
                coords[0],
                new_y1,
                coords[2],
                new_y2
            )

            new_color = random.choice(COLOR_NAMES)
            block["color"] = new_color

            canvas.itemconfig(
                block["id"],
                fill=COLORS[new_color]
            )

    game_loop_id = root.after(30, move_blocks)


def game_over():
    global game_running, game_loop_id

    game_running = False

    if game_loop_id is not None:
        root.after_cancel(game_loop_id)
        game_loop_id = None

    canvas.create_rectangle(
        40, 210, 340, 360,
        fill="white",
        outline="#222222",
        width=3
    )

    canvas.create_text(
        190, 245,
        text="GAME OVER",
        font=("Arial", 24, "bold"),
        fill="#222222"
    )

    canvas.create_text(
        190, 285,
        text=f"Final Score: {score}",
        font=("Arial", 16, "bold"),
        fill="#555555"
    )

    canvas.create_window(
        190, 325,
        window=tk.Button(
            root,
            text="PLAY AGAIN",
            font=("Arial", 12, "bold"),
            bg="#222222",
            fg="white",
            command=restart_game
        )
    )


def start_game():
    global score, selected_speed, game_running

    if game_loop_id is not None:
        root.after_cancel(game_loop_id)

    score = 0
    selected_speed = int(
        speed_choice.get().replace("x", "")
    )
    game_running = True

    start_frame.pack_forget()
    game_frame.pack(fill="both", expand=True)

    score_label.config(text="Score: 0")
    speed_label.config(
        text=f"Speed: {selected_speed}x"
    )

    choose_target()
    create_blocks()
    move_blocks()


def restart_game():
    global game_running, game_loop_id

    game_running = False

    if game_loop_id is not None:
        root.after_cancel(game_loop_id)
        game_loop_id = None

    game_frame.pack_forget()
    start_frame.pack(fill="both", expand=True)


# ---------- RUN GAME ----------

root.mainloop()
