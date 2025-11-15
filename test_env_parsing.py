from dotenv import load_dotenv, dotenv_values
import os

# Load with explicit path
load_dotenv(dotenv_path='.env')
key = os.getenv('OPENAI_API_KEY')
print(f'Key from load_dotenv(.env): {key[:50] if key else None}...')
print(f'Length: {len(key) if key else 0}')
if key:
    print(f'Last 10 chars: ...{key[-10:]}')

# Load with dotenv_values
config = dotenv_values('.env')
key2 = config.get('OPENAI_API_KEY')
print(f'\nKey from dotenv_values(): {key2[:50] if key2 else None}...')
print(f'Length: {len(key2) if key2 else 0}')
if key2:
    print(f'Last 10 chars: ...{key2[-10:]}')

# Read directly
with open('.env', 'r') as f:
    for line in f:
        if line.startswith('OPENAI_API_KEY'):
            parts = line.split('=', 1)
            if len(parts) == 2:
                direct_key = parts[1].strip()
                print(f'\nDirect read: {direct_key[:50]}...')
                print(f'Length: {len(direct_key)}')
                print(f'Last 10 chars: ...{direct_key[-10:]}')
