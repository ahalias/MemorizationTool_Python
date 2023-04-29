from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///flashcard.db?check_same_thread=False')

Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class Flashcard(Base):
    __tablename__ = "flashcard"
    id = Column(Integer, primary_key=True)
    question = Column(String, nullable=False)
    answer = Column(String, nullable=False)
    box = Column(Integer, nullable=False, default=1)

Base.metadata.create_all(engine)


class MemTool:
    def __init__(self):
        pass

    def process_menu(self, menu_items):
        for index, item in menu_items.items():
            print(index, item)

    def main_menu(self):
        menu_items = {'1.': 'Add flashcards', '2.': 'Practice flashcards', '3.': 'Exit'}
        self.process_menu(menu_items)
        inp = input()
        options = {"1": self.add_flashcards_menu, "2":  self.practice_flashcards, "3": self.exit}
        try:
            options[inp]()
        except Exception as e:
            print(f"{inp} is not an option")

    def add_flashcards_menu(self):
        menu_items = {'1.': 'Add a new flashcard', '2.': 'Exit'}
        self.process_menu(menu_items)
        inp = input()
        options = {"1": self.add_flashcard, "2": self.exit}
        try:
            options[inp]()
        except Exception as e:
            print(f"{inp} is not an option")
            self.add_flashcards_menu()

    def practice_flashcards(self):
        if not session.query(Flashcard).all():
            print("There is no flashcard to practice!")
            self.main_menu()
        for card in session.query(Flashcard).all():
            print(f"Question: {card.question}")
            inp = input('''press "y" to see the answer:
press "n" to skip:
press "u" to update:''')
            if inp == "y":
                print(f"Answer: {card.answer}")
                card_stat = input('''press "y" if your answer is correct:
press "n" if your answer is wrong:''')
                if card_stat == "y":
                    if card.box == 2:
                        session.delete(card)
                        session.commit()
                    else:
                        card.box += 1
                        session.commit()

                elif card_stat == "n":
                    card.box = 1
                    session.commit()
                else:
                    print(f"{card_stat} is not an option")
            if inp == "u":
                self.update_card(card)
            elif inp == "n":
                pass

    def update_card(self, card):
        inp = input('''press "d" to delete the flashcard:
press "e" to edit the flashcard:''')
        if inp == "e":
            print(f"current question: {card.question}")
            new_question = input("please write a new question:")
            card.question = new_question
            print(f"current answer: {card.answer}")
            new_answer = input("please write a new answer:\n")
            card.answer = new_answer
            session.commit()
        if inp == "d":
            session.delete(card)
            session.commit()


    def add_flashcard(self):
        question = ""
        answer = ""
        while not question.strip():
            question = input("Question:\n")
        while not answer.strip():
            answer = input("Answer:\n")
        flashcard = Flashcard(question=question, answer=answer)
        session.add(flashcard)
        session.commit()
        self.add_flashcards_menu()

    def exit(self):
        print("Bye!")
        exit()



memTool = MemTool()
while True:
    memTool.main_menu()



