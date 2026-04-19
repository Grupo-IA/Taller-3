"""
cnf_transform.py — Transformaciones a Forma Normal Conjuntiva (CNF).
El pipeline completo to_cnf() llama a todas las transformaciones en orden.
"""

from __future__ import annotations

from src.logic_core import And, Atom, Formula, Not, Or, Implies, Iff


# --- FUNCION GUÍA SUMINISTRADA COMPLETA ---


def eliminate_double_negation(formula: Formula) -> Formula:
    """
    Elimina dobles negaciones recursivamente.

    Transformacion:
        Not(Not(a)) -> a

    Se aplica recursivamente hasta que no queden dobles negaciones.

    Ejemplo:
        >>> eliminate_double_negation(Not(Not(Atom('p'))))
        Atom('p')
        >>> eliminate_double_negation(Not(Not(Not(Atom('p')))))
        Not(Atom('p'))
    """
    if isinstance(formula, Atom):
        return formula
    if isinstance(formula, Not):
        if isinstance(formula.operand, Not):
            return eliminate_double_negation(formula.operand.operand)
        return Not(eliminate_double_negation(formula.operand))
    if isinstance(formula, And):
        return And(*(eliminate_double_negation(c) for c in formula.conjuncts))
    if isinstance(formula, Or):
        return Or(*(eliminate_double_negation(d) for d in formula.disjuncts))
    return formula


# --- FUNCIONES QUE DEBEN IMPLEMENTAR ---


def eliminate_iff(formula: Formula) -> Formula:
    """
    Elimina bicondicionales recursivamente.

    Transformacion:
        Iff(a, b) -> And(Implies(a, b), Implies(b, a))

    Debe aplicarse recursivamente a todas las sub-formulas.

    Ejemplo:
        >>> eliminate_iff(Iff(Atom('p'), Atom('q')))
        And(Implies(Atom('p'), Atom('q')), Implies(Atom('q'), Atom('p')))

    Hint: Usa pattern matching sobre el tipo de la formula.
          Para cada tipo, aplica eliminate_iff recursivamente a los operandos,
          y solo transforma cuando encuentras un Iff.
    """
    # === YOUR CODE HERE ===
    
    # caso base: nada que transformar
    if isinstance(formula, Atom):
        return formula

    # caso bicondicional
    if isinstance(formula, Iff):
        # uso IA: equivalencia lógica y recursividad
        left = eliminate_iff(formula.left)
        right = eliminate_iff(formula.right)
        return And(Implies(left, right), Implies(right, left))

    # caso negación: recursión sobre operando
    if isinstance(formula, Not):
        return Not(eliminate_iff(formula.operand))

    # caso conjunción: recursión sobre cada uno
    if isinstance(formula, And):
        return And(*(eliminate_iff(c) for c in formula.conjuncts))

    # caso disyunción: recursión sobre cada uno
    if isinstance(formula, Or):
        return Or(*(eliminate_iff(d) for d in formula.disjuncts))

    # caso implicación: procesar subformulas
    if isinstance(formula, Implies):
        return Implies(
            eliminate_iff(formula.antecedent),
            eliminate_iff(formula.consequent)
        )

    # fallback si pasa algo
    return formula

    # === END YOUR CODE ===


