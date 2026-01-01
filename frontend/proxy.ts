import { auth } from "@/lib/auth";
import { NextRequest, NextResponse } from "next/server";

export default auth((req: NextRequest & { auth?: unknown }) => {
  const isLoggedIn = !!req.auth
  const isOnDashboard = req.nextUrl.pathname.startsWith("/chat") ||
    req.nextUrl.pathname.startsWith("/discussions");
  const isOnAuth = req.nextUrl.pathname === "/login" ||
    req.nextUrl.pathname === "/register";

  if (!isLoggedIn && isOnDashboard) {
    return NextResponse.redirect(new URL("/login", req.url));
  }

  if (isLoggedIn && isOnAuth) {
    return NextResponse.redirect(new URL("/chat", req.url));
  }

  return NextResponse.next();
})

export const config = {
  matcher: ["/((?!api|_next/static|_next/image|favicon.ico).*)"],
}