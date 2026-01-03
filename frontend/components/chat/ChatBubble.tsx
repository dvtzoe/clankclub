"use client";

import { useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkMath from "remark-math";
import remarkGfm from "remark-gfm";
import rehypeKatex from "rehype-katex";
import rehypeRaw from "rehype-raw";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { oneDark } from "react-syntax-highlighter/dist/esm/styles/prism";
import "katex/dist/katex.min.css";
import { Card, CardContent } from "@/components/ui/card";
import { Avatar } from "@/components/ui/avatar";
import Attachment from "@/components/chat/Attachment";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import { Button } from "@/components/ui/button";
import { ButtonGroup } from "@/components/ui/button-group";
import {
  Tooltip,
  TooltipContent,
  TooltipTrigger,
} from "@/components/ui/tooltip";

import { User, Copy, Check, RotateCcw, AtSign } from "lucide-react";

function CodeBlock({ children, language }: { children: string; language: string }) {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    await navigator.clipboard.writeText(children);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="relative group">
      <button
        onClick={handleCopy}
        className="absolute right-2 top-2 p-2 rounded-md bg-gray-700 hover:bg-gray-600 text-gray-300 opacity-0 group-hover:opacity-100 transition-opacity z-10"
        title="Copy code"
      >
        {copied ? <Check size={16} /> : <Copy size={16} />}
      </button>
      <SyntaxHighlighter
        style={oneDark}
        language={language}
        PreTag="div"
        showLineNumbers={language !== "text"}
        wrapLongLines
      >
        {children}
      </SyntaxHighlighter>
    </div>
  );
}

export default function ChatBubble({
  message,
  isUser,
  attachments,
  loading,
}: Readonly<{
  message?: string;
  isUser?: boolean;
  attachments?: { id: string, name: string }[],
  loading?: boolean;
}>) {
  if (isUser) {
    return (
      <div className="w-full flex flex-row justify-end">
        <Card size="sm" className="max-w-[80%]">
          <CardContent className="flex flex-row-reverse">
            <Avatar size="lg" className="flex justify-center content-center"><User className="my-auto" /></Avatar>
            <div className="flex flex-col my-auto mr-4 gap-2">
              <div className="text-right whitespace-pre-wrap break-words">
                {message}
              </div>
              <div className="flex flex-row justify-end mt-2 gap-1">
                {attachments && attachments.length > 0 && attachments.map(attachment => (
                  <Attachment key={attachment.id} id={attachment.id} name={attachment.name} />
                ))}
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    )
  } else {
    if (loading) {
      return (
        <div className="w-full p-4 animate-pulse">
          Clankers are discussing...
        </div>
      )
    } else {
      const [copied, setCopied] = useState(false);

      const handleCopyMessage = async () => {
        await navigator.clipboard.writeText(message || "");
        setCopied(true);
        setTimeout(() => setCopied(false), 2000);
      };

      return (
        <div className="w-full p-4 justify-start max-w-[95%] prose prose-sm dark:prose-invert prose-pre:p-0 prose-pre:m-0 prose-code:before:content-none prose-code:after:content-none overflow-x-auto hover:bg-gray-900/60 transition-all rounded-2xl">
          <div className="font-semibold text-gray-200">ClankClub discussion results:</div>
          <ReactMarkdown
            remarkPlugins={[remarkMath, remarkGfm]}
            rehypePlugins={[rehypeKatex, rehypeRaw]}
            components={{
              code(props) {
                const { children, className, node, ...rest } = props;
                const match = /language-(\w+)/.exec(className || "");
                const inline = !match && !String(children).includes("\n");
                const codeString = String(children).replace(/\n$/, "");

                return !inline && match ? (
                  <CodeBlock language={match[1]}>{codeString}</CodeBlock>
                ) : !inline ? (
                  <CodeBlock language="text">{codeString}</CodeBlock>
                ) : (
                  <code
                    className={`${className || ""} bg-gray-200 dark:bg-gray-700 px-1 py-0.5 rounded text-sm`}
                    {...rest}
                  >
                    {children}
                  </code>
                );
              },
              a({ href, children }) {
                return (
                  <a
                    href={href}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-blue-500 hover:underline"
                  >
                    {children}
                  </a>
                );
              },
              table({ children }) {
                return (
                  <div className="overflow-x-auto my-4">
                    <Table>
                      {children}
                    </Table>
                  </div>
                );
              },
              thead({ children }) {
                return <TableHeader>{children}</TableHeader>;
              },
              tbody({ children }) {
                return <TableBody>{children}</TableBody>;
              },
              tr({ children }) {
                return <TableRow>{children}</TableRow>;
              },
              th({ children }) {
                return <TableHead>{children}</TableHead>;
              },
              td({ children }) {
                return <TableCell>{children}</TableCell>;
              },
              h1({ children }) {
                return <h1 className="text-3xl font-bold mt-6 mb-4">{children}</h1>;
              },
              h2({ children }) {
                return <h2 className="text-2xl font-bold mt-5 mb-3">{children}</h2>;
              },
              h3({ children }) {
                return <h3 className="text-xl font-bold mt-4 mb-2">{children}</h3>;
              },
              h4({ children }) {
                return <h4 className="text-lg font-bold mt-3 mb-2">{children}</h4>;
              },
              h5({ children }) {
                return <h5 className="text-base font-bold mt-2 mb-1">{children}</h5>;
              },
              h6({ children }) {
                return <h6 className="text-sm font-bold mt-2 mb-1">{children}</h6>;
              },
              ul({ children }) {
                return <ul className="list-disc list-inside my-2 space-y-1">{children}</ul>;
              },
              ol({ children }) {
                return <ol className="list-decimal list-inside my-2 space-y-1">{children}</ol>;
              },
              li({ children }) {
                return <li className="ml-4">{children}</li>;
              },
              blockquote({ children }) {
                return (
                  <blockquote className="border-l-4 border-gray-300 dark:border-gray-600 pl-4 my-4 italic text-gray-700 dark:text-gray-300">
                    {children}
                  </blockquote>
                );
              },
              hr() {
                return <hr className="my-6 border-gray-300 dark:border-gray-600" />;
              },
              p({ children }) {
                return <p className="my-2">{children}</p>;
              },
            }}
          >
            {message || ""}
          </ReactMarkdown>
          <div>
            <ButtonGroup>
              <Tooltip>
                <TooltipTrigger asChild>
                  <Button size="icon-sm" variant="ghost">
                    <RotateCcw />
                  </Button>
                </TooltipTrigger>
                <TooltipContent>
                  <p>Regenerate Response</p>
                </TooltipContent>
              </Tooltip>
              <Tooltip>
                <TooltipTrigger asChild>
                  <Button size="icon-sm" variant="ghost">
                    <AtSign />
                  </Button>
                </TooltipTrigger>
                <TooltipContent>
                  <p>Mention this message</p>
                </TooltipContent>
              </Tooltip>
              <Tooltip>
                <TooltipTrigger asChild>
                  <Button size="icon-sm" variant="ghost" onClick={handleCopyMessage}>
                    {copied ? <Check /> : <Copy />}
                  </Button>
                </TooltipTrigger>
                <TooltipContent>
                  <p>{copied ? "Copied!" : "Copy to Clipboard"}</p>
                </TooltipContent>
              </Tooltip>
            </ButtonGroup>
          </div>
        </div>
      )
    }
  }
}