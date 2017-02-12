import string

__author__ = "Jérémy Farnault"


class ActionPointsZone:
    # Zone des points d'action
    HEIGHT = 120
    IMAGE_1_Y = 0
    IMAGE_2_Y = 40
    IMAGE_3_Y = 80
    IMAGES_X = 5
    WIDTH = 40
    ZONE_POS_X = 10
    ZONE_POS_Y = 10


class ActionsSelectionZone:
    # Zone de sélection des actions disponibles
    ACTION_1_MARGIN_Y = 10
    ACTION_2_MARGIN_Y = 60
    ACTION_3_MARGIN_Y = 110
    ACTION_4_MARGIN_Y = 160
    ACTION_5_MARGIN_Y = 210
    ACTION_6_MARGIN_Y = 260
    CIRCLE_RADIUS = 20
    HEIGHT = 350
    MARGIN_ACTION_X = 20
    MARGIN_TOOLTIP = 7
    WIDTH = 130
    ZONE_POS_Y = 0


class Battle:
    # Bataille à deux joueurs en local
    ACTION_POINTS = 3
    ACTION_POINTS_MARGIN = 5
    COLUMNS_BF = 16
    DECK_IMAGE_RECT_MARGIN = 2
    DECK_IMAGE_RECT_MARGIN_RIGHT = 10
    DECK_IMAGE_RECT_MARGIN_BOT = 10
    DECK_TXT_MARGIN = 30
    LINES_BF = 12
    MARGIN_DRAW = 10
    MARGIN_POINTS = 50
    MIN_TIMER = 0
    PLAYER_NAME_MARGIN = 20
    POS_Y_BACK_START = 15
    SEC_TIMER = 59
    SIZE_SQUARE_BF = 49
    TOP_TEXT_POINTS = 605


class Card:
    # Cartes
    COST_SURFACE_LIST_MARGIN = 10
    IN_DECK_SURFACE_LIST_MARGIN = 5
    MINIATURE_IN_LIST_MARGIN = 10
    NAME_SURFACE_LIST_MARGIN = 25
    START_X_MINIATURE_PART = 30
    START_Y_MINIATURE_PART = 15
    SURFACE_LIST_WIDTH = 223
    SURFACE_LIST_HEIGHT = 30
    WIDTH_MINIATURE_PART = 75


class Colors:
    # Colors
    BLACK = (0, 0, 0, 255)
    BLACK_150_ALPHA = (0, 0, 0, 150)
    BLACK_200_ALPHA = (0, 0, 0, 200)
    BLACK_FULL_ALPHA = (0, 0, 0, 0)
    BRONZE = (140, 120, 83, 255)
    BRONZE_150_ALPHA = (140, 120, 83, 150)
    DARK_RED = (102, 0, 0, 255)
    DARK_GRAY = (31, 31, 31, 255)
    DARK_GRAY_150_ALPHA = (31, 31, 31, 150)
    DARK_SLATE_GRAY = (47, 79, 79, 255)
    DARK_SLATE_GRAY_100_ALPHA = (47, 79, 79, 100)
    DARK_SLATE_GRAY_150_ALPHA = (47, 79, 79, 100)
    ELECTRIC_BLUE = (44, 117, 255, 255)
    ELECTRIC_BLUE_150_ALPHA = (44, 117, 255, 150)
    GOLD = (255, 215, 0, 255)
    GOLD_150_ALPHA = (255, 215, 0, 150)
    GOLDENROD = (205, 155, 29, 255)
    GOLDENROD_150_ALPHA = (205, 155, 29, 150)
    GREEN = (0, 153, 0, 255)
    GREEN_150_ALPHA = (0, 153, 0, 150)
    LIGHT_GRAY = (217, 217, 217, 255)
    LIGHT_GRAY_150_ALPHA = (217, 217, 217, 150)
    ORANGE_RED = (255, 69, 0, 255)
    ORANGE_RED_150_ALPHA = (255, 69, 0, 150)
    OVERLAY_ALPHA = 220
    PURPLE_150_ALPHA = (127, 0, 255, 150)
    PURPLE = (127, 0, 255, 255)
    RED = (255, 0, 0, 255)
    RED_150_ALPHA = (255, 0, 0, 150)
    ROYAL_BLUE = (19, 66, 148, 255)
    ROYAL_BLUE_150_ALPHA = (19, 66, 148, 150)
    SADDLE_BROW = (139, 69, 19, 255)
    SQUARE_BATTLEFIELD_ALPHA = 150
    WHITE = (255, 255, 255, 255)


