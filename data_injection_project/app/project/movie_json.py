import requests
import time

from app.utilty import utily


def excel_to_json_file():
    """
    Converts Excel data to JSON file.
    """
    try:
        sample_movie_data = utily.read_json_file("sample_movie.json")

        if sample_movie_data.get("error"):
            raise ValueError(sample_movie_data.get("error"))
        sample_movie_data = sample_movie_data.get("data")

        constant = utily.read_json_file("sample.json")
        if constant.get("error"):
            raise ValueError(constant.get("error"))
        constant = constant.get("data")

        df = utily.read_excel_file("VR CORE MOVIES.xlsx")
        if df.get("error"):
            raise ValueError(df.get("error"))
        df = df.get("data")

        count = 0
        conut_upload = 0
        print("df.index", df.index)
        for ind in df.index:

            count += 1
            conut_upload  += 1
            # Generating unique IDs and content IDs
            string_to_uniqueid = f"{df['asset_id'][ind]} {df['movie_title_en'][ind]} {df['imdbId'][ind]}"
            unique_number = utily.string_to_7_digit_number(string_to_uniqueid).get("data")
            clientContentId = f"PACK000000000{unique_number}"
            externalId = "".join(
                ("AggregatedMovie_", str(utily.create_uuid(string_to_uniqueid).get("data"))))

            sample_movie_data["externalId"] = externalId
            sample_movie_data["clientContentId"] = clientContentId

            short_title = utily.add_value_to_key(
                "title", sample_movie_data, "short", df["movie_title_en"][ind])
            if short_title.get("error"):
                print(
                    f"Error in the VR Core movie file in record for asset_id: {df['asset_id'][ind]} and movie_title_en: {short_title.get('error')}")

            long_title = utily.add_value_to_key(
                "title", sample_movie_data, "long", df["movie_title_en"][ind])
            if long_title.get("error"):
                print(
                    f"Error in the VR Core movie file in record for asset_id: {df['asset_id'][ind]} and movie_title_en: {long_title.get('error')}")

            short_description = utily.add_value_to_key(
                "description", sample_movie_data, "short", df["description_en"][ind])
            if short_description.get("error"):
                print(
                    f"Error in the VR Core movie file in record for asset_id: {df['asset_id'][ind]} and description_en: {short_description.get('error')}")

            long_description =utily.add_value_to_key(
                "description", sample_movie_data, "long", df["description_en"][ind])
            if long_description.get("error"):
                print(
                    f"Error in the VR Core movie file in record for asset_id: {df['asset_id'][ind]} and description_en: {long_description.get('error')}")

            long_description = utily.add_value_to_key(
                "actor", sample_movie_data, None, df["actor_en"][ind])
            if long_description.get("error"):
                print(
                    f"Error in the VR Core movie file in record for asset_id: {df['asset_id'][ind]} and description_en: {long_description.get('error')}")

            long_description = utily.add_value_to_key(
                "director", sample_movie_data, None, df["director_en"][ind])
            if long_description.get("error"):
                print(
                    f"Error in the VR Core movie file in record for asset_id: {df['asset_id'][ind]} and description_en: {long_description.get('error')}")

            long_description = utily.add_value_to_key(
                "producer", sample_movie_data, None, df["producer_en"][ind])
            if long_description.get("error"):
                print(
                    f"Error in the VR Core movie file in record for asset_id: {df['asset_id'][ind]} and description_en: {long_description.get('error')}")

            primary_genre = utily.append_genre(
                "genre", sample_movie_data, "primary", df["genre_en"][ind])
            if primary_genre.get("error"):
                print(
                    f"Error in the VR Core movie file in record for asset_id: {df['asset_id'][ind]} and genre_en: {primary_genre.get('error')}")

            secondary_genre = utily.append_genre(
                "genre", sample_movie_data, "secondary", df["genre_en"][ind])
            if secondary_genre.get("error"):
                print(
                    f"Error in the VR Core movie file in record for asset_id: {df['asset_id'][ind]} and genre_en: {secondary_genre.get('error')}")

            boxcover = utily.append_image(
                sample_movie_data, "boxcover", df["cover_image_en"][ind])
            if boxcover.get("error"):
                print(
                    f"Error in the VR Core movie file in record for asset_id: {df['asset_id'][ind]} and cover_image_en: {boxcover.get('error')}")

            boxcover = utily.append_image(
                sample_movie_data, "poster", df["poster_image_en"][ind])
            if boxcover.get("error"):
                print(
                    f"Error in the VR Core movie file in record for asset_id: {df['asset_id'][ind]} and poster_image_en: {boxcover.get('error')}")

            boxcover = utily.append_image(
                sample_movie_data, "thumbnail", df["web_banner_image"][ind])
            if boxcover.get("error"):
                print(
                    f"Error in the VR Core movie file in record for asset_id: {df['asset_id'][ind]} and web_banner_image: {boxcover.get('error')}")

            sample_movie_data["yearOfRelease"] = int(df["movie_year"][ind])
            sample_movie_data["rating"] = str(df["rating"][ind])

            constant_data = constant.get(f"Content{count}")
            sample_movie_data["playUrls"][0]["duration"] = constant_data.get(
                "duration")
            sample_movie_data["playUrls"][0]["hls"]["fairplay"] = constant_data.get(
                "hls").get("fairplay")
            sample_movie_data["playUrls"][0]["dash"]["playready"] = constant_data.get(
                "dash").get("playready")
            sample_movie_data["playUrls"][0]["dash"]["widevine"] = constant_data.get(
                "dash").get("widevine")
            sample_movie_data["playUrls"][0]["licenseAcquisitionUrl"]["playready"] = constant_data.get(
                "licenseAcquisitionUrl").get("playready")
            sample_movie_data["playUrls"][0]["licenseAcquisitionUrl"]["widevine"] = constant_data.get(
                "licenseAcquisitionUrl").get("widevine")

            if count == 4:
                count = 0
            new_json =utily.create_json_file(
                sample_movie_data, f"{df['asset_id'][ind]}")
            # response = requests.request(
            #     "POST",
            #     BEACONSTAC_URL,
            #     # headers=headers,
            #     json=sample_movie_data
            # )
             
            if conut_upload > 22:
                time.sleep(2)
                headers = {
                'accept': '*/*',
                'Content-Type': 'application/json'
                }
                # url = "https://api.videoready.dev.xp.irdeto.com/metadata-ingestor/v1/metadata/ingest/vod/save?contentType=movie"

                # response = requests.request("POST", url, headers=headers, json=sample_movie_data)
                # print(response)
                

            if new_json.get("error"):
                raise ValueError(sample_movie_data.get("error"))
            print(f"Successfully file is generated : {new_json.get('data')}")

    except Exception as e:
        print(f"An error occurred during the conversion process: {e}")
