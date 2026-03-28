from __future__ import annotations

from contextlib import contextmanager
from typing import Iterator, Optional

from django.db import connection


def get_usuario_id_from_user(user) -> Optional[int]:
    usuario_id = getattr(user, "usuarioid", None) or getattr(user, "id", None)
    try:
        return int(usuario_id) if usuario_id is not None else None
    except (TypeError, ValueError):
        return None


@contextmanager
def sqlserver_usuario_context(usuario_id: Optional[int]) -> Iterator[None]:
    """
    Setea SESSION_CONTEXT('usuario_id') para que triggers en SQL Server lo puedan leer.
    Siempre lo resetea al salir para evitar "leaks" si la conexión se reusa.
    """
    with connection.cursor() as cursor:
        cursor.execute(
            "EXEC sp_set_session_context @key=N'usuario_id', @value=%s",
            [usuario_id],
        )
    try:
        yield
    finally:
        with connection.cursor() as cursor:
            cursor.execute(
                "EXEC sp_set_session_context @key=N'usuario_id', @value=%s",
                [None],
            )

