"""
Django Management Command: Load Portfolio Data

This command loads your portfolio information into the database with embeddings.
Run it with: python manage.py load_portfolio

You can either:
1. Provide a file path: python manage.py load_portfolio --file portfolio.txt
2. Use the default sample data provided in this file

The command will:
- Read your portfolio text
- Split it into intelligent chunks using LangChain (respects paragraphs, sentences)
- Generate embeddings for semantic search
- Save everything to the database for RAG

NEW: Uses LangChain's RecursiveCharacterTextSplitter for much better chunking!
"""
from django.core.management.base import BaseCommand
from api.rag_utils import load_portfolio_text
from api.models import PortfolioData


class Command(BaseCommand):
    help = 'Load portfolio data into the database for RAG'

    def add_arguments(self, parser):
        """Add command line arguments"""
        parser.add_argument(
            '--file',
            type=str,
            help='Path to a text file containing portfolio information',
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing portfolio data before loading',
        )

    def handle(self, *args, **options):
        """Execute the command"""
        
        # Clear existing data if requested
        if options['clear']:
            count = PortfolioData.objects.count()
            PortfolioData.objects.all().delete()
            self.stdout.write(
                self.style.WARNING(f'Cleared {count} existing portfolio entries')
            )
        
        # Load from file or use sample data
        if options['file']:
            self.load_from_file(options['file'])
        else:
            self.load_sample_data()
        
        self.stdout.write(
            self.style.SUCCESS('Portfolio data loaded successfully!')
        )

    def load_from_file(self, file_path):
        """Load portfolio data from a text file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # You can customize the category or parse it from the file
            count = load_portfolio_text(content, category='other')
            self.stdout.write(
                self.style.SUCCESS(f'Loaded {count} chunks from {file_path}')
            )
        except FileNotFoundError:
            self.stdout.write(
                self.style.ERROR(f'File not found: {file_path}')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error loading file: {str(e)}')
            )

    def load_sample_data(self):
        """
        Load sample portfolio data.
        
        CUSTOMIZE THIS: Replace with your actual portfolio information!
        Add details about your experience, skills, education, projects, etc.
        """
        self.stdout.write('Loading sample portfolio data...')
        
        # Sample Experience
        experience = """
        Mid-level Software Developer with over 5 years of experience, primarily in full-stack web development using React, C#, .NET, and Node.js, with additional experience in real time simulation, game engines and more. Proven track record in creating efficient website functionality with strong system design principles, reworking legacy code to improve performance using modern technologies, while ensuring alignment with existing project design principles.
