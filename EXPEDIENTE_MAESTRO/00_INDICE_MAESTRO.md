# EXPEDIENTE MAESTRO DE CUMPLIMIENTO — CENTRO MIRË

**Establecimiento:** CENTRO MIRË DE BELLEZA INTEGRAL Y DISEÑO
**Giro autorizado:** SCIAN 812110 — Salones y clínicas de belleza y peluquerías
**Aviso de Funcionamiento COFEPRIS:** 2509135018X00286
**Domicilio:** Av. del Conscripto 13, Col. Manuel Ávila Camacho, C.P. 11610, Alcaldía Miguel Hidalgo, Ciudad de México
**Versión:** 2.0 — reestructurada por destinatario
**Documento de control interno. No se entrega a clientes ni a terceros.**

---

## 1. CÓMO ESTÁ ARMADO ESTE EXPEDIENTE

Seis tomos. Cada tomo es **un solo PDF continuo, en blanco y negro, listo para imprimir sin edición previa**. No hay documentos sueltos que haya que buscar ni combinar.

| Tomo | Contenido | Se imprime | Destinatario | ¿Aparece el nombre de la titular? |
|---|---|---|---|---|
| **1** | Ficha de cliente con ficha clínica, valoración y consentimiento; control de sesiones y dos anexos | **Una hoja** por cliente nuevo | Cliente | **No** |
| **2** | Dictamen de riesgo, matriz de procedimientos, plan de acción, protección patrimonial | Un ejemplar, uso reservado | Titular y sus asesores | **Sí** (es su documento) |
| **3** | Convenio de colaboración e indicación médica | Un juego por médico | Médico que refiere | **Sí** (es parte contratante) |
| **4** | Política de servicios, guiones, POE de higiene, urgencias, conducta ante autoridad, confidencialidad | Un juego por persona que trabaja en el centro | Personal | **No** (se firma como "la Titular") |
| **5** | Carpeta de verificación: ficha del establecimiento, checklist, inventarios y bitácoras | Un ejemplar en carpeta física + copia digital | Autoridad sanitaria en visita | **Sí** (obligatorio ante autoridad) |
| **6** | Avisos y rótulos para fijar a la vista, y aviso de privacidad integral de recepción | Un ejemplar de cada uno | Público | **No** |

**Regla operativa:** la hoja de ficha y consentimiento se llena y se firma **completa** antes del servicio, por los dos lados. Nunca se atiende sin ella.

### 1.1 Instrucciones de impresión (ahorro de papel)

Los formatos están compuestos para gastar el mínimo de hojas: sin páginas de portada en los tomos de tiraje repetido, sin espacios muertos y con los documentos corriendo uno tras otro, separados por una línea de corte visible. Cada documento conserva su título y su folio, de modo que sigue siendo un instrumento identificable aunque comparta hoja con otro.

| Tomo | Págs. | Cómo imprimirlo | Hojas |
|---|---|---|---|
| 1 · Cliente | 5 | **Doble cara.** Juego base: **páginas 1 y 2**, una sola hoja por cliente. Control de sesiones: página 3, solo si habrá varias sesiones. Anexo A: página 4, solo si viene de cirugía. Anexo B: página 5, solo si autoriza imagen | **1** base |
| 2 · Titular | 8 | Doble cara | 4 |
| 3 · Médico | 5 | Doble cara. Cada instrumento inicia hoja: convenio por duplicado, indicación médica por paciente, carta suelta | 3 |
| 4 · Personal | 11 | Doble cara. Solo el protocolo de urgencias inicia hoja, porque se fija a la vista en el área de servicio | 6 |
| 5 · Verificación | 10 | Doble cara. Inventario y bitácoras inician hoja, porque se reemplazan cada mes | 5 |
| 6 · Avisos al público | 7 | **Una cara**, un aviso por hoja. El aviso de privacidad integral se conserva en recepción para consulta | 7 |

**El costo recurrente es el Tomo 1:** una hoja por cliente. Imprimirlo en tiros de 30 o 50, foliado a mano, y tener copias sueltas del control de sesiones y de los dos anexos. Al editar cualquier documento, regenerar con `python3 _build_expediente.py`: avisa si una página quedó con más de 20% de espacio muerto al pie.