class DeckSelection:
    # Deck selection
    BOT_BUTTONS_TEXT = 40
    BUTTON_ARROW_LEFT_MARGIN = 630
    BUTTON_ARROW_RIGHT_MARGIN = 660
    BUTTON_ARROWS_PADDING = 30
    BUTTON_LISTS_PADDING = 50
    BUTTON_SORT_MARGIN = 570
    BUTTON_SORT_PADDING = 20
    BUTTON_START_MARGIN = 695
    CARDS_PER_PAGE = 15
    DETAILS_MARGIN_TOP = 5
    DIFF_AVAILABLE_TEXT = 170
    DIFF_MINIATURE_TEXT = 155
    LINE_LENGTH = 5
    LIST_IN_DETAIL_ZONE_X = 41
    LIST_IN_DETAIL_ZONE_Y = 39
    MARGIN_X = 140
    MARGIN_Y = 190
    NAME_MARGIN = 20
    NAME_MARGIN_DETAILS = 35
    POS_SEARCH_FIELD_X = 230
    POS_SEARCH_FIELD_Y = 10
    SEARCH_TEXT_PADDING = 5
    SQUARE_HOVERED_DIFF = 3
    START_MINIATURE_X = 25
    START_MINIATURE_Y = 45
    START_BUTTON_LISTS_Y = 10
    TOP_BUTTONS_ARROWS = 100
    TOTAL_CARDS = 10


class DeckVisualization:
    # Visualisation du deck
    BUTTON_BACK_MARGIN = 50
    BUTTONS_PADDING = 20
    RECT_WIDTH = 2
    SURFACE_DECK_MARGIN = 10


class Files:
    # Files
    HEROES_FILE = "heroes"
    TEAMS_SAVE = "teams_save"
    CARDS_FILE = "cards"
    DECKS_SAVE = "decks_save"


class Fonts:
    # Polices
    ARIAL = "arial"


class Framerate:
    # Framerate
    FRAMERATE = 60


class HeroesDeployment:
    # Déploiement des héros
    COLUMNS_BF = 16
    DECK_IMAGE_RECT_MARGIN = 2
    DECK_IMAGE_RECT_MARGIN_RIGHT = 10
    DECK_IMAGE_RECT_MARGIN_BOT = 10
    DECK_TXT_MARGIN = 30
    LIMIT_FPLAYER = 4
    LIMIT_SPLAYER = 12
    LINES_BF = 12
    MARGIN_POINTS = 50
    MIN_TIMER = 2
    PLAYER_NAME_MARGIN = 20
    POS_Y_BACK_START = 15
    SEC_TIMER = 0
    SIZE_SQUARE_BF = 49
    TOP_TEXT_POINTS = 605


class HeroDetailsZone:
    # Zone de détail du héro
    WIDTH = 300
    HEIGHT = 150


