# Django Shell Plus Commands for Seeding Data

This document provides ready-to-use commands for adding dummy data to your Deal Pipeline application using Django's shell_plus.

## Getting Started

First, make sure you have django-extensions installed and configured (already done).

To enter the Django shell with all models auto-imported:

```bash
cd backend
python manage.py shell_plus
```

## Creating Test Deals

### Quick Setup: Create Multiple Deals Across All Stages

This command creates 10+ sample deals distributed across all pipeline stages:

```python
from models.models import User, Deal
from decimal import Decimal
from datetime import datetime, timedelta
import random

# Get an analyst user (or create one if needed)
analyst = User.objects.filter(role__name='Analyst').first()

if not analyst:
    print("No Analyst user found! Please create one first.")
else:
    # Sample deals data
    deals_data = [
        # Sourced stage
        {'name': 'TechStart AI', 'company_url': 'https://techstart.ai', 'stage': 'Sourced', 'round': 'Seed', 'check_size': Decimal('500000')},
        {'name': 'CloudVentures', 'company_url': 'https://cloudventures.io', 'stage': 'Sourced', 'round': 'Pre-Seed', 'check_size': Decimal('250000')},
        {'name': 'DataFlow Systems', 'company_url': 'https://dataflow.systems', 'stage': 'Sourced', 'round': 'Seed', 'check_size': Decimal('750000')},
        
        # Screen stage
        {'name': 'FinanceFlow', 'company_url': 'https://financeflow.com', 'stage': 'Screen', 'round': 'Series A', 'check_size': Decimal('2000000')},
        {'name': 'SecureChain', 'company_url': 'https://securechain.tech', 'stage': 'Screen', 'round': 'Seed', 'check_size': Decimal('1000000')},
        
        # Diligence stage
        {'name': 'HealthTech Pro', 'company_url': 'https://healthtech.pro', 'stage': 'Diligence', 'round': 'Seed', 'check_size': Decimal('750000')},
        {'name': 'EduPlatform', 'company_url': 'https://eduplatform.online', 'stage': 'Diligence', 'round': 'Series A', 'check_size': Decimal('3000000')},
        
        # IC stage
        {'name': 'CloudNine', 'company_url': 'https://cloudnine.io', 'stage': 'IC', 'round': 'Series B', 'check_size': Decimal('5000000')},
        {'name': 'MarketPlace AI', 'company_url': 'https://marketplace-ai.com', 'stage': 'IC', 'round': 'Series A', 'check_size': Decimal('2500000')},
        
        # Invested stage
        {'name': 'DataInsights', 'company_url': 'https://datainsights.com', 'stage': 'Invested', 'round': 'Series A', 'check_size': Decimal('3000000')},
        {'name': 'GreenEnergy Tech', 'company_url': 'https://greenenergy.tech', 'stage': 'Invested', 'round': 'Seed', 'check_size': Decimal('1500000')},
        
        # Passed stage
        {'name': 'SocialConnect', 'company_url': 'https://socialconnect.app', 'stage': 'Passed', 'round': 'Pre-Seed', 'check_size': Decimal('200000')},
    ]
    
    # Create deals
    created_deals = []
    for deal_data in deals_data:
        deal = Deal.objects.create(owner=analyst, **deal_data)
        created_deals.append(deal)
        print(f"✓ Created: {deal.name} - {deal.stage}")
    
    print(f"\n✅ Successfully created {len(created_deals)} deals!")
```

### Create a Single Deal

```python
from models.models import User, Deal
from decimal import Decimal

# Get an analyst user
analyst = User.objects.filter(role__name='Analyst').first()

# Create a single deal
deal = Deal.objects.create(
    name='My Custom Deal',
    company_url='https://example.com',
    owner=analyst,
    stage='Sourced',
    round='Seed',
    check_size=Decimal('500000'),
    status='active'
)

print(f"Created: {deal.name} (ID: {deal.id})")
```

### Update an Existing Deal

```python
from models.models import Deal

# Get a deal by ID
deal = Deal.objects.get(id=1)

# Update its stage
deal.stage = 'Diligence'
deal.save()

print(f"Updated {deal.name} to stage: {deal.stage}")
```

### Create Activity Records (Optional)

Activity records are automatically created when deals are moved via the API, but you can create them manually:

```python
from models.models import Activity, Deal, User

deal = Deal.objects.first()
user = User.objects.first()

activity = Activity.objects.create(
    deal=deal,
    user=user,
    action=f"moved '{deal.name}' from Sourced to Screen"
)

print(f"Created activity: {activity.action}")
```

## Viewing Data

### List All Deals

```python
from models.models import Deal

# Get all active deals
deals = Deal.objects.filter(status='active').select_related('owner', 'owner__role')

for deal in deals:
    print(f"{deal.id}: {deal.name} - {deal.stage} - Owner: {deal.owner.username}")
```

### Count Deals by Stage

```python
from models.models import Deal
from django.db.models import Count

stage_counts = Deal.objects.filter(status='active').values('stage').annotate(count=Count('id'))

for item in stage_counts:
    print(f"{item['stage']}: {item['count']} deals")
```

### View Deal Activities

```python
from models.models import Activity, Deal

deal = Deal.objects.first()
activities = Activity.objects.filter(deal=deal).select_related('user')

print(f"\nActivities for {deal.name}:")
for activity in activities:
    print(f"  - {activity.user.username}: {activity.action} ({activity.created_at})")
```

## Cleaning Up Data

### Delete All Deals

```python
from models.models import Deal

# Delete all deals (use with caution!)
count = Deal.objects.all().count()
Deal.objects.all().delete()
print(f"Deleted {count} deals")
```

### Archive Specific Deals

```python
from models.models import Deal

# Archive deals in 'Passed' stage
passed_deals = Deal.objects.filter(stage='Passed')
count = passed_deals.update(status='archived')
print(f"Archived {count} deals")
```

## Tips

1. **Always check for existing users**: Before creating deals, make sure you have users with appropriate roles
   ```python
   User.objects.filter(role__name='Analyst').exists()
   ```

2. **Use transactions for bulk operations**: When creating many records, wrap them in a transaction
   ```python
   from django.db import transaction
   
   with transaction.atomic():
       # Your bulk create operations here
       pass
   ```

3. **Check the current state**: Before seeding, check what data already exists
   ```python
   Deal.objects.count()
   ```

4. **Exit the shell**: When done, type `exit()` or press `Ctrl+D`

## Quick Reference

| Command | Description |
|---------|-------------|
| `python manage.py shell_plus` | Enter Django shell with auto-imported models |
| `Deal.objects.all()` | Get all deals |
| `Deal.objects.filter(stage='Sourced')` | Filter deals by stage |
| `deal.save()` | Save changes to a deal |
| `Deal.objects.create(**data)` | Create a new deal |
| `exit()` | Exit the shell |

