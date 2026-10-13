from dataclasses import dataclass, field


@dataclass
class Actor:
    id: str
    name: str
    height: int
    date_of_birth: str
    known_for_movies: str
    lista_film: list = field(default_factory=list)



    def __hash__(self):
        return hash(self.id)

    def __str__(self):
        return f"{self.name}"

    def __eq__(self, other):
        return self.id == other.id

    def count_film(self):
        return len(self.lista_film)