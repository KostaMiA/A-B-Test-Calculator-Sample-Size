import numpy as np
from scipy import stats

def calculate_conversion_test(
    count_a: int, 
    n_a: int, 
    count_b: int, 
    n_b: int, 
    alpha: float = 0.05
) -> dict[str, any]:
    """
    Расчет Z-теста для двух пропорций (конверсий).
    """
    p_a = count_a / n_a
    p_b = count_b / n_b
    
    # Объединенная пропорция для Z-статистики
    p_pooled = (count_a + count_b) / (n_a + n_b)
    se_pooled = np.sqrt(p_pooled * (1 - p_pooled) * (1/n_a + 1/n_b))
    
    z_stat = (p_b - p_a) / se_pooled
    p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))
    
    # Доверительный интервал для разницы p_b - p_a
    se_diff = np.sqrt((p_a * (1 - p_a) / n_a) + (p_b * (1 - p_b) / n_b))
    z_crit = stats.norm.ppf(1 - alpha / 2)
    diff = p_b - p_a
    ci_lower = diff - z_crit * se_diff
    ci_upper = diff + z_crit * se_diff
    
    relative_lift = ((p_b - p_a) / p_a) * 100 if p_a > 0 else 0
    
    return {
        "cr_a": p_a,
        "cr_b": p_b,
        "relative_lift": relative_lift,
        "p_value": p_value,
        "is_significant": p_value < alpha,
        "ci_lower": ci_lower,
        "ci_upper": ci_upper
    }