# mi_app/views.py
from __future__ import annotations

import hashlib
import secrets
import string
import uuid
from datetime import timedelta
from xml.sax.saxutils import escape

from django.conf import settings
from django.core.mail import send_mail
from django.db import connection, transaction
from django.http import HttpResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import (
    CatTiposMovimiento,
    Clientes,
    Departamentos,
    MenuCategorias,
    MenuHistorialPrecios,
    MenuLotes,
    MenuMovimientos,
    MenuProductos,
    MenuProveedores,
    MenuUnidadesMedida,
    Pantallas,
    PasswordResetToken,
    Permisos,
    Roles,
    RolPantallas,
    RolPermisos,
    SesionesQR,
    Usuarios,
)
from .permissions import obtener_pantallas_usuario, usuario_tiene_acceso_pantalla
from .serializers import (
    CatTiposMovimientoSerializer,
    ClientesSerializer,
    DepartamentosSerializer,
    MenuCategoriasSerializer,
    MenuHistorialPreciosSerializer,
    MenuLotesSerializer,
    MenuMovimientosSerializer,
    MenuProductosSerializer,
    MenuProveedoresSerializer,
    MenuUnidadesMedidaSerializer,
    PantallasSerializer,
    PasswordResetConfirmSerializer,
    PasswordResetRequestSerializer,
    PasswordResetTokenSerializer,
    PermisosSerializer,
    RolesSerializer,
    RolPantallasSerializer,
    RolPermisosSerializer,
    UsuariosSerializer,
)


def home(request):
    return HttpResponse("Backend Django OK")


def _is_sha256_hex(value: str) -> bool:
    if not isinstance(value, str):
        return False
    txt = value.strip()
    if len(txt) != 64:
        return False
    try:
        int(txt, 16)
        return True
    except ValueError:
        return False


def _normalize_password_input(value: str) -> str:
    if value is None:
        return ""
    raw = str(value).strip()
    if _is_sha256_hex(raw):
        return raw.upper()
    return hashlib.sha256(raw.encode("utf-8")).hexdigest().upper()


@csrf_exempt
@api_view(["POST"])
@permission_classes([AllowAny])
def login_usuario(request):
    data = request.data or {}
    email = (data.get("email") or "").strip()
    password = data.get("password")

    if not email or not password:
        return Response({"error": "Email y password requeridos."}, status=400)

    try:
        usuario = Usuarios.objects.get(email=email)
    except Usuarios.DoesNotExist:
        return Response({"error": "Credenciales inválidas."}, status=401)

    incoming_hash = _normalize_password_input(password)
    stored_hash = (usuario.passwordhash or "").strip().upper()
    if not stored_hash or incoming_hash != stored_hash:
        return Response({"error": "Credenciales inválidas."}, status=401)

    refresh = RefreshToken.for_user(usuario)
    return Response(
        {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "usuario": {
                "usuarioid": usuario.usuarioid,
                "nombre": usuario.nombre,
                "apellido": usuario.apellido,
                "email": usuario.email,
                "nombreusuario": usuario.nombreusuario,
                "rolid": usuario.rolid_id,
                "departamentoid": usuario.departamentoid_id,
            },
        }
    )


# ============================================
# Helpers CRUD por funciones (compatibilidad)
# ============================================


def _get_or_404(model, pk):
    try:
        return model.objects.get(pk=pk)
    except model.DoesNotExist:
        return None


def _crud_list(request, model, serializer_cls, order_by: str):
    if request.method == "GET":
        qs = model.objects.all().order_by(order_by)
        return Response(serializer_cls(qs, many=True).data)
    serializer = serializer_cls(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=201)


def _crud_detail(request, model, serializer_cls, pk: int):
    obj = _get_or_404(model, pk)
    if obj is None:
        return Response({"error": "No encontrado."}, status=404)
    if request.method == "GET":
        return Response(serializer_cls(obj).data)
    if request.method in {"PUT", "PATCH"}:
        serializer = serializer_cls(obj, data=request.data, partial=(request.method == "PATCH"))
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    obj.delete()
    return Response(status=204)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def clientes_list(request):
    return _crud_list(request, Clientes, ClientesSerializer, "clienteid")


