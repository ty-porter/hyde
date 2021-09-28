class TestCase {
  init() {
    this.successSymbol = ".";
    this.failureSymbol = "F";
    this.testRunners = Array(0);
  }

  assert(value) {
    return value == True;
  }

  assertEquals(value1, value2) {
    return value1 == value2;
  }

  name() {
    print "UNDEFINED";
  }

  loadTests(testRunners) {
    var newTestRunners = arrayConcat(this.testRunners, testRunners);

    this.testRunners = newTestRunners;
  }

  runEach() {
    var testSize = this.testRunners.length();

    if (testSize == 0) {
      return 0;
    }

    var results = Array(0);

    for (var i = 0; i < testSize; i = i + 1) {
      var test = this.testRunners.get(i);

      var value = test();

      var result = Map();
      result.set("result", value);
      result.set("test_name", test);

      results = arrayAppend(results, result);
    }

    this.printTestResults(results);
    
    return results.length();
  }

  printTestResults(results) {
    var outputBuffer = "  ";

    for (var i = 0; i < results.length(); i = i + 1) {
      var value = results.get(i).get("result");
      var test = results.get(i).get("test_name");

      if (value == True) {
        outputBuffer = outputBuffer + ".";
      } else {
        this.printNonEmptyString(outputBuffer);
        print "  F " + this.name() + "." + toString(test) + " ";

        outputBuffer = "  ";
      }
    }

    this.printNonEmptyString(outputBuffer);
  }

  printNonEmptyString(string) {
    if (string != "  ") {
      print string;
    }
  }
}
