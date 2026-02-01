"use client"
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Loader2, Briefcase, MapPin, Building2, Wifi } from "lucide-react";

interface SearchBarProps {
  onSearch: (params: {
    keyword?: string;
    location?: string;
    job_type?: string;
    company_name?: string;
  }) => void;
  loading?: boolean;
}

export function SearchBar({ onSearch, loading }: SearchBarProps) {
  const [jobTitle, setJobTitle] = useState("");
  const [city, setCity] = useState("");
  const [workMode, setWorkMode] = useState("");
  const [jobType, setJobType] = useState("");
  const [companyName, setCompanyName] = useState("");

  const handleSearch = () => {
    // Construire le keyword: job title
    const keyword = jobTitle || undefined;
    
    // Construire la location: city ou work mode
    let location = undefined;
    if (workMode && workMode !== "all") {
      location = workMode; // "remote", "onsite", "hybrid"
    } else if (city) {
      location = city; // "Paris", "Lyon", etc.
    }
    
    onSearch({
      keyword,
      location,
      job_type: jobType || undefined,
      company_name: companyName || undefined,
    });
  };

  const handleReset = () => {
    setJobTitle("");
    setCity("");
    setWorkMode("");
    setJobType("");
    setCompanyName("");
    onSearch({});
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow-sm space-y-5">
      <div className="mb-3">
        <h2 className="text-xl font-bold mb-2 flex items-center gap-2">
          <Briefcase className="w-5 h-5 text-primary" />
          Recherche d&apos;offres d&apos;emploi
        </h2>
        <p className="text-sm text-gray-600">
          🌐 Recherche hybride : base de données locale + scraping Internet (RemoteOK)
        </p>
      </div>
      
      {/* Ligne 1: Poste + Entreprise */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            <Briefcase className="inline w-4 h-4 mr-1" />
            Intitulé du poste
          </label>
          <Input
            placeholder="Ex: Data Scientist, Développeur Python..."
            value={jobTitle}
            onChange={(e) => setJobTitle(e.target.value)}
            onKeyPress={(e) => e.key === "Enter" && handleSearch()}
            disabled={loading}
            className="h-11"
          />
          <p className="text-xs text-gray-500 mt-1.5">
            Le titre du poste que vous recherchez
          </p>
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            <Building2 className="inline w-4 h-4 mr-1" />
            Entreprise <span className="text-gray-400 font-normal">(optionnel)</span>
          </label>
          <Input
            placeholder="Ex: Google, Microsoft..."
            value={companyName}
            onChange={(e) => setCompanyName(e.target.value)}
            onKeyPress={(e) => e.key === "Enter" && handleSearch()}
            disabled={loading}
            className="h-11"
          />
          <p className="text-xs text-gray-500 mt-1.5">
            Filtrer par entreprise spécifique
          </p>
        </div>
      </div>

      {/* Ligne 2: Mode de travail + Ville */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            <Wifi className="inline w-4 h-4 mr-1" />
            Mode de travail
          </label>
          <select
            className="flex h-11 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring disabled:opacity-50"
            value={workMode}
            onChange={(e) => setWorkMode(e.target.value)}
            disabled={loading}
          >
            <option value="all">Tous les modes</option>
            <option value="remote">🏠 Télétravail / Remote</option>
            <option value="onsite">🏢 Présentiel / Sur site</option>
            <option value="hybrid">🔀 Hybride (Télétravail + Bureau)</option>
          </select>
          <p className="text-xs text-gray-500 mt-1.5">
            💡 Sélectionnez &quot;Télétravail&quot; pour plus de résultats
          </p>
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            <MapPin className="inline w-4 h-4 mr-1" />
            Ville / Région <span className="text-gray-400 font-normal">(optionnel)</span>
          </label>
          <Input
            placeholder="Ex: Paris, Lyon, Île-de-France..."
            value={city}
            onChange={(e) => setCity(e.target.value)}
            onKeyPress={(e) => e.key === "Enter" && handleSearch()}
            disabled={loading}
            className="h-11"
          />
          <p className="text-xs text-gray-500 mt-1.5">
            Laissez vide si &quot;Télétravail&quot; sélectionné
          </p>
        </div>
      </div>

      {/* Ligne 3: Type de contrat */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          📄 Type de contrat
        </label>
        <select
          className="flex h-11 w-full md:w-1/2 rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring disabled:opacity-50"
          value={jobType}
          onChange={(e) => setJobType(e.target.value)}
          disabled={loading}
        >
          <option value="">Tous les types de contrat</option>
          <option value="fulltime">CDI / Full-time</option>
          <option value="contract">CDD / Contract</option>
          <option value="parttime">Temps partiel / Part-time</option>
          <option value="internship">Stage / Internship</option>
          <option value="temporary">Intérim / Temporary</option>
          <option value="freelance">Freelance / Indépendant</option>
        </select>
        <p className="text-xs text-gray-500 mt-1.5">
          Le type de contrat recherché
        </p>
      </div>
      
      {/* Boutons d'action */}
      <div className="flex gap-3 pt-2">
        <Button 
          onClick={handleSearch} 
          className="flex-1 h-11 text-base font-semibold" 
          disabled={loading}
        >
          {loading ? (
            <>
              <Loader2 className="mr-2 h-5 w-5 animate-spin" />
              Recherche en cours...
            </>
          ) : (
            <>
              🔍 Lancer la recherche
            </>
          )}
        </Button>
        <Button 
          onClick={handleReset} 
          variant="outline" 
          className="h-11 px-6"
          disabled={loading}
        >
          🔄 Réinitialiser
        </Button>
      </div>
      
      {/* Message d'attente pendant le scraping */}
      {loading && (
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <div className="flex items-start gap-3">
            <Loader2 className="w-5 h-5 text-blue-600 animate-spin mt-0.5" />
            <div>
              <p className="text-sm text-blue-800 font-semibold mb-1">
                ⏳ Recherche en cours... Veuillez patienter
              </p>
              <p className="text-xs text-blue-700 leading-relaxed">
                Le système recherche d&apos;abord dans votre base de données locale, 
                puis scrape RemoteOK pour trouver de nouvelles offres. 
                Cette opération peut prendre <strong>10 à 30 secondes</strong> selon le nombre de résultats.
              </p>
            </div>
          </div>
        </div>
      )}
      
      {/* Aide contextuelle */}
      {!loading && (
        <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
          <p className="text-xs text-gray-600 leading-relaxed">
            <strong>�� Conseil:</strong> Pour obtenir plus de résultats, sélectionnez 
            &quot;Télétravail / Remote&quot; dans le mode de travail. RemoteOK est spécialisé 
            dans les offres en télétravail complet.
          </p>
        </div>
      )}
    </div>
  );
}
