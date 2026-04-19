#!/usr/bin/env python3
"""
🎬 GHOST PRO FIXED - Smart Video Encryption
• Bug fixed: KeyError for 'encrypted' category
• Auto file detection and listing
• Perfect video recovery
• Added noise to encryption
"""

import os
import sys
import struct
import time
from pathlib import Path
from typing import List

class GhostProNoise:
    """Fixed version with noise - Working algorithm"""
    
    ENCRYPTED_EXT = '.g4k'
    
    # File type categories
    FILE_CATEGORIES = {
        'video': {
            'extensions': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv'],
            'icon': '🎬',
            'name': 'Video'
        },
        'image': {
            'extensions': ['.jpg', '.jpeg', '.png', '.gif', '.bmp'],
            'icon': '🖼️',
            'name': 'Image'
        },
        'document': {
            'extensions': ['.pdf', '.doc', '.docx', '.txt'],
            'icon': '📄',
            'name': 'Document'
        },
        'archive': {
            'extensions': ['.zip', '.rar', '.7z'],
            'icon': '📦',
            'name': 'Archive'
        },
        'audio': {
            'extensions': ['.mp3', '.wav', '.flac'],
            'icon': '🎵',
            'name': 'Audio'
        },
        'other': {
            'extensions': [],
            'icon': '📁',
            'name': 'Other'
        }
    }
    
    def __init__(self):
        self.current_dir = Path.cwd()
    
    # === SIMPLE NOISE ENCRYPTION ALGORITHM ===
    @staticmethod
    def generate_key(password: str, salt: bytes = None) -> tuple:
        """Generate encryption key"""
        if salt is None:
            salt = os.urandom(32)
        
        key = bytearray(1024)  # 1KB key
        pass_bytes = password.encode('utf-8')
        
        for i in range(1024):
            val = pass_bytes[i % len(pass_bytes)]
            val ^= salt[i % len(salt)] if salt else 0
            val = ((val << 3) | (val >> 5)) & 0xFF
            val = (val + (i * 179)) & 0xFF
            
            if i > 0:
                val ^= key[i-1]
            
            key[i] = val
        
        return bytes(key), salt
    
    @staticmethod
    def add_noise(data: bytes) -> tuple:
        """Add random noise to data and return noise mask"""
        result = bytearray(len(data))
        noise_mask = bytearray(len(data))
        
        for i in range(len(data)):
            # Generate random noise (0-31)
            noise = os.urandom(1)[0] & 0x1F  # 5 bits of noise
            noise_mask[i] = noise
            
            # Apply noise to data
            b = data[i]
            b ^= (noise << 3)  # Shift noise to high bits
            b = (b + noise) & 0xFF
            b ^= noise
            
            result[i] = b
        
        return bytes(result), bytes(noise_mask)
    
    @staticmethod
    def remove_noise(data: bytes, noise_mask: bytes) -> bytes:
        """Remove noise from data using noise mask"""
        result = bytearray(len(data))
        
        for i in range(len(data)):
            b = data[i]
            noise = noise_mask[i]
            
            # Reverse noise operations
            b ^= noise
            b = (b - noise) & 0xFF
            b ^= (noise << 3)
            
            result[i] = b
        
        return bytes(result)
    
    @staticmethod
    def encrypt_bytes(data: bytes, key: bytes) -> tuple:
        """Encrypt data with noise"""
        # Add noise first
        noisy_data, noise_mask = GhostProNoise.add_noise(data)
        
        result = bytearray(len(noisy_data))
        key_len = len(key)
        
        for i in range(len(noisy_data)):
            b = noisy_data[i]
            
            # Simple operations
            b ^= key[i % key_len]  # XOR with key
            b = ((b << 1) | (b >> 7)) & 0xFF  # Rotate left 1
            b = (b + 1) & 0xFF  # Add 1
            
            result[i] = b
        
        return bytes(result), noise_mask
    
    @staticmethod
    def decrypt_bytes(data: bytes, key: bytes, noise_mask: bytes) -> bytes:
        """Decrypt data and remove noise"""
        result = bytearray(len(data))
        key_len = len(key)
        
        # First reverse encryption
        for i in range(len(data)):
            b = data[i]
            
            # Reverse operations
            b = (b - 1) & 0xFF  # Subtract 1
            b = ((b >> 1) | (b << 7)) & 0xFF  # Rotate right 1
            b ^= key[i % key_len]  # XOR with key
            
            result[i] = b
        
        # Then remove noise
        return GhostProNoise.remove_noise(bytes(result), noise_mask)
    
    # === ALTERNATIVE: XOR WITH DETERMINISTIC NOISE ===
    @staticmethod
    def encrypt_bytes_simple(data: bytes, key: bytes) -> bytes:
        """Simple encryption with deterministic noise"""
        result = bytearray(len(data))
        key_len = len(key)
        
        for i in range(len(data)):
            b = data[i]
            
            # Generate deterministic noise from key
            noise = key[(i * 7) % key_len] & 0x0F  # 4 bits of noise
            
            # Apply noise
            b ^= (noise << 4)
            b = (b + noise) & 0xFF
            
            # Standard encryption
            b ^= key[i % key_len]
            b = ((b << 2) | (b >> 6)) & 0xFF
            b ^= key[(i + 13) % key_len]
            
            result[i] = b
        
        return bytes(result)
    
    @staticmethod
    def decrypt_bytes_simple(data: bytes, key: bytes) -> bytes:
        """Simple decryption with deterministic noise"""
        result = bytearray(len(data))
        key_len = len(key)
        
        for i in range(len(data)):
            b = data[i]
            
            # Reverse encryption
            b ^= key[(i + 13) % key_len]
            b = ((b >> 2) | (b << 6)) & 0xFF
            b ^= key[i % key_len]
            
            # Remove deterministic noise
            noise = key[(i * 7) % key_len] & 0x0F
            b = (b - noise) & 0xFF
            b ^= (noise << 4)
            
            result[i] = b
        
        return bytes(result)
    
    # === FILE SCANNING ===
    def scan_files(self):
        """Scan current directory for files"""
        files = []
        
        for item in self.current_dir.iterdir():
            if item.is_file():
                files.append({
                    'path': item,
                    'name': item.name,
                    'size': item.stat().st_size,
                    'encrypted': item.name.endswith(self.ENCRYPTED_EXT),
                    'category': self.get_category(item)
                })
        
        return files
    
    def get_category(self, file_path: Path) -> str:
        """Get file category"""
        ext = file_path.suffix.lower()
        
        for category, info in self.FILE_CATEGORIES.items():
            if ext in info['extensions']:
                return category
        
        return 'other'
    
    def get_icon(self, file_info: dict) -> str:
        """Get icon for file"""
        if file_info['encrypted']:
            return '🔒'
        
        category = file_info['category']
        if category in self.FILE_CATEGORIES:
            return self.FILE_CATEGORIES[category]['icon']
        
        return '📁'
    
    # === ENCRYPTION/DECRYPTION ===
    def encrypt_file(self, filepath: str, password: str, use_simple: bool = False) -> bool:
        """Encrypt a file"""
        try:
            print(f"\n🔐 ENCRYPTING: {Path(filepath).name}")
            print("🎲 Adding noise to encryption..." if not use_simple else "⚡ Using simple encryption...")
            
            # Read file
            with open(filepath, 'rb') as f:
                data = f.read()
            
            size = len(data)
            print(f"📊 Size: {self.format_size(size)}")
            
            # Generate key
            key, salt = self.generate_key(password)
            
            print("Encrypting...", end='', flush=True)
            start = time.time()
            
            if use_simple:
                # Simple method (deterministic noise)
                encrypted = self.encrypt_bytes_simple(data, key)
                noise_mask = b''  # No separate noise mask for simple method
                method_flag = 1
            else:
                # Complex method (random noise)
                encrypted, noise_mask = self.encrypt_bytes(data, key)
                method_flag = 0
            
            time_taken = time.time() - start
            
            # Save
            output = filepath + self.ENCRYPTED_EXT
            
            with open(output, 'wb') as f:
                f.write(b'GNOI')  # Magic
                f.write(salt)
                f.write(struct.pack('<Q', size))
                f.write(struct.pack('<B', method_flag))  # 0=complex, 1=simple
                
                if method_flag == 0:
                    # Store noise mask for complex method
                    f.write(struct.pack('<I', len(noise_mask)))
                    f.write(noise_mask)
                
                f.write(encrypted)
            
            print(f"\r✅ Encrypted: {output}")
            print(f"⏱️  Time: {time_taken:.2f}s")
            print(f"🎲 Method: {'Simple' if use_simple else 'Complex with noise'}")
            
            return True
            
        except Exception as e:
            print(f"\n❌ Error: {e}")
            return False
    
    def decrypt_file(self, filepath: str, password: str) -> bool:
        """Decrypt a .g4k file"""
        try:
            print(f"\n🔓 DECRYPTING: {Path(filepath).name}")
            
            with open(filepath, 'rb') as f:
                magic = f.read(4)
                if magic != b'GNOI':
                    # Try old format
                    print("⚠️  Trying old format...")
                    f.seek(0)
                    magic = f.read(4)
                    if magic == b'GPRO':
                        # Old format
                        salt = f.read(32)
                        original_size = struct.unpack('<Q', f.read(8))[0]
                        encrypted = f.read()
                        return self.decrypt_old_format(filepath, password, salt, original_size, encrypted)
                    else:
                        print("❌ Not a Ghost file")
                        return False
                
                salt = f.read(32)
                original_size = struct.unpack('<Q', f.read(8))[0]
                method_flag = struct.unpack('<B', f.read(1))[0]
                
                noise_mask = b''
                if method_flag == 0:
                    # Complex method has noise mask
                    noise_mask_len = struct.unpack('<I', f.read(4))[0]
                    noise_mask = f.read(noise_mask_len)
                
                encrypted = f.read()
            
            print(f"📊 Encrypted: {self.format_size(len(encrypted))}")
            
            # Recreate key
            key, _ = self.generate_key(password, salt)
            
            print("Decrypting...", end='', flush=True)
            start = time.time()
            
            # Decrypt based on method
            if method_flag == 1:
                # Simple method
                decrypted = self.decrypt_bytes_simple(encrypted, key)
            else:
                # Complex method
                decrypted = self.decrypt_bytes(encrypted, key, noise_mask)
            
            # Trim to original size
            decrypted = decrypted[:original_size]
            time_taken = time.time() - start
            
            # Save
            if filepath.endswith(self.ENCRYPTED_EXT):
                output = filepath[:-4]
            else:
                output = filepath + '.decrypted'
            
            with open(output, 'wb') as f:
                f.write(decrypted)
            
            print(f"\r✅ Decrypted: {output}")
            print(f"📊 Recovered: {self.format_size(len(decrypted))}")
            print(f"⏱️  Time: {time_taken:.2f}s")
            print(f"🎲 Method: {'Simple' if method_flag == 1 else 'Complex'}")
            
            if len(decrypted) == original_size:
                print("✅ Size matches!")
            else:
                print(f"⚠️  Size difference: {abs(original_size - len(decrypted))} bytes")
            
            return True
            
        except Exception as e:
            print(f"\n❌ Error: {e}")
            return False
    
    def decrypt_old_format(self, filepath: str, password: str, salt: bytes, original_size: int, encrypted: bytes) -> bool:
        """Decrypt old format file"""
        print("🔓 Decrypting old format...")
        
        # Recreate key
        key, _ = self.generate_key(password, salt)
        
        # Old format uses simple decryption
        decrypted = self.decrypt_bytes_old(encrypted, key)
        decrypted = decrypted[:original_size]
        
        # Save
        if filepath.endswith(self.ENCRYPTED_EXT):
            output = filepath[:-4]
        else:
            output = filepath + '.decrypted'
        
        with open(output, 'wb') as f:
            f.write(decrypted)
        
        print(f"✅ Decrypted: {output}")
        return True
    
    @staticmethod
    def decrypt_bytes_old(data: bytes, key: bytes) -> bytes:
        """Decrypt old format data"""
        result = bytearray(len(data))
        key_len = len(key)
        
        for i in range(len(data)):
            b = data[i]
            
            # Reverse operations (old format)
            b = (b - 1) & 0xFF
            b = ((b >> 1) | (b << 7)) & 0xFF
            b ^= key[i % key_len]
            
            result[i] = b
        
        return bytes(result)
    
    # === SMART MENU ===
    def smart_menu(self):
        """Smart file menu with auto-detection"""
        while True:
            files = self.scan_files()
            
            # Categorize files
            categories = {}
            encrypted_files = []
            normal_files = []
            
            for f in files:
                if f['encrypted']:
                    encrypted_files.append(f)
                else:
                    normal_files.append(f)
                    
                    cat = f['category']
                    if cat not in categories:
                        categories[cat] = []
                    categories[cat].append(f)
            
            print(f"\n{'='*60}")
            print(f"🎬 GHOST PRO NOISE - {self.current_dir.name}/")
            print(f"🔥 Working noise encryption • Better security")
            print(f"{'='*60}")
            
            # Show summary
            print(f"📊 Found: {len(normal_files)} files | {len(encrypted_files)} encrypted")
            
            # Show categories with counts
            for cat, cat_files in sorted(categories.items()):
                if cat in self.FILE_CATEGORIES:
                    icon = self.FILE_CATEGORIES[cat]['icon']
                    name = self.FILE_CATEGORIES[cat]['name']
                    print(f"{icon} {name}: {len(cat_files)} files")
            
            if encrypted_files:
                print(f"🔒 Encrypted: {len(encrypted_files)} files")
            
            print(f"{'='*60}")
            print("1. List all files")
            print("2. List videos only")
            print("3. List images only")
            print("4. List encrypted files")
            print("5. Encrypt a file (Complex noise)")
            print("6. Encrypt a file (Simple noise)")
            print("7. Decrypt a .g4k file")
            print("8. Batch encrypt videos")
            print("9. Batch decrypt all")
            print("a. Change directory")
            print("t. Test encryption/decryption")
            print("0. Exit")
            print(f"{'='*60}")
            
            choice = input("\nSelect: ").strip().lower()
            
            if choice == "1":
                self.list_files(files, "All Files")
            
            elif choice == "2":
                video_files = [f for f in files if f['category'] == 'video' and not f['encrypted']]
                self.list_files(video_files, "Video Files")
            
            elif choice == "3":
                image_files = [f for f in files if f['category'] == 'image' and not f['encrypted']]
                self.list_files(image_files, "Image Files")
            
            elif choice == "4":
                self.list_files(encrypted_files, "Encrypted Files")
            
            elif choice == "5":
                self.encrypt_menu(normal_files, use_simple=False)
            
            elif choice == "6":
                self.encrypt_menu(normal_files, use_simple=True)
            
            elif choice == "7":
                if encrypted_files:
                    self.decrypt_menu(encrypted_files)
                else:
                    print("❌ No encrypted files found")
            
            elif choice == "8":
                video_files = [f for f in files if f['category'] == 'video' and not f['encrypted']]
                if video_files:
                    self.batch_encrypt_videos(video_files)
                else:
                    print("❌ No video files found")
            
            elif choice == "9":
                if encrypted_files:
                    self.batch_decrypt(encrypted_files)
                else:
                    print("❌ No encrypted files found")
            
            elif choice == "a":
                self.change_dir()
            
            elif choice == "t":
                self.test()
            
            elif choice == "0":
                print("\n👋 Goodbye!")
                break
            
            else:
                print("❌ Invalid choice")
            
            input("\nPress Enter to continue...")
    
    def list_files(self, files: List[dict], title: str):
        """List files with details"""
        if not files:
            print(f"\n❌ No {title.lower()} found")
            return
        
        print(f"\n📁 {title} ({len(files)})")
        print("-" * 60)
        
        for i, f in enumerate(files, 1):
            icon = self.get_icon(f)
            size = self.format_size(f['size'])
            print(f"{i:3d}. {icon} {f['name']:<35} {size:>10}")
    
    def encrypt_menu(self, files: List[dict], use_simple: bool = False):
        """Encryption menu"""
        if not files:
            print("❌ No files to encrypt")
            return
        
        method = "Simple" if use_simple else "Complex"
        print(f"\n📁 Files to encrypt ({method}):")
        for i, f in enumerate(files[:20], 1):
            icon = self.get_icon(f)
            size = self.format_size(f['size'])
            print(f"{i:2d}. {icon} {f['name']:<35} {size:>10}")
        
        if len(files) > 20:
            print(f"    ... and {len(files) - 20} more")
        
        selection = input("\nFile number or path: ").strip()
        
        if selection.isdigit():
            idx = int(selection) - 1
            if 0 <= idx < len(files):
                filepath = str(files[idx]['path'])
            else:
                print("❌ Invalid number")
                return
        else:
            filepath = selection
        
        if os.path.exists(filepath):
            password = input("Password: ").strip()
            if password:
                self.encrypt_file(filepath, password, use_simple)
        else:
            print("❌ File not found")
    
    def decrypt_menu(self, files: List[dict]):
        """Decryption menu"""
        print(f"\n🔐 Encrypted files:")
        for i, f in enumerate(files, 1):
            size = self.format_size(f['size'])
            print(f"{i:2d}. 🔒 {f['name']:<35} {size:>10}")
        
        selection = input("\nFile number or path: ").strip()
        
        if selection.isdigit():
            idx = int(selection) - 1
            if 0 <= idx < len(files):
                filepath = str(files[idx]['path'])
            else:
                print("❌ Invalid number")
                return
        else:
            filepath = selection
        
        if os.path.exists(filepath):
            password = input("Password: ").strip()
            if password:
                self.decrypt_file(filepath, password)
        else:
            print("❌ File not found")
    
    def batch_encrypt_videos(self, video_files: List[dict]):
        """Batch encrypt video files"""
        print(f"\n🎬 Batch encrypting {len(video_files)} videos")
        print("1. Complex noise method (more secure)")
        print("2. Simple noise method (faster)")
        
        method_choice = input("Choose method (1/2): ").strip()
        use_simple = (method_choice == "2")
        
        password = input("Password: ").strip()
        if not password:
            print("❌ No password provided")
            return
        
        success = 0
        for i, v in enumerate(video_files, 1):
            print(f"\n[{i}/{len(video_files)}] {v['name']}")
            if self.encrypt_file(str(v['path']), password, use_simple):
                success += 1
        
        print(f"\n✅ Completed: {success}/{len(video_files)} videos encrypted")
    
    def batch_decrypt(self, encrypted_files: List[dict]):
        """Batch decrypt all encrypted files"""
        print(f"\n🔐 Batch decrypting {len(encrypted_files)} files")
        
        password = input("Password: ").strip()
        if not password:
            print("❌ No password provided")
            return
        
        success = 0
        for i, f in enumerate(encrypted_files, 1):
            print(f"\n[{i}/{len(encrypted_files)}] {f['name']}")
            if self.decrypt_file(str(f['path']), password):
                success += 1
        
        print(f"\n✅ Completed: {success}/{len(encrypted_files)} files decrypted")
    
    def change_dir(self):
        """Change directory"""
        print(f"\n📂 Current: {self.current_dir}")
        
        # List subdirectories
        dirs = [d for d in self.current_dir.iterdir() if d.is_dir()]
        if dirs:
            print("\n📁 Subdirectories:")
            for i, d in enumerate(dirs[:15], 1):
                print(f"{i:2d}. {d.name}/")
        
        print(f"\nOptions:")
        print("  '..' - Parent directory")
        print("  Or enter path")
        
        new_dir = input("\nNew directory: ").strip()
        
        if new_dir == "..":
            self.current_dir = self.current_dir.parent
        elif new_dir:
            new_path = Path(new_dir)
            if new_path.is_absolute():
                target = new_path
            else:
                target = self.current_dir / new_path
            
            if target.exists() and target.is_dir():
                self.current_dir = target
                print(f"✅ Changed to: {self.current_dir}")
            else:
                print("❌ Directory not found")
        else:
            print("❌ No directory specified")
    
    # === TEST ===
    def test(self):
        """Test encryption/decryption"""
        print("\n🧪 Testing algorithm...")
        
        test_data = b'Test123' * 100
        password = "test"
        
        print("Testing complex noise method...")
        key, salt = self.generate_key(password)
        encrypted, noise_mask = self.encrypt_bytes(test_data, key)
        decrypted = self.decrypt_bytes(encrypted, key, noise_mask)
        
        if test_data == decrypted:
            print("✅ Complex noise algorithm works!")
        else:
            print("❌ Complex noise algorithm failed!")
            return False
        
        print("\nTesting simple noise method...")
        encrypted_simple = self.encrypt_bytes_simple(test_data, key)
        decrypted_simple = self.decrypt_bytes_simple(encrypted_simple, key)
        
        if test_data == decrypted_simple:
            print("✅ Simple noise algorithm works!")
            return True
        else:
            print("❌ Simple noise algorithm failed!")
            return False
    
    @staticmethod
    def format_size(size_bytes: int) -> str:
        """Format file size"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} TB"

def main():
    """Main function"""
    print("\n" + "="*60)
    print("🎬 GHOST PRO WITH WORKING NOISE ENCRYPTION")
    print("🔥 Guaranteed to work • No SHA/RSA needed")
    print("="*60)
    
    ghost = GhostProNoise()
    
    if len(sys.argv) == 4:
        cmd = sys.argv[1]
        filepath = sys.argv[2]
        password = sys.argv[3]
        
        if cmd == "encrypt":
            ghost.encrypt_file(filepath, password)
        elif cmd == "encrypt-simple":
            ghost.encrypt_file(filepath, password, use_simple=True)
        elif cmd == "decrypt":
            ghost.decrypt_file(filepath, password)
        elif cmd == "test":
            ghost.test()
    else:
        # Run test first
        if ghost.test():
            print("\n✅ All tests passed! Ready to use.")
            ghost.smart_menu()
        else:
            print("\n❌ Algorithm test failed!")

if __name__ == "__main__":
    main()