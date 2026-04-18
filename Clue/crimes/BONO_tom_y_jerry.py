"""
BONO_tom_y_jerry.py — El Robo del Queso

El queso desapareció de la cocina durante la noche. Tom fue visto cerca de la nevera y dejo
arañazos en la puerta. Jerry tiene acceso a la nevera y fue encontrado con boronas de queso. 
Spike estuvo en el patio toda la noche y no estuvo cerca de la cocina. Nibbles fue visto en el
pasillo pero no tiene acceso a la nevera ni evidencia en su contra. Tom acusa a Jerry;
Jerry dice que Tom dejo arañazos en la puerta; Tom dice que Jerry actuó solo.

Como detective, he llegado a las siguientes conclusiones:
Quien estaba lejos de la escena queda descartado. 
Quien fue visto solo en el pasillo queda descartado. 
Quien dejo arañazos en la puerta forzó el acceso y es cómplice.
Quien tiene boronas y acceso directo a la nevera es el autor principal.
El autor principal y el cómplice son culpables.
Si hay autor principal y cómplice, operaron juntos.
"""

from src.crime_case import CrimeCase, QuerySpec
from src.predicate_logic import ExistsGoal, ForallGoal, KnowledgeBase, Predicate, Rule, Term


def crear_kb() -> KnowledgeBase:
    """Construye la KB según la narrativa del módulo."""
    kb = KnowledgeBase()

    # Constantes del caso
    tom     = Term("tom")
    jerry   = Term("jerry")
    spike   = Term("spike")
    nibbles = Term("nibbles")

    # --- HECHOS ---

    kb.add_fact(Predicate("visto_cerca_nevera",        (tom,)))
    kb.add_fact(Predicate("dejo_arañazos_en_puerta",        (tom,)))
    kb.add_fact(Predicate("acceso_nevera",             (jerry,)))
    kb.add_fact(Predicate("tiene_boronas_de_queso",          (jerry,)))
    kb.add_fact(Predicate("ubicacion_alejada",         (spike,)))
    kb.add_fact(Predicate("acusa",                     (tom, jerry)))
    kb.add_fact(Predicate("visto_en_pasillo",          (nibbles,)))

    # --- REGLAS ---

    X = Term("$X")
    Y = Term("$Y")

    # Quien estaba lejos de la escena queda descartado
    kb.add_rule(Rule(
        head=Predicate("descartado",       (X,)),
        body=[Predicate("ubicacion_alejada", (X,))],
    ))

    # Quien fue visto solo en el pasillo queda descartado
    kb.add_rule(Rule(
        head=Predicate("descartado",       (X,)),
        body=[Predicate("visto_en_pasillo", (X,))],
    ))

    # Quien dejo arañazos en la puerta forzó el acceso
    kb.add_rule(Rule(
        head=Predicate("forzó_acceso",     (X,)),
        body=[Predicate("dejo_arañazos_en_puerta", (X,))],
    ))

    # Quien forzó el acceso es cómplice
    kb.add_rule(Rule(
        head=Predicate("complice",         (X,)),
        body=[Predicate("forzó_acceso",    (X,))],
    ))

    # Quien tiene boronas de queso y acceso a la nevera es el autor principal
    kb.add_rule(Rule(
        head=Predicate("autor_principal",  (X,)),
        body=[
            Predicate("tiene_boronas_de_queso",  (X,)),
            Predicate("acceso_nevera",     (X,)),
        ],
    ))

    # El autor principal es culpable
    kb.add_rule(Rule(
        head=Predicate("culpable",         (X,)),
        body=[Predicate("autor_principal", (X,))],
    ))

    # El cómplice también es culpable
    kb.add_rule(Rule(
        head=Predicate("culpable",         (X,)),
        body=[Predicate("complice",        (X,))],
    ))

    # Autor principal + cómplice → operaron juntos
    kb.add_rule(Rule(
        head=Predicate("operacion_conjunta", (X, Y)),
        body=[
            Predicate("autor_principal",   (X,)),
            Predicate("complice",          (Y,)),
        ],
    ))

    return kb


CASE = CrimeCase(
    id="BONO_tom_y_jerry",
    title="El Robo del Queso",
    suspects=("tom", "jerry", "spike", "nibbles"),
    narrative=__doc__,
    description=(
        "El queso desapareció de la cocina. Jerry tiene acceso y boronas encima. "
        "Tom dejo arañazos en la puerta. Spike durmió en el patio. Nibbles fue visto en el pasillo. "
    ),
    create_kb=crear_kb,
    queries=(
        QuerySpec(
            description="¿Spike está descartado?",
            goal=Predicate("descartado", (Term("spike"),)),
        ),
        QuerySpec(
            description="¿Nibbles está descartado?",
            goal=Predicate("descartado", (Term("nibbles"),)),
        ),
        QuerySpec(
            description="¿Tom forzó el acceso?",
            goal=Predicate("forzó_acceso", (Term("tom"),)),
        ),
        QuerySpec(
            description="¿Tom es cómplice?",
            goal=Predicate("complice", (Term("tom"),)),
        ),
        QuerySpec(
            description="¿Jerry es el autor principal?",
            goal=Predicate("autor_principal", (Term("jerry"),)),
        ),
        QuerySpec(
            description="¿Jerry es culpable?",
            goal=Predicate("culpable", (Term("jerry"),)),
        ),
        QuerySpec(
            description="¿Tom y Jerry operaron en conjunto?",
            goal=Predicate("operacion_conjunta", (Term("jerry"), Term("tom"))),
        ),
        QuerySpec(
            description="¿Existe algún culpable?",
            goal=ExistsGoal("$X", Predicate("culpable", (Term("$X"),))),
        ),
        QuerySpec(
            description="¿Todo autor principal tiene acceso a la nevera?",
            goal=ForallGoal(
                "$X",
                Predicate("autor_principal", (Term("$X"),)),
                Predicate("acceso_nevera",   (Term("$X"),)),
            ),
        ),
    ),
)