Skilled in deploying, hosting, and migrating applications to cloud environments (Azure), managing on-premises systems, and implementing efficient CI/CD pipelines.
Strong focus on structured workflows using clear issue tracking (Jira), concise git logs and daily scrums. Excellent communicator and team player, while also able to work in a solo environment. 
        
        Sabbatical
        8 months (Jan 2025 – Sep 2025)
        Crick Software
        Software Developer – 1 Year (Mar 2024 – Jan 2025)
        Crick Software is a company that makes accessibility-first educational software for children and adults that may need additional support.
        Key Responsibilities:  Managing, updating, hosting and maintaining the websites responsible for the licensing of the software sold by the company (C#, Postgres).  Migrating existing applications into the cloud (Azure).  Creating matching algorithms to reduce data redundancy in their databases (Python).  Working alongside the UI/UX designer to rework the website to be more user friendly and accessible.
        Connected Places Catapult
        Software Developer – 4.5 Years (Nov 2019 – Mar 2024)
        CPC is a non-profit innovation organisation partially funded by government bodies such as Innovation UK, Dept. for Transport, etc. Mainly working with SMEs to “catapult” innovative ideas into reality.
        Key Responsibilities:  Leading work packages as a solo developer or managing a small technical team. Coding and contributing towards greenfield projects to create MVP / demonstrators, including all stages of the software development life cycle.  Mentoring other colleagues in their progression as a software developer through code walkthroughs, peer development and code reviews.  Hosting and maintaining project deliverables in the cloud (Azure) and streamlining processes with CICD pipelines.  Holding workshops with clients and other stakeholders to build up and document requirements (became a lead contributor in solution design) and presenting the project outputs.
        """
        count = load_portfolio_text(experience, category='experience')
        self.stdout.write(f'  ✓ Loaded {count} experience chunks')
        
        # Sample Skills
        skills = """
        Technical Skills:
        
        C# - 2 Years in industry
        C++ - 2 Years in industry
        Python - 5 Years in industry
        React - 4 Years in industry
        SQL - 5 Years in industry
        PostgreSQL - 5 Years in industry
        JavaScript - 5 Years in industry
        HTML - 5 Years in industry
        CSS - 5 Years in industry
        TypeScript - 2 Years in industry
        .NET - 2 Years in industry
        Node.js - 5 Years in industry
        RESTful APIs - 5 Years in industry
        GitHub - 5 Years in industry
        Docker - 3 Years in industry
        Azure - 5 Years in industry
        Git - 5 Years in industry
        
        SQL / Relational Databases / Data Layer

With ~5 years of experience, I’m comfortable designing normalized schemas and translating domain models into relational tables, relationships, indexing strategies, constraints, and migrations.

I regularly write optimized queries involving JOINs, subqueries, aggregates, window functions, CTEs, and transactions.

I’ve applied performance tuning: identifying slow queries via execution plans, tuning indexes, rewriting queries or denormalizing where necessary to reduce latency.

I understand ACID properties, isolation levels, concurrency conflicts, and how to avoid/handle deadlocks and race conditions in high-traffic systems.

I’ve managed database schema migrations (backwards/forwards safe), data migrations, versioning, rollbacks, and ensuring data integrity through migration scripts and validation.

In cloud & distributed settings, I’ve handled scaling considerations: partitioning, read replicas, caching layers, sharding (if needed), and consistency trade-offs.

Back End / APIs / .NET / C#

I design and implement RESTful APIs (or RPC / gRPC where appropriate), with proper routing, validation, serialization, authentication and authorization.

I use modern C# features: async/await, LINQ, generics, nullable reference types, pattern matching, and newer .NET language constructs (e.g. records, init-only properties).

I build maintainable systems using SOLID principles, dependency injection, interface-driven design, separation of concerns, layering, and modular architecture.

I handle cross-cutting concerns: logging, error handling, exception propagation, metrics, tracing, circuit breakers, retry logic, and rate limiting.

I refactor legacy code: restructuring, reducing technical debt, extracting modular components, improving maintainability, and aligning with modern .NET (e.g. migrating from older .NET versions or frameworks to .NET Core / .NET 8+).

I integrate with external systems: third-party APIs, message queues, event-driven architectures, and background tasks (workers, scheduled jobs).

I design domain logic and business rules carefully, ensuring testability, decoupling, and extendibility.

Front End / React / JavaScript / UI Integration

I build reusable React components, manage component state (via hooks, Context API, or state management libraries), and organize component hierarchies cleanly.

I integrate front end with APIs (REST or GraphQL), handle data fetching, error handling, caching, pagination, optimistic updates, and synchronization.

I ensure responsive and accessible UI: layout across breakpoints, ARIA attributes, keyboard navigation, contrast, and support for assistive technologies.

I optimize performance: code splitting, lazy loading, memoization, reducing re-renders, virtualizing lists, and minimizing bundle size.

I manage CSS (or CSS-in-JS, SASS, or styled components) alongside React, dynamic styling, theming, and modular styles.

I debug across browsers, inspect network requests, handle asynchronous flows, and maintain consistency across devices.

Cloud / DevOps / Infrastructure / Deployment

I migrate monolithic or on-prem systems to cloud architectures (Azure), rewriting or adapting services to leverage cloud-native services.

I deploy and manage apps in Azure (App Services, Azure SQL / PostgreSQL, serverless functions, storage accounts, service bus, key vaults).

I build and maintain CI/CD pipelines (GitHub Actions, Azure DevOps, or equivalent): build, test, deploy, rollback strategies, environment promotion (dev → staging → production).

I configure infrastructure as code (IaC) using ARM templates, Bicep, Terraform, or Azure Resource Manager; I version, review, and roll out infrastructure changes.

I monitor, observe, and maintain observability: setting up logging, metrics, alerts, dashboards (e.g. Application Insights, Prometheus, Grafana) to detect anomalies or failures early.

I manage scaling and availability: auto-scaling rules, load balancing, failover, high availability design, geo-distribution where needed.

I enforce security best practices: secrets management, network isolation (VNets, subnets, NSGs), identity & access management (IAM), and ensuring compliance (SSL/TLS, encryption at rest/in transit).

Architecture, System Design & High-Level Thinking

I can break down a product requirement or user story into subsystems, modules, interfaces, and APIs; I reason about coupling, cohesion, and trade-offs.

I evaluate design alternatives and choose appropriate patterns (e.g. MVC, CQRS, event sourcing, repository, unit-of-work, mediator) based on context and constraints.

I weigh scalability, maintainability, extensibility, cost, and performance trade-offs when making architectural decisions.

I anticipate and mitigate failure modes (cascading failures, bottlenecks, single points of failure) by introducing fallback paths, retries, circuit breakers, bulkheads, and graceful degradation.

I decompose monoliths when needed into services or modules, considering domain boundaries, data ownership, communication patterns (synchronous vs asynchronous).

I define APIs and contracts that are versionable, resilient to change, and backwards-compatible.

I engage in design reviews, critique proposals, and evaluate architecture trade-offs from multiple perspectives (Scalability, Security, Performance, Maintainability).

Testing, Quality & Reliability

I write unit tests, integration tests, and automated end-to-end tests; I use test doubles (mocks, stubs) appropriately, and structure tests for determinism and isolation.

I practice TDD or behavior-driven development (where suitable) to drive design and ensure coverage.

I maintain CI gates: test suites, linting, static analysis to enforce quality, consistency, and early detection of regressions.

I set up performance / load tests (e.g. for critical endpoints), and benchmark and detect regressions.

I introduce resiliency tests: chaos or fault injection, error paths, timeouts, circuit-breaking, and monitoring of failure scenarios.

I track and address technical debt proactively, maintain code hygiene (refactoring, cleanup, removing obsolete code).

Mentorship, Collaboration & Communication

I conduct code reviews and provide feedback focusing on clarity, readability, consistency, performance, and maintainability.

I mentor junior developers: share patterns, best practices, pair programming, walkthroughs, and help unblock them.

I lead or contribute to architectural and technical discussions, presenting ideas, trade-offs, risks, and alternatives clearly to both technical and non-technical stakeholders.

I facilitate requirement-gathering sessions with product / business teams: ask probing questions, uncover edge cases, define acceptance criteria, understand constraints.

I write clear documentation (design docs, API specs, system diagrams, runbooks) so others can onboard or maintain systems after me.

I communicate progress, trade-offs, risks, and blockers transparently in Agile ceremonies (standups, sprint planning, retrospectives).

Personal & Cognitive Traits (Soft / Non-Technical)

I show curiosity and continuous learning: staying updated on new technologies, reading blogs, attending meetups, experimenting with new tools or patterns.

I embrace problem-solving mindset: breaking ambiguous problems into solvable parts, validating assumptions, iterating toward solutions.

I practice empathy and active listening: understanding teammates’ perspectives, learning preferences, and constraints before proposing solutions.

I take ownership and accountability: when something fails or slips, I dive in to fix, learn, and prevent recurrence.

I adapt to ambiguity and change: switching focus, reworking features, balancing priorities under shifting requirements.

I foster collaboration: I’m open to feedback, able to compromise, and willing to help others succeed.

I maintain attention to detail, especially in edge cases, security, error handling, and data integrity.

I show time management and prioritisation: deciding which tasks move the project forward, balancing speed vs quality, avoiding over-engineering.

I exercise resilience and patience, especially when debugging production issues or handling technical debt.

        """
        count = load_portfolio_text(skills, category='skills')
        self.stdout.write(f'  ✓ Loaded {count} skills chunks')
        
        # Sample Education
        education = """
        Education:
        
        Bachelor of Science in Computer Science
        University of Lincoln, 2016-2019
        Grade: 2:1 (0.5% from a 1st)
        
        Relevant Coursework:
        - Data Structures and Algorithms
        - Database Systems
        - Web Development
        - Software Engineering
        - Robotics
        - Mobile Application Development
        - Operating Systems
        - Computer Networks
        - Artificial Intelligence
        - Human-Computer Interaction
        
        """
        count = load_portfolio_text(education, category='education')
        self.stdout.write(f'  ✓ Loaded {count} education chunks')
        
        # Sample Projects
        projects = """
        Notable Projects:
        
        1. Licensing System for Crick Software
            - Updated visuals and added new functionality to the existing licensing system
            - tech Stack: C#, .NET, PostgreSQL, React, CSS, HTML, Blazor, Azure
            - Created a Python script that automated the matching of organisations and licenses between our two legacy systems using data from the Microsoft Dynamics API.
            - Periodically addressed bugs in the backlog to ensure smooth operation of the licensing system.
        
        2. Building Management Portal
           - Developed a website portal for housing monitoring officers to manage the status of their buildings, allowing for visualisations, reporting, and issue tracking.
           - Tech: React, Node.js, PostgreSQL, CSS, HTML, JavaScript, Docker, Azure 
        
        3. AI-Powered Portfolio API (2025)
           - Created an intelligent portfolio API using RAG (Retrieval-Augmented Generation)
           - Tech: Django, OpenAI API, Sentence Transformers, PostgreSQL
           - Provides context-aware responses about my career and skills

        4. Automated Driving System Testing Simulation
              - Developed a simulation environment for testing automated driving systems
              - Tech: C++, Prescan
              - Implemented various traffic scenarios to evaluate system performance and safety
        """
        count = load_portfolio_text(projects, category='projects')
        self.stdout.write(f'  ✓ Loaded {count} projects chunks')
        
        # Sample Preferences
        preferences = """
        Work Preferences:

        I'm looking for a remote or hybrid position up to 3 days in the office per week.

        I enjoy:
        - Building scalable backend systems
        - Solving complex technical problems
        - Mentoring other developers
        - Learning new technologies
        
        I'm particularly interested in:
        - AI/ML integration in web applications
        - Microservices architecture
        - Real-time systems
        - API design and development
        
        Location: Open to remote opportunities worldwide or hybrid roles in London
        Availability: Available for full-time positions starting immediately
        Salary Expectations: Competitive market rate based on experience
        """
        count = load_portfolio_text(preferences, category='preferences')
        self.stdout.write(f'  ✓ Loaded {count} preferences chunks')
        
        # Sample Achievements
        achievements = """
        """
        count = load_portfolio_text(achievements, category='achievements')
        self.stdout.write(f'  ✓ Loaded {count} achievements chunks')
        
        total = PortfolioData.objects.count()
        self.stdout.write(
            self.style.SUCCESS(f'\n📊 Total portfolio chunks in database: {total}')
        )
