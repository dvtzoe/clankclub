import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";

import Link from "next/link";

export default async function Topbar({ showLogo }: Readonly<{ showLogo?: boolean }>) {
  return (
    <>
      <div
        className="fixed inset-x-0 top-0 h-8 pointer-events-none z-30"
        style={{
          backdropFilter: 'blur(24px)',
          WebkitBackdropFilter: 'blur(24px)',
          maskImage: 'linear-gradient(to bottom, black 0%, transparent 100%)',
          WebkitMaskImage: 'linear-gradient(to bottom, black 0%, transparent 100%)'
        }}
      />
      <div
        className="fixed inset-x-0 top-0 h-32 pointer-events-none z-30 bg-linear-to-b from-primary/40 via-primary/20 via-30% to-transparent"
      />
      <div className="w-full top-0 sticky px-4 pt-2 flex flex-row justify-between z-40">
        { showLogo && <Link href="/" className="font-bold my-auto">ClankClub</Link> }
        <Avatar>
          <AvatarFallback>U</AvatarFallback>
        {/* Auth component to be added here */}
        </Avatar>
      </div>
    </>
  )
}