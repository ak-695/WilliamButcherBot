from wbb import app
from wbb.utils.errors import capture_err
from wbb.utils.json_prettify import json_prettify
from wbb.utils.dbfunctions import (update_karma, get_karma, get_karmas,
    int_to_alpha, alpha_to_int)
from pyrogram import filters

__MODULE__ = "Karma"
__HELP__ = """[UPVOTE] - Use upvote keywords like "+", "+1", "thanks" etc to upvote a message.
[DOWNVOTE] - Use downvote keywords like "-", "-1", etc to downvote a message.
Reply to a message with /karma to check a user's karma
Send /karma without replying to any message to chek karma list of top 10 users"""


regex_upvote = r"^((?i)\+|\+\+|\+1|thx|tnx|ty|thank you|thanx|thanks|pro|cool|good|👍)$"
regex_downvote = r"^(\-|\-\-|\-1|👎)$"


@app.on_message(filters.text
                & filters.group
                & filters.incoming
                & filters.reply
                & filters.regex(regex_upvote)
                & ~filters.via_bot
                & ~filters.bot
                & ~filters.edited, group=3)
async def upvote(_, message):
    if message.reply_to_message.from_user.id == message.from_user.id:
        return
    chat_id = message.chat.id
    user_id = message.reply_to_message.from_user.id
    user_mention = message.reply_to_message.from_user.mention
    current_karma = await get_karma(chat_id, await int_to_alpha(user_id))
    if current_karma:
        current_karma = current_karma['karma']
        karma = current_karma + 1
        new_karma = {"karma": karma}
        await update_karma(chat_id, await int_to_alpha(user_id), new_karma)
    else:
        karma = 1
        new_karma = {"karma": karma}
        await update_karma(chat_id, await int_to_alpha(user_id), new_karma)
    await message.reply_text(
        f'Incremented Karma of {user_mention} By 1 \nTotal Points: {karma}'
    )


@app.on_message(filters.text
                & filters.group
                & filters.incoming
                & filters.reply
                & filters.regex(regex_downvote)
                & ~filters.via_bot
                & ~filters.bot
                & ~filters.edited, group=4)
async def downvote(_, message):
    if message.reply_to_message.from_user.id == message.from_user.id:
        return
    chat_id = message.chat.id
    user_id = message.reply_to_message.from_user.id
    user_mention = message.reply_to_message.from_user.mention
    current_karma = await get_karma(chat_id, await int_to_alpha(user_id))
    if current_karma:
        current_karma = current_karma['karma']
        karma = current_karma - 1
        new_karma = {"karma": karma}
        await update_karma(chat_id, await int_to_alpha(user_id), new_karma)
    else:
        karma = 1
        new_karma = {"karma": karma}
        await update_karma(chat_id, await int_to_alpha(user_id), new_karma)
    await message.reply_text(
    f'Decremented Karma Of {user_mention} By 1 \nTotal Points: {karma}'
)


@app.on_message(filters.command("karma") & filters.group)
async def karma(_, message):
    chat_id = message.chat.id

    if not message.reply_to_message:
        karma = await get_karmas(chat_id)
        msg = f"**Karma list of {message.chat.title}:- **\n"
#        output = await json_prettify(karma)
        limit = 0
        for i in karma:
            if limit > 9:
                break
            ii = ""
            user_id = await alpha_to_int(i)
            user_karma = karma[i]['karma']
            user_name = (await app.get_users(user_id)).username
            ii += f"{user_name}  {user_karma}"
            msg += f"`{ii}`\n"
            limit += 1
        await message.reply_text(msg)
    else:
        user_id = message.reply_to_message.from_user.id
        karma = await get_karma(chat_id, await int_to_alpha(user_id))
        if karma:
            karma = karma['karma']
            await message.reply_text(f'**Total Points**: __{karma}__')
        else:
            karma = 0
            await message.reply_text(f'**Total Points**: __{karma}__')

