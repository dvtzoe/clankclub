import { Button } from "@/components/ui/button";

import { SquarePen } from "lucide-react";

export default function ChatTitle({ title }: Readonly<{ title: string }>) {
  return (
    <div className="fixed top-0 z-50 text-center max-w-4xl w-full pt-2 h-12 font-bold text-gray-300 flex flex-row justify-center pointer-events-none">
      <div className="flex flex-row backdrop-blur-sm px-4 rounded-full">
        <span className="my-auto">{title}</span>
        <Button variant="ghost" size="icon" className="ml-2 my-auto">
          <SquarePen />
        </Button>
      </div>
    </div>
  )
}