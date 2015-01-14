import scala.math.Ordering.Implicits._

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

case class Factor[VAL: Ordering](
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
    implicit val ordering = Ordering.by{
      (assignment: Map[Variable[VAL],VAL]) => assignment.toSeq.map{
        case (variable, value) => (variable.symbol.toString, value)
      }
    }
    this.assignmentScores.toSeq.sorted.mkString("", "\n", "\n")
  }
}
object Factor {
  def apply[VAL : Ordering](
    variables: List[Variable[VAL]],
    assignments: (List[VAL], Double)*): Factor[VAL] = {
    Factor(variables, assignments.map{
      case (values, score) => (variables zip values).toMap -> score
    }.toMap)
  }
}

val A = new Variable('A, List(true, false))
val B = new Variable('B, List(true, false))
val C = new Variable('B, List(true, false))
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

val ab = Factor(
  List(A, B),
  List(true, true) -> 0.3,
  List(true, false) -> 0.1,
  List(false, true) -> 0.7,
  List(false, false) -> 0.9)

val bc = Factor(
  List(B, C),
  List(true, true) -> 0.6,
  List(true, false) -> 0.8,
  List(false, true) -> 0.4,
  List(false, false) -> 0.2)

println(ab * bc)
println((ab * bc) - B)


val X2 = new Variable('X, List("x", "y", "z"))
val A2 = new Variable('A, List("a", "¬a"))
val I2 = new Variable('I, List("i", "j"))


val xa = Factor(
  List(X2, A2),
  List("x", "a") -> 1,
  List("x", "¬a") -> 4,
  List("y", "a") -> 3,
  List("y", "¬a") -> 2,
  List("z", "a") -> 2,
  List("z", "¬a") -> 5)

val ai = Factor(
  List(A2, I2),
  List("a", "i") -> 3,
  List("a", "j") -> 6,
  List("¬a", "i") -> 2,
  List("¬a", "j") -> 4)

println(xa * ai)
println((xa * ai) - A2)
