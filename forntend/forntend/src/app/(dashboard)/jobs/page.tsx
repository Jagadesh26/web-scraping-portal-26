"use client";

import * as React from "react";
import { 
  Search, 
  MapPin, 
  Briefcase, 
  Building2, 
  SlidersHorizontal, 
  ArrowUpRight, 
  Bookmark, 
  Calendar,
  Clock,
  CheckCircle,
  Share2,
  DollarSign
} from "lucide-react";
import { cn } from "@/lib/utils";

interface JobRecord {
  id: string;
  title: string;
  company: string;
  location: string;
  salary: string;
  experience: string;
  postedTime: string;
  matchScore: number;
  tags: string[];
  description: string;
}

const MOCK_JOB_DATABASE: JobRecord[] = [
  {
    id: "job-01",
    title: "Senior Full Stack Architect (Django & Next.js)",
    company: "Vortex SaaS Engineering",
    location: "Chennai, TN (Hybrid)",
    salary: "₹18,00,000 - ₹24,00,000 P.A.",
    experience: "5 - 8 Yrs",
    postedTime: "2 hours ago",
    matchScore: 98,
    tags: ["Django", "Next.js 15", "PostgreSQL", "React", "AWS"],
    description: "We are scout-tracking a Lead Architect to direct our backend enterprise systems integration layer. You will take ownership of cross-platform API contracts, microservice event queues, and implement scalable dashboard processing matrices."
  },
  {
    id: "job-02",
    title: "AI Integration & Pipelines Specialist",
    company: "Helix Intelligence Corp",
    location: "Remote (India)",
    salary: "₹22,00,000 - ₹30,00,000 P.A.",
    experience: "3 - 6 Yrs",
    postedTime: "1 day ago",
    matchScore: 91,
    tags: ["Python", "FastAPI", "LLM Orchestration", "LangChain", "Redis"],
    description: "Join our core machine learning operations workspace. This production assignment focuses on structuring absolute high-throughput vector extraction layers, custom model quantization paths, and building fault-tolerant middleware caches."
  },
  {
    id: "job-03",
    title: "Backend Cloud Infrastructure Lead",
    company: "Aether Systems Labs",
    location: "Bangalore, KA (On-Site)",
    salary: "₹25,00,000 - ₹35,00,000 P.A.",
    experience: "8 - 12 Yrs",
    postedTime: "3 days ago",
    matchScore: 86,
    tags: ["Docker", "Kubernetes", "CI/CD Actions", "GCP", "Terraform"],
    description: "Manage global cluster deployment metrics, maintain infrastructure-as-code asset trees, and enforce extreme network isolation rules across production relational nodes and processing brokers."
  },
  {
    id: "job-04",
    title: "Python Web Application Engineer",
    company: "Quantum Analytics Inc",
    location: "Hyderabad, TS (Hybrid)",
    salary: "₹12,00,000 - ₹16,00,000 P.A.",
    experience: "2 - 4 Yrs",
    postedTime: "4 days ago",
    matchScore: 84,
    tags: ["Django REST Framework", "Celery", "PostgreSQL", "Redis"],
    description: "Maintain core multi-tenant business automation logic portals. Build transaction pipelines, manage async telemetry calculation worker queues, and refine raw SQL database access pathways."
  }
];

