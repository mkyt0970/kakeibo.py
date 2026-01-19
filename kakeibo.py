

import streamlit as st
import pandas as pd
import datetime
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = "Hiragino Sans"

#CSV読み込み
def load_data():
    try:
        return pd.read_csv("家計簿.csv")
    except FileNotFoundError:
        return pd.DataFrame(columns=["日付","カテゴリ","金額","メモ"])
    
df = load_data()

if not df.empty:
    df["日付"] = pd.to_datetime(df["日付"],format = 'mixed')
    df["年月"] = df["日付"].dt.to_period("M")

st.title("家計簿アプリ")

#入力フォーム
with st.form("entry_form"):
    date = st.date_input("日付",datetime.date.today())
    category = st.selectbox("カテゴリ",["食費","交通費","娯楽","その他"])
    amount = st.number_input("金額",min_value=0)
    memo = st.text_input("メモ")
    submitted = st.form_submit_button("追加")

    if submitted:
        new_data = pd.DataFrame([[date,category,amount,memo]],
                                columns=["日付","カテゴリ","金額","メモ"])
        df = pd.concat([df,new_data],ignore_index=True)
        df.to_csv("家計簿.csv",index=False)
        st.success("データを追加しました")
        st.rerun()

#表示
st.subheader("履歴")

if not df.empty:
    #削除ボタン付きテーブル
    for i, row in df.iterrows():
        cols = st.columns([2, 2, 2, 3, 1])
        cols[0].write(row["日付"])
        cols[1].write(row["カテゴリ"])
        cols[2].write(row["金額"])
        cols[3].write(row["メモ"])
        if cols[4].button("削除", key=f"del_{i}"):
            df = df.drop(i).reset_index(drop=True)
            df.to_csv("家計簿.csv", index=False)
            st.success("削除しました")
            st.rerun()
else:
    st.write("データがありません。")


#円グラフ（カテゴリ別支出）
if not df.empty:
    months = sorted(df["年月"].astype(str).unique(),reverse=True)
    selected_month = st.selectbox("表示する月を選択",months)

    monthly_data = df[df["年月"].astype(str) == selected_month]
    if not monthly_data.empty:
        category_sum = monthly_data.groupby("カテゴリ")["金額"].sum()
        st.subheader(f"{selected_month}のカテゴリ別支出")
        st.pyplot(category_sum.plot.pie(
             labels=category_sum.index,      # ←カテゴリ名をラベルにする
             autopct="%.1f%%",
             ylabel=""
        ).figure)
    else:
        st.info("この月のデータはありません。")


