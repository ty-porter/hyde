load "test/helpers/test_case.hy";

class Test < TestCase {
  name() {
    return "Globals";
  }

  # Most tests are simple assertions as they are handled in Python.
  testClock() {
    clock();

    return super.assert(True);
  }

  testToString() {
    var str = toString("string");
    var num = toString(1);
    var fn  = toString(this.name);

    var expectedStr = "string";
    var expectedNum = "1.0";
    var expectedFn  = "<fn name>";

    if (str != expectedStr) {
      return super.assert(False);
    }

    if (num != expectedNum) {
      return super.assert(False);
    }

    if (fn != expectedFn) {
      return super.assert(False);
    }

    return super.assert(True);
  }

  testArrayInit() {
    var array = Array(0);

    return super.assert(True);
  }

  testArrayInitWithSize() {
    var array = Array(5);

    return super.assertEquals(array.length(), 5);
  }

  testMapInit() {
    var map = Map();

    return super.assert(True);
  }

  testBasicHttpRequestHandlerInit() {
    var handler = BasicHttpRequestHandler;

    return super.assert(True);
  }


  loadTests() {
    var tests = Array(0);

    tests = arrayAppend(tests, this.testClock);
    tests = arrayAppend(tests, this.testToString);
    tests = arrayAppend(tests, this.testArrayInit);
    tests = arrayAppend(tests, this.testArrayInitWithSize);
    tests = arrayAppend(tests, this.testMapInit);
    tests = arrayAppend(tests, this.testBasicHttpRequestHandlerInit);

    super.loadTests(tests);
  }
}