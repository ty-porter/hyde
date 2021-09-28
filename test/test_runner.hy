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
    var testCount = 0;

    for (var i = 0; i < testSize; i = i + 1) {
      var testClass = this.testClasses.get(i);
      var test = testClass();

      test.loadTests();

      print test.name() + ":";

      var newTestCount = test.runEach();
      testCount = testCount + newTestCount;
      
      if (newTestCount == 0) {
        print "  No tests found for " + test.name() + ".";
      }
    }

    endTime = clock();
    duration = (endTime - startTime) / 1000;

    print "";
    print "Completed!";
    print "  Ran " + toString(testCount) + " tests in " + toString(duration) + " seconds.";
  }
}