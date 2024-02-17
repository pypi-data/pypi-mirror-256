"""
Sort of like an evaluator, but for types.
Replaces the old type-inference pass.

The idea here is to run the type-level program before running the value-level program.
If the type-level program computes a type, then the value-level program is certainly
well-typed with that type. Otherwise, the value-level program is at serious risk of
experiencing a type-error in practice.

This module represents one straightforward type-level execution mechanism.
The type side of things can be call-by-value, which is a bit easier I think.
The tricky bit is (mutually) recursive functions.
"""
from typing import Iterable, Sequence
from boozetools.support.foundation import Visitor
from .ontology import Symbol, SELF
from . import syntax, primitive, diagnostics
from .resolution import RoadMap, TopDown
from .stacking import RootFrame, Activation
from .syntax import ValExpr
from .calculus import (
	TYPE_ENV,
	SophieType, TypeVisitor, AdHocType,
	OpaqueType, ProductType, ArrowType, TypeVariable,
	RecordType, SumType, SubType, TaggedRecord, EnumType,
	UDFType, UDAType, InterfaceType, MessageType, UserTaskType,
	ParametricTemplateType, ConcreteTemplateType, BehaviorType,
	BOTTOM, ERROR, EMPTY_PRODUCT
)

class DependencyPass(TopDown):
	"""
	Solve the problem of which-all formal parameters does the value (and thus, type)
	of each user-defined function actually depend on. A simplistic answer would be to just
	use the parameters of the outermost function in a given nest. But inner functions
	might not be so generic as all that. Better precision here means smarter memoization,
	and thus faster type-checking.
	
	The nature of the algorithm is a transitive-closure / least-fixpoint operation.
	Preparation is by means of a tree-walk.
	
	To understand how this works (and why) start by reading the code for visit_PlainReference.
	In short, the `env` symbol is the type of the thing which depends,
	while the type of a formal-parameter is the thing upon which it depends.
	
	For behaviors, naively the final type is always "act", but that assumes no errors.
	It's still necessary to verify that the input types are compatible with the code and state.
	
	Incidentally:
	Related analysis could determine the deepest non-local needed for a function,
	which could possibly allow some functions to run at a shallower static-depth
	than however they may appear in the source code. This could make the simple evaluator
	a bit faster by improving the lifetime of thunks.
	"""

	def __init__(self):
		# The interesting result:
		self.depends: dict[Symbol, set[syntax.FormalParameter]] = {}
		
		# All manner of temp data, which should be cleaned afterward:
		self._outer: dict[Symbol, set[syntax.FormalParameter]] = {}
		self._parent: dict[Symbol, Symbol] = {}
		self._outflows: dict[Symbol, set[Symbol]] = {}
		self._overflowing = set()
		
	def visit_Module(self, module: syntax.Module):
		self._walk_children(module.outer_functions, None)
		self._walk_children(module.agent_definitions, None)
		for expr in module.main:
			self.visit(expr, None)
		self._flow_dependencies()
		self._clean_up_after()

	def _prepare(self, sym:Symbol, parent):
		self._parent[sym] = parent
		self.depends[sym] = set()
		self._outer[sym] = set()
		self._outflows[sym] = set()

	def _walk_children(self, children: Sequence[Symbol], parent):
		for child in children: self._prepare(child, parent)
		for child in children: self.visit(child, parent)

	def _insert(self, param:syntax.FormalParameter, env:Symbol):
		depends = self.depends[env]
		if self._is_in_scope(param, env) and param not in depends:
			depends.add(param)
			outer = self._outer[env]
			if self._is_non_local(param, env) and param not in outer:
				outer.add(param)
				self._overflowing.add(env)
	
	def _flow_dependencies(self):
		# This algorithm might not be theoretically perfect,
		# but for what it's about, it should be plenty fast.
		# And it's straightforward to understand.
		while self._overflowing:
			source = self._overflowing.pop()
			spill = self._outer[source]
			for destination in self._outflows[source]:
				for parameter in spill:
					self._insert(parameter, destination)
	
	def _clean_up_after(self):
		self._outer.clear()
		self._parent.clear()
		self._outflows.clear()
		self._overflowing.clear()

	def _is_in_scope(self, param:syntax.FormalParameter, env:Symbol):
		if env is None:
			return False
		if isinstance(env, (syntax.UserFunction, syntax.Behavior)):
			return param in env.params or self._is_in_scope(param, self._parent[env])
		if isinstance(env, syntax.Subject):
			return self._is_in_scope(param, self._parent[env])
		if isinstance(env, syntax.UserAgent):
			return param in env.fields or self._is_in_scope(param, self._parent[env])
		assert False, (param, env)

	@staticmethod
	def _is_non_local(param:syntax.FormalParameter, env:Symbol):
		if isinstance(env, (syntax.UserFunction, syntax.Behavior)):
			return param not in env.params
		if isinstance(env, syntax.Subject):
			return True
		assert False, type(env)

	def visit_UserFunction(self, udf: syntax.UserFunction, env):
		# Params refer to themselves in this arrangement.
		# The "breadcrumb" serves to indicate the nearest enclosing symbol.
		self._parent[udf] = env
		self._walk_children(udf.where, udf)
		self.visit(udf.expr, udf)
	
	def visit_Behavior(self, b:syntax.Behavior, env:syntax.UserAgent):
		self._parent[b] = env
		self.visit(b.expr, b)
	
	def visit_UserAgent(self, uda:syntax.UserAgent, env):
		assert env is None
		self._walk_children(uda.behaviors, uda)

	def visit_Lookup(self, lu: syntax.Lookup, env):
		self.visit(lu.ref, env)

	def _is_relevant(self, sym):
		return self._parent.get(sym) is not None

	def visit_PlainReference(self, ref: syntax.PlainReference, env:Symbol):
		dfn = ref.dfn
		if isinstance(dfn, syntax.FormalParameter):
			self._insert(dfn, env)
		elif self._is_relevant(dfn):
			self._outflows[dfn].add(env)
	
	def visit_AssignField(self, af:syntax.AssignField, env:Symbol):
		dfn = af.dfn
		assert isinstance(dfn, syntax.FormalParameter)
		self._insert(dfn, env)
		self.visit(af.expr, env)
	
	def visit_QualifiedReference(self, ref:syntax.QualifiedReference, env:Symbol):
		pass

	def visit_MatchExpr(self, mx: syntax.MatchExpr, env:Symbol):
		self._prepare(mx.subject, env)
		self._outflows[mx.subject].add(env)
		self.visit(mx.subject.expr, env)
		for alt in mx.alternatives:
			self._walk_children(alt.where, mx.subject)
			self.visit(alt.sub_expr, mx.subject)
		if mx.otherwise is not None:
			self.visit(mx.otherwise, mx.subject)

	def visit_DoBlock(self, db: syntax.DoBlock, env:Symbol):
		for new_agent in db.agents:
			self._parent[new_agent] = env
			self.visit(new_agent.expr, env)
		for s in db.steps:
			self.visit(s, env)


