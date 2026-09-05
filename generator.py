import os
import json
import uuid
import random
from typing import List, Dict, Any
from system_prompts import (
    SYSTEM_PROMPT,
    ELABORATION_PROMPT_TEMPLATE,
    StudentInput,
    GenerationResponse,
    ProjectIdea,
    TechStackItem,
    ElaborationInput,
    ElaborationResponse
)
from candidate_db import CANDIDATE_IDEAS

def generate_ideas(student: StudentInput) -> GenerationResponse:
    """
    Generates 3 tailored project ideas using Gemini API if key exists,
    or smart fallback matrix engine if key is absent.
    """
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    
    if api_key:
        try:
            from google import genai
            from google.genai import types
            
            client = genai.Client(api_key=api_key)
            prompt = f"""
            Student Profile:
            - Known Skills/Languages: {', '.join(student.skills) if student.skills else 'Python, SQL, HTML'}
            - Preferred Interest Domains: {', '.join(student.domains) if student.domains else 'General CS / AI'}
            - Available Time: {student.available_time_weeks} weeks
            - Team Size: {student.team_size} person(s)
            - Target Profile: {student.target_profile}
            - Hardware/Budget Constraints: {student.hardware_constraints}
            - Preferred Difficulty: {student.difficulty}

            IMPORTANT:
            1. Scope complexity strictly according to Target Profile ({student.target_profile}).
            2. ALL 3 generated ideas MUST belong to the user's selected interest domains: {', '.join(student.domains)}.
            3. Explicitly select ONE idea as the Top AI Recommendation (is_top_recommendation=true) and provide a compelling ai_recommendation_reason.

            Return a JSON object with key "ideas" containing an array of 3 objects matching the schema:
            title, pitch, problem_and_beneficiaries, core_features (list), tech_stack (list of tool/justification), data_sources, data_platform_source, milestones (list), risk_flags (list), ethical_flags, stretch_feature, domain, target_profile, ai_recommendation_reason, is_top_recommendation.
            """
            
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    response_mime_type="application/json",
                    temperature=0.7
                )
            )
            
            data = json.loads(response.text)
            raw_ideas = data.get("ideas", [])
            
            ideas_list = []
            for i, raw in enumerate(raw_ideas[:3]):
                idea_id = f"gen-{uuid.uuid4().hex[:6]}"
                tech_items = [
                    TechStackItem(tool=t.get("tool", "Python"), justification=t.get("justification", "Standard choice"))
                    if isinstance(t, dict) else TechStackItem(tool=str(t), justification="Chosen for feasibility")
                    for t in raw.get("tech_stack", [])
                ]
                
                ideas_list.append(ProjectIdea(
                    id=idea_id,
                    title=raw.get("title", f"Tailored Project #{i+1}"),
                    pitch=raw.get("pitch", "A practical capstone project."),
                    problem_and_beneficiaries=raw.get("problem_and_beneficiaries", "Solves key domain problem for target users."),
                    core_features=raw.get("core_features", ["Feature 1", "Feature 2", "Feature 3"]),
                    tech_stack=tech_items,
                    data_sources=raw.get("data_sources", "Publicly available Kaggle/Open datasets."),
                    data_platform_source=raw.get("data_platform_source", "Kaggle Open Datasets"),
                    milestones=raw.get("milestones", ["Week 1: Setup", "Week 2: Core MVP", "Week 3: Polish"]),
                    risk_flags=raw.get("risk_flags", ["Scope creep risk"]),
                    ethical_flags=raw.get("ethical_flags", "Ensure user privacy and clear disclaimers."),
                    stretch_feature=raw.get("stretch_feature", "Add analytics dashboard"),
                    domain=raw.get("domain", student.domains[0] if student.domains else "Software Engineering"),
                    target_profile=student.target_profile,
                    ai_recommendation_reason=raw.get("ai_recommendation_reason", "Highest technical impact to timeline ratio."),
                    is_top_recommendation=raw.get("is_top_recommendation", i == 0)
                ))
            
            summary = f"Generated 3 tailored projects for a {student.target_profile} ({student.team_size} person team, {student.available_time_weeks} weeks) focusing on {', '.join(student.domains)}."
            return GenerationResponse(student_profile_summary=summary, ideas=ideas_list)
            
        except Exception as e:
            print(f"Gemini API Call failed or key invalid: {e}. Falling back to Smart Matrix Engine.")

    # SMART FALLBACK MATRIX ENGINE
    return _generate_smart_fallback(student)

