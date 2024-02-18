from reformatter import functions as fn
import json

def check_save_obj_to_file(obj, save_path):
    fn.save_obj_to_file(obj, save_path)
    with open(save_path, "r", encoding="utf-8") as f:
        assert obj == json.load(f)
        
def test_save_obj_to_file(tmp_path):
    obj = {"a": 1, "b": 2, "c": 3}
    save_path = tmp_path / "test.json"
    check_save_obj_to_file(obj, save_path)
    
    