class ArityError(Exception):
	pass

_literal_type_map : dict[type, OpaqueType] = {
	bool: primitive.literal_flag,
	str: primitive.literal_string,
	int: primitive.literal_number,
	float: primitive.literal_number,
}

BINARY_TYPES = {}
UNARY_TYPES = {}

def _arrow_of(typ: SophieType, arity: int) -> ArrowType:
	assert arity > 0
	product = ProductType((typ,) * arity).exemplar()
	return ArrowType(product, typ).exemplar()

logical_shortcut = _arrow_of(primitive.literal_flag, 2)

def _init():
	def relop_type(case):
		pair = ProductType((case, case)).exemplar()
		return ArrowType(pair, primitive.literal_flag).exemplar()
	
	math_op = _arrow_of(primitive.literal_number, 2)
	
	for op in '^ * / DIV MOD + -'.split():
		BINARY_TYPES[op] = AdHocType(op, 2)
		BINARY_TYPES[op].cases.append(math_op)
	
	numeric = relop_type(primitive.literal_number)
	stringy = relop_type(primitive.literal_string)
	flagged = relop_type(primitive.literal_flag)
	
	def eq(op):
		rel(op)
		BINARY_TYPES[op].cases.append(flagged)
	
	def rel(op):
		BINARY_TYPES[op] = AdHocType(op, 2)
		BINARY_TYPES[op].cases.append(numeric)
		BINARY_TYPES[op].cases.append(stringy)
	
	eq("==")
	eq("!=")
	rel("<=")
	rel("<")
	rel(">=")
	rel(">")
	
	UNARY_TYPES['-'] = AdHocType("-", 1)
	UNARY_TYPES["-"].cases.append(_arrow_of(primitive.literal_number, 1))
	UNARY_TYPES["NOT"] = _arrow_of(primitive.literal_flag, 1)

_init()

class ManifestBuilder(Visitor):
	"""Converts the syntax of manifest types into corresponding type-calculus objects."""
	_bind : dict[syntax.TypeParameter:SophieType]
	
	def __init__(self, tps: Sequence[syntax.TypeParameter], type_args: list[SophieType]):
		self._bind = dict(zip(tps, type_args))
		
	def _make_product(self, formals:Iterable[syntax.ARGUMENT_TYPE]) -> ProductType:
		return ProductType(map(self.visit, formals)).exemplar()
		
	def visit_RecordSpec(self, rs:syntax.RecordSpec) -> ProductType:
		# This is sort of a handy special case: Things use it to build constructor arrows.
		return self._make_product(field.type_expr for field in rs.fields)
	
	def visit_TypeCall(self, tc:syntax.TypeCall) -> SophieType:
		dfn = tc.ref.dfn
		if isinstance(dfn, syntax.TypeParameter):
			return self._bind[dfn]
		if isinstance(dfn, syntax.Opaque):
			return OpaqueType(dfn).exemplar()
		args = [self.visit(a) for a in tc.arguments]
		if isinstance(dfn, syntax.Record):
			return RecordType(dfn, args).exemplar()
		if isinstance(dfn, syntax.Variant):
			return SumType(dfn, args).exemplar()
		if isinstance(dfn, syntax.TypeAlias):
			return ManifestBuilder(dfn.type_params, args).visit(dfn.body)
		if isinstance(dfn, syntax.Interface):
			return InterfaceType(dfn, args).exemplar()
		raise NotImplementedError(type(dfn))
	
	def visit_ArrowSpec(self, spec:syntax.ArrowSpec):
		return ArrowType(self._make_product(spec.lhs), self.visit(spec.rhs))
	
	def visit_MessageSpec(self, ms:syntax.MessageSpec) -> SophieType:
		if ms.type_exprs:
			product = self._make_product(ms.type_exprs)
			return MessageType(product).exemplar()
		else:
			return primitive.literal_msg
		
	def make_agent_template(self, uda:syntax.UserAgent, module_scope:TYPE_ENV):
		if uda.fields:
			product = self._make_product(field.type_expr for field in uda.fields)
			return ParametricTemplateType(uda, product, module_scope)
		else:
			# In this case, we have a (stateless) template ready to go.
			return ConcreteTemplateType(uda, EMPTY_PRODUCT, module_scope)

