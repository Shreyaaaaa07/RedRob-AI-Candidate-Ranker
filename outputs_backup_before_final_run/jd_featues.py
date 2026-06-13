import json

with open("outputs/jd_features.json", "r") as f:
    jd = json.load(f)

print("Must Have Skills:")
print(jd.get("must_have_skills"))

print("\nPreferred Skills:")
print(jd.get("preferred_skills"))

