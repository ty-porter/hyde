load "test/helpers/test_case.hy";

class Test < TestCase {
  name() {
    return "Scope";
  }

  testGlobalScope() {
    var b = "global";

    {
      var b = "local";
    }

    return super.assertEquals(b, "global");
  }

  testLocalScope() {
    var b = "global";

    {
      var b = "local";
      return super.assertEquals(b, "local");
    }
  }

  loadTests() {
    var tests = Array(0);

    tests = arrayAppend(tests, this.testGlobalScope);
    tests = arrayAppend(tests, this.testLocalScope);

    super.loadTests(tests);
  }
}