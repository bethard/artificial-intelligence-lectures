// This is far from efficient. But at least it verifies the calculations in the book.

class Variable[VAL](val symbol: Symbol, val values: List[VAL]) {
  override def toString: String = this.symbol.toString
}
object Variable {
  def assignments[VAL](variables: List[Variable[VAL]]): List[Map[Variable[VAL], VAL]] = {
    variables match {
      case Nil => List(Map.empty)
      case variable :: Nil =>
        for (value <- variable.values) yield Map(variable -> value)
      case variable :: rest =>
        Variable.assignments(rest).map{
          assignment => variable.values.map{
            value => Map(variable -> value) ++ assignment
          }
        }.flatten
    }
  }
}

case class Factor[VAL](
  variables: List[Variable[VAL]],
  assignmentScores: Map[Map[Variable[VAL], VAL], Double]) {

  def * (that: Factor[VAL]): Factor[VAL] = {
    val variables = (this.variables ++ that.variables).distinct
    val assignmentScores = for (assignment <- Variable.assignments(variables)) yield {
      val thisAssignment = assignment.filterKeys(this.variables.contains)
      val thatAssignment = assignment.filterKeys(that.variables.contains)
      val thisScore = this.assignmentScores(thisAssignment)
      val thatScore = that.assignmentScores(thatAssignment)
      assignment -> thisScore * thatScore
    }
    Factor(variables, assignmentScores.toMap)
  }

  def - (variable: Variable[VAL]): Factor[VAL] = {
    val variables = this.variables.filter(_ != variable)
    val assignmentScores = for (assignment <- Variable.assignments(variables)) yield {
      assignment -> variable.values.map{
        value => this.assignmentScores(Map(variable -> value) ++ assignment)
      }.sum
    }
    Factor(variables, assignmentScores.toMap)
  }

  def normalized: Factor[VAL] = {
    val sum = assignmentScores.values.sum
    Factor(this.variables, assignmentScores.mapValues(_ / sum))
  }

  override def toString = {
    this.assignmentScores.mkString("", "\n", "\n")
  }
}
object Factor {
  def apply[VAL](
    variables: List[Variable[VAL]],
    assignments: (List[VAL], Double)*): Factor[VAL] = {
    Factor(variables, assignments.map{
      case (values, score) => (variables zip values).toMap -> score
    }.toMap)
  }
}

val A = new Variable('A, List(true, false))
val B = new Variable('B, List(true, false))
val E = new Variable('E, List(true, false))

val X = new Variable('X, List("a", "b", "c"))
val Y = new Variable('Y, List("c", "d"))

val pB = Factor(
  List(B),
  List(true) -> 0.001,
  List(false) -> 0.999)

val pE = Factor(
  List(E),
  List(true) -> 0.002,
  List(false) -> 0.998)

val pABE = Factor(
  List(A, B, E),
  List(true, true, true) -> 0.95,
  List(true, true, false) -> 0.94,
  List(true, false, true) -> 0.29,
  List(true, false, false) -> 0.001,
  List(false, true, true) -> 0.05,
  List(false, true, false) -> 0.06,
  List(false, false, true) -> 0.71,
  List(false, false, false) -> 0.999)

val pjA = Factor(
  List(A),
  List(true) -> 0.9,
  List(false) -> 0.05)

val pmA = Factor(
  List(A),
  List(true) -> 0.7,
  List(false) -> 0.01)


println(pjA * pmA)
println(pABE * pjA * pmA)
println((pABE * pjA * pmA - A))
println(pE * (pABE * pjA * pmA - A))
println(pE * (pABE * pjA * pmA - A) - E)
println(pB * (pE * (pABE * pjA * pmA - A) - E))
println((pB * pE * pABE * pjA * pmA - A - E).normalized)
