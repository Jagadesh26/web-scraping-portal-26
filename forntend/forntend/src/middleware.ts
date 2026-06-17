import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

const PUBLIC_ROUTES = [
  "/login",
  "/register",
  "/forgot-password",
  "/reset-password",
  "/verify-email"
];

const PROTECTED_ROUTE_PREFIXES = [
  "/dashboard",
  "/profile",
  "/resume",
  "/jobs",
  "/ats",
  "/settings"
];

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;
  
  // Extract state flag cookie directly from edge header params
  const hasSession = request.cookies.has("talentai_has_session");

  const isPublicRoute = PUBLIC_ROUTES.some((route) => pathname.startsWith(route));
  const isProtectedRoute = PROTECTED_ROUTE_PREFIXES.some((prefix) => pathname.startsWith(prefix));

  // Case A: Authenticated user attempting access to public onboarding fields -> Redirect to app
  if (hasSession && isPublicRoute) {
    return NextResponse.redirect(new URL("/dashboard", request.url));
  }

  // Case B: Unauthenticated request attempting access inside protected scope matrices -> Drop back to login
  if (!hasSession && isProtectedRoute) {
    const loginUrl = new URL("/login", request.url);
    loginUrl.searchParams.set("callbackUrl", pathname);
    return NextResponse.redirect(loginUrl);
  }

  return NextResponse.next();
}

export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - api (API routes handlers)
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     */
    "/((?!api|_next/static|_next/image|favicon.ico).*)",
  ],
};