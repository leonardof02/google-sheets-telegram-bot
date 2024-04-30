from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler, CallbackContext
from SheetsService import SheetsService
from MenuTemplate import MenuTemplate
from Routes import Routes

from telegram.constants import ParseMode  


TOKEN = "6817877108:AAHG5jH6Ot1MDg1TVog1IdeF4KwD1C8PNhE"
application = ApplicationBuilder().token(TOKEN).build()

sheetConfig = SheetsService("creds.json")
sheet = sheetConfig.get_sheet_by_id("1Ubkm1NgFNn_2fzUoSpYpeN-6qQPofU6TTf3_0xq64FA")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    (text, reply_markup) = MenuTemplate.get_principal_menu_view()
    await update.message.reply_text(text=text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)
    
async def show_menu( update: Update, context: CallbackContext ):
    (text, reply_markup) = MenuTemplate.get_principal_menu_view()
    await update.callback_query.answer()
    await update.callback_query.message.edit_text(text=text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)
    
async def show_products(update: Update, context: CallbackContext ):
    all_values = sheet.sheet1.get_all_values()
    message = update.callback_query.message
    text, reply_markup = MenuTemplate.get_products_view_from_table_values(all_values)
    await update.callback_query.answer()
    await message.edit_text(text, reply_markup=reply_markup)
    
async def make_order( update: Update, context: CallbackContext ):
    all_values = sheet.sheet1.get_all_values()
    message = update.callback_query.message
    text, reply_markup = MenuTemplate.get_create_order_view(all_values)
    await update.callback_query.answer()
    await message.edit_text(text, reply_markup=reply_markup)
    pass

async def register_order( update: Update, context: ContextTypes.DEFAULT_TYPE ):
    message = update.callback_query.message
    username = update.effective_user.username
    full_name = update.effective_user.full_name
    product_name = update.callback_query.data.split(":")[1]
    worksheet = sheet.get_worksheet(1)
    worksheet.append_row([username, full_name, product_name])
    await update.callback_query.answer()
    await message.reply_text(f"Pedido realizado: {product_name}")
    pass

async def get_my_orders(update: Update, context: ContextTypes.DEFAULT_TYPE ):
    worksheet = sheet.get_worksheet(1)
    all_values = worksheet.get_all_values()
    username = update.effective_user.username
    message = update.callback_query.message
    text, reply_markup = MenuTemplate.get_my_orders(all_values, username )
    await update.callback_query.answer()
    await message.edit_text(text, reply_markup=reply_markup)


application.add_handler( CommandHandler( "start", start ) )
application.add_handler( CallbackQueryHandler(show_products, pattern=Routes.PRODUCTS) )
application.add_handler( CallbackQueryHandler(show_menu, pattern=Routes.MENU) )
application.add_handler( CallbackQueryHandler(make_order, pattern=Routes.CREATE_ORDER) )
application.add_handler( CallbackQueryHandler(register_order, pattern=Routes.REGISTER_ORDER) )
application.add_handler( CallbackQueryHandler( get_my_orders, pattern=Routes.GET_MY_ORDERS ) )
application.run_polling(allowed_updates=Update.ALL_TYPES)