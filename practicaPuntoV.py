import tkinter as tk
from tkinter import ttk, messagebox

# Datos
USUARIOS = {
    "admin": {"password": "123", "rol": "Administrador"},
    "vendedor": {"password": "123", "rol": "Vendedor"}
}

PRODUCTOS = [
    {"id": "1", "nombre": "Tenis Adidas", "tipo": "Zapatillas", "cantidad": 15, "color": "Negro/Blanco", "talla": "28",
     "precio": 1200.0},
    {"id": "2", "nombre": "Mocasines 271", "tipo": "Mocasines", "cantidad": 10, "color": "Café", "talla": "26",
     "precio": 850.0},
    {"id": "3", "nombre": "Converse All Star", "tipo": "Tenis", "cantidad": 20, "color": "Rojo", "talla": "27",
     "precio": 950.0}
]

CLIENTES = [
    {"id": "C1", "nombre": "Carlos Verdi", "telefono": "7711234567", "correo": "carlos@gmail.com"},
    {"id": "C2", "nombre": "Camila Villeda", "telefono": "7719876543", "correo": "camila@gmail.com"}
]

VENTAS = []


# Ventana Principal del Sistema
class SistemaTiendaGUI:
    def __init__(self, root, usuario, rol):
        self.root = root
        self.usuario = usuario
        self.rol = rol
        self.carrito = []

        self.root.title(f"Sistema Tienda - Usuario: {self.usuario} ({self.rol})")
        self.root.geometry("900x650")
        self.root.config(bg="#f0f0f0")

        # Barra superior de estado
        top_frame = tk.Frame(self.root, bg="#2c3e50", height=40)
        top_frame.pack(side="top", fill="x")
        lbl_user = tk.Label(top_frame, text=f"Bienvenido: {self.usuario} | Rol: {self.rol}", fg="white", bg="#2c3e50",
                            font=("Arial", 11, "bold"))
        lbl_user.pack(side="left", padx=15, pady=8)

        # Contenedor de pestañas (Notebook)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)

        # Crear pestañas
        self.frame_pv = tk.Frame(self.notebook, bg="#ffffff")
        self.notebook.add(self.frame_pv, text="Punto de Venta")
        self.setup_punto_venta()

        self.frame_inv = tk.Frame(self.notebook, bg="#ffffff")
        self.notebook.add(self.frame_inv, text="Inventario de Productos")
        self.setup_inventario()

        self.frame_cli = tk.Frame(self.notebook, bg="#ffffff")
        self.notebook.add(self.frame_cli, text="Gestión de Clientes")
        self.setup_clientes()

        # Restricción de rol
        if self.rol != "Administrador":
            # Deshabilitar pestaña de inventario para vendedores simples si fuera necesario
            pass

    # MÓDULO 1: Punto de venta
    def setup_punto_venta(self):
        # Panel superior: Selección
        panel_top = tk.LabelFrame(self.frame_pv, text=" Datos de la Venta ", bg="white", font=("Arial", 10, "bold"))
        panel_top.pack(fill="x", padx=10, pady=5)

        tk.Label(panel_top, text="Cliente:", bg="white").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.cb_clientes = ttk.Combobox(panel_top, values=[f"{c['id']} - {c['nombre']}" for c in CLIENTES],
                                        state="readonly", width=30)
        self.cb_clientes.grid(row=0, column=1, padx=5, pady=5)
        if CLIENTES:
            self.cb_clientes.current(0)

        tk.Label(panel_top, text="Producto:", bg="white").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.cb_productos = ttk.Combobox(panel_top,
                                         values=[f"{p['id']} - {p['nombre']} (${p['precio']:.2f})" for p in PRODUCTOS],
                                         state="readonly", width=35)
        self.cb_productos.grid(row=0, column=3, padx=5, pady=5)
        if PRODUCTOS:
            self.cb_productos.current(0)

        tk.Label(panel_top, text="Cantidad:", bg="white").grid(row=1, column=2, padx=5, pady=5, sticky="e")
        self.entry_cant = tk.Entry(panel_top, width=10)
        self.entry_cant.insert(0, "1")
        self.entry_cant.grid(row=1, column=3, padx=5, pady=5, sticky="w")

        btn_agregar = tk.Button(panel_top, text="Agregar al Carrito", bg="#27ae60", fg="white",
                                font=("Arial", 9, "bold"), command=self.agregar_al_carrito)
        btn_agregar.grid(row=1, column=4, padx=15, pady=5)

        # Tabla del Carrito
        panel_tabla = tk.Frame(self.frame_pv, bg="white")
        panel_tabla.pack(fill="both", expand=True, padx=10, pady=5)

        cols = ("ID", "Producto", "Precio U.", "Cantidad", "Importe")
        self.tree_cart = ttk.Treeview(panel_tabla, columns=cols, show="headings", height=8)
        for col in cols:
            self.tree_cart.heading(col, text=col)
            self.tree_cart.column(col, anchor="center")
        self.tree_cart.pack(fill="both", expand=True, side="left")

        # Resumen de Venta
        panel_totales = tk.Frame(self.frame_pv, bg="#f8f9fa", bd=1, relief="solid")
        panel_totales.pack(fill="x", padx=10, pady=10)

        self.lbl_subtotal = tk.Label(panel_totales, text="Subtotal: $0.00", font=("Arial", 11), bg="#f8f9fa")
        self.lbl_subtotal.pack(side="left", padx=20, pady=10)

        self.lbl_iva = tk.Label(panel_totales, text="IVA (16%): $0.00", font=("Arial", 11), bg="#f8f9fa")
        self.lbl_iva.pack(side="left", padx=20, pady=10)

        self.lbl_total = tk.Label(panel_totales, text="Total: $0.00", font=("Arial", 12, "bold"), fg="#c0392b",
                                  bg="#f8f9fa")
        self.lbl_total.pack(side="left", padx=20, pady=10)

        btn_generar = tk.Button(panel_totales, text="Generar Ticket / Procesar", bg="#2980b9", fg="white",
                                font=("Arial", 10, "bold"), command=self.procesar_venta)
        btn_generar.pack(side="right", padx=20, pady=10)

    def agregar_al_carrito(self):
        prod_sel = self.cb_productos.get()
        cant_str = self.entry_cant.get()

        if not prod_sel or not cant_str.isdigit():
            messagebox.showerror("Error", "Ingrese una cantidad válida.")
            return

        cant = int(cant_str)
        if cant <= 0:
            messagebox.showerror("Error", "La cantidad debe ser mayor a 0.")
            return

        prod_id = prod_sel.split(" - ")[0]
        producto = next((p for p in PRODUCTOS if p["id"] == prod_id), None)

        if producto:
            if producto["cantidad"] < cant:
                messagebox.showwarning("Stock Insuficiente", f"Solo quedan {producto['cantidad']} unidades en stock.")
                return

            importe = cant * producto["precio"]
            self.carrito.append({
                "id": producto["id"],
                "nombre": producto["nombre"],
                "precio": producto["precio"],
                "cantidad": cant,
                "importe": importe
            })
            self.actualizar_tabla_carrito()

    def actualizar_tabla_carrito(self):
        for item in self.tree_cart.get_children():
            self.tree_cart.delete(item)

        subtotal = 0.0
        for item in self.carrito:
            self.tree_cart.insert("", "end",
                                  values=(item["id"], item["nombre"], f"${item['precio']:.2f}", item["cantidad"],
                                          f"${item['importe']:.2f}"))
            subtotal += item["importe"]

        iva = subtotal * 0.16
        total = subtotal + iva

        self.lbl_subtotal.config(text=f"Subtotal: ${subtotal:.2f}")
        self.lbl_iva.config(text=f"IVA (16%): ${iva:.2f}")
        self.lbl_total.config(text=f"Total: ${total:.2f}")

    def procesar_venta(self):
        if not self.carrito:
            messagebox.showwarning("Atención", "El carrito está vacío.")
            return

        cliente = self.cb_clientes.get()
        subtotal = sum(i["importe"] for i in self.carrito)
        iva = subtotal * 0.16
        total = subtotal + iva

        # Descontar inventario
        for item in self.carrito:
            p = next(prod for prod in PRODUCTOS if prod["id"] == item["id"])
            p["cantidad"] -= item["cantidad"]

        # Crear Ticket Digital
        ticket_win = tk.Toplevel(self.root)
        ticket_win.title("Ticket de Venta Digital")
        ticket_win.geometry("380x500")

        txt = tk.Text(ticket_win, font=("Courier", 10))
        txt.pack(fill="both", expand=True, padx=10, pady=10)

        ticket_txt = "=================================\n"
        ticket_txt += "      TIENDA ZAPATERÍA S.A.     \n"
        ticket_txt += "      TLAHUELILPAN, HIDALGO      \n"
        ticket_txt += "=================================\n"
        ticket_txt += f"Cliente: {cliente}\n"
        ticket_txt += f"Atendido por: {self.usuario}\n"
        ticket_txt += "---------------------------------\n"
        ticket_txt += f"{'Cant':<5}{'Producto':<15}{'Importe':>10}\n"
        ticket_txt += "---------------------------------\n"

        for i in self.carrito:
            ticket_txt += f"{i['cantidad']:<5}{i['nombre'][:14]:<15}${i['importe']:>9.2f}\n"

        ticket_txt += "---------------------------------\n"
        ticket_txt += f"Subtotal:          ${subtotal:>10.2f}\n"
        ticket_txt += f"IVA (16%):         ${iva:>10.2f}\n"
        ticket_txt += f"TOTAL:             ${total:>10.2f}\n"
        ticket_txt += "=================================\n"
        ticket_txt += "   ¡Gracias por su compra!   \n"

        txt.insert("1.0", ticket_txt)
        txt.config(state="disabled")

        # Limpiar carrito
        self.carrito = []
        self.actualizar_tabla_carrito()
        self.actualizar_tabla_inventario()
        messagebox.showinfo("Éxito", "Venta procesada exitosamente.")

    # MÓDULO 2: Inventario de productos
    def setup_inventario(self):
        panel_form = tk.LabelFrame(self.frame_inv, text=" Registrar Nuevo Producto ", bg="white")
        panel_form.pack(fill="x", padx=10, pady=5)

        fields = [("ID:", 0, 0), ("Nombre:", 0, 2), ("Tipo:", 1, 0), ("Cantidad:", 1, 2), ("Talla:", 2, 0),
                  ("Color:", 2, 2), ("Precio:", 3, 0)]
        self.entries_inv = {}

        for label, row, col in fields:
            tk.Label(panel_form, text=label, bg="white").grid(row=row, column=col, padx=5, pady=5, sticky="e")
            ent = tk.Entry(panel_form)
            ent.grid(row=row, column=col + 1, padx=5, pady=5)
            self.entries_inv[label] = ent

        btn_add = tk.Button(panel_form, text="Agregar a Inventario", bg="#27ae60", fg="white",
                            font=("Arial", 9, "bold"), command=self.agregar_producto)
        btn_add.grid(row=3, column=2, columnspan=2, pady=10)

        # Tabla de Productos
        panel_tabla = tk.Frame(self.frame_inv)
        panel_tabla.pack(fill="both", expand=True, padx=10, pady=5)

        cols = ("ID", "Nombre", "Tipo", "Cantidad", "Color", "Talla", "Precio")
        self.tree_inv = ttk.Treeview(panel_tabla, columns=cols, show="headings")
        for c in cols:
            self.tree_inv.heading(c, text=c)
            self.tree_inv.column(c, anchor="center", width=100)
        self.tree_inv.pack(fill="both", expand=True)

        self.actualizar_tabla_inventario()

    def agregar_producto(self):
        e = self.entries_inv
        try:
            nuevo_p = {
                "id": e["ID:"].get(),
                "nombre": e["Nombre:"].get(),
                "tipo": e["Tipo:"].get(),
                "cantidad": int(e["Cantidad:"].get()),
                "color": e["Color:"].get(),
                "talla": e["Talla:"].get(),
                "precio": float(e["Precio:"].get())
            }
            PRODUCTOS.append(nuevo_p)
            self.actualizar_tabla_inventario()
            # Actualizar tabla combinada del punto de venta
            self.cb_productos['values'] = [f"{p['id']} - {p['nombre']} (${p['precio']:.2f})" for p in PRODUCTOS]
            messagebox.showinfo("Éxito", "Producto registrado en el inventario.")
        except ValueError:
            messagebox.showerror("Error", "Asegúrese de ingresar valores numéricos válidos para Precio y Cantidad.")

    def actualizar_tabla_inventario(self):
        for item in self.tree_inv.get_children():
            self.tree_inv.delete(item)
        for p in PRODUCTOS:
            self.tree_inv.insert("", "end",
                                 values=(p["id"], p["nombre"], p["tipo"], p["cantidad"], p["color"], p["talla"],
                                         f"${p['precio']:.2f}"))

    # MÓDULO 3: Gestion de clientes
    def setup_clientes(self):
        panel_form = tk.LabelFrame(self.frame_cli, text=" Registrar Cliente ", bg="white")
        panel_form.pack(fill="x", padx=10, pady=5)

        tk.Label(panel_form, text="ID:", bg="white").grid(row=0, column=0, padx=5, pady=5)
        self.ent_cli_id = tk.Entry(panel_form)
        self.ent_cli_id.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(panel_form, text="Nombre:", bg="white").grid(row=0, column=2, padx=5, pady=5)
        self.ent_cli_nom = tk.Entry(panel_form)
        self.ent_cli_nom.grid(row=0, column=3, padx=5, pady=5)

        btn_reg = tk.Button(panel_form, text="Guardar Cliente", bg="#2980b9", fg="white", command=self.agregar_cliente)
        btn_reg.grid(row=0, column=4, padx=15, pady=5)

        # Tabla Clientes
        cols = ("ID", "Nombre", "Teléfono", "Correo")
        self.tree_cli = ttk.Treeview(self.frame_cli, columns=cols, show="headings")
        for c in cols:
            self.tree_cli.heading(c, text=c)
            self.tree_cli.column(c, anchor="center")
        self.tree_cli.pack(fill="both", expand=True, padx=10, pady=10)

        self.actualizar_tabla_clientes()

    def agregar_cliente(self):
        cid = self.ent_cli_id.get()
        cnom = self.ent_cli_nom.get()
        if cid and cnom:
            CLIENTES.append({"id": cid, "nombre": cnom, "telefono": "S/N", "correo": "S/N"})
            self.actualizar_tabla_clientes()
            self.cb_clientes['values'] = [f"{c['id']} - {c['nombre']}" for c in CLIENTES]
            messagebox.showinfo("Éxito", "Cliente registrado.")

    def actualizar_tabla_clientes(self):
        for item in self.tree_cli.get_children():
            self.tree_cli.delete(item)
        for c in CLIENTES:
            self.tree_cli.insert("", "end", values=(c["id"], c["nombre"], c["telefono"], c["correo"]))


