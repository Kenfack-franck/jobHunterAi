"use client";
import { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { ProtectedRoute } from '@/components/ProtectedRoute';
import { Mail, CheckCircle, Clock, XCircle, Calendar, Plus, Trash2, Edit2, Loader2 } from 'lucide-react';
import { Badge } from '@/components/ui/badge';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { toast } from 'sonner';
import { applicationsService, Application, ApplicationCreate, ApplicationStats } from '@/lib/applicationsService';

export default function ApplicationsPage() {
  const [applications, setApplications] = useState<Application[]>([]);
  const [stats, setStats] = useState<ApplicationStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [showAddForm, setShowAddForm] = useState(false);
  const [editingId, setEditingId] = useState<string | null>(null);
  const [editNotes, setEditNotes] = useState('');
  const [editStatus, setEditStatus] = useState<Application['status']>('pending');
  
  // Form state
  const [formData, setFormData] = useState<ApplicationCreate>({
    company_name: '',
    job_title: '',
    email_to: '',
    notes: ''
  });

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      const [appsData, statsData] = await Promise.all([
        applicationsService.getApplications(),
        applicationsService.getStats()
      ]);
      setApplications(appsData);
      setStats(statsData);
    } catch (error) {
      toast.error('Erreur lors du chargement des candidatures');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const handleAdd = async () => {
    if (!formData.company_name || !formData.job_title || !formData.email_to) {
      toast.error('Veuillez remplir tous les champs obligatoires');
      return;
    }

    try {
      await applicationsService.createApplication(formData);
      toast.success('Candidature ajoutée avec succès');
      setShowAddForm(false);
      setFormData({ company_name: '', job_title: '', email_to: '', notes: '' });
      loadData();
    } catch (error) {
      toast.error('Erreur lors de l\'ajout');
      console.error(error);
    }
  };

  const handleUpdate = async (id: string) => {
    try {
      await applicationsService.updateApplication(id, {
        status: editStatus,
        notes: editNotes
      });
      toast.success('Candidature mise à jour');
      setEditingId(null);
      loadData();
    } catch (error) {
      toast.error('Erreur lors de la mise à jour');
      console.error(error);
    }
  };

  const handleDelete = async (id: string) => {
    if (!confirm('Êtes-vous sûr de vouloir supprimer cette candidature ?')) return;
    
    try {
      await applicationsService.deleteApplication(id);
      toast.success('Candidature supprimée');
      loadData();
    } catch (error) {
      toast.error('Erreur lors de la suppression');
      console.error(error);
    }
  };

  const startEdit = (app: Application) => {
    setEditingId(app.id);
    setEditStatus(app.status);
    setEditNotes(app.notes || '');
  };

  const getStatusConfig = (status: Application['status']) => {
    const configs = {
      pending: { label: 'En attente', color: 'bg-yellow-100 text-yellow-700', icon: Clock },
      replied: { label: 'Réponse reçue', color: 'bg-blue-100 text-blue-700', icon: Mail },
      interview: { label: 'Entretien', color: 'bg-green-100 text-green-700', icon: CheckCircle },
      rejected: { label: 'Refusé', color: 'bg-red-100 text-red-700', icon: XCircle },
      accepted: { label: 'Accepté', color: 'bg-purple-100 text-purple-700', icon: CheckCircle }
    };
    return configs[status];
  };

  const formatDate = (dateStr: string) => {
    const date = new Date(dateStr);
    return date.toLocaleDateString('fr-FR', { 
      day: 'numeric', 
      month: 'long', 
      year: 'numeric'
    });
  };

  if (loading) {
    return (
      <ProtectedRoute>
        <div className="flex items-center justify-center h-96">
          <Loader2 className="h-8 w-8 animate-spin text-gray-400" />
        </div>
      </ProtectedRoute>
    );
  }

  return (
    <ProtectedRoute>
      <div className="space-y-6 min-h-screen relative">
        {/* Animated background blobs */}
        <div className="absolute inset-0 overflow-hidden pointer-events-none">
          <div className="absolute top-20 left-1/3 w-96 h-96 bg-blue-400/10 rounded-full blur-3xl animate-pulse" />
          <div className="absolute bottom-20 right-1/3 w-96 h-96 bg-green-400/10 rounded-full blur-3xl animate-pulse delay-1000" />
        </div>

        <div className="flex justify-between items-center bg-gradient-to-r from-blue-50 to-green-50 rounded-3xl p-8 border-2 border-blue-100 shadow-lg relative z-10">
          <div>
            <div className="flex items-center gap-3 mb-2">
              <div className="p-3 rounded-xl bg-gradient-to-br from-blue-500 to-green-600 shadow-md">
                <Mail className="w-7 h-7 text-white" />
              </div>
              <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-600 via-purple-600 to-green-600 bg-clip-text text-transparent">
                Mes Candidatures
              </h1>
            </div>
            <p className="text-gray-600 mt-2 text-lg ml-16">Journal de toutes vos candidatures envoyées</p>
          </div>
          <Button onClick={() => setShowAddForm(!showAddForm)} className="gap-2 shadow-lg hover:shadow-xl transition-all">
            <Plus className="h-5 w-5" />
            {showAddForm ? 'Annuler' : 'Nouvelle candidature'}
          </Button>
        </div>

        {showAddForm && (
          <Card className="border-2 border-purple-200 shadow-xl bg-white/90 backdrop-blur-sm relative z-10 hover:shadow-2xl transition-all">
            <CardHeader className="bg-gradient-to-r from-purple-50 to-blue-50">
              <CardTitle className="flex items-center gap-2">
                <Plus className="w-5 h-5 text-purple-600" />
                Ajouter une candidature
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="text-sm font-medium">Entreprise *</label>
                  <Input
                    value={formData.company_name}
                    onChange={(e) => setFormData({ ...formData, company_name: e.target.value })}
                    placeholder="Google"
                  />
                </div>
                <div>
                  <label className="text-sm font-medium">Poste *</label>
                  <Input
                    value={formData.job_title}
                    onChange={(e) => setFormData({ ...formData, job_title: e.target.value })}
                    placeholder="Senior Developer"
                  />
                </div>
              </div>
              <div>
                <label className="text-sm font-medium">Email destinataire *</label>
                <Input
                  type="email"
                  value={formData.email_to}
                  onChange={(e) => setFormData({ ...formData, email_to: e.target.value })}
                  placeholder="jobs@company.com"
                />
              </div>
              <div>
                <label className="text-sm font-medium">Notes (optionnel)</label>
                <Textarea
                  value={formData.notes}
                  onChange={(e) => setFormData({ ...formData, notes: e.target.value })}
                  placeholder="Via LinkedIn, contact: John Doe..."
                  rows={3}
                />
              </div>
              <Button onClick={handleAdd} className="w-full shadow-md hover:shadow-lg transition-all">
                <Plus className="w-4 h-4 mr-2" />
                Ajouter la candidature
              </Button>
            </CardContent>
          </Card>
        )}

        <div className="grid grid-cols-2 md:grid-cols-5 gap-4 relative z-10">
          <Card className="bg-gradient-to-br from-blue-50 to-blue-100 border-2 border-blue-200 shadow-lg hover:shadow-xl transition-all">
            <CardContent className="pt-6 text-center">
              <p className="text-4xl font-bold text-blue-900 mb-1">{stats?.total || 0}</p>
              <p className="text-sm text-blue-700 font-semibold">Total</p>
            </CardContent>
          </Card>
          <Card className="bg-gradient-to-br from-yellow-50 to-yellow-100 border-2 border-yellow-200 shadow-lg hover:shadow-xl transition-all">
            <CardContent className="pt-6 text-center">
              <p className="text-4xl font-bold text-yellow-900 mb-1">{stats?.by_status.pending || 0}</p>
              <p className="text-sm text-yellow-700 font-semibold">En attente</p>
            </CardContent>
          </Card>
          <Card className="bg-gradient-to-br from-blue-50 to-indigo-100 border-2 border-blue-300 shadow-lg hover:shadow-xl transition-all">
            <CardContent className="pt-6 text-center">
              <p className="text-4xl font-bold text-indigo-900 mb-1">{stats?.by_status.replied || 0}</p>
              <p className="text-sm text-indigo-700 font-semibold">Réponses</p>
            </CardContent>
          </Card>
          <Card className="bg-gradient-to-br from-green-50 to-green-100 border-2 border-green-200 shadow-lg hover:shadow-xl transition-all">
            <CardContent className="pt-6 text-center">
              <p className="text-4xl font-bold text-green-900 mb-1">{stats?.by_status.interview || 0}</p>
              <p className="text-sm text-green-700 font-semibold">Entretiens</p>
            </CardContent>
          </Card>
          <Card className="bg-gradient-to-br from-purple-50 to-purple-100 border-2 border-purple-200 shadow-lg hover:shadow-xl transition-all">
            <CardContent className="pt-6 text-center">
              <p className="text-4xl font-bold text-purple-900 mb-1">{stats?.response_rate || 0}%</p>
              <p className="text-sm text-purple-700 font-semibold">Taux réponse</p>
            </CardContent>
          </Card>
        </div>

        <div className="space-y-4 relative z-10">
          <div className="bg-white/70 backdrop-blur-sm rounded-2xl p-5 border-2 border-blue-100 shadow-sm">
            <h2 className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
              Historique ({applications.length})
            </h2>
          </div>
          
          {applications.length === 0 ? (
            <Card className="border-2 border-dashed border-blue-200 bg-white/80 backdrop-blur-sm shadow-lg">
              <CardContent className="pt-6 text-center py-12">
                <div className="p-4 rounded-full bg-gradient-to-br from-blue-100 to-purple-100 w-20 h-20 mx-auto mb-4 flex items-center justify-center">
                  <Mail className="h-10 w-10 text-blue-500" />
                </div>
                <p className="text-gray-600 mb-4 text-lg font-semibold">Aucune candidature envoyée</p>
                <Button onClick={() => setShowAddForm(true)} className="shadow-md hover:shadow-lg transition-all gap-2">
                  <Plus className="h-4 w-4" />
                  Ajouter votre première candidature
                </Button>
              </CardContent>
            </Card>
          ) : (
            applications.map((app) => {
              const statusConfig = getStatusConfig(app.status);
              const StatusIcon = statusConfig.icon;
              const isEditing = editingId === app.id;
              
              return (
                <Card key={app.id} className="border-2 border-gray-200 shadow-lg hover:shadow-xl hover:border-purple-300 transition-all bg-white/80 backdrop-blur-sm">
                  <CardHeader>
                    <div className="flex justify-between items-start">
                      <div className="flex-1">
                        <div className="flex items-center gap-3 mb-2">
                          <CardTitle className="text-lg">{app.company_name}</CardTitle>
                          {!isEditing ? (
                            <div className={`px-3 py-1 rounded-full text-xs font-semibold flex items-center gap-1 ${statusConfig.color}`}>
                              <StatusIcon className="h-3 w-3" />
                              {statusConfig.label}
                            </div>
                          ) : (
                            <Select value={editStatus} onValueChange={(v) => setEditStatus(v as Application['status'])}>
                              <SelectTrigger className="w-40">
                                <SelectValue />
                              </SelectTrigger>
                              <SelectContent>
                                <SelectItem value="pending">En attente</SelectItem>
                                <SelectItem value="replied">Réponse reçue</SelectItem>
                                <SelectItem value="interview">Entretien</SelectItem>
                                <SelectItem value="rejected">Refusé</SelectItem>
                                <SelectItem value="accepted">Accepté</SelectItem>
                              </SelectContent>
                            </Select>
                          )}
                        </div>
                        <CardDescription className="text-base">{app.job_title}</CardDescription>
                        <div className="flex gap-4 mt-3 text-sm text-gray-600">
                          <div className="flex items-center gap-1">
                            <Calendar className="h-4 w-4" />
                            <span>Envoyée le {formatDate(app.applied_at)}</span>
                          </div>
                          <div className="flex items-center gap-1">
                            <Mail className="h-4 w-4" />
                            <span>{app.email_to}</span>
                          </div>
                        </div>
                        {!isEditing && app.notes && (
                          <div className="mt-3 text-sm text-gray-700 bg-gray-50 p-3 rounded">
                            <strong>Notes:</strong> {app.notes}
                          </div>
                        )}
                        {isEditing && (
                          <div className="mt-3">
                            <Textarea
                              value={editNotes}
                              onChange={(e) => setEditNotes(e.target.value)}
                              placeholder="Ajouter des notes..."
                              rows={2}
                            />
                          </div>
                        )}
                      </div>
                      <div className="flex gap-2">
                        {!isEditing ? (
                          <>
                            <Button variant="ghost" size="sm" onClick={() => startEdit(app)}>
                              <Edit2 className="h-4 w-4" />
                            </Button>
                            <Button variant="ghost" size="sm" onClick={() => handleDelete(app.id)}>
                              <Trash2 className="h-4 w-4 text-red-500" />
                            </Button>
                          </>
                        ) : (
                          <>
                            <Button size="sm" onClick={() => handleUpdate(app.id)}>
                              Enregistrer
                            </Button>
                            <Button variant="outline" size="sm" onClick={() => setEditingId(null)}>
                              Annuler
                            </Button>
                          </>
                        )}
                      </div>
                    </div>
                  </CardHeader>
                </Card>
              );
            })
          )}
        </div>
      </div>
    </ProtectedRoute>
  );
}
