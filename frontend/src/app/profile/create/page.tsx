"use client"
import { useState } from "react";
import { useRouter } from "next/navigation";
import profileService from "@/lib/profile";
import { ProfileForm } from "@/components/profile/ProfileForm";
export default function CreateProfilePage() {
  const router = useRouter();
  const [isLoading, setIsLoading] = useState(false);
  const handleSubmit = async (data: any) => {
    setIsLoading(true);
    try {
      await profileService.createProfile(data);
      router.push("/profile");
    } catch (error) {
      console.error(error);
    } finally {
      setIsLoading(false);
    }
  };
  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-2xl mx-auto px-4">
        <h1 className="text-3xl font-bold mb-8">Créer votre profil</h1>
        <ProfileForm onSubmit={handleSubmit} isLoading={isLoading} />
      </div>
    </div>
  );
}
