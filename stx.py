import os
import subprocess
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

BOT_TOKEN = '7527215153:AAEskBpPW5Oynu9ZO-fZednXmCzX9bL0kac'
ALLOWED_USER_ID = 7316824198

# Store user's current working directory
current_dir = os.path.expanduser("~")  # Default: home directory

async def handle_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global current_dir
    user_id = update.effective_user.id
    if user_id != ALLOWED_USER_ID:
        await update.message.reply_text("Kamu siapa?")
        return

    command = update.message.text.strip()

    # If it's a "cd" command, update the current directory
    if command.startswith("cd "):
        path = command[3:].strip()
        new_dir = os.path.abspath(os.path.join(current_dir, path))
        if os.path.isdir(new_dir):
            current_dir = new_dir
            await update.message.reply_text(f"cd {current_dir}")
        else:
            await update.message.reply_text(f"No such directory: {new_dir}")
        return

    # Run the command in the current directory
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            cwd=current_dir,
            timeout=600
        )
        output = result.stdout.strip() + "\n" + result.stderr.strip()
        output = output.strip()
        if not output:
            output = "root@stxtamfan:~#"
    except Exception as e:
        output = f"Error: {str(e)}"

    # Send output in chunks if long
    for i in range(0, len(output), 4000):
        await update.message.reply_text(output[i:i+4000])

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_command))

if __name__ == '__main__':
    print("Bot running...")
    app.run_polling()
