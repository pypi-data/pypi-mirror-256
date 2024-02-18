print("windoweasy X pygame")
print("our contact: None")

class Colors:
    RED = (255, 0, 0)
    LIME = (0, 255, 0)
    BLUE = (0, 0, 254)
    YELLOW = (255, 255, 0)
    ORANGE = (255, 165, 0)
    CYAN = (0, 255, 255)
    NAVY = (0, 0, 128)
    TEAL = (0, 128, 128)
    GREEN = (0, 128, 0)
    OLIVE = (128, 128, 0)
    PURPLE = (127, 0, 127)
    FUCHSIA = (255, 0, 255)
    BLACK = (0, 0, 0)
    GRAY = (128, 128, 128)
    SILVER = (192, 192, 192)
    WHITE = (255, 255, 255)
    AQUA = (128, 255, 255)
    DARK_AQUA = (128, 205, 205)
    MAROON = (128, 0, 0)
    PINK = (255, 192, 203)
    GOLD = (255, 215, 0)
    DARK_GREEN = (0, 100, 0)
    DARK_GRAY = (64, 64, 64)
    LIGHT_GRAY = (211, 211, 211)
    INDIGO = (75, 0, 130)
    BROWN = (165, 42, 42)
    DARK_BLUE = (0, 0, 139)
    DARK_RED = (139, 0, 0)
    LIGHT_GREEN = (144, 238, 144)
    LIGHT_BLUE = (173, 216, 230)
    LIGHT_YELLOW = (255, 255, 224)
    LIGHT_PINK = (255, 182, 193)
    DARK_ORANGE = (255, 140, 0)
    DARK_CYAN = (0, 139, 139)
    DARK_BROWN = (101, 67, 33)
    LIGHT_BROWN = (210, 180, 140)
    DARK_PINK = (255, 105, 180)
    DARK_GOLD = (184, 134, 11)
    DARKER_PURPLE = (72, 61, 139)
    LIGHTER_PURPLE = (221, 160, 221)
    LIGHT_ORANGE = (255, 204, 153)
    LIGHT_CYAN = (224, 255, 255)
    DARK_YELLOW = (204, 204, 0)
    NAVY_BLUE = (0, 0, 128)
    TEAL_GREEN = (0, 128, 128)
    LIGHT_GOLD = (255, 215, 0)
    LIGHT_PURPLE = (204, 153, 255)
    DARK_GRAYISH_GREEN = (51, 64, 47)
    LIGHT_CORAL = (240, 128, 128)

    colors = {
        "red": RED, "lime": LIME, "blue": BLUE, "yellow": YELLOW, "orange": ORANGE, "cyan": CYAN, "navy": NAVY,
        "teal": TEAL, "green": GREEN, "olive": OLIVE, "purple": PURPLE, "fuchsia": FUCHSIA, "black": BLACK,
        "gray": GRAY, "silver": SILVER, "white": WHITE, "aqua": AQUA, "dark_aqua": DARK_AQUA,"maroon": MAROON, "pink": PINK, "gold": GOLD,
        "dark_green": DARK_GREEN, "dark_gray": DARK_GRAY, "light_gray": LIGHT_GRAY, "indigo": INDIGO, "brown": BROWN,
        "dark_blue": DARK_BLUE, "dark_red": DARK_RED, "light_green": LIGHT_GREEN, "light_blue": LIGHT_BLUE,
        "light_yellow": LIGHT_YELLOW, "light_pink": LIGHT_PINK, "dark_orange": DARK_ORANGE, "dark_cyan": DARK_CYAN,
        "dark_brown": DARK_BROWN, "light_brown": LIGHT_BROWN, "dark_pink": DARK_PINK, "dark_gold": DARK_GOLD,
        "darker_purple": DARKER_PURPLE, "lighter_purple": LIGHTER_PURPLE, "light_orange": LIGHT_ORANGE,
        "light_cyan": LIGHT_CYAN, "dark_yellow": DARK_YELLOW, "navy_blue": NAVY_BLUE, "teal_green": TEAL_GREEN,
        "light_gold": LIGHT_GOLD, "light_purple": LIGHT_PURPLE, "dark_grayish_green": DARK_GRAYISH_GREEN,
        "light_coral": LIGHT_CORAL
    }

def window(screen):
    def decorator(func):
        def wrapper():
            running = True
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                func(screen)
            pygame.quit()
        return wrapper
    return decorator

