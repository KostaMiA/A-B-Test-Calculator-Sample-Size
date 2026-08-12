import streamlit as st
from stats import calculate_conversion_test
from plots import plot_conversion_distributions, plot_difference_distribution
import config

st.set_page_config(page_title=config.APP_TITLE, layout="wide")
st.title(config.APP_TITLE)

# Боковое меню
st.sidebar.header("Параметры эксперимента")
alpha = st.sidebar.slider("Alpha (Уровень значимости)", 0.01, 0.10, config.DEFAULT_ALPHA, 0.01, help=config.HELP_ALPHA)

# Входные данные
col_a, col_b = st.columns(2)

with col_a:
    st.subheader("Группа A (Control)")
    n_a = st.number_input("Выборка A (N)", min_value=1, value=1000, key="n_a")
    conv_a = st.number_input("Конверсии A (K)", min_value=0, max_value=n_a, value=100, key="conv_a")

with col_b:
    st.subheader("Группа B (Treatment)")
    n_b = st.number_input("Выборка B (N)", min_value=1, value=1000, key="n_b")
    conv_b = st.number_input("Конверсии B (K)", min_value=0, max_value=n_b, value=130, key="conv_b")

# Расчет статистики
results = calculate_conversion_test(conv_a, n_a, conv_b, n_b, alpha)

st.divider()

# Основные метрики (KPI)
m1, m2, m3, m4 = st.columns(4)
m1.metric("CR Группы A", f"{results['cr_a']:.2%}")
m2.metric("CR Группы B", f"{results['cr_b']:.2%}")
m3.metric("Относительный прирост", f"{results['relative_lift']:.2f}%")
m4.metric("P-value", f"{results['p_value']:.4f}")

# Вывод статуса
if results['is_significant']:
    st.success(f"Различие статистически значимо на уровне α = {alpha}!")
else:
    st.warning("Различие статистически НЕ значимо. Недостаточно данных для отклонения нулевой гипотезы.")

st.divider()

# Визуализация результатов
st.header("Визуализация распределений")
tab1, tab2 = st.tabs(["Сравнение групп A и B", "Распределение разницы и ДИ"])

with tab1:
    fig_comp = plot_conversion_distributions(conv_a, n_a, conv_b, n_b, alpha)
    st.plotly_chart(fig_comp, use_container_width=True)

with tab2:
    fig_diff = plot_difference_distribution(conv_a, n_a, conv_b, n_b, alpha)
    st.plotly_chart(fig_diff, use_container_width=True)