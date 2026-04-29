import streamlit as st
import pandas as pd
import plotly.express as px

# 加载数据
@st.cache_data
def load_data():
    df = pd.read_csv('population-with-un-projections.csv')
    # 处理缺失值，将空字符串转换为NaN
    df = df.replace('', pd.NA)
    # 合并实际人口和预测人口为一个列
    df['Population'] = df['Population'].fillna(df['Population (Projected)'])
    return df

# 主应用
def main():
    st.title('全球人口数据与预测分析')
    
    # 加载数据
    df = load_data()
    
    # 侧边栏控件
    st.sidebar.title('控制面板')
    
    # 国家/地区选择
    entities = sorted(df['Entity'].unique())
    selected_entity = st.sidebar.selectbox('选择国家/地区', entities)
    
    # 时间范围选择
    min_year = int(df['Year'].min())
    max_year = int(df['Year'].max())
    year_range = st.sidebar.slider('选择年份范围', min_year, max_year, (min_year, max_year))
    
    # 过滤数据
    filtered_df = df[(df['Entity'] == selected_entity) & 
                    (df['Year'] >= year_range[0]) & 
                    (df['Year'] <= year_range[1])]
    
    # 主内容区
    st.header(f'{selected_entity} 人口数据')
    
    # 人口趋势图
    st.subheader('人口趋势')
    fig = px.line(filtered_df, x='Year', y='Population', 
                  title=f'{selected_entity} 人口变化趋势 ({year_range[0]}-{year_range[1]})')
    fig.update_layout(xaxis_title='年份', yaxis_title='人口数量')
    st.plotly_chart(fig)
    
    # 人口增长率
    st.subheader('人口增长率')
    filtered_df['Growth Rate'] = filtered_df['Population'].pct_change() * 100
    growth_fig = px.line(filtered_df, x='Year', y='Growth Rate', 
                         title=f'{selected_entity} 人口增长率 ({year_range[0]}-{year_range[1]})')
    growth_fig.update_layout(xaxis_title='年份', yaxis_title='增长率 (%)')
    st.plotly_chart(growth_fig)
    
    # 数据表格
    st.subheader('详细数据')
    st.dataframe(filtered_df[['Year', 'Population', 'Growth Rate']].round(2))
    
    # 统计信息
    st.subheader('统计信息')
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric('起始年份人口', f"{int(filtered_df['Population'].iloc[0]):,}")
    
    with col2:
        st.metric('结束年份人口', f"{int(filtered_df['Population'].iloc[-1]):,}")
    
    with col3:
        population_change = int(filtered_df['Population'].iloc[-1]) - int(filtered_df['Population'].iloc[0])
        st.metric('人口变化', f"{population_change:,}")
    
    # 全球比较
    st.subheader('全球人口比较')
    top_countries = df[df['Year'] == 2023].nlargest(10, 'Population')
    fig_top = px.bar(top_countries, x='Entity', y='Population', 
                     title='2023年人口最多的10个国家/地区')
    fig_top.update_layout(xaxis_title='国家/地区', yaxis_title='人口数量')
    st.plotly_chart(fig_top)

if __name__ == '__main__':
    main()