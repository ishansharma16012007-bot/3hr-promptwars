CANDIDATE_IDEAS = [
    {
        "id": "cand-se-1",
        "domain": "Software Engineering",
        "title": "DevMentor AI: Automated Code Reviewer for Student Repos",
        "pitch": "An AI code-review assistant that flags code smells, suggests refactors, and explains why for student-level codebases.",
        "problem_and_beneficiaries": "Student developers lack senior code reviewers to catch anti-patterns early; professors and students benefit from automated, educational feedback.",
        "data_platform_source": "GitHub REST API & PyLint Rule Engine",
        "target_profile": "Final-Year Student",
        "core_features": [
            "GitHub repository link ingestion & diff parsing",
            "Static analysis + LLM-based AST code review",
            "Code smell severity scoring (Critical, Warning, Info)",
            "Inline suggested diffs with explanations",
            "Weekly repository code health score dashboard"
        ],
        "tech_stack": [
            {"tool": "Python (FastAPI)", "justification": "Fast async backend for git diff parsing"},
            {"tool": "React / Tailwind", "justification": "Modern UI for displaying inline diffs"},
            {"tool": "GitHub REST API", "justification": "Fetch public repository file trees and commits"},
            {"tool": "Gemini / Claude API", "justification": "LLM reasoning for educational code explanations"}
        ],
        "data_sources": "Public GitHub repositories & PyLint/ESLint open-source rule sets.",
        "milestones": [
            "Week 1: Setup Python FastAPI backend & test single Python script paste parser",
            "Week 2: Integrate GitHub API service to pull commit diffs directly",
            "Week 3: Build React syntax-highlighted diff viewer & severity score logic",
            "Week 4: Add exportable PDF health report and test edge cases"
        ],
        "risk_flags": [
            "LLM context limit exceeded on large repositories (mitigate by analyzing single file diffs)"
        ],
        "ethical_flags": "Ensure private user repositories are never cached or stored without user consent.",
        "stretch_feature": "One-click 'Create GitHub PR Comment' clipboard generator.",
        "elaboration": {
            "folder_structure": """devmentor-ai/
├── backend/
│   ├── app/
│   │   ├── api/          # FastAPI routers (github.py, review.py)
│   │   ├── services/     # GitHub API parser & Gemini LLM engine
│   │   └── main.py       # FastAPI server entry
│   ├── requirements.txt
└── frontend/
    ├── index.html       # Clean multi-page UI
    └── app.js""",
            "mvp_feature_cut": [
                "Single-file code paste review with line-by-line recommendations",
                "Severity score rating (0-100)",
                "Inline suggested replacement code snippets"
            ],
            "features_to_skip": [
                "Skip GitHub OAuth multi-user organization login",
                "Skip background cron jobs for repository webhooks",
                "Skip complex database clustering"
            ],
            "step_by_step_build_order": [
                "1. Initialize Python FastAPI server with `/api/review` endpoint",
                "2. Write Python parser to pass code snippets to Gemini LLM JSON schema",
                "3. Build HTML/React frontend with code textarea and diff viewer",
                "4. Add GitHub API fetch service for public repo URLs",
                "5. Calculate overall repo Health Score"
            ],
            "top_3_blockers": [
                {
                    "blocker": "Gemini API returning markdown ```json blocks instead of pure JSON",
                    "fix": "Strip markdown code block fences using regex before parsing json.loads()."
                },
                {
                    "blocker": "GitHub API rate limits on unauthenticated IP addresses",
                    "fix": "Pass a standard GitHub Personal Access Token in request headers."
                },
                {
                    "blocker": "Code diff overflow breaking UI layout",
                    "fix": "Apply CSS overflow-x: auto and wrap code in font-mono pre tags."
                }
            ],
            "demo_script_60s": "Paste a Python script containing duplicate loops and SQL injection risks into DevMentor AI. Click 'Scan Code'. Within 3 seconds, the AI flags 3 code smells, displays inline diff recommendations, and gives an educational 65/100 code health score.",
            "wow_factor_20min": "Add a 'Copy GitHub PR Comment' button that formats Markdown ready for pasting directly onto GitHub!"
        }
    },
    {
        "id": "cand-ds-2",
        "domain": "Data Science",
        "title": "SkillGap AI: Placement Predictor & Job-Readiness Analytics",
        "pitch": "A machine-learning dashboard predicting student internship/job readiness while pinpointing target skill gaps.",
        "problem_and_beneficiaries": "Engineering students miss campus placements without knowing missing technical gaps; career advisors gain objective skill readiness metrics.",
        "data_platform_source": "Kaggle Open Campus Placement Dataset",
        "target_profile": "Intern / Junior Developer",
        "core_features": [
            "Student profile & academic resume feature extraction",
            "XGBoost placement probability model",
            "Target job role radar chart comparing student skill vector vs industry benchmarks",
            "Personalized 4-week skill closing roadmap"
        ],
        "tech_stack": [
            {"tool": "Python / scikit-learn", "justification": "Industry-standard machine learning library"},
            {"tool": "XGBoost", "justification": "High accuracy on tabular placement datasets"},
            {"tool": "Streamlit / React", "justification": "Rapid interactive dashboard rendering"}
        ],
        "data_sources": "Kaggle Campus Placement datasets & web-scraped open tech job descriptions.",
        "milestones": [
            "Week 1: Clean Kaggle placement dataset in Python & drop sensitive demographic features",
            "Week 2: Train XGBoost baseline classification model & evaluate ROC-AUC",
            "Week 3: Build skill vector subtraction engine comparing candidate vs job benchmarks",
            "Week 4: Build web dashboard UI with interactive skill gap radar charts"
        ],
        "risk_flags": [
            "Small sample size bias (mitigate by framing output as guidance estimates, not verdicts)"
        ],
        "ethical_flags": "Explicitly drop protected demographic attributes (gender, origin) to prevent model bias.",
        "stretch_feature": "Drag-and-drop PDF resume skill parser.",
        "elaboration": {
            "folder_structure": """skillgap-ai/
├── data/
│   ├── placement_data.csv
│   └── job_benchmarks.json
├── models/
│   ├── xgboost_model.pkl
│   └── train.py
├── app.py              # Main dashboard application
└── requirements.txt""",
            "mvp_feature_cut": [
                "Form inputs: CGPA, 5 core tech skills, # of projects",
                "Instant placement probability percentage score",
                "Skill gap bar chart comparing current vs role requirements"
            ],
            "features_to_skip": [
                "Skip real-time LinkedIn profile scraping",
                "Skip complex neural network embeddings for tabular data",
                "Skip automated recruiter email dispatchers"
            ],
            "step_by_step_build_order": [
                "1. Clean Kaggle placement CSV in Jupyter Notebook using Python pandas",
                "2. Train XGBoost classifier & save serialized model using joblib",
                "3. Write Python API taking student metrics and returning prediction probability",
                "4. Build frontend UI with sliders and radar chart visualizer",
                "5. Generate 4-week personalized skill roadmap"
            ],
            "top_3_blockers": [
                {
                    "blocker": "Pickle version incompatibility between training and server environment",
                    "fix": "Export model to JSON format using xgboost.save_model('model.json')."
                },
                {
                    "blocker": "Feature scaling discrepancy during single inference",
                    "fix": "Wrap feature scaling transformation inside a scikit-learn Pipeline object."
                },
                {
                    "blocker": "Radar chart overlapping labels",
                    "fix": "Limit radar chart axes to top 6 primary technical skill categories."
                }
            ],
            "demo_script_60s": "Input CGPA 7.4 and Python/SQL skills aiming for a Data Engineer role. Click 'Analyze Readiness'. The model outputs 68% Placement Readiness and highlights a critical gap in 'Distributed Spark'. Click 'Generate Plan' to view a 4-week learning roadmap.",
            "wow_factor_20min": "Add a drag-and-drop PDF resume parser using pdfplumber to auto-fill form fields!"
        }
    },
    {
        "id": "cand-nlp-3",
        "domain": "NLP",
        "title": "Antigravity: Intelligent Capstone Project Mentor",
        "pitch": "An NLP system that parses student skills and semantically matches them to feasibility-checked capstone blueprints.",
        "problem_and_beneficiaries": "Final-year students waste weeks choosing buildable projects; students get instant structured project briefs with weekly build plans.",
        "data_platform_source": "Curated Open Capstone Knowledge Base",
        "target_profile": "Final-Year Student",
        "core_features": [
            "Skill & Interest profile extraction",
            "Embedding similarity matching engine",
            "Structured 9-field project generator",
            "One-click PDF project brief exporter"
        ],
        "tech_stack": [
            {"tool": "Python / FastAPI", "justification": "Fast async REST API server"},
            {"tool": "Gemini API", "justification": "Structured JSON outputs with direct mentoring tone"},
            {"tool": "Tailwind CSS / HTML5", "justification": "Clean multi-page web application UI"}
        ],
        "data_sources": "Curated capstone database across SE, Data Science, NLP, CV, Healthcare, Fintech, & Sustainability.",
        "milestones": [
            "Week 1: Curate idea knowledge base & write structured system prompt in Python",
            "Week 2: Implement FastAPI REST endpoints & Pydantic schema validation",
            "Week 3: Build multi-page light-theme web UI with profile wizard",
            "Week 4: Integrate html2pdf brief exporter and test edge-case fallbacks"
        ],
        "risk_flags": [
            "LLM proposing infeasible or proprietary datasets (mitigate via explicit system constraints)"
        ],
        "ethical_flags": "Explicitly highlight privacy risks when domain involves personal or biometric data.",
        "stretch_feature": "Conversational multi-turn project scope refinement chat.",
        "elaboration": {
            "folder_structure": """antigravity-mentor/
├── app.py              # Main FastAPI server
├── system_prompts.py   # System prompts & Pydantic schemas
├── candidate_db.py     # Reference project blueprints
├── generator.py        # Gemini API & fallback engine
├── static/
│   └── index.html      # Light-theme multi-page web UI
└── requirements.txt""",
            "mvp_feature_cut": [
                "Profile wizard taking skills, time budget, and team size",
                "3 tailored idea cards with MVP features and milestones",
                "Deep-dive mentor view"
            ],
            "features_to_skip": [
                "Skip user registration authentication databases",
                "Skip video tutorial generation pipelines",
                "Skip multi-region database clustering"
            ],
            "step_by_step_build_order": [
                "1. Define Python Pydantic models for StudentInput and ProjectIdea",
                "2. Write `generator.py` with structured Gemini LLM prompt and fallback matrix",
                "3. Build FastAPI routes `/api/generate` and `/api/elaborate`",
                "4. Build Tailwind CSS multi-page frontend with responsive tabs",
                "5. Wire html2pdf.js for client-side PDF project brief export"
            ],
            "top_3_blockers": [
                {
                    "blocker": "Gemini API key missing or quota exhausted during live demo",
                    "fix": "Implement smart template-driven fallback engine that generates custom ideas dynamically without external network dependency."
                },
                {
                    "blocker": "HTML2PDF clipping text on multi-page exports",
                    "fix": "Apply CSS page-break-inside: avoid on card containers."
                },
                {
                    "blocker": "FastAPI CORS errors on localhost",
                    "fix": "Add CORSMiddleware with allow_origins=['*']."
                }
            ],
            "demo_script_60s": "Select 'Python, React' with 8 weeks available for a Final-Year Student aiming for Fintech. Click 'Generate 3 Project Ideas'. 3 custom projects appear in under 2 seconds. Click 'Deep Dive Mentor' to view folder structure, build order, and blocker fixes. Click 'Export PDF' to download the proposal.",
            "wow_factor_20min": "Add a one-click 'Copy GitHub README.md Template' button pre-populated with milestones and tech stack!"
        }
    },
    {
        "id": "cand-cv-4",
        "domain": "Computer Vision",
        "title": "VisionTrack: Privacy-Preserving Classroom Attendance Logger",
        "pitch": "A campus face detection system logging attendance and attention metrics without saving biometric facial templates.",
        "problem_and_beneficiaries": "Manual roll-call wastes 10 minutes of class time; university faculty receive automated attendance logs while protecting student privacy.",
        "data_platform_source": "MediaPipe Vision & DAiSEE Dataset",
        "target_profile": "Intern / Junior Developer",
        "core_features": [
            "Webcam face detection via MediaPipe (CPU friendly)",
            "Head pose orientation & attention score proxy heuristic",
            "Automated attendance sheet log exporter (CSV)",
            "Classroom engagement timeline dashboard"
        ],
        "tech_stack": [
            {"tool": "Python / OpenCV", "justification": "Standard image processing framework"},
            {"tool": "MediaPipe", "justification": "Lightweight CPU facial landmark detection"},
            {"tool": "FastAPI", "justification": "Backend server for processing frame metrics"},
            {"tool": "SQLite", "justification": "Local relational store for attendance timestamps"}
        ],
        "data_sources": "Live local webcam feed or open DAiSEE classroom video dataset.",
        "milestones": [
            "Week 1: Initialize MediaPipe Face Mesh in Python & verify face count logic",
            "Week 2: Calculate head pose orientation vector to derive attention score",
            "Week 3: Build FastAPI backend & SQLite database for logging timestamps",
            "Week 4: Build web dashboard UI with attendance table export"
        ],
        "risk_flags": [
            "Privacy concerns regarding video capture (mitigate by storing only numeric anonymized counts)"
        ],
        "ethical_flags": "Requires explicit opt-in consent flow; avoid biometric facial recognition matching.",
        "stretch_feature": "Edge deployment on Raspberry Pi with local status LED.",
        "elaboration": {
            "folder_structure": """visiontrack/
├── backend/
│   ├── vision.py        # MediaPipe face & head pose logic
│   ├── database.py      # SQLite session logs
│   └── app.py           # FastAPI endpoints
├── static/
│   └── index.html       # Classroom dashboard UI
└── requirements.txt""",
            "mvp_feature_cut": [
                "Webcam frame processing",
                "Face count detection",
                "CSV attendance sheet exporter"
            ],
            "features_to_skip": [
                "Skip multi-camera RTSP network streaming",
                "Skip 3D facial recognition identification matching",
                "Skip facial emotion sentiment analysis"
            ],
            "step_by_step_build_order": [
                "1. Write Python script initializing MediaPipe Face Mesh",
                "2. Calculate head orientation vector from nose and eye landmarks",
                "3. Log timestamp + attention score to SQLite every 5 seconds",
                "4. Build FastAPI web UI displaying face count and attention graph",
                "5. Add 'Export CSV' button for faculty"
            ],
            "top_3_blockers": [
                {
                    "blocker": "Webcam streaming thread freezing browser UI",
                    "fix": "Run frame processing inside a dedicated background Python thread."
                },
                {
                    "blocker": "False face detections in dim lighting",
                    "fix": "Apply OpenCV histogram equalization (cv2.equalizeHist) before detection."
                },
                {
                    "blocker": "Browser blocking camera access on HTTP",
                    "fix": "Test on localhost or use mkcert for local HTTPS."
                }
            ],
            "demo_script_60s": "Turn on webcam. As you turn your head toward the screen, attention reads 95% (Green). Turn away, and the score drops to 30% (Yellow). Click 'End Session' to download the attendance CSV.",
            "wow_factor_20min": "Add a 'Privacy Mode' toggle that blurs faces in the live UI while keeping numeric counts!"
        }
    },
    {
        "id": "cand-health-5",
        "domain": "Healthcare + ML",
        "title": "ArogyaAssist: Rural Symptom Checker & Triage Guidance Bot",
        "pitch": "An offline-first symptom checker classifying triage urgency for rural healthcare centers with clear medical disclaimers.",
        "problem_and_beneficiaries": "Rural clinics lack initial triage staff; health workers receive rapid guidance on patient urgency.",
        "data_platform_source": "Kaggle Disease-Symptom Open Dataset & WHO Guidelines",
        "target_profile": "Beginner Student",
        "core_features": [
            "Interactive conversational symptom intake checklist",
            "Probabilistic disease shortlist classifier (scikit-learn)",
            "Urgency triage classification (Immediate ER vs Doctor vs Home Monitor)",
            "Nearest rural clinic locator static map"
        ],
        "tech_stack": [
            {"tool": "Python / scikit-learn", "justification": "Fast, interpretable disease prediction model"},
            {"tool": "FastAPI", "justification": "Lightweight web backend"},
            {"tool": "Tailwind CSS / HTML5", "justification": "Mobile-friendly web interface"}
        ],
        "data_sources": "Kaggle Disease Symptom Prediction dataset & WHO symptom guidelines.",
        "milestones": [
            "Week 1: Clean Kaggle symptom dataset in Python & normalize symptom names",
            "Week 2: Train scikit-learn Decision Tree classifier & safety triage rules",
            "Week 3: Build chat UI for symptom intake with prominent disclaimers",
            "Week 4: Add offline nearest clinic locator map and test 5 test cases"
        ],
        "risk_flags": [
            "Risk of user treating output as medical advice (mitigate with mandatory disclaimer banner)"
        ],
        "ethical_flags": "MUST include prominent medical disclaimers; never present output as a diagnosis.",
        "stretch_feature": "Multilingual regional language switcher.",
        "elaboration": {
            "folder_structure": """arogya-assist/
├── model/
│   ├── train.py
│   └── disease_symptom_matrix.csv
├── app.py              # FastAPI server & triage rules
├── static/
│   └── index.html      # Mobile chat interface
└── requirements.txt""",
            "mvp_feature_cut": [
                "Text symptom selection checklist",
                "Top 3 probabilistic condition matches",
                "Triage urgency color badge (Red/Yellow/Green) + Disclaimer"
            ],
            "features_to_skip": [
                "Skip Electronic Health Record (EHR) hospital database integration",
                "Skip automated prescription writing",
                "Skip live video consultation calls"
            ],
            "step_by_step_build_order": [
                "1. Clean Kaggle symptom dataset mapping 40 symptoms in Python pandas",
                "2. Train Decision Tree classifier outputting probability scores",
                "3. Implement safety triage override rules (e.g. chest pain forces RED TRIAGE)",
                "4. Build chat UI for symptom intake with prominent medical disclaimers",
                "5. Verify triage safety outputs on test medical scenarios"
            ],
            "top_3_blockers": [
                {
                    "blocker": "Model overconfidence on rare diseases",
                    "fix": "Apply predict_proba() thresholding (> 0.20 cutoff) to display top 3 matches."
                },
                {
                    "blocker": "User typing informal symptom slang",
                    "fix": "Use fuzzy string matching (fuzzywuzzy/RapidFuzz) to map input to medical terms."
                },
                {
                    "blocker": "Regulatory concerns regarding medical advice",
                    "fix": "Place an un-dismissable 'Educational Triage Tool Only' banner at the top of every screen."
                }
            ],
            "demo_script_60s": "Open ArogyaAssist. Accept disclaimer. Select 'High Fever' and 'Cough'. The bot outputs 'Triage: Consult Doctor Within 24 Hours' and displays 2 nearby community healthcare centers.",
            "wow_factor_20min": "Add a one-click Language Switcher changing UI from English to Hindi in 100ms!"
        }
    },
    {
        "id": "cand-fin-6",
        "domain": "Fintech",
        "title": "SpendGuard: Personal Finance Anomaly Detector",
        "pitch": "A privacy-first personal finance tracker that flags unusual spending spikes using Isolation Forests and gives AI budget tips.",
        "problem_and_beneficiaries": "Young adults suffer budget leaks from unexpected trial charges; users receive instant spending anomaly alerts.",
        "data_platform_source": "Kaggle Synthetic Financial Transaction Datasets",
        "target_profile": "Beginner Student",
        "core_features": [
            "Bank statement CSV parser & auto-categorization",
            "Isolation Forest spending anomaly detection",
            "Category spend breakdown dashboard",
            "AI-generated budget optimization tips"
        ],
        "tech_stack": [
            {"tool": "Python / Pandas", "justification": "Robust transaction data manipulation"},
            {"tool": "scikit-learn", "justification": "Isolation Forest for unsupervised outlier detection"},
            {"tool": "FastAPI / HTML5", "justification": "Clean financial dashboard layout"}
        ],
        "data_sources": "Anonymized sample bank statement CSV datasets.",
        "milestones": [
            "Week 1: Write Python CSV parser normalizing Date, Description, & Amount columns",
            "Week 2: Train scikit-learn Isolation Forest model on transaction amounts",
            "Week 3: Build dashboard layout with expense pie chart & anomaly badges",
            "Week 4: Add AI budgeting tips & export monthly health report"
        ],
        "risk_flags": [
            "Sensitive financial data leak risk (mitigate by processing CSV data locally in memory)"
        ],
        "ethical_flags": "Ensure user bank statements are never saved to disk or uploaded to external servers.",
        "stretch_feature": "Recurring subscription detector flagging forgotten trial charges.",
        "elaboration": {
            "folder_structure": """spendguard/
├── app.py              # FastAPI entry point
├── parser.py           # Bank CSV cleaner
├── anomaly.py          # Isolation Forest detector
├── static/
│   └── index.html      # Financial dashboard UI
└── sample_data.csv""",
            "mvp_feature_cut": [
                "CSV bank statement uploader",
                "Transaction anomaly highlighter table",
                "3 AI budget reduction recommendations"
            ],
            "features_to_skip": [
                "Skip live Plaid bank account API connections",
                "Skip multi-currency exchange rate converters",
                "Skip stock investment portfolio tracking"
            ],
            "step_by_step_build_order": [
                "1. Write Python CSV parser normalizing columns (Date, Description, Amount)",
                "2. Fit scikit-learn IsolationForest(contamination=0.05) on Amount feature",
                "3. Filter transactions marked as -1 (Anomalies) & highlight in red in UI",
                "4. Generate budget tips for top spending categories",
                "5. Render summary metrics (Total Spent, # of Anomalies, Savings)"
            ],
            "top_3_blockers": [
                {
                    "blocker": "Bank CSV column names varying across different banks",
                    "fix": "Implement fuzzy column matching (mapping 'Debit', 'Cost', 'Txn Amount' to 'Amount')."
                },
                {
                    "blocker": "Isolation Forest flagging high legitimate rent payments",
                    "fix": "Add rule-based overrides excluding recurring fixed amounts from anomaly scores."
                },
                {
                    "blocker": "Large CSV files freezing browser UI",
                    "fix": "Limit parsing to max 1,000 rows for real-time processing."
                }
            ],
            "demo_script_60s": "Upload sample statement CSV. SpendGuard flags 2 red anomaly alerts: an unexpected $140 subscription and a 300% dining spike. View the AI tip: 'You spent 42% on food delivery — meal prep could save $180/mo.'",
            "wow_factor_20min": "Add an interactive 'Savings Slider' projecting 12-month savings when cutting identified anomalies!"
        }
    },
    {
        "id": "cand-sust-7",
        "domain": "Sustainability / IoT",
        "title": "EcoSort: Edge Waste Sorting & Recycling Assistant",
        "pitch": "A camera-based waste classifier guiding correct recyclable vs compostable disposal with gamified eco-score tracking.",
        "problem_and_beneficiaries": "Improper waste disposal contaminates recycling streams; university campuses improve recycling accuracy.",
        "data_platform_source": "Kaggle TrashNet Open Dataset (2,500+ Images)",
        "target_profile": "Intern / Junior Developer",
        "core_features": [
            "Real-time camera image classification (MobileNet)",
            "Disposal bin recommendation (Recyclable, Organic, General)",
            "Campus sustainability analytics dashboard",
            "Gamified Eco-Score leaderboard"
        ],
        "tech_stack": [
            {"tool": "Python / PyTorch", "justification": "Transfer learning on MobileNetV2"},
            {"tool": "FastAPI", "justification": "API server for image inference"},
            {"tool": "Tailwind CSS / HTML5", "justification": "Mobile camera interface"}
        ],
        "data_sources": "Kaggle TrashNet dataset (2,500+ labeled images of glass, paper, plastic, trash).",
        "milestones": [
            "Week 1: Prepare TrashNet dataset in Python & run MobileNetV2 transfer learning",
            "Week 2: Evaluate model classification accuracy (target > 88%)",
            "Week 3: Build web camera capture UI submitting images to FastAPI backend",
            "Week 4: Add Eco-Score gamification system & campus waste dashboard"
        ],
        "risk_flags": [
            "Model misclassification on crushed items (mitigate by showing top-2 predictions)"
        ],
        "ethical_flags": "Ensure camera feed processing occurs locally without recording background visitors.",
        "stretch_feature": "Carbon offset savings estimator per item recycled.",
        "elaboration": {
            "folder_structure": """ecosort/
├── model/
│   ├── train.py
│   └── mobilenet_model.pth
├── app.py              # FastAPI backend
├── static/
│   └── index.html      # Camera UI
└── requirements.txt""",
            "mvp_feature_cut": [
                "Webcam snapshot capture",
                "Waste classification output (Organic / Plastic / Paper)",
                "Bin color recommendation (Green / Blue / Black)"
            ],
            "features_to_skip": [
                "Skip robotic arm servo-motor hardware integration",
                "Skip multi-object bounding box detection",
                "Skip product barcode scanning"
            ],
            "step_by_step_build_order": [
                "1. Train MobileNetV2 on TrashNet dataset using PyTorch in Python",
                "2. Build HTML5 webcam snapshot UI submitting base64 image to backend",
                "3. Return category + confidence score + matching bin icon from FastAPI",
                "4. Track total items recycled count in session",
                "5. Calculate CO2 offset metric"
            ],
            "top_3_blockers": [
                {
                    "blocker": "PyTorch model file size too large (> 100MB) for GitHub",
                    "fix": "Quantize model weights to int8 to reduce model size to < 15MB."
                },
                {
                    "blocker": "Low confidence on complex background images",
                    "fix": "Crop center bounding box before running inference."
                },
                {
                    "blocker": "Webcam resolution mismatching model input shape",
                    "fix": "Resize image array to 224x224 RGB tensor using OpenCV."
                }
            ],
            "demo_script_60s": "Hold a plastic water bottle up to the webcam. Click 'Scan Item'. In 0.5s, EcoSort displays: 'Plastic Bottle — 94% Confidence → Dispose in BLUE RECYCLING BIN'. Eco-Score increases +10 points.",
            "wow_factor_20min": "Add a 'Carbon Offset Counter' calculating kg of CO2 saved for every 10 items recycled!"
        }
    },
    {
        "id": "cand-sec-8",
        "domain": "Cyber Security",
        "title": "PhishShield: Real-Time Email Phishing & URL Scanner",
        "pitch": "A security analyzer evaluating email headers, link redirects, and domain age to flag malicious phishing attempts.",
        "problem_and_beneficiaries": "Employees and students fall victim to credential harvesting; security teams receive instant risk scores.",
        "data_platform_source": "PhishTank API & WHOIS Domain Database",
        "target_profile": "Final-Year Student",
        "core_features": [
            "Email header & SPF/DKIM verification parser",
            "URL redirect expander & WHOIS domain age checker",
            "Machine learning phishing risk classifier",
            "Security audit report exporter"
        ],
        "tech_stack": [
            {"tool": "Python / FastAPI", "justification": "Fast backend for WHOIS lookups"},
            {"tool": "scikit-learn", "justification": "Random Forest model trained on URL features"},
            {"tool": "HTML5 / Tailwind", "justification": "Clean security dashboard"}
        ],
        "data_sources": "PhishTank open API & Kaggle Malicious URLs dataset.",
        "milestones": [
            "Week 1: Write Python URL feature extractor (URL length, @ symbol count, WHOIS age)",
            "Week 2: Train Random Forest classifier on Kaggle phishing dataset",
            "Week 3: Build FastAPI endpoint `/api/scan-url` and link expander",
            "Week 4: Build web dashboard UI with security risk indicators"
        ],
        "risk_flags": [
            "False positives on newly registered legitimate domains (mitigate via WHOIS age weighting)"
        ],
        "ethical_flags": "Obfuscate user email credentials before scanning email headers.",
        "stretch_feature": "Browser extension popup flagging malicious links on hover.",
        "elaboration": {
            "folder_structure": """phishshield/
├── backend/
│   ├── scanner.py       # URL & WHOIS parser
│   ├── model.pkl        # Random Forest model
│   └── app.py           # FastAPI endpoints
├── static/
│   └── index.html      # Security UI
└── requirements.txt""",
            "mvp_feature_cut": [
                "URL text scanner input",
                "Phishing risk score (0-100%)",
                "3 key risk indicators (Domain age, SSL status, Redirect chain)"
            ],
            "features_to_skip": [
                "Skip enterprise Active Directory LDAP integration",
                "Skip automated firewall IP blocking scripts",
                "Skip multi-node SIEM log ingestion"
            ],
            "step_by_step_build_order": [
                "1. Build Python feature extractor taking URL strings",
                "2. Train scikit-learn Random Forest model on Kaggle Phishing dataset",
                "3. Build FastAPI REST endpoint returning risk score JSON",
                "4. Build frontend scanner UI with red/yellow/green indicator badges",
                "5. Add exportable PDF security report"
            ],
            "top_3_blockers": [
                {
                    "blocker": "WHOIS lookup timeout on slow DNS servers",
                    "fix": "Apply 3-second timeout cutoff on python-whois requests."
                },
                {
                    "blocker": "Shortened URLs hiding destination domains",
                    "fix": "Use python requests.head(url, allow_redirects=True) to resolve final destination."
                },
                {
                    "blocker": "False positives on HTTPS domains",
                    "fix": "Include domain SSL certificate validity as an explicit model feature."
                }
            ],
            "demo_script_60s": "Paste a suspicious login URL into PhishShield. Click 'Scan Link'. Within 2 seconds, the tool flags 'High Risk: 92% Phishing Probability' highlighting a 2-day-old domain age and suspicious IP redirect.",
            "wow_factor_20min": "Add a one-click 'Report to PhishTank' button formatting an automated threat report!"
        }
    }
]
