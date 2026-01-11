// typescript
// File: frontend/proxy.ts

import { withAuth } from "next-auth/middleware";
import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

export default withAuth(
  (req: NextRequest) => {
    const { pathname } = req.nextUrl;

    if (
      pathname.startsWith("/api/auth") ||
      pathname.startsWith("/_next") ||
      pathname.startsWith("/static") ||
      pathname === "/favicon.ico" ||
      pathname.includes(".")
    ) {
      return NextResponse.next();
    }

    const isProtected =
      pathname.startsWith("/chat") || pathname.startsWith("/discussions");

    const token = (req as any).nextauth?.token;
    const isLoggedIn = !!token;

    if (isProtected && !isLoggedIn) {
      const loginUrl = new URL("/login", req.url);

      const original = req.nextUrl.clone();
      original.searchParams.delete("callbackUrl");
      const callbackPath = original.pathname + original.search;

      if (callbackPath && callbackPath !== "/") {
        loginUrl.searchParams.set("callbackUrl", callbackPath);
      }

      return NextResponse.redirect(loginUrl);
    }

    return NextResponse.next();
  },
  {
    callbacks: {
      authorized: ({ token }) => !!token,
    },
  }
);

export const config = {
  matcher: ["/chat/:path*", "/discussions/:path*"],
};
