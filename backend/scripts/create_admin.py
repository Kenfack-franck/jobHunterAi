#!/usr/bin/env python3
"""
Script to create or promote a user to admin role
Usage: 
  python scripts/create_admin.py --email user@example.com
  OR via Docker:
  docker compose exec backend python scripts/create_admin.py --email user@example.com
"""

import argparse
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
import sys
import os

# Add parent directory to path to import app modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.core.config import settings
from app.models.user import User


async def set_admin_role(email: str):
    """Set admin role for a user by email"""
    
    # Create async engine
    engine = create_async_engine(
        settings.DATABASE_URL,
        echo=False,
    )
    
    # Create async session
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    
    async with async_session() as session:
        # Find user by email
        stmt = select(User).where(User.email == email)
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()
        
        if not user:
            print(f"❌ User with email '{email}' not found in database")
            print(f"   Please create an account first at: {settings.FRONTEND_URL}/auth/register")
            return False
        
        # Check if already admin
        if user.role == 'admin':
            print(f"✅ User '{email}' is already an admin")
            print(f"   Name: {user.full_name}")
            print(f"   Active: {user.is_active}")
            return True
        
        # Set admin role
        user.role = 'admin'
        await session.commit()
        
        print(f"✅ Successfully promoted '{email}' to admin role!")
        print(f"   Name: {user.full_name}")
        print(f"   Active: {user.is_active}")
        print(f"\n🎯 You can now access the admin panel at: {settings.FRONTEND_URL}/admin")
        
        return True


async def list_admins():
    """List all admin users"""
    
    engine = create_async_engine(settings.DATABASE_URL, echo=False)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        stmt = select(User).where(User.role == 'admin')
        result = await session.execute(stmt)
        admins = result.scalars().all()
        
        if not admins:
            print("❌ No admin users found in database")
            return
        
        print(f"\n📋 Admin users ({len(admins)}):")
        print("-" * 80)
        for admin in admins:
            status = "✅ Active" if admin.is_active else "🔴 Blocked"
            print(f"  {admin.email:40s} {admin.full_name:20s} {status}")
        print("-" * 80)


def main():
    parser = argparse.ArgumentParser(
        description='Create or promote user to admin role',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Promote existing user to admin
  python scripts/create_admin.py --email admin@example.com
  
  # Via Docker (production)
  docker compose exec backend python scripts/create_admin.py --email admin@example.com
  
  # List all admins
  python scripts/create_admin.py --list
        """
    )
    
    parser.add_argument(
        '--email',
        type=str,
        help='Email of the user to promote to admin'
    )
    
    parser.add_argument(
        '--list',
        action='store_true',
        help='List all admin users'
    )
    
    args = parser.parse_args()
    
    if args.list:
        asyncio.run(list_admins())
    elif args.email:
        success = asyncio.run(set_admin_role(args.email))
        sys.exit(0 if success else 1)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()
