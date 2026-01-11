import Link from "next/link";
import {
  File,
  FileImage,
  FileText,
  FileVideo,
  FileAudio,
  FileCode,
  FileArchive,
  FileSpreadsheet,
} from "lucide-react";

function getFileIcon(filename: string) {
  const ext = filename.split(".").pop()?.toLowerCase() || "";

  const iconMap: Record<string, React.ElementType> = {
    // Images
    jpg: FileImage,
    jpeg: FileImage,
    png: FileImage,
    gif: FileImage,
    svg: FileImage,
    webp: FileImage,
    // Documents
    pdf: FileText,
    doc: FileText,
    docx: FileText,
    txt: FileText,
    // Video
    mp4: FileVideo,
    mov: FileVideo,
    avi: FileVideo,
    webm: FileVideo,
    // Audio
    mp3: FileAudio,
    wav: FileAudio,
    ogg: FileAudio,
    // Code
    js: FileCode,
    ts: FileCode,
    jsx: FileCode,
    tsx: FileCode,
    html: FileCode,
    css: FileCode,
    json: FileCode,
    // Archives
    zip: FileArchive,
    rar: FileArchive,
    tar: FileArchive,
    gz: FileArchive,
    // Spreadsheets
    xls: FileSpreadsheet,
    xlsx: FileSpreadsheet,
    csv: FileSpreadsheet,
  };

  return iconMap[ext] || File;
}

export default function Attachment({
                                           id,
                                           name,
                                         }: Readonly<{
  id: string;
  name: string;
}>) {
  const Icon = getFileIcon(name);

  return (
    <Link className="border py-2 px-4 rounded-xl min-w-48 w-fit bg-blue-950/50 hover:bg-blue-950/30 hover:shadow-xl transition-all flex items-center gap-2" href={`/api/attachments/${id}`}>
      <Icon className="h-4 w-4" />
      <div className="flex flex-col">
        <span className="text-sm font-medium truncate">{name}</span>
        <span className="text-xs text-gray-200 truncate">{id}</span>
      </div>
    </Link>
  );
}
