package pants.avrohugger.app

import pants.avrohugger.avro.TestRecord

object MainApp extends App {
    val record = TestRecord("foo")
    println("record = %s".format(record))
}
