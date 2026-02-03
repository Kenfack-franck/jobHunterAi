'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { authService } from '@/lib/auth';
import { ProtectedRoute } from '@/components/ProtectedRoute';

interface PredefinedSource {
  id: string;
  name: string;
  url: string;
  source_type: string;
  scraper_type: string;
  priority: number;
  enabled_by_default: boolean;
}

interface SourcesData {
  aggregators: PredefinedSource[];
  companies: PredefinedSource[];
  all_sources: PredefinedSource[];
  total_count: number;
}

interface UserPreferences {
  id?: string;
  enabled_sources: string[];
  priority_sources: string[];
  use_cache: boolean;
  cache_ttl_hours: number;
  max_priority_sources: number;
  background_scraping_enabled: boolean;
}

export default function SourcesPage() {
  const [sources, setSources] = useState<SourcesData | null>(null);
  const [preferences, setPreferences] = useState<UserPreferences | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState<{type: 'success' | 'error', text: string} | null>(null);
  const router = useRouter();

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const token = authService.getToken();
      
      if (!token) {
        console.error('[Sources] ❌ Pas de token au chargement !');
        setMessage({ type: 'error', text: '❌ Non authentifié. Redirection...' });
        setTimeout(() => router.push('/auth/login'), 2000);
        return;
      }
      
      console.log('[Sources] 🔑 Token chargement:', token.substring(0, 20) + '...');

      const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';
      
      const sourcesRes = await fetch(`${API_URL}/sources/predefined`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      
      if (!sourcesRes.ok) {
        if (sourcesRes.status === 401) {
          setMessage({ type: 'error', text: '❌ Session expirée. Redirection...' });
          setTimeout(() => router.push('/auth/login'), 2000);
          return;
        }
        throw new Error('Erreur chargement sources');
      }
      const sourcesData = await sourcesRes.json();
      setSources(sourcesData);

      const prefsRes = await fetch(`${API_URL}/sources/preferences`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      
      if (!prefsRes.ok) {
        if (prefsRes.status === 401) {
          setMessage({ type: 'error', text: '❌ Session expirée. Redirection...' });
          setTimeout(() => router.push('/auth/login'), 2000);
          return;
        }
        throw new Error('Erreur chargement préférences');
      }
      const prefsData = await prefsRes.json();
      setPreferences(prefsData);
      
      setLoading(false);
    } catch (error) {
      console.error('[Sources] ❌ Erreur chargement:', error);
      setMessage({ type: 'error', text: 'Erreur chargement des données' });
      setLoading(false);
    }
  };

  const toggleSource = (sourceId: string) => {
    if (!preferences) return;
    
    const isEnabled = preferences.enabled_sources.includes(sourceId);
    let newEnabled: string[];
    let newPriority = [...preferences.priority_sources];

    if (isEnabled) {
      newEnabled = preferences.enabled_sources.filter(id => id !== sourceId);
      newPriority = newPriority.filter(id => id !== sourceId);
    } else {
      newEnabled = [...preferences.enabled_sources, sourceId];
    }

    setPreferences({
      ...preferences,
      enabled_sources: newEnabled,
      priority_sources: newPriority
    });
  };

  const togglePriority = (sourceId: string) => {
    if (!preferences) return;
    
    const isPriority = preferences.priority_sources.includes(sourceId);
    let newPriority: string[];

    if (isPriority) {
      newPriority = preferences.priority_sources.filter(id => id !== sourceId);
    } else {
      if (preferences.priority_sources.length >= preferences.max_priority_sources) {
        setMessage({ 
          type: 'error', 
          text: `Maximum ${preferences.max_priority_sources} sources prioritaires` 
        });
        setTimeout(() => setMessage(null), 3000);
        return;
      }
      newPriority = [...preferences.priority_sources, sourceId];
    }

    setPreferences({
      ...preferences,
      priority_sources: newPriority
    });
  };

  const savePreferences = async () => {
    if (!preferences) return;
    
    setSaving(true);
    setMessage(null); // Clear any previous message
    
    try {
      const token = authService.getToken();
      
      if (!token) {
        console.error('[Sources] ❌ Pas de token trouvé !');
        setMessage({ type: 'error', text: '❌ Session expirée. Veuillez vous reconnecter.' });
        // Rediriger vers login après 2 secondes
        setTimeout(() => router.push('/auth/login'), 2000);
        return;
      }
      
      console.log('[Sources] 💾 Sauvegarde des préférences...', preferences);
      console.log('[Sources] 🔑 Token présent:', token.substring(0, 20) + '...');
      
      const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';
      
      const response = await fetch(`${API_URL}/sources/preferences`, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(preferences)
      });

      const data = await response.json();
      console.log('[Sources] 📡 Réponse API:', response.status, data);

      if (!response.ok) {
        throw new Error(data.detail || 'Erreur sauvegarde');
      }
      
      setMessage({ 
        type: 'success', 
        text: `✅ Préférences sauvegardées ! ${preferences.enabled_sources.length} sources activées, ${preferences.priority_sources.length} prioritaires.` 
      });
      
      // Auto-hide après 5 secondes
      setTimeout(() => setMessage(null), 5000);
      
    } catch (error) {
      console.error('[Sources] ❌ Erreur sauvegarde:', error);
      setMessage({ 
        type: 'error', 
        text: `❌ Erreur: ${error instanceof Error ? error.message : 'Impossible de sauvegarder'}` 
      });
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Chargement...</p>
        </div>
      </div>
    );
  }

  if (!sources || !preferences) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-red-600">Erreur chargement des données</div>
      </div>
    );
  }

  const groupedCompanies = sources.companies.reduce((acc, company) => {
    if (!acc[company.source_type]) {
      acc[company.source_type] = [];
    }
    acc[company.source_type].push(company);
    return acc;
  }, {} as Record<string, PredefinedSource[]>);

  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-gray-50 py-8 px-4">
        <div className="max-w-6xl mx-auto">
          <div className="mb-8">
            <h1 className="text-3xl font-bold text-gray-900 mb-2">
              🔍 Configuration des Sources
            </h1>
            <p className="text-gray-600">
              Choisissez les sources pour la recherche d'offres
            </p>
          </div>

          <div className="bg-white rounded-lg shadow p-6 mb-6">
            <div className="grid grid-cols-3 gap-4">
              <div>
                <div className="text-2xl font-bold text-blue-600">{sources.total_count}</div>
                <div className="text-sm text-gray-600">Sources disponibles</div>
              </div>
              <div>
                <div className="text-2xl font-bold text-green-600">{preferences.enabled_sources.length}</div>
                <div className="text-sm text-gray-600">Sources activées</div>
              </div>
              <div>
                <div className="text-2xl font-bold text-purple-600">{preferences.priority_sources.length}/{preferences.max_priority_sources}</div>
                <div className="text-sm text-gray-600">Sources prioritaires</div>
              </div>
            </div>
          </div>

          {/* Agrégateurs d'offres */}
          <div className="mb-8">
            <h2 className="text-xl font-bold text-gray-900 mb-4">
              🌐 Agrégateurs d'offres
            </h2>
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
              {sources.aggregators.map(source => {
                const isEnabled = preferences.enabled_sources.includes(source.id);
                const isPriority = preferences.priority_sources.includes(source.id);
                
                return (
                  <div key={source.id} className={`bg-white rounded-lg border-2 p-4 transition ${
                    isEnabled ? 'border-blue-500' : 'border-gray-200'
                  }`}>
                    <div className="flex items-start justify-between mb-3">
                      <div className="flex items-center gap-3">
                        <input
                          type="checkbox"
                          checked={isEnabled}
                          onChange={() => toggleSource(source.id)}
                          className="w-5 h-5 text-blue-600 rounded focus:ring-2 focus:ring-blue-500"
                        />
                        <div>
                          <h3 className="font-semibold text-gray-900">{source.name}</h3>
                          <span className="text-xs text-gray-500">{source.scraper_type}</span>
                        </div>
                      </div>
                      {isEnabled && (
                        <button
                          onClick={() => togglePriority(source.id)}
                          className={`text-xs px-2 py-1 rounded ${
                            isPriority 
                              ? 'bg-purple-100 text-purple-700 border border-purple-300' 
                              : 'bg-gray-100 text-gray-600 border border-gray-300'
                          }`}
                          title="Marquer comme prioritaire pour scraping temps réel"
                        >
                          {isPriority ? '⭐ Prioritaire' : 'Priorité'}
                        </button>
                      )}
                    </div>
                    <a href={source.url} target="_blank" rel="noopener noreferrer" 
                       className="text-xs text-blue-600 hover:underline break-all">
                      {source.url}
                    </a>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Sites carrières entreprises */}
          <div className="mb-8">
            <h2 className="text-xl font-bold text-gray-900 mb-4">
              🏢 Sites carrières d'entreprises
            </h2>
            <div className="space-y-6">
              {Object.entries(groupedCompanies).map(([type, companies]) => (
                <div key={type}>
                  <h3 className="text-lg font-semibold text-gray-800 mb-3 capitalize">
                    {type.replace('_', ' ')}
                  </h3>
                  <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
                    {companies.map(source => {
                      const isEnabled = preferences.enabled_sources.includes(source.id);
                      const isPriority = preferences.priority_sources.includes(source.id);
                      
                      return (
                        <div key={source.id} className={`bg-white rounded-lg border-2 p-4 transition ${
                          isEnabled ? 'border-blue-500' : 'border-gray-200'
                        }`}>
                          <div className="flex items-start justify-between mb-3">
                            <div className="flex items-center gap-3">
                              <input
                                type="checkbox"
                                checked={isEnabled}
                                onChange={() => toggleSource(source.id)}
                                className="w-5 h-5 text-blue-600 rounded focus:ring-2 focus:ring-blue-500"
                              />
                              <div>
                                <h4 className="font-semibold text-gray-900">{source.name}</h4>
                                <span className="text-xs text-gray-500">{source.scraper_type}</span>
                              </div>
                            </div>
                            {isEnabled && (
                              <button
                                onClick={() => togglePriority(source.id)}
                                className={`text-xs px-2 py-1 rounded ${
                                  isPriority 
                                    ? 'bg-purple-100 text-purple-700 border border-purple-300' 
                                    : 'bg-gray-100 text-gray-600 border border-gray-300'
                                }`}
                                title="Marquer comme prioritaire pour scraping temps réel"
                              >
                                {isPriority ? '⭐ Prioritaire' : 'Priorité'}
                              </button>
                            )}
                          </div>
                          <a href={source.url} target="_blank" rel="noopener noreferrer" 
                             className="text-xs text-blue-600 hover:underline break-all">
                            {source.url}
                          </a>
                        </div>
                      );
                    })}
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6 sticky bottom-4 z-50">
            {message && (
              <div className={`mb-4 p-4 rounded-lg border-2 font-semibold text-base ${
                message.type === 'success' 
                  ? 'bg-green-50 text-green-800 border-green-300' 
                  : 'bg-red-50 text-red-800 border-red-300'
              }`}>
                {message.text}
              </div>
            )}
            
            <div className="flex items-center justify-between">
              <div className="text-sm text-gray-600">
                💡 Sources prioritaires = scraping en temps réel (plus rapide)
              </div>
              <button
                onClick={savePreferences}
                disabled={saving}
                className="px-6 py-3 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition"
              >
                {saving ? 'Sauvegarde...' : 'Sauvegarder'}
              </button>
            </div>
          </div>
        </div>
      </div>
    </ProtectedRoute>
  );
}
