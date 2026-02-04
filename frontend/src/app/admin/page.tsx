'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { 
  Users, 
  UserCheck, 
  UserX, 
  TrendingUp, 
  AlertTriangle,
  BarChart3,
  Shield
} from 'lucide-react';
import { adminService, AdminDashboardStats } from '@/lib/adminService';

export default function AdminDashboard() {
  const router = useRouter();
  const [stats, setStats] = useState<AdminDashboardStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    loadStats();
  }, []);

  const loadStats = async () => {
    try {
      setLoading(true);
      setError('');
      const data = await adminService.getDashboardStats();
      setStats(data);
    } catch (err: any) {
      console.error('Error loading stats:', err);
      if (err.message.includes('403') || err.message.includes('Forbidden')) {
        setError('Accès refusé. Vous devez être administrateur.');
        setTimeout(() => router.push('/dashboard'), 2000);
      } else {
        setError(err.message || 'Erreur lors du chargement des statistiques');
      }
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-purple-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Chargement des statistiques...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-purple-50 flex items-center justify-center">
        <div className="bg-white p-8 rounded-2xl shadow-lg border-2 border-red-200 max-w-md">
          <div className="text-red-600 text-center">
            <AlertTriangle className="w-12 h-12 mx-auto mb-4" />
            <h2 className="text-xl font-bold mb-2">Erreur</h2>
            <p className="text-gray-700">{error}</p>
          </div>
        </div>
      </div>
    );
  }

  if (!stats) return null;

  const statCards = [
    {
      title: 'Total Utilisateurs',
      value: stats.total_users,
      icon: Users,
      color: 'from-blue-500 to-purple-600',
      bgColor: 'bg-blue-50'
    },
    {
      title: 'Actifs',
      value: stats.active_users,
      icon: UserCheck,
      color: 'from-green-500 to-emerald-600',
      bgColor: 'bg-green-50'
    },
    {
      title: 'Bloqués',
      value: stats.blocked_users,
      icon: UserX,
      color: 'from-red-500 to-pink-600',
      bgColor: 'bg-red-50'
    },
    {
      title: 'Nouveaux (7j)',
      value: stats.new_users_this_week,
      icon: TrendingUp,
      color: 'from-violet-500 to-purple-600',
      bgColor: 'bg-violet-50'
    },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-purple-50">
      {/* Header avec gradient animé */}
      <div className="relative overflow-hidden bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 text-white">
        <div className="absolute inset-0 bg-grid-white/10"></div>
        
        {/* Blobs animés */}
        <div className="blob blob-purple top-0 left-0"></div>
        <div className="blob blob-blue top-0 right-0"></div>
        
        <div className="relative max-w-7xl mx-auto px-6 py-12">
          <div className="flex items-center gap-3 mb-4">
            <div className="w-12 h-12 bg-white/20 backdrop-blur-sm rounded-xl flex items-center justify-center">
              <Shield className="w-6 h-6" />
            </div>
            <div>
              <h1 className="text-3xl font-bold">Panneau Admin</h1>
              <p className="text-blue-100">Gestion des utilisateurs et statistiques</p>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-6 py-8">
        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {statCards.map((stat, index) => (
            <div
              key={index}
              className="bg-white rounded-2xl shadow-lg border-2 border-gray-100 p-6 hover:shadow-xl transition-all hover:scale-105"
            >
              <div className="flex items-center justify-between mb-4">
                <div className={`w-12 h-12 ${stat.bgColor} rounded-xl flex items-center justify-center`}>
                  <stat.icon className={`w-6 h-6 bg-gradient-to-r ${stat.color} bg-clip-text text-transparent`} />
                </div>
                <div className="text-3xl font-bold bg-gradient-to-r from-gray-900 to-gray-700 bg-clip-text text-transparent">
                  {stat.value}
                </div>
              </div>
              <h3 className="text-sm font-medium text-gray-600">{stat.title}</h3>
            </div>
          ))}
        </div>

        {/* Actions rapides */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          <Link
            href="/admin/users"
            className="bg-white rounded-2xl shadow-lg border-2 border-gray-100 p-8 hover:shadow-xl transition-all hover:border-purple-400 group"
          >
            <div className="flex items-center gap-4">
              <div className="w-16 h-16 bg-gradient-to-br from-blue-500 to-purple-600 rounded-2xl flex items-center justify-center group-hover:scale-110 transition-transform">
                <Users className="w-8 h-8 text-white" />
              </div>
              <div>
                <h3 className="text-xl font-bold text-gray-900 mb-1">Gérer les Utilisateurs</h3>
                <p className="text-gray-600">Liste, recherche, blocage, suppression</p>
              </div>
            </div>
          </Link>

          <div className="bg-white rounded-2xl shadow-lg border-2 border-gray-100 p-8">
            <div className="flex items-center gap-4">
              <div className="w-16 h-16 bg-gradient-to-br from-violet-500 to-pink-600 rounded-2xl flex items-center justify-center">
                <BarChart3 className="w-8 h-8 text-white" />
              </div>
              <div>
                <h3 className="text-xl font-bold text-gray-900 mb-1">Nouveaux Aujourd'hui</h3>
                <p className="text-3xl font-bold text-purple-600">{stats.new_users_today}</p>
              </div>
            </div>
          </div>
        </div>

        {/* Utilisateurs proches des limites */}
        {stats.users_near_limit.length > 0 && (
          <div className="bg-white rounded-2xl shadow-lg border-2 border-orange-200 p-6">
            <div className="flex items-center gap-3 mb-4">
              <AlertTriangle className="w-6 h-6 text-orange-600" />
              <h2 className="text-xl font-bold text-gray-900">
                Utilisateurs proches des limites ({stats.users_near_limit.length})
              </h2>
            </div>
            <div className="space-y-2">
              {stats.users_near_limit.map((user, index) => (
                <div key={index} className="flex items-center justify-between p-3 bg-orange-50 rounded-lg">
                  <span className="font-medium text-gray-900">{user.email}</span>
                  <span className="text-sm text-orange-600">{user.usage}</span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Inscriptions 7 derniers jours */}
        {stats.registrations_last_7_days && Object.keys(stats.registrations_last_7_days).length > 0 && (
          <div className="bg-white rounded-2xl shadow-lg border-2 border-gray-100 p-6 mt-6">
            <h2 className="text-xl font-bold text-gray-900 mb-4">Inscriptions - 7 derniers jours</h2>
            <div className="grid grid-cols-7 gap-2">
              {Object.entries(stats.registrations_last_7_days).map(([date, count]) => (
                <div key={date} className="text-center">
                  <div className="h-24 bg-gradient-to-t from-purple-600 to-blue-500 rounded-lg mb-2 flex items-end justify-center">
                    <div 
                      className="w-full bg-gradient-to-t from-purple-600 to-pink-500 rounded-lg transition-all"
                      style={{ height: `${Math.max(20, (count / Math.max(...Object.values(stats.registrations_last_7_days))) * 100)}%` }}
                    ></div>
                  </div>
                  <p className="text-xs text-gray-600 font-medium">{new Date(date).toLocaleDateString('fr-FR', { weekday: 'short' })}</p>
                  <p className="text-sm font-bold text-gray-900">{count}</p>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
