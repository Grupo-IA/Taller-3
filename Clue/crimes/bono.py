"""
bono.py — Filtración de la pelicula de Avatar Studios

La película completa "Aang: The Last Airbender" se filtró en redes sociales ayer tras un presunto error de envío.
Paramount confirmó que el material incluye escenas clave y secuencias sin terminar (fragmentos 3D).
El Editor Jefe envió un email a un destinatario externo el día de ayer.
Un Animador Senior estaba en el servidor de renderizado durante la filtración, pero sin acceso a correos.
El servidor de renderizado es una red aislada es imposible enviar correos externos desde allí.
La Directora del Estudio es la autoridad máxima tiene acceso a correos, estaba conectada y envió un correo al Animador Senior ayer.
El Becario declara que el Editor Jefe estuvo en una reunión desconectado durante la hora del envío.
La Directora, el Animador Senior y el Editor Jefe tienen acceso a la pelicula completa.

Como detective de ciberseguridad, he llegado a las siguientes conclusiones:
Quien estaba en una red aislada sin acceso a herramientas de difusión está descartado.
El culpable debe tener acceso a correo.
Solo alguien con acceso la pelicula completa puede ser responsable de la filtración.
El responsable debió estar desconectado durante la hora del envío.
El correo debió estar dirigido a un destinatario externo para que se filtrara en redes sociales.
"""

from src.crime_case import CrimeCase, QuerySpec
from src.predicate_logic import ExistsGoal, KnowledgeBase, Predicate, Rule, Term

def crear_kb() -> KnowledgeBase:
    """Construye la KB según la narrativa del módulo."""
    kb = KnowledgeBase()

    # Constantes del caso
    editor_jefe  = Term("editor_jefe")
    animador     = Term("animador_senior")
    directora    = Term("directora_estudio")
    becario      = Term("becario")
    red_aislada  = Term("red_render")
    email_server = Term("servidor_correo")
    externo      = Term("externo")

    # HECHOS
    kb.add_fact(Predicate("acceso_pelicula", (editor_jefe,)))
    kb.add_fact(Predicate("acceso_pelicula", (animador,)))
    kb.add_fact(Predicate("acceso_pelicula", (directora,)))
    kb.add_fact(Predicate("ubicacion", (animador, red_aislada)))
    kb.add_fact(Predicate("es_red_aislada", (red_aislada,)))
    kb.add_fact(Predicate("tiene_acceso_correo", (editor_jefe,)))
    kb.add_fact(Predicate("tiene_acceso_correo", (directora,)))
    kb.add_fact(Predicate("estado_desconectado", (editor_jefe,)))
    kb.add_fact(Predicate("envio_correo_a", (editor_jefe, externo)))
    kb.add_fact(Predicate("envio_correo_a", (directora, animador)))

    # REGLAS
    X, R, D = Term("$X"), Term("$R"), Term("$D")

    kb.add_rule(Rule(Predicate("descartado", (X,)),
        [Predicate("ubicacion", (X, R)), Predicate("es_red_aislada", (R,))]
    ))
    kb.add_rule(Rule(Predicate("sospechoso_tecnico", (X,)),
        [Predicate("acceso_pelicula", (X,)), Predicate("tiene_acceso_correo", (X,))]
    ))
    kb.add_rule(Rule(Predicate("envio_externo_detectado", (X,)),
        [Predicate("envio_correo_a", (X, externo))]
    ))
    kb.add_rule(Rule(Predicate("responsable_filtracion", (X,)),
        [Predicate("sospechoso_tecnico", (X,)),
         Predicate("envio_externo_detectado", (X,)),
         Predicate("estado_desconectado", (X,))
        ]
    ))

    return kb

CASE = CrimeCase(
    id="filtracion_avatar_estudios",
    title="Filtración de la película de Avatar Studios",
    suspects=("editor_jefe", "animador_senior", "directora_estudio", "becario"),
    narrative=__doc__,
    description=(
        "La película de Aang se filtró. El Editor Jefe envió un correo externo "
        "estando supuestamente desconectado, mientras que la Directora solo "
        "envió correos internos y el Animador no tenía acceso a la red."
    ),
    create_kb=crear_kb,
    queries=(
        QuerySpec(
            description="¿Está el Animador Senior descartado?",
            goal=Predicate("descartado", (Term("animador_senior"),)),
        ),
        QuerySpec(
            description="¿Es la Directora una sospechosa técnica?",
            goal=Predicate("sospechoso_tecnico", (Term("directora_estudio"),)),
        ),
        QuerySpec(
            description="¿La Directora realizó un envío externo?",
            goal=Predicate("envio_externo_detectado", (Term("directora_estudio"),)),
        ),
        QuerySpec(
            description="¿Es el Editor Jefe el responsable de la filtración?",
            goal=Predicate("responsable_filtracion", (Term("editor_jefe"),)),
        ),
        QuerySpec(
            description="¿Existe algún responsable identificado?",
            goal=ExistsGoal("$Alguien", Predicate("responsable_filtracion", (Term("$Alguien"),))),
        ),
    ),
)