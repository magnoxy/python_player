class ModificationHistory:
    def __init__(self):
        """Armazena o histórico de modificações realizadas na mídia"""
        self.history = []

    def add_entry(self, modification_type, description, params=None):
        """
        Adiciona uma entrada ao histórico.
        
        Args:
            modification_type (str): Tipo de modificação (e.g., "Filtro", "Corte").
            description (str): Descrição da modificação (e.g., "Filtro Grayscale aplicado").
            params (dict, optional): Parâmetros adicionais da modificação.
        """
        entry = {
            "type": modification_type,
            "description": description,
            "params": params or {}
        }
        self.history.append(entry)

    def get_history(self):
        """Retorna o histórico completo de modificações."""
        return self.history

    def clear_history(self):
        """Limpa o histórico de modificações."""
        self.history = []
