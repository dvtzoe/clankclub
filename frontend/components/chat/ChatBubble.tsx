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
} from "@/components/ui/table";
import { Button } from "@/components/ui/button";
import { ButtonGroup } from "@/components/ui/button-group";
import {
  Tooltip,
  TooltipContent,
  TooltipTrigger,
} from "@/components/ui/tooltip";

import { User, Copy, Check, RotateCcw, AtSign } from "lucide-react";
import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from "@/components/ui/collapsible";

function CodeBlock({ children, language }: { children: string; language: string }) {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(children);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (e) {
      // ignore copy errors silently
    }
  };

  return (
    <div className="relative group rounded-md overflow-hidden border border-gray-700">
      <button
        onClick={handleCopy}
        aria-label={copied ? "Copied code" : "Copy code"}
        className="absolute right-2 top-2 p-1 rounded-md bg-gray-800/80 hover:bg-gray-700 text-gray-200 opacity-0 group-hover:opacity-100 transition-opacity z-10 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
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
        className="text-sm bg-transparent"
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
  confidence,
  opinions,
}: Readonly<{
  message?: string;
  isUser?: boolean;
  attachments?: { id: string; name: string }[];
  loading?: boolean;
  confidence?: number;
  opinions?: { model: string; opinion: string }[];
}>) {
  if (isUser) {
    return (
      <div className="w-full flex flex-row justify-end">
        <Card size="sm" className="max-w-[80%]">
          <CardContent className="flex flex-row-reverse">
            <Avatar size="lg" className="flex justify-center content-center"><User className="my-auto" /></Avatar>
            <div className="flex flex-col my-auto mr-4 gap-2">
              <div className="text-right whitespace-pre-wrap wrap-break-words">
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
    );
  } else {
    if (loading) {
      return (
        <div className="w-full p-4 animate-pulse text-gray-400">
          Clankers are discussing...
        </div>
      );
    } else {
      const [copied, setCopied] = useState(false);

      const handleCopyMessage = async () => {
        try {
          await navigator.clipboard.writeText(message || "");
          setCopied(true);
          setTimeout(() => setCopied(false), 2000);
        } catch (e) {
          // ignore
        }
      };

      return (
        <div className="w-full p-6 justify-start max-w-[95%] prose prose-sm dark:prose-invert prose-pre:p-0 prose-pre:m-0 prose-code:before:content-none prose-code:after:content-none overflow-x-auto hover:bg-gray-900/60 transition-all rounded-2xl">
          <div className="mb-3 flex items-center gap-3">
            <Avatar size="sm" className="shrink-0">
              <User className="text-gray-300" />
              <span className="sr-only">ClankClub</span>
            </Avatar>
            <div className="flex items-center gap-2">
              <h5 className="m-0 text-sm font-semibold text-gray-200">ClankClub</h5>
              {typeof confidence === "number" && (
                <span className="text-xs font-medium bg-gray-800 text-gray-200 px-2 py-0.5 rounded-full">
                  {(confidence * 100).toFixed(0)}% confident
                </span>
              )}
            </div>
          </div>

          <Collapsible>
            <CollapsibleTrigger asChild>
              <Button
                className="font-semibold text-gray-200 bg-gray-800/60 hover:bg-gray-800"
                aria-expanded={false}
              >
                Discussion details
              </Button>
            </CollapsibleTrigger>
            <CollapsibleContent className="mt-3">
              <Card>
                <CardContent>
                  <div className="flex flex-col gap-3">
                    {opinions && opinions.length > 0 ? (
                      opinions.map((opinion, index) => (
                        <div
                          key={index}
                          className="flex flex-col gap-2 p-3 border border-gray-700 rounded-lg bg-gray-50/5"
                        >
                          <h6 className="font-semibold text-gray-300">{opinion.model}</h6>
                          <p className="my-0! text-sm text-gray-200">{opinion.opinion}</p>
                        </div>
                      ))
                    ) : (
                      <p className="text-sm text-gray-400">No additional opinions available.</p>
                    )}
                  </div>
                </CardContent>
              </Card>
            </CollapsibleContent>
          </Collapsible>

          <div className="mt-3">
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
                    <a href={href} target="_blank" rel="noopener noreferrer" className="text-blue-400 hover:underline">
                      {children}
                    </a>
                  );
                },
                table({ children }) {
                  return (
                    <div className="overflow-x-auto my-4 rounded">
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
                  return <h1 className="text-3xl font-bold mt-6 mb-4 text-gray-100">{children}</h1>;
                },
                h2({ children }) {
                  return <h2 className="text-2xl font-bold mt-5 mb-3 text-gray-100">{children}</h2>;
                },
                h3({ children }) {
                  return <h3 className="text-xl font-bold mt-4 mb-2 text-gray-100">{children}</h3>;
                },
                h4({ children }) {
                  return <h4 className="text-lg font-bold mt-3 mb-2 text-gray-100">{children}</h4>;
                },
                h5({ children }) {
                  return <h5 className="text-base font-bold mt-2 mb-1 text-gray-100">{children}</h5>;
                },
                h6({ children }) {
                  return <h6 className="text-sm font-bold mt-2 mb-1 text-gray-100">{children}</h6>;
                },
                ul({ children }) {
                  return <ul className="list-disc list-inside space-y-1">{children}</ul>;
                },
                ol({ children }) {
                  return <ol className="list-decimal list-inside my-2 space-y-1">{children}</ol>;
                },
                li({ children }) {
                  return <li>{children}</li>;
                },
                blockquote({ children }) {
                  return (
                    <blockquote className="border-l-4 border-gray-600 pl-4 my-4 italic text-gray-300">
                      {children}
                    </blockquote>
                  );
                },
                hr() {
                  return <hr className="my-6 border-gray-700" />;
                },
                p({ children }) {
                  return <p className="my-2 text-gray-200">{children}</p>;
                },
              }}
            >
              {message || ""}
            </ReactMarkdown>
          </div>

          <div className="mt-4 border-t border-gray-700 pt-3 flex justify-between items-center">
            <div>
              <ButtonGroup>
                <Tooltip>
                  <TooltipTrigger asChild>
                    <Button size="icon-sm" variant="ghost" aria-label="Regenerate response">
                      <RotateCcw />
                    </Button>
                  </TooltipTrigger>
                  <TooltipContent>
                    <p>Regenerate Response</p>
                  </TooltipContent>
                </Tooltip>
                <Tooltip>
                  <TooltipTrigger asChild>
                    <Button size="icon-sm" variant="ghost" aria-label="Mention message">
                      <AtSign />
                    </Button>
                  </TooltipTrigger>
                  <TooltipContent>
                    <p>Mention this message</p>
                  </TooltipContent>
                </Tooltip>
                <Tooltip>
                  <TooltipTrigger asChild>
                    <Button size="icon-sm" variant="ghost" onClick={handleCopyMessage} aria-label="Copy message">
                      {copied ? <Check /> : <Copy />}
                    </Button>
                  </TooltipTrigger>
                  <TooltipContent>
                    <p>{copied ? "Copied!" : "Copy to Clipboard"}</p>
                  </TooltipContent>
                </Tooltip>
              </ButtonGroup>
            </div>
            <div className="text-xs text-gray-400">&nbsp;</div>
          </div>
        </div>
      );
    }
  }
}

