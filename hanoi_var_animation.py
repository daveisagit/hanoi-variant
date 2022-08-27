import pygame
import seaborn as sns
import vidmaker

from hanoi_var import HanoiVar, history

pygame.init()
total_poles = 7
total_rings = 2 ** (total_poles - 1) - 1
vel = 120
FPS = 60

# seaborn generates nice colour palettes
palette = sns.color_palette("pastel", total_rings + 1)

screen_width = 1800
screen_height = 1000

y_margin = 20
ring_space = (screen_height - 2 * y_margin) // (total_rings + 2)
height = int(ring_space * 0.85)
gap = ring_space - height
font_size = int(height * 0.7)

dis = pygame.display.set_mode((screen_width, screen_height))
run = True
clock = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', font_size)

pole_space = screen_width // total_poles
pole_width = int(pole_space * 0.8)
pole_gap = (screen_width - (pole_width * total_poles)) // (total_poles + 1)
min_ring_width = 40
pole_y = screen_height - y_margin
ring_base_y = pole_y

# Load all the moves into history
v = HanoiVar(total_poles)
v.solve()
paused = False

# start video capture
video = vidmaker.Video(
    path=f"Hanoi Variant - {total_poles} poles.mp4",
    fps=FPS,
    resolution=(screen_width, screen_height)
)


def new_frame():
    """Pause, update pygame display and video capture"""
    clock.tick(FPS)
    pygame.display.flip()
    video.update(pygame.surfarray.pixels3d(dis).swapaxes(0, 1), inverted=False)


def ring_width(ring):
    """Calculate the width of ring #"""
    return min_ring_width + ring * (pole_width - min_ring_width) // total_rings


def clear_ring_at(ring, x, y):
    """For animation, clear the previous ring image"""
    w = ring_width(ring) + 5
    h = height + gap - 2
    pygame.draw.rect(
        dis,
        (0, 0, 0),
        pygame.Rect(x - w // 2, y - h // 2, w, h)
    )


def draw_ring_centered_at(ring, x, y):
    w = ring_width(ring)
    pygame.draw.rect(
        dis,
        tuple(int(col * 255) for col in palette[ring]),
        pygame.Rect(x - w // 2, y - height // 2, w, height),
        border_radius=10
    )
    # Ring number
    text = font.render(str(ring), True, (0, 0, 0))
    text_rect = text.get_rect()
    text_rect.center = (x, y)
    dis.blit(text, text_rect)


def draw_state(state):
    dis.fill((0, 0, 0))
    idx = 0
    for pole in state:
        idx += 1
        x = int((idx - 0.5) * pole_space)
        w = pole_width
        pygame.draw.rect(
            dis,
            (255, 255, 255),
            pygame.Rect(x - w // 2, pole_y - gap, w, 20)
        )

        if not pole:
            continue

        y = ring_base_y
        for ring in range(pole[1], pole[0] - 1, -1):
            y -= height + gap
            draw_ring_centered_at(ring, x, y)

    new_frame()


def animate_move(state, move):
    # find clearance height over the intermediate rings for the move
    max_rings = 1
    if move[0] < move[1]:
        p_a = move[0]
        p_b = move[1]
    else:
        p_a = move[1]
        p_b = move[0]

    for idx in range(p_a, p_b + 1):
        pole = state[idx]
        if pole:
            size = pole[1] - pole[0] + 1
            if max_rings < size:
                max_rings = size

    # establish the height (in rings of the start and end position)
    from_pole = state[move[0]]
    ring = from_pole[0]
    to_pole = state[move[1]]
    h_start = from_pole[1] - from_pole[0]  # 0 is on base
    if to_pole:
        h_end = to_pole[1] - to_pole[0] + 1  # 1 is on a single existing one
    else:
        h_end = 0

    # determine the actual co-ordinates and x-move direction
    y_from = ring_base_y - (h_start + 1) * (height + gap)
    y_to = ring_base_y - (max_rings + 1) * (height + gap)
    x_from = x = int((move[0] + 0.5) * pole_space)
    x_to = x = int((move[1] + 0.5) * pole_space)
    d = 1
    if x_to < x_from:
        d = -1

    # move up
    for y in range(y_from, y_to, -vel):
        clear_ring_at(ring, x_from, y)
        draw_ring_centered_at(ring, x_from, max(y - vel, y_to))
        new_frame()

    # move across
    for x in range(x_from, x_to, vel * d):
        clear_ring_at(ring, x, y_to)
        if d == 1:
            x2 = min(x + vel * d, x_to)
        else:
            x2 = max(x + vel * d, x_to)
        draw_ring_centered_at(ring, x2, y_to)
        new_frame()

    # move down
    y_to = ring_base_y - (h_end + 1) * (height + gap)
    y_from = ring_base_y - (max_rings + 1) * (height + gap)
    for y in range(y_from, y_to, vel):
        clear_ring_at(ring, x_to, y)
        draw_ring_centered_at(ring, x_to, min(y + vel, y_to))
        new_frame()


# ===================
# Main loop
# ===================


idx = -1
while run:
    # Keys: q-quit, p-pause (at the end of a move)
    # Loop through history and animate the move

    if not paused and idx < len(history) - 1:
        idx += 1
        move = history[idx]
        draw_state(move.state)
        new_frame()
        animate_move(move.state, move.move)

    # check events (keys and window close)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                run = False
            if event.key == pygame.K_p:
                paused = not paused

        if event.type == pygame.QUIT:
            run = False

    if not run:
        break

# Just wait to quit
while run:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                run = False
        if event.type == pygame.QUIT:
            run = False
    new_frame()

pygame.quit()
video.export(verbose=True)
