"use client";
import { useAuth } from '@/contexts/AuthContext';
import { usePathname } from 'next/navigation';
import { Navbar } from './Navbar';
import { Sidebar } from './Sidebar';
import { Footer } from './Footer';

export function AppShell({ children }: { children: React.ReactNode }) {
  const { isAuthenticated } = useAuth();
  const pathname = usePathname();

  // Pages publiques qui ne doivent PAS avoir la structure Dashboard (Navbar/Sidebar)
  const publicPages = ['/', '/auth/login', '/auth/register'];
  const isPublicPage = publicPages.includes(pathname);

  // Si page publique OU utilisateur non authentifié → pas de structure Dashboard
  if (!isAuthenticated || isPublicPage) {
    return <>{children}</>;
  }

  // Sinon → structure Dashboard complète (Navbar + Sidebar)
  return (
    <div className="flex flex-col h-screen bg-gray-50 overflow-hidden">
      <Navbar />
      <div className="flex flex-1 overflow-hidden">
        <Sidebar />
        <main className="flex-1 overflow-y-auto">
          <div className="container mx-auto p-4 lg:p-6 max-w-screen-2xl">
            {children}
          </div>
          <Footer />
        </main>
      </div>
    </div>
  );
}
