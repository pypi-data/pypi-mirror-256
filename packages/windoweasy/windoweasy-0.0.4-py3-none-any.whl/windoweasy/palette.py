import windoweasy

color = windoweasy.Colors()

width = 700
height = 700
size = 100

title = 'windoweasy - pallete'
screen = windoweasy.Screen(width, height, title)


color_array = list(color.colors.values())
color_matrix = []
color_array_names = list(color.colors.keys())
color_matrix_names = []

n = 0
for i in range(7):
    color_matrix.append([])
    color_matrix_names.append([])
    for j in range(7):
        n += 1
        color_matrix_names[i].append(color_array_names[n-1])
        color_matrix[i].append(color_array[n-1])

@windoweasy.window(screen)
def main(s):
    for i in range(7):
        for j in range(7):
            rect_color = color_matrix[j][i]
            name = color_matrix_names[j][i]
            s.draw_rect(rect_color, i*100, j*100, size, size)
            s.draw_text(s.get_invert_color(rect_color, True, 255), name.replace('_', '\n').upper(), 30-(len(name)//(name.count('_')+1)), i*100+10, j*100+10, wrap=True)
            s.draw_text(s.get_invert_color(rect_color, True, 255), name.upper(), 15-(3 if name.upper() == 'DARK_GRAYISH_GREEN' else 0), i*100+3, j*100+85, wrap=True)

    s.update(30)


main()