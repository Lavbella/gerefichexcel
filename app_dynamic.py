import json
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import customtkinter as ctk
import pandas as pd
import matplotlib.pyplot as plt

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class ExportColumnsWindow(ctk.CTkToplevel):
    """Janela secundária para seleção de colunas."""
    def __init__(self, parent, columns, callback):
        super().__init__(parent)
        self.title("Selecionar Colunas")
        self.geometry("450x500")
        self.after(250, lambda: self.iconbitmap(None))
        self.grab_set()
        
        self.callback = callback
        self.vars = {}

        ctk.CTkLabel(self, text="Escolha as colunas a incluir no Excel:", font=("Arial", 14, "bold")).pack(pady=15)

        self.scroll_frame = ctk.CTkScrollableFrame(self, width=380, height=300)
        self.scroll_frame.pack(fill="both", expand=True, padx=20, pady=5)

        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkButton(btn_frame, text="Selecionar Todas", width=120, fg_color="gray", hover_color="#555555", command=self.select_all).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Desmarcar Todas", width=120, fg_color="gray", hover_color="#555555", command=self.deselect_all).pack(side="left", padx=5)

        for col in columns:
            var = tk.BooleanVar(value=True)
            self.vars[col] = var
            cb = ctk.CTkCheckBox(self.scroll_frame, text=col, variable=var)
            cb.pack(fill="x", pady=5, padx=10)

        ctk.CTkButton(
            self, text="Confirmar e Gravar Excel", font=("Arial", 12, "bold"), fg_color="#2da44e", hover_color="#22863a", height=40, command=self.confirm
        ).pack(fill="x", padx=20, pady=20)

    def select_all(self):
        for var in self.vars.values(): var.set(True)

    def deselect_all(self):
        for var in self.vars.values(): var.set(False)

    def confirm(self):
        selected_cols = [col for col, var in self.vars.items() if var.get()]
        if not selected_cols:
            messagebox.showwarning("Aviso", "Selecione pelo menos uma coluna.")
            return
        self.callback(selected_cols)
        self.destroy()

