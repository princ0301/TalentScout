import json
import os
from datetime import datetime
from typing import Dict, List, Any

def save_candidate_data(candidate_data: Dict[str, Any], filename: str = None) -> str:
    """Save candidate data to JSON file"""
    if not os.path.exists("data"):
        os.makedirs("data")
    
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"data/candidate_{timestamp}.json"
    
    with open(filename, 'w') as f:
        json.dump(candidate_data, f, indent=2)
    
    return filename

def get_tech_stack_categories() -> Dict[str, List[str]]:
    """Get predefined tech stack categories for validation"""
    return {
        "Programming Languages": [
            "Python", "JavaScript", "Java", "C++", "C#", "Go", "Rust", "PHP", 
            "Ruby", "Swift", "Kotlin", "TypeScript", "Scala", "R"
        ],
        "Frontend": [
            "React", "Vue.js", "Angular", "Svelte", "Next.js", "HTML", "CSS", "Bootstrap"
        ],
        "Backend": [
            "Django", "Flask", "FastAPI", "Express.js", "Spring Boot", "Laravel"
        ],
        "Databases": [
            "MySQL", "PostgreSQL", "MongoDB", "Redis", "SQLite", "Oracle"
        ],
        "Cloud": [
            "AWS", "Google Cloud", "Azure", "Docker", "Kubernetes"
        ],
        "Tools": [
            "Git", "Jenkins", "Terraform", "Linux", "Nginx"
        ]
    }

def validate_tech_stack(tech_stack: List[str]) -> Dict[str, Any]:
    """Validate and categorize tech stack"""
    categories = get_tech_stack_categories()
    all_techs = []
    for category_techs in categories.values():
        all_techs.extend([tech.lower() for tech in category_techs])
    
    validated = []
    unknown = []
    categorized = {category: [] for category in categories.keys()}
    
    for tech in tech_stack:
        tech_clean = tech.strip()
        tech_lower = tech_clean.lower()
        
        found = False
        for category, category_techs in categories.items():
            for known_tech in category_techs:
                if tech_lower == known_tech.lower():
                    validated.append(known_tech)
                    categorized[category].append(known_tech)
                    found = True
                    break
            if found:
                break
        
        if not found:
            unknown.append(tech_clean)
    
    return {
        "validated": validated,
        "unknown": unknown,
        "categorized": {k: v for k, v in categorized.items() if v},
        "total_count": len(validated) + len(unknown)
    }

def generate_candidate_report(candidate_data: Dict[str, Any]) -> str:
    """Generate a formatted candidate report"""
    report = []
    report.append("=" * 50)
    report.append("CANDIDATE SCREENING REPORT")
    report.append("=" * 50)
    report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("")
    
    report.append("BASIC INFORMATION:")
    report.append("-" * 20)
    for field in ["full_name", "email", "phone", "experience_years", "desired_position", "location"]:
        if field in candidate_data:
            label = field.replace("_", " ").title()
            value = candidate_data[field]
            if field == "experience_years":
                value = f"{value} years"
            report.append(f"{label}: {value}")
    
    report.append("")
    
    if "tech_stack" in candidate_data:
        report.append("TECHNICAL SKILLS:")
        report.append("-" * 20)
        tech_validation = validate_tech_stack(candidate_data['tech_stack'])
        
        if tech_validation['categorized']:
            for category, techs in tech_validation['categorized'].items():
                report.append(f"{category}: {', '.join(techs)}")
        
        if tech_validation['unknown']:
            report.append(f"Other Technologies: {', '.join(tech_validation['unknown'])}")
        
        report.append(f"Total Technologies: {tech_validation['total_count']}")
    
    report.append("")
    
    if "technical_responses" in candidate_data:
        report.append("TECHNICAL RESPONSES:")
        report.append("-" * 20)
        for i, response in enumerate(candidate_data['technical_responses'], 1):
            report.append(f"Response {i}: {response['response'][:100]}...")
            report.append("")
    
    report.append("=" * 50)
    return "\n".join(report)