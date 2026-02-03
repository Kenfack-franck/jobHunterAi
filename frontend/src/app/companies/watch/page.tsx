"use client";
import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { Loading } from '@/components/ui/loading';

export default function CompaniesWatchPage() {
  const router = useRouter();

  useEffect(() => {
    // Redirection immédiate vers la nouvelle page de configuration des sources
    router.replace('/settings/sources');
  }, [router]);

  return (
    <div className="flex items-center justify-center min-h-screen">
      <Loading text="Redirection vers Configuration des sources..." size="lg" />
    </div>
  );
}
