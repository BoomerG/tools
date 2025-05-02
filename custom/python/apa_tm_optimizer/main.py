import ui
from itertools import combinations

# Player skill sets and max handicap
og_players8 = {
    "Aaron": 5,
    "Rob": 3,
    "Martin": 3,
    "Mike": 6,
    "Michael": 4,
    "Steve": 6,
    "Abe": 4,
}
og_players9 = {
    "Aaron": 5,
    "Rob": 4,
    "Martin": 4,
    "Mike": 6,
    "Michael": 3,
    "Steve": 7,
    "Abe": 5,
    "Mark": 6,
}
players8 = og_players8.copy()
players9 = og_players9.copy()
handicap = 23  # Handicap limit


# Generate all possible combos for 5-man team
def find_opt_teams(players, handicap):
    valid_combos = [
        combo
        for combo in combinations(players.items(), 5)
        if sum(skill for name, skill in combo) == handicap
    ]
    presorted_combos = [
        sorted(combo, key=lambda item: item[1], reverse=True) for combo in valid_combos
    ]
    sorted_combos = sorted(presorted_combos, key=lambda item: item[0][1], reverse=True)
    formatted_teams = [
        "Team: "
        + ", ".join(name for name, skill in combo)
        + "\nSkills: "
        + ", ".join(str(skill) for name, skill in combo)
        for combo in sorted_combos
    ]
    return formatted_teams


def remove_player_action(sender):
    player_name = sender.superview["name_input"].text
    players8.pop(player_name, None)
    players9.pop(player_name, None)

    opt_tm8 = find_opt_teams(players8, handicap)
    opt_tm9 = find_opt_teams(players9, handicap)

    results_tm8.text = (
        "\n\n".join(opt_tm8) if opt_tm8 else "No valid combinations found."
    )
    results_tm9.text = (
        "\n\n".join(opt_tm9) if opt_tm9 else "No valid combinations found."
    )


def refresh(sender):
    global results_tm8, results_tm9

    # Start with fresh players list
    players8 = og_players8.copy()
    players9 = og_players9.copy()

    opt_tm8 = find_opt_teams(players8, handicap)
    opt_tm9 = find_opt_teams(players9, handicap)

    results_tm8.text = (
        "\n\n".join(opt_tm8) if opt_tm8 else "No valid combinations found."
    )
    results_tm9.text = (
        "\n\n".join(opt_tm9) if opt_tm9 else "No valid combinations found."
    )


def setup_ui():
    global results_tm8, results_tm9
    screen_width, screen_height = ui.get_screen_size()
    padding = 10
    view_width = screen_width - (padding * 2)
    main_view = ui.View(
        frame=(0, 0, screen_width, screen_height),
        name="APA Team Optimizer",
        background_color="black",
    )
    name_input = ui.TextField(
        frame=(padding, screen_height * 0.79, view_width * 0.7, 50),
        placeholder="Enter player name to remove",
        name="name_input",
    )
    main_view.add_subview(name_input)
    submit_button = ui.Button(
        title="Remove Player",
        frame=(screen_width * 0.72, screen_height * 0.79, 0, 0),
        bg_color="#d10000",
        tint_color="white",
        action=remove_player_action,
    )
    main_view.add_subview(submit_button)

    def create_label(text, y_position):
        return ui.Label(
            frame=(padding, y_position, view_width, screen_height * 0.03),
            text=text,
            alignment=ui.ALIGN_CENTER,
            font=("menlo-bold", 24),
            text_color="#ffeb93",
        )

    def create_text_view(text, y_position, view_height):
        return ui.TextView(
            frame=(padding, y_position, view_width, view_height),
            text=text,
            font=("menlo", 14),
            text_color="white",
            background_color="black",
            editable=False,
        )

    label1 = create_label("8-Ball", screen_height * 0.01)
    main_view.add_subview(label1)
    results_tm8 = create_text_view("", screen_height * 0.05, screen_height * 0.20)
    results_tm8.name = "results_tm8"
    main_view.add_subview(results_tm8)
    label2 = create_label("9-Ball", screen_height * 0.3)
    main_view.add_subview(label2)
    results_tm9 = create_text_view("", screen_height * 0.34, screen_height * 0.41)
    results_tm9.name = "results_tm9"
    main_view.add_subview(results_tm9)
    refresh_button = ui.Button(
        title="Refresh",
        action=refresh,
        frame=(screen_width * 0.85, screen_height * 0.01, 0, 0),
        bg_color="#007aff",
        tint_color="white",
    )
    main_view.add_subview(refresh_button)

    # Initial refresh to display data
    refresh(None)
    main_view.present("fullscreen")

# Find optimal teams
setup_ui()
