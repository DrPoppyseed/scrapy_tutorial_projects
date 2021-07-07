import os
import json

target_filename = "./latest_layers.txt"


def merge(filename: str) -> list:
    f = open(filename, "r")
    files = f.readlines()
    return files


def extract_cwur(dicts: dict, data: dict) -> dict:
    for school in data:
        school_data = data[school]

        # initialize
        schoolname = school_data["name"]
        ff_schoolname = school
        country = school_data["country"]

        # add to dict --- general information
        dicts[ff_schoolname] = {
            "general": {
                "name": schoolname,
                "ff_name": ff_schoolname,
                "country": country,
                "forbes_description": "",
                "forbes_uri": "",
            },
            "rankings_by_category": {"cwur": {}},
        }

        for key in school_data.keys():
            if key != "name" and key != "country" and key != "score":
                category_name = key.lower().replace(" ", "_")

                # add to dict --- rankings information
                dicts[ff_schoolname]["rankings_by_category"]["cwur"][
                    category_name
                ] = school_data[key]

    return dicts


def extract_forbes(dicts: dict, data: dict) -> dict:
    for school in data:
        school_data = data[school]

        schoolname = school_data["name"]
        ff_schoolname = school

        # if school already exists in dicts
        # => add rankings to pre-existing dicts entry
        if ff_schoolname in dicts.keys():
            # general info
            dicts[ff_schoolname]["general"]["forbes_description"] = (
                school_data.get("description") or ""
            )
            dicts[ff_schoolname]["general"]["forbes_uri"] = (
                school_data.get("forbes_uri") or ""
            )
            # populating rankings data
            dicts[ff_schoolname]["rankings_by_category"]["forbes"] = {
                "forbes_2019_ranking": {
                    "year": "2019",
                    "rank": school_data.get("forbes_rank"),
                },
                "child_rankings_by_category": school_data.get("rankings_by_category"),
            }
        # if school does not exist in dicts
        # => create new dicts item
        else:
            dicts[ff_schoolname] = {
                "general": {
                    "name": schoolname,
                    "ff_name": ff_schoolname,
                    "country": "",
                    "forbes_description": school_data.get("description") or "",
                    "forbes_uri": school_data.get("forbes_uri") or "",
                },
                "rankings_by_category": {
                    "forbes": {
                        "forbes_2019_ranking": {
                            "year": "2019",
                            "rank": school_data.get("forbes_rank"),
                        },
                        "child_rankings_by_category": school_data.get(
                            "rankings_by_category"
                        ),
                    }
                },
            }

    return dicts


def extract_qs(dicts: dict, data: dict) -> dict:
    for school in data:
        school_data = data[school]

        schoolname = school_data["name"]
        ff_schoolname = school

        if ff_schoolname in dicts.keys():
            # if country does not exist, populate it
            if dicts[ff_schoolname]["general"]["country"] == "":
                dicts[ff_schoolname]["general"]["country"] = school_data["country"]

            dicts[ff_schoolname]["rankings_by_category"]["qs"] = school_data[
                "rankings_by_category"
            ]

        else:
            dicts[ff_schoolname] = {
                "general": {
                    "name": schoolname,
                    "ff_name": ff_schoolname,
                    "country": school_data["country"],
                    "forbes_description": "",
                    "forbes_uri": "",
                },
                "rankings_by_category": {"qs": school_data["rankings_by_category"]},
            }

    return dicts


def extract_the(dicts: dict, data: dict) -> dict:
    for school in data:
        school_data = data[school]
        schoolname = school_data["name"]
        ff_schoolname = school

        if ff_schoolname in dicts.keys():
            if dicts[ff_schoolname]["general"]["country"] == "":
                dicts[ff_schoolname]["general"]["country"] = school_data["country"]

            dicts[ff_schoolname]["rankings_by_category"]["the"] = school_data[
                "rankings_by_category"
            ]

        else:
            dicts[ff_schoolname] = {
                "general": {
                    "name": schoolname,
                    "ff_name": ff_schoolname,
                    "country": school_data["country"],
                    "forbes_description": "",
                    "forbes_uri": "",
                },
                "rankings_by_category": {"the": school_data["rankings_by_category"]},
            }

    return dicts


def extract_from_files(filename: str) -> None:
    files = merge(filename)
    dicts = {}
    for i, file in enumerate(files):
        f = open(file.strip())
        data = json.load(f)

        if i == 0:
            # cwur
            dicts = extract_cwur(dicts, data)
        elif i == 1:
            # forbes
            dicts = extract_forbes(dicts, data)
        elif i == 2:
            # qs
            dicts = extract_qs(dicts, data)
        elif i == 3:
            # the
            dicts = extract_the(dicts, data)

    with open("./layer_1_output.json", "w+") as outfile:
        outfile.write(json.dumps(dicts))


def main() -> None:
    extract_from_files(target_filename)


main()
