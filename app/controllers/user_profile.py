import requests
import json
import os

from fastapi import Request, APIRouter, status, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from models.request_models import IdRequestModel, UrlRequestModel

router = APIRouter()

load_dotenv()

""" environment variables """
X_AUTHORIZATION_TOKEN = os.getenv('X_AUTHORIZATION_TOKEN')
X_COOKIE_TOKEN = os.getenv('X_COOKIE_TOKEN')
X_CSRF_TOKEN = os.getenv('X_CSRF_TOKEN')
X_USER_FOLLOWING_API_ENDPOINT = os.getenv('X_USER_FOLLOWING_API_ENDPOINT')
X_USER_MEDIA_API_ENDPOINT = os.getenv('X_USER_MEDIA_API_ENDPOINT')


@router.get("/user/top-following-accounts")
async def get_user_top_following_accounts(request: Request, payload: IdRequestModel):
    user_ids = payload.user_ids
    all_following_accounts = []

    for user_id in user_ids:
        user_following_accounts = []

        variables = json.dumps({
            "userId": user_id,
            "count": 100,
            "includePromotedContent": False
        })
        features = json.dumps({
            "rweb_tipjar_consumption_enabled": True,
            "responsive_web_graphql_exclude_directive_enabled": True,
            "verified_phone_label_enabled": False,
            "creator_subscriptions_tweet_preview_api_enabled": True,
            "responsive_web_graphql_timeline_navigation_enabled": True,
            "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
            "communities_web_enable_tweet_community_results_fetch": True,
            "c9s_tweet_anatomy_moderator_badge_enabled": True,
            "articles_preview_enabled": True,
            "tweetypie_unmention_optimization_enabled": True,
            "responsive_web_edit_tweet_api_enabled": True,
            "graphql_is_translatable_rweb_tweet_is_translatable_enabled": True,
            "view_counts_everywhere_api_enabled": True,
            "longform_notetweets_consumption_enabled": True,
            "responsive_web_twitter_article_tweet_consumption_enabled": True,
            "tweet_awards_web_tipping_enabled": False,
            "creator_subscriptions_quote_tweet_preview_enabled": False,
            "freedom_of_speech_not_reach_fetch_enabled": True,
            "standardized_nudges_misinfo": True,
            "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": True,
            "rweb_video_timestamps_enabled": True,
            "longform_notetweets_rich_text_read_enabled": True,
            "longform_notetweets_inline_media_enabled": True,
            "responsive_web_enhance_cards_enabled": False
        })

        url = X_USER_FOLLOWING_API_ENDPOINT
        params = {
            "variables": variables,
            "features": features
        }
        headers = {
            "authorization": X_AUTHORIZATION_TOKEN,
            "cookie": X_COOKIE_TOKEN,
            "x-csrf-token": X_CSRF_TOKEN
        }

        try:
            response = requests.get(url, params=params, headers=headers)

            if response.status_code == 200:
                data = response.json()
                following_accounts = data["data"]["user"]["result"]["timeline"]["timeline"]["instructions"][-1]["entries"][:-2]

                for account in following_accounts:
                    user_following_accounts.append({
                        "account_id": account.get("content", None).get("itemContent", None).get("user_results", None).get("result", None).get("rest_id", None),
                        "account_name": account.get("content", None).get("itemContent", None).get("user_results", None).get("result", None).get("legacy", None).get("name", None),
                        "account_username": account.get("content", None).get("itemContent", None).get("user_results", None).get("result", None).get("legacy", None).get("screen_name", None),
                        "account_is_blue_verified": account.get("content", None).get("itemContent", None).get("user_results", None).get("result", None).get("is_blue_verified", None),
                        "account_followers_count": account.get("content", None).get("itemContent", None).get("user_results", None).get("result", None).get("legacy", None).get("followers_count", None),
                        "account_location": account.get("content", None).get("itemContent", None).get("user_results", None).get("result", None).get("legacy", None).get("location", None)
                    })

                all_following_accounts.append({
                    "user_id": user_id,
                    "following_accounts": user_following_accounts
                })
            else:
                print(f"Error: {response.status_code}")

        except Exception as e:
            print(f"Error: {e}")

    return JSONResponse(content=all_following_accounts, status_code=status.HTTP_200_OK)