class DuplicateViewerWindow(ctk.CTkToplevel):
    """Janela secundária para análise isolada de registos duplicados."""
    def __init__(self, parent, dataframe):
        super().__init__(parent)
        self.title("Análise de Registos Duplicados")
        self.geometry("900x550")
        self.after(250, lambda: self.iconbitmap(None))
        self.grab_set()

        self.df_source = dataframe.copy() if dataframe is not None else None

        # Painel Superior de Configuração
        top_bar = ctk.CTkFrame(self, corner_radius=10)
        top_bar.pack(fill="x", padx=15, pady=10)

        ctk.CTkLabel(top_bar, text="Coluna para verificação:", font=("Arial", 12, "bold")).pack(side="left", padx=15, pady=15)
        
        columns = list(self.df_source.columns) if self.df_source is not None else []
        self.cb_dup_col = ctk.CTkComboBox(top_bar, values=columns, width=220, state="readonly" if columns else "disabled")
        self.cb_dup_col.pack(side="left", padx=5, pady=15)
        if columns: self.cb_dup_col.set(columns)

        self.btn_check = ctk.CTkButton(top_bar, text="🔍 Executar Análise", fg_color="#6f42c1", hover_color="#5a32a3", command=self.process_duplicates)
        self.btn_check.pack(side="left", padx=15, pady=15)

        self.lbl_dup_status = ctk.CTkLabel(top_bar, text="Aguardando análise...", font=("Arial", 11, "italic"), text_color="gray")
        self.lbl_dup_status.pack(side="right", padx=15, pady=15)

        # Contentor da Tabela de Duplicados
        self.table_container = ctk.CTkFrame(self, corner_radius=10)
        self.table_container.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        self.tree = ttk.Treeview(self.table_container, show="headings")
        vsb = ttk.Scrollbar(self.table_container, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(self.table_container, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        vsb.pack(side="right", fill="y", padx=(0,2), pady=2)
        hsb.pack(side="bottom", fill="x", padx=2, pady=(0,2))
        self.tree.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.apply_table_theme()

    def apply_table_theme(self):
        style = ttk.Style()
        style.theme_use("default")
        is_dark = ctk.get_appearance_mode() == "Dark"
        bg = "#1e1e1e" if is_dark else "#ffffff"
        fg = "#ffffff" if is_dark else "#000000"
        style.configure(self.tree, background=bg, foreground=fg, fieldbackground=bg, rowheight=26, borderwidth=0)
        style.configure(f"{self.tree}.Heading", background="#2d2d2d" if is_dark else "#f0f0f0", foreground=fg, font=("Arial", 10, "bold"))
        self.row_colors = (bg, "#2a2a2a" if is_dark else "#f9f9f9")

    def process_duplicates(self):
        if self.df_source is None or self.df_source.empty: return

        col = self.cb_dup_col.get()
        if not col: return

        dup_mask = self.df_source.duplicated(subset=[col], keep=False)
        df_dups = self.df_source[dup_mask].sort_values(by=col)

        self.tree.delete(*self.tree.get_children())
        
        if df_dups.empty:
            self.lbl_dup_status.configure(text="Nenhum registo duplicado encontrado.", text_color="#2da44e")
            return

        cols = list(df_dups.columns)
        self.tree["columns"] = cols
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=130, anchor="w")

        for idx, (_, row) in enumerate(df_dups.iterrows()):
            row_values = ["" if pd.isna(val) else val for val in row]
            tag = "even" if idx % 2 == 0 else "odd"
            self.tree.insert("", "end", values=row_values, tags=(tag,))

        self.tree.tag_configure("even", background=self.row_colors)
        self.tree.tag_configure("odd", background=self.row_colors)
        
        self.lbl_dup_status.configure(text=f"Encontradas {len(df_dups)} linhas duplicadas.", text_color="#d73a49")


class UniversalExcelFilterApp(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.title("Filtrador Avançado Universal com Gráficos Estatísticos")
        self.geometry("1400x850")

        self.df = None
        self.filtered_df = None
        self.active_filters = []
        self.sort_ascending = {}

        # --- Bloco Superior: Ficheiro ---
        top_frame = ctk.CTkFrame(self, corner_radius=10)
        top_frame.pack(fill="x", padx=15, pady=10)

        self.btn_load = ctk.CTkButton(top_frame, text="📁 Carregar Ficheiro Excel", font=("Arial", 12, "bold"), command=self.load_file)
        self.btn_load.pack(side="left", padx=15, pady=15)

        self.lbl_status = ctk.CTkLabel(top_frame, text="Aguardando carregamento de ficheiro...", font=("Arial", 11, "italic"), text_color="gray")
        self.lbl_status.pack(side="left", padx=10, pady=15)

        # --- Bloco Central: Filtros ---
        self.filter_container = ctk.CTkFrame(self, corner_radius=10)
        self.filter_container.pack(fill="x", padx=15, pady=5)

        ctk.CTkLabel(self.filter_container, text="⚙️ Construtor de Filtros Dinâmicos", font=("Arial", 13, "bold")).pack(anchor="w", padx=15, pady=(10,0))

        self.btn_add_filter = ctk.CTkButton(self.filter_container, text="➕ Adicionar Condição", fg_color="#6f42c1", hover_color="#5a32a3", width=150, state="disabled", command=self.add_filter_row)
        self.btn_add_filter.pack(anchor="w", padx=15, pady=10)

        self.scroll_filters_frame = ctk.CTkScrollableFrame(self.filter_container, height=120, fg_color="transparent")
        self.scroll_filters_frame.pack(fill="x", padx=10, pady=(0,10))

        # --- Bloco de Ações e Layout Principal Inferior ---
        action_frame = ctk.CTkFrame(self, fg_color="transparent")
        action_frame.pack(fill="x", padx=15, pady=5)

        self.btn_apply = ctk.CTkButton(action_frame, text="🔍 Aplicar Filtros", fg_color="#2da44e", hover_color="#22863a", font=("Arial", 12, "bold"), state="disabled", command=self.apply_filters)
        self.btn_apply.pack(side="left", padx=5)

        self.btn_reset = ctk.CTkButton(action_frame, text="🔄 Limpar Tudo", fg_color="#d73a49", hover_color="#cb2431", state="disabled", command=self.reset_all)
        self.btn_reset.pack(side="left", padx=5)

        self.btn_save_filters = ctk.CTkButton(action_frame, text="💾 Guardar Filtros", fg_color="gray", hover_color="#555555", state="disabled", command=self.save_filters_to_file)
        self.btn_save_filters.pack(side="left", padx=5)

        self.btn_load_filters = ctk.CTkButton(action_frame, text="📂 Carregar Filtros", fg_color="gray", hover_color="#555555", state="disabled", command=self.load_filters_from_file)
        self.btn_load_filters.pack(side="left", padx=5)

        self.btn_export = ctk.CTkButton(action_frame, text="💾 Exportar Excel", fg_color="#005ea2", hover_color="#004f88", font=("Arial", 12, "bold"), state="disabled", command=self.open_export_selector)
        self.btn_export.pack(side="right", padx=5)

        # Botão para abrir a ferramenta de verificação de duplicados
        self.btn_open_dups = ctk.CTkButton(
            action_frame, 
            text="🔍 Ver Duplicados Filtrados", 
            fg_color="#e17055", 
            hover_color="#d65d40", 
            font=("Arial", 12, "bold"), 
            state="disabled", 
            command=self.open_duplicate_viewer
        )
        self.btn_open_dups.pack(side="right", padx=5)

        # Divisão Inferior: Tabela (Esquerda) + Ferramentas de Gráficos (Direita)
        main_bottom_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_bottom_frame.pack(fill="both", expand=True, padx=15, pady=10)

        # Container da Tabela
        table_container = ctk.CTkFrame(main_bottom_frame, corner_radius=10)
        table_container.pack(side="left", fill="both", expand=True, padx=(0,10))

        self.setup_modern_table_styles()
        self.tree = ttk.Treeview(table_container, show="headings", style="Modern.Treeview")
        vsb = ttk.Scrollbar(table_container, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(table_container, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        vsb.pack(side="right", fill="y", padx=(0,2), pady=2)
        hsb.pack(side="bottom", fill="x", padx=2, pady=(0,2))
        self.tree.pack(fill="both", expand=True, padx=5, pady=5)

        # Container de Análise Gráfica (Painel Direito)
        self.chart_container = ctk.CTkFrame(main_bottom_frame, width=280, corner_radius=10)
        self.chart_container.pack(side="right", fill="y")
        self.chart_container.pack_propagate(False)

        ctk.CTkLabel(self.chart_container, text="📊 Análise Estatística", font=("Arial", 14, "bold")).pack(pady=15)
        ctk.CTkLabel(self.chart_container, text="Selecione a Coluna:", font=("Arial", 11)).pack(anchor="w", padx=20)
        
        self.cb_chart_col = ctk.CTkComboBox(self.chart_container, values=["Aguardando Excel..."], width=240, state="disabled")
        self.cb_chart_col.pack(pady=10, padx=20)

        self.btn_bar_chart = ctk.CTkButton(self.chart_container, text="📊 Gráfico de Barras", fg_color="#e17055", hover_color="#d65d40", font=("Arial", 12, "bold"), state="disabled", command=lambda: self.generate_chart("bar"))
        self.btn_bar_chart.pack(fill="x", padx=20, pady=10)

        self.btn_pie_chart = ctk.CTkButton(self.chart_container, text="🍕 Gráfico de Queijo", fg_color="#0984e3", hover_color="#076bba", font=("Arial", 12, "bold"), state="disabled", command=lambda: self.generate_chart("pie"))
        self.btn_pie_chart.pack(fill="x", padx=20, pady=5)

    def setup_modern_table_styles(self):
        style = ttk.Style()
        style.theme_use("default")
        
        is_dark = ctk.get_appearance_mode() == "Dark"
        bg_color = "#1e1e1e" if is_dark else "#ffffff"
        fg_color = "#ffffff" if is_dark else "#000000"
        header_bg = "#2d2d2d" if is_dark else "#f0f0f0"
        header_fg = "#ffffff" if is_dark else "#000000"
        
        # Guardamos as cores individuais para usar nas linhas alternadas
        self.bg_principal = bg_color
        self.bg_alternado = "#2a2a2a" if is_dark else "#f9f9f9"

        style.configure("Modern.Treeview", background=bg_color, foreground=fg_color, fieldbackground=bg_color, rowheight=28, borderwidth=0)
        style.map("Modern.Treeview", background=[("selected", "#005ea2")], foreground=[("selected", "white")])
        style.configure("Modern.Treeview.Heading", background=header_bg, foreground=header_fg, font=("Arial", 10, "bold"), borderwidth=1)

    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx *.xls")])
        if not file_path: return

        try:
            self.df = pd.read_excel(file_path)
            self.df.columns = self.df.columns.astype(str).str.strip()
            self.filtered_df = self.df.copy()

            self.clear_filter_rows()
            self.sort_ascending = {col: True for col in self.df.columns}

            # Ativar controlos de filtros e de gráficos
            self.btn_add_filter.configure(state="normal")
            self.btn_apply.configure(state="normal")
            self.btn_save_filters.configure(state="normal")
            self.btn_load_filters.configure(state="normal")
            self.btn_open_dups.configure(state="normal")

            # Configurar o seletor de colunas para gráficos
            columns = list(self.df.columns)
            self.cb_chart_col.configure(values=columns, state="readonly")
            self.cb_chart_col.set(columns if "QZP" not in columns else "QZP")
            self.btn_bar_chart.configure(state="normal")
            self.btn_pie_chart.configure(state="normal")

            self.lbl_status.configure(text=f"Carregado: {len(self.df)} linhas | {len(self.df.columns)} colunas.", text_color="#2da44e")
            self.add_filter_row()
            self.display_data(self.filtered_df)

        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível ler o ficheiro:\n{str(e)}")

    def generate_chart(self, chart_type):
        """Gera um gráfico do matplotlib com base nos dados atualmente filtrados."""
        if self.filtered_df is None or self.filtered_df.empty:
            messagebox.showwarning("Aviso", "Não existem dados filtrados para gerar gráficos.")
            return

        col = self.cb_chart_col.get()
        if col not in self.filtered_df.columns: return

        # Agrupa e conta a frequência dos dados (limita aos top 15 itens mais frequentes para legibilidade)
        contagem = self.filtered_df[col].dropna().astype(str).value_counts().head(15)

        if contagem.empty:
            messagebox.showinfo("Informação", "A coluna selecionada não contém dados válidos para amostragem.")
            return

        # Fecha janelas de gráficos anteriores abertas para evitar sobreposição
        plt.close('all')

        # Configura o estilo visual do gráfico adaptável ao tema Dark/Light
        is_dark = ctk.get_appearance_mode() == "Dark"
        bg_color = "#1e1e1e" if is_dark else "#ffffff"
        text_color = "#ffffff" if is_dark else "#000000"

        fig, ax = plt.subplots(figsize=(8, 6), facecolor=bg_color)
        ax.set_facecolor(bg_color)

        if chart_type == "bar":
            contagem.plot(kind="bar", ax=ax, color="#0984e3", edgecolor=text_color)
            ax.set_title(f"Distribuição por {col} (Top 15)", color=text_color, fontsize=14, fontweight="bold")
            ax.set_ylabel("Número de Ocorrências", color=text_color)
            ax.tick_params(colors=text_color, labelsize=10)
            plt.xticks(rotation=45, ha='right')
        
        elif chart_type == "pie":
            contagem.plot(kind="pie", ax=ax, autopct='%1.1f%%', startangle=90, textprops={'color': text_color, 'fontsize': 10})
            ax.set_title(f"Proporção por {col} (Top 15)", color=text_color, fontsize=14, fontweight="bold")
            ax.set_ylabel("") # Remove etiqueta vertical padrão do pandas

        plt.tight_layout()
        plt.show() # Abre o gráfico numa janela reativa e interativa nativa com botões de zoom e guardar

    def add_filter_row(self, data_predefinida=None):
        if self.df is None: return
        row_frame = ctk.CTkFrame(self.scroll_filters_frame, fg_color="transparent")
        row_frame.pack(fill="x", pady=4)

        is_first = len(self.active_filters) == 0
        cb_logic = ctk.CTkComboBox(row_frame, values=["E (AND)", "OU (OR)"], width=110)
        cb_logic.pack(side="left", padx=5)
        cb_logic.set(data_predefinida.get("logic", "E (AND)") if data_predefinida else "E (AND)")
        if is_first: cb_logic.configure(state="disabled")

        columns = list(self.df.columns)
        cb_col = ctk.CTkComboBox(row_frame, values=columns, width=200)
        cb_col.pack(side="left", padx=5)
        cb_col.set(data_predefinida.get("column", columns if columns else "") if data_predefinida else (columns if columns else ""))

        conditions = ["Contém (Texto)", "Igual a", "Começa com", "Termina com", "Maior que (>)", "Menor que (<)", "Entre (Intervalo)"]
        cb_cond = ctk.CTkComboBox(row_frame, values=conditions, width=150, command=lambda val, rf=row_frame: self.on_condition_change(rf))
        cb_cond.pack(side="left", padx=5)
        cb_cond.set(data_predefinida.get("condition", "Contém (Texto)") if data_predefinida else "Contém (Texto)")

        ent_val = ctk.CTkEntry(row_frame, width=220, placeholder_text="Digite o valor...")
        ent_val.pack(side="left", padx=5)
        if data_predefinida: ent_val.insert(0, data_predefinida.get("value", ""))

        btn_remove = ctk.CTkButton(row_frame, text="❌", width=35, fg_color="#d73a49", hover_color="#cb2431", command=lambda: self.remove_filter_row(row_frame))
        btn_remove.pack(side="left", padx=5)

        self.active_filters.append({
            "frame": row_frame, "logic": cb_logic, "column": cb_col, "condition": cb_cond, "value": ent_val
        })
        self.on_condition_change(row_frame)

    def on_condition_change(self, row_frame):
        for f in self.active_filters:
            if f["frame"] == row_frame:
                if f["condition"].get() == "Entre (Intervalo)" and not f["value"].get():
                    f["value"].configure(placeholder_text="Ex: Min;Max")

    def remove_filter_row(self, frame):
        frame.destroy()
        self.active_filters = [f for f in self.active_filters if f["frame"] != frame]
        if self.active_filters: self.active_filters["logic"].configure(state="disabled")

    def clear_filter_rows(self):
        for f in self.active_filters: f["frame"].destroy()
        self.active_filters = []

    def display_data(self, dataframe):
        self.tree.delete(*self.tree.get_children())
        columns = list(dataframe.columns)
        self.tree["columns"] = columns
        
        self.setup_modern_table_styles()

        for col in columns:
            self.tree.heading(col, text=col, command=lambda c=col: self.sort_by_column(c))
            self.tree.column(col, width=140, anchor="w")

        for idx, (_, row) in enumerate(dataframe.iterrows()):
            row_values = ["" if pd.isna(val) else val for val in row]
            tag = "even" if idx % 2 == 0 else "odd"
            self.tree.insert("", "end", values=row_values, tags=(tag,))
            
        # Corrigido: Aplicamos apenas uma cor de texto por tag de forma segura
        self.tree.tag_configure("even", background=self.bg_principal)
        self.tree.tag_configure("odd", background=self.bg_alternado)

    def sort_by_column(self, col_name):
        if self.filtered_df is None or self.filtered_df.empty: return
        ascending_mode = self.sort_ascending.get(col_name, True)
        try:
            numeric_col = pd.to_numeric(self.filtered_df[col_name], errors='coerce')
            if numeric_col.notna().sum() > (len(self.filtered_df) / 2):
                self.filtered_df = self.filtered_df.iloc[numeric_col.argsort(kind='mergesort')]
                if not ascending_mode: self.filtered_df = self.filtered_df.iloc[::-1]
            else:
                self.filtered_df = self.filtered_df.sort_values(by=col_name, ascending=ascending_mode, kind='mergesort')
        except Exception:
            self.filtered_df = self.filtered_df.sort_values(by=col_name, ascending=ascending_mode)

        self.sort_ascending[col_name] = not ascending_mode
        self.display_data(self.filtered_df)

    def apply_filters(self):
        if self.df is None: return
        final_mask = pd.Series(True, index=self.df.index)
        first_valid_processed = False

        try:
            for f in self.active_filters:
                col = f["column"].get()
                cond = f["condition"].get()
                val = f["value"].get().strip()
                logic = f["logic"].get()

                if not val: continue

                series_str = self.df[col].astype(str)
                current_mask = pd.Series(False, index=self.df.index)

                if cond == "Contém (Texto)":
                    current_mask = series_str.str.contains(val, case=False, na=False)
                elif cond == "Igual a":
                    current_mask = (series_str == val)
                elif cond == "Começa com":
                    current_mask = series_str.str.startswith(val, na=False)
                elif cond == "Termina com":
                    current_mask = series_str.str.endswith(val, na=False)
                elif cond == "Maior que (>)":
                    current_mask = (pd.to_numeric(self.df[col], errors='coerce') > float(val))
                elif cond == "Menor que (<)":
                    current_mask = (pd.to_numeric(self.df[col], errors='coerce') < float(val))
                elif cond == "Entre (Intervalo)":
                    if ";" not in val: raise ValueError("Use o formato Min;Max")
                    min_val, max_val = val.split(";")
                    numeric_series = pd.to_numeric(self.df[col], errors='coerce')
                    current_mask = (numeric_series >= float(min_val.strip())) & (numeric_series <= float(max_val.strip()))

                if not first_valid_processed:
                    final_mask = current_mask
                    first_valid_processed = True
                else:
                    final_mask = (final_mask | current_mask) if "OU" in logic else (final_mask & current_mask)

            self.filtered_df = self.df[final_mask].copy()
            self.display_data(self.filtered_df)
            self.btn_export.configure(state="normal")
            self.lbl_status.configure(text=f"Filtros aplicados: {len(self.filtered_df)} resultados.", text_color="#005ea2")
        except Exception as e:
            messagebox.showerror("Erro na Filtragem", str(e))

    def save_filters_to_file(self):
        if not self.active_filters: return
        filter_data_list = [{"logic": f["logic"].get(), "column": f["column"].get(), "condition": f["condition"].get(), "value": f["value"].get()} for f in self.active_filters]
        save_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
        if save_path:
            with open(save_path, "w", encoding="utf-8") as file:
                json.dump(filter_data_list, file, indent=4, ensure_ascii=False)
            messagebox.showinfo("Sucesso", "Filtros guardados!")

    def load_filters_from_file(self):
        if self.df is None: return
        file_path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
        if file_path:
            with open(file_path, "r", encoding="utf-8") as file:
                filter_data_list = json.load(file)
            self.clear_filter_rows()
            for item in filter_data_list: self.add_filter_row(data_predefinida=item)
            self.apply_filters()

    def reset_all(self):
        if self.df is None: return
        self.clear_filter_rows()
        self.filtered_df = self.df.copy()
        self.display_data(self.df)
        self.add_filter_row()
        self.btn_export.configure(state="disabled")
        self.lbl_status.configure(text="Ficheiro original restaurado.", text_color="#2da44e")

    def open_export_selector(self):
        if self.filtered_df is None or self.filtered_df.empty: return
        ExportColumnsWindow(self, list(self.df.columns), self.execute_export)

    def execute_export(self, selected_columns):
        save_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel Files", "*.xlsx")])
        if save_path:
            self.filtered_df[selected_columns].to_excel(save_path, index=False)
            messagebox.showinfo("Sucesso", "Ficheiro exportado!")
            
    def open_duplicate_viewer(self):
        """Abre a janela pop-up secundária enviando os dados atualmente filtrados."""
        if self.filtered_df is None or self.filtered_df.empty:
            messagebox.showwarning("Aviso", "Não existem dados filtrados para analisar duplicados.")
            return
        DuplicateViewerWindow(self, self.filtered_df)

if __name__ == "__main__":
    app = UniversalExcelFilterApp()
    app.mainloop()