class Rewriter(TypeVisitor):
	def __init__(self, gamma:dict):
		self._gamma = gamma
	def on_opaque(self, o: OpaqueType):
		return o
	def on_tag_record(self, t: TaggedRecord):
		return TaggedRecord(t.st, [a.visit(self) for a in t.type_args])
	def on_record(self, r: RecordType):
		return RecordType(r.symbol, [a.visit(self) for a in r.type_args])
	def on_variable(self, v: TypeVariable):
		return self._gamma.get(v, BOTTOM)
	def on_sum(self, s:SumType):
		return SumType(s.variant, [a.visit(self) for a in s.type_args])
	def on_arrow(self, a: ArrowType):
		return ArrowType(a.arg.visit(self), a.res.visit(self))
	def on_product(self, p: ProductType):
		return ProductType([f.visit(self) for f in p.fields])
	def on_message(self, m: MessageType):
		return MessageType(m.arg.visit(self))

class Binder(Visitor):
	"""
	Discovers (or fails) a substitution-of-variables (in the formal)
	which makes the formal accept the actual as an instance.
	"""
	def __init__(self, engine:"DeductionEngine", env:TYPE_ENV):
		self.gamma = {}
		self.ok = True
		self._engine = engine
		self._dynamic_link = env
		self._task = None
		self.why = None
		
	def fail(self, why:str):
		self.ok = False
		self.why = why
	
	def inputs(self, formal_types, actual_types, args):
		for expr, need, got in zip(args, formal_types, actual_types):
			if self.ok:
				self.bind_param(expr, need, got)
		return self
	
	def bind_param(self, expr, need, got):
		self._task = expr, need, got
		self.bind(need, got)
	
	def complain(self, report:diagnostics.Report):
		report.bad_type(self._dynamic_link, *self._task, self.why)
				
	def bind(self, formal: SophieType, actual: SophieType):
		if actual in (BOTTOM, ERROR) or formal.number == actual.number:
			return
		else:
			self.visit(formal, actual)
	
	def visit_TypeVariable(self, formal: TypeVariable, actual: SophieType):
		if formal in self.gamma:
			union_finder = UnionFinder()
			result = union_finder.do(self.gamma[formal], actual)
			if result is ERROR:
				self.fail("Unable to unify %s with %s"%(self.gamma[formal], actual))
			else:
				self.gamma[formal] = result
		else:
			self.gamma[formal] = actual
	
	def parallel(self, formal: Sequence[SophieType], actual: Sequence[SophieType]):
		assert len(formal) == len(actual)
		for f, a in zip(formal, actual): self.bind(f, a)
	
	def visit_ProductType(self, formal: ProductType, actual: SophieType):
		if not isinstance(actual, ProductType):
			return self.fail("%s has not the product nature."%actual)
		if len(formal.fields) != len(actual.fields):
			return self.fail("%s and %s have not the same arity."%(formal, actual))
		self.parallel(formal.fields, actual.fields)
		
	def visit_ArrowType(self, formal: ArrowType, actual: SophieType):
		if isinstance(actual, ArrowType):
			# Use a nested type-environment to bind the arguments "backwards":
			# The argument to the formal-function must be acceptable to the actual-function.
			# The actual-function does its work on that set of bindings.
			save_gamma = self.gamma
			self.gamma = dict(save_gamma)  # Generally fairly small, so asymptotic is NBD here.
			self.bind(actual.arg, formal.arg)
			# The actual-result could contain type-variables from the formal side,
			# and these must be suitable as what the formal-result dictates.
			result = actual.res.visit(Rewriter(self.gamma))
			self.gamma = save_gamma
			self.bind(formal.res, result)
		elif isinstance(actual, UDFType):
			if actual.expected_arity() != len(formal.arg.fields):
				self.fail("Arity mismatch between formal function and user-defined function.")
			else:
				result = self._engine.apply_UDF(actual, formal.arg.fields, self._dynamic_link)
				self.bind(formal.res, result)
		else:
			self.fail("Using a %s where some sort of function is needed."%actual)
	
	def visit_OpaqueType(self, formal: OpaqueType, actual: SophieType):
		self.fail("Opaque type %s is not %s"%(formal, actual))
	
	def visit_SumType(self, formal: SumType, actual: SophieType):
		if isinstance(actual, SumType):
			if formal.variant is actual.variant:
				self.parallel(formal.type_args, actual.type_args)
			else:
				self.fail("Variant %s is not variant %s"%(formal.variant, actual.variant))
		elif isinstance(actual, TaggedRecord):
			if formal.variant is actual.st.variant:
				self.parallel(formal.type_args, actual.type_args)
			else:
				self.fail("Variant %s is not variant %s"%(formal.variant, actual.st.variant))
		elif isinstance(actual, EnumType):
			if formal.variant is actual.st.variant:
				pass
			else:
				self.fail("Variant %s is not variant %s"%(formal.variant, actual.st.variant))
		else:
			self.fail("%s is a variant, but %s is not a subtype of any variant."%(formal, actual))
	
	def visit_RecordType(self, formal: RecordType, actual: SophieType):
		if isinstance(actual, RecordType) and formal.symbol is actual.symbol:
			self.parallel(formal.type_args, actual.type_args)
		else:
			self.fail("Record %s is not %s"%(formal, actual))
	
	def visit_MessageType(self, formal: MessageType, actual: SophieType):
		if isinstance(actual, MessageType):
			return self.visit(formal.arg, actual.arg)
		elif isinstance(actual, UserTaskType):
			if actual.expected_arity() == len(formal.arg.fields):
				result = self._engine.apply_UDF(actual.udf_type, formal.arg.fields, self._dynamic_link)
				# At this point, either an act or another message will be acceptable.
				if not _quacks_like_an_action(result):
					self.fail("%s does not an action make."%result)
			else:
				self.fail("%s has different arity from %s"%(formal, actual))
		elif isinstance(actual, BehaviorType):
			if actual.expected_arity() == len(formal.arg.fields):
				result = self._engine.apply_behavior(actual, formal.arg.fields, self._dynamic_link)
				# At this point, either an act or another message will be acceptable.
				if not _quacks_like_an_action(result):
					self.fail("%s does not an action make."%result)
			else:
				self.fail("%s has different arity from %s"%(formal, actual))
		else:
			self.fail("Not sure how to use a %s as a %s"%(actual, formal))

