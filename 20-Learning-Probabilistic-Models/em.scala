import scala.collection.Map
import scala.collection.immutable.ListMap

package object em {

  val coinData = List(
    "HHHHTHHHHH",
    "HTHTTTHHTT",
    "HTHHHHHTHH",
    "THHHTHHHTH",
    "HTTTHHTHTH").map(_.toSeq)

  val candyCountsData = ListMap(
    Map("Flavor" -> "cherry", "Wrapper" -> "red", "Hole" -> "true") -> 273,
    Map("Flavor" -> "cherry", "Wrapper" -> "red", "Hole" -> "false") -> 93,
    Map("Flavor" -> "cherry", "Wrapper" -> "green", "Hole" -> "true") -> 104,
    Map("Flavor" -> "cherry", "Wrapper" -> "green", "Hole" -> "false") -> 90,
    Map("Flavor" ->  "lime", "Wrapper" -> "red", "Hole" -> "true") -> 79,
    Map("Flavor" -> "lime", "Wrapper" -> "red", "Hole" -> "false") -> 100,
    Map("Flavor" -> "lime", "Wrapper" -> "green", "Hole" -> "true") -> 94,
    Map("Flavor" ->  "lime", "Wrapper" -> "green", "Hole" -> "false") -> 167)

  val bcxyData = Seq(
    ("bc".toSeq, "xy".toSeq),
    ("b".toSeq, "y".toSeq))

  val blueHouseData = Seq(
    (Seq("la", "casa", "azul"), Seq("the", "blue", "house")),
    (Seq("la", "casa"), Seq("the", "house")))

  val printParameters = (parameters: Map[_, Map[_, Double]]) => {
    for ((key, value) <- parameters) {
      printf("%s -> %s\n", key, value)
    }
    println
  }
}

package em {

abstract class ExpectationMaximization[NAME, VALUE] {
  type Parameters = Map[NAME, Map[VALUE, Double]]

  val initialParameters: Parameters

  def collectCounts(parameters: Parameters): Parameters

  def normalize(parameters: Parameters): Parameters = {
    for ((name, valueCounts) <- parameters) yield {
      (name, this.normalizeMap(valueCounts))
    }
  }

  def iterator = {
    var parameters = this.initialParameters
    Iterator(parameters) ++ Iterator.continually {
      parameters = this.normalize(this.collectCounts(parameters))
      parameters
    }
  }

  protected def emptyCounts = {
    for ((name, valueProbs) <- this.initialParameters) yield {
      val counts = for ((value, prob) <- valueProbs) yield (value, 0.0)
      val countsMap = collection.mutable.Map.empty[VALUE, Double] ++ counts
      (name, countsMap)
    }
  }

  protected def normalizeMap[T](valueCounts: Map[T, Double]) = {
    val total = valueCounts.values.sum
    valueCounts.mapValues(_ / total)
  }
}

class CandyProblem(candyCounts: Map[Map[String, String], Int])
extends ExpectationMaximization[String, String] {

  val initialParameters = Map(
    "Bag" -> Map("1" -> 0.6, "2" -> 0.4),
    "1Flavor" -> Map("cherry" -> 0.6, "lime" -> 0.4),
    "1Wrapper" -> Map("red" -> 0.6, "green" -> 0.4),
    "1Hole" -> Map("true" -> 0.6, "false" -> 0.4),
    "2Flavor" -> Map("cherry" -> 0.4, "lime" -> 0.6),
    "2Wrapper" -> Map("red" -> 0.4, "green" -> 0.6),
    "2Hole" -> Map("true" -> 0.4, "false" -> 0.6))

  def collectCounts(parameters: Parameters): Parameters = {
    val counts = this.emptyCounts

    val total = candyCounts.values.sum
    for ((features, count) <- candyCounts) {
      // P(Bag=1|...)
      val bagProbs = this.normalizeMap(
        for ((bag, bagProb) <- parameters("Bag")) yield {
          val featureProbs = features.map{
            case (name, value) => parameters(bag + name)(value)
          }
          (bag, featureProbs.product * bagProb)
        })

      // partial counts:
      // (how many times was bag 1/2 chosen?)
      // (how many times was each feature chosen from bag 1/2?)
      for ((bag, prob) <- bagProbs) {
        counts("Bag")(bag) += prob * count
        for ((name, value) <- features) {
          counts(bag + name)(value) += prob * count
        }
      }
    }

    counts
  }
}

class TranslationProblem[T](val data: Seq[(Seq[T], Seq[T])])
extends ExpectationMaximization[T, T] {

  val initialParameters = {
    val pairs =
      for ((source, target) <- this.data; s <- source; t <- target)
      yield (s -> t)
    pairs.groupBy{ case (s, t) => s }.mapValues{
      values => this.normalizeMap(values.map{ case (s, t) => t -> 1.0 }.toMap)
    }
  }

  def collectCounts(parameters: Parameters): Parameters = {
    val counts = this.emptyCounts
    for ((source, target) <- data) {
      val alignments = target.permutations.map(source -> _).toList
      val observedAlignmentProbs = for (alignment <- alignments) yield {
        val probs = alignment.zipped.map{
          case (sWord, tWord) => parameters(sWord)(tWord)
        }
        (alignment, probs.product)
      }
      val alignmentProbs = this.normalizeMap(observedAlignmentProbs.toMap)

      for (alignment <- alignments; (sWord, tWord) <- alignment.zipped) {
        counts(sWord)(tWord) += alignmentProbs(alignment)
      }
    }
    counts
  }
}

class CoinProblem(
  data: Seq[Seq[Char]], probA: Double, probAH: Double, probBH: Double)
extends ExpectationMaximization[Char, Char] {

  val initialParameters = Map(
    'C' -> Map('A' -> probA, 'B' -> (1.0 - probA)),
    'A' -> Map('H' -> probAH, 'T' -> (1.0 - probAH)),
    'B' -> Map('H' -> probBH, 'T' -> (1.0 - probBH)))

  def collectCounts(parameters: Parameters): Parameters = {
    val counts = this.emptyCounts
    val c = parameters('C')
    val ab = parameters - 'C'

    for (tosses <- data) {
      // P(C=A|"HTTTHHTHTH")
      // = \alpha * P("HTTTHHTHTH"|C=A) * P(C=A)
      // = \alpha * P(H|C=A) * P(T|C=A) * ... * P(C=A)
      // = \alpha * P(H|A) * P(T|A) * ... * P(C=A)
      val coinProbs = this.normalizeMap(ab.map{
        case (name, valueProbs) =>
          (name, tosses.map(valueProbs).product * c(name))
      })

      // partial counts (how many times was coin A/B chosen?)
      // C -> A += P(C=A|...)
      // C -> B += P(C=B|...)
      // partial counts (how many times did heads/tails come up on coin A/B?)
      // A -> H += P(C=A|...)
      // A -> T += P(C=A|...)
      // B -> H += P(C=B|...)
      // B -> T += P(C=B|...)
      for ((coin, prob) <- coinProbs) {
        counts('C')(coin) += prob
        for (value <- tosses) {
          counts(coin)(value) += prob
        }
      }
    }
    counts
  }
}

}

