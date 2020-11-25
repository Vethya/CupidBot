from pyrogram import filters
from cupid import app

help_text = """Here's the help for this **Cupid Bot**:

**Available commands:**

- Picking:
• `/pick`: picks a random couple in the chat (with gender if gender support is on).
- Last Pick:
• `/last`: gets the last picked couple.
- Gender support:
• `/register <male/female>`: registers a gender.
- Caching:
• `/cachemember`: cache the member list to the database.
> aliases: `/cm`
- Stats:
• `/toplovers`: gets the lovers in the current chat.
> aliases: `/top`
• `/mystats`: if in pm gets the global pick stats. if in group gets your pick in the current group.

**Admins only:**

- Gender Support:
• `/gendersupport <on/off>`: turns on or off gender support in the current chat.
> aliases: /gs

- Autopin:
• `autopin <on/off>`: turns on or off autopin in the current chat.
> aliases: `/ap`
"""

@app.on_message(filters.text & filters.regex(r'^/help') & filters.private)
async def get_help(client, m):
    await m.reply_text(help_text, parse_mode='md')
