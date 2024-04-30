from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from Routes import Routes

from typing import Sequence, Tuple, List


class MenuTemplate:
    
    BACK_BUTTON = InlineKeyboardButton("🔙 Volver al menú", callback_data=Routes.MENU)
    
    @staticmethod
    def get_principal_menu_view() -> Tuple[str, InlineKeyboardMarkup]:
        menu_view_text = "```Menu principal```"
        keyboard = [
            [InlineKeyboardButton("👀 Ver Productos", callback_data=Routes.PRODUCTS)],
            [InlineKeyboardButton("🛒 Ver mis pedidos", callback_data=Routes.GET_MY_ORDERS)],
            [InlineKeyboardButton("🤚🏻 Hacer un pedido", callback_data=Routes.CREATE_ORDER)]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        return menu_view_text, reply_markup
    
    @staticmethod
    def get_products_view_from_table_values(table: List[List[str]]) -> Tuple[str, InlineKeyboardMarkup]:
        table.pop(0)
        keyboard = [[ MenuTemplate.BACK_BUTTON ]]
        products_str = "*📜 Productos del menú de hoy:*"
        products_str += '\n' + (len(products_str) * '-') + '\n'
        for row in table:
            row_str = ' | '.join(row)
            products_str += row_str + '\n'
        reply_markup = InlineKeyboardMarkup(keyboard)
        return products_str, reply_markup
    
    @staticmethod
    def get_create_order_view(table: List[List[str]]) -> Tuple[str, InlineKeyboardMarkup]:
        table.pop(0)
        order_view_text = "**🤔 ¿Que vas a pedir? ...**\n\n👇Selecciona uno de los productos de abajo para hacer el pedido"
        order_buttons: Sequence[InlineKeyboardButton] = []
        
        for row in table:
            product_name = row[1]
            row_str = ' | '.join(row)
            order_buttons.append([InlineKeyboardButton(text=row_str, callback_data=f"Order:{product_name}")])
        order_buttons.append([MenuTemplate.BACK_BUTTON])
        reply_markup = InlineKeyboardMarkup(order_buttons)
        return order_view_text, reply_markup
    
    @staticmethod
    def get_my_orders( table: List[List[str]], username: str  ) -> Tuple[str, InlineKeyboardMarkup]:
        my_orders = '\n'.join( [order_row[2] for order_row in table if order_row[0] == username] )
        reply_markup = InlineKeyboardMarkup([[ MenuTemplate.BACK_BUTTON ]])
        return my_orders, reply_markup