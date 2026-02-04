"use client";
import { useState, useEffect } from 'react';
import Link from 'next/link';
import { useAuth } from '@/contexts/AuthContext';
import { useProfile } from '@/contexts/ProfileContext';
import { Button } from '@/components/ui/button';
import { Bell, HelpCircle, User, LogOut, Settings, Menu, Shield } from 'lucide-react';
import { 
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet";

export function Navbar() {
  const { user, logout } = useAuth();
  const { completion } = useProfile();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  return (
    <nav className="sticky top-0 z-50 w-full border-b bg-white shadow-sm">
      <div className="flex h-16 items-center px-4 lg:px-6 max-w-screen-2xl mx-auto">
        {/* Mobile Menu Button */}
        <Sheet open={mobileMenuOpen} onOpenChange={setMobileMenuOpen}>
          <SheetTrigger asChild>
            <Button variant="ghost" size="sm" className="lg:hidden mr-2">
              <Menu className="h-5 w-5" />
            </Button>
          </SheetTrigger>
          <SheetContent side="left" className="w-72 p-0">
            <MobileNav onClose={() => setMobileMenuOpen(false)} logout={logout} />
          </SheetContent>
        </Sheet>

        {/* Logo - avec menu déroulant */}
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <button className="flex items-center gap-2 mr-4 hover:opacity-80 transition-opacity">
              <span className="text-2xl">🎯</span>
              <span className="font-bold text-base lg:text-lg hidden sm:block">Job Hunter AI</span>
            </button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="start">
            <DropdownMenuItem asChild>
              <Link href="/" className="cursor-pointer">
                🏠 Page d'accueil
              </Link>
            </DropdownMenuItem>
            <DropdownMenuItem asChild>
              <Link href="/dashboard" className="cursor-pointer">
                📊 Dashboard
              </Link>
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>

        <div className="flex-1" />

        {/* Actions */}
        <div className="flex items-center gap-1 sm:gap-2">
          {/* Notifications */}
          <Button variant="ghost" size="sm" className="relative hidden sm:flex">
            <Bell className="h-5 w-5" />
            <span className="absolute top-1 right-1 h-2 w-2 bg-red-500 rounded-full" />
          </Button>

          {/* Help */}
          <Link href="/help" className="hidden sm:block">
            <Button variant="ghost" size="sm">
              <HelpCircle className="h-5 w-5" />
            </Button>
          </Link>

          {/* User Menu */}
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost" size="sm" className="flex items-center gap-2">
                <div className="h-8 w-8 rounded-full bg-primary/10 flex items-center justify-center">
                  <User className="h-4 w-4" />
                </div>
                <div className="hidden lg:block text-left">
                  <p className="text-sm font-medium truncate max-w-[120px]">
                    {user?.full_name || user?.email}
                  </p>
                  <p className="text-xs text-gray-500">Profil {completion}%</p>
                </div>
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end" className="w-56">
              <DropdownMenuLabel>Mon compte</DropdownMenuLabel>
              <DropdownMenuSeparator />
              <DropdownMenuItem asChild>
                <Link href="/profile" className="cursor-pointer">
                  <User className="mr-2 h-4 w-4" />
                  Mon profil
                </Link>
              </DropdownMenuItem>
              <DropdownMenuItem asChild>
                <Link href="/settings" className="cursor-pointer">
                  <Settings className="mr-2 h-4 w-4" />
                  Paramètres
                </Link>
              </DropdownMenuItem>
              <DropdownMenuSeparator />
              <DropdownMenuItem onClick={logout} className="text-red-600 cursor-pointer">
                <LogOut className="mr-2 h-4 w-4" />
                Déconnexion
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
      </div>
    </nav>
  );
}

function MobileNav({ onClose, logout }: { onClose: () => void; logout: () => void }) {
  const { user } = useAuth();
  const { completion } = useProfile();
  const [isAdmin, setIsAdmin] = useState(false);

  useEffect(() => {
    // Vérifier si l'utilisateur est admin
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
    <div className="flex flex-col h-full">
      {/* User Info */}
      <div className="p-6 border-b bg-gradient-to-br from-primary/5 to-primary/10">
        <div className="flex items-center gap-3">
          <div className="h-12 w-12 rounded-full bg-primary/20 flex items-center justify-center">
            <User className="h-6 w-6 text-primary" />
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-sm font-semibold truncate">{user?.full_name || user?.email}</p>
            <p className="text-xs text-gray-600">Profil {completion}% complété</p>
          </div>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 overflow-y-auto p-4">
        <div className="space-y-1">
          {/* Admin Panel si admin */}
          {isAdmin && (
            <Link href="/admin" onClick={onClose}>
              <div className="flex items-center gap-3 px-4 py-3 rounded-lg bg-gradient-to-r from-purple-600 to-pink-600 text-white shadow-lg mb-2">
                <Shield className="h-5 w-5" />
                <span className="text-sm font-bold">Admin Panel</span>
              </div>
            </Link>
          )}
          
          <MobileNavLink href="/dashboard" icon="📊" label="Dashboard" onClick={onClose} />
          <MobileNavLink href="/jobs" icon="🔍" label="Recherche d'offres" onClick={onClose} />
          <MobileNavLink href="/settings/sources" icon="🏢" label="Sources" onClick={onClose} />
          <MobileNavLink href="/profile" icon="👤" label="Mon Profil" onClick={onClose} />
          <MobileNavLink href="/documents" icon="📄" label="Documents" onClick={onClose} />
          <MobileNavLink href="/applications" icon="👁️" label="Candidatures" onClick={onClose} />
          <MobileNavLink href="/help" icon="❓" label="Aide" onClick={onClose} />
          <MobileNavLink href="/settings" icon="⚙️" label="Paramètres" onClick={onClose} />
        </div>
      </nav>

      {/* Logout Button */}
      <div className="p-4 border-t">
        <Button
          variant="outline"
          className="w-full justify-start text-red-600 hover:bg-red-50"
          onClick={() => {
            logout();
            onClose();
          }}
        >
          <LogOut className="mr-2 h-4 w-4" />
          Déconnexion
        </Button>
      </div>
    </div>
  );
}

function MobileNavLink({ href, icon, label, onClick }: { href: string; icon: string; label: string; onClick: () => void }) {
  return (
    <Link href={href} onClick={onClick}>
      <div className="flex items-center gap-3 px-4 py-3 rounded-lg hover:bg-gray-100 transition-colors">
        <span className="text-xl">{icon}</span>
        <span className="text-sm font-medium">{label}</span>
      </div>
    </Link>
  );
}
