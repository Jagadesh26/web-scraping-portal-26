// src/app/page.tsx
export default function CoreLandingPage() {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-background text-foreground px-4">
      <main className="max-w-md text-center space-y-4">
        <div className="inline-flex items-center justify-center p-2 bg-primary/10 rounded-xl text-primary mb-2">
          <svg className="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
          </svg>
        </div>
        <h1 className="text-3xl font-bold tracking-tight sm:text-4xl">
          Platform Architecture Ready
        </h1>
        <p className="text-muted-foreground text-sm sm:text-base">
          Next.js 15, TanStack Query, Zustand, Axios, and Tailwind CSS foundations are fully bound and ready for development.
        </p>
      </main>
    </div>
  );
}