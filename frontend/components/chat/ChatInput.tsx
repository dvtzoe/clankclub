import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { ButtonGroup } from "@/components/ui/button-group";
import { Textarea } from "@/components/ui/textarea";
import { Card, CardContent } from "@/components/ui/card";

import { Send, Paperclip } from "lucide-react";

export default async function ChatInput() {
  return (
    <div className="w-full">
      <Card size="sm" className="border-t">
        <form>
          <CardContent className="space-y-2">
            <Textarea />
            <div className="flex flex-row justify-between">
              <Button variant="ghost">
                <Paperclip /> Attact File
              </Button>
              <Button type="submit" size="icon">
                <Send />
              </Button>
            </div>
          </CardContent>

        </form>
      </Card>
    </div>
  );
}