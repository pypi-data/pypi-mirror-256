"""
The set of parse-nodes in simple form.
The parser calls these constructors with subordinate semantic-values in a bottom-up tree transduction.
These constructors may add a touch of organization.
Class-level type annotations make peace with pycharm wherever later passes add fields.
"""
from pathlib import Path
from typing import Optional, Any, Sequence, NamedTuple, Union
from boozetools.parsing.interface import SemanticError
from .ontology import (
	Nom, Symbol, NS, Reference,
	Expr, Term,
)

class MismatchedBookendsError(SemanticError):
	# The one semantic error we catch early enough to interrupt the parse.
	# It's early warning that things have gotten out of whack.
	def __init__(self, head: slice, coda: slice):
		super().__init__(head, coda)

class TypeParameter(Symbol):
	def __init__(self, nom:Nom):
		super().__init__(nom)
	def head(self) -> slice:
		return self.nom.head()
	def has_value_domain(self) -> bool:
		return False

class TypeDeclaration(Symbol):
	param_space: NS   # Will address the type parameters. Word-definer fills this.
	type_params: tuple[TypeParameter, ...]
	
	def __init__(self, nom: Nom, type_params:tuple[TypeParameter, ...]):
		super().__init__(nom)
		self.type_params = type_params

def type_parameters(param_names:Sequence[Nom]):
	return tuple(TypeParameter(n) for n in param_names)



class SimpleType(Expr):
	def can_construct(self) -> bool: raise NotImplementedError(type(self))

class ValExpr(Expr):
	is_volatile: bool
	pass

class PlainReference(Reference):
	def head(self) -> slice: return self.nom.head()
	def __str__(self): return "<ref:%s>"%self.nom.text

class QualifiedReference(Reference):
	space: Nom
	def __init__(self, nom:Nom, space:Nom):
		super().__init__(nom)
		self.space = space
	def head(self) -> slice:
		return slice(self.nom.head().start, self.space.head().stop)

ARGUMENT_TYPE = Union[SimpleType, "ImplicitTypeVariable", "ExplicitTypeVariable"]

class ArrowSpec(SimpleType):
	lhs: Sequence[ARGUMENT_TYPE]
	_head: Nom
	rhs: ARGUMENT_TYPE
	
	def __init__(self, lhs, _head:Nom, rhs):
		assert rhs is not None
		self.lhs = lhs
		self._head = _head
		self.rhs = rhs
	def head(self) -> slice: return self._head.head()
	def can_construct(self) -> bool: return False

class MessageSpec(SimpleType):
	type_exprs: Sequence[ARGUMENT_TYPE]
	def __init__(self, _head:Nom, type_exprs):
		self._head = _head
		self.type_exprs = type_exprs or ()
	def head(self): return self._head.head()
	def can_construct(self) -> bool: return False

class TypeCall(SimpleType):
	def __init__(self, ref: Reference, arguments: Optional[Sequence[ARGUMENT_TYPE]] = ()):
		assert isinstance(ref, Reference)
		self.ref, self.arguments = ref, arguments or ()
	def head(self) -> slice: return self.ref.head()
	def can_construct(self) -> bool: return self.ref.dfn.has_value_domain()

class ImplicitTypeVariable:
	""" Stand-in as the relevant type-expression for when the syntax doesn't bother. """
	def __init__(self, head:Nom):
		self._head = head
	def head(self) -> slice:
		return self._head.head()

class ExplicitTypeVariable(Reference):
	def __init__(self, _hook, nom:Nom):
		super().__init__(nom)
		self._hook = _hook
	def head(self) -> slice:
		return slice(self._hook.head().start, self.nom.head().stop)

class FormalParameter(Symbol):
	def has_value_domain(self): return True
	def __init__(self, stricture, nom:Nom, type_expr: Optional[ARGUMENT_TYPE]):
		super().__init__(nom)
		self.is_strict = stricture is not None
		self.type_expr = type_expr
	def head(self) -> slice: return self.nom.head()
	def key(self): return self.nom.key()
	def __repr__(self): return "<:%s:%s>"%(self.nom.text, self.type_expr)

def FieldDefinition(nom:Nom, type_expr: Optional[ARGUMENT_TYPE]):
	return FormalParameter(None, nom, type_expr)

class RecordSpec:
	field_space: NS  # WordDefiner pass fills this in.
	def __init__(self, fields: list[FormalParameter]):
		self.fields = fields
	
	def field_names(self):
		return [f.nom.text for f in self.fields]

class VariantSpec(NamedTuple):
	subtypes: list["SubTypeSpec"]

class Opaque(TypeDeclaration):
	def has_value_domain(self): return False

class TypeAlias(TypeDeclaration):
	body: SimpleType
	def __init__(self, nom: Nom, type_params:tuple[TypeParameter, ...], body:SimpleType):
		super().__init__(nom, type_params)
		self.body = body
	def has_value_domain(self) -> bool: return self.body.can_construct()

