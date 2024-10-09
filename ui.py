from tkinter import *
from quiz_brain import QuizBrain

THEME_COLOR = "#375362"
CANVAS_WIDTH = 500
CANVAS_HEIGHT = 300
QUESTION_WIDTH = CANVAS_WIDTH - 20


class QuizInterface:

    def __init__(self, quiz_brain: QuizBrain):

        self.quiz = quiz_brain

        # Window configurations
        self.window = Tk()
        self.window.title("Quiz App")
        self.window.config(padx=20, pady=20, bg=THEME_COLOR)

        # Score label
        self.score_label = Label(text="Score: 0",
                                 bg=THEME_COLOR,
                                 fg="white",
                                 font=("Arial", 16, "bold")
                                 )
        self.score_label.grid(row=0, column=1)

        # Canvas
        self.canvas = Canvas()
        self.canvas.config(height=CANVAS_HEIGHT, width=CANVAS_WIDTH, bg="white")

        # Question Text
        self.question_text = self.canvas.create_text(CANVAS_WIDTH // 2,
                                                     CANVAS_HEIGHT // 2,
                                                     text="Question: What is your name?",
                                                     fill=THEME_COLOR)
        self.canvas.itemconfig(self.question_text, font=("Arial", 20, "italic"), width=QUESTION_WIDTH)

        self.canvas.grid(row=1, column=0, columnspan=2, pady=50)

        # True Button
        true_image = PhotoImage(file="images/true.png")
        self.true_button = Button(image=true_image, highlightthickness=0, command=self.true_command)
        self.true_button.grid(row=2, column=0)

        # False Button
        false_image = PhotoImage(file="images/false.png")
        self.false_button = Button(image=false_image, highlightthickness=0, command=self.false_command)
        self.false_button.grid(row=2, column=1)

        # Get next question
        self.get_next_question()

        self.window.mainloop()

    def get_next_question(self):
        """
        Get next question from Quiz brain
        """
        self.set_background()
        self.score_label.config(text=f"Score: {self.quiz.score}")
        if self.quiz.still_has_questions():
            q_text = self.quiz.next_question()
            self.canvas.itemconfig(self.question_text, text=q_text)
        else:
            self.display_result()

    def true_command(self):
        """
        Code to execute when true button was clicked
        """
        background_color = "red"
        # For a correct answer, update score and background color to change canvas
        if self.quiz.check_answer(user_answer="true"):
            background_color = "green"

        # Update canvas with next question
        self.set_background(bg=background_color)
        self.window.after(1000, self.get_next_question)

    def false_command(self):
        """
        Code to execute when false button was clicked
        """
        background_color = "red"

        # For a correct answer, update score and background color to change canvas
        if self.quiz.check_answer(user_answer="false"):
            background_color = "green"

        # Update canvas with next question
        self.set_background(bg=background_color)
        self.window.after(1000, self.get_next_question)

    def set_background(self, bg: str = "white"):
        """
        Set canvas background back to white
        """
        self.canvas.config(bg=bg)

    def display_result(self):
        """
        Display final score after quiz is completed
        """
        self.true_button.config(state="disabled")
        self.false_button.config(state="disabled")
        self.canvas.itemconfig(self.question_text,
                               text=f"Quiz Completed!"
                                    f"\nFinal Score: {self.quiz.score}/{len(self.quiz.question_list)}")