import json
import hypothesis
import hypothesis.strategies as st


def serialize(obj: dict[str, str]):
    return json.dumps(obj)


def bad_deserialize(json_str: str):
    # print(json_str)
    out = json.loads(json_str)
    if "0" in out:
        del out["0"]
    return out


@hypothesis.given(st.data())
def test_inverse_1(data: st.DataObject):
    obj = data.draw(st.dictionaries(st.text(), st.text()))
    assert bad_deserialize(serialize(obj)) == obj


@hypothesis.given(st.data())
def test_inverse_2(data: st.DataObject):
    obj = data.draw(st.dictionaries(st.text(), st.text()))
    s = serialize(obj)
    assert serialize(bad_deserialize(s)) == s
