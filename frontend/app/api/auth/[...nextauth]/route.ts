import NextAuth from "next-auth"
import Credentials from "next-auth/providers/credentials"
import type { NextAuthOptions } from "next-auth"
import type { JWT } from "next-auth/jwt"
import type { Session as NextAuthSession } from "next-auth"

const options: NextAuthOptions = {
  providers: [
    Credentials({
      name: "Credentials",
      credentials: {
        email: { label: "Email", type: "email" },
        password: { label: "Password", type: "password" },
      },
      async authorize(credentials) {
        if (!credentials) return null
        const res = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/api/auth/login`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            email: credentials.email,
            password: credentials.password,
          }),
        })

        if (!res.ok) return null
        const user = await res.json()
        return user
      },
    }),
  ],
  secret: process.env.NEXTAUTH_SECRET,
  pages: {
    signIn: "/login",
  },
  callbacks: {
    async jwt({ token, user }: { token: JWT; user?: any }) {
      if (user) (token as any).user = user
      return token
    },
    async session({ session, token }: { session: NextAuthSession; token: JWT }) {
      if ((token as any).user) session.user = (token as any).user
      return session
    },
  },
}

const handler = NextAuth(options)

export { handler as GET, handler as POST }