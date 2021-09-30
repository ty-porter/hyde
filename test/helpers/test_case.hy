class TestCase {
  init() {
    this.successSymbol = ".";
    this.successColor  = "\033[1;32;48m";

    this.failureSymbol = "F";
    this.failureColor  = "\033[1;31;48m";

    this.termColor     = "\033[1;37;0m";

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
    var passCount = 0;
    var failCount = 0;

    for (var i = 0; i < testSize; i = i + 1) {
      var test = this.testRunners.get(i);

      var value = test();

      var result = Map();
      result.set("result", value);
      result.set("test_name", test);

      if (value == True) {
        passCount = passCount + 1;
      }

      if (value == False) {
        failCount = failCount + 1;
      }

      results = arrayAppend(results, result);
    }

    this.printTestResults(results);
    
    var totals = Map();
    totals.set("count", results.length());
    totals.set("passed", passCount);
    totals.set("failed", failCount);

    return totals;
  }

  printTestResults(results) {
    var outputBuffer = "";

    for (var i = 0; i < results.length(); i = i + 1) {
      var value = results.get(i).get("result");
      var test = results.get(i).get("test_name");

      if (value == True) {
        if (outputBuffer == "") {
        outputBuffer = this.successColor + "  .";
        } else {
          outputBuffer = outputBuffer + ".";
        }
      } else {
        this.printNonEmptyString(outputBuffer);

        var failureString = this.failureColor + "  F " + this.name() + "." + toString(test) + this.termColor;
        print failureString;

        outputBuffer = "";
      }
    }

    this.printNonEmptyString(outputBuffer);
  }

  printNonEmptyString(string) {
    if (string != "  ") {
      print string + this.termColor;
    }
  }
}