def _generate_smart_fallback(student: StudentInput) -> GenerationResponse:
    """
    Generates 3 tailored project ideas strictly aligned with selected domains, target profile, and programming skills.
    """
    selected_domains = student.domains if student.domains else ["Software Engineering"]
    skills = student.skills if student.skills else ["Python", "SQL", "React"]
    primary_lang = skills[0] if skills else "Python"
    time_w = student.available_time_weeks
    team_s = student.team_size
    profile = student.target_profile
    
    # Domain Knowledge templates dictionary with explicit platform sources
    domain_templates = {
        "Software Engineering": [
            {
                "title": f"DevFlow: Automated CI/CD & Code Smell Reviewer",
                "pitch": f"A micro-service pipeline written in {primary_lang} that analyzes Git commits and flags code anti-patterns.",
                "problem": "Student developers lack automated pull-request feedback; computer science students benefit from instant static linting.",
                "platform": "GitHub REST API & PyLint Engine",
                "core": ["GitHub repository diff parser", "Static AST code smell analyzer", "Severity score dashboard", "Automated inline code suggestion generator"],
                "data": "Public GitHub open-source repositories & PyLint/ESLint JSON rule sets.",
                "ethical": "Ensure private user repositories are never cached or logged without explicit consent.",
                "stretch": "One-click 'Create GitHub Pull Request' comment integration.",
                "rec_reason": f"🌟 AI Top Recommendation (98% Match): Perfectly matches your {primary_lang} skills for a {profile} seeking a high-velocity GitHub portfolio project in {time_w} weeks."
            },
            {
                "title": f"API-Pulse: Microservices Health & Dependency Visualizer",
                "pitch": f"A visual architecture tracker in {primary_lang} that maps REST endpoint dependencies and monitors latency in real-time.",
                "problem": "Debugging multi-service web apps is difficult for juniors; software teams benefit from visual dependency graphs.",
                "platform": "OpenAPI / Swagger Spec Parser",
                "core": ["OpenAPI / Swagger spec parser", "Real-time HTTP health check worker", "Interactive network dependency graph", "Latency threshold alert system"],
                "data": "Synthetic HTTP traffic logs and standard OpenAPI JSON schemas.",
                "ethical": "Obfuscate sensitive API keys or auth headers before logging metrics.",
                "stretch": "Automated alert notifications via Webhooks/Discord.",
                "rec_reason": "High backend architecture score with clean modular microservice design."
            },
            {
                "title": f"BugRadar: Intelligent Issue Categorizer & Duplicate Detector",
                "pitch": f"An issue triage assistant using {primary_lang} semantic text matching to group duplicate bug reports.",
                "problem": "Open-source projects get flooded with duplicate bug reports; maintainers save hours of manual triage time.",
                "platform": "Jira & GitHub Open Issue Datasets",
                "core": ["Issue ticket text parsing", "TF-IDF / Embedding similarity matching", "Duplicate score ranking", "Developer tag suggestion board"],
                "data": "Public GitHub/Jira open issue tracker datasets.",
                "ethical": "Avoid storing user emails or personal user data from issue trackers.",
                "stretch": "Auto-generation of bug reproduction steps.",
                "rec_reason": "Great machine learning + software engineering hybrid candidate."
            }
        ],
        "Data Science": [
            {
                "title": f"SkillGap AI: Student Placement & Career Readiness Analyzer",
                "pitch": f"An analytical pipeline in {primary_lang} predicting student job readiness and recommending skill closing roadmaps.",
                "problem": "Students miss placement opportunities without knowing missing technical gaps; career counselors gain objective metrics.",
                "platform": "Kaggle Open Campus Placement Dataset",
                "core": ["Academic & skill vector feature engineering", "XGBoost placement probability model", "Target job role skill gap radar chart", "Personalized 4-week learning roadmap"],
                "data": "Anonymized Kaggle Campus Placement datasets & industry skill benchmarks.",
                "ethical": "Explicitly drop protected demographic attributes (gender, origin) to prevent model bias.",
                "stretch": "Drag-and-drop PDF resume skill extraction parser.",
                "rec_reason": f"🌟 AI Top Recommendation (96% Match): High statistical rigor using Kaggle benchmarks perfectly scoped for {profile}."
            }
        ],
        "NLP": [
            {
                "title": f"Antigravity: Intelligent Capstone Project Mentor",
                "pitch": f"An NLP mentoring tool built with {primary_lang} that extracts student skills and semantically matches project blueprints.",
                "problem": "Final-year students waste weeks choosing buildable projects; students get instant structured project briefs.",
                "platform": "Curated Open Capstone Knowledge Base",
                "core": ["Skill & Interest profile extraction", "Embedding similarity matching engine", "Structured 9-field project generator", "One-click PDF project brief exporter"],
                "data": "Curated capstone idea knowledge base across core CS domains.",
                "ethical": "Highlight privacy concerns explicitly when domain involves personal user data.",
                "stretch": "Conversational multi-turn chat for project scope refinement.",
                "rec_reason": f"🌟 AI Top Recommendation (99% Match): Direct match for NLP interest, fully finishable in {time_w} weeks."
            }
        ],
        "Computer Vision": [
            {
                "title": f"VisionTrack: Campus Attendance & Privacy-First Engagement Logger",
                "pitch": f"A computer vision face detection app in {primary_lang} logging attendance and attention metrics without saving facial templates.",
                "problem": "Manual attendance wastes 10 minutes of lecture time; faculty receive instant logs without violating student privacy.",
                "platform": "MediaPipe Vision & DAiSEE Dataset",
                "core": ["Webcam face detection (MediaPipe CPU engine)", "Head pose orientation & attention score heuristic", "Automated attendance log exporter (CSV)", "Classroom engagement timeline graph"],
                "data": "Live webcam stream or DAiSEE classroom video dataset.",
                "ethical": "Processing occurs strictly in RAM without storing raw facial embeddings or identity databases.",
                "stretch": "Edge deployment support on Raspberry Pi / Jetson Nano.",
                "rec_reason": f"🌟 AI Top Recommendation (95% Match): High visual impact demo with zero GPU dependencies required."
            }
        ],
        "Healthcare + ML": [
            {
                "title": f"ArogyaAssist: Rural Symptom Checker & Triage Guidance Bot",
                "pitch": f"An offline-first symptom checker in {primary_lang} classifying triage urgency for rural clinics with medical disclaimers.",
                "problem": "Rural healthcare centers lack triage doctors; health workers receive rapid guidance on patient urgency.",
                "platform": "WHO Guidelines & Kaggle Disease Dataset",
                "core": ["Interactive symptom intake chat flow", "Probabilistic disease shortlist classifier", "Urgency triage badge", "Nearest rural clinic static map"],
                "data": "Kaggle Disease Symptom Prediction dataset.",
                "ethical": "MUST include prominent medical disclaimers: 'Educational & Triage Tool Only — Not a Licensed Diagnosis'.",
                "stretch": "Offline voice input & regional language translation.",
                "rec_reason": f"🌟 AI Top Recommendation (97% Match): Outstanding social impact narrative for capstone evaluation panels."
            }
        ],
        "Fintech": [
            {
                "title": f"SpendGuard: Personal Finance Anomaly Detector",
                "pitch": f"A finance tracker written in {primary_lang} that detects unusual spending spikes using Isolation Forests and gives AI budget tips.",
                "problem": "Young adults suffer budget leaks from forgotten subscriptions; users get instant spending anomaly alerts.",
                "platform": "Kaggle Synthetic Transaction Dataset",
                "core": ["Bank statement CSV transaction parser", "Isolation Forest spending anomaly detector", "Expense category breakdown charts", "AI-generated budget optimization tips"],
                "data": "Anonymized bank statement CSV datasets.",
                "ethical": "Process all CSV data locally in memory without uploading user financial statements.",
                "stretch": "Interactive 12-month savings projection slider.",
                "rec_reason": f"🌟 AI Top Recommendation (94% Match): Fast to build with isolation forest algorithms."
            }
        ],
        "Sustainability / IoT": [
            {
                "title": f"EcoSort: Edge Waste Sorting & Recycling Guidance System",
                "pitch": f"A camera waste classifier in {primary_lang} guiding recyclable vs organic disposal with gamified eco-score tracking.",
                "problem": "Improper waste disposal contaminates recycling streams; university campuses improve recycling accuracy.",
                "platform": "Kaggle TrashNet Dataset (2,500+ Images)",
                "core": ["Real-time camera waste classification (MobileNet)", "Bin color recommendation output", "Eco-Score points tracker", "Campus sustainability dashboard"],
                "data": "Kaggle TrashNet dataset (2,500+ labeled images).",
                "ethical": "Process camera frames locally without saving background images.",
                "stretch": "CO2 offset savings estimator per item recycled.",
                "rec_reason": f"🌟 AI Top Recommendation (96% Match): Excellent sustainability story with high accuracy TrashNet dataset."
            }
        ],
        "Cyber Security": [
            {
                "title": f"PhishShield: Real-Time Email Phishing & URL Scanner",
                "pitch": f"A security scanner written in {primary_lang} evaluating email headers, link redirects, and WHOIS domain age.",
                "problem": "Employees and students fall victim to credential harvesting; security teams receive instant risk scores.",
                "platform": "PhishTank API & WHOIS Database",
                "core": ["Email header & SPF/DKIM verification parser", "URL redirect expander & WHOIS domain age checker", "Machine learning phishing risk classifier", "Security audit report exporter"],
                "data": "PhishTank open API & Kaggle Malicious URLs dataset.",
                "ethical": "Obfuscate user email credentials before scanning email headers.",
                "stretch": "Browser extension popup flagging malicious links on hover.",
                "rec_reason": f"🌟 AI Top Recommendation (95% Match): High security value and easy to demonstrate to judges."
            }
        ]
    }
    
    # Collect matching candidate pools
    pool = []
    for domain_name in selected_domains:
        matched_key = None
        for key in domain_templates.keys():
            if domain_name.lower() in key.lower() or key.lower() in domain_name.lower():
                matched_key = key
                break
        if matched_key:
            for item in domain_templates[matched_key]:
                item_copy = dict(item)
                item_copy["target_domain"] = matched_key
                pool.append(item_copy)
                
    if len(pool) < 3:
        for key, items in domain_templates.items():
            for item in items:
                item_copy = dict(item)
                item_copy["target_domain"] = key
                if item_copy not in pool:
                    pool.append(item_copy)

    chosen_items = pool[:3]
    generated_ideas = []
    weeks_step = max(1, time_w // 4)
    
    for idx, item in enumerate(chosen_items):
        idea_id = f"idea-{uuid.uuid4().hex[:6]}"
        is_top = (idx == 0)
        
        # Tailor core features based on profile
        core_feats = list(item["core"])
        if profile == "Beginner Student":
            core_feats = core_feats[:3]
        elif profile == "Final-Year Student":
            if len(core_feats) < 4:
                core_feats.append("Automated test suite & PDF performance report exporter")

        # Tech stack incorporating student's skills
        tech_list = []
        for s in skills[:2]:
            tech_list.append(TechStackItem(tool=s, justification=f"Primary tool requested for {profile} profile"))
            
        default_tools = [("FastAPI", "API backend"), ("SQLite", "Relational database"), ("Tailwind CSS", "UI framework")]
        for t_name, t_just in default_tools:
            if len(tech_list) < 5 and t_name not in [t.tool for t in tech_list]:
                tech_list.append(TechStackItem(tool=t_name, justification=t_just))

        # Milestones referencing actual programming language
        milestones = [
            f"Weeks 1-{weeks_step}: Set up environment in {primary_lang} & connect {item['platform']}",
            f"Weeks {weeks_step+1}-{weeks_step*2}: Build MVP core feature: {core_feats[0]}",
            f"Weeks {weeks_step*2+1}-{weeks_step*3}: Build user interface & connect {primary_lang} backend REST endpoints",
            f"Weeks {weeks_step*3+1}-{time_w}: Verification, edge-case testing & 60s demo script preparation"
        ]
        
        risk_flags = [
            f"Scope creep on advanced features (mitigate by freezing MVP at Week {weeks_step*2})"
        ]
        if "none" in student.hardware_constraints.lower():
            risk_flags.append("Hardware constraints: CPU-friendly lightweight models prioritized over heavy GPUs.")

        generated_ideas.append(ProjectIdea(
            id=idea_id,
            title=item["title"],
            pitch=item["pitch"],
            problem_and_beneficiaries=item["problem"],
            core_features=core_feats,
            tech_stack=tech_list,
            data_sources=item["data"],
            data_platform_source=item["platform"],
            milestones=milestones,
            risk_flags=risk_flags,
            ethical_flags=item["ethical"],
            stretch_feature=item["stretch"],
            domain=item["target_domain"],
            target_profile=profile,
            ai_recommendation_reason=item.get("rec_reason", f"Optimal feasibility-to-impact match for {primary_lang}."),
            is_top_recommendation=is_top
        ))
        
    summary = f"Generated 3 tailored projects for a {profile} ({team_s}-person team, {time_w}-week timeline) using {primary_lang} in {', '.join(selected_domains)}."
    return GenerationResponse(student_profile_summary=summary, ideas=generated_ideas)

def elaborate_idea(data: ElaborationInput) -> ElaborationResponse:
    """
    Generates Section 4 Elaboration details with DOMAIN-SPECIFIC features to skip and build order.
    """
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    
    for cand in CANDIDATE_IDEAS:
        if cand["title"].lower() in data.title.lower() or data.title.lower() in cand["title"].lower():
            elab = cand["elaboration"]
            return ElaborationResponse(
                idea_title=data.title,
                folder_structure=elab["folder_structure"],
                mvp_feature_cut=elab["mvp_feature_cut"],
                features_to_skip=elab["features_to_skip"],
                step_by_step_build_order=elab["step_by_step_build_order"],
                top_3_blockers=elab["top_3_blockers"],
                demo_script_60s=elab["demo_script_60s"],
                wow_factor_20min=elab["wow_factor_20min"]
            )
            
    if api_key:
        try:
            from google import genai
            from google.genai import types
            
            client = genai.Client(api_key=api_key)
            prompt = ELABORATION_PROMPT_TEMPLATE.format(
                title=data.title,
                pitch=data.pitch,
                team_size=data.team_size,
                skills=", ".join(data.skills) if data.skills else "Python, Web Dev",
                available_time_weeks=data.available_time_weeks,
                target_profile=data.target_profile,
                hardware_constraints=data.hardware_constraints,
                domain=data.domain
            )
            
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction="You are a senior engineering mentor. Respond in JSON with keys: folder_structure, mvp_feature_cut (list), features_to_skip (list), step_by_step_build_order (list), top_3_blockers (list of objects with blocker and fix), demo_script_60s, wow_factor_20min.",
                    response_mime_type="application/json"
                )
            )
            res = json.loads(response.text)
            return ElaborationResponse(
                idea_title=data.title,
                folder_structure=res.get("folder_structure", "project/\n├── app.py\n└── static/"),
                mvp_feature_cut=res.get("mvp_feature_cut", ["Basic input form", "Core data processing", "Output display"]),
                features_to_skip=res.get("features_to_skip", ["OAuth user login", "Complex DB schema", "Multi-tenant auth"]),
                step_by_step_build_order=res.get("step_by_step_build_order", ["1. Backend API", "2. Core Logic", "3. Frontend UI"]),
                top_3_blockers=res.get("top_3_blockers", [{"blocker": "API limits", "fix": "Cache requests"}]),
                demo_script_60s=res.get("demo_script_60s", "Show input, run pipeline, demonstrate results in under 60 seconds."),
                wow_factor_20min=res.get("wow_factor_20min", "Add one-click PDF brief export.")
            )
        except Exception as e:
            print(f"Elaboration LLM call failed: {e}")
            
    domain_lower = data.domain.lower()
    primary_lang = data.skills[0] if data.skills else "Python"
    clean_name = data.title.lower().replace(' ', '-').replace(':', '')
    
    domain_skip_rules = {
        "software engineering": [
            "Skip GitHub OAuth multi-user organization login",
            "Skip real-time background cron job webhooks",
            "Skip multi-region database clustering & Redis caching"
        ],
        "data science": [
            "Skip real-time web scraping during live inference",
            "Skip complex deep neural network embeddings for tabular data",
            "Skip automated recruiter email notification pipelines"
        ],
        "nlp": [
            "Skip fine-tuning 70B parameter LLMs locally",
            "Skip real-time multi-user chat socket servers",
            "Skip video/audio speech-to-text generation"
        ],
        "computer vision": [
            "Skip multi-camera RTSP network streaming servers",
            "Skip 3D facial recognition identification databases",
            "Skip facial emotion sentiment analysis"
        ],
        "healthcare + ml": [
            "Skip Electronic Health Record (EHR) hospital integration",
            "Skip automated prescription writing engines",
            "Skip live video consultation calls with doctors"
        ],
        "fintech": [
            "Skip live Plaid bank account API credentials",
            "Skip multi-currency real-time exchange rate converters",
            "Skip stock investment portfolio tracking"
        ],
        "sustainability / iot": [
            "Skip robotic arm servo-motor hardware integration",
            "Skip multi-object bounding box detection",
            "Skip barcode scanning cameras"
        ],
        "cyber security": [
            "Skip enterprise Active Directory LDAP integration",
            "Skip automated firewall IP blocking scripts",
            "Skip multi-node SIEM log ingestion"
        ]
    }
    
    skips = domain_skip_rules.get(domain_lower, [
        "Skip OAuth user registration & login databases",
        "Skip third-party payment gateway integration",
        "Skip multi-region cloud server clustering"
    ])
    
    return ElaborationResponse(
        idea_title=data.title,
        folder_structure=f"""{clean_name}/
├── backend/
│   ├── app.py           # FastAPI server ({primary_lang})
│   ├── services.py      # Core processing logic for {data.domain}
│   └── requirements.txt
├── frontend/
│   ├── index.html       # 3D dark-emerald web application UI
│   └── app.js           # Client application logic
└── README.md""",
        mvp_feature_cut=[
            f"Core input form tailored for {data.domain}",
            f"Primary feature logic written in {primary_lang}",
            f"Clean output dashboard with status badges"
        ],
        features_to_skip=skips,
        step_by_step_build_order=[
            f"1. Initialize project directory & install {primary_lang} dependencies",
            f"2. Build FastAPI REST endpoint `/api/process` taking student inputs",
            f"3. Implement domain processing logic in `services.py` with synthetic data fallback",
            f"4. Connect frontend web UI form to {primary_lang} backend REST API",
            f"5. Verify edge-case error handling and test 60-second judge demo script"
        ],
        top_3_blockers=[
            {
                "blocker": "API Rate Limits or Network Disconnection during live judge demo",
                "fix": "Implement local caching and synthetic fallback data response."
            },
            {
                "blocker": "CORS (Cross-Origin Resource Sharing) header errors",
                "fix": "Add FastAPI `CORSMiddleware` with `allow_origins=['*']`."
            },
            {
                "blocker": "Scope creep delaying MVP completion",
                "fix": "Freeze MVP feature set after completing core data pipeline."
            }
        ],
        demo_script_60s=f"Demonstrate {data.title} by entering sample inputs, triggering the {primary_lang} processing pipeline, and showing judges the instant results in under 60 seconds.",
        wow_factor_20min="Add an interactive PDF project brief export button for instant proposal submission!"
    )