def _quacks_like_an_action(result:SophieType) -> bool:
	assert isinstance(result, SophieType), result
	# Let ERROR quack to stop cascades of messages.
	return result in (primitive.literal_act, primitive.literal_msg, ERROR)

class UnionFinder(Visitor):
	def __init__(self):
		self._prototype = BOTTOM
		self._expr = None
	
	def result(self):
		return self._prototype
	
	def unify_with(self, env, expr, typ:SophieType, report:diagnostics.Report):
		if ERROR not in (self._prototype, typ):
			union = self.do(self._prototype, typ)
			if union is ERROR:
				report.type_mismatch(env, self._expr, self._prototype, expr, typ)
			else:
				self._prototype = union
				self._expr = expr
				return True
	
	def parallel(self, these:Sequence[SophieType], those:Sequence[SophieType]):
		assert len(these) == len(those)
		return [self.do(a, b) for a,b in zip(these, those)]
	
	def do(self, this: SophieType, that: SophieType):
		if this.number == that.number or that is BOTTOM: return this
		elif that is ERROR: return that
		else:
			typ = self.visit(this, that)
			if typ is None:
				return ERROR
			else:
				return typ

	@staticmethod
	def visit__Bottom(_, that: SophieType):
		return that
		
	@staticmethod
	def visit_OpaqueType(_, __):
		return None
		
	def visit_RecordType(self, this: RecordType, that: SophieType):
		if isinstance(that, RecordType) and this.symbol is that.symbol:
			return RecordType(this.symbol, self.parallel(this.type_args, that.type_args))
	
	def visit_SumType(self, this: SumType, that: SophieType):
		if isinstance(that, SumType):
			if this.variant is that.variant:
				type_args = self.parallel(this.type_args, that.type_args)
				return SumType(this.variant, type_args)
		elif isinstance(that, TaggedRecord):
			if this.variant is that.st.variant:
				type_args = self.parallel(this.type_args, that.type_args)
				return SumType(this.variant, type_args)
		elif isinstance(that, EnumType):
			if this.variant is that.st.variant:
				return this
			
	def visit_TaggedRecord(self, this: TaggedRecord, that: SophieType):
		if isinstance(that, TaggedRecord):
			if this.st is that.st:
				type_args = self.parallel(this.type_args, that.type_args)
				return TaggedRecord(this.st, type_args)
			if this.st.variant is that.st.variant:
				type_args = self.parallel(this.type_args, that.type_args)
				return SumType(this.st.variant, type_args)
		elif isinstance(that, EnumType):
			if this.st.variant is that.st.variant:
				return SumType(this.st.variant, this.type_args)
		elif isinstance(that, SumType):
			return self.visit_SumType(that, this)
		
	def visit_EnumType(self, this: EnumType, that: SophieType):
		if isinstance(that, SumType):
			return self.visit_SumType(that, this)
		elif isinstance(that, TaggedRecord):
			return self.visit_TaggedRecord(that, this)
		elif isinstance(that, EnumType):
			if this.st.variant is that.st.variant:
				type_args = tuple(BOTTOM for _ in this.st.variant.type_params)
				return SumType(this.st.variant, type_args)

	def visit_UDFType(self, this:UDFType, that: SophieType):
		if isinstance(that, UDFType):
			if len(this.fn.params) == len(that.fn.params):
				# In principle, we take the intersection of the parameters to the union of the results.
				# In practice, that means some sort of "try both" logic,
				# and it's entirely too complicated for a five-minute hack session.
				raise NotImplementedError("To do.")
			else:
				return None  # Non-matching arity is a definite error.
		elif isinstance(that, ArrowType):
			# If trying to unify with arrow-type, then the arrow-type itself may be a suitable unifier.
			# Try the arrow-type as a binder, and if it works, then it's a win.
			raise NotImplementedError("To do.")
		else:
			return None  # Not a function.
	
	@staticmethod
	def visit__Error(this: ERROR, that: SophieType):
		return this