class Record(TypeDeclaration):
	def __init__(self, nom: Nom, type_params:tuple[TypeParameter, ...], spec:RecordSpec):
		super().__init__(nom, type_params)
		self.spec = spec
	def has_value_domain(self) -> bool: return True

class Variant(TypeDeclaration):
	sub_space: NS  # WordDefiner pass fills this in.
	def __init__(self, nom: Nom, type_params:tuple[TypeParameter, ...], spec:VariantSpec):
		super().__init__(nom, type_params)
		self.subtypes = spec.subtypes
		for s in spec.subtypes: s.variant = self
	def has_value_domain(self) -> bool: return False

class MethodSpec(Symbol):
	interface_decl : "Interface"
	def __init__(self, nom:Nom, type_exprs:Sequence[SimpleType]):
		super().__init__(nom)
		self.type_exprs = type_exprs
	def has_value_domain(self) -> bool: return False

class Interface(TypeDeclaration):
	method_space: NS
	def __init__(self, nom: Nom, type_params:tuple[TypeParameter, ...], spec:Sequence[MethodSpec]):
		super().__init__(nom, type_params)
		self.spec = spec
	def has_value_domain(self) -> bool: return False

class SubTypeSpec(Symbol):
	body: Optional[Union[RecordSpec, TypeCall, ArrowSpec]]
	variant: Variant
	# To clarify: The SubType here describes a *tagged* value, not the type of the value so tagged.
	# One can tag any kind of value; even a function. Therefore yes, you can always
	# treat a (tagged) subtype as a function. At least, once everything works right.
	def has_value_domain(self) -> bool: return True
	def __init__(self, nom:Nom, body=None):
		super().__init__(nom)
		self.body = body
	def head(self) -> slice: return self.nom.head()
	def key(self): return self.nom.key()
	def __repr__(self): return "<:%s:%s>"%(self.nom.text, self.body)

class Assumption(NamedTuple):
	names: list[Nom]
	type_expr: SimpleType

def _bookend(head: Nom, coda: Nom):
	if head.text != coda.text:
		raise MismatchedBookendsError(head.head(), coda.head())

class Function(Term):
	"""
	Representation shared between two subclasses.
	They differ only to distinguish semantics.
	"""
	source_path: Path
	namespace: NS
	params: Sequence[FormalParameter]
	where: Sequence["UserFunction"]
	
	def __init__(
			self,
			nom: Nom,
			params: Sequence[FormalParameter],
			expr_type: Optional[ARGUMENT_TYPE],
			expr: ValExpr,
			where: Optional["WhereClause"]
	):
		super().__init__(nom)
		self.params = params or ()
		self.strictures = tuple(i for i, p in enumerate(self.params) if p.is_strict)
		self.result_type_expr = expr_type
		self.expr = expr
		if where:
			_bookend(nom, where.coda)
			self.where = where.sub_fns
		else:
			self.where = ()
			
	def has_volatility(self):
		return self.expr.is_volatile or any(f.has_volatility() for f in self.where)
	
	def head(self) -> slice:
		return self.nom.head()
	
	def __repr__(self):
		p = ", ".join(map(str, self.params))
		return "{fn|%s(%s)}" % (self.nom.text, p)

class UserFunction(Function):
	pass

class OperatorOverload(Function):
	pass

class WhereClause(NamedTuple):
	sub_fns: Sequence[UserFunction]
	coda: Nom

class UserAgent(Term):
	source_path: Path
	field_space: NS
	fields: Sequence[FormalParameter]
	message_space: NS
	def head(self) -> slice: return self.nom.head()
	def __init__(
		self,
		nom: Nom,
		fields: Optional[Sequence[FormalParameter]],
		behaviors: Sequence["Behavior"],
		coda: Nom,
	):
		super().__init__(nom)
		self.fields = fields or ()
		self.behaviors = behaviors
		_bookend(nom, coda)

	def field_names(self):
		return [f.nom.text for f in self.fields]


class Behavior(Term):
	source_path: Path
	namespace: NS
	def head(self) -> slice: return self.nom.head()
	def __repr__(self):
		p = ", ".join(map(str, self.params))
		return "{to %s(%s)}" % (self.nom.text, p)
	def __init__(
		self,
		nom: Nom,
		params: Sequence[FormalParameter],
		expr: ValExpr,
	):
		super().__init__(nom)
		self.params = params or ()
		for p in self.params: p.is_strict = True
		self.expr = expr

class Literal(ValExpr):
	is_volatile = False  # Not that this will ever be tested, but it's well to be consistent.
	
	def __init__(self, value: Any, a_slice: slice):
		self.value, self._slice = value, a_slice
	
	def __str__(self):
		return "<Literal %r>" % self.value
	
	def head(self) -> slice:
		return self._slice

