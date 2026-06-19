import re

from apps.resumes.models import (
    ResumeSkill,
    Skill,
)


class SkillExtractorService:

    SKILL_CATALOG = {
    "Programming Languages": [
        "Python", "Java", "JavaScript", "TypeScript", "SQL", "C++", "C#", "Go", "Golang",
        "Ruby", "PHP", "Rust", "Kotlin", "Swift", "Scala", "R", "HTML5", "CSS3", "Sass"
    ],
    "Frameworks": [
        "Django", "Django REST Framework", "DRF", "Flask", "FastAPI", "React", "React.js",
        "Node.js", "Express.js", "NestJS", "Angular", "Vue.js", "Next.js", "Spring Boot",
        "Laravel", "Ruby on Rails", "Tailwind CSS", "Bootstrap", "GraphQL"
    ],
    "Databases": [
        "PostgreSQL", "Postgres", "MySQL", "Redis", "MongoDB", "SQLite", "Oracle",
        "Microsoft SQL Server", "DynamoDB", "Cassandra", "Elasticsearch", "Neo4j", "Firebase"
    ],
    "Cloud Platforms": [
        "AWS", "Amazon Web Services", "Azure", "GCP", "Google Cloud Platform", "Heroku", "DigitalOcean"
    ],
    "DevOps Tools": [
        "Docker", "Kubernetes", "Git", "GitHub", "GitLab", "CI/CD", "Jenkins", "Ansible",
        "Terraform", "Celery", "Nginx", "Apache", "Prometheus", "Grafana", "CircleCI", "ArgoCD",
        "Jira", "Slack", "Trello", "Asana", "Notion", "Confluence", "Kanban", "Scrum"
    ],
    "Data Engineering Tools": [
        "Kafka", "Apache Kafka", "Spark", "Apache Spark", "Hadoop", "Databricks", "Airflow",
        "Apache Airflow", "Snowflake", "dbt", "Hive", "Flink", "Redshift", "BigQuery", "Snowflake"
    ],
    "AI / Machine Learning": [
        "TensorFlow", "PyTorch", "Scikit-Learn", "Keras", "OpenCV", "Pandas", "NumPy",
        "LangChain", "OpenAI", "Hugging Face", "LLM", "NLP", "Computer Vision", "Speech Recognition",

    ],
    "Testing Frameworks": [
        "PyTest", "Unittest", "Jest", "Mocha", "Selenium", "Cypress", "Postman", "JUnit"
    ],
    "Architecture / Concepts": [
        "Microservices", "REST API", "gRPC", "WebSockets", "Serverless", "OOP", "MVC", "TDD"
    ]
    }

    NORMALIZED_NAMES = {
        # Programming Languages
        "python": "Python",
        "java": "Java",
        "javascript": "JavaScript",
        "js": "JavaScript",
        "typescript": "TypeScript",
        "ts": "TypeScript",
        "sql": "SQL",
        "c++": "C++",
        "cpp": "C++",
        "c#": "C#",
        "csharp": "C#",
        "golang": "Go",
        "go": "Go",
        "ruby": "Ruby",
        "php": "PHP",
        "rust": "Rust",
        "kotlin": "Kotlin",
        "swift": "Swift",
        "scala": "Scala",
        "html": "HTML5",
        "html5": "HTML5",
        "css": "CSS3",
        "css3": "CSS3",
        "sass": "Sass",

        # Frameworks
        "django": "Django",
        "djangorestframework": "Django REST Framework",
        "django rest framework": "Django REST Framework",
        "drf": "DRF",
        "flask": "Flask",
        "fastapi": "FastAPI",
        "react": "React",
        "reactjs": "React",
        "react.js": "React",
        "node": "Node.js",
        "nodejs": "Node.js",
        "node.js": "Node.js",
        "express": "Express.js",
        "expressjs": "Express.js",
        "nestjs": "NestJS",
        "angular": "Angular",
        "angularjs": "Angular",
        "vue": "Vue.js",
        "vuejs": "Vue.js",
        "nextjs": "Next.js",
        "next.js": "Next.js",
        "springboot": "Spring Boot",
        "spring boot": "Spring Boot",
        "laravel": "Laravel",
        "rails": "Ruby on Rails",
        "ruby on rails": "Ruby on Rails",
        "graphql": "GraphQL",

        # Databases
        "postgres": "PostgreSQL",
        "postgresql": "PostgreSQL",
        "mysql": "MySQL",
        "redis": "Redis",
        "mongodb": "MongoDB",
        "mongo": "MongoDB",
        "sqlite": "SQLite",
        "mssql": "Microsoft SQL Server",
        "sql server": "Microsoft SQL Server",
        "dynamodb": "DynamoDB",
        "cassandra": "Cassandra",
        "elasticsearch": "Elasticsearch",
        "firebase": "Firebase",

        # Cloud Platforms
        "aws": "AWS",
        "amazon web services": "AWS",
        "azure": "Azure",
        "gcp": "GCP",
        "google cloud": "GCP",
        "google cloud platform": "GCP",
        "heroku": "Heroku",

        # DevOps Tools
        "docker": "Docker",
        "k8s": "Kubernetes",
        "kubernetes": "Kubernetes",
        "git": "Git",
        "github": "GitHub",
        "gitlab": "GitLab",
        "cicd": "CI/CD",
        "ci/cd": "CI/CD",
        "jenkins": "Jenkins",
        "ansible": "Ansible",
        "terraform": "Terraform",
        "celery": "Celery",
        "nginx": "Nginx",

        # Data Engineering Tools
        "kafka": "Kafka",
        "apache kafka": "Kafka",
        "spark": "Spark",
        "apache spark": "Spark",
        "hadoop": "Hadoop",
        "databricks": "Databricks",
        "airflow": "Airflow",
        "apache airflow": "Airflow",
        "snowflake": "Snowflake",
        "dbt": "dbt",

        # AI / Machine Learning
        "tensorflow": "TensorFlow",
        "tf": "TensorFlow",
        "pytorch": "PyTorch",
        "scikit-learn": "Scikit-Learn",
        "sklearn": "Scikit-Learn",
        "pandas": "Pandas",
        "numpy": "NumPy",
        "langchain": "LangChain",
        "openai": "OpenAI",

        # Testing & Architecture
        "pytest": "PyTest",
        "unittest": "Unittest",
        "selenium": "Selenium",
        "postman": "Postman",
        "microservices": "Microservices",
        "rest": "REST API",
        "rest api": "REST API",
        "restful": "REST API",
        "grpc": "gRPC",
        "websockets": "WebSockets",
        "serverless": "Serverless"
    }

    @classmethod
    def get_catalog_items(cls):
        items = []

        for category, skills in cls.SKILL_CATALOG.items():
            for skill_name in skills:
                normalized = cls.normalize_skill_name(
                    skill_name
                )
                items.append(
                    (
                        normalized,
                        category,
                    )
                )

        return items

    @classmethod
    def normalize_skill_name(cls, skill_name):
        value = " ".join(
            skill_name.strip().split()
        )
        lower_value = (
            value.lower()
            .replace(".", "")
            .replace(" ", "")
        )

        return cls.NORMALIZED_NAMES.get(
            lower_value,
            value.upper() if value.lower() in {"aws", "gcp", "drf"} else value.title()
        )

    @staticmethod
    def contains_skill(text, skill_name):
        escaped = re.escape(
            skill_name.lower()
        )
        pattern = rf"(?<![a-z0-9+#]){escaped}(?![a-z0-9+#])"

        return re.search(
            pattern,
            text,
            re.IGNORECASE
        ) is not None

    @classmethod
    def extract_skills_from_text(cls, raw_text):
        if not raw_text:
            return []

        text = raw_text.lower()
        matches = []
        seen = set()

        for skill_name, _ in cls.get_catalog_items():
            if skill_name.lower() in seen:
                continue

            if cls.contains_skill(
                text,
                skill_name
            ):
                matches.append(
                    skill_name
                )
                seen.add(
                    skill_name.lower()
                )

        return matches

    @classmethod
    def extract_skills(
        cls,
        resume,
        raw_text
    ):

        if not raw_text:
            return []

        extracted_skills = cls.extract_skills_from_text(
            raw_text
        )
        catalog_categories = dict(
            cls.get_catalog_items()
        )

        for skill_name in extracted_skills:
            category = catalog_categories.get(
                skill_name,
                ""
            )

            skill, _ = Skill.objects.get_or_create(
                name=skill_name,
                defaults={
                    "category": category
                }
            )

            if not skill.category:
                skill.category = category
                skill.save(
                    update_fields=["category"]
                )

            ResumeSkill.objects.get_or_create(
                resume=resume,
                skill=skill,
                defaults={
                    "confidence_score": 100
                }
            )

        return extracted_skills
