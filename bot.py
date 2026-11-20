import logging
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# Behtareen logging setup taake har ghalti aur ghalib notice ho sake
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Yahan apna asal API Token paste karein
TOKEN = '9222638142:AAE8t8rwnOlQpnLgt3I4AELg0VRfcF8ft2M'
DOWNLOAD_DIR = 'books'

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Assalam-o-Alaikum! Main aapki e-books store karne ke liye hazir hoon. "
        "Bas koi bhi document ya PDF mujhe bhejein."
    )

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    document = update.message.document
    
    if not document:
        return

    # Folder create karna agar pehle se nahi hai
    if not os.path.exists(DOWNLOAD_DIR):
        os.makedirs(DOWNLOAD_DIR)

    status_message = await update.message.reply_text(f"File {document.file_name} receive ho gayi hai, download ho rahi hai...")

    try:
        # File ka object get karna
        file_obj = await context.bot.get_file(document.file_id)
        
        # Mehfooz karne ka mukammal path
        file_path = os.path.join(DOWNLOAD_DIR, document.file_name)
        
        # File download aur save karna
        await file_obj.download_to_drive(custom_path=file_path)
        
        await status_message.edit_text(f"Zabardast! {document.file_name} kamyabi ke sath save ho gayi hai.")
        logging.info(f"File {document.file_name} saved successfully by user {user.id}")

    except Exception as e:
        await status_message.edit_text("Afsoos! File save karne mein masla aaya hai. Dobara koshish karein.")
        logging.error(f"Error saving file: {e}")

if __name__ == '__main__':
    # Bot Application build karna
    application = ApplicationBuilder().token(TOKEN).build()

    # Handlers lagana
    application.add_handler(MessageHandler(filters.COMMAND & filters.Command(['start']), start_command))
    application.add_handler(MessageHandler(filters.Document.ALL, handle_document))

    print("Bot kamyabi ke sath shuru ho gaya hai. Polling jaari hai...")
    application.run_polling()
