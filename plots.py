import numpy as np
import plotly.graph_objects as go
from scipy import stats

def plot_conversion_distributions(
    count_a: int, 
    n_a: int, 
    count_b: int, 
    n_b: int, 
    alpha: float = 0.05
) -> go.Figure:
    """
    Строит сравнительный график распределений конверсий для двух групп (A и B).
    """
    p_a = count_a / n_a
    p_b = count_b / n_b
    
    se_a = np.sqrt(p_a * (1 - p_a) / n_a)
    se_b = np.sqrt(p_b * (1 - p_b) / n_b)
    
    # Определение диапазона значений x для графика
    min_x = min(p_a - 4 * se_a, p_b - 4 * se_b)
    max_x = max(p_a + 4 * se_a, p_b + 4 * se_b)
    x = np.linspace(min_x, max_x, 500)
    
    y_a = stats.norm.pdf(x, p_a, se_a)
    y_b = stats.norm.pdf(x, p_b, se_b)
    
    fig = go.Figure()
    
    # График для Группы A (Control)
    fig.add_trace(go.Scatter(
        x=x, y=y_a, 
        mode='lines', 
        name=f'Группа A (Control): {p_a:.2%}',
        line=dict(color='#2B5C8F', width=2),
        fill='tozeroy',
        fillcolor='rgba(43, 92, 143, 0.15)'
    ))
    
    # График для Группы B (Treatment)
    fig.add_trace(go.Scatter(
        x=x, y=y_b, 
        mode='lines', 
        name=f'Группа B (Treatment): {p_b:.2%}',
        line=dict(color='#E05A47', width=2),
        fill='tozeroy',
        fillcolor='rgba(224, 90, 71, 0.15)'
    ))
    
    # Вертикальные пунктирные линии средних значений
    fig.add_vline(x=p_a, line_dash="dash", line_color="#2B5C8F", annotation_text="CR A")
    fig.add_vline(x=p_b, line_dash="dash", line_color="#E05A47", annotation_text="CR B")
    
    fig.update_layout(
        title="<b>Плотность распределения конверсий</b>",
        xaxis_title="Conversion Rate",
        yaxis_title="Плотность вероятности",
        xaxis_tickformat=".2%",
        hovermode="x unified",
        template="plotly_white",
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
    )
    
    return fig


def plot_difference_distribution(
    count_a: int, 
    n_a: int, 
    count_b: int, 
    n_b: int, 
    alpha: float = 0.05
) -> go.Figure:
    """
    Строит распределение разницы конверсий (B - A) с выделением доверительного интервала.
    """
    p_a = count_a / n_a
    p_b = count_b / n_b
    diff = p_b - p_a
    
    se_diff = np.sqrt((p_a * (1 - p_a) / n_a) + (p_b * (1 - p_b) / n_b))
    
    z_crit = stats.norm.ppf(1 - alpha / 2)
    ci_lower = diff - z_crit * se_diff
    ci_upper = diff + z_crit * se_diff
    
    x = np.linspace(diff - 4 * se_diff, diff + 4 * se_diff, 500)
    y = stats.norm.pdf(x, diff, se_diff)
    
    fig = go.Figure()
    
    # Линия распределения разницы
    fig.add_trace(go.Scatter(
        x=x, y=y,
        mode='lines',
        name='Разница (B - A)',
        line=dict(color='#27AE60', width=2)
    ))
    
    # Закрашивание области доверительного интервала
    x_ci = np.linspace(ci_lower, ci_upper, 200)
    y_ci = stats.norm.pdf(x_ci, diff, se_diff)
    
    fig.add_trace(go.Scatter(
        x=np.concatenate([[ci_lower], x_ci, [ci_upper]]),
        y=np.concatenate([[0], y_ci, [0]]),
        fill='toself',
        fillcolor='rgba(39, 174, 96, 0.25)',
        line=dict(color='rgba(255,255,255,0)'),
        name=f'{int((1 - alpha) * 100)}% Доверительный интервал'
    ))
    
    # Линия H0 (нулевая гипотеза - отсутствие разницы)
    fig.add_vline(x=0, line_color="#7F8C8D", line_width=1.5, line_dash="dot", annotation_text="H0 (Разница = 0)")
    
    # Линия точечной оценки разницы
    fig.add_vline(x=diff, line_color="#27AE60", line_width=2, line_dash="dash", annotation_text=f"Diff: {diff:+.2%}")
    
    fig.update_layout(
        title=f"<b>Распределение абсолютной разницы (B - A) и {int((1 - alpha) * 100)}% ДИ</b>",
        xaxis_title="Разница в конверсии (p_B - p_A)",
        yaxis_title="Плотность вероятности",
        xaxis_tickformat=".2%",
        hovermode="x unified",
        template="plotly_white",
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
    )
    
    return fig