class Screen:
    def __init__(self, width, height, title='windoweasy - pygame'):
        global pygame
        import pygame

        pygame.init() 
        self.clock = pygame.time.Clock()

        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)

    def update(self, fps=240, clear=(0, 0, 0)):
        self.clock.tick(fps)
        pygame.display.flip()
        if clear: self.change_bg_color(clear)

    def change_title(self, caption):
        pygame.display.set_caption(caption)

    def change_bg_color(self, color):
        self.screen.fill(color)



    def get_title(self):
        return pygame.display.get_caption()

    def get_fps(self):
        return self.clock.get_fps()

    def get_rect(self, height1, width1, height2, width2):
        return (height1, width1, height1+height2, width1+width2)

    def get_keys(self):
        key_pressed = pygame.key.get_pressed()
        all_keys = {
            "backspace": key_pressed[pygame.K_BACKSPACE],
            "tab": key_pressed[pygame.K_TAB],
            "return": key_pressed[pygame.K_RETURN],
            "escape": key_pressed[pygame.K_ESCAPE],
            "space": key_pressed[pygame.K_SPACE],
            "exclaim": key_pressed[pygame.K_EXCLAIM],
            "quotedbl": key_pressed[pygame.K_QUOTEDBL],
            "hash": key_pressed[pygame.K_HASH],
            "dollar": key_pressed[pygame.K_DOLLAR],
            "ampersand": key_pressed[pygame.K_AMPERSAND],
            "quote": key_pressed[pygame.K_QUOTE],
            "leftparen": key_pressed[pygame.K_LEFTPAREN],
            "rightparen": key_pressed[pygame.K_RIGHTPAREN],
            "asterisk": key_pressed[pygame.K_ASTERISK],
            "plus": key_pressed[pygame.K_PLUS],
            "comma": key_pressed[pygame.K_COMMA],
            "minus": key_pressed[pygame.K_MINUS],
            "period": key_pressed[pygame.K_PERIOD],
            "slash": key_pressed[pygame.K_SLASH],
            "0": key_pressed[pygame.K_0],
            "1": key_pressed[pygame.K_1],
            "2": key_pressed[pygame.K_2],
            "3": key_pressed[pygame.K_3],
            "4": key_pressed[pygame.K_4],
            "5": key_pressed[pygame.K_5],
            "6": key_pressed[pygame.K_6],
            "7": key_pressed[pygame.K_7],
            "8": key_pressed[pygame.K_8],
            "9": key_pressed[pygame.K_9],
            "colon": key_pressed[pygame.K_COLON],
            "semicolon": key_pressed[pygame.K_SEMICOLON],
            "less": key_pressed[pygame.K_LESS],
            "equals": key_pressed[pygame.K_EQUALS],
            "greater": key_pressed[pygame.K_GREATER],
            "question": key_pressed[pygame.K_QUESTION],
            "at": key_pressed[pygame.K_AT],
            "leftbracket": key_pressed[pygame.K_LEFTBRACKET],
            "backslash": key_pressed[pygame.K_BACKSLASH],
            "rightbracket": key_pressed[pygame.K_RIGHTBRACKET],
            "caret": key_pressed[pygame.K_CARET],
            "underscore": key_pressed[pygame.K_UNDERSCORE],
            "backquote": key_pressed[pygame.K_BACKQUOTE],
            "a": key_pressed[pygame.K_a],
            "b": key_pressed[pygame.K_b],
            "c": key_pressed[pygame.K_c],
            "d": key_pressed[pygame.K_d],
            "e": key_pressed[pygame.K_e],
            "f": key_pressed[pygame.K_f],
            "g": key_pressed[pygame.K_g],
            "h": key_pressed[pygame.K_h],
            "i": key_pressed[pygame.K_i],
            "j": key_pressed[pygame.K_j],
            "k": key_pressed[pygame.K_k],
            "l": key_pressed[pygame.K_l],
            "m": key_pressed[pygame.K_m],
            "n": key_pressed[pygame.K_n],
            "o": key_pressed[pygame.K_o],
            "p": key_pressed[pygame.K_p],
            "q": key_pressed[pygame.K_q],
            "r": key_pressed[pygame.K_r],
            "s": key_pressed[pygame.K_s],
            "t": key_pressed[pygame.K_t],
            "u": key_pressed[pygame.K_u],
            "v": key_pressed[pygame.K_v],
            "w": key_pressed[pygame.K_w],
            "x": key_pressed[pygame.K_x],
            "y": key_pressed[pygame.K_y],
            "z": key_pressed[pygame.K_z],
            "delete": key_pressed[pygame.K_DELETE],
            "kp0": key_pressed[pygame.K_KP0],
            "kp1": key_pressed[pygame.K_KP1],
            "kp2": key_pressed[pygame.K_KP2],
            "kp3": key_pressed[pygame.K_KP3],
            "kp4": key_pressed[pygame.K_KP4],
            "kp5": key_pressed[pygame.K_KP5],
            "kp6": key_pressed[pygame.K_KP6],
            "kp7": key_pressed[pygame.K_KP7],
            "kp8": key_pressed[pygame.K_KP8],
            "kp9": key_pressed[pygame.K_KP9],
            "kp_period": key_pressed[pygame.K_KP_PERIOD],
            "kp_divide": key_pressed[pygame.K_KP_DIVIDE],
            "kp_multiply": key_pressed[pygame.K_KP_MULTIPLY],
            "kp_minus": key_pressed[pygame.K_KP_MINUS],
            "kp_plus": key_pressed[pygame.K_KP_PLUS],
            "kp_enter": key_pressed[pygame.K_KP_ENTER],
            "kp_equals": key_pressed[pygame.K_KP_EQUALS],
            "up": key_pressed[pygame.K_UP],
            "down": key_pressed[pygame.K_DOWN],
            "left": key_pressed[pygame.K_LEFT],
            "right": key_pressed[pygame.K_RIGHT],
            "insert": key_pressed[pygame.K_INSERT],
            "home": key_pressed[pygame.K_HOME],
            "end": key_pressed[pygame.K_END],
            "pageup": key_pressed[pygame.K_PAGEUP],
            "pagedown": key_pressed[pygame.K_PAGEDOWN],
            "f1": key_pressed[pygame.K_F1],
            "f2": key_pressed[pygame.K_F2],
            "f3": key_pressed[pygame.K_F3],
            "f4": key_pressed[pygame.K_F4],
            "f5": key_pressed[pygame.K_F5],
            "f6": key_pressed[pygame.K_F6],
            "f7": key_pressed[pygame.K_F7],
            "f8": key_pressed[pygame.K_F8],
            "f9": key_pressed[pygame.K_F9],
            "f10": key_pressed[pygame.K_F10],
            "f11": key_pressed[pygame.K_F11],
            "f12": key_pressed[pygame.K_F12],
            "numlock": key_pressed[pygame.K_NUMLOCK],
            "capslock": key_pressed[pygame.K_CAPSLOCK],
            "scrollock": key_pressed[pygame.K_SCROLLOCK],
            "rshift": key_pressed[pygame.K_RSHIFT],
            "lshift": key_pressed[pygame.K_LSHIFT],
            "rctrl": key_pressed[pygame.K_RCTRL],
            "lctrl": key_pressed[pygame.K_LCTRL],
            "ralt": key_pressed[pygame.K_RALT],
            "lalt": key_pressed[pygame.K_LALT],
            "rmeta": key_pressed[pygame.K_RMETA],
            "lmeta": key_pressed[pygame.K_LMETA],
            "lsuper": key_pressed[pygame.K_LSUPER],
            "rsuper": key_pressed[pygame.K_RSUPER],
            "mode": key_pressed[pygame.K_MODE],
            "help": key_pressed[pygame.K_HELP],
            "print": key_pressed[pygame.K_PRINT],
            "sysreq": key_pressed[pygame.K_SYSREQ],
            "break": key_pressed[pygame.K_BREAK],
            "menu": key_pressed[pygame.K_MENU],
            "power": key_pressed[pygame.K_POWER],
            "euro": key_pressed[pygame.K_EURO]}

        return all_keys

    def get_mouse(self):
        mouse_buttons = pygame.mouse.get_pressed()
        return {'pos': {'x': pygame.mouse.get_pos()[0], 'y': pygame.mouse.get_pos()[1]},
                'lmb': mouse_buttons[0],
                'scroll': mouse_buttons[1],
                'rmb': mouse_buttons[2]
               }

    def point_in_range(self, x, y, x1, y1=-1, x2=-1, y2=-1):
        if -1 in (y1, x2, y2): x1, y1, x2, y2 = x1[0], x1[1], x1[2], x1[3]
        if x1 <= x <= x2 and y1 <= y <= y2:
            return True
        else:
            return False

    def get_invert_color(self, rgb, white_n_black=False, entry_threshold=255):
        if white_n_black:
            if rgb[0] + rgb[1] >= entry_threshold or rgb[1] + rgb[2] >= entry_threshold or rgb[0] + rgb[2] >= entry_threshold:
                return (0, 0, 0)
            return (255, 255, 255)
        else:
            if rgb[0] == rgb[1] == rgb[2]:
                if rgb[0] + rgb[1] >= 255:
                    return (0, 0, 0)
                return (255, 255, 255)
            return tuple(255 - value for value in rgb)




    def draw_text(self, color, text, fontsize, x, y, bg=None, font=None, smoothing=True, wrap=False):
        font = pygame.font.SysFont(font, fontsize)
        if wrap:
            lines = text.split("\n")
            rendered_lines = []
            for line in lines:
                rendered_lines.append(font.render(line, smoothing, color))
            line_height = font.get_linesize()
            for i, rendered_line in enumerate(rendered_lines):
                line_y = y + i * line_height
                self.screen.blit(rendered_line, (x, line_y))
        else:
            text_surface = font.render(text, smoothing, color)
            self.screen.blit(text_surface, (x, y))


    def draw_rect(self, color, x, y, height, width=-1):
        if width == -1: width = height
        pygame.draw.rect(self.screen, color, (x, y, height, width))
        return {'x': x, 'y': y, 'height': height, 'width': width}

    def draw_line(self, color, startx, starty, endx, endy, width=1):
        pygame.draw.line(self.screen, color, (startx, starty), (endx, endy), width)

    def draw_ellipse(self, color, rect, width=0):
        pygame.draw.ellipse(self.screen, color, rect, width)