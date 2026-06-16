import * as React from "react";
import { 
  Sparkles, 
  Briefcase, 
  Layers, 
  Activity, 
  ArrowUpRight,
  TrendingUp, 
  AlertTriangle, 
  CheckCircle2, 
  Award,
  ChevronRight,
  MapPin
} from "lucide-react";

// Mock Schema definitions for visual pipeline demonstration
interface MockJob {
  id: string;
  title: string;
  company: string;
  location: string;
  matchScore: number;
  type: string;
}

const RECOMMENDED_JOBS: MockJob[] = [
  { id: "1", title: "Senior AI Integration Engineer", company: "Aether Systems Labs", location: "San Francisco, CA (Hybrid)", matchScore: 96, type: "Full-Time" },
  { id: "2", title: "Python Software Architect", company: "QuantumData Corp", location: "Remote (US)", matchScore: 91, type: "Full-Time" },
  { id: "3", title: "Machine Learning Platform Engineer", company: "Helix AI Technologies", location: "New York, NY (On-Site)", matchScore: 88, type: "Contract" },
  { id: "4", title: "Full Stack Engineer (Django + React)", company: "Skyline SaaS Engineering", location: "Austin, TX (Hybrid)", matchScore: 85, type: "Full-Time" },
  { id: "5", title: "Data Pipelines Infrastructure Lead", company: "Vortex Intelligence", location: "Remote (Global)", matchScore: 82, type: "Full-Time" }
];

