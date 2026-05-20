import sqlite3
import random


class DatabaseManager:
    """
    Gestiona la base de datos local SQLite del catálogo de productos Veltri Tecnologic.
    Catálogo ampliado: 100+ productos incluyendo laptops, periféricos, monitores y componentes.
    """

    def __init__(self, db_path: str = "veltri_shop.db"):
        self.db_path = db_path
        self._init_db()

    def _get_conn(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        """Crea las tablas e inserta datos semilla si la BD está vacía."""
        with self._get_conn() as conn:
            c = conn.cursor()

            # Migración automática si existe esquema antiguo
            c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='productos'")
            if c.fetchone():
                c.execute("PRAGMA table_info(productos)")
                cols = [row[1] for row in c.fetchall()]
                if "precio_base" not in cols or "descripcion" not in cols:
                    c.execute("DROP TABLE productos")
                    conn.commit()

            c.execute("""
                CREATE TABLE IF NOT EXISTS productos (
                    id              INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre          TEXT    NOT NULL UNIQUE,
                    categoria       TEXT    NOT NULL,
                    marca           TEXT    NOT NULL,
                    precio_base     REAL    NOT NULL,
                    stock_base      INTEGER NOT NULL,
                    garantia_meses  INTEGER NOT NULL,
                    descripcion     TEXT    DEFAULT ''
                )
            """)

            c.execute("SELECT COUNT(*) FROM productos")
            if c.fetchone()[0] == 0:
                semilla = [
                    # ── LAPTOPS (20 unidades) ─────────────────────────────────────────────
                    ("Laptop ASUS VivoBook 15 i5-1235U",   "Laptops", "ASUS",    2890.0, 8,  12, "15.6\" FHD, 8GB RAM, 512GB SSD, ideal ofimática y estudio"),
                    ("Laptop ASUS TUF Gaming A15 RTX 4060","Laptops", "ASUS",    5490.0, 5,  12, "15.6\" 144Hz, Ryzen 7 7745HX, 16GB DDR5, 512GB NVMe, gaming"),
                    ("Laptop Lenovo IdeaPad 3 Ryzen 5",    "Laptops", "Lenovo",  2490.0, 10, 12, "15.6\" FHD, 8GB RAM, 256GB SSD, buena relación calidad/precio"),
                    ("Laptop Lenovo Legion 5 RTX 4070",    "Laptops", "Lenovo",  6890.0, 3,  12, "16\" QHD 165Hz, Ryzen 7 7745HX, 16GB DDR5, 1TB NVMe, gaming pro"),
                    ("Laptop HP Pavilion 15 i5-1335U",     "Laptops", "HP",      2790.0, 7,  12, "15.6\" FHD, 12GB RAM, 512GB SSD, diseño delgado"),
                    ("Laptop HP OMEN 16 RTX 4060",         "Laptops", "HP",      5990.0, 4,  12, "16.1\" 165Hz, i7-13700HX, 16GB DDR5, 512GB NVMe, gaming"),
                    ("Laptop Acer Aspire 5 i5-1235U",      "Laptops", "Acer",    2590.0, 9,  12, "15.6\" FHD IPS, 8GB RAM, 512GB SSD, batería de larga duración"),
                    ("Laptop Acer Nitro 5 RTX 4050",       "Laptops", "Acer",    4490.0, 6,  12, "15.6\" 144Hz, i5-13500H, 16GB DDR5, 512GB NVMe, gaming entry"),
                    ("Laptop MSI Katana 15 RTX 4060",      "Laptops", "MSI",     5290.0, 4,  12, "15.6\" 144Hz, i7-13620H, 16GB DDR5, 512GB NVMe, gaming"),
                    ("Laptop MSI Modern 14 i5-1335U",      "Laptops", "MSI",     2850.0, 6,  12, "14\" FHD IPS, 8GB DDR4, 512GB NVMe, ultradelgada para trabajo"),
                    ("Laptop Dell Inspiron 15 3000 i5",    "Laptops", "Dell",    2690.0, 8,  12, "15.6\" FHD, 8GB RAM, 512GB SSD, confiable para uso diario"),
                    ("Laptop Dell G15 RTX 4060",           "Laptops", "Dell",    5590.0, 4,  12, "15.6\" 165Hz, i7-13650HX, 16GB DDR5, 512GB NVMe, gaming"),
                    ("Laptop Lenovo ThinkPad E14 i5",      "Laptops", "Lenovo",  3290.0, 5,  24, "14\" FHD IPS, 16GB RAM, 512GB SSD, empresarial premium"),
                    ("Laptop ASUS ExpertBook B1 i3",       "Laptops", "ASUS",    1990.0, 12, 12, "15.6\" FHD, 8GB RAM, 256GB SSD, ofimática económica"),
                    ("Laptop HP 250 G9 i3-1215U",          "Laptops", "HP",      1790.0, 15, 12, "15.6\" FHD, 8GB RAM, 256GB SSD, la más económica"),
                    ("Laptop ASUS ROG Strix G16 RTX 4070", "Laptops", "ASUS",    8490.0, 2,  12, "16\" QHD 240Hz, i9-13980HX, 32GB DDR5, 1TB NVMe, tope de gama"),
                    ("Laptop Acer Swift 3 i7-1260P",       "Laptops", "Acer",    3490.0, 5,  12, "14\" 2K IPS, 16GB LPDDR5, 512GB NVMe, ultrabook premium"),
                    ("Laptop Lenovo IdeaPad Gaming 3 RTX 3050","Laptops","Lenovo",3890.0, 6, 12, "15.6\" 120Hz, Ryzen 5 6600H, 8GB DDR5, 512GB NVMe, gaming básico"),
                    ("Laptop Dell XPS 15 i7-13700H",       "Laptops", "Dell",    9490.0, 2,  12, "15.6\" OLED Touch, 16GB DDR5, 512GB NVMe, premium creativo"),
                    ("Laptop HP Victus 15 RTX 4050",       "Laptops", "HP",      4190.0, 7,  12, "15.6\" 144Hz, Ryzen 5 7535H, 8GB DDR5, 512GB NVMe, gaming accesible"),

                    # ── TARJETAS DE VIDEO ─────────────────────────────────────────────────
                    ("RTX 4060 8GB ASUS Dual",             "Tarjetas de Video", "ASUS",     1490.0, 12, 24, "Ideal 1080p gaming, bajo consumo 115W, ray tracing"),
                    ("RTX 4060 8GB Gigabyte Windforce",    "Tarjetas de Video", "Gigabyte", 1420.0, 10, 12, "Excelente refrigeración, triple ventilador"),
                    ("RTX 4060 Ti 16GB MSI Ventus",        "Tarjetas de Video", "MSI",      2050.0,  7, 24, "16GB VRAM, ideal 1080p-1440p, creación de contenido"),
                    ("RTX 4070 12GB ASUS TUF",             "Tarjetas de Video", "ASUS",     2850.0,  5, 36, "1440p nativo, DLSS 3, excelente relación rendimiento/precio"),
                    ("RTX 4070 Super 12GB MSI Gaming X",   "Tarjetas de Video", "MSI",      3190.0,  4, 24, "Rinde casi como la 4080, top ventas Veltri"),
                    ("RTX 4070 Ti Super 16GB Gigabyte",    "Tarjetas de Video", "Gigabyte", 4290.0,  3, 24, "4K gaming fluido, ideal streamers y creadores"),
                    ("RTX 4080 Super 16GB ASUS ROG",       "Tarjetas de Video", "ASUS",     6490.0,  2, 36, "4K a máxima calidad, lo mejor de NVIDIA actualmente"),
                    ("RTX 4090 24GB MSI Suprim X",         "Tarjetas de Video", "MSI",     11990.0,  1, 36, "La GPU más potente del mercado, para entusiastas"),
                    ("RX 7600 8GB Sapphire Pulse",         "Tarjetas de Video", "Sapphire", 1290.0, 10, 12, "Alternativa AMD 1080p, buena eficiencia"),
                    ("RX 7700 XT 12GB PowerColor",         "Tarjetas de Video", "PowerColor",1890.0, 6, 12, "1440p AMD, excelente en rasterización"),
                    ("RX 7900 GRE 16GB Sapphire",          "Tarjetas de Video", "Sapphire", 3490.0,  3, 24, "High-end AMD, sin ray tracing DLSS pero gran rasterización"),
                    ("RTX 3060 12GB Zotac Twin Edge",      "Tarjetas de Video", "Zotac",    1090.0, 15, 12, "Generación anterior, más económica, sigue siendo sólida 1080p"),

                    # ── PROCESADORES ─────────────────────────────────────────────────────
                    ("Intel Core i3-12100F",               "Procesadores", "Intel",  420.0, 25, 12, "4 núcleos, sin gráficos integrados, el más económico con buen rendimiento"),
                    ("Intel Core i5-12400F",               "Procesadores", "Intel",  680.0, 20, 12, "6 núcleos/12 hilos, excelente relación calidad/precio gaming"),
                    ("Intel Core i5-13600K",               "Procesadores", "Intel",  990.0, 12, 12, "14 núcleos híbridos, overclockeble, ideal gaming y trabajo"),
                    ("Intel Core i7-12700F",               "Procesadores", "Intel",  980.0, 10, 12, "12 núcleos híbridos, gaming y productividad"),
                    ("Intel Core i7-13700K",               "Procesadores", "Intel", 1290.0,  8, 12, "16 núcleos, tope gaming Intel gen 13"),
                    ("Intel Core i9-13900K",               "Procesadores", "Intel", 2490.0,  4, 12, "24 núcleos, overclock extremo, workstation/gaming"),
                    ("AMD Ryzen 5 5600X",                  "Procesadores", "AMD",    720.0, 15, 12, "6 núcleos AM4, excelente para gaming 1080p"),
                    ("AMD Ryzen 5 7600X",                  "Procesadores", "AMD",    890.0, 12, 12, "6 núcleos AM5 DDR5, eficiente y rápido"),
                    ("AMD Ryzen 7 5700X",                  "Procesadores", "AMD",    850.0, 10, 12, "8 núcleos AM4, trabajo y gaming equilibrado"),
                    ("AMD Ryzen 7 7700X",                  "Procesadores", "AMD",    990.0,  8, 12, "8 núcleos AM5, alto IPC, top ventas AMD"),
                    ("AMD Ryzen 9 7900X",                  "Procesadores", "AMD",   1890.0,  4, 12, "12 núcleos AM5, workstation y gaming extremo"),
                    ("AMD Ryzen 9 7950X",                  "Procesadores", "AMD",   3490.0,  2, 12, "16 núcleos AM5, el procesador más potente de escritorio AMD"),

                    # ── MEMORIAS RAM ─────────────────────────────────────────────────────
                    ("DDR4 8GB 3200MHz Kingston ValueRAM", "Memorias RAM", "Kingston",   95.0, 30, 36, "Básica y confiable, ideal complementar o reemplazar"),
                    ("DDR4 16GB 3200MHz Corsair Vengeance","Memorias RAM", "Corsair",   180.0, 22, 36, "Kit 2x8GB, la más vendida en Veltri"),
                    ("DDR4 32GB 3600MHz G.Skill Ripjaws",  "Memorias RAM", "G.Skill",   320.0, 12, 36, "Kit 2x16GB, para multitarea y edición de video"),
                    ("DDR5 16GB 5200MHz Crucial",          "Memorias RAM", "Crucial",   270.0, 15, 36, "Kit 2x8GB, plataforma AM5/Intel Gen13"),
                    ("DDR5 32GB 5600MHz Kingston Fury",    "Memorias RAM", "Kingston",  410.0, 10, 36, "Kit 2x16GB, DDR5 de gama media-alta"),
                    ("DDR5 64GB 6000MHz G.Skill Trident Z","Memorias RAM", "G.Skill",   890.0,  5, 36, "Kit 2x32GB, workstation y edición profesional"),
                    ("DDR4 16GB 3600MHz Team T-Force",     "Memorias RAM", "Team",      195.0, 18, 36, "Con RGB, buen precio"),
                    ("DDR5 32GB 6400MHz Corsair Dominator", "Memorias RAM","Corsair",   580.0,  7, 36, "Kit 2x16GB, overclock DDR5, RGB premium"),

                    # ── ALMACENAMIENTO ───────────────────────────────────────────────────
                    ("SSD NVMe 500GB Samsung 980",         "Almacenamiento", "Samsung",  220.0, 20, 60, "Gen 3, 3500MB/s lectura, SO y programas"),
                    ("SSD NVMe 1TB Samsung 980 Pro",       "Almacenamiento", "Samsung",  420.0, 14, 60, "Gen 4, 7000MB/s lectura, máximo rendimiento"),
                    ("SSD NVMe 2TB Samsung 990 Pro",       "Almacenamiento", "Samsung",  780.0,  8, 60, "Gen 4, 7450MB/s, para creadores de contenido"),
                    ("SSD NVMe 1TB WD Black SN850X",       "Almacenamiento", "WD",       450.0, 10, 60, "Gen 4, PS5 compatible, 7300MB/s"),
                    ("SSD NVMe 1TB Kingston NV2",          "Almacenamiento", "Kingston", 290.0, 18, 36, "Gen 4, económico y rápido, buena compra"),
                    ("SSD NVMe 2TB Crucial P3 Plus",       "Almacenamiento", "Crucial",  490.0, 10, 36, "Gen 4, costo/GB excelente para gran capacidad"),
                    ("SSD SATA 1TB Kingston A400",         "Almacenamiento", "Kingston", 180.0, 25, 36, "SATA III, económico, ideal upgrade de HDD"),
                    ("SSD SATA 480GB Kingston A400",       "Almacenamiento", "Kingston",  95.0, 30, 36, "SATA III, el más vendido por precio"),
                    ("HDD 1TB Seagate Barracuda",          "Almacenamiento", "Seagate",  130.0, 20, 12, "7200RPM, para almacenamiento masivo"),
                    ("HDD 2TB WD Blue",                    "Almacenamiento", "WD",       190.0, 15, 12, "5400RPM, silencioso, backup y almacenamiento"),
                    ("HDD 4TB Seagate BarraCuda",          "Almacenamiento", "Seagate",  310.0,  8, 12, "Máxima capacidad económica, NAS/backup"),

                    # ── FUENTES DE PODER ─────────────────────────────────────────────────
                    ("Fuente EVGA 500W 80+ White",         "Fuentes de Poder", "EVGA",     230.0, 25, 12, "Básica confiable, builds económicas"),
                    ("Fuente Corsair CV550 80+ Bronze",    "Fuentes de Poder", "Corsair",  260.0, 20, 36, "Semi-modular, ideal builds mid-range"),
                    ("Fuente Corsair RM750e 80+ Gold",     "Fuentes de Poder", "Corsair",  520.0, 10, 84, "Completamente modular, 7 años garantía"),
                    ("Fuente Seasonic Focus GX-750 Gold",  "Fuentes de Poder", "Seasonic", 620.0,  7, 60, "Premium silenciosa, 80+ Gold"),
                    ("Fuente EVGA SuperNOVA 850W Gold",    "Fuentes de Poder", "EVGA",     680.0,  6, 60, "Para builds con RTX 4080/4090"),
                    ("Fuente Corsair HX1000 Platinum",     "Fuentes de Poder", "Corsair",  980.0,  4, 84, "1000W modular, para setups extremos"),
                    ("Fuente Cooler Master MWE 650W Gold", "Fuentes de Poder", "Cooler Master",410.0, 12, 60, "Eficiente y económica, buena compra"),
                    ("Fuente Thermaltake Toughpower 750W", "Fuentes de Poder", "Thermaltake",530.0, 8, 60, "Modular, 80+ Gold, silenciosa"),

                    # ── PLACAS MADRE ─────────────────────────────────────────────────────
                    ("Placa ASUS PRIME B660M-A DDR4",      "Placas Madre", "ASUS",    490.0, 10, 12, "mATX, LGA1700, Intel Gen 12/13, DDR4"),
                    ("Placa Gigabyte B760M DS3H DDR4",     "Placas Madre", "Gigabyte", 450.0, 12, 12, "mATX, LGA1700, económica y confiable"),
                    ("Placa MSI MAG B650M Mortar DDR5",    "Placas Madre", "MSI",      690.0,  8, 12, "mATX, AM5, Ryzen 7000, DDR5"),
                    ("Placa ASUS ROG Strix B650-A DDR5",   "Placas Madre", "ASUS",     890.0,  5, 12, "ATX, AM5, alta calidad VRM para OC"),
                    ("Placa Gigabyte X670E AORUS Elite",   "Placas Madre", "Gigabyte",1290.0,  3, 12, "ATX, AM5, top para Ryzen 9, PCIe 5.0"),
                    ("Placa MSI PRO B550M-VC WiFi",        "Placas Madre", "MSI",      380.0, 15, 12, "mATX, AM4, Ryzen 5000 compatible"),
                    ("Placa ASUS TUF Gaming B550-PLUS",    "Placas Madre", "ASUS",     550.0, 10, 12, "ATX, AM4, robusta para Ryzen 5000"),

                    # ── GABINETES ─────────────────────────────────────────────────────────
                    ("Gabinete NZXT H510 Flow",            "Gabinetes", "NZXT",    490.0,  8, 12, "ATX mid-tower, panel frontal malla, excelente airflow"),
                    ("Gabinete Lian Li Lancool 216",       "Gabinetes", "Lian Li", 590.0,  6, 12, "ATX, dual 160mm fans incluidos, top airflow"),
                    ("Gabinete Fractal Design Meshify C",  "Gabinetes", "Fractal",  480.0,  7, 12, "ATX compacto, malla frontal, silencioso"),
                    ("Gabinete Cooler Master Q300L",       "Gabinetes", "Cooler Master",210.0, 15, 12, "mATX económico, buen airflow"),
                    ("Gabinete Phanteks P400A Digital",    "Gabinetes", "Phanteks", 450.0,  8, 12, "ATX, panel vidrio, RGB incluido"),

                    # ── COOLING / REFRIGERACIÓN ───────────────────────────────────────────
                    ("Cooler CPU Cooler Master Hyper 212", "Cooling", "Cooler Master",130.0, 20, 12, "Torre doble, compatible LGA1700/AM5, clásico confiable"),
                    ("Cooler CPU Noctua NH-D15",           "Cooling", "Noctua",    490.0,  5, 72, "El mejor cooler air, silencioso y potente"),
                    ("AIO 240mm NZXT Kraken X53",          "Cooling", "NZXT",      590.0,  7, 36, "Refrigeración líquida 240mm, excelente para i7/Ryzen 7"),
                    ("AIO 360mm Corsair iCUE H150i",       "Cooling", "Corsair",   890.0,  4, 36, "Refrigeración líquida 360mm, para i9/Ryzen 9"),
                    ("Pasta Térmica Thermal Grizzly",      "Cooling", "Thermal Grizzly",35.0, 30, 0,  "La mejor pasta térmica del mercado"),
                    ("Cooler CPU Arctic Freezer 36",       "Cooling", "Arctic",    120.0, 18, 72, "Compacto, silencioso, excelente precio"),

                    # ── MONITORES ────────────────────────────────────────────────────────
                    ("Monitor 24\" LG 24GN600 IPS 144Hz",  "Monitores", "LG",       590.0, 10, 12, "1080p, 1ms, FreeSync, ideal gaming entrada"),
                    ("Monitor 27\" ASUS VG27AQ IPS 165Hz", "Monitores", "ASUS",     890.0,  6, 24, "1440p QHD, G-Sync compatible, gaming premium"),
                    ("Monitor 27\" Samsung Odyssey G5",    "Monitores", "Samsung",  790.0,  8, 12, "1440p curvo, 144Hz, VA, buen contraste"),
                    ("Monitor 32\" LG 32GN650 VA 165Hz",   "Monitores", "LG",      1090.0,  5, 12, "QHD curvo, 1ms, FreSync, inmersivo"),
                    ("Monitor 24\" Dell S2421HGF",         "Monitores", "Dell",     490.0, 12, 24, "1080p 144Hz IPS, sin marcos, versátil"),

                    # ── PERIFÉRICOS ──────────────────────────────────────────────────────
                    ("Teclado Mecánico Redragon K552 TKL", "Periféricos", "Redragon",  150.0, 20, 12, "TKL, switches rojo, RGB, para gaming"),
                    ("Mouse Gaming Logitech G305",         "Periféricos", "Logitech",  190.0, 15, 24, "Inalámbrico, sensor HERO, 25K DPI"),
                    ("Mouse Gaming Razer DeathAdder V3",   "Periféricos", "Razer",     320.0, 10, 12, "Ergonómico, 30K DPI, ultraligero"),
                    ("Audífonos HyperX Cloud II",          "Periféricos", "HyperX",    290.0, 12, 24, "7.1 virtual surround, cómodos, micrófono desmontable"),
                    ("Mousepad XL SteelSeries QcK Heavy",  "Periféricos", "SteelSeries",90.0, 25, 12, "XXL 900x300mm, superficie de control"),
                    ("Webcam Logitech C920 1080p",         "Periféricos", "Logitech",  290.0, 10, 24, "1080p 30fps, ideal streaming y videollamadas"),
                ]
                c.executemany("""
                    INSERT INTO productos (nombre, categoria, marca, precio_base, stock_base, garantia_meses, descripcion)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, semilla)
                conn.commit()

    # ------------------------------------------------------------------
    # Búsqueda con variabilidad dinámica
    # ------------------------------------------------------------------

    def buscar_producto(self, query: str, verbose: bool = False) -> list[dict]:
        """
        Busca productos por nombre, categoría o descripción.
        Introduce variabilidad realista: fluctuación de stock, descuentos flash.
        """
        with self._get_conn() as conn:
            c = conn.cursor()
            q = f"%{query.lower()}%"
            c.execute(
                """SELECT nombre, categoria, marca, precio_base, stock_base, garantia_meses, descripcion
                   FROM productos
                   WHERE LOWER(nombre) LIKE ? OR LOWER(categoria) LIKE ? OR LOWER(descripcion) LIKE ?""",
                (q, q, q)
            )
            filas = c.fetchall()

        resultado = []
        for nombre, categoria, marca, precio_base, stock_base, garantia, desc in filas:
            stock_actual = max(0, stock_base + random.randint(-3, 3))
            descuento    = random.choice([0.0, 0.05, 0.10])
            precio_hoy   = round(precio_base * (1 - descuento), 2)

            if verbose:
                print(f"  [SQL] '{nombre}': stock={stock_actual} | precio=S/.{precio_hoy} ({int(descuento*100)}%dto)")

            resultado.append({
                "nombre":         nombre,
                "categoria":      categoria,
                "marca":          marca,
                "precio":         precio_hoy,
                "precio_base":    precio_base,
                "stock":          stock_actual,
                "garantia_meses": garantia,
                "descripcion":    desc,
                "en_stock":       stock_actual > 0,
                "tiene_descuento": descuento > 0,
            })

        return resultado

    def obtener_catalogo_texto(self, query: str, verbose: bool = False) -> str:
        """Devuelve el catálogo formateado como texto para inyectarlo en el prompt."""
        productos = self.buscar_producto(query, verbose=verbose)
        if not productos:
            return f"No se encontraron productos relacionados con '{query}' en el inventario actual."

        lineas = ["CATÁLOGO EN TIEMPO REAL — VELTRI TECNOLOGIC:"]
        for p in productos:
            estado = "✅ En stock" if p["en_stock"] else "❌ Sin stock"
            oferta = f" 🔥 ¡Oferta hoy! (precio normal S/.{p['precio_base']})" if p["tiene_descuento"] else ""
            lineas.append(
                f"  • {p['nombre']} | {p['marca']} | S/.{p['precio']}{oferta} | "
                f"{p['stock']} uds | Garantía: {p['garantia_meses']} meses | {estado}"
            )
            if p["descripcion"]:
                lineas.append(f"    └ {p['descripcion']}")
        return "\n".join(lineas)

    def listar_categorias(self) -> list[str]:
        """Retorna las categorías disponibles."""
        with self._get_conn() as conn:
            c = conn.cursor()
            c.execute("SELECT DISTINCT categoria FROM productos ORDER BY categoria")
            return [row[0] for row in c.fetchall()]