@router.get("/user/get-user-medias")
async def get_user_medias(request: Request, payload: IdRequestModel):
    user_ids = payload.user_ids
    all_medias = []
    user_screen_name = None

    for user_id in user_ids:
        user_medias = []

        variables = json.dumps({"userId": user_id, "count": 100, "includePromotedContent": False,
                                "withClientEventToken": False, "withBirdwatchNotes": False, "withVoice": True, "withV2Timeline": True})
        features = json.dumps({"rweb_tipjar_consumption_enabled": True, "responsive_web_graphql_exclude_directive_enabled": True, "verified_phone_label_enabled": False, "creator_subscriptions_tweet_preview_api_enabled": True, "responsive_web_graphql_timeline_navigation_enabled": True, "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False, "communities_web_enable_tweet_community_results_fetch": True, "c9s_tweet_anatomy_moderator_badge_enabled": True, "articles_preview_enabled": True, "tweetypie_unmention_optimization_enabled": True, "responsive_web_edit_tweet_api_enabled": True, "graphql_is_translatable_rweb_tweet_is_translatable_enabled": True,
                               "view_counts_everywhere_api_enabled": True, "longform_notetweets_consumption_enabled": True, "responsive_web_twitter_article_tweet_consumption_enabled": True, "tweet_awards_web_tipping_enabled": False, "creator_subscriptions_quote_tweet_preview_enabled": False, "freedom_of_speech_not_reach_fetch_enabled": True, "standardized_nudges_misinfo": True, "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": True, "rweb_video_timestamps_enabled": True, "longform_notetweets_rich_text_read_enabled": True, "longform_notetweets_inline_media_enabled": True, "responsive_web_enhance_cards_enabled": False})
        fieldToggles = json.dumps({"withArticlePlainText": False})

        url = X_USER_MEDIA_API_ENDPOINT
        params = {"variables": variables,
                  "features": features, "fieldToggles": fieldToggles}
        headers = {"authorization": X_AUTHORIZATION_TOKEN,
                   "cookie": X_COOKIE_TOKEN, "x-csrf-token": X_CSRF_TOKEN}
        bottom_cursor = None

        try:
            while True:
                response = requests.get(url, params=params, headers=headers)

                if response.status_code == 200:
                    data = response.json()

                    if bottom_cursor is None:
                        medias = data["data"]["user"]["result"]["timeline_v2"]["timeline"][
                            "instructions"][-1]["entries"][0]["content"]["items"]
                        bottom_cursor = data["data"]["user"]["result"]["timeline_v2"][
                            "timeline"]["instructions"][-1]["entries"][-1]["content"]["value"]
                    else:
                        medias = data["data"]["user"]["result"]["timeline_v2"]["timeline"][
                            "instructions"][0]["moduleItems"]
                        bottom_cursor = data["data"]["user"]["result"]["timeline_v2"][
                            "timeline"]["instructions"][-1]["entries"][-1]["content"]["value"]

                    params["variables"] = json.dumps({"userId": user_id, "count": 100, "includePromotedContent": False,
                                                      "withClientEventToken": False, "withBirdwatchNotes": False, "withVoice": True, "withV2Timeline": True, "cursor": bottom_cursor})

                    for media in medias:
                        user_screen_name = media.get("item", None).get("itemContent", None).get(
                            "tweet_results", None).get("result", None).get("core", None).get("user_results", None).get("result", None).get("legacy", None).get("screen_name", None)

                        media = media.get("item", None).get("itemContent", None).get(
                            "tweet_results", None).get("result", None).get("legacy", None).get("entities", None).get("media", None)
                        if media is None:
                            continue

                        for media_item in media:
                            media_type = media_item.get("type", None)
                            if media_type == "animated_gif":
                                continue

                            media_url = None

                            if media_type is not None and media_type == "video":
                                media_url = media_item.get("video_info", None).get(
                                    "variants", None)[-1].get("url", None)
                            elif media_type is not None and media_type == "photo":
                                media_url = media_item.get(
                                    "media_url_https", None)

                            user_medias.append({
                                "media_type": media_type,
                                "media_url": media_url
                            })

                else:
                    print(f"Error: {response.status_code}")

        except Exception as e:
            print(f"Error: {e}")

        finally:
            all_medias.append({
                "user_screen_name": user_screen_name,
                "user_id": user_id,
                "medias": user_medias
            })

    return JSONResponse(content=all_medias, status_code=status.HTTP_200_OK)


@router.get("/user/download-user-medias")
async def download_user_medias(request: Request, payload: UrlRequestModel):
    users = payload.users

    for user in users:
        user_screen_name = user.get("user_screen_name", None)
        user_id = user.get("user_id", None)
        user_medias = user.get("medias", None)
        photo_count = 0
        video_count = 0

        for media in user_medias:
            media_type = media.get("media_type", None)
            media_url = media.get("media_url", None)
            if media_type == "photo":
                photo_count += 1
            if media_type == "video":
                video_count += 1

            try:
                response = requests.get(media_url, stream=True)

                if response.status_code == 200:
                    if not os.path.exists("medias"):
                        os.makedirs("medias")

                    if not os.path.exists(f"medias/{user_screen_name}"):
                        os.makedirs(f"medias/{user_screen_name}")
                        os.makedirs(
                            f"medias/{user_screen_name}/{user_screen_name}_X_Photos")
                        os.makedirs(
                            f"medias/{user_screen_name}/{user_screen_name}_X_Videos")

                    if media_type == "video":
                        with open(f"medias/{user_screen_name}/{user_screen_name}_X_Videos/{user_screen_name}_X_Vid_{video_count}.mp4", "wb") as file:
                            for chunk in response.iter_content(chunk_size=1024):
                                file.write(chunk)
                    elif media_type == "photo":
                        with open(f"medias/{user_screen_name}/{user_screen_name}_X_Photos/{user_screen_name}_X_Pic_{photo_count}.jpg", "wb") as file:
                            file.write(response.content)

            except Exception as e:
                print(f"Error: {e}")

    return JSONResponse(content={"message": "Medias downloaded successfully"}, status_code=status.HTTP_200_OK)
