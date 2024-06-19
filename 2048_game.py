import random
import tkinter as tk
def initialize_grid():
    grid=[]
    for i in range(4):
        row=[]
        for j in range(4):
            row.append(0)
        grid.append(row)
    add_two(grid)
    add_two(grid)
    return grid
def add_two(grid):
    empty=[]
    for i in range(4):
        for j in range(4):
            if grid[i][j]==0:
                empty.append((i, j))
    if empty:
        pos=random.choice(empty)
        grid[pos[0]][pos[1]]=random.choice([2, 4])
def print_grid(grid):
    for row in grid:
        print('\t'.join(map(str, row)))
    print()
# def get_user_input():
#     valid_moves=['W','A','S','D']
#     move=input('Enter move (W/A/S/D): ').upper()
#     while move not in valid_moves:
#         move=input('Invalid move. Enter move (W/A/S/D): ').upper()
#     return move
def slide_and_merge_row_left(row):
    new_row=[num for num in row if num!=0]
    for i in range(len(new_row)-1):
        if new_row[i]==new_row[i+1]:
            new_row[i]*=2
            new_row[i+1]=0
    merged_row=[]
    for num in new_row:
        if num!=0:
            merged_row.append(num)
    while len(merged_row)<len(row):
        merged_row.append(0)
    return merged_row
def move_left(grid):
    for i in range(len(grid)):
        grid[i]=slide_and_merge_row_left(grid[i])
def move_right(grid):
    for i in range(len(grid)):
        grid[i]=grid[i][::-1]
        grid[i]=slide_and_merge_row_left(grid[i])
        grid[i]=grid[i][::-1]
def move_up(grid):
    for i in range(4):
        column=[]
        for j in range(4):
            column.append(grid[j][i])
        new_column=slide_and_merge_row_left(column)
        for j in range(4):
            grid[j][i]=new_column[j]
def move_down(grid):
    for i in range(4):
        column=[]
        for j in range(4):
            column.append(grid[j][i])
        column.reverse()
        new_column=slide_and_merge_row_left(column)
        new_column.reverse()
        for j in range(4):
            grid[j][i]=new_column[j]
def check_win(grid):
    for row in grid:
        if 2048 in row:
            return True
    return False
def check_game_over(grid):
    for row in grid:
        if 0 in row:
            return False
    for i in range(4):
        for j in range(3):
            if grid[i][j]==grid[i][j + 1]:
                return False
    for i in range(3):
        for j in range(4):
            if grid[i][j]==grid[i + 1][j]:
                return False
    return True
COLORS = {
    0: ("#CDC1B4", "black"),
    2: ("#EEE4DA", "black"),
    4: ("#EDE0C8", "black"),
    8: ("#F2B179", "white"),
    16: ("#F59563", "white"),
    32: ("#F67C5F", "white"),
    64: ("#F65E3B", "white"),
    128: ("#EDCF72", "white"),
    256: ("#EDCC61", "white"),
    512: ("#EDC850", "white"),
    1024: ("#EDC53F", "white"),
    2048: ("#EDC22E", "white"),
}
def update_grid_display():
    for i in range(4):
        for j in range(4):
            tile = grid[i][j]
            text = str(tile) if tile != 0 else ""
            bg_color, fg_color = COLORS.get(tile, ("#CDC1B4", "black"))
            tiles[i][j].config(text=text, bg=bg_color, fg=fg_color)
def key_press(event):
    if event.keysym == 'Up':
        move_up(grid)
    elif event.keysym == 'Left':
        move_left(grid)
    elif event.keysym == 'Down':
        move_down(grid)
    elif event.keysym == 'Right':
        move_right(grid)
    else:
        return
    add_two(grid)
    update_grid_display()
    if check_win(grid):
        label.config(text="Congratulations! You won!")
        root.unbind("<Key>")
    elif check_game_over(grid):
        label.config(text="Game over, no more valid moves.")
        root.unbind("<Key>")
def play_game():
    global grid, tiles, root, label
    grid = initialize_grid()
    root = tk.Tk()
    root.title("2048 Game")
    frame = tk.Frame(root)
    frame.grid()
    tiles = [[tk.Label(frame, text="", width=6, height=3, font=("Arial", 24, "bold"), borderwidth=2, relief="solid") for _ in range(4)] for _ in range(4)]
    for i in range(4):
        for j in range(4):
            tiles[i][j].grid(row=i, column=j, padx=5, pady=5)
    label = tk.Label(root, text="Use arrow keys to play.", font=("Arial", 18))
    label.grid(row=1)
    update_grid_display()
    root.bind("<Key>", key_press)
    root.mainloop()
play_game()