"use client";
import { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { ProtectedRoute } from '@/components/ProtectedRoute';
import { Building2, Plus, RefreshCw, ExternalLink, Trash2 } from 'lucide-react';
import { toast } from 'sonner';
import { companiesService, WatchedCompany } from '@/lib/companiesService';
import { Loading } from '@/components/ui/loading';
import { EmptyState } from '@/components/ui/empty-state';

export default function CompaniesWatchPage() {
  const [companies, setCompanies] = useState<WatchedCompany[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [showAddForm, setShowAddForm] = useState(false);
  const [newCompany, setNewCompany] = useState({ name: '', url: '' });
  const [isAdding, setIsAdding] = useState(false);

  useEffect(() => {
    loadCompanies();
  }, []);

  const loadCompanies = async () => {
    try {
      setIsLoading(true);
      const data = await companiesService.getWatchedCompanies();
      setCompanies(data);
    } catch (error) {
      toast.error('Erreur lors du chargement des entreprises');
      console.error(error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleAdd = async () => {
    if (!newCompany.name || !newCompany.url) {
      toast.error('Veuillez remplir tous les champs');
      return;
    }

    try {
      setIsAdding(true);
      await companiesService.addCompanyWatch({
        company_name: newCompany.name,
        careers_url: newCompany.url
      });
      toast.success(`${newCompany.name} ajoutée à la veille !`);
      setNewCompany({ name: '', url: '' });
      setShowAddForm(false);
      await loadCompanies();
    } catch (error) {
      toast.error('Erreur lors de l\'ajout');
      console.error(error);
    } finally {
      setIsAdding(false);
    }
  };

  const handleScrape = async (companyId: number) => {
    try {
      toast.info('Scraping en cours...');
      await companiesService.triggerManualScrape(companyId);
      toast.success('Scraping terminé !');
      await loadCompanies();
    } catch (error) {
      toast.error('Erreur lors du scraping');
      console.error(error);
    }
  };

  const handleDelete = async (watchId: number, companyName: string) => {
    if (!confirm(`Supprimer ${companyName} de la veille ?`)) return;

    try {
      await companiesService.deleteCompanyWatch(watchId);
      toast.success('Entreprise supprimée');
      await loadCompanies();
    } catch (error) {
      toast.error('Erreur lors de la suppression');
      console.error(error);
    }
  };

  const formatLastUpdate = (date?: string) => {
    if (!date) return 'Jamais';
    const diffHours = Math.floor((Date.now() - new Date(date).getTime()) / (1000 * 60 * 60));
    if (diffHours < 1) return 'Il y a moins d\'1h';
    if (diffHours < 24) return `Il y a ${diffHours}h`;
    return `Il y a ${Math.floor(diffHours / 24)} jour(s)`;
  };

  if (isLoading) {
    return (
      <ProtectedRoute>
        <Loading text="Chargement des entreprises surveillées..." size="lg" />
      </ProtectedRoute>
    );
  }

  return (
    <ProtectedRoute>
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold">🏢 Veille Entreprise</h1>
            <p className="text-gray-600 mt-1">Surveillez les nouvelles offres de vos entreprises cibles</p>
          </div>
          <Button onClick={() => setShowAddForm(!showAddForm)} disabled={showAddForm}>
            <Plus className="mr-2 h-4 w-4" />
            Ajouter
          </Button>
        </div>

        {showAddForm && (
          <Card>
            <CardHeader>
              <CardTitle>Ajouter une entreprise</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <Label>Nom de l'entreprise</Label>
                <Input 
                  placeholder="Amazon" 
                  value={newCompany.name} 
                  onChange={(e) => setNewCompany({ ...newCompany, name: e.target.value })} 
                />
              </div>
              <div>
                <Label>URL page carrières</Label>
                <Input 
                  placeholder="https://amazon.jobs" 
                  value={newCompany.url} 
                  onChange={(e) => setNewCompany({ ...newCompany, url: e.target.value })} 
                />
              </div>
              <div className="flex gap-2">
                <Button onClick={handleAdd} disabled={isAdding}>
                  {isAdding ? 'Ajout...' : 'Ajouter'}
                </Button>
                <Button variant="outline" onClick={() => setShowAddForm(false)}>
                  Annuler
                </Button>
              </div>
            </CardContent>
          </Card>
        )}

        {companies.length > 0 && (
          <div className="grid grid-cols-3 gap-4">
            <Card>
              <CardContent className="pt-6 text-center">
                <p className="text-3xl font-bold">{companies.length}</p>
                <p className="text-sm text-gray-600">Entreprises</p>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="pt-6 text-center">
                <p className="text-3xl font-bold">{companies.reduce((s, c) => s + c.offers_count, 0)}</p>
                <p className="text-sm text-gray-600">Offres trouvées</p>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="pt-6 text-center">
                <p className="text-3xl font-bold">Auto</p>
                <p className="text-sm text-gray-600">Scraping périodique</p>
              </CardContent>
            </Card>
          </div>
        )}

        <div className="space-y-4">
          {companies.length === 0 ? (
            <EmptyState
              icon={Building2}
              title="Aucune entreprise surveillée"
              description="Ajoutez des entreprises pour recevoir automatiquement leurs nouvelles offres d'emploi"
              actionLabel="Ajouter une entreprise"
              onAction={() => setShowAddForm(true)}
            />
          ) : (
            companies.map((company) => (
              <Card key={company.id}>
                <CardHeader>
                  <div className="flex justify-between items-start">
                    <div>
                      <CardTitle className="flex items-center gap-2">
                        <Building2 className="h-5 w-5" />
                        {company.company_name}
                      </CardTitle>
                      <CardDescription className="flex items-center gap-2 mt-2">
                        <ExternalLink className="h-4 w-4" />
                        <a 
                          href={company.careers_url} 
                          target="_blank" 
                          rel="noopener noreferrer" 
                          className="hover:underline"
                        >
                          {company.careers_url}
                        </a>
                      </CardDescription>
                    </div>
                    <div className="flex gap-2">
                      <Button 
                        variant="outline" 
                        size="sm" 
                        onClick={() => handleScrape(company.id)}
                      >
                        <RefreshCw className="h-4 w-4" />
                      </Button>
                      <Button 
                        variant="ghost" 
                        size="sm" 
                        onClick={() => handleDelete(company.id, company.company_name)}
                      >
                        <Trash2 className="h-4 w-4 text-red-600" />
                      </Button>
                    </div>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600">
                      Dernière MAJ : {formatLastUpdate(company.last_scraped_at)}
                    </span>
                    <span className="font-bold text-primary">{company.offers_count} offres</span>
                  </div>
                </CardContent>
              </Card>
            ))
          )}
        </div>
      </div>
    </ProtectedRoute>
  );
}
