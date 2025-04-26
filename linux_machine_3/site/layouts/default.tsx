import { Link } from "@heroui/link";

import { Head } from "./head";

import { Navbar } from "@/components/navbar";

export default function DefaultLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="relative flex flex-col h-screen">
      <div className='sticky text-2xl isolate bg-white/20 shadow-lg ring-1 ring-black/5 p-5 flex '>
        <h1>My Web Application</h1>
        <div className="flex w-1/3 justify-evenly items-center">
          <Link className="cursor-pointer">Home</Link>
          <Link className="cursor-pointer">About</Link>
          <Link className="cursor-pointer">Contact</Link>
          <Link className="cursor-pointer">Upload</Link>
        </div>
      </div>
      <main className="w-screen px-12 flex-grow pt-16 bg-[rgb(223,229,241)] ">
        {children}
      </main>
      <footer className="w-full flex items-center justify-center py-3">
      </footer>
    </div>
  );
}
