import pandas as pd
import streamlit as st    
import random

@st.cache
def read_data():
    ret = pd.read_csv('https://www.dropbox.com/s/odjd1akl32q4gum/%EB%B9%85%EB%8D%B0%EC%9D%B4%ED%84%B0_%EB%B6%84%EC%84%9D%EA%B8%B0%EC%82%AC_%EC%B1%97%EB%B4%87.csv?dl=1')
    return ret

df = read_data()

if 'user_state' not in st.session_state:
    st.session_state['user_state'] = 'question'

if 'question_no' not in st.session_state:
    len_df = int(len(df))
    idx = random.randint(0, len_df-1)
    st.session_state['question_no'] = idx
    
if 'user_selection' not in st.session_state:
    st.session_state['user_selection'] = 0
    
def create_questions():
    # print('CREATE QUESTION', st.session_state['question_no'])
    idx = st.session_state['question_no']
    question = df.loc[idx, '문제']
    options = df.loc[idx, ['보기1', '보기2', '보기3', '보기4']].values
    answer = df.loc[idx, '정답_num']
    comments = df.loc[idx, '해설']
    level = df.loc[idx, '난이도']
    return {
        'question': question, 
        'options': options,
        'answer': int(answer),
        'comments': comments, 
        'level': level,
    }
    
def get_index(selection, options):
    for idx, value in enumerate(options):
        if selection == value:
            return idx
    return 0

q = create_questions()
st.session_state['true_answer'] = q['answer']
st.session_state['comments'] = q['comments']
st.title('빅데이터 분석기사 기출문제')
form =  st.form('question_form')
form.markdown(f"난이도 ({q['level']})")
form.markdown(q['question'])
radio_select = form.radio('<보기>', options=q['options'], key='user_answer')
submit_btn = form.form_submit_button('제출')

correction = st.empty()
true_value = st.empty()
comment_title = st.empty()
comment_section = st.empty()

def clear_everything():
    st.session_state['user_state'] = 'question'
    st.session_state['user_selection'] = 0
    q = create_questions() 
    correction = st.empty()
    true_value = st.empty()
    comment_title = st.empty()
    comment_section = st.empty()
    len_df = int(len(df))
    idx = random.randint(0, len_df-1)
    st.session_state['question_no'] = idx

    
if submit_btn:
    st.session_state['disabled'] = True
    answer = st.session_state['user_answer']
    true_answer = st.session_state['true_answer']
    user_selection = get_index(answer, q['options'])
    st.session_state['user_selection'] = user_selection
    if user_selection == (int(true_answer) - 1):
        correction.markdown('`정답`입니다👍👍👍')
    else:
        correction.markdown('아쉽게도 `오답`입니다😱😱 정답은👇👇')
    true_value.warning(q['options'][int(true_answer) - 1])
    comment_title.write('🔥해설🔥')
    comment_section.info(st.session_state['comments'])
    
    
    st.session_state['user_state'] = 'answer'
    len_df = int(len(df))
    idx = random.randint(0, len_df-1)
    st.session_state['question_no'] = idx

next_btn = st.button('다음 문제', type='primary')
st.markdown('----\n✨모든 문제는 ChatGPT 3.5 엔진 기반으로 생성된 문제이며, **정답에 대한 신뢰성을 100% 보장하지 않으므로**, 이점 유념해 주시기 바랍니다🙏🙏')
st.markdown('- teddylee777@gmail.com\n- https://teddylee777.github.io')
if next_btn:
    len_df = int(len(df))
    idx = random.randint(0, len_df-1)
    st.session_state['question_no'] = idx
    st.experimental_rerun()
    
    
        
