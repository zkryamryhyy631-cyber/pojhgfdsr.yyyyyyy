# -*- coding: utf-8 -*-
import os
import telebot
from telebot import types
from collections import defaultdict

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_IDS = [7145036494]
CHANNEL = "@pkwbiwjwbekeekkw"
CHANNEL_URL = "https://t.me/pkwbiwjwbekeekkw"
ADMIN_URL = "https://t.me/TQ4YE"
STORE_NAME = "\u0647\u0644\u0627 \u0641\u064a \u0645\u062a\u062c\u0631 \u0627\u0631\u0642\u0645 \u0648\u0627\u062d\u062f \u0641\u064a \u0627\u0644\u0639\u0627\u0644\u0645 \u0645\u062a\u062c\u0631 \u0627\u0628\u0644\u064a\u0633 \u0634\u062e\u0635\u064a\u0627 \u064a\u0631\u062d\u0628 \u0628\u0643\u0645"

bot = telebot.TeleBot(TOKEN, parse_mode="HTML", threaded=True)
pts = defaultdict(int)
invited = defaultdict(set)
ads_watched = defaultdict(int)
state = {}

def is_admin(uid): return uid in ADMIN_IDS
def get_pts(uid): return 999999999 if is_admin(uid) else pts.get(uid,0)
def is_sub(uid):
    if is_admin(uid): return True
    try: return bot.get_chat_member(CHANNEL, uid).status in ('member','administrator','creator')
    except: return False

def sub_kb():
    mk = types.InlineKeyboardMarkup()
    mk.add(types.InlineKeyboardButton("\u0627\u0634\u062a\u0631\u0643", url=CHANNEL_URL))
    mk.add(types.InlineKeyboardButton("\u062a\u062d\u0642\u0642", callback_data="check_sub"))
    return mk

def main_menu():
    mk = types.InlineKeyboardMarkup(row_width=2)
    mk.add(
        types.InlineKeyboardButton("\u0627\u0631\u0642\u0627\u0645 \u0648\u0647\u0645\u064a", callback_data="cat_nums"),
        types.InlineKeyboardButton("\u0641\u0643 \u062d\u0638\u0631", callback_data="cat_unban"),
        types.InlineKeyboardButton("\u0627\u0631\u0628\u062d 2 \u0646\u0642\u0637\u0629 \u0639\u0646 \u0643\u0644 \u062f\u0639\u0648\u0629", callback_data="invite"),
        types.InlineKeyboardButton("\u0642\u0633\u0645 \u0627\u0644\u0627\u0639\u0644\u0627\u0646\u0627\u062a", callback_data="ads"),
        types.InlineKeyboardButton("\u0627\u0633\u062a\u0636\u0627\u0641\u0629 \u0645\u0644\u0641\u0627\u062a", callback_data="cat_files"),
        types.InlineKeyboardButton("\u0631\u0635\u064a\u062f\u064a", callback_data="my_pts"),
        types.InlineKeyboardButton("\u062a\u0648\u0627\u0635\u0644 \u0645\u0639 \u0627\u0644\u0627\u062f\u0645\u0646", url=ADMIN_URL)
    )
    return mk

def nums_menu():
    mk = types.InlineKeyboardMarkup(row_width=2)
    mk.add(
        types.InlineKeyboardButton("\u0627\u0645\u0631\u064a\u0643\u0627 [10]", callback_data="num_usa"),
        types.InlineKeyboardButton("\u0628\u0631\u064a\u0637\u0627\u0646\u064a\u0627 [10]", callback_data="num_uk"),
        types.InlineKeyboardButton("\u0627\u0644\u064a\u0645\u0646 [10]", callback_data="num_ye"),
        types.InlineKeyboardButton("\u0631\u062c\u0648\u0639", callback_data="back_main")
    )
    return mk

def unban_menu():
    mk = types.InlineKeyboardMarkup(row_width=2)
    mk.add(
        types.InlineKeyboardButton("\u0648\u0627\u062a\u0633 [15]", callback_data="un_whats"),
        types.InlineKeyboardButton("\u062a\u0644\u064a\u062c\u0631\u0627\u0645 [15]", callback_data="un_tele"),
        types.InlineKeyboardButton("\u0627\u064a\u0645\u0648 [15]", callback_data="un_imo"),
        types.InlineKeyboardButton("\u0631\u062c\u0648\u0639", callback_data="back_main")
    )
    return mk

def ads_menu():
    mk = types.InlineKeyboardMarkup(row_width=1)
    mk.add(
        types.InlineKeyboardButton("\u0634\u0627\u0647\u062f \u0627\u0639\u0644\u0627\u0646 +1 \u0646\u0642\u0637\u0629", callback_data="watch_ad"),
        types.InlineKeyboardButton("\u0631\u062c\u0648\u0639", callback_data="back_main")
    )
    return mk