export default function ProfessionalJobsBoard() {
  const [selectedJob, setSelectedJob] = React.useState<JobRecord>(MOCK_JOB_DATABASE[0]);
  const [searchQuery, setSearchQuery] = React.useState("");

  return (
    <div className="space-y-6 max-w-[1600px] mx-auto h-[calc(100vh-6rem)] flex flex-col">
      
      {/* 1. UPPER OMNI-SEARCH FILTERS WRAPPER PANEL */}
      <div className="p-4 bg-card border border-border/80 rounded-2xl shadow-sm space-y-3 flex-shrink-0">
        <div className="grid gap-3 md:grid-cols-7">
          {/* Key Skill Context String Input */}
          <div className="md:col-span-3 relative flex items-center">
            <Search className="absolute left-3.5 h-4 w-4 text-muted-foreground" />
            <input
              type="text"
              placeholder="Enter active design tags, roles, or software stack keywords..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full bg-background border border-border rounded-xl pl-10 pr-4 py-2 text-xs text-foreground focus:outline-none focus:border-primary transition-all font-medium placeholder:text-muted-foreground/60"
            />
          </div>

          {/* Location Anchor Input field */}
          <div className="md:col-span-2 relative flex items-center">
            <MapPin className="absolute left-3.5 h-4 w-4 text-muted-foreground" />
            <input
              type="text"
              placeholder="Preferred work city or 'Remote'..."
              className="w-full bg-background border border-border rounded-xl pl-10 pr-4 py-2 text-xs text-foreground focus:outline-none focus:border-primary transition-all font-medium placeholder:text-muted-foreground/60"
            />
          </div>

          {/* Experience Range Dropdown Mockup */}
          <div className="md:col-span-1 relative flex items-center">
            <Briefcase className="absolute left-3.5 h-4 w-4 text-muted-foreground" />
            <select className="w-full bg-background border border-border rounded-xl pl-10 pr-4 py-2 text-xs text-foreground focus:outline-none focus:border-primary transition-all font-semibold appearance-none cursor-pointer">
              <option>Experience</option>
              <option>Entry Level</option>
              <option>Mid Senior</option>
              <option>Executive</option>
            </select>
          </div>

          {/* Primary Action Find Buttons */}
          <button className="md:col-span-1 w-full bg-white text-black hover:bg-white/90 text-xs font-bold rounded-xl transition-all cursor-pointer flex items-center justify-center gap-1.5 h-9">
            <span>Search Jobs</span>
          </button>
        </div>

        {/* Quick Filter Pill Chips Row */}
        <div className="flex flex-wrap items-center justify-between gap-4 border-t border-border/40 pt-3">
          <div className="flex items-center gap-2">
            <span className="text-[10px] uppercase font-bold tracking-wider text-muted-foreground">Quick Sorting:</span>
            {["Remote Only", "Salary > ₹15L", "Match Score > 90%", "Posted Last 24h"].map((pill) => (
              <button key={pill} className="px-3 py-1 bg-background border border-border hover:border-muted-foreground text-[11px] font-semibold text-foreground/90 rounded-lg transition-colors cursor-pointer">
                {pill}
              </button>
            ))}
          </div>
          <button className="text-xs text-muted-foreground hover:text-foreground font-bold flex items-center gap-1.5 cursor-pointer">
            <SlidersHorizontal className="h-3.5 w-3.5" />
            <span>Advanced Search Rules</span>
          </button>
        </div>
      </div>

      {/* 2. DUAL SPLIT VIEW INFORMATION WORKSPACE LAYOUT */}
      <div className="grid lg:grid-cols-5 gap-6 flex-1 overflow-hidden min-h-0">
        
        {/* LEFT COLUMN: Scrollable Reusable Feed List (Takes 2 columns space layout) */}
        <div className="lg:col-span-2 overflow-y-auto pr-2 space-y-3 custom-feed-scrollbar">
          <div className="text-xs font-bold text-muted-foreground px-1 pb-1">
            Showing {MOCK_JOB_DATABASE.length} highly targeted position profiles matching your profile
          </div>
          
          {MOCK_JOB_DATABASE.map((job) => {
            const isSelected = selectedJob.id === job.id;
            return (
              <div
                key={job.id}
                onClick={() => setSelectedJob(job)}
                className={cn(
                  "p-5 border rounded-2xl shadow-sm transition-all cursor-pointer group relative bg-card",
                  isSelected 
                    ? "border-white bg-white/[0.02]" 
                    : "border-border/80 hover:border-zinc-700"
                )}
              >
                {/* AI Vector Alignment Indicator floating Pill */}
                <div className="absolute top-5 right-5 text-[10px] font-black tracking-tight text-emerald-500 bg-emerald-500/10 border border-emerald-500/20 px-2 py-0.5 rounded-md">
                  {job.matchScore}% Match
                </div>

                <div className="space-y-2 max-w-[80%]">
                  <h3 className="text-xs font-black text-foreground group-hover:text-white transition-colors leading-snug">
                    {job.title}
                  </h3>
                  
                  <div className="flex items-center gap-2 text-[11px] text-muted-foreground font-semibold">
                    <Building2 className="h-3.5 w-3.5 flex-shrink-0 text-muted-foreground/60" />
                    <span className="text-foreground">{job.company}</span>
                  </div>

                  <div className="flex flex-wrap items-center gap-x-3 gap-y-1 text-[11px] text-muted-foreground/80 font-medium pt-1">
                    <span className="flex items-center gap-1">
                      <MapPin className="h-3 w-3 text-muted-foreground/50" />
                      {job.location}
                    </span>
                    <span>•</span>
                    <span className="flex items-center gap-1">
                      <Clock className="h-3 w-3 text-muted-foreground/50" />
                      {job.experience}
                    </span>
                  </div>
                </div>

                {/* Micro Tech Skill Stack Badges chips block */}
                <div className="flex flex-wrap gap-1.5 pt-4">
                  {job.tags.slice(0, 3).map((tag) => (
                    <span key={tag} className="px-2 py-0.5 bg-background border border-border text-[10px] font-semibold text-muted-foreground rounded">
                      {tag}
                    </span>
                  ))}
                  {job.tags.length > 3 && (
                    <span className="text-[9px] font-bold text-muted-foreground/60 self-center pl-1">
                      +{job.tags.length - 3} more
                    </span>
                  )}
                </div>

                <div className="border-t border-border/40 mt-4 pt-3 flex items-center justify-between text-[11px] text-muted-foreground font-medium">
                  <span>{job.postedTime}</span>
                  <span className="text-foreground font-bold opacity-0 group-hover:opacity-100 transition-opacity flex items-center gap-0.5">
                    <span>Inspect Details</span>
                    <ChevronRight className="h-3 w-3" />
                  </span>
                </div>
              </div>
            );
          })}
        </div>

        {/* RIGHT COLUMN: Static Contextual Description Overview Workspace Frame (3 columns) */}
        <div className="hidden lg:flex lg:col-span-3 border border-border/80 bg-card rounded-2xl flex-col overflow-hidden">
          {/* Header Metadata Ribbon Block */}
          <div className="p-6 border-b border-border/60 space-y-4 bg-white/[0.01]">
            <div className="flex items-start justify-between gap-4">
              <div className="space-y-1.5">
                <h2 className="text-sm font-black text-foreground leading-tight">
                  {selectedJob.title}
                </h2>
                <div className="text-xs font-bold text-white/90 hover:underline cursor-pointer">
                  {selectedJob.company}
                </div>
              </div>
              
              <div className="text-right flex-shrink-0">
                <div className="text-xs font-black text-emerald-500 bg-emerald-500/10 border border-emerald-500/20 px-2.5 py-1 rounded-xl inline-block">
                  {selectedJob.matchScore}% Match Index
                </div>
              </div>
            </div>

            {/* Quick Metrics Dashboard Bar */}
            <div className="grid grid-cols-3 gap-2 p-3 bg-background border border-border rounded-xl text-[11px] font-semibold text-muted-foreground">
              <div className="space-y-0.5 border-r border-border">
                <span className="block text-[10px] text-muted-foreground/50 uppercase font-bold">Experience Reqd</span>
                <span className="text-foreground font-bold">{selectedJob.experience}</span>
              </div>
              <div className="space-y-0.5 border-r border-border pl-2">
                <span className="block text-[10px] text-muted-foreground/50 uppercase font-bold">Salary Range</span>
                <span className="text-foreground font-bold">{selectedJob.salary.split(" ")[0]}</span>
              </div>
              <div className="space-y-0.5 pl-2">
                <span className="block text-[10px] text-muted-foreground/50 uppercase font-bold">Work Location</span>
                <span className="text-foreground font-bold truncate block">{selectedJob.location.split(" ")[0]}</span>
              </div>
            </div>

            {/* Action Submissions Buttons Frame */}
            <div className="flex items-center justify-between gap-3 pt-1">
              <div className="flex items-center gap-2 text-[11px] text-muted-foreground font-medium">
                <Calendar className="h-3.5 w-3.5 text-muted-foreground/60" />
                <span>Posted: <span className="text-foreground font-semibold">{selectedJob.postedTime}</span></span>
              </div>
              
              <div className="flex items-center gap-2">
                <button className="p-2 border border-border hover:border-muted-foreground rounded-xl text-foreground transition-colors cursor-pointer" title="Save this description profile mapping">
                  <Bookmark className="h-4 w-4" />
                </button>
                <button className="p-2 border border-border hover:border-muted-foreground rounded-xl text-foreground transition-colors cursor-pointer" title="Share asset link coordinates">
                  <Share2 className="h-4 w-4" />
                </button>
                <button className="bg-white text-black hover:bg-white/90 text-xs font-bold h-9 px-5 rounded-xl transition-all shadow-sm cursor-pointer flex items-center gap-1">
                  <span>Apply Position</span>
                  <ArrowUpRight className="h-3.5 w-3.5" />
                </button>
              </div>
            </div>
          </div>

          {/* Body Content Description Scrollable Box Area */}
          <div className="flex-1 overflow-y-auto p-6 space-y-6 custom-feed-scrollbar text-xs leading-relaxed text-muted-foreground font-medium">
            
            {/* Context A: Summary Text */}
            <div className="space-y-2">
              <h4 className="text-xs font-black text-foreground uppercase tracking-wide">Role Overview Summary</h4>
              <p className="text-foreground/80 font-medium leading-relaxed">{selectedJob.description}</p>
            </div>

            {/* Context B: AI Skill Target Verification Check list matrix */}
            <div className="space-y-3 border-t border-border/40 pt-5">
              <h4 className="text-xs font-black text-foreground uppercase tracking-wide">AI Analyzer Target Keyword Requirements</h4>
              <div className="grid gap-2 sm:grid-cols-2">
                {selectedJob.tags.map((tag) => (
                  <div key={tag} className="flex items-center gap-2 px-3 py-2 bg-background border border-border rounded-xl">
                    <CheckCircle className="h-4 w-4 text-white flex-shrink-0" />
                    <span className="text-foreground font-bold text-[11px]">{tag}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* Context C: General Operational Workflow Parameters */}
            <div className="space-y-2 border-t border-border/40 pt-5">
              <h4 className="text-xs font-black text-foreground uppercase tracking-wide">Key Candidate Responsibilities</h4>
              <ul className="list-disc pl-4 space-y-1.5 text-muted-foreground font-medium">
                <li>Drive development sprints across critical user paths using scalable technical architecture patterns.</li>
                <li>Write modular, performant, and type-safe front-end scripts bound to asynchronous API states.</li>
                <li>Coordinate directly with server operations teams to deploy isolated virtualization images onto cloud instances.</li>
                <li>Conduct deep profile diagnostics on database lookup arrays to trace runtime bottlenecks.</li>
              </ul>
            </div>
          </div>
        </div>

      </div>
    </div>
  );
}

// Minimal supporting layout vector glyph handle representation component
function ChevronRight(props: React.SVGProps<SVGSVGElement>) {
  return (
    <svg className={props.className} fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M9 5l7 7-7 7" />
    </svg>
  );
}