from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="customers_home"),
    path('sendemail/', views.email, name="sendemail"),
    path('user/', views.userPage, name="user-page"),
    path('products/', views.ProductsIndex.as_view(), name="products"),
    path('products/getproduct/', views.getproduct, name="getproduct"),
    
    path('cust/<str:pk>/', views.customer, name="cust"),

    path('create_order/<str:pk>/', views.createOrder, name="create_order"),
    path('delete_order/<str:pk>/', views.deleteOrder, name="delete_order"),
    path('delete_order_ajax/<str:pk>/', views.deleteOrder_ajax, name="delete_order_ajax"),
    
    path('delete_customer/<str:pk>/', views.deleteCustomer, name="delete_customer"),

    path('cust_list/', views.customers, name="customers_list"),

    
    path('order/<int:order_id>/', views.order, name='order'),
    path('order2/<int:order_id>/', views.order_registered, name='order_registered'),
    
    path('order/new/', views.new_order, name='new_order'),
    path('order/new/check/', views.check_item, name='check_order_item'),
    path('order/<int:customer_pk>/new/', views.new_order_customer, name='new_order_customer'),
    
    path('order/<int:order_id>/item/<int:orderitem_id>/delete/', views.delete_item, name='delete_order_item'),
    path('order/<int:order_id>/item/add/', views.add_item, name='add_order_item'),
    

    path('order_list2/', views.orders, name="orders_list2"),
    path('order_list/complete/', views.OrdersIndex.as_view(),{'complete_status': 'True'}, name="orders_list_complete", ),#arg={}
    path('order_list_1/', views.OrdersIndex.as_view(),{'complete_status': 'False'}, name="orders_list_1", ),
    path('order_list/', views.orders, name="orders_list", ),
    #path('myclientlist/', views.myclientlist, name="myclientlist", ),

    
    path('entry/create/product/',
         views.ProductCreate.as_view(),  name='product_new'),
    path('entry/create/customer/',
         views.CustomerCreate.as_view(),  name='customer_new'),

 
    path('order/<int:order_id>/print/', views.print_order, name='print_order'),
    
    path('order/<int:order_id>/update/', views.update_order, name='update_order'),
   
    # Attachments
    path('order/<int:order_id>/attachments/add/', views.upload_order_attachment, name='upload_order_attachment'),
    path('order/<int:order_id>/attachments/<int:orderattachment_id>/delete/', views.delete_order_attachment, name='delete_order_attachment'),
  
   # # # REPORTS

    path('accounting/', views.accounting, name='orders_accounting'),
    path('orders_export/', views.export_orders, name='export_orders'),
    path('orders_export_monthly/', views.export_monthly_orders, name='export_monthly_orders'),
    path('financial_statement/', views.ExportView.as_view(), name='export_financial_statement'),

     #print html2pdf
    path('order/<int:order_id>/print/view/', views.ViewPDF.as_view(), name="order_pdf_view"),
    path('order/<int:order_id>/print/download/', views.DownloadPDF.as_view(), name="order_pdf_download"),

    #edit product
    
    
   
    path('product_update/<str:pk>/', views.product_update, name="update_product"),

    path('delete_product_old/<str:pk>/', views.deleteProduct, name="delete_product_okd"),

    path('delete_product/<str:id>/<int:page_no>/', views.delete_product_ajax, name="delete_product"),

    path('unlock_product/<str:pk>/', views.unlockProduct, name="unlock_product"),
    path('lock_product/<str:pk>/', views.lockProduct, name="lock_product"), 
    
    path('order/<str:pk>/to_invoice/', views.make_invoice_from_order, name="make_invoice_from_order"),
    

     path('u/p/load_status_ajax/', views.get_user_products_load_status_ajax, name="userproducts_load_status_ajax"),
     path('display_userproduct_ajax/', views.display_userproduct_ajax, name="display_userproduct_ajax"),
     path('user_product_search/<str:slug>/search/tags/', views.product_search_and_tags_ajax,{'search_type': 1}, name='user_product_search_and_tags_ajax'), 
     path('user_product_search/<str:slug>/tags/', views.product_search_and_tags_ajax,{'search_type': 0}, name='user_product_tags_ajax'), 
 
     path('u/p/0/', views.get_user_products,{'type': 'all'}, name="user_products"),
     # path('u/p/1/', views.get_user_products,{'type': 'open'}, name="user_businesses_open"),
     # path('u/p/2/', views.get_user_products,{'type': 'closed'}, name="user_businesses_closed"),
     # path('u/p/', views.get_user_products,{'type': 'unread'}, name="user_businesses_unread"),

     path('u_product_ajax/', views.create_userproduct_ajax, name="create_userproduct_ajax"),
     path('u/c/load_status_ajax/<str:status>', views.get_user_clients_load_status_ajax, name="user_clients_load_status_ajax"),
     path('u/c/0/', views.get_user_clients,{'type': 'all'}, name="user_clients"),



     path('u/o/load_status_ajax/', views.get_user_orders_load_status_ajax, name="userorders_load_status_ajax"),
     path('display_useroders_ajax/', views.display_userorders_ajax, name="display_userorders_ajax"),
     path('display_user_clients_ajax/', views.display_user_clients_ajax, name="display_user_clients_ajax"),


     path('client_search/<str:status>/<str:slug>/search/tags/', views.client_search_and_tags_ajax,{'search_type': 1}, name='client_search_and_tags_ajax'), 
     path('client_search/<str:status>/tags/', views.client_search_and_tags_ajax,{'search_type': 0}, name='client_tags_ajax'), 

    
     path('full_fill_order/<str:id>/', views.display_toggle_order_ajax, name="order-fullfill"),
]
