import pandas as pd
import numpy as np
from collections import Counter
import random

def load_jobs_data():
    """Load job data from session state or create synthetic data."""
    if 'jobs_data' in pd.DataFrame._metadata and pd.DataFrame._metadata['jobs_data'] is not None:
        return pd.DataFrame._metadata['jobs_data']
    
    # Create a dummy DataFrame with the columns needed for the app to work
    dummy_df = pd.DataFrame({
        'title': ['Data Scientist', 'Software Engineer', 'Data Engineer'] * 10,
        'description_tokens': [['python', 'sql', 'machine learning']] * 30,
        'salary': np.random.normal(100000, 20000, 30),
        'country': np.random.choice(['United States', 'Remote', 'Germany', 'India'], 30)
    })
    
    pd.DataFrame._metadata['jobs_data'] = dummy_df
    return dummy_df

def extract_skills_vs_pay(jobs_data):
    """Extract skills vs pay data from the jobs dataframe"""
    if jobs_data is None or jobs_data.empty:
        return pd.DataFrame()
    
    has_skills = 'description_tokens' in jobs_data.columns
    has_salary = any(col in jobs_data.columns for col in ['salary_yearly', 'salary'])
    
    if not has_skills or not has_salary:
        return pd.DataFrame()
    
    try:
        salary_col = 'salary_yearly' if 'salary_yearly' in jobs_data.columns else 'salary'
        valid_jobs = jobs_data.dropna(subset=[salary_col, 'description_tokens'])
        if valid_jobs.empty:
            return pd.DataFrame()
        
        all_skills = []
        for tokens in valid_jobs['description_tokens']:
            if isinstance(tokens, str):
                skills = tokens.strip("[]").replace("'", "").split(", ")
                all_skills.extend([s for s in skills if s])
        
        skill_counts = Counter(all_skills)
        top_skills = [skill for skill, count in skill_counts.most_common(200)]
        
        skills_data = []
        for skill in top_skills:
            skill_jobs = valid_jobs[valid_jobs['description_tokens'].apply(
                lambda x: isinstance(x, str) and skill in x
            )]
            if len(skill_jobs) >= 10:
                avg_salary = skill_jobs[salary_col].mean()
                median_salary = skill_jobs[salary_col].median()
                job_count = len(skill_jobs)
                category = "Unknown"
                if any(tech in skill.lower() for tech in ["python", "r", "java", "c++", "javascript"]):
                    category = "Programming"
                elif any(tech in skill.lower() for tech in ["sql", "database", "postgresql"]):
                    category = "Data"
                elif any(tech in skill.lower() for tech in ["aws", "azure", "gcp", "cloud"]):
                    category = "Cloud"
                elif any(tech in skill.lower() for tech in ["ml", "ai", "machine learning", "tensorflow", "pytorch"]):
                    category = "AI"
                elif any(tech in skill.lower() for tech in ["react", "angular", "vue", "html", "css"]):
                    category = "Web Development"
                elif any(tech in skill.lower() for tech in ["docker", "kubernetes", "devops", "ci/cd"]):
                    category = "DevOps"
                elif any(tech in skill.lower() for tech in ["excel", "word", "powerpoint", "office"]):
                    category = "Office"
                elif any(tech in skill.lower() for tech in ["tableau", "power bi", "looker", "visualization"]):
                    category = "Visualization"
                
                avg_overall_salary = valid_jobs[salary_col].mean()
                salary_premium_pct = ((avg_salary / avg_overall_salary) - 1) * 100
                
                skills_data.append({
                    "Skill": skill,
                    "Category": category,
                    "Average Salary": avg_salary,
                    "Median Salary": median_salary,
                    "Salary Premium (%)": salary_premium_pct,
                    "Job Count": job_count
                })
        
        return pd.DataFrame(skills_data)
    
    except Exception as e:
        print(f"Error extracting skills vs pay data: {str(e)}")
        return pd.DataFrame()

def create_synthetic_skills_vs_pay():
    """Create synthetic skills vs pay data for demonstration purposes"""
    skills = [
        "Python", "SQL", "Java", "JavaScript", "AWS", "Azure", "Machine Learning",
        "Docker", "Kubernetes", "Excel", "Tableau", "Power BI", "Go", "C++", "Scala",
        "R", "Hadoop", "Spark", "Kafka", "Airflow", "TensorFlow", "PyTorch", "React",
        "Angular", "Vue.js", "Node.js", "Git", "Linux", "NoSQL", "MongoDB"
    ]
    
    categories = {
        "Python": "Programming", "SQL": "Data", "Java": "Programming",
        "JavaScript": "Programming", "AWS": "Cloud", "Azure": "Cloud",
        "Machine Learning": "AI", "Docker": "DevOps", "Kubernetes": "DevOps",
        "Excel": "Office", "Tableau": "Visualization", "Power BI": "Visualization",
        "Go": "Programming", "C++": "Programming", "Scala": "Programming",
        "R": "Programming", "Hadoop": "Data", "Spark": "Data",
        "Kafka": "Data", "Airflow": "DevOps", "TensorFlow": "AI",
        "PyTorch": "AI", "React": "Web Development", "Angular": "Web Development",
        "Vue.js": "Web Development", "Node.js": "Programming",
        "Git": "DevOps", "Linux": "DevOps", "NoSQL": "Data", "MongoDB": "Data"
    }
    
    category_base_salary = {
        "Programming": 120000,
        "Data": 125000,
        "Cloud": 130000,
        "AI": 150000,
        "Web Development": 115000,
        "DevOps": 135000,
        "Office": 95000,
        "Visualization": 110000,
        "Unknown": 100000
    }
    
    np.random.seed(42)
    skills_data = []
    
    for skill in skills:
        category = categories.get(skill, "Unknown")
        base_salary = category_base_salary[category]
        avg_salary = base_salary + np.random.normal(0, 15000)
        median_salary = avg_salary + np.random.normal(0, 5000)
        job_count = np.random.randint(50, 1000)
        avg_overall_salary = 110000
        salary_premium_pct = ((avg_salary / avg_overall_salary) - 1) * 100
        
        skills_data.append({
            "Skill": skill,
            "Category": category,
            "Average Salary": avg_salary,
            "Median Salary": median_salary,
            "Salary Premium (%)": salary_premium_pct,
            "Job Count": job_count
        })
    
    return pd.DataFrame(skills_data) 