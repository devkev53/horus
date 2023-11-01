from compra.models import Buy, BuyDetail
from venta.models import Sale, SaleDetail
from catalogo.models import Product



# *--*-*-*-*-*- UTIL METHOD FOR ADD BUY INCREMENT STOCK *--*-*-*-*-*-
def update_product_stock():
    for prod in Product.objects.all():
        stock_increment = 0
        stock_decrement = 0
        # print('------------- MANEGANDO EL AUMENTO DE STOCK -------------')

        # ------------- MANEGANDO EL AUMENTO DE STOCK -------------
        # Sumando la cantidad de productos en compras activas
        for buy in Buy.objects.filter(is_active=True).all():
            for detail in BuyDetail.objects.filter(buy_id=buy).all():
                if prod == detail.product_id:
                    stock_increment += detail.quantity
                    # print('Sumando compras activas')
        # Sumando la cantidad de productos en ventas inactivas
        for sale in Sale.objects.filter(is_active=False).all():
            for detail in SaleDetail.objects.filter(sale_id=sale).all():
                if prod == detail.product_id:
                    stock_increment += detail.quantity
                    # print('Sumando ventas inactivas')

        # ------------- MANEGANDO EL DECREMENTO DE STCOK -------------
        # Sumando la cantidad de productos en compras inactivas
        for buy in Buy.objects.filter(is_active=False).all():
            for detail in BuyDetail.objects.filter(buy_id=buy).all():
                if prod == detail.product_id:
                    stock_increment += detail.quantity
                    # print('Restando compras inactivas')
        # Sumando la cantidad de productos en ventas activas
        for sale in Sale.objects.filter(is_active=True).all():
            for detail in SaleDetail.objects.filter(sale_id=sale).all():
                if prod == detail.product_id:
                    stock_increment += detail.quantity
                    # print('Restando ventas activas')

        # print('------------- MOSTRANDO STOCKS STOCK -------------')
        # print(stock_increment)
        # print(stock_decrement)

        prod.stock = stock_increment - stock_decrement
        prod.save()
