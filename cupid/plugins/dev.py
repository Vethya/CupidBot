from pyrogram import filters
from cupid import app, sudo_only
import html
import os
import asyncio
import signal

@app.on_message(filters.text & filters.regex(r'^/exec(?: \n| |\n)([\s\S]+)'))
@sudo_only
async def execc(client, m):
    code = m.matches[0].group(1)
    exec(
        'async def __ex(client, m):' +
        ''.join([f'\n {l}' for l in code.split('\n')])
    )
    aw = await m.reply_text(
        '<b>' + 'INPUT' + '</b>\n'
        '<code>' + html.escape(code) + '</code>\n'
        '<b>' + 'OUTPUT\n' + '</b>'
    )
    output = await locals()['__ex'](client, m)
    end = '<code>'+ html.escape(str(output)) + '</code>' if output is not None else 'None'
    await aw.edit_text(
        '<b>' + 'INPUT' + '</b>\n'
        '<code>'+ html.escape(code) +'</code>\n'
        '<b>' + 'OUTPUT\n' + '</b>'
        f'<code>{end}</code>'
    )

@app.on_message(filters.text & filters.regex(r'^/(?:shell|sh|bash|term) (.+)(?:\n([\s\S]+))?'))
@sudo_only
async def run_shell(client, m):
    cmd, stdin = m.matches[0].group(1), m.matches[0].group(2)
    stdin = stdin.encode() if stdin else None
    ptext = f'<b>STDIN:</b>\n<code>{html.escape(cmd)}</code>\n'
    if stdin:
        ptext += 'stdin: \n'
        ptext += f'<code>{html.escape(stdin.decode())}</code>\n\n'
    text = ptext
    aw = await m.reply_text(text)
    proc = await asyncio.create_subprocess_shell(
        cmd, stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await proc.communicate(stdin)
    text = ptext
    text += f'STDERR: \n<code>{html.escape(stderr.decode())}</code>\n\n' if stderr else ''
    text += f'<b>STDOUT:</b>\n<code>{html.escape(stdout.decode())}</code>' if stdout else ''
    text += f'\nReturnCode: <code>{proc.returncode}</code>'
    if len(text) > 4096:
        with open('shell.txt', 'w+') as f:
            f.write(text)
        await e.client.send_file(e.chat_id, 'shell.txt')
        os.remove('shell.txt')
    else:
        await aw.edit_text(text)

@app.on_message(filters.text & filters.regex(r'^/(shutdown|poweroff)'))
@sudo_only
async def shutdown(client, m):
    await m.reply_text('Successfully shutdown!')
    os.kill(os.getpid(), signal.SIGINT)
