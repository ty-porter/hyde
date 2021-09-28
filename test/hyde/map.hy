load "test/helpers/test_case.hy";

class Test < TestCase {
  name() {
    return "Map";
  }
  
  testMapSetAndGet() {
    var map = Map();
    map.set("expected", True);

    return super.assert(map.get("expected"));
  }

  loadTests() {
    var tests = Array(0);

    tests = arrayAppend(tests, this.testMapSetAndGet);

    super.loadTests(tests);
  }
}