@api_view(["GET", "PUT", "PATCH", "DELETE"])
@permission_classes([IsAuthenticated])
def cliente_detail(request, pk: int):
    return _crud_detail(request, Clientes, ClientesSerializer, pk)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def clientes_activos(request):
    qs = Clientes.objects.filter(activo=True).order_by("clienteid")
    return Response(ClientesSerializer(qs, many=True).data)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def departamentos_list(request):
    return _crud_list(request, Departamentos, DepartamentosSerializer, "departamentoid")


@api_view(["GET", "PUT", "PATCH", "DELETE"])
@permission_classes([IsAuthenticated])
def departamento_detail(request, pk: int):
    return _crud_detail(request, Departamentos, DepartamentosSerializer, pk)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def departamentos_activos(request):
    qs = Departamentos.objects.filter(activo=True).order_by("departamentoid")
    return Response(DepartamentosSerializer(qs, many=True).data)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def roles_list(request):
    return _crud_list(request, Roles, RolesSerializer, "rolid")


@api_view(["GET", "PUT", "PATCH", "DELETE"])
@permission_classes([IsAuthenticated])
def rol_detail(request, pk: int):
    return _crud_detail(request, Roles, RolesSerializer, pk)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def roles_activos(request):
    qs = Roles.objects.filter(activo=True).order_by("rolid")
    return Response(RolesSerializer(qs, many=True).data)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def usuarios_list(request):
    return _crud_list(request, Usuarios, UsuariosSerializer, "usuarioid")


@api_view(["GET", "PUT", "PATCH", "DELETE"])
@permission_classes([IsAuthenticated])
def usuario_detail(request, pk: int):
    return _crud_detail(request, Usuarios, UsuariosSerializer, pk)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def usuarios_activos(request):
    qs = Usuarios.objects.filter(activo=True).order_by("usuarioid")
    return Response(UsuariosSerializer(qs, many=True).data)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def permisos_list(request):
    return _crud_list(request, Permisos, PermisosSerializer, "permisoid")


@api_view(["GET", "PUT", "PATCH", "DELETE"])
@permission_classes([IsAuthenticated])
def permiso_detail(request, pk: int):
    return _crud_detail(request, Permisos, PermisosSerializer, pk)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def permisos_por_modulo(request, modulo: str):
    qs = Permisos.objects.filter(modulo=modulo).order_by("permisoid")
    return Response(PermisosSerializer(qs, many=True).data)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def rolpermisos_list(request):
    return _crud_list(request, RolPermisos, RolPermisosSerializer, "rolpermisoid")


@api_view(["GET", "PUT", "PATCH", "DELETE"])
@permission_classes([IsAuthenticated])
def rolpermiso_detail(request, pk: int):
    return _crud_detail(request, RolPermisos, RolPermisosSerializer, pk)


# ============================================
# ViewSets (DRF Router)
# ============================================


class ClientesViewSet(viewsets.ModelViewSet):
    queryset = Clientes.objects.all().order_by("clienteid")
    serializer_class = ClientesSerializer


class DepartamentosViewSet(viewsets.ModelViewSet):
    queryset = Departamentos.objects.all().order_by("departamentoid")
    serializer_class = DepartamentosSerializer


class RolesViewSet(viewsets.ModelViewSet):
    queryset = Roles.objects.all().order_by("rolid")
    serializer_class = RolesSerializer


class UsuariosViewSet(viewsets.ModelViewSet):
    queryset = Usuarios.objects.all().order_by("usuarioid")
    serializer_class = UsuariosSerializer


class PermisosViewSet(viewsets.ModelViewSet):
    queryset = Permisos.objects.all().order_by("permisoid")
    serializer_class = PermisosSerializer


class RolPermisosViewSet(viewsets.ModelViewSet):
    queryset = RolPermisos.objects.all().order_by("rolpermisoid")
    serializer_class = RolPermisosSerializer


class PantallasViewSet(viewsets.ModelViewSet):
    queryset = Pantallas.objects.all().order_by("pantallaid")
    serializer_class = PantallasSerializer

    @action(detail=False, methods=["get"])
    def eliminadas(self, request):
        qs = Pantallas.objects.filter(activo=False).order_by("-pantallaid")
        return Response(PantallasSerializer(qs, many=True).data)


