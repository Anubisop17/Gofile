import random,subprocess
import string
import re
from telegram.ext import CommandHandler

from bot import LOGGER,DOWNLOAD_DIR, dispatcher, CLONE_LIMIT, download_dict, download_dict_lock, Interval
from bot.helper.download_utils.ddl_generator import appdrive, gdtot
from bot.helper.drive_utils.gdriveTools import GoogleDriveHelper
from bot.helper.ext_utils.bot_utils import new_thread, get_readable_file_size, is_gdrive_link, \
    is_appdrive_link, is_gdtot_link

from bot.helper.ext_utils.fs_utils import get_path_size
from bot.helper.ext_utils.exceptions import DDLExceptionHandler
from bot.helper.status_utils.clone_status import CloneStatus
from bot.helper.telegram_helper.message_utils import sendMessage, editMessage, deleteMessage, \
    delete_all_messages, update_all_messages, sendStatusMessage
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.telegram_helper.filters import CustomFilters
from pathlib import PurePath
from .compress import CompressListener
from bot.helper.status_utils.upload_status import UploadStatus
def up(update, context):
      args = update.message.text.split(" ", maxsplit=2)
      if(len(args) > 1):
        msg2 = sendMessage(f"Processing..patch",context.bot,update.message) 
        name = " ".join(map(str, args[1:]))
        result = subprocess.run(['curl', '-T', name, 'https://pixeldrain.com/api/file/'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        file_id = re.search(r'"id":"(\w+)"', result.stdout.decode()).group(1)
        msg = f"https://pixeldrain.com/api/file/{file_id}"
        sendMessage(msg,context.bot,update.message)
        subprocess.run(["rm", "-rf",name])
        deleteMessage(context.bot, msg2)
        
        """uid = update.message.message_id
        tag = update.message.from_user.mention_html(update.message.from_user.first_name)
        gid = ''.join(random.SystemRandom().choices(string.ascii_letters + string.digits, k=12))
        listener = CompressListener(context.bot, update.message, is_archive=False, is_extract=False,)
        #up_dir = f'{DOWNLOAD_DIR}{uid}/'
        name = " ".join(map(str, args[1:]))# args[1:]
        #subprocess.run(["mv",name,up_dir])
        #ot = subprocess.Popen(["find", ".", "-name", f'{up_dir}/{name}'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #stdout, stderr = ot.communicate()
        up_path = name
        print(up_path)
        up_dir = PurePath(up_path).parents[0]
        size = get_path_size(f'{up_dir}/{name}')
        sendMessage(f"Uploading: {name}",context.bot,update.message)
        drive = GoogleDriveHelper(name, up_dir, listener)
        upload_status = UploadStatus(drive, size, gid, listener)"""
            
        '''
        with download_dict_lock:
            download_dict[uid] = upload_status
        update_all_messages()
        '''
        #drive.upload(name)
       
      else:
          sendMessage(f"Send File Name",context.bot,update.message) 
up_handler = CommandHandler(BotCommands.UpCommand, up,
                               filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True)
dispatcher.add_handler(up_handler)
