import hashlib
import os
import uuid
import json
import pandas as pd
import time
import requests


# Function to read an Excel file and return a DataFrame
def read_excel_file(file_path):
    """
    Reads an Excel file and returns a DataFrame.
    """
    try:
        current_path = f"{os.getcwd()}/app/files/excel/{file_path}"
        df = pd.read_excel(current_path)

        return {"data": df}

    except Exception as err:
        print(f"Error while reading Excel file: {err}")
        return {
            "error": f"Error while reading Excel file for file name: {file_path}"
        }


def read_json_file(file_path):
    """
    Reads a JSON file and returns data.
    """
    try:
        current_path = f"{os.getcwd()}/app/files/excel/{file_path}"
        with open(current_path, 'r') as f:
            data = json.load(f)

        return {"data": data}
    except Exception as err:
        print(f"Error while reading json file : {err}")
        return {
            "error": f"Error while reading json file for file name: {file_path}"
        }


def create_json_file(data, file_name,folder):
    """
    Creates a JSON file from data.
    """
    try:
        current_path = f"{os.getcwd()}/app/project/{folder}/{file_name}"
        with open(current_path, 'w') as f:
            json.dump(data, f, indent=4)

        return {
            "data": file_name
        }

    except Exception as err:
        print(f"Error while creating json file: {err}")
        return {
            "error": f"Error while creating json file for file name: {file_name}"
        }


def create_uuid(uniquestring):
    """
    Creates a UUID from a given string.
    """
    try:
        namespace = uuid.NAMESPACE_DNS
        generated_uuid = uuid.uuid5(namespace, uniquestring)

        return {
            "data": generated_uuid
        }

    except Exception as err:
        print(f"Error while genrating UUID: {err}")
        return {
            "error": f"Error while genrating UUID for uniquestring : {uniquestring}"
        }


def string_to_7_digit_number(input_string):
    """
    Converts a string to a 7-digit number using SHA-256 hash.
    """

    try:
        hash_object = hashlib.sha256(input_string.encode())
        hex_dig = hash_object.hexdigest()
        hash_int = int(hex_dig, 16)
        seven_digit_number = (hash_int % 9000000) + 1000000

        return {
            "data": seven_digit_number
        }

    except Exception as err:
        print(f"Error while creating string to 7 digit number: {err}")
        return {
            "error": f"Error while creating string to 7 digit number for uniquestring : {input_string}"
        }


def add_value_to_key(key, sample_movie_data, title_type, data):
    """
    Appends short and long titles or descriptions to sample_movie_data.
    """
    try:

        for title_type_key in ["eng", "may", "tam", "chi", "tha", "ind"]:

            if key not in ["title", "description"]:
                sample_movie_data[key][title_type_key] = str(data).split(",")
            else:
                sample_movie_data[key][title_type][title_type_key] = data
        return {
            "data": True
        }
    except Exception as err:
        print(f"Error in the add_value_to_key function : {str(err)}")
        return {
            "error": data
        }


def append_genre(key, sample_movie_data, title_type, data):
    """
    Appends genre information to sample_movie_data.
    """
    try:
        for title_type_key in ["eng", "may", "tam", "chi", "tha", "ind"]:
            if title_type == "primary":
                data = data.split(",")[0]
            else:
                if len(data.split(",")) > 1:
                    data = data.split(",")[1]
                else:
                    data = data.split(",")[0]
            sample_movie_data[key][title_type][0]["name"][title_type_key] = data
        return {
            "data": True
        }
    except Exception as err:
        print(f"Error in the append_genre function : {str(err)}")
        return {
            "error": data
        }


def append_image(sample_movie_data, type, url):
    """
    Appends image URLs to sample_movie_data.
    """
    try:
       
        url = f"https://datastore.videoready.int.xp.irdeto.com/{url}"
        for item in sample_movie_data['images']:
            if item['type'] == type:
                item['url'] = url
            elif item['type'] == type:
                item['url'] = url
            elif item['type'] == type:
                item['url'] = url
        return {
            "data": True
        }
    except Exception as err:
        print(f"Error in the append_image function : {str(err)}")
        return {
            "error": url
        }


