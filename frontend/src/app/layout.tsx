import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import { Toaster } from 'sonner'
import { AuthProvider } from '@/contexts/AuthContext'
import { ProfileProvider } from '@/contexts/ProfileContext'
import { AppShell } from '@/components/layout/AppShell'
import { FeedbackButton } from '@/components/feedback/FeedbackButton'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Job Hunter AI - Automatisez votre recherche d\'emploi',
  description: 'Assistant intelligent pour générer des candidatures personnalisées',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="fr">
      <body className={inter.className}>
        <AuthProvider>
          <ProfileProvider>
            <AppShell>{children}</AppShell>
            <FeedbackButton />
            <Toaster position="top-right" richColors />
          </ProfileProvider>
        </AuthProvider>
      </body>
    </html>
  )
}
