"use client";
import Link from 'next/link';

export function Footer() {
  return (
    <footer className="border-t bg-gray-50 mt-auto">
      <div className="container mx-auto px-4 py-6">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div>
            <h3 className="font-bold text-lg mb-3">🎯 Job Hunter AI</h3>
            <p className="text-sm text-gray-600">Automatisez votre recherche d'emploi avec l'IA</p>
          </div>
          <div>
            <h4 className="font-semibold mb-3">Produit</h4>
            <ul className="space-y-2 text-sm">
              <li><Link href="/jobs" className="text-gray-600 hover:text-primary">Recherche d'emploi</Link></li>
              <li><Link href="/companies/watch" className="text-gray-600 hover:text-primary">Veille entreprise</Link></li>
              <li><Link href="/documents" className="text-gray-600 hover:text-primary">Documents générés</Link></li>
            </ul>
          </div>
          <div>
            <h4 className="font-semibold mb-3">Support</h4>
            <ul className="space-y-2 text-sm">
              <li><Link href="/profile" className="text-gray-600 hover:text-primary">Mon profil</Link></li>
              <li><a href="mailto:support@jobhunterai.com" className="text-gray-600 hover:text-primary">Contact</a></li>
            </ul>
          </div>
          <div>
            <h4 className="font-semibold mb-3">Ressources</h4>
            <ul className="space-y-2 text-sm">
              <li><a href="https://github.com/yourusername/jobhunter" target="_blank" rel="noopener noreferrer" className="text-gray-600 hover:text-primary">GitHub</a></li>
              <li><Link href="/applications" className="text-gray-600 hover:text-primary">Mes candidatures</Link></li>
            </ul>
          </div>
        </div>
        <div className="mt-8 pt-6 border-t text-center text-sm text-gray-600">
          <p>© {new Date().getFullYear()} Job Hunter AI. Développé avec ❤️ par votre équipe</p>
        </div>
      </div>
    </footer>
  );
}
