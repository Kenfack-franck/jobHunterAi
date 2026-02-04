"use client";
import { useState, useEffect } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { cn } from '@/lib/utils';
import { Home, Search, Briefcase, FileText, Eye, Settings, ChevronLeft, ChevronRight, Building2, HelpCircle, Shield } from 'lucide-react';

const navItems = [
  { href: '/dashboard', label: 'Accueil', icon: Home },
  { href: '/jobs', label: 'Recherche', icon: Search },
  { href: '/settings/sources', label: 'Sources', icon: Building2 },
  { href: '/profile', label: 'Mon Profil', icon: Briefcase },
  { href: '/documents', label: 'Documents', icon: FileText },
  { href: '/applications', label: 'Candidatures', icon: Eye },
  { href: '/settings', label: 'Paramètres', icon: Settings },
  { href: '/help', label: 'Aide', icon: HelpCircle },
];

export function Sidebar() {
  const [collapsed, setCollapsed] = useState(false);
  const [isAdmin, setIsAdmin] = useState(false);
  const pathname = usePathname();

  useEffect(() => {
    // Vérifier si l'utilisateur est admin via le token
    try {
      const token = localStorage.getItem('auth_token');
      if (token) {
        const payload = JSON.parse(atob(token.split('.')[1]));
        setIsAdmin(payload.role === 'admin');
      }
    } catch (error) {
      console.error('Error checking admin role:', error);
    }
  }, []);

  return (
    <aside className={cn(
      "h-full border-r bg-white transition-all duration-300 hidden lg:block shrink-0 flex-none",
      collapsed ? "w-16" : "w-64"
    )}>
      <div className="flex flex-col h-full">
        {/* Navigation */}
        <nav className="flex-1 p-2 space-y-1 overflow-y-auto">
          {/* Admin link si utilisateur est admin */}
          {isAdmin && (
            <Link
              href="/admin"
              className={cn(
                "flex items-center gap-3 px-3 py-2 rounded-lg transition-colors",
                pathname?.startsWith('/admin') 
                  ? "bg-gradient-to-r from-purple-600 to-pink-600 text-white shadow-lg" 
                  : "text-purple-700 bg-purple-50 hover:bg-purple-100 border-2 border-purple-200",
                collapsed && "justify-center"
              )}
              title={collapsed ? "Admin" : undefined}
            >
              <Shield className="h-5 w-5 flex-shrink-0" />
              {!collapsed && <span className="text-sm font-bold">Admin Panel</span>}
            </Link>
          )}
          
          {navItems.map((item) => {
            // Éviter que /settings soit actif quand on est sur /settings/sources
            const isActive = pathname === item.href || 
              (pathname?.startsWith(item.href + '/') && item.href !== '/settings');
            const Icon = item.icon;
            return (
              <Link
                key={item.href}
                href={item.href}
                className={cn(
                  "flex items-center gap-3 px-3 py-2 rounded-lg transition-colors",
                  isActive ? "bg-primary text-white" : "text-gray-700 hover:bg-gray-100",
                  collapsed && "justify-center"
                )}
                title={collapsed ? item.label : undefined}
              >
                <Icon className="h-5 w-5 flex-shrink-0" />
                {!collapsed && <span className="text-sm font-medium">{item.label}</span>}
              </Link>
            );
          })}
        </nav>

        {/* Toggle Button */}
        <div className="p-2 border-t shrink-0">
          <button
            onClick={() => setCollapsed(!collapsed)}
            className="w-full flex items-center justify-center p-2 rounded-lg hover:bg-gray-100 transition-colors"
            aria-label={collapsed ? "Expand sidebar" : "Collapse sidebar"}
          >
            {collapsed ? <ChevronRight className="h-5 w-5" /> : <ChevronLeft className="h-5 w-5" />}
          </button>
        </div>
      </div>
    </aside>
  );
}
