# 🛠️ Checklist de funcionalidades para el gestor de inventario de componentes electrónicos

## 🔍 Funcionalidades básicas de gestión
- [ ] Búsqueda por cualquier campo
- [ ] Filtros avanzados (por tipo, encapsulado, cantidad mínima, etc.)
- [ ] Ordenar columnas (clic en encabezado)
- [ ] Coloreado condicional (por ejemplo, rojo si la cantidad < 5)
- [ ] Botón de "Añadir componente rápido"
- [ ] Duplicar componente
- [ ] Tags o etiquetas por proyecto o categoría

## 📤 Entrada / salida de datos
- [ ] Importar desde CSV
- [ ] Importar desde Excel
- [x] Exportar a CSV
- [x] Exportar a Excel
- [ ] Exportar a JSON
- [ ] Exportar inventario a PDF
- [ ] Copia de seguridad automática del archivo SQLite

## 📸 Funcionalidades visuales y usabilidad
- [ ] Vista por tarjetas (modo visual alternativo con imágenes)
- [ ] Iconos por tipo de componente
- [ ] Tema oscuro / claro
- [ ] Guardar tamaño y orden de columnas entre sesiones
- [ ] Menú contextual con acciones rápidas (clic derecho)
- [ ] Personalización de fuente y tamaño

## 🧠 Funcionalidades inteligentes o técnicas
- [ ] Comparar inventario con CSV de proveedor
- [ ] Gestión de stock mínimo y alertas
- [ ] Soporte para múltiples ubicaciones físicas (cajón, armario…)
- [ ] Historial de cambios por componente
- [ ] OCR desde imágenes o etiquetas
- [ ] Integración con catálogos online (Digi-Key, LCSC, Mouser…)

## 🔗 Conectividad y automatización
- [ ] Sincronización con carpeta en la nube (Dropbox, Nextcloud…)
- [ ] API REST local para acceso desde otras apps
- [ ] Modo de lectura simplificado para móvil
- [ ] Escaneo de códigos QR o barras
- [ ] Soporte para escáneres USB

## 🧪 Funcionalidades para desarrolladores o makers
- [ ] Asociación de archivos de proyectos (KiCad, Eagle, datasheets…)
- [ ] Generador de lista BOM para proyectos
- [ ] Compatibilidad con exportaciones `.xml` de BOM desde KiCad
- [ ] Vista de resumen por tipo de componente y cantidad total
