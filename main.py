import pandas as pd
import streamlit as st    
import random

INITIAL_QUESTION_TYPE = '빅데이터 분석기사'
QUESTION_TYPE_OPTIONS = ['빅데이터 분석기사', '통계학', '확률과 통계']

@st.cache_data
def read_data1():
    '''빅데이터 분석기사'''
    ret = pd.read_csv('https://www.dropbox.com/s/odjd1akl32q4gum/%EB%B9%85%EB%8D%B0%EC%9D%B4%ED%84%B0_%EB%B6%84%EC%84%9D%EA%B8%B0%EC%82%AC_%EC%B1%97%EB%B4%87.csv?dl=1')
    return ret

@st.cache_data
def read_data2():
    '''통계학'''
    ret = pd.read_csv('https://www.dropbox.com/s/zdpl4zi5l3v9c9m/%ED%86%B5%EA%B3%84%ED%95%99_%EC%B1%97%EB%B4%87.csv?dl=1')
    return ret

@st.cache_data
def read_data3():
    '''확률과 통계'''
    ret = pd.read_csv('https://www.dropbox.com/s/du1lbvsg4uex19j/%ED%99%95%EB%A5%A0%EA%B3%BC%ED%86%B5%EA%B3%84_%EC%B1%97%EB%B4%87.csv?dl=1')
    return ret


if 'user_state' not in st.session_state:
    st.session_state['user_state'] = 'question'
    
def update_question_no(data):
    user_state = st.session_state['user_state']
    if user_state == 'submit':
        return
    len_df = int(len(data))
    idx = random.randint(0, len_df-1)
    st.session_state['question_no'] = idx
    
if 'question_type' not in st.session_state:
    st.session_state['question_type'] = INITIAL_QUESTION_TYPE
    
if 'prev_question_type' not in st.session_state:
    st.session_state['prev_question_type'] = INITIAL_QUESTION_TYPE
    
def update_question_type(data):
    if st.session_state['question_type'] != st.session_state['prev_question_type']:
        st.session_state['prev_question_type'] = st.session_state['question_type']
        update_question_no(df)
    
if st.session_state['question_type'] == QUESTION_TYPE_OPTIONS[0]:
    df = read_data1()
    update_question_type(df)
elif st.session_state['question_type'] == QUESTION_TYPE_OPTIONS[1]:
    df = read_data2()
    update_question_type(df)
elif st.session_state['question_type'] == QUESTION_TYPE_OPTIONS[2]:
    df = read_data3()
    update_question_type(df)

if 'question_no' not in st.session_state:
    update_question_no(df)
    
if 'user_selection' not in st.session_state:
    st.session_state['user_selection'] = 0

title = st.empty()

def selectbox_callback():
    st.session_state['disabled'] = False
    
question_type = st.selectbox('문제유형', options=QUESTION_TYPE_OPTIONS, key='question_type', on_change=selectbox_callback)
    
def create_questions():
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

if 'disabled' not in st.session_state:
    st.session_state['disabled'] = False

def disable():
    st.session_state['disabled'] = True

q = create_questions()
st.session_state['true_answer'] = q['answer']
st.session_state['comments'] = q['comments']
title.title(f'문제유형: {st.session_state["question_type"]}')
form =  st.form('question_form')
form.markdown(f"난이도 ({q['level']})")
form.markdown(q['question'])
radio_select = form.radio('<보기>', options=q['options'], key='user_answer')
submit_btn = form.form_submit_button('제출', disabled=st.session_state['disabled'], type='primary', use_container_width=True, on_click=disable)

next_btn = st.button('다음 문제', use_container_width=False)
correction = st.empty()
true_value = st.empty()
comment_title = st.empty()
comment_section = st.empty()
    
if submit_btn:
    st.session_state['disabled'] = True
    st.session_state['user_state'] = 'submit'
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
    


st.markdown('----\n✨모든 문제는 ChatGPT 3.5 엔진 기반으로 생성된 문제이며, **정답에 대한 신뢰성을 100% 보장하지 않으므로**, 이점 유념해 주시기 바랍니다🙏🙏')
st.markdown('- teddylee777@gmail.com\n- https://teddylee777.github.io')
if next_btn:
    st.session_state['disabled'] = False
    len_df = int(len(df))
    idx = random.randint(0, len_df-1)
    st.session_state['question_no'] = idx
    st.experimental_rerun()
    
    
        