class ImagesPath:
    # Images paths
    ACTION_POINT_MOUSE_PATH = r"assets\various\action_point_mouse_path.png"
    ACTION_POINT_UNUSED = r"assets\various\action_point_unused.png"
    ACTION_POINT_USED = r"assets\various\action_point_used.png"
    ATTACK_ACTION = r"assets\actions_tokens\attack_action.png"
    ATTACK_ARMOR_ACTION = r"assets\actions_tokens\attack_armor_action.png"
    BACK_NAME_SELECT = r"assets\backgrounds\name_selection.png"
    B_S_S_SCREEN = r"assets\backgrounds\battle_size_selection.png"
    BACK_START_DEPLOYMENT = r"assets\various\back_start_deployment.png"
    BATTLEFIELD_MS = r"assets\backgrounds\battlefield_mount_sunday.png"
    BATTLEFIELD_DARK = r"assets\backgrounds\battlefield_dark.png"
    BUTTON_ARROW_DOWN_BASE = r"assets\buttons\arrow_down.png"
    BUTTON_ARROW_DOWN_DISABLED = r"assets\buttons\arrow_down_disabled.png"
    BUTTON_ARROW_DOWN_HOVERED = r"assets\buttons\arrow_down_hover.png"
    BUTTON_ARROW_LEFT_BASE = r"assets\buttons\arrow_left.png"
    BUTTON_ARROW_LEFT_DISABLED = r"assets\buttons\arrow_left_disabled.png"
    BUTTON_ARROW_LEFT_HOVERED = r"assets\buttons\arrow_left_hover.png"
    BUTTON_ARROW_RIGHT_BASE = r"assets\buttons\arrow_right.png"
    BUTTON_ARROW_RIGHT_DISABLED = r"assets\buttons\arrow_right_disabled.png"
    BUTTON_ARROW_RIGHT_HOVERED = r"assets\buttons\arrow_right_hover.png"
    BUTTON_ARROW_UP_BASE = r"assets\buttons\arrow_up.png"
    BUTTON_ARROW_UP_DISABLED = r"assets\buttons\arrow_up_disabled.png"
    BUTTON_ARROW_UP_HOVERED = r"assets\buttons\arrow_up_hover.png"
    DECK = r"assets\various\deck.png"
    DEFENSE_ACTION = r"assets\actions_tokens\defense_action.png"
    DEFENSE_ACTION_CONFIRMATION = r"assets\actions_tokens\defense_action_confirmation.png"
    FRAME_DETAILS = r"assets\various\frame_details.png"
    INTRO_SCREEN = r"assets\backgrounds\intro_screen.jpg"
    LOADING = r"assets\various\loading.png"
    MAGIC_ACTION = r"assets\actions_tokens\magic_action.png"
    MENU_SCREEN = r"assets\backgrounds\menu_screen.jpg"
    MODAL_BSS = r"assets\modals\modal_battle_size_selection.png"
    MODAL_EXIT = r"assets\modals\modal_exit.png"
    MODAL_POINTS_LEFT = r"assets\modals\modal_points_left.png"
    MOVEMENT_ACTION = r"assets\actions_tokens\movement_action.png"
    PRESS_TO_CONTINUE = r"assets\texts\press_to_continue.png"
    RANGED_ATTACK_ACTION = r"assets\actions_tokens\ranged_attack_action.png"
    T_S_SCREEN = r"assets\backgrounds\team_selection.jpg"
    ZOOM = r"assets\buttons\zoom.png"
    ZOOM_DISABLED = r"assets\buttons\zoom_disabled.png"
    ZOOM_HOVERED = r"assets\buttons\zoom_hovered.png"


class InitiativeBar:
    # Barre d'initiative
    BUTTON_MARGIN = 5
    END_FIRST_LINE = 499
    END_LAST_LINE = 560
    END_SEC_LINE = 501
    FIRST_HERO = 530
    HEIGHT = 450
    LINE_THICK = 2
    MAX_HERO_LEN = 10
    SIZE_X_RECT = 425
    SIZE_Y_RECT = 10
    SIZE_LINE_TOKEN = 10
    START_FIRST_LINE = 140
    START_Y_LINE = 375
    START_X_RECT = 138
    START_Y_RECT = 371
    START_Y_RECT_TOP = 370
    START_Y_RECT_BOT = 381
    TOKEN_MARGIN = 40
    TOKEN_SPACING = 30
    WIDTH = 700
    WIDTH_BAR = 6


class Intro:
    # Intro
    POS_TEXT_Y = 300


class Main:
    DELAY = 500
    INTERVAL = 30


class Menu:
    # Menu
    NBR_BUTTONS_MENU = 7


class Modals:
    # Modals
    BSS_LARGE = 1000
    BSS_MEDIUM = 700
    BSS_SMALL = 400
    FRAME_LOAD_THICK = 3
    MAX_SAVES_IN_LIST = 17
    POS_ELEM_LOAD = 240
    POS_ELEM_SAVE = 60
    POS_TEXT_BSS_1 = 160
    POS_TEXT_BSS_2 = 90
    POS_TEXT_EXIT_1 = 110
    POS_TEXT_EXIT_2 = 60
    POS_TEXT_LDC = 110
    POS_TEXT_LOAD_TEAM_TITLE = 140
    POS_TEXT_YES_NO = 70


class NameSelectionMultiLocal:
    # Sélection du nom des joueurs
    ELEM_FAR = 100
    ELEM_NEAR = 50
    MARGIN_NEXT = 20
    MIN_LEN_NAME = 3


class Overlays:
    # Overlays
    BUTTON_ARROWS_MARGIN_MODAL = 20


class SquareBattlefield:
    # Carrés du champ de bataille
    CIRCLE_HEROES = 22
    HEROES = 44
    HEROES_MARGIN_BOT = 15
    LITTLE_SQUARE = 25
    MOVEMENT_ACTION_POINTS_PADDING = 10
    SQUARE = 50
    START_X = 112
    START_Y = 15
    THICK_BIG = 4
    THICK_SMALL = 2


