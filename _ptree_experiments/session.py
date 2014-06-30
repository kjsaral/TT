from ptree.session import SessionType


def session_types():
    return [
        SessionType(
            name="Prisoner Dilemma",
            base_pay=400,
            num_participants=2,
            subsession_apps=['prisoner',],
            doc=""""""
        ),
        SessionType(
            name='Trust Game',
            base_pay=10,
            num_participants=2,
            subsession_apps=['trust',],
            doc=""""""
        ),
        SessionType(
            name='Public Goods',
            base_pay=10,
            num_participants=4,
            subsession_apps=['public_goods',],
            doc=""""""
        ),
        SessionType(
            name='Dictator',
            base_pay=100,
            num_participants=2,
            subsession_apps=['dictator',],
            doc=""""""
        ),
        SessionType(
            name='Matching Pennies',
            base_pay=100,
            num_participants=2,
            subsession_apps=['matching_pennies',],
            doc=""""""
        ),
        SessionType(
            name='Travelers Dilemma',
            base_pay=0,
            num_participants=2,
            subsession_apps=['travelers_dilemma',],
            doc=""""""
        ),
        SessionType(
            name='Simple Questionnaire',
            base_pay=0,
            num_participants=2,
            subsession_apps=['questionnaire_zurich',],
            doc=""""""
        ),
    ]


def show_on_demo_page(session_type_name):
    return True

demo_page_intro_text = """
Click on one of the below links to learn more and play.
You can read the source code of these games <a href="https://github.com/wickens/ptree_library">here</a>.
"""
