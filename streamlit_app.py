import streamlit as st
import pandas as pd
import time


st.set_page_config(
   page_title = "Aslan Kazbek",
   page_icon="🔱",
   layout="centered",
)
st.title("🎈 Test my new app")
st.write(
   "My new app"
)
@st.cache_data
def load_data(url):
   df = pd.read_csv(url, sep=',', index_col=0)
   return df

df = load_data("hw_25000.csv")
st.dataframe(df.style.highlight_max(axis=0), use_container_width=True)
if st.checkbox("Show line chart"):
   st.line_chart(df.head(50), use_container_width=True)
# st.write(df.head(4))
# st.table(df)

st.title('test_FORMS')
with st.form('my form'):
   st.write("Inside from")
   slider_val = st.slider("slider val", min_value=0, max_value=10, value=2)
   chek_box = st.checkbox("check box")

   submitted = st.form_submit_button("Submit")
   if submitted:
      st.write("Slider",slider_val, "Checkbox", chek_box)
st.write("Outside from")

st.button("Rerun")
df_new = pd.DataFrame({
   'fisrt_column':['a','b',3,4],
   'second_column':[5,6,7,8]
   })
option = st.sidebar.selectbox(
   'Something chose',
   df_new['fisrt_column'])
'You chosed: ', option

left_column, right_column, third_clomn = st.columns(3)
with left_column:
   cont_1 = left_column.container(height=100)
   cont_1.write('Something in container')
   cont_1.divider()
   cont_1.write('new text')

with right_column:
   chosen = st.radio('Sorting hat',
                     ('a1','b2','c3'))
   st.write(f"Hat give:{chosen}!")
with third_clomn:
   st.metric(label='Metric', value='95%', delta='5%')

Some_text = """
asdag sakgj;g asd as sfgsndl fmxvm;b
sf jdsfg kjn dflkv ndslkrg **asdasd** asd sg
fdsgk jnsdfkgj dvdfg fg gdfh
"""
def stream_data():
   for word in Some_text.split(" "):
      yield word + " "
      time.sleep(0.08)

if st.button("Stream data"):
   st.write_stream(stream_data)