import streamlit as st  
import pandas as pd
import numpy as np
chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=["a", "b", "c"])
st.title("Uputstvo za koriscenje aplikacije")
st.subheader("Ovde ide podnaslov")
col1, col2 = st.columns(2)
with col1:
    with st.expander("Uputstvo za koriscenje aplikacije (otvorite da vidite detalje)", expanded=False):
        st.write("Ovde ide uputstvo za koriscenje aplikacije")
        st.info("Ovde ide info poruka")
        st.success("Ovde ide potvrda uspeha")
        st.warning("Ovde ide upozorenje")
        st.error("Ovde erro message")
        st.image("https://test.georgemposi.com/wp-content/uploads/2023/05/positive-logo-red.jpg%22", width=200)
        st.video("https://youtu.be/zuCXesfBxzo")
        st.markdown("**Ovde ide markdown tekst**  __nesto__  *italic*  ~~strikethrough~~  `code`  [link](https://www.streamlit.io/)")
        st.latex(r''' e^{i\pi} + 1 = 0 ''')
    df = pd.DataFrame(
    np.random.randn(300, 2) / [50, 50] + [37.76, -122.4],
    columns=['lat', 'lon'])
    st.map(df)
with col2:
    st.date_input("Datum")
    st.time_input("Vreme")
    st.color_picker("Izaberi boju")
    st.json({"ime": "Marko", "prezime": "Markovic"})
    
    st.caption("Tabela je editabilna!!")
    df = pd.DataFrame(
        [
        {"command": "st.selectbox", "rating": 4, "is_widget": True},
        {"command": "st.balloons", "rating": 5, "is_widget": False},
        {"command": "st.time_input", "rating": 3, "is_widget": True},
    ]
    )
    edited_df = st.data_editor(df)
st.divider()
st.bar_chart(chart_data)
st.line_chart(chart_data)
st.area_chart(chart_data)