@bot.message_handler(commands=['start','myid'])
def start_cmd(m):
    try:
        if m.text.startswith('/myid'):
            bot.reply_to(m, f"ID: {m.from_user.id}\nPoints: {get_pts(m.from_user.id)}\nInvited: {len(invited[m.from_user.id])}")
            return

        # نظام الدعوة - اذا دخل برابط دعوة
        ref_id = None
        if len(m.text.split()) > 1:
            arg = m.text.split()[1]
            if arg.startswith('ref_'):
                try: ref_id = int(arg.replace('ref_',''))
                except: pass

        if ref_id and ref_id != m.from_user.id and m.from_user.id not in invited[ref_id]:
            if not is_admin(ref_id):
                pts[ref_id] += 2
            invited[ref_id].add(m.from_user.id)
            try: bot.send_message(ref_id, f"\u0645\u0628\u0631\u0648\u0643 \u0634\u062e\u0635 \u062c\u062f\u064a\u062f \u062f\u062e\u0644 \u0628\u0631\u0627\u0628\u0637\u0643\n\u0631\u0628\u062d\u062a 2 \u0646\u0642\u0637\u0629\n\u0631\u0635\u064a\u062f\u0643 \u0627\u0644\u0627\u0646: {get_pts(ref_id)}")
            except: pass

        if not is_sub(m.from_user.id):
            bot.send_message(m.chat.id, f"{STORE_NAME}\n\n\u064a\u062c\u0628 \u0627\u0644\u0627\u0634\u062a\u0631\u0627\u0643 \u0627\u0648\u0644\u0627", reply_markup=sub_kb())
            return

        bot.send_message(m.chat.id, f"{STORE_NAME}\n\n\u0631\u0635\u064a\u062f\u0643: {get_pts(m.from_user.id)}\n\u0627\u062f\u0639 \u0627\u0635\u062d\u0627\u0628\u0643 \u0648\u0627\u0631\u0628\u062d 2 \u0639\u0644\u0649 \u0643\u0644 \u0648\u0627\u062d\u062f", reply_markup=main_menu())
    except Exception as e:
        bot.reply_to(m, f"Error {e}")