def truth(a_slice:slice): return Literal(True, a_slice)
def falsehood(a_slice:slice): return Literal(False, a_slice)

class Lookup(ValExpr):
	# Reminder: This AST node exists in opposition to TypeCall so I can write
	# behavior for references in value context vs. references in type context.
	ref:Reference
	is_volatile = False
	def __init__(self, ref: Reference): self.ref = ref
	def head(self) -> slice: return self.ref.head()
	def __str__(self): return str(self.ref)

def is_self_reference(it):
	if isinstance(it, Lookup):
		if isinstance(it.ref, PlainReference):
			return it.ref.nom.text == "SELF"
	return False

class FieldReference(ValExpr):
	def __init__(self, lhs: ValExpr, field_name: Nom):
		self.lhs, self.field_name = lhs, field_name
		self.is_volatile = lhs.is_volatile or is_self_reference(lhs)
	def __str__(self): return "(%s.%s)" % (self.lhs, self.field_name.text)
	def head(self) -> slice: return self.field_name.head()

class BindMethod(ValExpr):
	def __init__(self, receiver: ValExpr, _bang:Nom, method_name: Nom):
		self.receiver, self.method_name = receiver, method_name
		self._head = _bang.head()
		self.is_volatile = receiver.is_volatile
	def __str__(self): return "(%s.%s)" % (self.receiver, self.method_name.text)
	def head(self) -> slice: return self._head

class AsTask(ValExpr):
	is_volatile = False
	def __init__(self, head:slice, sub:ValExpr):
		self._head = head
		self.sub = sub
	def head(self) -> slice: return self._head

class Skip(ValExpr):
	is_volatile = False
	def __init__(self, head: slice): self._head = head
	def head(self) -> slice: return self._head

class Binary(ValExpr):
	def __init__(self, lhs: ValExpr, op:Nom, rhs: ValExpr):
		self.lhs, self.op, self.rhs = lhs, op, rhs
		self.is_volatile = self.lhs.is_volatile or self.rhs.is_volatile
	def head(self) -> slice: return self.op.head()

class BinExp(Binary): pass
class ShortCutExp(Binary): pass

class UnaryExp(ValExpr):
	def __init__(self, op:Nom, arg: ValExpr):
		self.op, self.arg = op, arg
		self.is_volatile = arg.is_volatile

	def head(self) -> slice: return self.op.head()

class Cond(ValExpr):
	_kw: slice
	def __init__(self, then_part: ValExpr, _kw, if_part: ValExpr, else_part: ValExpr):
		self._kw = _kw
		self.then_part, self.if_part, self.else_part = then_part, if_part, else_part
		self.is_volatile = any(x.is_volatile for x in (then_part, if_part, else_part))
	def head(self) -> slice:
		return self._kw

def CaseWhen(when_parts: list, else_part: ValExpr):
	for _kw, test, then in reversed(when_parts):
		else_part = Cond(then, _kw, test, else_part)
	return else_part

class Call(ValExpr):
	def __init__(self, fn_exp: ValExpr, args: list[ValExpr]):
		self.fn_exp, self.args = fn_exp, args
		self.is_volatile = self.fn_exp.is_volatile or any(a.is_volatile for a in args)
	
	def __str__(self):
		return "%s(%s)" % (self.fn_exp, ', '.join(map(str, self.args)))
	
	def head(self) -> slice: return self.fn_exp.head()

def call_upon_list(fn_exp: ValExpr, list_arg: ValExpr):
	return Call(fn_exp, [list_arg])

class ExplicitList(ValExpr):
	def __init__(self, elts: list[ValExpr]):
		for e in elts:
			assert isinstance(e, ValExpr), e
		self.elts = elts
		self.is_volatile = any(e.is_volatile for e in elts)
		
	def head(self) -> slice:
		return slice(self.elts[0].head().start, self.elts[-1].head().stop)

class Alternative(Symbol):
	sub_expr: ValExpr
	where: Sequence[UserFunction]
	
	namespace: NS  # WordDefiner fills

	def __init__(self, pattern:Nom, _head:Nom, sub_expr:ValExpr, where:Optional[WhereClause]):
		super().__init__(pattern)
		self._head = _head
		self.sub_expr = sub_expr
		if where:
			_bookend(pattern, where.coda)
			self.where = where.sub_fns
		else:
			self.where = ()
	def head(self) -> slice:
		return self._head.head()
	
	def has_volatility(self):
		return self.sub_expr.is_volatile or any(f.has_volatility() for f in self.where)

class Absurdity(ValExpr):
	is_volatile = False
	def __init__(self, _head:slice, reason:Literal):
		self._head = _head
		self.reason = reason
	def head(self) -> slice:
		return slice(self._head.start, self.reason.head().stop)