class RolPantallasViewSet(viewsets.ModelViewSet):
    queryset = RolPantallas.objects.all().order_by("rolpantallaid")
    serializer_class = RolPantallasSerializer


class MenuCategoriasViewSet(viewsets.ModelViewSet):
    queryset = MenuCategorias.objects.all().order_by("id_categoria")
    serializer_class = MenuCategoriasSerializer


class MenuUnidadesMedidaViewSet(viewsets.ModelViewSet):
    queryset = MenuUnidadesMedida.objects.all().order_by("id_unidad_medida")
    serializer_class = MenuUnidadesMedidaSerializer


class MenuProductosViewSet(viewsets.ModelViewSet):
    queryset = MenuProductos.objects.all().order_by("id_producto")
    serializer_class = MenuProductosSerializer


class MenuLotesViewSet(viewsets.ModelViewSet):
    queryset = MenuLotes.objects.all().order_by("id_lote")
    serializer_class = MenuLotesSerializer


class MenuHistorialPreciosViewSet(viewsets.ModelViewSet):
    queryset = MenuHistorialPrecios.objects.all().order_by("-fecha_cambio_precio", "-id_historial_precio")
    serializer_class = MenuHistorialPreciosSerializer


class MenuProveedoresViewSet(viewsets.ModelViewSet):
    queryset = MenuProveedores.objects.all().order_by("id_proveedor")
    serializer_class = MenuProveedoresSerializer


class CatTiposMovimientoViewSet(viewsets.ModelViewSet):
    queryset = CatTiposMovimiento.objects.all().order_by("orden", "id_tipo_movimiento")
    serializer_class = CatTiposMovimientoSerializer


class MenuMovimientosViewSet(viewsets.ModelViewSet):
    queryset = MenuMovimientos.objects.all().order_by("-id_movimiento")
    serializer_class = MenuMovimientosSerializer

    def perform_create(self, serializer):
        serializer.save(usuario_id=self.request.user)


# ============================================
# MENU INVENTARIO (SQL)
# ============================================


def _dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def _dictfetchall_sets(cursor):
    sets = []
    while True:
        if cursor.description:
            sets.append(_dictfetchall(cursor))
        if not cursor.nextset():
            break
    return sets