@bot.callback_query_handler(func=lambda c: True)
def all_cb(c):
    try:
        bot.answer_callback_query(c.id)
        uid = c.from_user.id
        d = c.data

        if d == "check_sub":
            if is_sub(uid): bot.edit_message_text(f"{STORE_NAME}\n\u062a\u0645 \u0627\u0644\u0627\u0634\u062a\u0631\u0627\u0643", c.message.chat.id, c.message.message_id, reply_markup=main_menu())
            return
        if d == "back_main":
            bot.edit_message_text(f"{STORE_NAME}\n\u0631\u0635\u064a\u062f\u0643: {get_pts(uid)}", c.message.chat.id, c.message.message_id, reply_markup=main_menu())
            return
        if d == "cat_nums":
            bot.edit_message_text("\u0627\u0631\u0642\u0627\u0645 \u0648\u0647\u0645\u064a:", c.message.chat.id, c.message.message_id, reply_markup=nums_menu())
            return
        if d == "cat_unban":
            bot.edit_message_text("\u0641\u0643 \u062d\u0638\u0631:", c.message.chat.id, c.message.message_id, reply_markup=unban_menu())
            return
        if d == "cat_files":
            state[uid] = "file"
            bot.send_message(c.message.chat.id, "\u0627\u0631\u0633\u0644 \u0627\u0644\u0645\u0644\u0641 \u0627\u0644\u0627\u0646 - \u0627\u0644\u0628\u0648\u062a \u064a\u0633\u062a\u0636\u064a\u0641\u0647 \u0644\u0643 [20 \u0646\u0642\u0637\u0629]")
            return
        if d == "invite":
            bot_info = bot.get_me()
            link = f"https://t.me/{bot_info.username}?start=ref_{uid}"
            bot.send_message(c.message.chat.id, f"\u0631\u0627\u0628\u0637 \u062f\u0639\u0648\u062a\u0643 \u0627\u0644\u062e\u0627\u0635:\n{link}\n\n\u0643\u0644 \u0634\u062e\u0635 \u064a\u062f\u062e\u0644 \u0645\u0646 \u0631\u0627\u0628\u0637\u0643 \u062a\u0631\u0628\u062d 2 \u0646\u0642\u0637\u0629\n\u062f\u0639\u0648\u062a {len(invited[uid])} \u0634\u062e\u0635\n\u0631\u0635\u064a\u062f\u0643: {get_pts(uid)}", reply_markup=main_menu())
            return
        if d == "ads":
            bot.edit_message_text(f"\u0642\u0633\u0645 \u0627\u0644\u0627\u0639\u0644\u0627\u0646\u0627\u062a\n\u0634\u0627\u0647\u062f \u0627\u0639\u0644\u0627\u0646 \u0648\u0627\u0631\u0628\u062d \u0646\u0642\u0637\u0629\n\u0634\u0627\u0647\u062f\u062a {ads_watched[uid]} \u0627\u0639\u0644\u0627\u0646\n\u0631\u0635\u064a\u062f\u0643: {get_pts(uid)}", c.message.chat.id, c.message.message_id, reply_markup=ads_menu())
            return
        if d == "watch_ad":
            if not is_admin(uid):
                pts[uid] += 1
            ads_watched[uid] += 1
            bot.send_message(c.message.chat.id, f"\u062a\u0645 \u0645\u0634\u0627\u0647\u062f\u0629 \u0627\u0644\u0627\u0639\u0644\u0627\u0646\n\u0631\u0628\u062d\u062a 1 \u0646\u0642\u0637\u0629\n\u0631\u0635\u064a\u062f\u0643: {get_pts(uid)}", reply_markup=ads_menu())
            return
        if d == "my_pts":
            bot.send_message(c.message.chat.id, f"\u0631\u0635\u064a\u062f\u0643: {get_pts(uid)}\n\u062f\u0639\u0648\u062a {len(invited[uid])} \u0634\u062e\u0635\n\u0634\u0627\u0647\u062f\u062a {ads_watched[uid]} \u0627\u0639\u0644\u0627\u0646")
            return

        cost = 15 if d.startswith("un_") else 10
        if is_admin(uid): cost = 0
        if not is_admin(uid) and pts.get(uid,0) < cost:
            mk = types.InlineKeyboardMarkup()
            mk.add(types.InlineKeyboardButton("\u0627\u062f\u0639 \u0627\u0635\u062d\u0627\u0628\u0643 +2", callback_data="invite"))
            mk.add(types.InlineKeyboardButton("\u0634\u0627\u0647\u062f \u0627\u0639\u0644\u0627\u0646 +1", callback_data="ads"))
            bot.send_message(c.message.chat.id, f"\u0644\u064a\u0633 \u0644\u062f\u064a\u0643 \u0646\u0642\u0627\u0637\n\u062a\u062d\u062a\u0627\u062c {cost} - \u0631\u0635\u064a\u062f\u0643 {get_pts(uid)}", reply_markup=mk)
            return
        if not is_admin(uid): pts[uid] -= cost

        if d.startswith("un_"):
            state[uid] = d
            bot.send_message(c.message.chat.id, f"\u0627\u0631\u0633\u0644 \u0627\u0644\u0631\u0642\u0645 \u0627\u0644\u0645\u062d\u0638\u0648\u0631 \u0627\u0644\u0627\u0646 - \u0627\u0644\u0628\u0648\u062a \u0628\u064a\u0646\u0641\u0630\n\u0631\u0635\u064a\u062f\u0643: {get_pts(uid)}")
        else:
            bot.send_message(c.message.chat.id, f"\u0627\u0644\u0628\u0648\u062a \u0646\u0641\u0630 {d}\n\u0631\u0635\u064a\u062f\u0643: {get_pts(uid)}\n{STORE_NAME}")

    except Exception as e:
        try: bot.send_message(c.message.chat.id, f"Error {e}")
        except: pass

@bot.message_handler(content_types=['document','photo','video'])
def file_h(m):
    if state.get(m.from_user.id) != "file": return
    try:
        if not is_admin(m.from_user.id) and pts.get(m.from_user.id,0) < 20:
            bot.reply_to(m, "\u0644\u064a\u0633 \u0644\u062f\u064a\u0643 \u0646\u0642\u0627\u0637")
            return
        fid = m.photo[-1].file_id if m.content_type == 'photo' else getattr(m, m.content_type).file_id
        finfo = bot.get_file(fid)
        url = f"https://api.telegram.org/file/bot{TOKEN}/{finfo.file_path}"
        if not is_admin(m.from_user.id): pts[m.from_user.id] -= 20
        state.pop(m.from_user.id, None)
        bot.reply_to(m, f"\u062a\u0645 \u0631\u0641\u0639 \u0645\u0644\u0641\u0643:\n{url}\n\u0631\u0635\u064a\u062f\u0643: {get_pts(m.from_user.id)}")
    except Exception as e:
        bot.reply_to(m, f"Error {e}")

@bot.message_handler(func=lambda m: True)
def txt(m):
    if state.get(m.from_user.id, '').startswith("un_"):
        bot.reply_to(m, f"\u062a\u0645 \u0627\u0633\u062a\u0644\u0627\u0645 {m.text} - \u0633\u064a\u0641\u0643 \u0627\u0644\u062d\u0638\u0631\n{STORE_NAME}")
        state.pop(m.from_user.id, None)

@bot.message_handler(commands=['add'])
def add(m):
    if not is_admin(m.from_user.id): return
    try:
        _, uid, amt = m.text.split()
        pts[int(uid)] += int(amt)
        bot.reply_to(m, f"Added {amt}")
    except: bot.reply_to(m, "Use /add id 100")

print("Iblis Store Invite+Ads+Files Running")
bot.infinity_polling(none_stop=True, timeout=60)