def eliminate_implication(formula: Formula) -> Formula:
    """
    Elimina implicaciones recursivamente.

    Transformacion:
        Implies(a, b) -> Or(Not(a), b)

    Debe aplicarse recursivamente a todas las sub-formulas.

    Ejemplo:
        >>> eliminate_implication(Implies(Atom('p'), Atom('q')))
        Or(Not(Atom('p')), Atom('q'))

    Hint: Similar a eliminate_iff. Recorre recursivamente y transforma
          solo los nodos Implies.
    """
    # === YOUR CODE HERE ===
   
    # caso base: fórmula sin transformación
    if isinstance(formula, Atom):
        return formula

    # caso implicación: eliminar usando equivalencia lógica
    if isinstance(formula, Implies):
        # uso IA: equivalencia A → B ≡ ¬A ∨ B
        antecedent = eliminate_implication(formula.antecedent)
        consequent = eliminate_implication(formula.consequent)
        return Or(Not(antecedent), consequent)

    # caso negación: usar recursión sobre el operando
    if isinstance(formula, Not):
        return Not(eliminate_implication(formula.operand))

    # caso conjunción: usar recursión sobre cada operando
    if isinstance(formula, And):
        return And(*(eliminate_implication(c) for c in formula.conjuncts))

    # caso disyunción: usar recursión sobre cada operando
    if isinstance(formula, Or):
        return Or(*(eliminate_implication(d) for d in formula.disjuncts))

   # fallback si pasa algo
    return formula

    # === END YOUR CODE ===


def push_negation_inward(formula: Formula) -> Formula:
    """
    Aplica las leyes de De Morgan y mueve negaciones hacia los atomos.

    Transformaciones:
        Not(And(a, b, ...)) -> Or(Not(a), Not(b), ...)   (De Morgan)
        Not(Or(a, b, ...))  -> And(Not(a), Not(b), ...)   (De Morgan)

    Debe aplicarse recursivamente a todas las sub-formulas.

    Ejemplo:
        >>> push_negation_inward(Not(And(Atom('p'), Atom('q'))))
        Or(Not(Atom('p')), Not(Atom('q')))
        >>> push_negation_inward(Not(Or(Atom('p'), Atom('q'))))
        And(Not(Atom('p')), Not(Atom('q')))

    Hint: Cuando encuentres un Not, revisa que hay adentro:
          - Si es Not(And(...)): aplica De Morgan para convertir en Or de negaciones.
          - Si es Not(Or(...)): aplica De Morgan para convertir en And de negaciones.
          - Si es Not(Atom): dejar como esta.
          Para And y Or sin negacion encima, simplemente recursa sobre los hijos.

    Nota: Esta funcion se llama DESPUES de eliminar Iff e Implies,
          asi que no necesitas manejar esos tipos.
    """
    # === YOUR CODE HERE ===
    if isinstance(formula, Atom):
        return formula
    
    if isinstance(formula, Not):
        inner = formula.operand
        if isinstance(inner, And):
            procesados = []
            for c in inner.conjuncts:
                hijo_transformado = push_negation_inward(Not(c))
                procesados.append(hijo_transformado)
            return Or(*procesados)
        
        if isinstance(inner, Or):
            procesados = []
            for d in inner.disjuncts:
                hijo_transformado = push_negation_inward(Not(d))
                procesados.append(hijo_transformado)
            return And(*procesados)
        
        if isinstance(inner, Not):
            return push_negation_inward(inner.operand)
        
        return Not(push_negation_inward(inner))

    if isinstance(formula, And):
        procesados = []
        for c in formula.conjuncts:
            procesados.append(push_negation_inward(c))
        return And(*procesados)
    
    if isinstance(formula, Or):
        procesados = []
        for d in formula.disjuncts:
            procesados.append(push_negation_inward(d))
        return Or(*procesados)
    
    return formula
    # === END YOUR CODE ===


