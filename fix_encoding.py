import os

with open('frontend/components.py', 'r', encoding='utf-8') as f:
    text = f.read()

replacements = {
    'ðŸ§ ': '&#x1F9E0;',
    'Â·': '&middot;',
    'ðŸ“„': '&#x1F4C4;',
    'ðŸŸ¢': '&#x1F7E2;',
    'ðŸ”´': '&#x1F534;',
    'ðŸ‘¤': '&#x1F464;',
    'â€”': '&mdash;',
    'â”€': '-',
    '🤖': '&#x1F916;',
    'ðŸ¤–': '&#x1F916;',
    'â€¦': '&hellip;',
    'ðŸ”Ž': '&#x1F50D;',
    'ðŸŽ¯': '&#x1F3AF;',
    'âš¡': '&#x26A1;',
    'ðŸ’¬': '&#x1F4AC;',
    'ðŸ›¡ï¸ ': '&#x1F6E1;&#xFE0F;',
    'ðŸ›¡': '&#x1F6E1;',
    'ðŸ”’': '&#x1F512;'
}

for k, v in replacements.items():
    text = text.replace(k, v)

with open('frontend/components.py', 'w', encoding='utf-8') as f:
    f.write(text)