---

## 2. POLÍTICA DE IDENTIFICACIÓN DE LA TITULAR (criterio jurídico)

La instrucción es que **la titularidad del negocio no se difunda** salvo donde sea necesaria. Así se implementa en este expediente:

### 2.1 Documentos donde NO se imprime el nombre de la titular
Cliente, personal y público. En ellos el sujeto obligado se identifica como **"CENTRO MIRË DE BELLEZA INTEGRAL Y DISEÑO"** (nombre comercial del establecimiento), con domicilio, correo y número de Aviso de Funcionamiento. Quien firma lo hace como **"la Titular del Establecimiento"** o **"quien atiende"**, sin asentar el nombre en el cuerpo impreso.

Sustento: la LFPDPPP exige identificar al **responsable** y su domicilio, no exhibir su nombre de nacimiento; el nombre comercial del establecimiento, más domicilio y medio de contacto, es identificación suficiente y verificable. En el Aviso de Privacidad Integral se incluye la cláusula de **identificación a solicitud del titular de los datos**, que cierra cualquier objeción de transparencia.

### 2.2 Documentos donde el nombre SÍ va, porque la ley lo exige
No es negociable en:

1. **Aviso de Funcionamiento y trámites ante COFEPRIS/DIGIPRiS** — el obligado es la persona física.
2. **Acta de verificación sanitaria** y cualquier actuación ante autoridad.
3. **Contratos**: convenio con médicos, arrendamiento del local, contratos laborales, pólizas de seguro.
4. **Materia fiscal**: RFC, CFDI, constancia de situación fiscal.
5. **IMPI**: solicitud de registro de marca (aunque puede solicitarse a nombre de persona moral si se constituye).

### 2.3 Advertencia estratégica (leer)
La reserva de titularidad es **comercial y reputacional, no defensiva**. Frente a la autoridad la titularidad es pública y trazable: el Aviso de Funcionamiento, el RFC y el domicilio la identifican. Intentar ocultarla en una visita o en un trámite se lee como **ocultamiento de información al verificador**, agrava la posición y puede constituir por sí mismo una infracción. Por eso:

- Ante COFEPRIS, Alcaldía, Protección Civil, PROFECO o cualquier autoridad: **la titular se identifica plenamente y de inmediato.**
- Ante clientes, público, redes y proveedores no esenciales: se identifica **el establecimiento**, no la persona.
- El personal **no comenta quién es la dueña** ni la estructura del negocio con clientes o terceros (Tomo 4, carta de confidencialidad).

### 2.4 Medida que sí blinda la reserva de titularidad
Si el objetivo es que el negocio deje de estar atado al nombre personal, la vía real es **constituir persona moral** (S.A.S. o S. de R.L. de C.V.) y migrar a ella el aviso sanitario, los contratos y la facturación. A partir de ese momento el sujeto visible es la sociedad y la persona física aparece solo en el acta constitutiva y en registros societarios. Esto se analiza en el Tomo 2, apartado de protección patrimonial. Mientras opere como persona física, la reserva será siempre parcial.

---

## 3. REGLA DE ORO DEL EXPEDIENTE

Este expediente no sirve para aparentar cumplimiento: sirve para **sostener que la operación real coincide con el giro autorizado**. Un documento que contradice lo que ocurre en el establecimiento no protege, **acusa**: se convierte en prueba fechada y firmada en contra. Antes de usar el Tomo 1 con clientes, deben estar ejecutadas las acciones críticas del Tomo 2, apartado 4.

---

## 4. CONTROL DE VERSIONES Y RESGUARDO

| Tomo | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| Última revisión y quién | | | | | | |

**Resguardo:** las hojas firmadas del Tomo 1 y el Tomo 2 contienen datos sensibles y estrategia legal: bajo llave, con acceso exclusivo de la titular. Copias digitales en carpeta con contraseña; **no en galerías de teléfono ni en chats de WhatsApp.**
