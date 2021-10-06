from typing import List
from app.ml_models.answer_generation.answer_generator import AnswerGenerator
from app.ml_models.distractor_generation.distractor_generator import DistractorGenerator
from app.ml_models.question_generation.question_generator import QuestionGenerator
from app.models.question import Question

#TODO: Call the neeeded ml models to generate the desired count of multiple choice quesitons. Currently using 3 different ML models, but later it could be only 1. 

def generate(context: str, desired_count: int) -> List[Question]:
    #TODO Clean the text

    questions = _generate_answers(context, desired_count)
    questions = _generate_questions(context, questions)
    questions = _generate_distractors(context, questions)
    
    for question in questions:
        print('-------------------')
        print(question.answerText)
        print(question.questionText)
        print(question.distractors)

    return questions

def _generate_answers(context: str, desired_count: int) -> List[Question]:
    answer_generator = AnswerGenerator()

    answers = answer_generator.generate(context, 4)

    #TODO: remove duplicate answers 

    questions = []
    for answer in answers:
        questions.append(Question(answer))

    return questions

def _generate_questions(context: str, questions: List[Question]) -> List[Question]:
    question_generator = QuestionGenerator()

    for question in questions:
        question.questionText = question_generator.generate(question.answerText, context)

    return questions

def _generate_distractors(context: str, questions: List[Question]) -> List[Question]:
    distractor_generator = DistractorGenerator()

    for question in questions:
        question.distractors = distractor_generator.generate(5, question.answerText, question.questionText, context)

    return questions