def distribute_or_over_and(formula: Formula) -> Formula:
    """
    Distribuye Or sobre And para obtener CNF.

    Transformacion:
        Or(A, And(B, C)) -> And(Or(A, B), Or(A, C))

    Debe aplicarse recursivamente hasta que no queden Or que contengan And.

    Ejemplo:
        >>> distribute_or_over_and(Or(Atom('p'), And(Atom('q'), Atom('r'))))
        And(Or(Atom('p'), Atom('q')), Or(Atom('p'), Atom('r')))

    Hint: Para un nodo Or, primero distribuye recursivamente en los hijos.
          Luego busca si algun hijo es un And. Si lo encuentras, aplica la
          distribucion y recursa sobre el resultado (podria haber mas).
          Para And, simplemente recursa sobre cada conjuncion.
          Atomos y Not se retornan sin cambio.

    Nota: Esta funcion se llama DESPUES de mover negaciones hacia adentro,
          asi que solo veras Atom, Not(Atom), And y Or.
    """
    # === YOUR CODE HERE ===
    if isinstance(formula, Atom) or isinstance(formula, Not):
        return formula
    
    if isinstance(formula, And):
        procesados = []
        for c in formula.conjuncts:
            procesados.append(distribute_or_over_and(c))
        return And(*procesados)
    
    if isinstance(formula, Or):
        disjuncts_procesados = []
        for d in formula.disjuncts:
            disjuncts_procesados.append(distribute_or_over_and(d))
        
        for i, d in enumerate(disjuncts_procesados):
            if isinstance(d, And):
                others = disjuncts_procesados[:i] + disjuncts_procesados[i+1:]
                
                new_conjuncts = []
                for a in d.conjuncts:
                    new_conjuncts.append(distribute_or_over_and(Or(a, *others)))
                return And(*new_conjuncts)
        
        return Or(*disjuncts_procesados)

    return formula
    # === END YOUR CODE ===


def flatten(formula: Formula) -> Formula:
    """
    Aplana conjunciones y disyunciones anidadas.

    Transformaciones:
        And(And(a, b), c) -> And(a, b, c)
        Or(Or(a, b), c)   -> Or(a, b, c)

    Debe aplicarse recursivamente.

    Ejemplo:
        >>> flatten(And(And(Atom('a'), Atom('b')), Atom('c')))
        And(Atom('a'), Atom('b'), Atom('c'))
        >>> flatten(Or(Or(Atom('a'), Atom('b')), Atom('c')))
        Or(Atom('a'), Atom('b'), Atom('c'))

    Hint: Para un And, recorre cada hijo. Si un hijo tambien es And,
          agrega sus conjuncts directamente en vez de agregar el And.
          Igual para Or con sus disjuncts.
          Si al final solo queda 1 elemento, retornalo directamente.
    """
    # === YOUR CODE HERE ===
    if isinstance(formula, Atom) or isinstance(formula, Not):
        return formula
    
    if isinstance(formula, And):
        new_conjuncts = []
        for c in formula.conjuncts:
            c_flat = flatten(c)
            if isinstance(c_flat, And):
                new_conjuncts.extend(c_flat.conjuncts)
            else:
                new_conjuncts.append(c_flat)
        
        if len(new_conjuncts) > 1:
            return And(*new_conjuncts)
        else:
            return new_conjuncts[0]

    if isinstance(formula, Or):
        new_disjuncts = []
        for d in formula.disjuncts:
            d_flat = flatten(d)
            if isinstance(d_flat, Or):
                new_disjuncts.extend(d_flat.disjuncts)
            else:
                new_disjuncts.append(d_flat)
            
        if len(new_disjuncts) > 1:
            return Or(*new_disjuncts)
        else:
            return new_disjuncts[0]

    return formula
    # === END YOUR CODE ===


# --- PIPELINE COMPLETO ---


def to_cnf(formula: Formula) -> Formula:
    """
    [DADO] Pipeline completo de conversion a CNF.

    Aplica todas las transformaciones en el orden correcto:
    1. Eliminar bicondicionales (Iff)
    2. Eliminar implicaciones (Implies)
    3. Mover negaciones hacia adentro (Not)
    4. Eliminar dobles negaciones (Not Not)
    5. Distribuir Or sobre And
    6. Aplanar conjunciones/disyunciones

    Ejemplo:
        >>> to_cnf(Implies(Atom('p'), And(Atom('q'), Atom('r'))))
        And(Or(Not(Atom('p')), Atom('q')), Or(Not(Atom('p')), Atom('r')))
    """
    formula = eliminate_iff(formula)
    formula = eliminate_implication(formula)
    formula = push_negation_inward(formula)
    formula = eliminate_double_negation(formula)
    formula = distribute_or_over_and(formula)
    formula = flatten(formula)
    return formula
