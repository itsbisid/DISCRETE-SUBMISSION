import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import app
from bs4 import BeautifulSoup

c=app.test_client()
# Start a quiz with 1 question
r=c.post('/quiz/start', data={'count':'1'}, follow_redirects=True)
r=c.get('/quiz')
soup=BeautifulSoup(r.data,'html.parser')
q_text=soup.select_one('.question').text.strip()
print('Question:', q_text)
options=[el.text.strip() for el in soup.select('.opt span')]
print('Options:', options)

with c.session_transaction() as sess:
    q=sess['quiz_questions'][sess['quiz_index']]
    answer_letter=q['answer']
    letter_to_index={'A':0,'B':1,'C':2,'D':3}
    correct_value=q['options'][letter_to_index[answer_letter]]

print('Correct option text:', correct_value)
# Choose the first wrong option
wrong_value=next(v for v in options if v!=correct_value)
print('Submitting wrong answer:', wrong_value)
r=c.post('/quiz', data={'answer':wrong_value}, follow_redirects=True)
soup=BeautifulSoup(r.data,'html.parser')
hint_div=soup.select_one('.hint')
print('Hint present?', bool(hint_div))
print('Hint text:', hint_div.text.strip() if hint_div else 'N/A')
# Now test Finish button points correctly
finish_link=soup.select_one('a.btn.secondary')
print('Finish link href:', finish_link['href'])

# Now simulate a correct submission and ensure hint is not shown
print('--- Testing correct answer behavior ---')
# Restart quiz
r=c.post('/quiz/start', data={'count':'1'}, follow_redirects=True)
r=c.get('/quiz')
soup=BeautifulSoup(r.data,'html.parser')
with c.session_transaction() as sess:
    q=sess['quiz_questions'][sess['quiz_index']]
    answer_letter=q['answer']
    letter_to_index={'A':0,'B':1,'C':2,'D':3}
    correct_value=q['options'][letter_to_index[answer_letter]]
print('Submitting correct answer:', correct_value)
r=c.post('/quiz', data={'answer':correct_value}, follow_redirects=True)
soup=BeautifulSoup(r.data,'html.parser')
hint_div=soup.select_one('.hint')
print('Hint present after correct answer?', bool(hint_div))