def _to_bool(value, default=True):
    if value is None:
        return default
    return str(value).strip().lower() in {"1", "true", "t", "yes", "y"}


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def menu_inventario_completo_list(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM vw_menu_inventario_completo")
        data = _dictfetchall(cursor)
    return Response(data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def menu_stock_bajo_list(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM vw_menu_stock_bajo")
        data = _dictfetchall(cursor)
    return Response(data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def menu_proximos_vencer_list(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM vw_menu_proximos_vencer")
        data = _dictfetchall(cursor)
    return Response(data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def menu_inventario_detallado_list(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM vw_menu_inventario_detallado")
        data = _dictfetchall(cursor)
    return Response(data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def menu_buscar_productos(request):
    termino = request.query_params.get("termino", "").strip()
    id_categoria = request.query_params.get("id_categoria")
    if not termino:
        return Response({"error": "El parametro 'termino' es requerido."}, status=400)

    categoria = None
    if id_categoria not in (None, ""):
        try:
            categoria = int(id_categoria)
        except ValueError:
            return Response({"error": "El parametro 'id_categoria' debe ser numerico."}, status=400)

    with connection.cursor() as cursor:
        cursor.execute(
            "EXEC sp_menu_buscar_productos @termino_busqueda=%s, @id_categoria=%s",
            [termino, categoria],
        )
        data = _dictfetchall(cursor)
    return Response(data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def menu_reporte_inventario(request):
    incluir_stock_bajo = 1 if _to_bool(request.query_params.get("incluir_stock_bajo"), True) else 0
    incluir_proximos_vencer = 1 if _to_bool(request.query_params.get("incluir_proximos_vencer"), True) else 0

    with connection.cursor() as cursor:
        cursor.execute(
            "EXEC sp_menu_reporte_inventario @incluir_stock_bajo=%s, @incluir_proximos_vencer=%s",
            [incluir_stock_bajo, incluir_proximos_vencer],
        )
        sets = _dictfetchall_sets(cursor)

    return Response(
        {
            "resumen": sets[0] if len(sets) > 0 else [],
            "stock_bajo": sets[1] if len(sets) > 1 else [],
            "proximos_vencer": sets[2] if len(sets) > 2 else [],
        }
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def menu_registrar_venta(request):
    usuario = (request.data.get("usuario") or "SISTEMA").strip()
    productos = request.data.get("productos", [])

    if not isinstance(productos, list) or len(productos) == 0:
        return Response({"error": "Debes enviar una lista 'productos' con al menos un item."}, status=400)

    partes = ["<ventas>"]
    for idx, item in enumerate(productos):
        try:
            id_producto = int(item.get("id_producto"))
            id_lote = int(item.get("id_lote"))
            cantidad = int(item.get("cantidad"))
            precio = float(item.get("precio"))
        except (TypeError, ValueError):
            return Response({"error": f"Producto en posicion {idx} tiene datos invalidos."}, status=400)

        if cantidad <= 0 or precio < 0:
            return Response({"error": f"Producto en posicion {idx} tiene cantidad/precio invalido."}, status=400)

        precio_txt = escape(f"{precio:.2f}")
        partes.append(
            f'<producto id_producto="{id_producto}" id_lote="{id_lote}" cantidad="{cantidad}" precio="{precio_txt}" />'
        )
    partes.append("</ventas>")
    productos_xml = "".join(partes)

    with connection.cursor() as cursor:
        cursor.execute(
            "EXEC sp_menu_registrar_venta @productos_xml=%s, @usuario=%s",
            [productos_xml, usuario],
        )
        data = _dictfetchall(cursor) if cursor.description else [{"mensaje": "Venta registrada"}]
    return Response(data)


# ============================================
# Pantallas / Accesos (endpoints)
# ============================================


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def pantallas_usuario(request):
    return Response(obtener_pantallas_usuario(request.user))


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def verificar_acceso_pantalla(request):
    if request.method == "GET":
        codigo = (request.query_params.get("codigo_pantalla") or "").strip()
        if not codigo:
            return Response({"error": "codigo_pantalla es requerido"}, status=400)
        return Response({"codigo_pantalla": codigo, "tiene_acceso": usuario_tiene_acceso_pantalla(request.user, codigo)})

    codigos = request.data.get("codigos_pantalla", [])
    if not isinstance(codigos, list) or not codigos:
        return Response({"error": "codigos_pantalla debe ser una lista no vacía"}, status=400)
    return Response({str(c): usuario_tiene_acceso_pantalla(request.user, str(c)) for c in codigos})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def pantallas_list(request):
    qs = Pantallas.objects.all().order_by("pantallaid")
    return Response(PantallasSerializer(qs, many=True).data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def rol_pantallas_list(request, rol_id: int):
    qs = RolPantallas.objects.filter(rolid_id=rol_id).order_by("rolpantallaid")
    return Response(RolPantallasSerializer(qs, many=True).data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def asignar_pantalla_rol(request):
    rolid = request.data.get("rolid")
    pantallaid = request.data.get("pantallaid")
    acceso = bool(request.data.get("acceso", True))
    try:
        rolid = int(rolid)
        pantallaid = int(pantallaid)
    except (TypeError, ValueError):
        return Response({"error": "rolid y pantallaid deben ser numéricos"}, status=400)

    obj, _created = RolPantallas.objects.update_or_create(
        rolid_id=rolid,
        pantallaid_id=pantallaid,
        defaults={"acceso": acceso, "fechaasignacion": timezone.now()},
    )
    return Response(RolPantallasSerializer(obj).data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def asignar_multiples_pantallas_rol(request):
    rolid = request.data.get("rolid")
    pantallas = request.data.get("pantallas", [])
    try:
        rolid = int(rolid)
    except (TypeError, ValueError):
        return Response({"error": "rolid debe ser numérico"}, status=400)
    if not isinstance(pantallas, list) or not pantallas:
        return Response({"error": "pantallas debe ser una lista no vacía"}, status=400)

    results = []
    with transaction.atomic():
        for item in pantallas:
            try:
                pantallaid = int(item.get("pantallaid"))
                acceso = bool(item.get("acceso", True))
            except (TypeError, ValueError):
                continue
            obj, _created = RolPantallas.objects.update_or_create(
                rolid_id=rolid,
                pantallaid_id=pantallaid,
                defaults={"acceso": acceso, "fechaasignacion": timezone.now()},
            )
            results.append(RolPantallasSerializer(obj).data)
    return Response({"rolid": rolid, "asignaciones": results})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def todos_roles_pantallas(request):
    roles = Roles.objects.all().order_by("rolid")
    data = []
    for rol in roles:
        asignaciones = RolPantallas.objects.filter(rolid=rol).order_by("rolpantallaid")
        data.append({"rol": RolesSerializer(rol).data, "pantallas": RolPantallasSerializer(asignaciones, many=True).data})
    return Response(data)


# ============================================
# Password Reset
# ============================================


@csrf_exempt
@api_view(["POST"])
@permission_classes([AllowAny])
def solicitar_recuperacion_password(request):
    serializer = PasswordResetRequestSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data["email"]

    try:
        usuario = Usuarios.objects.get(email=email)
    except Usuarios.DoesNotExist:
        return Response({"mensaje": "Si el correo existe, se enviaron instrucciones."})

    token_value = uuid.uuid4().hex + secrets.token_urlsafe(16)
    expiracion = timezone.now() + timedelta(hours=1)
    token_obj = PasswordResetToken(
        usuarioid=usuario,
        token=token_value,
        email=email,
        fecha_expiracion=expiracion,
        utilizado=False,
        ip_address=request.META.get("REMOTE_ADDR"),
        user_agent=request.META.get("HTTP_USER_AGENT", ""),
    )
    token_obj.save()

    reset_url_template = getattr(settings, "PASSWORD_RESET_URL_TEMPLATE", "http://localhost:5173/reset-password/{token}")
    reset_url = reset_url_template.format(token=token_value)

    send_mail(
        subject="Recuperación de contraseña",
        message=f"Usa este enlace para restablecer tu contraseña: {reset_url}",
        from_email=getattr(settings, "DEFAULT_FROM_EMAIL", "no-reply@backend.local"),
        recipient_list=[email],
        fail_silently=True,
    )
    return Response({"mensaje": "Si el correo existe, se enviaron instrucciones."})


@csrf_exempt
@api_view(["POST"])
@permission_classes([AllowAny])
def confirmar_recuperacion_password(request):
    serializer = PasswordResetConfirmSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    token_value = serializer.validated_data["token"]
    new_password = serializer.validated_data["new_password"]

    try:
        token_obj = PasswordResetToken.objects.get(token=token_value)
    except PasswordResetToken.DoesNotExist:
        return Response({"error": "Token inválido."}, status=400)
    if not token_obj.is_valid:
        return Response({"error": "Token inválido o expirado."}, status=400)

    new_hash = _normalize_password_input(new_password)
    with transaction.atomic():
        usuario = token_obj.usuarioid
        usuario.passwordhash = new_hash
        usuario.save()
        token_obj.utilizado = True
        token_obj.fecha_utilizacion = timezone.now()
        token_obj.save()
    return Response({"mensaje": "Contraseña actualizada correctamente."})


@api_view(["GET"])
@permission_classes([AllowAny])
def verificar_token_recuperacion(request, token: str):
    try:
        token_obj = PasswordResetToken.objects.get(token=token)
    except PasswordResetToken.DoesNotExist:
        return Response({"token": token, "valido": False})
    return Response({"token": token, "valido": bool(token_obj.is_valid)})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def listar_tokens_recuperacion(request):
    qs = PasswordResetToken.objects.all().order_by("-fecha_creacion")[:200]
    return Response(PasswordResetTokenSerializer(qs, many=True).data)


# ============================================
# QR Login (JSON básico)
# ============================================


def generar_codigo_sesion() -> str:
    caracteres = string.ascii_letters + string.digits
    return "".join(secrets.choice(caracteres) for _ in range(32))


def limpiar_sesiones_expiradas() -> int:
    ahora = timezone.now()
    expiradas = SesionesQR.objects.filter(fechaexpiracion__lt=ahora, estado="pendiente")
    count = expiradas.count()
    expiradas.update(estado="expirada")
    return count


@csrf_exempt
@api_view(["GET", "POST"])
@permission_classes([AllowAny])
def generar_qr_login(request):
    limpiar_sesiones_expiradas()
    codigo_sesion = generar_codigo_sesion()
    ahora = timezone.now()
    expiracion = ahora + timedelta(minutes=5)
    sesion = SesionesQR(
        codigosesion=codigo_sesion,
        dispositivosinfo=request.META.get("HTTP_USER_AGENT", ""),
        iporigen=request.META.get("REMOTE_ADDR", "0.0.0.0"),
        estado="pendiente",
        fechacreacion=ahora,
        fechaexpiracion=expiracion,
    )
    sesion.save()
    return Response({"codigo_sesion": codigo_sesion, "expiracion": expiracion})


@api_view(["GET"])
@permission_classes([AllowAny])
def verificar_estado_qr(request, codigo_sesion: str):
    try:
        sesion = SesionesQR.objects.get(codigosesion=codigo_sesion)
    except SesionesQR.DoesNotExist:
        return Response({"error": "Código no encontrado"}, status=404)

    payload = {"codigo_sesion": codigo_sesion, "estado": sesion.estado, "expiracion": sesion.fechaexpiracion}
    if sesion.estado == "aprobada" and sesion.tokenacceso:
        payload["access"] = sesion.tokenacceso
        payload["refresh"] = sesion.tokenrefresh
    return Response(payload)


@csrf_exempt
@api_view(["GET", "POST"])
@permission_classes([AllowAny])
def escanear_qr_movil(request):
    data = request.data or {}
    codigo = (request.query_params.get("code") or data.get("code") or "").strip()
    email = (request.query_params.get("email") or data.get("email") or "").strip()
    password = request.query_params.get("password") or data.get("password")

    if request.method == "GET" and codigo and not email:
        return Response({"codigo_sesion": codigo, "mensaje": "Envía email/password para aprobar."})
    return aprobar_qr_desde_movil(request)


@csrf_exempt
@api_view(["POST"])
@permission_classes([AllowAny])
def aprobar_qr_desde_movil(request):
    data = request.data or {}
    codigo = (data.get("code") or "").strip()
    email = (data.get("email") or "").strip()
    password = data.get("password")

    if not codigo or not email or not password:
        return Response({"error": "code, email y password son requeridos"}, status=400)

    try:
        sesion = SesionesQR.objects.get(codigosesion=codigo)
    except SesionesQR.DoesNotExist:
        return Response({"error": "Código no encontrado"}, status=404)

    if sesion.estado != "pendiente" or sesion.fechaexpiracion <= timezone.now():
        return Response({"error": "Sesión expirada o inválida"}, status=400)

    try:
        usuario = Usuarios.objects.get(email=email)
    except Usuarios.DoesNotExist:
        return Response({"error": "Credenciales inválidas"}, status=401)

    incoming_hash = _normalize_password_input(password)
    stored_hash = (usuario.passwordhash or "").strip().upper()
    if incoming_hash != stored_hash:
        return Response({"error": "Credenciales inválidas"}, status=401)

    refresh = RefreshToken.for_user(usuario)
    sesion.usuarioid = usuario
    sesion.estado = "aprobada"
    sesion.fechaaprobacion = timezone.now()
    sesion.tokenacceso = str(refresh.access_token)
    sesion.tokenrefresh = str(refresh)
    sesion.save()
    return Response({"mensaje": "Aprobado", "access": sesion.tokenacceso, "refresh": sesion.tokenrefresh})


@api_view(["GET", "POST"])
@permission_classes([AllowAny])
def login_con_qr(request):
    data = request.data or {}
    codigo = (request.query_params.get("code") or data.get("code") or "").strip()
    if not codigo:
        return Response({"error": "code es requerido"}, status=400)
    return verificar_estado_qr(request, codigo)
