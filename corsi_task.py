from psychopy.visual import Window, Rect, TextStim, TextBox2
from psychopy import core, event
import numpy as np

DISPSIZE = (1920, 1080)

def grid800():
    grid = []
    for i in range(10):
        for j in range(10):
            x = (j * 80) - 360
            y = (i * 80) - 360
            grid.append({'x': x, 'y': y})
    return grid

def generateCordsForBlocks():
    grid = grid800()
    np.random.shuffle(grid)
    return grid[:9]

def drawNineBlocks(window, cords, clicked=None, ready_for_input=False):
    for i, cord in enumerate(cords):
        px, py = cord['x'], cord['y']
        position = (px, py)
        if clicked is not None and i in clicked:
            color = (-1, -1, 1)
            goLeft = TextStim(window, text=f"Go!", color='yellow', height=50, pos=(530, 30))
            goLeft.draw()
            goRight = TextStim(window, text=f"Go!", color='yellow', height=50, pos=(-530, 30))
            goRight.draw()
        elif ready_for_input:
            color = (1, 1, 1)
            goLeft = TextStim(window, text=f"Go!", color='yellow', height=50, pos=(530, 30))
            goLeft.draw()
            goRight = TextStim(window, text=f"Go!", color='yellow', height=50, pos=(-530, 30))
            goRight.draw()
        else:
            color = (1, 1, 1)
        block = Rect(window, width=70, height=70, units='pix', pos=position, color=color)
        block.draw()
    window.flip()

def lightUp(window, cords, num_blocks):
    sequence = np.random.choice(len(cords), min(num_blocks, len(cords)), replace=False)
    for i in sequence:
        for j, cord in enumerate(cords):
            px, py = cord['x'], cord['y']
            position = (px, py)
            if j == i:
                block_color = (-1, -1, 1)
            else:
                block_color = (1, 1, 1)
            block = Rect(window, width=70, height=70, units='pix', pos=position, color=block_color)
            block.draw()
        window.flip()
        core.wait(1)
        if event.getKeys(['escape']):
            return None
        drawNineBlocks(window, cords)
    return sequence

def checkClicks(window, cords, sequence):
    mouse = event.Mouse(win=window)
    clicked_sequence = []
    clicked_blocks = []
    last_clicked = None
    while len(clicked_sequence) < len(sequence):
        if mouse.getPressed()[0]:
            mouse_click = mouse.getPos()
            for j, cord in enumerate(cords):
                px, py = cord['x'], cord['y']
                if abs(mouse_click[0] - px) <= 35 and abs(mouse_click[1] - py) <= 35:
                    if j != last_clicked:
                        clicked_sequence.append(j)
                        clicked_blocks.append(j)
                        last_clicked = j
                        drawNineBlocks(window, cords, clicked_blocks, ready_for_input=True)
                    break
        event.clearEvents()
        if event.getKeys(['escape']):
            return None
    return clicked_sequence == list(sequence)

def main():
    nineCubesWindow = Window(size=DISPSIZE, color=(-1,-1,-1), fullscr=False, units='pix')
    max_sequence_length = 1
    fail_count = 0
    idText = TextStim(nineCubesWindow, text="Please enter the ID of the participant:", color='white', height=40, pos=(0, 200), wrapWidth=1200)
    participant_id_input = TextBox2(nineCubesWindow, text='', letterHeight=40, color='white', size=(800, 100), pos=(0, 0), alignment='center')
    cont = TextStim(nineCubesWindow, text="Press 'Enter' to continue!", color='yellow', height=30, pos=(0, -200), wrapWidth=1200)
    idText.draw()
    participant_id_input.draw()
    cont.draw()
    nineCubesWindow.flip()
    participant_id = ''
    while True:
        keys = event.getKeys()
        if keys:
            if 'escape' in keys:
                core.quit() 
            elif 'backspace' in keys:
                participant_id = participant_id[:-1]
            elif 'return' in keys:
                if participant_id:
                    break
            else:
                participant_id += keys[0]
            participant_id_input.setText(participant_id)
            idText.draw()
            participant_id_input.draw()
            cont.draw()
            nineCubesWindow.flip()
    intro1 = TextStim(nineCubesWindow, text="CORSI BLOCK-TAPPING TASK", color='white', height=70, pos=(0, 300), bold=True, wrapWidth=1200)
    intro2 = TextStim(nineCubesWindow, text="Welcome to the Corsi Block-Tapping Task! Nine white blocks will appear on the screen. Your objective is to replicate a sequence in which the blocks light up blue. A sequence will be presented, and when you see 'Go!' on the sides, it's your turn to click on the blocks in the same order. Once you click on a block, it can't be changed. If you get a sequence wrong, you'll get another chance. Your score is based on the longest sequence you reproduce correctly. Good luck!", color='white', height=40, pos=(0, 0), wrapWidth=1200)
    intro3 = TextStim(nineCubesWindow, text="Press 'Space' to begin!", color='yellow', height=30, pos=(0, -270))
    intro1.draw()
    intro2.draw()
    intro3.draw()
    nineCubesWindow.flip()
    event.waitKeys(keyList=['space', 'escape'])
    while True:
        if event.getKeys(['escape']):
            core.quit()
            break
        cords = generateCordsForBlocks()
        drawNineBlocks(nineCubesWindow, cords)
        core.wait(2)
        sequence = lightUp(nineCubesWindow, cords, max_sequence_length)
        if sequence is None:
            core.quit()
            break
        drawNineBlocks(nineCubesWindow, cords, ready_for_input=True)
        correct = checkClicks(nineCubesWindow, cords, sequence)
        if correct is None:
            core.quit()
            break
        if correct:
            feedback = TextStim(nineCubesWindow, text="Correct!", color='lime', height=100, pos=(0, 50))
            max_sequence_length += 1
            fail_count = 0
        else:
            feedback = TextStim(nineCubesWindow, text="Incorrect!", color='red', height=100, pos=(0, 50))
            fail_count += 1
        core.wait(0.5)
        feedback.draw()
        nineCubesWindow.flip()
        core.wait(1)
        if fail_count == 2 or max_sequence_length == 9:
            break
        core.wait(1)
        if event.getKeys(['escape']):
            core.quit()
            break
    endText1 = TextStim(nineCubesWindow, text=f"Corsi Span: {max_sequence_length - 1}", color='white', height=80, pos=(0, 70))
    endText2 = TextStim(nineCubesWindow, text="Press 'Space' to quit!", color='yellow', height=30, pos=(0, -20))
    endText1.draw()
    endText2.draw()
    nineCubesWindow.flip()
    event.waitKeys(keyList=['space', 'escape'])
    nineCubesWindow.close()
    data = open('corsi_data_output.csv', 'a')
    data.write(f'{participant_id},{max_sequence_length - 1},\n')
    data.close()
    print(f"Corsi Span: {max_sequence_length - 1}")

if __name__ == "__main__":
    main()
