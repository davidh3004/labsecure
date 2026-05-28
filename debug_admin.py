import sys
import os

# Add project root to python path to import backend modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.db.firebase_client import init_firebase
from backend.db.repositories import AdminRepository
from backend.db.schemas import AdminCreate

def debug_admin():
    print("Initializing Firebase...")
    init_firebase()
    
    print("Fetching all admins...")
    admins = AdminRepository.get_all()
    print(f"Found {len(admins)} admins")
    
    for admin in admins:
        print(f"- id: {admin.id}, username: {admin.username}")
        # Test password verification
        is_valid = AdminRepository.verify_password("admin", admin.password_hash)
        print(f"  Password 'admin' is valid? {is_valid}")
        print(f"  Hash: {admin.password_hash}")

    if not admins:
        print("No admins found, creating one now...")
        admin = AdminRepository.create(AdminCreate(username="admin", password="admin"))
        print(f"Created admin {admin.id}")

if __name__ == "__main__":
    debug_admin()
