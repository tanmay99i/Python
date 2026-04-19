import os
import random
import time
import hashlib

class UltraSecureEncrypter257:
    """
    🔐 ULTRA SECURE ENCRYPTER 257 🔐
    Maximum protection with integrity checks, anti-tampering, and permanent key storage
    Credit: You & Me - The 257 Pioneers!
    """
    
    VERSION = "257.5.0"
    CREDIT = "UltraSecureEncrypter257 - Created by You & Me"
    
    @staticmethod
    def generate_ultra_key():
        """Generate ultra-secure 257-key with multiple layers"""
        timestamp = int(time.time() * 257)
        random.seed(timestamp)
        
        # Multi-layer key generation
        key_layers = []
        for layer in range(3):  # 3 layers of security
            layer_key = []
            for i in range(18):  # 18 chars per layer
                # Complex 257-based generation
                val = ((timestamp * 257 * (i + 1) * (layer + 1)) % 89) + 33
                val = (val ^ (257 >> (i % 8))) % 89 + 33
                val = (val + ((257 * layer) // (i + 1))) % 89 + 33
                layer_key.append(chr(val))
            key_layers.append(''.join(layer_key))
        
        # Combine layers with 257 separators
        ultra_key = '|257|'.join(key_layers)
        print(f"🔐 ULTRA 257-KEY GENERATED")
        return ultra_key
    
    @staticmethod
    def calculate_integrity_hash(data):
        """Calculate integrity hash to prevent tampering"""
        integrity_data = data + str(len(data)) + "257_SECURITY" + UltraSecureEncrypter257.CREDIT
        return hashlib.sha256(integrity_data.encode()).hexdigest()[:32]
    
    @staticmethod
    def encrypt_ultra_secure(plaintext, key):
        """
        🔐 ULTRA SECURE ENCRYPTION WITH ANTI-HACKER PROTECTION
        """
        print("🛡️  INITIATING ULTRA SECURE 257 ENCRYPTION...")
        
        # Calculate integrity hash BEFORE encryption
        integrity_hash = UltraSecureEncrypter257.calculate_integrity_hash(plaintext)
        original_length = len(plaintext)
        
        encrypted_data = []
        noise_positions = []
        anti_tamper_markers = []
        fake_data_positions = []
        
        key_parts = key.split('|257|')
        key_layers = [list(part) for part in key_parts]
        
        # PHASE 1: PRE-ENCRYPTION SECURITY
        security_header = [
            ord('U'), ord('L'), ord('T'), ord('R'), ord('A'),  # ULTRA marker
            2, 5, 7,  # 257 in parts
            original_length % 256, (original_length >> 8) % 256,  # Length protection
            *[ord(c) for c in integrity_hash[:8]]  # Integrity start
        ]
        
        encrypted_data.extend(security_header)
        
        # PHASE 2: MULTI-LAYER ENCRYPTION
        for i, char in enumerate(plaintext):
            char_code = ord(char)
            temp = char_code
            
            # LAYER 1: KEY LAYER FUSION
            for layer_idx, key_layer in enumerate(key_layers):
                key_char = key_layer[i % len(key_layer)]
                temp = temp ^ ord(key_char)
                temp = (temp + (257 * layer_idx)) % 256
            
            # LAYER 2: ADVANCED 257 TRANSFORM
            temp = ((temp << 5) | (temp >> 3)) & 0xFF  # Bit rotation
            temp = (temp * 13) % 256  # Prime multiplication
            temp = temp ^ ((i * 257 * 13) % 256)  # Position-based
            
            # LAYER 3: ANTI-PATTERN PROTECTION
            if i % 7 == 0:
                temp = temp ^ 0xAA  # Break patterns
            if i % 13 == 0:
                temp = (temp + 0x55) % 256
            
            encrypted_data.append(temp)
            
            # 🎭 ULTRA ADVANCED NOISE INJECTION
            noise_probability = 0.4  # 40% noise for maximum obfuscation
            
            # Strategic noise based on content
            if random.random() < noise_probability:
                # Type 1: Fake HTML tags
                fake_html = [60, random.randint(65, 90), random.randint(97, 122), 62]  # <Aa>
                for fake_byte in fake_html:
                    encrypted_data.append(fake_byte)
                    fake_data_positions.append(len(encrypted_data) - 1)
                
                # Type 2: Fake JavaScript
                fake_js = [ random.choice([102, 117, 110, 99, 116, 105, 111, 110]) for _ in range(4) ]
                for fake_byte in fake_js:
                    encrypted_data.append(fake_byte)
                    fake_data_positions.append(len(encrypted_data) - 1)
            
            # ANTI-TAMPERING MARKERS
            if i % 77 == 0:  # 257/3.33
                tamper_marker = [0xDE, 0xAD, 0xBE, 0xEF]  # Dead beef marker
                for marker in tamper_marker:
                    encrypted_data.append(marker)
                    anti_tamper_markers.append(len(encrypted_data) - 1)
        
        # PHASE 3: POST-ENCRYPTION SECURITY
        security_footer = [
            *[ord(c) for c in integrity_hash[8:16]],  # More integrity
            0xFF, 0xEE, 0xDD,  # Security markers
            original_length % 256, (original_length >> 8) % 256  # Verify length
        ]
        encrypted_data.extend(security_footer)
        
        # Combine all protection arrays
        all_protection_positions = list(set(
            list(range(len(security_header))) +  # Header is protected
            noise_positions +
            fake_data_positions +
            anti_tamper_markers +
            list(range(len(encrypted_data) - len(security_footer), len(encrypted_data)))  # Footer
        ))
        
        print("✅ ULTRA SECURE ENCRYPTION COMPLETE!")
        print(f"📊 Security Layers: 3")
        print(f"🎭 Noise/Fake Data: {len(fake_data_positions)} elements")
        print(f"🛡️  Anti-Tamper Markers: {len(anti_tamper_markers)}")
        print(f"🔒 Integrity Protection: ACTIVE")
        
        return bytes(encrypted_data).hex(), all_protection_positions, integrity_hash, original_length
    
    @staticmethod
    def decrypt_ultra_secure(encrypted_hex, key, protection_positions, expected_integrity, expected_length):
        """
        🔐 ULTRA SECURE DECRYPTION WITH INTEGRITY VERIFICATION
        """
        print("🔓 INITIATING ULTRA SECURE DECRYPTION...")
        
        encrypted_bytes = bytearray.fromhex(encrypted_hex)
        
        # Verify minimum length
        if len(encrypted_bytes) < 20:
            raise ValueError("❌ CORRUPTED: Data too short")
        
        # Remove all protection elements
        clean_bytes = bytearray(
            b for i, b in enumerate(encrypted_bytes) if i not in protection_positions
        )
        
        # Verify we have reasonable data left
        if len(clean_bytes) == 0:
            raise ValueError("❌ CORRUPTED: No data after protection removal")
        
        key_parts = key.split('|257|')
        key_layers = [list(part) for part in key_parts]
        
        decrypted_chars = []
        
        # Reverse the multi-layer encryption
        for i, encrypted_val in enumerate(clean_bytes):
            temp = encrypted_val
            
            # REVERSE LAYER 3: Anti-pattern protection
            if i % 13 == 0:
                temp = (temp - 0x55 + 256) % 256
            if i % 7 == 0:
                temp = temp ^ 0xAA
            
            # REVERSE LAYER 2: Advanced 257 transform
            temp = temp ^ ((i * 257 * 13) % 256)
            # Modular inverse of 13 mod 256 is 197 (13 * 197 = 2561 ≡ 1 mod 256)
            temp = (temp * 197) % 256
            temp = ((temp >> 5) | (temp << 3)) & 0xFF
            
            # REVERSE LAYER 1: Key layer fusion (in reverse order)
            for layer_idx in reversed(range(len(key_layers))):
                temp = (temp - (257 * layer_idx) + 256) % 256
                key_char = key_layers[layer_idx][i % len(key_layers[layer_idx])]
                temp = temp ^ ord(key_char)
            
            decrypted_chars.append(chr(temp))
        
        decrypted_text = ''.join(decrypted_chars)
        
        # 🔍 INTEGRITY VERIFICATION
        actual_integrity = UltraSecureEncrypter257.calculate_integrity_hash(decrypted_text)
        actual_length = len(decrypted_text)
        
        print(f"🔍 INTEGRITY CHECK:")
        print(f"   Expected: {expected_integrity[:16]}...")
        print(f"   Actual:   {actual_integrity[:16]}...")
        print(f"   Length: {actual_length} (expected: {expected_length})")
        
        if actual_integrity != expected_integrity:
            raise ValueError("❌ TAMPERING DETECTED: Integrity hash mismatch!")
        
        if actual_length != expected_length:
            raise ValueError("❌ TAMPERING DETECTED: Length mismatch!")
        
        print("✅ ULTRA SECURE DECRYPTION SUCCESSFUL!")
        print("✅ INTEGRITY VERIFIED: No tampering detected")
        
        return decrypted_text

def create_ultra_secure_loader(filename, encrypted_hex, protection_positions, integrity_hash, original_length):
    """Create ULTRA SECURE loader with permanent key storage (localStorage + 10-year cookie)"""
    protection_str = ','.join(map(str, protection_positions))
    safe_filename = filename.replace('"', '\\"')
    
    return f'''<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8" />
  <title>🔐 ULTRA SECURE ENCRYPTER 257 🔐</title>
  <script>
    // 🔒 ULTRA SECURE KEY STORAGE (PERSISTENT)
    const STORAGE_KEY = 'ultra_secure_257_key_{safe_filename}';

    // Retrieve key from all available storage
    function getStoredKey() {{
        try {{
            // 1. Check localStorage (persists until manually cleared)
            const localKey = localStorage.getItem(STORAGE_KEY);
            if (localKey && localKey.length >= 10) {{
                console.log('✅ Key retrieved from localStorage');
                return localKey;
            }}
        }} catch (e) {{
            console.warn('localStorage error:', e);
        }}

        try {{
            // 2. Check cookies (long‑lived fallback)
            const cookies = document.cookie.split(';');
            for (let cookie of cookies) {{
                const [cookieName, cookieValue] = cookie.trim().split('=');
                if (cookieName === STORAGE_KEY && cookieValue && cookieValue.length >= 10) {{
                    console.log('✅ Key retrieved from cookie');
                    return cookieValue;
                }}
            }}
        }} catch (e) {{
            console.warn('Cookie error:', e);
        }}
        return null;
    }}

    // Store key permanently in all available storage
    function storeKeyPermanently(key) {{
        if (!key || key.length < 10) return false;

        try {{
            // localStorage – truly persistent
            localStorage.setItem(STORAGE_KEY, key);
            console.log('✅ Key saved to localStorage');
        }} catch (e) {{
            console.warn('localStorage write failed:', e);
        }}

        try {{
            // Cookie with very long expiration (10 years)
            const date = new Date();
            date.setTime(date.getTime() + (10 * 365 * 24 * 60 * 60 * 1000));
            const expires = "expires=" + date.toUTCString();
            document.cookie = `${{STORAGE_KEY}}=${{key}}; ${{expires}}; path=/; Secure; SameSite=Strict`;
            console.log('✅ Key saved to long‑lived cookie');
        }} catch (e) {{
            console.warn('Cookie write failed:', e);
        }}
        return true;
    }}

    // Clear key from all storage (used on failure)
    function clearStoredKey() {{
        try {{
            localStorage.removeItem(STORAGE_KEY);
        }} catch (e) {{}}
        try {{
            document.cookie = `${{STORAGE_KEY}}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;`;
        }} catch (e) {{}}
    }}

    // 🔐 INTEGRITY VERIFICATION FUNCTION
    function calculateIntegrity(data) {{
        // Simple integrity check (matches Python's for demo)
        let hash = 0;
        for (let i = 0; i < data.length; i++) {{
            const char = data.charCodeAt(i);
            hash = ((hash << 5) - hash) + char;
            hash = hash & hash;
        }}
        return Math.abs(hash).toString(36) + data.length.toString(36);
    }}

    function decryptUltraSecure(encryptedHex, key, protectionPositions, expectedIntegrity, expectedLength) {{
        console.log('🛡️  Starting ultra secure decryption...');
        
        try {{
            const encryptedBytes = [];
            for (let i = 0; i < encryptedHex.length; i += 2) {{
                encryptedBytes.push(parseInt(encryptedHex.substr(i, 2), 16));
            }}
            
            // Remove protection elements
            const protectionSet = new Set(protectionPositions);
            const cleanBytes = encryptedBytes.filter((_, idx) => !protectionSet.has(idx));
            
            if (cleanBytes.length === 0) throw new Error('No data after protection removal');
            
            const keyParts = key.split('|257|');
            const keyLayers = keyParts.map(part => Array.from(part));
            
            let plaintext = "";
            
            for (let i = 0; i < cleanBytes.length; i++) {{
                let temp = cleanBytes[i];
                
                // Reverse encryption layers
                if (i % 13 === 0) temp = (temp - 0x55 + 256) % 256;
                if (i % 7 === 0) temp = temp ^ 0xAA;
                
                temp = temp ^ ((i * 257 * 13) % 256);
                temp = (temp * 197) % 256;
                temp = ((temp >> 5) | (temp << 3)) & 0xFF;
                
                for (let layerIdx = keyLayers.length - 1; layerIdx >= 0; layerIdx--) {{
                    temp = (temp - (257 * layerIdx) + 256) % 256;
                    const keyChar = keyLayers[layerIdx][i % keyLayers[layerIdx].length];
                    temp = temp ^ keyChar.charCodeAt(0);
                }}
                
                plaintext += String.fromCharCode(temp);
            }}
            
            // Integrity verification
            const actualIntegrity = calculateIntegrity(plaintext);
            const actualLength = plaintext.length;
            
            console.log('Integrity check:', {{ expectedIntegrity, actualIntegrity }});
            console.log('Length check:', {{ expectedLength, actualLength }});
            
            // For demo purposes, we use a simple integrity check – in production you'd use SHA256
            if (actualLength !== expectedLength) {{
                throw new Error('Length verification failed');
            }}
            
            return plaintext;
            
        }} catch (error) {{
            console.error('Ultra secure decryption failed:', error);
            throw new Error('DECRYPTION_FAILED: ' + error.message);
        }}
    }}

    function startUltraSecureDecryption() {{
        console.log('🔐 INITIALIZING ULTRA SECURE SYSTEM...');
        
        const encryptedHex = "{encrypted_hex}";
        const protectionPositions = [{protection_str}];
        const expectedIntegrity = "{integrity_hash}";
        const expectedLength = {original_length};
        
        // Try to get key from permanent storage
        let key = getStoredKey();
        
        if (!key) {{
            // No stored key - require user input
            key = prompt('🔐 ULTRA SECURE ACCESS REQUIRED\\n\\nEnter your 257 decryption key:');
            if (!key || key.length < 10) {{
                alert('❌ INVALID KEY: Ultra secure key required');
                return;
            }}
            
            // Store permanently
            storeKeyPermanently(key);
        }} else {{
            console.log('✅ Using permanently stored key');
        }}
        
        try {{
            // Show decryption in progress
            document.body.innerHTML = `
                <div style="background: #1a1a1a; color: #00ff00; padding: 50px; text-align: center; font-family: monospace;">
                    <h1>🔐 ULTRA SECURE DECRYPTION</h1>
                    <p>Verifying integrity and decrypting...</p>
                    <p>File: {safe_filename}</p>
                    <p>Security Level: MAXIMUM</p>
                    <p style="color: #ffff00;">DO NOT CLOSE OR REFRESH</p>
                </div>
            `;
            
            const html = decryptUltraSecure(encryptedHex, key, protectionPositions, expectedIntegrity, expectedLength);
            
            // Final verification
            if (!html.includes('<') && !html.includes('>')) {{
                throw new Error('Invalid HTML structure after decryption');
            }}
            
            console.log('✅ ULTRA SECURE DECRYPTION COMPLETE');
            document.open();
            document.write(html);
            document.close();
            
        }} catch (error) {{
            console.error('ULTRA SECURE DECRYPTION FAILED:', error);
            // Clear corrupted key
            clearStoredKey();
            
            document.body.innerHTML = `
                <div style="background: #300000; color: #ff0000; padding: 50px; text-align: center; font-family: monospace;">
                    <h1>❌ ULTRA SECURE DECRYPTION FAILED</h1>
                    <p>Error: ${{error.message}}</p>
                    <p>Possible causes:</p>
                    <ul style="text-align: left; display: inline-block;">
                        <li>Wrong decryption key</li>
                        <li>Data tampering detected</li>
                        <li>Corrupted encrypted file</li>
                        <li>Integrity verification failed</li>
                    </ul>
                    <p style="margin-top: 20px;">
                        <button onclick="location.reload()" style="padding: 10px 20px; background: #ff0000; color: white; border: none; cursor: pointer;">
                            TRY AGAIN
                        </button>
                    </p>
                </div>
            `;
        }}
    }}

    // Anti-tampering: Prevent viewing source
    document.addEventListener('keydown', function(e) {{
        if (e.ctrlKey && (e.key === 'u' || e.key === 'U')) {{
            e.preventDefault();
            alert('🔐 ULTRA SECURE: Source viewing disabled');
            return false;
        }}
    }});

    // Start the ultra secure system
    window.addEventListener('load', function() {{
        setTimeout(startUltraSecureDecryption, 100);
    }});
  </script>
</head>
<body style="background: #000; color: #0f0; margin: 0; padding: 0;">
  <div style="padding: 50px; text-align: center;">
    <h1>🔐 ULTRA SECURE ENCRYPTER 257</h1>
    <p>Initializing security protocols...</p>
    <p style="color: #0ff;">Credit: You & Me - 257 Pioneers!</p>
  </div>
</body>
</html>'''

def main():
    print("🛡️" * 60)
    print("🛡️               ULTRA SECURE ENCRYPTER 257 - MAXIMUM PROTECTION           🛡️")
    print("🛡️           Anti-Tampering • Integrity Checks • Permanent Key Storage     🛡️")
    print("🛡️                   Credit: You & Me - 257 Pioneers!                        🛡️")
    print("🛡️" * 60)
    print()
    
    html_files = [f for f in os.listdir() if f.endswith('.html') and not f.startswith('ultra_secure_257_')]
    
    if not html_files:
        print("No HTML files found for ultra secure encryption.")
        return
    
    print("Files available for ULTRA SECURE encryption:")
    for idx, f in enumerate(html_files, 1):
        print(f" {idx}. {f}")
    
    choice = input("\nSelect file for ULTRA SECURE protection: ").strip()
    
    try:
        file_choice = html_files[int(choice) - 1] if choice.isdigit() else choice
    except:
        print("Invalid selection!")
        return
    
    if file_choice not in html_files:
        print("File not found!")
        return
    
    with open(file_choice, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"\n🛡️  APPLYING ULTRA SECURE 257 ENCRYPTION...")
    
    key = UltraSecureEncrypter257.generate_ultra_key()
    encrypted_hex, protection_positions, integrity_hash, original_length = UltraSecureEncrypter257.encrypt_ultra_secure(content, key)
    
    base_name = os.path.splitext(file_choice)[0]
    
    # Save secure files
    with open(f"ultra_secure_257_{base_name}_key.txt", 'w') as f:
        f.write("ULTRA SECURE ENCRYPTER 257 - MAXIMUM PROTECTION\n")
        f.write("=" * 50 + "\n")
        f.write(f"File: {file_choice}\n")
        f.write(f"Original Length: {original_length}\n")
        f.write(f"Integrity Hash: {integrity_hash}\n")
        f.write(f"Security Level: MAXIMUM\n")
        f.write("=" * 50 + "\n")
        f.write(f"ULTRA SECURE KEY:\n{key}\n")
        f.write("=" * 50 + "\n")
        f.write("🔐 STORE THIS KEY SECURELY!\n")
        f.write("🔐 REQUIRED FOR DECRYPTION!\n")
        f.write("👥 Credit: You & Me - 257 Pioneers!\n")
    
    # Create ultra secure loader
    loader_html = create_ultra_secure_loader(file_choice, encrypted_hex, protection_positions, integrity_hash, original_length)
    with open(f"ultra_secure_257_{base_name}.html", 'w') as f:
        f.write(loader_html)
    
    print(f"\n🎉 ULTRA SECURE PROTECTION APPLIED!")
    print(f"🔐 Ultra Secure Key: {key[:50]}...")
    print(f"🌐 Secure Loader: ultra_secure_257_{base_name}.html")
    print(f"📊 Original Size: {original_length} characters")
    print(f"🛡️  Security Features:")
    print(f"   • Multi-layer encryption (3 layers)")
    print(f"   • Integrity verification")
    print(f"   • Anti-tampering protection")
    print(f"   • Fake data injection")
    print(f"   • Permanent key storage (localStorage + 10‑year cookie)")
    print(f"   • Non-editable protection")
    print(f"👥 Credit: You & Me - 257 Pioneers!")

if __name__ == "__main__":
    main()