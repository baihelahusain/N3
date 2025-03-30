def generate_insight_recommendation(skill, salary):
    """
    Generate an insight recommendation for a given skill and salary.
    This is a fallback when Gemini API is not available.
    
    Args:
        skill (str): The name of the skill
        salary (float): The average salary for the skill
        
    Returns:
        str: An insight recommendation
    """
    # Fallback recommendation when Gemini API is not available
    return (
        f"Based on current trends, '{skill}' appears to be in high demand with a competitive "
        f"salary of ${salary:,.0f} per year. Professionals with this skill typically work in "
        f"positions that require specialized technical knowledge and problem-solving abilities. "
        f"Investing in this skill could enhance your career prospects and market value. "
        f"Consider combining it with complementary skills to maximize your earning potential."
    ) 