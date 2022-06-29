import turtle
import pandas


# # This method prints the coordinates at the location on which you clicked
# def get_mouse_click_cord(x, y):
#     print(x, y)
# turtle.onscreenclick(get_mouse_click_cord)

screen = turtle.Screen()
screen.title("U. S. States Game")
img = "./us-states-game-start/blank_states_img.gif"
screen.addshape(img)
turtle.shape(img)

data = pandas.read_csv("./us-states-game-start/50_states.csv")
all_states = data.state.tolist()

guessed_states = []
while len(guessed_states) < 50:
    answer_state = screen.textinput(title=f"{len(guessed_states)}/50 States correct",
                                    prompt="What's another state's name").title()

    if answer_state == "Exit":
        missing_states = [state for state in all_states if state not in guessed_states]

        new_data = pandas.DataFrame(missing_states)
        new_data.to_csv("Missed States.csv")
        break
    
    # If answer state is one of the states in all states of the 50_states:
    if answer_state in all_states:
        # Create a turtle to write the name of the state at the state's x and y coordinate
        guessed_states.append(answer_state)
        t = turtle.Turtle()
        t.penup()
        t.hideturtle()
        
        # To get the row of the correctly guessed data
        state_data = data[data.state == answer_state]
        t.goto(int(state_data.x), int(state_data.y))
        t.write(answer_state)