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

  testKeys() {
    var map = Map();

    map.set("key", True);
    for (var i = 0; i < 1; i = i + 1) {
      return super.assertEquals(map.keys().get(0), "key");
    }
  }

  testMerge() {
    var map1 = Map();
    var map2 = Map();

    map1.set("map1", True);
    map2.set("map2", True);

    var map3 = map1.merge(map2);

    return super.assert(map3.get("map1") and map3.get("map2"));
  }

  loadTests() {
    var tests = Array(0);

    tests = arrayAppend(tests, this.testMapSetAndGet);
    tests = arrayAppend(tests, this.testKeys);
    tests = arrayAppend(tests, this.testMerge);

    super.loadTests(tests);
  }
}