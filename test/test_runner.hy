class TestRunner {
  init() {
    this.testClasses = Array(0);
  }

  registerTestClass(test) {
    var testClasses = arrayAppend(this.testClasses, testClass);
    this.testClasses = testClasses;
  }

  run() {
    var testSize = this.testClasses.length();
    var startTime = clock();
    var endTime;
    var duration;
    var totalTestResults = Map();

    for (var i = 0; i < testSize; i = i + 1) {
      var testClass = this.testClasses.get(i);
      var test = testClass();

      test.loadTests();

      print test.name() + ":";

      var testTotals = test.runEach();
      totalTestResults = this.addMapValues(totalTestResults, testTotals);
      
      if (testTotals.get("count") == 0) {
        print "  No tests found for " + test.name() + ".";
      }
    }

    endTime = clock();
    duration = (endTime - startTime) / 1000;

    var testCount = totalTestResults.get("count");
    var passCount = totalTestResults.get("passed");
    var failCount = totalTestResults.get("failed");

    print "";
    print "Completed!";
    print "  Ran " + toString(testCount) + " tests in " + toString(duration) + " seconds.";
    print "  (" + toString(passCount) + " passed, " + toString(failCount) + " failed)";
  }

  addMapValues(map1, map2) {
    var map3 = Map();

    for (var i = 0; i < map2.keys().length(); i = i + 1) {
      var key = map2.keys().get(i);
      var map1Value = map1.get(key) or 0;
      var map2Value = map2.get(key) or 0;

      map3.set(key, map1Value + map2Value);
    }

    return map3;
  }
}