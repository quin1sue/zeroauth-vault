'use client';
import { GoogleLogin, CredentialResponse } from '@react-oauth/google';
import { useVault } from '@/lib/contexts/vaultcontext';
import api from '@/lib/api';
import { AuthTokenResponse } from '@/lib/types/backend';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { ShieldCheck, Lock, Cpu } from "lucide-react";

export default function LoginPage() {
  const { setKeyFromSecret, masterKey } = useVault();

  const handleLoginSuccess = async (response: CredentialResponse) => {
    if (!response.credential) return;

    try {
      // res.data expects the salt from the backend
      const res = await api.post<AuthTokenResponse & { vault_salt: string }>('/auth/google', {
        id_token: response.credential,
      });

      // Store the access token securely (consider HttpOnly cookies for production)
      // will set as cookies soon
      localStorage.setItem('bondee_token', res.data.accessToken);

      // Deriving the key (The "Baking" process)
      await setKeyFromSecret(res.data.user.id.toString(), res.data.vault_salt);
      
    } catch (err) {
      console.error("Authentication failed", err);
    }
  };

  return (
    <main className="flex min-h-screen items-center justify-center bg-slate-50 p-4">
      <Card className="max-w-md w-full shadow-lg border-t-4 border-t-blue-600">
        <CardHeader className="text-center">
          <div className="flex justify-center mb-2">
            <div className="p-3 bg-blue-100 rounded-full">
              <ShieldCheck className="w-8 h-8 text-blue-600" />
            </div>
          </div>
          <CardTitle className="text-2xl font-bold">Bondee Vault</CardTitle>
          <CardDescription>
            Zero-Knowledge encryption starts in your browser.
          </CardDescription>
        </CardHeader>

        <CardContent className="space-y-6">
          <div className="flex flex-col items-center justify-center py-4 border-y border-slate-100 space-y-4">
            <GoogleLogin 
              onSuccess={handleLoginSuccess} 
              onError={() => console.log('Login Failed')}
              useOneTap
              shape="pill"
            />
          </div>

          {/* Security Visualizer - Great for Resume/User Trust */}
          <div className="grid grid-cols-2 gap-4 text-xs text-slate-500">
            <div className="flex items-center gap-2 bg-slate-100 p-2 rounded">
              <Lock className="w-4 h-4 text-green-600" />
              <span>AES-256 GCM</span>
            </div>
            <div className="flex items-center gap-2 bg-slate-100 p-2 rounded">
              <Cpu className="w-4 h-4 text-blue-600" />
              <span>PBKDF2 Local</span>
            </div>
          </div>

          {masterKey && (
            <div className="animate-in fade-in zoom-in duration-300 p-3 bg-green-50 border border-green-200 rounded-md text-green-700 text-sm flex items-center justify-center gap-2">
              <ShieldCheck className="w-4 h-4" />
              Master Key Derived & Active in RAM
            </div>
          )}
        </CardContent>
      </Card>
    </main>
  );
}