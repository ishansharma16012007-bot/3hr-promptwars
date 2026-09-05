from typing import List, Optional
from pydantic import BaseModel, Field

SYSTEM_PROMPT = """
You are Antigravity, an AI mentor for final-year engineering/CS students building
capstone projects. Your job is to convert a student's skills, interests, time
budget, and constraints into 3 tailored, buildable project ideas — never vague,
always scoped to be finishable solo or in a 2-4 person team within the given
timeframe.

INPUTS you will receive from the student:
- Known skills/languages (e.g., Python, React, SQL)
- Interest domains (e.g., healthcare, fintech, gaming, sustainability)
- Available time (weeks) and team size
- Target Profile: Beginner / Intern / Final-Year Student
- Hardware/budget constraints (GPU access? cloud credits? none?)
- Preferred difficulty (beginner / intermediate / advanced)

FOR EACH IDEA YOU GENERATE, OUTPUT JSON matching the schema below:
1. Title (short, specific)
2. One-line pitch
3. Problem it solves + who benefits
4. Core features (3-5, MVP-first)
5. Tech stack (justify each choice briefly)
6. Data sources & Data Platform Source (e.g. Kaggle, GitHub API, OpenFDA, WHO)
7. Development milestones: Week-by-week MVP -> enhancement path
8. Risk/difficulty flags
9. Ethical & privacy flags if applicable
10. A stretch feature for bonus marks
11. ai_recommendation_reason: Specific explanation of why AI recommends this project for the student's profile.
12. is_top_recommendation: Boolean flag (set true for the single best match among the 3 ideas).

CONSTRAINTS:
- Adjust complexity strictly based on Target Profile.
- Never suggest an idea requiring proprietary data the student can't access.
- Prioritize feasibility within stated time budget over ambition.

TONE: Direct, practical, encouraging — like a senior engineer mentoring a junior.
"""

ELABORATION_PROMPT_TEMPLATE = """
I've chosen this project idea: {title} — {pitch}.

Context:
- Team size: {team_size}, skills: {skills}
- Time remaining: {available_time_weeks} weeks
- Target Profile: {target_profile}
- Hardware/Constraints: {hardware_constraints}
- Target domain: {domain}

Please give me:
1. A minimal file/folder structure for this project.
2. The exact MVP feature cut (what to build first).
3. The exact features to explicitly skip given this specific domain and target profile.
4. Step-by-step build order in sequence referencing the chosen programming language.
5. The 3 most likely technical blockers for this specific stack, with a one-line fix for each.
6. A 60-second demo script highlighting the AI/ML component clearly for judges.
7. One "wow factor" addition I could add in the last 20 minutes if time permits.

Keep it concrete and code-oriented where relevant.
"""

class StudentInput(BaseModel):
    skills: List[str] = Field(default_factory=list)
    domains: List[str] = Field(default_factory=list)
    available_time_weeks: int = 8
    team_size: int = 2
    target_profile: str = "Final-Year Student"
    hardware_constraints: str = "None / Low Spec"
    difficulty: str = "Intermediate"

class TechStackItem(BaseModel):
    tool: str
    justification: str

class ProjectIdea(BaseModel):
    id: str
    title: str
    pitch: str
    problem_and_beneficiaries: str
    core_features: List[str]
    tech_stack: List[TechStackItem]
    data_sources: str
    data_platform_source: str = "Kaggle Open Datasets"
    milestones: List[str]
    risk_flags: List[str]
    ethical_flags: Optional[str] = None
    stretch_feature: str
    domain: str
    target_profile: str = "Final-Year Student"
    ai_recommendation_reason: Optional[str] = "Best overall feasibility and skill alignment."
    is_top_recommendation: bool = False

class GenerationResponse(BaseModel):
    student_profile_summary: str
    ideas: List[ProjectIdea]

class ElaborationInput(BaseModel):
    title: str
    pitch: str
    skills: List[str] = Field(default_factory=list)
    available_time_weeks: int = 8
    team_size: int = 2
    target_profile: str = "Final-Year Student"
    hardware_constraints: str = "None"
    domain: str = "General"
    core_features: Optional[List[str]] = None
    tech_stack: Optional[List[TechStackItem]] = None

class ElaborationResponse(BaseModel):
    idea_title: str
    folder_structure: str
    mvp_feature_cut: List[str]
    features_to_skip: List[str]
    step_by_step_build_order: List[str]
    top_3_blockers: List[dict]
    demo_script_60s: str
    wow_factor_20min: str