def excel_to_json_file():
    """
    Converts Excel data to JSON file.
    """
    try:
        sample_brand_data = read_json_file("sample_brand.json")
        sample_season_data = read_json_file("sample_season.json")
        sample_episode_data = read_json_file("sample_episode.json")

        # if sample_movie_data.get("error"):
        #     raise ValueError(sample_movie_data.get("error"))
        sample_brand_data = sample_brand_data.get("data")
        sample_season_data = sample_season_data.get("data")
        sample_episode_data = sample_episode_data.get("data")


        constant = read_json_file("sample.json")
        if constant.get("error"):
            raise ValueError(constant.get("error"))
        constant = constant.get("data")

        df_brand= read_excel_file("VR BRAND DATA.xlsx")
        # if df.get("error"):
        #     raise ValueError(df.get("error"))
        df_brand_data = df_brand.get("data")

        df_season = read_excel_file("VR SEASON DATA.xlsx")
        df_season_data = df_season.get("data")

        df_episode = read_excel_file("EPISODE DATA.xlsx")
        df_episode_data = df_episode.get("data")
        # Merge df1 and df2 on 'key'
        merged_df1_df2 = pd.merge(df_brand_data, df_season_data, left_on='asset_id',right_on="brand_id", how='left')
        df = pd.merge(merged_df1_df2, df_episode_data, left_on='asset_id_x',right_on="brand_id", how='left')
        # merged_df1_df2.to_excel("output.xlsx")


        count = 0
        conut_upload = 0
        print("df.index", df.index)
        for ind in df.index:

            count += 1
            conut_upload +=1
            # Generating brand
            string_to_uniqueid_brand = f"{df['asset_id_x'][ind]} {df['brand_title_en'][ind]} {df['imdbId'][ind]}"
            unique_number_brand  = string_to_7_digit_number(string_to_uniqueid_brand).get("data")
            clientContentId = f"PACK000000000{unique_number_brand}"
            externalId = "".join(
                ("AggregatedSeries_", str(create_uuid(string_to_uniqueid_brand).get("data"))))
            sample_brand_data["externalId"] = externalId
            sample_brand_data["clientContentId"] = clientContentId
            

            # Generating season
            string_to_uniqueid_season = f"{df['asset_id_x'][ind]} {df['season_title_en'][ind]} {df['brand_id_x'][ind]}"
            unique_number_season  = string_to_7_digit_number(string_to_uniqueid_season).get("data")
            clientContentId_season = f"PACK000000000{unique_number_season}"
            externalId_season = "".join(
                ("AggregatedSeason_", str(create_uuid(string_to_uniqueid_season).get("data"))))
            sample_season_data["externalId"] = externalId_season
            sample_season_data["clientContentId"] = clientContentId_season

            # Generating eploye
            string_to_uniqueid_episode = f"{df['brand_id_y'][ind]} {df['season_id'][ind]} {df['asset_id'][ind]}"
            unique_number_episode  = string_to_7_digit_number(string_to_uniqueid_episode).get("data")
            clientContentId_episode = f"PACK000000000{unique_number_episode}"
            externalId_episode = "".join(
                ("AggregatedTvShow_", str(create_uuid(string_to_uniqueid_episode).get("data"))))
            sample_episode_data["externalId"] = externalId_episode
            sample_episode_data["clientContentId"] = clientContentId_episode
            


            short_title = add_value_to_key(
                "title", sample_brand_data, "short", df["brand_title_en"][ind])
            if short_title.get("error"):
                print(
                    f"Error in the VR Core movie file in record for asset_id: {df['asset_id'][ind]} and movie_title_en: {short_title.get('error')}")

            long_title = add_value_to_key(
                "title", sample_brand_data, "long", df["brand_title_en"][ind])
            if long_title.get("error"):
                print(
                    f"Error in the VR Core movie file in record for asset_id: {df['asset_id'][ind]} and movie_title_en: {long_title.get('error')}")
                

            #session title
            short_title = add_value_to_key(
                "title", sample_season_data, "short", df["season_title_en"][ind])
            if short_title.get("error"):
                print(
                    f"Error in the VR Core movie file in record for asset_id: {df['asset_id'][ind]} and movie_title_en: {short_title.get('error')}")

            long_title = add_value_to_key(
                "title", sample_season_data, "long", df["season_title_en"][ind])
            if long_title.get("error"):
                print(
                    f"Error in the VR Core movie file in record for asset_id: {df['asset_id'][ind]} and movie_title_en: {long_title.get('error')}")
                
            

            # eployee
            short_title = add_value_to_key(
                "title", sample_episode_data, "short", df["episode_title_en"][ind])
            if short_title.get("error"):
                print(
                    f"Error in the VR Core movie file in record for asset_id: {df['asset_id'][ind]} and movie_title_en: {short_title.get('error')}")

            long_title = add_value_to_key(
                "title", sample_episode_data, "long", df["episode_title_en"][ind])
            if long_title.get("error"):
                print(
                    f"Error in the VR Core movie file in record for asset_id: {df['asset_id'][ind]} and movie_title_en: {long_title.get('error')}")
                


            short_description = add_value_to_key(
                "description", sample_brand_data, "short", df["brand_description_en"][ind])
            if short_description.get("error"):
                print(
                    f"Error in the VR Core movie file in record for asset_id: {df['asset_id'][ind]} and description_en: {short_description.get('error')}")

            long_description = add_value_to_key(
                "description", sample_brand_data, "long", df["brand_description_en"][ind])
            if long_description.get("error"):
                print(
                    f"Error in the VR Core movie file in record for asset_id: {df['asset_id'][ind]} and description_en: {long_description.get('error')}")
                

            # session description 
            short_description = add_value_to_key(
                "description", sample_season_data, "short", df["season_description_en"][ind])
            if short_description.get("error"):
                print(
                    f"Error in the VR Core movie file in record for asset_id: {df['asset_id'][ind]} and description_en: {short_description.get('error')}")

            long_description = add_value_to_key(
                "description", sample_season_data, "long", df["season_description_en"][ind])
            if long_description.get("error"):
                print(
                    f"Error in the VR Core movie file in record for asset_id: {df['asset_id'][ind]} and description_en: {long_description.get('error')}")
    
            # eployee
            short_description = add_value_to_key(
                "description", sample_episode_data, "short", df["episode_description_en"][ind])
            if short_description.get("error"):
                print(
                    f"Error in the VR Core movie file in record for asset_id: {df['asset_id'][ind]} and description_en: {short_description.get('error')}")

            long_description = add_value_to_key(
                "description", sample_episode_data, "long", df["episode_description_en"][ind])
            if long_description.get("error"):
                print(
                    f"Error in the VR Core movie file in record for asset_id: {df['asset_id'][ind]} and description_en: {long_description.get('error')}")
                




            long_description = add_value_to_key(
                "actor", sample_brand_data, None, df["brand_actor_en"][ind])
            if long_description.get("error"):
                print(
                    f"Error in the VR Core movie file in record for asset_id: {df['asset_id'][ind]} and description_en: {long_description.get('error')}")

            long_description = add_value_to_key(
                "director", sample_brand_data, None, df["brand_director_en"][ind])
            if long_description.get("error"):
                print(
                    f"Error in the VR Core movie file in record for asset_id: {df['asset_id'][ind]} and description_en: {long_description.get('error')}")

            long_description = add_value_to_key(
                "producer", sample_brand_data, None, df["brandProducer_en"][ind])
            if long_description.get("error"):
                print(
                    f"Error in the VR Core movie file in record for asset_id: {df['asset_id'][ind]} and description_en: {long_description.get('error')}")
                

           # session actor
            long_description = add_value_to_key(
                "actor", sample_season_data, None, df["brand_actor_en"][ind])
            if long_description.get("error"):
                print(
                    f"Error in the VR Core movie file in record for asset_id: {df['asset_id'][ind]} and description_en: {long_description.get('error')}")

            long_description = add_value_to_key(
                "director", sample_season_data, None, df["brand_director_en"][ind])
            if long_description.get("error"):
                print(
                    f"Error in the VR Core movie file in record for asset_id: {df['asset_id'][ind]} and description_en: {long_description.get('error')}")

            long_description = add_value_to_key(
                "producer", sample_season_data, None, df["brandProducer_en"][ind])
            if long_description.get("error"):
                print(
                    f"Error in the VR Core movie file in record for asset_id: {df['asset_id'][ind]} and description_en: {long_description.get('error')}")
     
            # eployeee
            long_description = add_value_to_key(
                "actor", sample_episode_data, None, df["brand_actor_en"][ind])
            if long_description.get("error"):
                print(
                    f"Error in the VR Core movie file in record for asset_id: {df['asset_id'][ind]} and description_en: {long_description.get('error')}")

            long_description = add_value_to_key(
                "director", sample_episode_data, None, df["brand_director_en"][ind])
            if long_description.get("error"):
                print(
                    f"Error in the VR Core movie file in record for asset_id: {df['asset_id'][ind]} and description_en: {long_description.get('error')}")

            long_description = add_value_to_key(
                "producer", sample_episode_data, None, df["brandProducer_en"][ind])
            if long_description.get("error"):
                print(
                    f"Error in the VR Core movie file in record for asset_id: {df['asset_id'][ind]} and description_en: {long_description.get('error')}")
     


            primary_genre = append_genre(
                "genre", sample_brand_data, "primary", df["brand_genre_en"][ind])
            if primary_genre.get("error"):
                print(
                    f"Error in the VR Core movie file in record for asset_id: {df['asset_id'][ind]} and genre_en: {primary_genre.get('error')}")

            secondary_genre = append_genre(
                "genre", sample_brand_data, "secondary", df["brand_genre_en"][ind])
            if secondary_genre.get("error"):
                print(
                    f"Error in the VR Core movie file in record for asset_id: {df['asset_id'][ind]} and genre_en: {secondary_genre.get('error')}")
                
            # session genre
            primary_genre = append_genre(
                "genre", sample_season_data, "primary", df["brand_genre_en"][ind])
            if primary_genre.get("error"):
                print(
                    f"Error in the VR Core movie file in record for asset_id: {df['asset_id'][ind]} and genre_en: {primary_genre.get('error')}")

            secondary_genre = append_genre(
                "genre", sample_season_data, "secondary", df["brand_genre_en"][ind])
            if secondary_genre.get("error"):
                print(
                    f"Error in the VR Core movie file in record for asset_id: {df['asset_id'][ind]} and genre_en: {secondary_genre.get('error')}")
                    
                
            # employee
            primary_genre = append_genre(
                "genre", sample_episode_data, "primary", df["brand_genre_en"][ind])
            if primary_genre.get("error"):
                print(
                    f"Error in the VR Core movie file in record for asset_id: {df['asset_id'][ind]} and genre_en: {primary_genre.get('error')}")

            secondary_genre = append_genre(
                "genre", sample_episode_data, "secondary", df["brand_genre_en"][ind])
            if secondary_genre.get("error"):
                print(
                    f"Error in the VR Core movie file in record for asset_id: {df['asset_id'][ind]} and genre_en: {secondary_genre.get('error')}")


            boxcover = append_image(
                sample_brand_data, "boxcover", df["brand_cover_image_en"][ind])
            if boxcover.get("error"):
                print(
                    f"Error in the VR Core movie file in record for asset_id: {df['asset_id'][ind]} and cover_image_en: {boxcover.get('error')}")

            boxcover = append_image(
                sample_brand_data, "poster", df["brand_poster_image_en"][ind])
            if boxcover.get("error"):
                print(
                    f"Error in the VR Core movie file in record for asset_id: {df['asset_id'][ind]} and poster_image_en: {boxcover.get('error')}")

            boxcover = append_image(
                sample_brand_data, "thumbnail", df["web_banner_image"][ind])
            if boxcover.get("error"):
                print(
                    f"Error in the VR Core movie file in record for asset_id: {df['asset_id'][ind]} and web_banner_image: {boxcover.get('error')}")
                
            # session imgage
            boxcover = append_image(
                sample_season_data, "boxcover", df["season_cover_image_en"][ind])
            if boxcover.get("error"):
                print(
                    f"Error in the VR Core movie file in record for asset_id: {df['asset_id'][ind]} and cover_image_en: {boxcover.get('error')}")

            boxcover = append_image(
                sample_season_data, "poster", df["season_poster_image_en"][ind])
            if boxcover.get("error"):
                print(
                    f"Error in the VR Core movie file in record for asset_id: {df['asset_id'][ind]} and poster_image_en: {boxcover.get('error')}")

            boxcover = append_image(
                sample_season_data, "thumbnail", df["season_cover_image_en"][ind])
            if boxcover.get("error"):
                print(
                    f"Error in the VR Core movie file in record for asset_id: {df['asset_id'][ind]} and web_banner_image: {boxcover.get('error')}")
                
            # employee
            boxcover = append_image(
                sample_episode_data, "boxcover", df["episode_cover_image_en"][ind])
            if boxcover.get("error"):
                print(
                    f"Error in the VR Core movie file in record for asset_id: {df['asset_id'][ind]} and cover_image_en: {boxcover.get('error')}")

            boxcover = append_image(
                sample_episode_data, "poster", df["episode_poster_image_en"][ind])
            if boxcover.get("error"):
                print(
                    f"Error in the VR Core movie file in record for asset_id: {df['asset_id'][ind]} and poster_image_en: {boxcover.get('error')}")

            boxcover = append_image(
                sample_episode_data, "thumbnail", df["episode_cover_image_en"][ind])
            if boxcover.get("error"):
                print(
                    f"Error in the VR Core movie file in record for asset_id: {df['asset_id'][ind]} and web_banner_image: {boxcover.get('error')}")
                    
    

            sample_brand_data["yearOfRelease"] = int(df["brand_year"][ind])
            import random
            # print(random.randint(0, 9))
            sample_brand_data["rating"] = str(random.randint(6, 10))

            # session
            sample_season_data["yearOfRelease"] = int(df["season_year"][ind])
            sample_season_data["rating"] = str(df["season_rating"][ind])

            # session
            sample_season_data["seriesId"] = externalId
            sample_season_data["seasonNumber"] = str(df["season_number"][ind])

            # epsode
            sample_episode_data["seriesId"] = externalId
            sample_episode_data["seasonId"] = externalId_season
            sample_episode_data["episodeNumber"] = str(df["episode_number"][ind])
            sample_episode_data["seasonNumber"] = str(df["season_number"][ind])
            sample_episode_data["yearOfRelease"] = int(df["brand_year"][ind])
            sample_episode_data["rating"] = str(df["episode_rating"][ind])


            constant_data = constant.get(f"Content{count}")
            sample_episode_data["playUrls"][0]["duration"] = constant_data.get(
                "duration")
            sample_episode_data["playUrls"][0]["hls"]["fairplay"] = constant_data.get(
                "hls").get("fairplay")
            sample_episode_data["playUrls"][0]["dash"]["playready"] = constant_data.get(
                "dash").get("playready")
            sample_episode_data["playUrls"][0]["dash"]["widevine"] = constant_data.get(
                "dash").get("widevine")
            sample_episode_data["playUrls"][0]["licenseAcquisitionUrl"]["playready"] = constant_data.get(
                "licenseAcquisitionUrl").get("playready")
            sample_episode_data["playUrls"][0]["licenseAcquisitionUrl"]["widevine"] = constant_data.get(
                "licenseAcquisitionUrl").get("widevine")

            if count == 4:
                count = 0
            new_json = create_json_file(
                sample_brand_data, f"{df['asset_id_x'][ind]}","series")
            if new_json.get("error"):
                raise ValueError(sample_brand_data.get("error"))
            print(f"Successfully file is generated : {new_json.get('data')}")
            

            # session save
            ew_json = create_json_file(
                sample_season_data, f"{df['asset_id_y'][ind]}_{df['asset_id_x'][ind]}","session")
            if len(sample_season_data)<25:
                print("sample_season_data",len(sample_season_data))
            ew_json = create_json_file(
                sample_episode_data, f"{df['asset_id'][ind]}_{df['asset_id_x'][ind]}","episode")
            # if str(new_json.get('data')) == "brand_86363400":
            #     #brand_86363493
            #     time.sleep(1)
            try: 
                headers = {
                    'accept': '*/*',
                    'Content-Type': 'application/json'
                    }
                url = "https://api555.videoready444.dev.xp.irdeto.com11/metadata-ingestor/v1/metadata/ingest/series/save?contentType=series"
                response = requests.request("POST", url, headers=headers, json=sample_brand_data)
                print(response)
                # url = "https://api.videoready.dev.xp.irdeto.com/metadata-ingestor/v1/metadata/ingest/season/save?contentType=season"
                # response = requests.request("POST", url, headers=headers,  json=sample_season_data)
                # print(response)
                # url = "https://api.videoready.dev.xp.irdeto.com/metadata-ingestor/v1/metadata/ingest/vod/save?contentType=tv_show"
                # response = requests.request("POST", url, headers=headers, json=sample_episode_data)
                # print(response)
                # break
            except Exception as e:
                print("scs")    
                
    except Exception as e:
        print(f"An error occurred during the conversion process: {e}")
