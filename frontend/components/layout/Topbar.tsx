"use client";

import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { SidebarTrigger, useSidebar } from "@/components/ui/sidebar";
import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { ButtonGroup } from "@/components/ui/button-group";
import { Tooltip, TooltipContent, TooltipTrigger } from "@/components/ui/tooltip";

import Link from "next/link";
import { HatGlasses, Plus } from "lucide-react";

export default function Topbar() {
  const { open } = useSidebar()

  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    // Trigger reveal animation after mount
    const timer = setTimeout(() => setMounted(true), 50);
    return () => clearTimeout(timer);
  }, []);

  return (
    <>
      <div
        className={"fixed top-0 right-0 h-16 pointer-events-none z-30 transition-all duration-300 ease-in-out" + (open ? " left-64" : " left-0")}
        style={{
          backdropFilter: 'blur(24px)',
          WebkitBackdropFilter: 'blur(24px)',
          maskImage: 'linear-gradient(to bottom, black 0%, transparent 100%)',
          WebkitMaskImage: 'linear-gradient(to bottom, black 0%, transparent 100%)',
          opacity: mounted ? 1 : 0,
          transform: mounted ? 'translateY(0)' : 'translateY(-100%)',
        }}
      />
      <div
        className={"fixed top-0 right-0 h-16 pointer-events-none z-30 bg-linear-to-b from-primary/40 via-primary/20 via-30% to-transparent transition-all duration-300 ease-in-out" + (open ? " left-64" : " left-0")}
        style={{
          opacity: mounted ? 1 : 0,
          transform: mounted ? 'translateY(0)' : 'translateY(-100%)',
        }}
      />
      <div className="w-full top-0 sticky px-4 pt-2 flex flex-row justify-between z-40 h-12">
          <div className="flex flex-row">
            <SidebarTrigger className="mr-4 my-auto" />
            {!open && (
              <Link
                href="/"
                className="font-bold my-auto transition-all duration-300 ease-in-out"
                style={{
                  opacity: mounted ? 1 : 0,
                  transform: mounted ? 'translateX(0)' : 'translateX(-20px)',
                }}
              >
                ClankClub
              </Link>
            )}
          </div>
        <div />
        <div className="flex flex-row gap-2">
          { !open && (
            <ButtonGroup className="w-full my-auto">
              <Tooltip>
                <TooltipTrigger asChild>
                  <Button className="grow"><Plus/> New</Button>
                </TooltipTrigger>
                <TooltipContent>Create New Chat</TooltipContent>
              </Tooltip>
              <Tooltip>
                <TooltipTrigger asChild>
                  <Button variant="secondary" size="icon"><HatGlasses/></Button>
                </TooltipTrigger>
                <TooltipContent>Private Mode</TooltipContent>
              </Tooltip>
            </ButtonGroup>
          )}
          <Avatar className="my-auto">
            <AvatarFallback>U</AvatarFallback>
            {/* Auth component to be added here */}
          </Avatar>
        </div>
      </div>
    </>
  )
}
