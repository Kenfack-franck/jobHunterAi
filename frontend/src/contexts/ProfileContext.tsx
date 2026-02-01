"use client";
import React, { createContext, useContext, useEffect, useState, useCallback } from 'react';
import profileService from '@/lib/profile';
import { useAuth } from './AuthContext';
import { Profile } from '@/types';

interface ProfileContextType {
  profile: Profile | null;
  hasProfile: boolean;
  isLoading: boolean;
  completion: number;
  refreshProfile: () => Promise<void>;
}

const ProfileContext = createContext<ProfileContextType | undefined>(undefined);

export function ProfileProvider({ children }: { children: React.ReactNode }) {
  const { isAuthenticated } = useAuth();
  const [profile, setProfile] = useState<Profile | null>(null);
  const [hasProfile, setHasProfile] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [completion, setCompletion] = useState(0);

  const loadProfile = useCallback(async () => {
    if (!isAuthenticated) {
      setProfile(null);
      setHasProfile(false);
      setIsLoading(false);
      return;
    }
    setIsLoading(true);
    try {
      const data = await profileService.getProfile();
      setProfile(data);
      setHasProfile(true);
      setCompletion(profileService.calculateCompletion(data));
    } catch (error: any) {
      if (error?.response?.status === 404) setHasProfile(false);
    } finally {
      setIsLoading(false);
    }
  }, [isAuthenticated]);

  useEffect(() => { loadProfile(); }, [loadProfile]);

  const refreshProfile = useCallback(async () => { await loadProfile(); }, [loadProfile]);

  return <ProfileContext.Provider value={{ profile, hasProfile, isLoading, completion, refreshProfile }}>{children}</ProfileContext.Provider>;
}

export function useProfile() {
  const context = useContext(ProfileContext);
  if (!context) throw new Error('useProfile must be used within ProfileProvider');
  return context;
}