export default function EnterpriseDashboardPage() {
  return (
    <div className="space-y-8 max-w-[1500px] mx-auto pb-12">
      
      {/* Welcome Metadata Hub Header */}
      <div className="flex flex-col gap-1 sm:flex-row sm:items-center sm:justify-between border-b border-border/40 pb-5">
        <div>
          <h1 className="text-xl font-extrabold tracking-tight md:text-2xl text-foreground">
            Resume Intelligence Hub
          </h1>
          <p className="text-xs text-muted-foreground font-medium mt-0.5">
            Monitor real-time applicant indexing tracking scores and AI-matched market job opportunities.
          </p>
        </div>
        <div className="flex items-center gap-2 mt-3 sm:mt-0 px-3 py-1.5 bg-primary/5 text-primary border border-primary/20 rounded-xl text-xs font-bold">
          <Activity className="h-3.5 w-3.5 animate-pulse" />
          <span>AI Engine Active v1.0</span>
        </div>
      </div>

      {/* Section 1: Premium Metric telemetry matrix cards */}
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        
        {/* Resume Score Tracking KPI */}
        <div className="p-5 bg-card border border-border/80 rounded-2xl shadow-sm hover:shadow-md hover:border-border transition-all group">
          <div className="flex items-center justify-between">
            <span className="text-[11px] font-bold uppercase tracking-wider text-muted-foreground">Resume ATS Score</span>
            <div className="p-2 bg-primary/10 rounded-xl text-primary group-hover:scale-105 transition-transform">
              <Award className="h-4 w-4" />
            </div>
          </div>
          <div className="mt-3 flex items-baseline gap-2">
            <span className="text-2xl font-black tracking-tight">84</span>
            <span className="text-xs font-semibold text-muted-foreground">/100</span>
          </div>
          <div className="mt-2 flex items-center gap-1.5 text-[11px] text-emerald-600 font-bold dark:text-emerald-500">
            <TrendingUp className="h-3 w-3" />
            <span>Top 8% of applicants in pool</span>
          </div>
        </div>

        {/* Total Job Matches Card */}
        <div className="p-5 bg-card border border-border/80 rounded-2xl shadow-sm hover:shadow-md hover:border-border transition-all group">
          <div className="flex items-center justify-between">
            <span className="text-[11px] font-bold uppercase tracking-wider text-muted-foreground">AI Job Matches</span>
            <div className="p-2 bg-primary/10 rounded-xl text-primary group-hover:scale-105 transition-transform">
              <Briefcase className="h-4 w-4" />
            </div>
          </div>
          <div className="mt-3">
            <span className="text-2xl font-black tracking-tight">1,248</span>
          </div>
          <div className="mt-2 text-[11px] text-muted-foreground font-medium">
            <span className="text-foreground font-bold">142 new</span> matching recommendations today
          </div>
        </div>

        {/* Skill Gap Analysis Telemetry */}
        <div className="p-5 bg-card border border-border/80 rounded-2xl shadow-sm hover:shadow-md hover:border-border transition-all group">
          <div className="flex items-center justify-between">
            <span className="text-[11px] font-bold uppercase tracking-wider text-muted-foreground">Skill Match Gap</span>
            <div className="p-2 bg-destructive/10 rounded-xl text-destructive group-hover:scale-105 transition-transform">
              <Layers className="h-4 w-4" />
            </div>
          </div>
          <div className="mt-3">
            <span className="text-2xl font-black tracking-tight text-destructive">-4 Core</span>
          </div>
          <div className="mt-2 text-[11px] text-muted-foreground font-medium">
            Missing stack elements found for peak profiles
          </div>
        </div>

        {/* Application Hub Pipeline Placement */}
        <div className="p-5 bg-card border border-border/80 rounded-2xl shadow-sm hover:shadow-md hover:border-border transition-all group">
          <div className="flex items-center justify-between">
            <span className="text-[11px] font-bold uppercase tracking-wider text-muted-foreground">Applications In Pipeline</span>
            <div className="p-2 bg-primary/10 rounded-xl text-primary group-hover:scale-105 transition-transform">
              <Sparkles className="h-4 w-4" />
            </div>
          </div>
          <div className="mt-3">
            <span className="text-2xl font-black tracking-tight">18</span>
          </div>
          <div className="mt-2 text-[11px] text-muted-foreground font-medium">
            <span className="text-primary font-bold">3 active interviews</span> scheduled this cycle
          </div>
        </div>
      </div>

      {/* Main Structural Information Grid Split Layout */}
      <div className="grid gap-6 lg:grid-cols-3 items-start">
        
        {/* PRIMARY ZONE: Listings and Structural Improvement Suggestions */}
        <div className="lg:col-span-2 space-y-6">
          
          {/* Section 2: Premium Recommended Jobs Section */}
          <div className="bg-card border border-border/80 rounded-2xl shadow-sm p-6 space-y-4">
            <div className="flex items-center justify-between border-b border-border/40 pb-3">
              <div>
                <h2 className="text-sm font-extrabold tracking-tight text-foreground">Top AI Recommendation Feed</h2>
                <p className="text-[11px] text-muted-foreground font-medium">Ranked position matching structures adjusted to your indexing file.</p>
              </div>
              <button className="text-xs text-primary font-bold flex items-center gap-0.5 hover:underline cursor-pointer">
                <span>View All Feed</span>
                <ChevronRight className="h-3.5 w-3.5" />
              </button>
            </div>

            <div className="divide-y divide-border/60">
              {RECOMMENDED_JOBS.map((job) => (
                <div key={job.id} className="py-4 first:pt-0 last:pb-0 flex items-start justify-between gap-4 group transition-colors">
                  <div className="space-y-1">
                    <h3 className="text-xs font-bold text-foreground group-hover:text-primary transition-colors cursor-pointer">
                      {job.title}
                    </h3>
                    <div className="flex flex-wrap items-center gap-x-2.5 gap-y-1 text-[11px] text-muted-foreground font-medium">
                      <span className="text-foreground font-semibold">{job.company}</span>
                      <span className="text-border-foreground/20">•</span>
                      <span className="flex items-center gap-1">
                        <MapPin className="h-3 w-3 text-muted-foreground/60" />
                        {job.location}
                      </span>
                      <span className="text-border-foreground/20">•</span>
                      <span className="px-1.5 py-0.5 bg-accent text-accent-foreground text-[10px] font-bold rounded">
                        {job.type}
                      </span>
                    </div>
                  </div>

                  <div className="flex items-center gap-3 flex-shrink-0">
                    <div className="text-right">
                      <div className="text-xs font-black text-emerald-600 dark:text-emerald-500 bg-emerald-500/10 px-2 py-0.5 rounded-lg border border-emerald-500/20 inline-block">
                        {job.matchScore}% Match
                      </div>
                    </div>
                    <button className="text-[11px] font-bold bg-primary text-primary-foreground hover:bg-primary/90 px-3 py-1.5 rounded-xl shadow-sm cursor-pointer transition-all flex items-center gap-0.5">
                      <span>Apply</span>
                      <ArrowUpRight className="h-3 w-3" />
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Section 5: Resume Improvement Advice Hub */}
          <div className="bg-card border border-border/80 rounded-2xl shadow-sm p-6 space-y-4">
            <div>
              <h2 className="text-sm font-extrabold tracking-tight text-foreground">Actionable Indexing Suggestions</h2>
              <p className="text-[11px] text-muted-foreground font-medium">Execute these changes to elevate matching priority by an estimated 12-18%.</p>
            </div>

            <div className="grid gap-3 sm:grid-cols-2">
              <div className="p-4 border border-border/60 bg-accent/20 rounded-xl space-y-1">
                <span className="px-2 py-0.5 bg-primary/10 text-primary font-bold text-[10px] rounded-md">Cloud Architectures</span>
                <h4 className="text-xs font-bold text-foreground mt-1.5">Add Cloud Technologies</h4>
                <p className="text-[11px] text-muted-foreground font-medium">Integrate specific operational summaries detailing AWS provisioning or deployment pipelines.</p>
              </div>

              <div className="p-4 border border-border/60 bg-accent/20 rounded-xl space-y-1">
                <span className="px-2 py-0.5 bg-primary/10 text-primary font-bold text-[10px] rounded-md">Metrics Impact</span>
                <h4 className="text-xs font-bold text-foreground mt-1.5">Measurable Achievements</h4>
                <p className="text-[11px] text-muted-foreground font-medium">Replace passive descriptions with quantitative numbers (e.g., "boosted API runtime operations by 30%").</p>
              </div>

              <div className="p-4 border border-border/60 bg-accent/20 rounded-xl space-y-1">
                <span className="px-2 py-0.5 bg-primary/10 text-primary font-bold text-[10px] rounded-md">Architecture Depth</span>
                <h4 className="text-xs font-bold text-foreground mt-1.5">Improve Project Descriptions</h4>
                <p className="text-[11px] text-muted-foreground font-medium">Elaborate on backend data topologies and concurrent processing parameters built using Django.</p>
              </div>

              <div className="p-4 border border-border/60 bg-accent/20 rounded-xl space-y-1">
                <span className="px-2 py-0.5 bg-primary/10 text-primary font-bold text-[10px] rounded-md">DevOps Pipeline</span>
                <h4 className="text-xs font-bold text-foreground mt-1.5">Add CI/CD Pipeline Context</h4>
                <p className="text-[11px] text-muted-foreground font-medium">Detail configuration handling for workflow build templates using GitHub Actions or GitLab CI.</p>
              </div>
            </div>
          </div>

        </div>

        {/* SECONDARY SIDEBAR ZONE: Insights, Badges matrix and gaps */}
        <div className="space-y-6">
          
          {/* Section 3: High Contrast Strengths & Weaknesses Panel */}
          <div className="bg-card border border-border/80 rounded-2xl shadow-sm p-6 space-y-4">
            <div>
              <h2 className="text-sm font-extrabold tracking-tight text-foreground">Parser Extraction Insights</h2>
              <p className="text-[11px] text-muted-foreground font-medium">AI vector alignment against market job requisitions.</p>
            </div>

            <div className="space-y-4">
              {/* Strengths Container */}
              <div className="space-y-2">
                <div className="text-[10px] font-bold text-emerald-600 dark:text-emerald-500 tracking-wider uppercase flex items-center gap-1">
                  <CheckCircle2 className="h-3.5 w-3.5 text-emerald-500" />
                  <span>Verified Platform Strengths</span>
                </div>
                <ul className="space-y-1.5 text-xs font-semibold text-foreground pl-1">
                  <li className="flex items-center gap-2 bg-accent/40 px-2.5 py-1.5 rounded-lg border border-border/40">
                    <span className="h-1.5 w-1.5 rounded-full bg-emerald-500" />
                    <span>Strong Python Core Mastery</span>
                  </li>
                  <li className="flex items-center gap-2 bg-accent/40 px-2.5 py-1.5 rounded-lg border border-border/40">
                    <span className="h-1.5 w-1.5 rounded-full bg-emerald-500" />
                    <span>High-Density Project Portfolio</span>
                  </li>
                  <li className="flex items-center gap-2 bg-accent/40 px-2.5 py-1.5 rounded-lg border border-border/40">
                    <span className="h-1.5 w-1.5 rounded-full bg-emerald-500" />
                    <span>Relevant Architectural Experience</span>
                  </li>
                </ul>
              </div>

              {/* Weaknesses/Gaps Container */}
              <div className="space-y-2">
                <div className="text-[10px] font-bold text-amber-600 dark:text-amber-500 tracking-wider uppercase flex items-center gap-1">
                  <AlertTriangle className="h-3.5 w-3.5 text-amber-500" />
                  <span>Identified Indexing Vulnerabilities</span>
                </div>
                <ul className="space-y-1.5 text-xs font-semibold text-foreground pl-1">
                  <li className="flex items-center gap-2 bg-accent/40 px-2.5 py-1.5 rounded-lg border border-border/40">
                    <span className="h-1.5 w-1.5 rounded-full bg-amber-500" />
                    <span>Missing Cloud Requisitions (AWS)</span>
                  </li>
                  <li className="flex items-center gap-2 bg-accent/40 px-2.5 py-1.5 rounded-lg border border-border/40">
                    <span className="h-1.5 w-1.5 rounded-full bg-amber-500" />
                    <span>Missing Virtualization Context (Docker)</span>
                  </li>
                  <li className="flex items-center gap-2 bg-accent/40 px-2.5 py-1.5 rounded-lg border border-border/40">
                    <span className="h-1.5 w-1.5 rounded-full bg-amber-500" />
                    <span>Missing Continuous Integration (CI/CD)</span>
                  </li>
                </ul>
              </div>
            </div>
          </div>

          {/* Section 4: Chip Badges Skill Gap Matrix */}
          <div className="bg-card border border-border/80 rounded-2xl shadow-sm p-6 space-y-4">
            <div>
              <h2 className="text-sm font-extrabold tracking-tight text-foreground">Target Stack Skill Gaps</h2>
              <p className="text-[11px] text-muted-foreground font-medium">Acquire or index these keywords to clear automated platform filters.</p>
            </div>

            <div className="flex flex-wrap gap-2 pt-1">
              <div className="px-3 py-1.5 bg-destructive/5 text-destructive border border-destructive/20 text-xs font-bold rounded-xl flex items-center gap-1.5 shadow-sm">
                <span className="h-1.5 w-1.5 rounded-full bg-destructive animate-pulse" />
                <span>Docker Containerization</span>
              </div>
              <div className="px-3 py-1.5 bg-destructive/5 text-destructive border border-destructive/20 text-xs font-bold rounded-xl flex items-center gap-1.5 shadow-sm">
                <span className="h-1.5 w-1.5 rounded-full bg-destructive animate-pulse" />
                <span>Amazon Web Services (AWS)</span>
              </div>
              <div className="px-3 py-1.5 bg-destructive/5 text-destructive border border-destructive/20 text-xs font-bold rounded-xl flex items-center gap-1.5 shadow-sm">
                <span className="h-1.5 w-1.5 rounded-full bg-destructive animate-pulse" />
                <span>Redis Distributed Caching</span>
              </div>
              <div className="px-3 py-1.5 bg-destructive/5 text-destructive border border-destructive/20 text-xs font-bold rounded-xl flex items-center gap-1.5 shadow-sm">
                <span className="h-1.5 w-1.5 rounded-full bg-destructive animate-pulse" />
                <span>Kubernetes Orchestration</span>
              </div>
            </div>
          </div>

        </div>
      </div>

    </div>
  );
}