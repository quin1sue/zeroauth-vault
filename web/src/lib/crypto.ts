export const deriveMasterKey = async (userSecret: string, salt: string): Promise<CryptoKey> => {
  const encoder = new TextEncoder();
  const baseKeyData = encoder.encode(userSecret);

  // 1. Import the "Key Material"
  const keyMaterial = await window.crypto.subtle.importKey(
    "raw",
    baseKeyData,
    "PBKDF2",
    false,
    ["deriveKey"]
  );

  return await window.crypto.subtle.deriveKey(
    {
      name: "PBKDF2",
      salt: encoder.encode(salt),
      iterations: 100000, 
      hash: "SHA-256",
    },
    keyMaterial,
    { name: "AES-GCM", length: 256 },
    true,
    ["encrypt", "decrypt"]
  );
};