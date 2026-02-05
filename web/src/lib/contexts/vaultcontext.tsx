'use client';
import React, { createContext, useContext, useState } from 'react';
import { deriveMasterKey } from '@/lib/crypto';

interface VaultContextType {
  masterKey: CryptoKey | null;
  setKeyFromSecret: (secret: string, salt: string) => Promise<void>;
  clearKey: () => void;
}

const VaultContext = createContext<VaultContextType | undefined>(undefined);

export const VaultProvider = ({ children }: { children: React.ReactNode }) => {
  const [masterKey, setMasterKey] = useState<CryptoKey | null>(null);

  const setKeyFromSecret = async (secret: string, salt: string) => {
    const key = await deriveMasterKey(secret, salt);
    setMasterKey(key);
  };

  const clearKey = () => setMasterKey(null);

  return (
    <VaultContext.Provider value={{ masterKey, setKeyFromSecret, clearKey }}>
      {children}
    </VaultContext.Provider>
  );
};

export const useVault = () => {
  const context = useContext(VaultContext);
  if (!context) throw new Error("useVault must be used within a VaultProvider");
  return context;
};