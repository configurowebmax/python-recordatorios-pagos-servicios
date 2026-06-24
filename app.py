"""
=====================================================================
 Recordatorios de Pagos de Servicios
 ConfiguroWeb · 2026 · Python real en el navegador (PyScript)
=====================================================================
"""
from pyscript import document, window
from js import localStorage
import json
import math

APP_CLAVE = "python_recordatorios_pagos_servicios_datos"
VERSION = "1.0.0"


# =====================================================================
#  Lógica de negocio
# =====================================================================
class Calculadora:
    """Modelo de cálculo de Recordatorios de Pagos de Servicios."""

    def __init__(self, cliente, monto, fecha):
        self.cliente = float(cliente)
        self.monto = float(monto)
        self.fecha = float(fecha)

    def calcular(self):
        """Ejecuta el cálculo principal y devuelve un dict de resultados."""

        msg = (f"Estimado/a {self.cliente}, le recordamos que tiene un pago pendiente "
               f"de {fmt_moneda(self.monto)} con vencimiento el {self.fecha}. "
               f"Evite recargos. Gracias.")
        return {"mensaje": msg, "caracteres": len(msg)}


    def diagnostico(self, resultados):
        """Texto explicativo del resultado."""
        return "✅ Recordatorio listo para enviar."


# =====================================================================
#  Formateadores
# =====================================================================
def fmt_moneda(v):
    if v is None:
        return "—"
    if math.isinf(v):
        return "∞"
    return f"${v:,.0f}"

def fmt_num(v):
    if v is None:
        return "—"
    if isinstance(v, float) and v.is_integer():
        v = int(v)
    return f"{v:,}"

def fmt_pct(v):
    if v is None:
        return "—"
    return f"{v:.1f}%"


# =====================================================================
#  Persistencia localStorage
# =====================================================================
def cargar_guardado():
    try:
        raw = localStorage.getItem(APP_CLAVE)
        if raw:
            return json.loads(raw)
    except Exception:
        pass
    return None

def guardar_ls(datos):
    try:
        localStorage.setItem(APP_CLAVE, json.dumps(datos))
        return True
    except Exception:
        return False


# =====================================================================
#  UI helpers
# =====================================================================
def input_float(eid):
    el = document.querySelector(f"#{eid}")
    if not el or not el.value:
        return 0.0
    try:
        return float(el.value)
    except (ValueError, TypeError):
        return 0.0

def mostrar(html, clase=""):
    caja = document.querySelector("#resultado")
    caja.innerHTML = html
    caja.classList.remove("hidden", "is-error", "is-success")
    if clase:
        caja.classList.add(clase)


# =====================================================================
#  Handlers
# =====================================================================
def calcular_handler(event=None):
    """Lee inputs, instancia, calcula y muestra."""

    c = Calculadora(
        document.querySelector("#cliente").value or "",
        input_float("monto"),
        document.querySelector("#fecha").value or "",
    )
    r = c.calcular()
    html = f"""
      <div class="result-value">💳 Recordatorio generado</div>
      <p style="white-space:pre-wrap;background:#fff;padding:1rem;border-radius:8px;border:1px solid var(--cweb-border);">{r["mensaje"]}</p>
    """
    mostrar(html, clase="is-success")



def guardar_datos(event=None):
    datos = {
            "cliente": input_float("cliente"),
            "monto": input_float("monto"),
            "fecha": input_float("fecha"),
        "version": VERSION,
    }
    ok = guardar_ls(datos)
    if ok:
        mostrar("💾 Datos guardados en este navegador.", clase="is-success")
    else:
        mostrar("❌ No se pudieron guardar los datos.", clase="is-error")


def cargar_al_inicio():
    datos = cargar_guardado()
    if not datos:
        return
    try:
        if "cliente" in datos:
            document.querySelector("#cliente").value = datos["cliente"]
        if "monto" in datos:
            document.querySelector("#monto").value = datos["monto"]
        if "fecha" in datos:
            document.querySelector("#fecha").value = datos["fecha"]
        aviso = document.querySelector("#resultado")
        aviso.innerHTML = "📂 Datos cargados. Pulsa <em>Calcular</em>."
        aviso.classList.remove("hidden")
    except Exception:
        pass


def inicializar():
    cargar_al_inicio()
    window.dispatchEvent(window.Event.new("py:ready"))

inicializar()