def absurdAlternative(pattern:Nom, _head:Nom, absurdity:Absurdity):
	return Alternative(pattern, _head, absurdity, None)
	
class Subject(Term):
	""" Within a match-case, a name must reach a different symbol with the particular subtype """
	expr: ValExpr
	def __init__(self, expr: ValExpr, nom: Nom):
		super().__init__(nom)
		self.expr = expr

def simple_subject(nom:Nom):
	return Subject(Lookup(PlainReference(nom)), nom)

class MatchExpr(ValExpr):
	subject:Subject  # Symbol in scope within alternative expressions; contains the value of interest
	hint: Optional[Reference]
	alternatives: list[Alternative]
	otherwise: Optional[ValExpr]
	
	namespace: NS  # WordDefiner fills
	
	variant:Variant  # Filled in match-check pass
	dispatch: dict[Optional[str]:ValExpr]
	
	def __init__(self, subject, hint, alternatives, otherwise):
		self.subject = subject
		self.hint = hint
		self.alternatives, self.otherwise = alternatives, otherwise
		self.is_volatile = subject.expr.is_volatile or any(a.has_volatility() for a in alternatives) or (otherwise and otherwise.is_volatile)
	
	def head(self) -> slice:
		return self.subject.head()

class NewAgent(Term):
	def __init__(self, nom:Nom, expr:ValExpr):
		super().__init__(nom)
		self.expr = expr

class DoBlock(ValExpr):
	namespace: NS  # WordDefiner fills
	
	# The value of a do-block does not depend on when it runs.
	# Its consequence may so depend, but by definition steps run in sequence.

	is_volatile = False

	def __init__(self, agents:list[NewAgent], _head:Nom, steps:list[ValExpr]):
		self.agents = agents
		self.steps = steps
		self._head = _head
		
	def head(self) -> slice:
		return self._head.head()

class AssignField(Reference):
	def __init__(self, nom:Nom, expr:ValExpr):
		super().__init__(nom)
		self.expr = expr
	def head(self) -> slice:
		return self.nom.head()

class ImportSymbol(NamedTuple):
	yonder : Nom
	hither : Optional[Nom]

class ImportModule(Symbol):
	module_key: Path  # Module loader fills this.
	def __init__(self, package:Optional[Nom], relative_path:Literal, nom:Optional[Nom], vocab:Optional[Sequence[ImportSymbol]]):
		super().__init__(nom)
		self.package = package
		self.relative_path = relative_path
		self.vocab = vocab or ()

class FFI_Alias(Term):
	""" Built-in and foreign (Python) function symbols. """
	val:Any  # Fill in during WordDefiner pass
	
	def __init__(self, nom:Nom, alias:Optional[Literal]):
		super().__init__(nom)
		self.nom = nom
		self.alias = alias
	
	def span_of_native_name(self):
		return (self.alias or self.nom).head()

def FFI_Symbol(nom:Nom):
	return FFI_Alias(nom, None)

class FFI_Group:
	param_space: NS   # Will address the type parameters. Word-definer fills this.
	def __init__(self, symbols:list[FFI_Alias], type_params:Optional[Sequence[TypeParameter]], type_expr:SimpleType):
		self.symbols = symbols
		self.type_params = type_params or ()
		self.type_expr = type_expr

class ImportForeign:
	def __init__(self, source:Literal, linkage:Optional[Sequence[Reference]], groups:list[FFI_Group]):
		self.source = source
		self.linkage = linkage
		self.groups = groups

ImportDirective = Union[ImportModule, ImportForeign]

class Module:
	imports: list[ImportModule]
	foreign: list[ImportForeign]
	assumptions: list[Assumption]
	outer_functions: list[UserFunction]
	agent_definitions: list[UserAgent]
	op_overloads: list[OperatorOverload]
	
	source_path: Path  # Module loader fills this.
	all_functions: list[UserFunction]  # Resolver fills this.

	def __init__(self, exports:list, imports:list[ImportDirective], types:list[TypeDeclaration], assumptions:list[Assumption], top_levels:list, main:list):
		self.exports = exports
		self.imports = [i for i in imports if isinstance(i, ImportModule)]
		self.foreign = [i for i in imports if isinstance(i, ImportForeign)]
		self.types = types
		self.assumptions = assumptions
		self.outer_functions = []
		self.agent_definitions = []
		self.op_overloads = []
		self.all_functions = []
		for item in top_levels:
			if isinstance(item, UserFunction): self.outer_functions.append(item)
			elif isinstance(item, UserAgent): self.agent_definitions.append(item)
			elif isinstance(item, OperatorOverload): self.op_overloads.append(item)
			else: assert False, type(item)
		self.main = main
	
	@staticmethod
	def head(): return slice(0,0)
