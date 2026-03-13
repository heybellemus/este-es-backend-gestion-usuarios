# mi_app/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'clientes', views.ClientesViewSet)
router.register(r'departamentos', views.DepartamentosViewSet)
router.register(r'roles', views.RolesViewSet)
router.register(r'usuarios', views.UsuariosViewSet)
router.register(r'permisos', views.PermisosViewSet)
router.register(r'rolpermisos', views.RolPermisosViewSet)
router.register(r'pantallas', views.PantallasViewSet)
router.register(r'rolpantallas', views.RolPantallasViewSet)
router.register(r'menu-categorias', views.MenuCategoriasViewSet)
router.register(r'menu-unidades-medida', views.MenuUnidadesMedidaViewSet)
router.register(r'menu-lotes', views.MenuLotesViewSet)
router.register(r'menu-historial-precios', views.MenuHistorialPreciosViewSet)
router.register(r'menu-proveedores', views.MenuProveedoresViewSet)
router.register(r'cat-tipos-movimiento', views.CatTiposMovimientoViewSet)
router.register(r'menu-movimientos', views.MenuMovimientosViewSet)
router.register(r'menu-productos', views.MenuProductosViewSet)

urlpatterns = [
    # Rutas API Menu Inventario
    path('api/menu/inventario-completo/', views.menu_inventario_completo_list, name='menu_inventario_completo_list'),
    path('api/menu/stock-bajo/', views.menu_stock_bajo_list, name='menu_stock_bajo_list'),
    path('api/menu/proximos-vencer/', views.menu_proximos_vencer_list, name='menu_proximos_vencer_list'),
    path('api/menu/inventario-detallado/', views.menu_inventario_detallado_list, name='menu_inventario_detallado_list'),
    path('api/menu/buscar-productos/', views.menu_buscar_productos, name='menu_buscar_productos'),
    path('api/menu/reporte-inventario/', views.menu_reporte_inventario, name='menu_reporte_inventario'),
    path('api/menu/registrar-venta/', views.menu_registrar_venta, name='menu_registrar_venta'),
    path('', views.home, name='home'),
    path('login/', views.login_usuario, name='login_usuario'),
    path('api/', include(router.urls)),
    # Rutas alternativas basadas en funciones
    path('clientes-list/', views.clientes_list, name='clientes_list'),
    path('clientes/<int:pk>/', views.cliente_detail, name='cliente_detail'),
    path('clientes-activos/', views.clientes_activos, name='clientes_activos'),

    # Rutas para departamentos
    path('departamentos-list/', views.departamentos_list, name='departamentos_list'),
    path('departamentos/<int:pk>/', views.departamento_detail, name='departamento_detail'),
    path('departamentos-activos/', views.departamentos_activos, name='departamentos_activos'),

    # Rutas para roles
    path('roles-list/', views.roles_list, name='roles_list'),
    path('roles/<int:pk>/', views.rol_detail, name='rol_detail'),
    path('roles-activos/', views.roles_activos, name='roles_activos'),

    # Rutas para usuarios
    path('usuarios-list/', views.usuarios_list, name='usuarios_list'),
    path('usuarios/<int:pk>/', views.usuario_detail, name='usuario_detail'),
    path('usuarios-activos/', views.usuarios_activos, name='usuarios_activos'),

    # Rutas para permisos
    path('permisos-list/', views.permisos_list, name='permisos_list'),
    path('permisos/<int:pk>/', views.permiso_detail, name='permiso_detail'),
    path('permisos/modulo/<str:modulo>/', views.permisos_por_modulo, name='permisos_por_modulo'),

    # Rutas para rol-permisos
    path('rolpermisos-list/', views.rolpermisos_list, name='rolpermisos_list'),
    path('rolpermisos/<int:pk>/', views.rolpermiso_detail, name='rolpermiso_detail'),

    #rutas qr 
    path('qr-generar/', views.generar_qr_login, name='generar_qr_login'),
    path('qr-status/<str:codigo_sesion>/', views.verificar_estado_qr, name='verificar_estado_qr'),
    path('qr-escanear/', views.escanear_qr_movil, name='escanear_qr_movil'),
    path('qr-aprobar-movil/', views.aprobar_qr_desde_movil, name='aprobar_qr_desde_movil'),
    path('qr-login/', views.login_con_qr, name='login_con_qr'),

    # Rutas para gestión de pantallas y permisos
    path('pantallas-usuario/', views.pantallas_usuario, name='pantallas_usuario'),
    path('verificar-acceso-pantalla/', views.verificar_acceso_pantalla, name='verificar_acceso_pantalla'),
    path('pantallas-list/', views.pantallas_list, name='pantallas_list'),
    path('rol-pantallas/<int:rol_id>/', views.rol_pantallas_list, name='rol_pantallas_list'),
    path('asignar-pantalla-rol/', views.asignar_pantalla_rol, name='asignar_pantalla_rol'),
    path('asignar-multiples-pantallas-rol/', views.asignar_multiples_pantallas_rol, name='asignar_multiples_pantallas_rol'),
    path('todos-roles-pantallas/', views.todos_roles_pantallas, name='todos_roles_pantallas'),
    path('pantallas-eliminadas/', views.PantallasViewSet.as_view({'get': 'eliminadas'}), name='pantallas_eliminadas'),

    # Rutas para recuperación de contraseña
    path('solicitar-recuperacion/', views.solicitar_recuperacion_password, name='solicitar_recuperacion'),
    path('confirmar-recuperacion/', views.confirmar_recuperacion_password, name='confirmar_recuperacion'),
    path('verificar-token/<str:token>/', views.verificar_token_recuperacion, name='verificar_token'),
    path('tokens-recuperacion/', views.listar_tokens_recuperacion, name='listar_tokens_recuperacion'),
]


