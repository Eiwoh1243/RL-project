
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle


PLAYER_COLOURS = ["royalblue", "crimson", "forestgreen", "darkorange"]


def draw_board(state, board_size=9):
    fig, ax = plt.subplots(figsize=(8, 8))

    # Draw the 9x9 grid
    ax.set_xlim(-0.5, board_size - 0.5)
    ax.set_ylim(-0.5, board_size - 0.5)
    ax.set_xticks(range(board_size))
    ax.set_yticks(range(board_size))
    ax.grid(True, linewidth=1.5, color="lightgrey")

    # Draw horizontal walls
    for x, y in state["horiz_walls"]:
        ax.add_patch(
            Rectangle(
                (x - 0.5, y + 0.35),
                2,
                0.3,
                color="black"
            )
        )

    # Draw vertical walls
    for x, y in state["vert_walls"]:
        ax.add_patch(
            Rectangle(
                (x + 0.35, y - 0.5),
                0.3,
                2,
                color="black"
            )
        )

    # Draw player pawns
    for player, (x, y) in enumerate(state["positions"]):
        ax.add_patch(
            Circle(
                (x, y),
                radius=0.3,
                color=PLAYER_COLOURS[player],
                label=f"Player {player}"
            )
        )

    # Display game information
    info = " | ".join(
        f"P{i}: {walls} walls"
        for i, walls in enumerate(state["walls_remaining"])
    )

    ax.set_title(
        f"Quoridor - Player {state['turn']}'s turn\n{info}"
    )

    ax.set_aspect("equal")
    ax.invert_yaxis()
    ax.legend(loc="upper left", bbox_to_anchor=(1, 1))

    plt.tight_layout()
    plt.show()
