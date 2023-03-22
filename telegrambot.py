from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from pytube import YouTube
import os

TOKEN = 'YOUR-TOKEN-HERE'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Welcome, {update.effective_user.first_name}! Send a YouTube URL')

async def wrong_format(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Please send a YouTube URL.')

async def download_from_url(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    await update.message.reply_text(
            "Thanks! I'm processing your request...⏳"
        )

    #Get url from message
    url = update.message.text

    try:
        #Get audio with pytube
        p = YouTube(str(url))
        audio = p.streams.filter(only_audio=True).first()
        out_file = audio.download(output_path='/tmp')
        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp3'
        os.rename(out_file, new_file)

        #Send the audio
        await update.message.reply_audio(
            open(new_file, 'rb')
        )

        await update.message.reply_text(
            f'{audio.title} has been successfully downloaded. 🎉'
        )

        #Delete audio from computer
        os.remove(f'{new_file}')

    except:
        await update.message.reply_text(
            'An error occurred. 😔 Check the URL or try later. If the error persists, the URL may be unavailable to download.'
        )



app = ApplicationBuilder().token(TOKEN).read_timeout(30).write_timeout(30).build()

app.add_handler(CommandHandler('start', start))
app.add_handler(MessageHandler(filters.TEXT, download_from_url))
app.add_handler(MessageHandler(~ filters.TEXT, wrong_format))

app.run_polling()