class TeamSelection:
    # Team selection
    BOT_BUTTONS_TEXT = 40
    BUTTON_ARROWS_MARGIN = 123
    BUTTON_ARROWS_PADDING = 30
    BUTTONS_LOADSAVE_MARGIN = 120
    BUTTON_REMOVE_MARGIN = 50
    BUTTON_NEXT_MARGIN = 80
    COLUMN_LENGTH = 6
    DETAIL_INSPECTED_X = 770
    DETAILS_ZONE = 720
    DIFF_TOKEN_TEXT = 60
    LIMIT_RIGHT = 710
    LINE_LENGTH = 7
    MARGIN_X = 100
    MARGIN_Y = 100
    MINIATURE_INSPECTED_Y = 45
    NAME_INSPECTED_Y = 150
    NAME_MARGIN = 20
    SIZE_TEXT_MULTILINES = 39
    SQUARE_HOVERED_DIFF = 5
    SQUARE_SELECTED_DIFF = 2
    START_DETAILS_Y = 190
    START_TOKEN_X = 40
    START_TOKEN_Y = 30
    TOP_BUTTONS_ARROWS = 80


class Textbox:
    # Textbox
    ACCEPTED = string.ascii_letters + string.punctuation + string.digits
    BLINK_TIMER = 200
    TEXTBOX_HEIGHT = 30
    TEXTBOX_WIDTH = 200


class Texts:
    # Texts
    ADD = "ADD"
    BACK = "< BACK"
    CANCEL = "CANCEL"
    CARDS_ALL = "ALL"
    CARDS_EVIL = "EVIL"
    CARDS_GOOD = "GOOD"
    BSS_LARGE_TEXT = "LARGE"
    BSS_MEDIUM_TEXT = "MEDIUM"
    BSS_SMALL_TEXT = "SMALL"
    BSS_TEXT_1 = "CHOOSE A"
    BSS_TEXT_2 = "BATTLE SIZE"
    DECK = "DECK"
    DELETE = "DELETE"
    DESCRIPTION = "Description : "
    DRAW = "DRAW CARD"
    EFFECTS = "Effects : "
    END_TURN = "END TURN"
    FIRST_PLAYER_NAME = "First player's name : "
    HAND = "HAND"
    LINKED_TO = "Linked to :"
    LOAD = "LOAD"
    LOAD_DECK = "LOAD DECK"
    LOAD_TEAM = "LOAD TEAM"
    MENU_EXIT = "EXIT"
    MENU_LOCALMP = "LOCAL MULTIPLAYER"
    MENU_ONLINEMP = "ONLINE MULTIPLAYER"
    MENU_OPTIONS = "OPTIONS"
    MENU_SKIRMISH = "SKIRMISH"
    MENU_STORY = "STORY MODE"
    MENU_TUTO = "TUTORIAL"
    MODAL_EXIT_1 = "ARE YOU SURE"
    MODAL_EXIT_2 = "YOU WANT TO LEAVE ?"
    MODAL_LOAD = "CHOOSE A TEAM TO LOAD :"
    MODAL_POINTS_LEFT_1 = "YOU HAVE {} POINTS LEFT"
    MODAL_POINTS_LEFT_2 = "ARE YOU SURE YOU WANT TO LEAVE ?"
    MODAL_SAVE = "ENTER A SAVE NAME :"
    MORE = "MORE"
    NEXT = "NEXT"
    NO = "NO"
    PLAYER_1 = "Player 1"
    PLAYER_2 = "Player 2"
    REMOVE = "REMOVE"
    SAVE = "SAVE"
    SAVE_DECK = "SAVE DECK"
    SAVE_TEAM = "SAVE TEAM"
    SEARCH = "SEARCH :"
    SECOND_PLAYER_NAME = "Second player's name : "
    SKILLS = "Skills : "
    SORT_AVAIL = "AVAIL."
    SORT_BY = "SORT BY :"
    SORT_BY_NAME = "SORT BY NAME"
    SORT_BY_COST = "SORT BY COST"
    SORT_COST = "COST"
    SORT_NAME = "NAME"
    START = "START"
    SUSPENSION = "..."
    YES = "YES"


class Window:
    # Window
    SCREEN_HEIGHT = 768
    SCREEN_WIDTH = 1024
    WINDOW_TITLE = "Heroes of the Ring"
