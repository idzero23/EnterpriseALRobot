from telegram.ext.filters import Filters
from tg_bot.modules.helper_funcs.decorators import kigcmd, kigmsg
from telegram import Update
from telegram.ext import CallbackContext
from ..modules.helper_funcs.anonymous import user_admin, AdminPerms, UserClass, resolve_user
import html
from ..modules.sql.antichannel_sql import antichannel_status, disable_antichannel, enable_antichannel

@kigcmd(command="antichannel", group=100)
@user_admin(UserClass.ADMIN, AdminPerms.CAN_RESTRICT_MEMBERS)
def set_antichannel(update: Update, context: CallbackContext):
    message = update.effective_message
    chat = update.effective_chat
    args = context.args
    u = update.effective_user
    user = resolve_user(u, message.message_id, chat)
    if len(args) > 0:
        s = args[0].lower()
        if s in ["yes", "on", "true"]:
            enable_antichannel(chat.id)
            message.reply_html("Enabled antichannel in {}".format(html.escape(chat.title)))
        elif s in ["off", "no", "false"]:
            disable_antichannel(chat.id)
            message.reply_html("Disabled antichannel in {}".format(html.escape(chat.title)))
        else:
            message.reply_text("Unrecognized arguments {}".format(s))
        return
    message.reply_html(
        "Antichannel setting is currently {} in {}".format(antichannel_status(chat.id), html.escape(chat.title)))


@kigmsg(Filters.chat_type.groups & Filters.sender_chat.channel & ~Filters.is_automatic_forward, group=110)
def eliminate_channel(update: Update, context: CallbackContext):
    message = update.effective_message
    chat = update.effective_chat
    bot = context.bot
    if not antichannel_status(chat.id):
        return
    message.delete()
    sender_chat = message.sender_chat
    bot.ban_chat_sender_chat(sender_chat_id=sender_chat.id, chat_id=chat.id)