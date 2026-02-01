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
              <li><span className="text-gray-400 cursor-not-allowed">Fonctionnalités</span></li>
              <li><span className="text-gray-400 cursor-not-allowed">Tarifs</span></li>
            </ul>
          </div>
          <div>
            <h4 className="font-semibold mb-3">Support</h4>
            <ul className="space-y-2 text-sm">
              <li><span className="text-gray-400 cursor-not-allowed">Aide</span></li>
              <li><a href="mailto:support@jobhunterai.com" className="text-gray-600 hover:text-primary">Contact</a></li>
            </ul>
          </div>
          <div>
            <h4 className="font-semibold mb-3">Légal</h4>
            <ul className="space-y-2 text-sm">
              <li><span className="text-gray-400 cursor-not-allowed">Confidentialité</span></li>
              <li><span className="text-gray-400 cursor-not-allowed">CGU</span></li>
            </ul>
          </div>
        </div>
        <div className="mt-8 pt-6 border-t text-center text-sm text-gray-600">
          <p>© {new Date().getFullYear()} Job Hunter AI. Tous droits réservés.</p>
        </div>
      </div>
    </footer>
  );
}