class Checker(Visitor):
	"""
	Responsible for checking type assertions/annotations.
	Compares syntax to SophieType objects.
	I don't need this too powerful,
	because the DeductionEngine does the hard stuff.
	This is just a layer to try to see where to blame for a typing failure.
	"""
	def __init__(self, types):
		self._types = types
		self._gamma : dict[Symbol,SophieType] = {}
		self.sick = False
	
	def _need(self, assertion):
		if not assertion:
			self.sick = True
	
	def bind(self, formal, actual:SophieType):
		if actual in [BOTTOM, ERROR]: return
		self.visit(formal, actual)
	
	def visit_FormalParameter(self, fp:syntax.FormalParameter, actual:SophieType):
		if fp.type_expr:
			self.bind(fp.type_expr, actual)
	
	def visit_ExplicitTypeVariable(self, etv:syntax.ExplicitTypeVariable, actual:SophieType):
		sym = etv.dfn
		if sym in self._gamma:
			self._need(self._gamma[sym] == actual)
		else:
			self._gamma[sym] = actual
	
	def visit_TypeCall(self, tc:syntax.TypeCall, actual:SophieType):
		formal = tc.ref.dfn
		if isinstance(formal, syntax.Opaque):
			self._need(isinstance(actual, OpaqueType) and actual.symbol is formal)
		elif isinstance(formal, syntax.Variant):
			if isinstance(actual, SumType):
				self._need(actual.variant is formal)
			elif isinstance(actual, SubType):
				self._need(actual.st.variant is formal)
			else:
				self._need(False)
		elif isinstance(formal, syntax.Record):
			self._need(isinstance(actual, RecordType) and actual.symbol is formal)
		else:
			print(type(formal), formal, actual)
			self._need(False)
	
	def visit_ArrowSpec(self, spec:syntax.ArrowSpec, actual:SophieType):
		arity = len(spec.lhs)
		self._need(arity == actual.expected_arity())
		if isinstance(actual, ArrowType):
			for f,a in zip(spec.lhs, actual.arg.fields):
				self.bind(f,a)
		elif isinstance(actual, UDFType):
			# Not worth wrestling with right now.
			pass
		else:
			self._need(False)

