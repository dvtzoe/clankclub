import {
  Sidebar,
  SidebarContent,
  SidebarGroup,
  SidebarGroupLabel,
  SidebarGroupContent,
  SidebarHeader,
  SidebarMenuItem,
  SidebarMenuButton,
  SidebarMenuAction
} from "@/components/ui/sidebar";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { Button } from "@/components/ui/button";
import { ButtonGroup } from "@/components/ui/button-group";
import { Tooltip, TooltipContent, TooltipTrigger } from "@/components/ui/tooltip";

import { Plus, HatGlasses, EllipsisVertical, SquarePen, Trash } from "lucide-react";

import Link from "next/link";

export default async function AppSidebar() {
  return (
    <Sidebar>
      <SidebarHeader>
        <Link href="/" className="font-bold ml-2 mt-1 z-50!">ClankClub</Link>
      </SidebarHeader>
      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupContent>
            <SidebarMenuItem className="px-2">
              <ButtonGroup className="w-full">
                <Tooltip>
                  <TooltipTrigger asChild>
                    <Button className="grow"><Plus /> New</Button>
                  </TooltipTrigger>
                  <TooltipContent>Create New Chat</TooltipContent>
                </Tooltip>
                <Tooltip>
                  <TooltipTrigger asChild>
                    <Button variant="secondary" size="icon"><HatGlasses /></Button>
                  </TooltipTrigger>
                  <TooltipContent>Private Mode</TooltipContent>
                </Tooltip>
              </ButtonGroup>
            </SidebarMenuItem>
          </SidebarGroupContent>
        </SidebarGroup>
        <SidebarGroup>
          <SidebarGroupLabel>Chats</SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenuItem>
              <SidebarMenuButton asChild>
                <Link href="/chat/1"><span>Example chat here</span></Link>
              </SidebarMenuButton>
              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <SidebarMenuAction><EllipsisVertical /></SidebarMenuAction>
                </DropdownMenuTrigger>
                <DropdownMenuContent side="right" align="start">
                  <DropdownMenuItem><SquarePen /> Rename</DropdownMenuItem>
                  <DropdownMenuItem variant="destructive"><Trash /> Delete</DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>
            </SidebarMenuItem>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>
    </Sidebar>
  );
}