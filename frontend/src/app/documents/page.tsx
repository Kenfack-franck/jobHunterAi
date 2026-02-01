"use client";
import { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { ProtectedRoute } from '@/components/ProtectedRoute';
import { FileText, Download, Eye, RefreshCw, Trash2 } from 'lucide-react';
import { toast } from 'sonner';
import { documentsService, DocumentWithDetails } from '@/lib/documentsService';
import { Loading } from '@/components/ui/loading';
import { EmptyState } from '@/components/ui/empty-state';

export default function DocumentsPage() {
  const [filter, setFilter] = useState<'all' | 'resume' | 'cover_letter'>('all');
  const [documents, setDocuments] = useState<DocumentWithDetails[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    loadDocuments();
  }, []);

  const loadDocuments = async () => {
    try {
      setIsLoading(true);
      const data = await documentsService.getDocuments();
      setDocuments(data);
    } catch (error) {
      toast.error('Erreur lors du chargement des documents');
      console.error(error);
    } finally {
      setIsLoading(false);
    }
  };

  const filteredDocs = documents.filter(doc => 
    filter === 'all' || doc.document_type === filter
  );

  const formatDate = (dateStr: string) => {
    const date = new Date(dateStr);
    const now = new Date();
    const diffDays = Math.floor((now.getTime() - date.getTime()) / (1000 * 60 * 60 * 24));
    
    if (diffDays === 0) return 'Aujourd\'hui';
    if (diffDays === 1) return 'Hier';
    if (diffDays < 7) return `Il y a ${diffDays} jours`;
    return date.toLocaleDateString('fr-FR', { day: 'numeric', month: 'short', year: 'numeric' });
  };

  const handleDownload = async (doc: DocumentWithDetails) => {
    try {
      const blob = await documentsService.downloadDocument(doc.id);
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = doc.filename || `document_${doc.id}.pdf`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
      toast.success(`${doc.filename} téléchargé`);
    } catch (error) {
      toast.error('Erreur lors du téléchargement');
      console.error(error);
    }
  };

  const handlePreview = (doc: DocumentWithDetails) => {
    toast.info('Aperçu (feature en développement)');
  };

  const handleRegenerate = (doc: DocumentWithDetails) => {
    toast.info('Régénération (feature en développement)');
  };

  const handleDelete = async (docId: number, filename?: string) => {
    if (!confirm(`Supprimer ${filename || 'ce document'} ?`)) return;

    try {
      await documentsService.deleteDocument(docId);
      toast.success('Document supprimé');
      await loadDocuments();
    } catch (error) {
      toast.error('Erreur lors de la suppression');
      console.error(error);
    }
  };

  const getTypeLabel = (type: string) => {
    return type === 'resume' ? 'CV' : 'Lettre';
  };

  if (isLoading) {
    return (
      <ProtectedRoute>
        <Loading text="Chargement des documents..." size="lg" />
      </ProtectedRoute>
    );
  }

  return (
    <ProtectedRoute>
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold">📄 Mes Documents</h1>
            <p className="text-gray-600 mt-1">Gérez tous vos CV et lettres générés</p>
          </div>
          <div className="flex gap-2">
            <Button 
              variant={filter === 'all' ? 'default' : 'outline'} 
              onClick={() => setFilter('all')}
            >
              Tous
            </Button>
            <Button 
              variant={filter === 'resume' ? 'default' : 'outline'} 
              onClick={() => setFilter('resume')}
            >
              CV
            </Button>
            <Button 
              variant={filter === 'cover_letter' ? 'default' : 'outline'} 
              onClick={() => setFilter('cover_letter')}
            >
              Lettres
            </Button>
          </div>
        </div>

        {documents.length > 0 && (
          <div className="grid grid-cols-3 gap-4">
            <Card>
              <CardContent className="pt-6 text-center">
                <p className="text-3xl font-bold">{documents.length}</p>
                <p className="text-sm text-gray-600">Documents totaux</p>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="pt-6 text-center">
                <p className="text-3xl font-bold">
                  {documents.filter(d => d.document_type === 'resume').length}
                </p>
                <p className="text-sm text-gray-600">CV générés</p>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="pt-6 text-center">
                <p className="text-3xl font-bold">
                  {documents.filter(d => d.document_type === 'cover_letter').length}
                </p>
                <p className="text-sm text-gray-600">Lettres générées</p>
              </CardContent>
            </Card>
          </div>
        )}

        <div className="space-y-4">
          <h2 className="text-xl font-semibold">Documents ({filteredDocs.length})</h2>
          
          {filteredDocs.length === 0 ? (
            <EmptyState
              icon={FileText}
              title="Aucun document"
              description="Analysez une offre d'emploi et générez vos premiers documents personnalisés"
              actionLabel="Voir les offres"
              onAction={() => window.location.href = '/jobs'}
            />
          ) : (
            filteredDocs.map((doc) => (
              <Card key={doc.id}>
                <CardHeader>
                  <div className="flex justify-between items-start">
                    <div className="flex-1">
                      <div className="flex items-center gap-3">
                        <div className={`px-2 py-1 rounded text-xs font-semibold ${
                          doc.document_type === 'resume' 
                            ? 'bg-blue-100 text-blue-700' 
                            : 'bg-green-100 text-green-700'
                        }`}>
                          {getTypeLabel(doc.document_type)}
                        </div>
                        <CardTitle className="text-lg">
                          {doc.filename || `Document ${doc.id}`}
                        </CardTitle>
                      </div>
                      {(doc.company_name || doc.job_title) && (
                        <CardDescription className="mt-2">
                          Pour : <span className="font-semibold">{doc.company_name || 'Entreprise'}</span>
                          {doc.job_title && ` - ${doc.job_title}`}
                        </CardDescription>
                      )}
                      <div className="flex gap-4 mt-2 text-sm text-gray-600">
                        <span>Généré : {formatDate(doc.generated_at)}</span>
                      </div>
                    </div>
                    <div className="flex gap-2">
                      <Button 
                        variant="outline" 
                        size="sm" 
                        onClick={() => handleDownload(doc)}
                      >
                        <Download className="h-4 w-4" />
                      </Button>
                      <Button 
                        variant="outline" 
                        size="sm" 
                        onClick={() => handlePreview(doc)}
                      >
                        <Eye className="h-4 w-4" />
                      </Button>
                      <Button 
                        variant="outline" 
                        size="sm" 
                        onClick={() => handleRegenerate(doc)}
                      >
                        <RefreshCw className="h-4 w-4" />
                      </Button>
                      <Button 
                        variant="ghost" 
                        size="sm" 
                        onClick={() => handleDelete(doc.id, doc.filename)}
                      >
                        <Trash2 className="h-4 w-4 text-red-600" />
                      </Button>
                    </div>
                  </div>
                </CardHeader>
              </Card>
            ))
          )}
        </div>
      </div>
    </ProtectedRoute>
  );
}