class DeductionEngine(Visitor):
	def __init__(self, roadmap:RoadMap, report:diagnostics.Report):
		# self._trace_depth = 0
		self._report = report  # .on_error("Checking Types")
		self._types = { ot.symbol: ot for ot in _literal_type_map.values() }
		self._types[primitive.literal_act.symbol]  = primitive.literal_act
		self._constructors : dict[syntax.Symbol, SophieType] = {}
		self._ffi : dict[syntax.FFI_Alias, SophieType] = {}
		self._memo = {}
		self._recursion = {}
		self._deps_pass = DependencyPass()
		self._list_symbol = roadmap.list_symbol
		self._udf = {}
		self._root = RootFrame()
		self.visit_Module(roadmap.preamble)
		for module in roadmap.each_module:
			self.visit_Module(module)
	
	def visit_Module(self, module:syntax.Module):
		self._report.info("Type-Check", module.source_path)
		self._deps_pass.visit_Module(module)
		for td in module.types: self.visit(td)
		for fi in module.foreign: self.visit(fi)
		local = Activation.for_module(self._root, module)
		builder = ManifestBuilder([], [])
		for uda in module.agent_definitions:
			self._constructors[uda] = builder.make_agent_template(uda, local)
		for expr in module.main:
			self._report.trace(" -->", expr)
			result = self.visit(expr, local)
			self._report.info(result)
		self._root._bindings.update(local._bindings)

	###############################################################################

	def visit_Record(self, r: syntax.Record):
		type_args = [TypeVariable() for _ in r.type_params]
		self._types[r] = RecordType(r, type_args)
		arg = ManifestBuilder(r.type_params, type_args).visit(r.spec)
		self._constructors[r] = ArrowType(arg, self._types[r])
	
	def visit_Variant(self, v: syntax.Variant):
		type_args = [TypeVariable() for _ in v.type_params]
		self._types[v] = SumType(v, type_args)
		builder = ManifestBuilder(v.type_params, type_args)
		for st in v.subtypes:
			if st.body is None:
				self._constructors[st] = EnumType(st)
			elif isinstance(st.body, syntax.RecordSpec):
				arg = builder.visit(st.body)
				res = TaggedRecord(st, type_args)
				self._constructors[st] = ArrowType(arg, res)
				
	def visit_TypeAlias(self, a: syntax.TypeAlias):
		type_args = [TypeVariable() for _ in a.type_params]
		self._types[a] = it = ManifestBuilder(a.type_params, type_args).visit(a.body)
		if isinstance(it, RecordType):
			formals = self._types[it.symbol].type_args
			original = self._constructors[it.symbol]
			gamma = dict(zip(formals, it.type_args))
			self._constructors[a] = original.visit(Rewriter(gamma))
	
	def visit_Opaque(self, td:syntax.Opaque):
		self._types[td] = OpaqueType(td)
	
	def visit_Interface(self, i:syntax.Interface):
		type_args = [TypeVariable() for _ in i.type_params]
		self._types[i] = InterfaceType(i, type_args)
	
	###############################################################################

	def visit_ImportForeign(self, d:syntax.ImportForeign):
		for group in d.groups:
			type_args = [TypeVariable() for _ in group.type_params]
			typ = ManifestBuilder(group.type_params, type_args).visit(group.type_expr)
			for sym in group.symbols:
				self._ffi[sym] = typ

	###############################################################################

	@staticmethod
	def visit_Literal(expr: syntax.Literal, env:TYPE_ENV) -> SophieType:
		return _literal_type_map[type(expr.value)]
	
	def apply_UDF(self, fn_type: UDFType, arg_types: Sequence[SophieType], env:TYPE_ENV) -> SophieType:
		# Question: Do the type-preconditions hold?
		checker = Checker(self._types)
		fn = fn_type.fn
		inner = Activation.for_function(fn_type.static_link, env, fn_type.fn, arg_types)
		for param, actual in zip(fn.params, arg_types):
			checker.bind(param, actual)
			if checker.sick:
				self._report.bad_argument(inner, param, actual, checker)
				return ERROR
		result_type = self.exec_UDF(fn, inner)
		if result_type is ERROR: return ERROR
		if fn.result_type_expr:
			checker.bind(fn.result_type_expr, result_type)
			if checker.sick:
				self._report.bad_result(inner, fn_type.fn, result_type, checker)
				return ERROR
		return result_type
	
	def apply_behavior(self, bt:BehaviorType, arg_types: Sequence[SophieType], env:TYPE_ENV) -> SophieType:
		env = Activation.for_behavior(bt.uda_type.frame, env, bt.behavior, arg_types)
		memo_key = self._memo_key(bt.behavior, env)
		if memo_key in self._memo:
			return self._memo[memo_key]
		elif memo_key in self._recursion:
			return primitive.literal_msg
		else:
			self._recursion[memo_key] = False
			got = self._memo[memo_key] = self.visit(bt.behavior.expr, env)
			self._recursion.pop(memo_key)
			if _quacks_like_an_action(got):
				return primitive.literal_act
			else:
				self._report.does_not_express_behavior(env, bt.behavior, got)
				return ERROR
	
	def _memo_key(self, symbol:Symbol, env:TYPE_ENV):
		# This definitely works for functions.
		# Things are a bit more sketchy on the behavior side.
		memo_symbols = self._deps_pass.depends[symbol]
		assert all(isinstance(s, syntax.FormalParameter) for s in memo_symbols)
		memo_types = tuple(
			env.chase(p).fetch(p)  # .number
			for p in memo_symbols
		)
		return symbol, memo_types
	
	def exec_UDF(self, fn:syntax.UserFunction, env:TYPE_ENV):
		# The part where memoization must happen.
		memo_key = self._memo_key(fn, env)
		if memo_key in self._memo:
			return self._memo[memo_key]
		elif memo_key in self._recursion:
			self._recursion[memo_key] = True
			# self._report.trace(">Recursive:", fn, dict(zip((s.nom.text for s in memo_symbols), memo_types)))
			return BOTTOM
		else:
			# TODO: Pass around judgements, not just types.
			self._recursion[memo_key] = False
			self._memo[memo_key] = self.visit(fn.expr, env)
			if self._recursion.pop(memo_key):
				prior = BOTTOM
				while prior != self._memo[memo_key]:
					prior = self._memo[memo_key]
					self._memo[memo_key] = self.visit(fn.expr, env)
				if prior is BOTTOM:
					self._report.ill_founded_function(env, fn)
				# self._report.trace("<Resolved:", fn)
					
		return self._memo[memo_key]
	
	def _call_site(self, site: syntax.ValExpr, callee_type, args:Sequence[ValExpr], env:TYPE_ENV) -> SophieType:
		actual_types = [self.visit(a, env) for a in args]
		if ERROR in actual_types:
			return ERROR
		
		env.pc = site
		if callee_type.expected_arity() != len(args):
			self._report.wrong_arity(env, site, callee_type.expected_arity(), args)
			return ERROR
		
		if isinstance(callee_type, AdHocType):
			return self._call_dynamic(callee_type, actual_types, args, env)
		else:
			return self._call_static(callee_type, actual_types, args, env)
		
	def _call_dynamic(self, ad_hoc:AdHocType, actual_types, args:Sequence[ValExpr], env:TYPE_ENV):
		for candidate in ad_hoc.cases:
			binder = Binder(self, env).inputs(candidate.arg.fields, actual_types, args)
			if binder.ok:
				return candidate.res.visit(Rewriter(binder.gamma))
		self._report.no_applicable_method(env, actual_types)
		return ERROR
		
	def _call_static(self, callee_type, actual_types, args:Sequence[ValExpr], env:TYPE_ENV):
		
		assert not isinstance(callee_type, AdHocType)
		
		if isinstance(callee_type, ArrowType):
			binder = Binder(self, env).inputs(callee_type.arg.fields, actual_types, args)
			if binder.ok:
				return callee_type.res.visit(Rewriter(binder.gamma))
			else:
				binder.complain(self._report)
				return ERROR
		
		elif isinstance(callee_type, UDFType):
			return self.apply_UDF(callee_type, actual_types, env)
		
		elif isinstance(callee_type, ParametricTemplateType):
			binder = Binder(self, env).inputs(callee_type.args.fields, actual_types, args)
			if binder.ok:
				return ConcreteTemplateType(callee_type.uda, ProductType(actual_types), callee_type.frame)
			else:
				binder.complain(self._report)
				return ERROR
		
		else:
			raise NotImplementedError(type(callee_type))
	
	def visit_Call(self, site: syntax.Call, env: TYPE_ENV) -> SophieType:
		fn_type = self.visit(site.fn_exp, env)
		if fn_type is ERROR: return ERROR
		return self._call_site(site, fn_type, site.args, env)
	
	def visit_BinExp(self, expr:syntax.BinExp, env:TYPE_ENV) -> SophieType:
		return self._call_site(expr, BINARY_TYPES[expr.op.text], (expr.lhs, expr.rhs), env)
	
	def visit_ShortCutExp(self, expr:syntax.ShortCutExp, env:TYPE_ENV) -> SophieType:
		return self._call_site(expr, logical_shortcut, (expr.lhs, expr.rhs), env)
	
	def visit_UnaryExp(self, expr: syntax.UnaryExp, env:TYPE_ENV) -> SophieType:
		return self._call_site(expr, UNARY_TYPES[expr.op.text], (expr.arg,), env)
		
	def visit_Lookup(self, lu:syntax.Lookup, env:TYPE_ENV) -> SophieType:
		target = lu.ref.dfn
		if isinstance(target, (syntax.TypeDeclaration, syntax.SubTypeSpec, syntax.UserAgent)):
			return self._constructors[target]  # Must succeed because of resolution.check_constructors
		if isinstance(target, syntax.FFI_Alias):
			return self._ffi[target]
		
		static_env = env.chase(target)
		if isinstance(target, syntax.UserFunction):
			if target.params:
				return UDFType(target, static_env).exemplar()
			else:
				inner = Activation.for_function(static_env, env, target, ())
				return self.exec_UDF(target, inner)
		else:
			assert target is SELF or isinstance(target, (syntax.FormalParameter, syntax.Subject, syntax.NewAgent)), type(target)
			return static_env.fetch(target)
	
	@staticmethod
	def visit_Absurdity(_:syntax.Absurdity, env:TYPE_ENV) -> SophieType:
		return BOTTOM
	
	def visit_ExplicitList(self, el:syntax.ExplicitList, env:TYPE_ENV) -> SumType:
		# Since there's guaranteed to be at least one value,
		# we should be able to glean a concrete type from it.
		# Having that, we should be able to get a union over them all.
		union_find = UnionFinder()
		for e in el.elts:
			if not union_find.unify_with(env, e, self.visit(e, env), self._report):
				return ERROR
		element_type = union_find.result()
		return SumType(self._list_symbol, (element_type,))

	def visit_Cond(self, cond:syntax.Cond, env:TYPE_ENV) -> SophieType:
		if_part_type = self.visit(cond.if_part, env)
		if if_part_type is ERROR: return ERROR
		if if_part_type != primitive.literal_flag:
			self._report.bad_type(env, cond.if_part, primitive.literal_flag, if_part_type, "There is no implicit Boolean conversion.")
			return ERROR
		uf = UnionFinder()
		uf.unify_with(env, cond.then_part, self.visit(cond.then_part, env), self._report)
		uf.unify_with(env, cond.else_part, self.visit(cond.else_part, env), self._report)
		return uf.result()
	
	def visit_MatchExpr(self, mx:syntax.MatchExpr, env:TYPE_ENV) -> SophieType:
		
		def try_one_alternative(alt, subtype:SubType) -> SophieType:
			inner = Activation.for_subject(env, mx.subject)
			inner.assign(mx.subject, subtype)
			for subfn in alt.where:
				inner.declare(subfn)
			return self.visit(alt.sub_expr, inner)
		
		def try_otherwise():
			inner = Activation.for_subject(env, mx.subject)
			inner.assign(mx.subject, subject_type)
			return self.visit(mx.otherwise, inner)
		
		def try_everything(type_args:Sequence[SophieType]):
			uf = UnionFinder()
			for alt in mx.alternatives:
				subtype_symbol = mx.namespace[alt.nom.key()]
				subtype = _hypothesis(subtype_symbol, type_args).exemplar()
				case_result = try_one_alternative(alt, subtype)
				if not uf.unify_with(env, alt.sub_expr, case_result, self._report):
					return ERROR
			if mx.otherwise is not None:
				if not uf.unify_with(env, mx.otherwise, try_otherwise(), self._report):
					return ERROR
			return uf.result()

		subject_type = self.visit(mx.subject.expr, env)
		if subject_type is ERROR:
			return ERROR

		if isinstance(subject_type, SumType):
			return try_everything(subject_type.type_args)
		
		elif subject_type is BOTTOM:
			return try_everything([BOTTOM] * len(mx.variant.type_params))
		
		elif isinstance(subject_type, SubType) and subject_type.st.variant is mx.variant:
			case_key = subject_type.st.nom.text
			if case_key in mx.dispatch:
				return try_one_alternative(mx.dispatch[case_key], subject_type)
			else:
				return try_otherwise()
		
		else:
			self._report.bad_type(env, mx.subject.expr, mx.variant, subject_type, "Square Peg; Round Hole.")
			return ERROR

	def visit_AssignField(self, af:syntax.AssignField, env:TYPE_ENV) -> SophieType:
		field_type = env.chase(af.dfn).fetch(af.dfn)
		expr_type = self.visit(af.expr, env)
		if expr_type == field_type or expr_type is ERROR:
			return primitive.literal_act
		else:
			self._report.bad_type(env, af.expr, field_type, expr_type, "Assignment must match field type exactly.")
			return ERROR
	
	def visit_FieldReference(self, fr:syntax.FieldReference, env:TYPE_ENV) -> SophieType:
		lhs_type = self.visit(fr.lhs, env)
		if isinstance(lhs_type, UDAType):
			if _is_a_self_reference(fr.lhs):
				try: symbol = lhs_type.uda.field_space[fr.field_name.key()]
				except KeyError:
					self._report.record_lacks_field(env, fr, lhs_type)
					return ERROR
				else:
					return lhs_type.frame.fetch(symbol)
			else:
				self._report.no_telepathy_allowed(env, fr, lhs_type)
				return ERROR
		elif isinstance(lhs_type, RecordType):
			spec = lhs_type.symbol.spec
			parameters = lhs_type.symbol.type_params
		elif isinstance(lhs_type, TaggedRecord):
			spec = lhs_type.st.body
			parameters = lhs_type.st.variant.type_params
		elif lhs_type is BOTTOM:
			# In principle the evaluator could make an observation / infer a constraint
			return lhs_type
		elif lhs_type is ERROR:
			# Complaint has already been issued.
			return lhs_type
		else:
			self._report.type_has_no_fields(env, fr, lhs_type)
			return ERROR
		try:
			field_spec = spec.field_space[fr.field_name.text]
		except KeyError:
			self._report.record_lacks_field(env, fr, lhs_type)
			return ERROR
		assert isinstance(field_spec, syntax.FormalParameter), field_spec
		return ManifestBuilder(parameters, lhs_type.type_args).visit(field_spec.type_expr)

	def visit_BindMethod(self, mr:syntax.BindMethod, env:TYPE_ENV) -> SophieType:
		lhs_type = self.visit(mr.receiver, env)
		if lhs_type is ERROR: return ERROR
		if isinstance(lhs_type, InterfaceType):
			try:
				ms = lhs_type.symbol.method_space[mr.method_name.key()]
			except KeyError:
				self._report.bad_message(env, mr, lhs_type)
				return ERROR
			else:
				assert isinstance(ms, syntax.MethodSpec)
				parameters = lhs_type.symbol.type_params
				builder = ManifestBuilder(parameters, lhs_type.type_args)
				if ms.type_exprs:
					args = ProductType(builder.visit(tx) for tx in ms.type_exprs)
					return ArrowType(args, primitive.literal_msg)
				else:
					return primitive.literal_act
		elif isinstance(lhs_type, UDAType):
			try:
				behavior = lhs_type.uda.message_space[mr.method_name.key()]
			except KeyError:
				self._report.bad_message(env, mr, lhs_type)
				return ERROR
			else:
				assert isinstance(behavior, syntax.Behavior)
				result = BehaviorType(lhs_type, behavior).exemplar()
				if behavior.params:
					return result
				else:
					return self.apply_behavior(result, (), env)
		else:
			self._report.bad_message(env, mr, lhs_type)
			return ERROR
	
	def visit_DoBlock(self, do:syntax.DoBlock, env:TYPE_ENV) -> SophieType:
		# A bit verbose to pick up all errors, not just the first.
		answer = primitive.literal_act
		# 1. Make a scope to contain new-agents:
		inner = Activation.for_do_block(env)
		for na in do.agents:
			assert isinstance(na, syntax.NewAgent)
			tt = self.visit(na.expr, env)
			if isinstance(tt, ConcreteTemplateType):
				frame = Activation(tt.frame, inner, tt.uda)
				agent_type = UDAType(tt.uda, tt.args, frame)
				frame.assign(SELF, agent_type)
				for f, t in zip(tt.uda.fields, tt.args.fields):
					frame.assign(f, t)
			else:
				self._report.bad_type(env, na.expr, "Agent Template", tt, "Casting call will repeat next Thursday.")
				agent_type = ERROR
				answer = ERROR
			inner.assign(na, agent_type)
		# 2. Judge types of step in the new scope:
		for step in do.steps:
			inner.pc = step
			step_type = self.visit(step, inner)
			assert isinstance(step_type, SophieType)
			if step_type is ERROR: answer = ERROR
			elif step_type is BOTTOM:
				if answer is not ERROR:
					answer = BOTTOM
			elif not _quacks_like_an_action(step_type):
				self._report.bad_type(inner, step, primitive.literal_act, step_type, "Only actions can be steps in a process.")
				answer = ERROR
		return answer

	@staticmethod
	def visit_Skip(s:syntax.Skip, env:TYPE_ENV) -> SophieType:
		return primitive.literal_act

	def visit_AsTask(self, at:syntax.AsTask, env:TYPE_ENV) -> SophieType:
		def is_act(t): return t.number == primitive.literal_act.number
		inner = self.visit(at.sub, env)
		if is_act(inner):
			return primitive.literal_msg
		elif isinstance(inner, ArrowType) and is_act(inner.res):
			return MessageType(inner.arg).exemplar()
		elif isinstance(inner, UDFType):
			return UserTaskType(inner).exemplar()
		else:
			self._report.bad_type(env, at.sub, "procedure", inner, "Concurrent tasks cannot return a value.")
			return ERROR

def _hypothesis(st:Symbol, type_args:Sequence[SophieType]) -> SubType:
	assert isinstance(st, syntax.SubTypeSpec)
	body = st.body
	if body is None:
		return EnumType(st)
	if isinstance(body, syntax.RecordSpec):
		return TaggedRecord(st, type_args)

def _is_a_self_reference(expr:ValExpr) -> bool:
	return isinstance(expr, syntax.Lookup) and expr.ref.dfn is SELF
