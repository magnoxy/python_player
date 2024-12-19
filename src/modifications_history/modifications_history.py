class ModificationHistory:
    def __init__(self, parent):
        """
        Armazena o histórico de modificações realizadas na mídia.
        
        Args:
            parent: Referência ao objeto MainWindow para monitorar `cascade`.
        """
        self.parent = parent  # Salva a referência ao MainWindow
        self.virtual_modification = None
        self.history = []

    def add_virtual_modification(self, entry):
        """
        Atualiza a modificação virtual com os detalhes fornecidos.

        Se `cascade` estiver ativo, adiciona a modificação virtual ao histórico.
        
        Args:
            modification_type (str): Tipo de modificação (e.g., "filtro", "corte").
            description (str): Descrição da modificação.
            params (dict, optional): Parâmetros adicionais da modificação.
        """
        self.virtual_modification = entry

    def add_entry(self, modification_type, description, params=None):
        """
        Adiciona uma entrada ao histórico.

        Se `cascade` estiver ativo, realiza operações específicas.

        Args:
            modification_type (str): Tipo de modificação (e.g., "filtro", "corte").
            description (str): Descrição da modificação (e.g., "filtro Grayscale aplicado").
            params (dict, optional): Parâmetros adicionais da modificação.
        """
        entry = {
            "type": modification_type,
            "description": description,
            "params": params or {}
        }

        self.add_virtual_modification(entry)
        
        if self.parent.cascade:
            self.history.append(self.virtual_modification)


    def get_virtual_modification(self):
        """Retorna a última modificação"""
        return self.virtual_modification
    
    def get_history(self):
        """Retorna o histórico completo de modificações."""
        return self.history

    def clear_history(self):
        """Limpa o histórico de modificações."""
        self.history = []
        self.virtual_modification = None
