class DFAMachine:
    def __init__(self, transitions, initial_state, accept_states):
        self.transitions = transitions
        self.initial_state = initial_state
        self.accept_states = accept_states

    def process(self, tokens: list[str]) -> bool:
        # Otomat alt-dizi taraması: Herhangi bir token pozisyonundan başlayarak
        # saldırı durumuna (accept_state) ulaşılıp ulaşılamadığına bakar.
        n = len(tokens)
        for start_idx in range(n):
            current = self.initial_state
            for j in range(start_idx, n):
                t = tokens[j]
                current = self.transitions.get((current, t))
                if not current:
                    break
                if current in self.accept_states:
                    return True
        return False