# Ventana de Inicio de Sesion
class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Iniciar Sesión Zapateria ")
        self.root.geometry("400x300")
        self.root.config(bg="#e8f8f5")

        frame = tk.Frame(self.root, bg="#ffffff", bd=2, relief="groove")
        frame.pack(expand=True, padx=20, pady=20)

        tk.Label(frame, text="Iniciar Sesión Zapt V1.0", font=("Arial", 14, "bold"), bg="white", fg="#16a085").grid(
            row=0, column=0, columnspan=2, pady=15)

        tk.Label(frame, text="Usuario:", bg="white", font=("Arial", 10)).grid(row=1, column=0, padx=10, pady=10,
                                                                              sticky="e")
        self.entry_user = tk.Entry(frame, font=("Arial", 10))
        self.entry_user.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(frame, text="Contraseña:", bg="white", font=("Arial", 10)).grid(row=2, column=0, padx=10, pady=10,
                                                                                 sticky="e")
        self.entry_pass = tk.Entry(frame, show="*", font=("Arial", 10))
        self.entry_pass.grid(row=2, column=1, padx=10, pady=10)

        btn_login = tk.Button(frame, text="Iniciar sesión", bg="#16a085", fg="white", font=("Arial", 10, "bold"),
                              command=self.validar_login)
        btn_login.grid(row=3, column=0, columnspan=2, pady=15)

    def validar_login(self):
        usr = self.entry_user.get()
        pwd = self.entry_pass.get()

        if usr in USUARIOS and USUARIOS[usr]["password"] == pwd:
            rol = USUARIOS[usr]["rol"]
            messagebox.showinfo("Acceso Correcto", f"Bienvenido {usr} ({rol})")
            self.root.destroy()  # Cerrar inicio de sesion

            # Abrir ventana principal
            main_root = tk.Tk()
            app = SistemaTiendaGUI(main_root, usr, rol)
            main_root.mainloop()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")


if __name__ == "__main__":
    root_login = tk.Tk()
    login_app = LoginWindow(root_login)
    root_login.mainloop()