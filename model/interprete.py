from dataclasses import dataclass
import datetime
from dataclasses import dataclass, field


@dataclass
class Interprete:
    id: str
    name: str
    date_of_birth: datetime.date | None
    film: set = field(default_factory=set)
    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id

    def __str__(self):
        return self.name