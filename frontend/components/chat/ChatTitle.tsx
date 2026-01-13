import { ButtonGroup } from "@/components/ui/button-group";
import { Button } from "@/components/ui/button";

import { SquarePen, Share2 } from "lucide-react";

export default function ChatTitle({ title }: Readonly<{ title: string }>) {
  return (
    <div className="fixed top-0 z-50 text-center max-w-4xl w-full pt-2 h-12 font-bold text-gray-300 flex flex-row justify-center pointer-events-none">
      <div className="flex flex-row backdrop-blur-sm px-4 rounded-full">
        <span className="my-auto">{title}</span>
        <ButtonGroup className="ml-2 my-auto">
          <Button variant="ghost" size="icon">
            <SquarePen />
          </Button>
          <Button variant="ghost" size="icon">
            <Share2 />
          </Button>
        </ButtonGroup>

      </div>
    </div>
  )
}