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
  MapPin,
  ShieldAlert,
  ArrowRight
} from "lucide-react";

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

export default function HighFidelityDashboardPage() {
  return (
    <div className="space-y-8 relative bg-radial-gradient min-h-screen">
      
      {/* 1. UPPER SAAS WELCOME HEADER PANEL */}
      <div className="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between border-b border-border/50 pb-6">
        <div>
          <h1 className="text-2xl font-black tracking-tight text-foreground sm:text-3xl">
            Resume Intelligence Workspace
          </h1>
          <p className="text-xs text-muted-foreground font-semibold mt-1">
            Real-time pipeline monitoring, automated ATS matching indices, and parsing telemetry analytics.
          </p>
        </div>
        <div className="flex items-center gap-2 self-start sm:self-center px-3.5 py-2 bg-card border border-border/80 rounded-xl premium-shadow text-xs font-bold text-foreground">
          <span className="h-2 w-2 rounded-full bg-feature-green animate-pulse" />
          <span>AI Engine Active v1.2</span>
        </div>
      </div>

      {/* 2. SPECIFIED FEATURE ACCENT KPI TELEMETRY GRID */}
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        
        {/* Card A: Resume Score - Blue Accent */}
        <div className="p-6 bg-card border border-border/60 border-l-4 border-l-feature-blue rounded-2xl premium-shadow hover:-translate-y-0.5 transition-all duration-300 group">
          <div className="flex items-center justify-between">
            <span className="text-[11px] font-bold uppercase tracking-wider text-muted-foreground">Resume ATS Score</span>
            <div className="p-2.5 bg-feature-blue/5 text-feature-blue rounded-xl group-hover:scale-105 transition-transform">
              <Award className="h-4 w-4" />
            </div>
          </div>
          <div className="mt-4 flex items-baseline gap-1.5">
            <span className="text-3xl font-black tracking-tight text-foreground">84</span>
            <span className="text-xs font-bold text-muted-foreground">/100</span>
          </div>
          <div className="mt-3 flex items-center gap-1.5 text-[11px] text-emerald-600 dark:text-emerald-500 font-bold">
            <TrendingUp className="h-3.5 w-3.5" />
            <span>Top 8% of sector pool entries</span>
          </div>
        </div>

        {/* Card B: Job Matches - Green Accent */}
        <div className="p-6 bg-card border border-border/60 border-l-4 border-l-feature-green rounded-2xl premium-shadow hover:-translate-y-0.5 transition-all duration-300 group">
          <div className="flex items-center justify-between">
            <span className="text-[11px] font-bold uppercase tracking-wider text-muted-foreground">AI Job Matches</span>
            <div className="p-2.5 bg-feature-green/5 text-feature-green rounded-xl group-hover:scale-105 transition-transform">
              <Briefcase className="h-4 w-4" />
            </div>
          </div>
          <div className="mt-4">
            <span className="text-3xl font-black tracking-tight text-foreground">1,248</span>
          </div>
          <div className="mt-3 text-[11px] text-muted-foreground font-semibold">
            <span className="text-feature-green font-extrabold">+142 entries</span> added since last sync
          </div>
        </div>

        {/* Card C: Skill Gap - Amber Accent */}
        <div className="p-6 bg-card border border-border/60 border-l-4 border-l-feature-amber rounded-2xl premium-shadow hover:-translate-y-0.5 transition-all duration-300 group">
          <div className="flex items-center justify-between">
            <span className="text-[11px] font-bold uppercase tracking-wider text-muted-foreground">Skill Match Gap</span>
            <div className="p-2.5 bg-feature-amber/5 text-feature-amber rounded-xl group-hover:scale-105 transition-transform">
              <Layers className="h-4 w-4" />
            </div>
          </div>
          <div className="mt-4">
            <span className="text-3xl font-black tracking-tight text-feature-amber">-4 Core</span>
          </div>
          <div className="mt-3 text-[11px] text-muted-foreground font-semibold flex items-center gap-1">
            <ShieldAlert className="h-3.5 w-3.5 text-feature-amber/80" />
            <span>Missing critical container tags</span>
          </div>
        </div>

        {/* Card D: ATS Dash Score Placement - Purple Accent */}
        <div className="p-6 bg-card border border-border/60 border-l-4 border-l-feature-purple rounded-2xl premium-shadow hover:-translate-y-0.5 transition-all duration-300 group">
          <div className="flex items-center justify-between">
            <span className="text-[11px] font-bold uppercase tracking-wider text-muted-foreground">ATS Index Ranking</span>
            <div className="p-2.5 bg-feature-purple/5 text-feature-purple rounded-xl group-hover:scale-105 transition-transform">
              <Sparkles className="h-4 w-4" />
            </div>
          </div>
          <div className="mt-4">
            <span className="text-3xl font-black tracking-tight text-foreground">Tier 1</span>
          </div>
          <div className="mt-3 text-[11px] text-feature-purple font-extrabold flex items-center gap-1">
            <span>Optimized for corporate scrapers</span>
          </div>
        </div>
      </div>

      {/* 3. DUAL COLUMN INFORMATION WORKSPACE GRID CONTENT */}
      <div className="grid gap-6 lg:grid-cols-3 items-start">
        
        {/* LEFT COMPONENT COLUMN (Takes 2 Columns) */}
        <div className="lg:col-span-2 space-y-6">
          
          {/* Recommended Jobs Card Container */}
          <div className="bg-card border border-border/60 rounded-2xl premium-shadow p-6 space-y-4">
            <div className="flex items-center justify-between border-b border-border/40 pb-4">
              <div>
                <h2 className="text-xs font-black uppercase tracking-wider text-foreground">Top AI Recommendation Feed</h2>
                <p className="text-[11px] text-muted-foreground font-semibold mt-0.5">Ranked position alignment scores optimized to your file profile.</p>
              </div>
              <button className="text-xs text-primary font-bold flex items-center gap-0.5 hover:underline cursor-pointer group">
                <span>View Full Board</span>
                <ChevronRight className="h-3.5 w-3.5 transition-transform group-hover:translate-x-0.5" />
              </button>
            </div>

            <div className="divide-y divide-border/40">
              {RECOMMENDED_JOBS.map((job) => (
                <div key={job.id} className="py-4 first:pt-0 last:pb-0 flex items-start justify-between gap-4 group">
                  <div className="space-y-1">
                    <h3 className="text-xs font-bold text-foreground group-hover:text-primary transition-colors cursor-pointer leading-snug">
                      {job.title}
                    </h3>
                    <div className="flex flex-wrap items-center gap-x-2.5 gap-y-1 text-[11px] text-muted-foreground font-semibold">
                      <span className="text-foreground/90">{job.company}</span>
                      <span className="text-border-foreground/10">•</span>
                      <span className="flex items-center gap-1">
                        <MapPin className="h-3 w-3 text-muted-foreground/60" />
                        {job.location}
                      </span>
                      <span className="text-border-foreground/10">•</span>
                      <span className="px-1.5 py-0.5 bg-secondary text-secondary-foreground text-[10px] font-bold rounded">
                        {job.type}
                      </span>
                    </div>
                  </div>

                  <div className="flex items-center gap-3 flex-shrink-0">
                    <span className="text-xs font-black text-emerald-600 dark:text-emerald-500 bg-feature-green/5 dark:bg-feature-green/10 px-2 py-1 rounded-lg border border-feature-green/10 whitespace-nowrap">
                      {job.matchScore}% Match
                    </span>
                    <button className="text-[11px] font-bold bg-zinc-900 dark:bg-zinc-100 text-zinc-50 dark:text-zinc-900 hover:bg-zinc-800 dark:hover:bg-zinc-200 h-8 px-3 rounded-xl shadow-sm transition-all cursor-pointer flex items-center gap-0.5">
                      <span>Apply</span>
                      <ArrowUpRight className="h-3 w-3" />
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Actionable Parsing Optimization Panel */}
          <div className="bg-card border border-border/60 rounded-2xl premium-shadow p-6 space-y-4">
            <div>
              <h2 className="text-xs font-black uppercase tracking-wider text-foreground">Actionable Indexing Optimization</h2>
              <p className="text-[11px] text-muted-foreground font-semibold mt-0.5">Execute these structural adjustments to clear corporate ATS filter rules.</p>
            </div>

            <div className="grid gap-3 sm:grid-cols-2">
              <div className="p-4 border border-border/60 hover:border-feature-blue/30 bg-background/40 rounded-xl space-y-1.5 transition-colors group cursor-pointer">
                <span className="px-2 py-0.5 bg-feature-blue/10 text-feature-blue font-bold text-[10px] rounded-md">Cloud Deployment</span>
                <h4 className="text-xs font-bold text-foreground mt-1 flex items-center gap-1">
                  <span>Add Cloud Technologies</span>
                  <ArrowRight className="h-3 w-3 opacity-0 group-hover:opacity-100 group-hover:translate-x-0.5 transition-all" />
                </h4>
                <p className="text-[11px] text-muted-foreground font-semibold leading-relaxed">Integrate operational descriptions detailing AWS provisioning setups.</p>
              </div>

              <div className="p-4 border border-border/60 hover:border-feature-green/30 bg-background/40 rounded-xl space-y-1.5 transition-colors group cursor-pointer">
                <span className="px-2 py-0.5 bg-feature-green/10 text-feature-green font-bold text-[10px] rounded-md">Metrics Evaluation</span>
                <h4 className="text-xs font-bold text-foreground mt-1 flex items-center gap-1">
                  <span>Measurable Achievements</span>
                  <ArrowRight className="h-3 w-3 opacity-0 group-hover:opacity-100 group-hover:translate-x-0.5 transition-all" />
                </h4>
                <p className="text-[11px] text-muted-foreground font-semibold leading-relaxed">Replace descriptive strings with explicit metrics (e.g., "optimized lookup speed by 40%").</p>
              </div>
            </div>
          </div>

        </div>

        {/* RIGHT METRICS SIDEBAR COMPONENT COLUMN (Takes 1 Column) */}
        <div className="space-y-6">
          
          {/* Parser Extraction Insights Insights panel card */}
          <div className="bg-card border border-border/60 rounded-2xl premium-shadow p-6 space-y-4">
            <div>
              <h2 className="text-xs font-black uppercase tracking-wider text-foreground">Parser Extraction Insights</h2>
              <p className="text-[11px] text-muted-foreground font-semibold mt-0.5">AI vector processing maps aligned to global demand models.</p>
            </div>

            <div className="space-y-4">
              {/* Strengths mapping array stack block */}
              <div className="space-y-2">
                <div className="text-[10px] font-black text-emerald-600 dark:text-emerald-500 tracking-wider uppercase flex items-center gap-1">
                  <CheckCircle2 className="h-3.5 w-3.5 text-feature-green" />
                  <span>Verified Platform Strengths</span>
                </div>
                <div className="space-y-1.5 text-xs font-semibold text-foreground">
                  <div className="px-3 py-2 bg-background border border-border/60 rounded-xl flex items-center gap-2">
                    <span className="h-1.5 w-1.5 rounded-full bg-feature-green" />
                    <span>Strong Python Core Mastery</span>
                  </div>
                  <div className="px-3 py-2 bg-background border border-border/60 rounded-xl flex items-center gap-2">
                    <span className="h-1.5 w-1.5 rounded-full bg-feature-green" />
                    <span>High-Density Project Portfolio</span>
                  </div>
                </div>
              </div>

              {/* Weaknesses mapping array stack block */}
              <div className="space-y-2">
                <div className="text-[10px] font-black text-feature-amber tracking-wider uppercase flex items-center gap-1">
                  <AlertTriangle className="h-3.5 w-3.5" />
                  <span>Identified Filter Weaknesses</span>
                </div>
                <div className="space-y-1.5 text-xs font-semibold text-foreground">
                  <div className="px-3 py-2 bg-background border border-border/60 rounded-xl flex items-center gap-2">
                    <span className="h-1.5 w-1.5 rounded-full bg-feature-amber" />
                    <span>Missing Virtualization Context (Docker)</span>
                  </div>
                  <div className="px-3 py-2 bg-background border border-border/60 rounded-xl flex items-center gap-2">
                    <span className="h-1.5 w-1.5 rounded-full bg-feature-amber" />
                    <span>Missing Automated Deployment (CI/CD)</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Chip badge skill block cluster */}
          <div className="bg-card border border-border/60 rounded-2xl premium-shadow p-6 space-y-4">
            <div>
              <h2 className="text-xs font-black uppercase tracking-wider text-foreground">Target Stack Skill Gaps</h2>
              <p className="text-[11px] text-muted-foreground font-semibold mt-0.5">Acquire or index these keys to clear automated filters.</p>
            </div>

            <div className="flex flex-wrap gap-1.5 pt-1">
              {["Docker Containerization", "Amazon Web Services", "Redis Clusters", "Kubernetes Mesh"].map((skill) => (
                <span key={skill} className="px-2.5 py-1.5 bg-feature-amber/5 text-feature-amber border border-feature-amber/20 text-[11px] font-bold rounded-xl flex items-center gap-1.5">
                  <span className="h-1.5 w-1.5 rounded-full bg-feature-amber animate-pulse" />
                  <span>{skill}</span>
                </span>
              ))}
            </div>
          </div>

        </div>
      </div>

    </div>
  );
}